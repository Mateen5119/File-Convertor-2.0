"""PDF Compressor widget – reduce PDF file size with pikepdf.

Uses pikepdf for stream-level compression and optimisation.
Falls back gracefully when the library is not installed.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QSizePolicy,
    QGroupBox,
)

# ---------------------------------------------------------------------------
# Graceful import
# ---------------------------------------------------------------------------
try:
    import pikepdf
    HAS_PIKEPDF = True
except ImportError:
    HAS_PIKEPDF = False


# ---------------------------------------------------------------------------
# Constants – Stitch design tokens
# ---------------------------------------------------------------------------
_SURFACE = "#131315"
_ON_SURFACE = "#e4e2e4"
_PRIMARY = "#adc6ff"
_TERTIARY = "#47e266"
_ERROR = "#ffb4ab"
_OUTLINE = "#8b90a0"


def _human_size(size_bytes: int) -> str:
    """Return a human-readable file size string."""
    for unit in ("B", "KB", "MB", "GB"):
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


# ---------------------------------------------------------------------------
# Compression worker
# ---------------------------------------------------------------------------
class _CompressWorker(QThread):
    """Compresses a PDF using pikepdf in a background thread."""

    finished = pyqtSignal(str, int)  # output_path, compressed_size
    error = pyqtSignal(str)

    # compression_level maps to pikepdf's object-stream mode and linearization
    def __init__(
        self,
        input_path: str,
        output_path: str,
        compression_level: int,  # 1-10
    ) -> None:
        super().__init__()
        self._input_path = input_path
        self._output_path = output_path
        self._level = compression_level

    def run(self) -> None:
        try:
            pdf = pikepdf.open(self._input_path)

            # Apply stream-level compression based on level
            # Level 1-3: light (preserve_pdfa, no object streams)
            # Level 4-7: medium (object streams, remove unreferenced)
            # Level 8-10: aggressive (recompress all, linearize)
            save_kwargs: dict = {}

            if self._level <= 3:
                save_kwargs["object_stream_mode"] = pikepdf.ObjectStreamMode.disable
                save_kwargs["compress_streams"] = True
                save_kwargs["recompress_flate"] = False
            elif self._level <= 7:
                save_kwargs["object_stream_mode"] = pikepdf.ObjectStreamMode.generate
                save_kwargs["compress_streams"] = True
                save_kwargs["recompress_flate"] = True
            else:
                save_kwargs["object_stream_mode"] = pikepdf.ObjectStreamMode.generate
                save_kwargs["compress_streams"] = True
                save_kwargs["recompress_flate"] = True
                save_kwargs["linearize"] = True

            # Always remove unused resources
            save_kwargs["fix_metadata_version"] = False

            pdf.remove_unreferenced_resources()
            pdf.save(self._output_path, **save_kwargs)
            pdf.close()

            compressed_size = os.path.getsize(self._output_path)
            self.finished.emit(self._output_path, compressed_size)
        except Exception as e:
            self.error.emit(str(e))


# ---------------------------------------------------------------------------
# Main widget
# ---------------------------------------------------------------------------
class PDFCompressWidget(QWidget):
    """PDF compression panel with file picker, level slider, and size stats."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("glassCard")
        self._input_path: Optional[str] = None
        self._input_size: int = 0
        self._workers: list[QThread] = []
        self._build_ui()

    # ---- UI Construction ---------------------------------------------------

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(14)

        # Dependency banner
        if not HAS_PIKEPDF:
            banner = QLabel(
                "⚠️  pikepdf is not installed. Run  pip install pikepdf  to enable PDF compression."
            )
            banner.setObjectName("labelError")
            banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
            banner.setWordWrap(True)
            root.addWidget(banner)
            return

        # Title
        title = QLabel("PDF Compressor")
        title.setObjectName("labelPrimary")
        title.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {_PRIMARY};")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        root.addWidget(title)

        # --- File picker group ---
        file_group = QGroupBox("Select PDF")
        file_group.setObjectName("glassCardRow")
        fg_layout = QHBoxLayout(file_group)

        self._file_label = QLabel("No file selected")
        self._file_label.setObjectName("labelOutline")
        self._file_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        fg_layout.addWidget(self._file_label)

        btn_browse = QPushButton("Browse…")
        btn_browse.setObjectName("primaryBtn")
        btn_browse.clicked.connect(self._browse_file)
        fg_layout.addWidget(btn_browse)

        root.addWidget(file_group)

        # --- Compression level ---
        level_group = QGroupBox("Compression Level")
        level_group.setObjectName("glassCardRow")
        lg_layout = QVBoxLayout(level_group)

        slider_row = QHBoxLayout()
        lbl_light = QLabel("Light")
        lbl_light.setObjectName("labelOutline")
        slider_row.addWidget(lbl_light)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setMinimum(1)
        self._slider.setMaximum(10)
        self._slider.setValue(5)
        self._slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._slider.setTickInterval(1)
        self._slider.valueChanged.connect(self._on_slider_changed)
        slider_row.addWidget(self._slider)

        lbl_heavy = QLabel("Aggressive")
        lbl_heavy.setObjectName("labelOutline")
        slider_row.addWidget(lbl_heavy)

        lg_layout.addLayout(slider_row)

        self._level_label = QLabel("Level: 5 / 10")
        self._level_label.setObjectName("labelPrimary")
        self._level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lg_layout.addWidget(self._level_label)

        root.addWidget(level_group)

        # --- Size display ---
        size_group = QGroupBox("File Size")
        size_group.setObjectName("glassCardRow")
        sg_layout = QHBoxLayout(size_group)

        self._before_label = QLabel("Before: —")
        self._before_label.setObjectName("labelOutline")
        sg_layout.addWidget(self._before_label)

        self._after_label = QLabel("After: —")
        self._after_label.setObjectName("labelTertiary")
        sg_layout.addWidget(self._after_label)

        self._savings_label = QLabel("")
        self._savings_label.setObjectName("labelPrimary")
        sg_layout.addWidget(self._savings_label)

        root.addWidget(size_group)

        # --- Progress ---
        self._progress = QProgressBar()
        self._progress.setRange(0, 0)  # indeterminate
        self._progress.setVisible(False)
        root.addWidget(self._progress)

        # --- Action buttons ---
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self._btn_compress = QPushButton("🗜️  Compress")
        self._btn_compress.setObjectName("primaryBtn")
        self._btn_compress.setEnabled(False)
        self._btn_compress.clicked.connect(self._compress)
        btn_row.addWidget(self._btn_compress)

        root.addLayout(btn_row)
        root.addStretch()

    # ---- Slots -------------------------------------------------------------

    def _on_slider_changed(self, value: int) -> None:
        self._level_label.setText(f"Level: {value} / 10")

    def _browse_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF", "", "PDF Files (*.pdf)"
        )
        if not path:
            return
        self._input_path = path
        self._input_size = os.path.getsize(path)
        self._file_label.setText(Path(path).name)
        self._before_label.setText(f"Before: {_human_size(self._input_size)}")
        self._after_label.setText("After: —")
        self._savings_label.setText("")
        self._btn_compress.setEnabled(True)

    def _compress(self) -> None:
        if not self._input_path:
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Compressed PDF", "", "PDF Files (*.pdf)"
        )
        if not save_path:
            return

        self._btn_compress.setEnabled(False)
        self._progress.setVisible(True)

        worker = _CompressWorker(
            self._input_path,
            save_path,
            self._slider.value(),
        )
        worker.finished.connect(self._on_compress_finished)
        worker.error.connect(self._on_compress_error)
        self._workers.append(worker)
        worker.start()

    def _on_compress_finished(self, output_path: str, compressed_size: int) -> None:
        self._progress.setVisible(False)
        self._btn_compress.setEnabled(True)
        self._after_label.setText(f"After: {_human_size(compressed_size)}")

        if self._input_size > 0:
            pct = (1 - compressed_size / self._input_size) * 100
            if pct > 0:
                self._savings_label.setText(f"Saved {pct:.1f}%  ✓")
                self._savings_label.setObjectName("labelTertiary")
            else:
                self._savings_label.setText("No size reduction")
                self._savings_label.setObjectName("labelOutline")
            self._savings_label.style().unpolish(self._savings_label)
            self._savings_label.style().polish(self._savings_label)

    def _on_compress_error(self, message: str) -> None:
        self._progress.setVisible(False)
        self._btn_compress.setEnabled(True)
        QMessageBox.critical(self, "Compression Error", f"Failed to compress PDF:\n{message}")
