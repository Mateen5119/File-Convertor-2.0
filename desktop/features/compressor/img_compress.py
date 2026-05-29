"""Image Compressor widget – reduce image file size with Pillow.

Supports JPEG, PNG, WebP, and TIFF. Falls back gracefully when Pillow is
not installed.
"""

from __future__ import annotations

import io
import os
import tempfile
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QImage
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
    from PIL import Image as PILImage
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


# ---------------------------------------------------------------------------
# Constants – Stitch design tokens
# ---------------------------------------------------------------------------
_SURFACE = "#131315"
_ON_SURFACE = "#e4e2e4"
_PRIMARY = "#adc6ff"
_TERTIARY = "#47e266"
_ERROR = "#ffb4ab"
_OUTLINE = "#8b90a0"

_SUPPORTED_FILTERS = "Images (*.jpg *.jpeg *.png *.webp *.tiff *.tif)"
_THUMB_MAX = QSize(360, 360)


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
    """Compresses an image in a background thread using Pillow."""

    finished = pyqtSignal(str, int)  # output_path, compressed_size
    error = pyqtSignal(str)

    def __init__(
        self,
        input_path: str,
        output_path: str,
        quality: int,  # 1-100
    ) -> None:
        super().__init__()
        self._input_path = input_path
        self._output_path = output_path
        self._quality = quality

    def run(self) -> None:
        try:
            img = PILImage.open(self._input_path)

            # Determine output format from extension
            ext = Path(self._output_path).suffix.lower()
            save_kwargs: dict = {}

            if ext in (".jpg", ".jpeg"):
                fmt = "JPEG"
                save_kwargs["quality"] = self._quality
                save_kwargs["optimize"] = True
                # Convert RGBA → RGB for JPEG
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
            elif ext == ".png":
                fmt = "PNG"
                # PNG uses compress_level 0-9 (inverse of quality)
                compress = max(0, min(9, 9 - int(self._quality / 11)))
                save_kwargs["compress_level"] = compress
                save_kwargs["optimize"] = True
            elif ext == ".webp":
                fmt = "WEBP"
                save_kwargs["quality"] = self._quality
                save_kwargs["method"] = 6  # best compression
            elif ext in (".tiff", ".tif"):
                fmt = "TIFF"
                save_kwargs["compression"] = "tiff_deflate"
            else:
                fmt = "JPEG"
                save_kwargs["quality"] = self._quality
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

            img.save(self._output_path, format=fmt, **save_kwargs)
            compressed_size = os.path.getsize(self._output_path)
            self.finished.emit(self._output_path, compressed_size)
        except Exception as e:
            self.error.emit(str(e))


# ---------------------------------------------------------------------------
# Main widget
# ---------------------------------------------------------------------------
class ImageCompressWidget(QWidget):
    """Image compression panel with preview, quality slider, and size stats."""

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
        if not HAS_PILLOW:
            banner = QLabel(
                "⚠️  Pillow is not installed. Run  pip install Pillow  to enable image compression."
            )
            banner.setObjectName("labelError")
            banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
            banner.setWordWrap(True)
            root.addWidget(banner)
            return

        # Title
        title = QLabel("Image Compressor")
        title.setObjectName("labelPrimary")
        title.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {_PRIMARY};")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        root.addWidget(title)

        # --- File picker group ---
        file_group = QGroupBox("Select Image")
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

        # --- Preview ---
        preview_group = QGroupBox("Preview")
        preview_group.setObjectName("glassCardRow")
        pg_layout = QVBoxLayout(preview_group)

        self._preview = QLabel("No image loaded")
        self._preview.setObjectName("labelOutline")
        self._preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._preview.setMinimumHeight(200)
        self._preview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        pg_layout.addWidget(self._preview)

        self._dimensions_label = QLabel("")
        self._dimensions_label.setObjectName("labelOutline")
        self._dimensions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pg_layout.addWidget(self._dimensions_label)

        root.addWidget(preview_group)

        # --- Quality slider ---
        quality_group = QGroupBox("Quality")
        quality_group.setObjectName("glassCardRow")
        qg_layout = QVBoxLayout(quality_group)

        slider_row = QHBoxLayout()
        lbl_low = QLabel("1")
        lbl_low.setObjectName("labelOutline")
        slider_row.addWidget(lbl_low)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setMinimum(1)
        self._slider.setMaximum(100)
        self._slider.setValue(75)
        self._slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._slider.setTickInterval(10)
        self._slider.valueChanged.connect(self._on_slider_changed)
        slider_row.addWidget(self._slider)

        lbl_high = QLabel("100")
        lbl_high.setObjectName("labelOutline")
        slider_row.addWidget(lbl_high)

        qg_layout.addLayout(slider_row)

        self._quality_label = QLabel("Quality: 75%")
        self._quality_label.setObjectName("labelPrimary")
        self._quality_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qg_layout.addWidget(self._quality_label)

        root.addWidget(quality_group)

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

    # ---- Slots -------------------------------------------------------------

    def _on_slider_changed(self, value: int) -> None:
        self._quality_label.setText(f"Quality: {value}%")

    def _browse_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", _SUPPORTED_FILTERS
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
        self._load_preview(path)

    def _load_preview(self, path: str) -> None:
        """Load a thumbnail preview of the selected image."""
        try:
            pm = QPixmap(path)
            if pm.isNull():
                self._preview.setText("Unable to preview this image")
                self._dimensions_label.setText("")
                return
            self._dimensions_label.setText(f"{pm.width()} × {pm.height()} px")
            scaled = pm.scaled(
                _THUMB_MAX,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self._preview.setPixmap(scaled)
        except Exception:
            self._preview.setText("Unable to preview this image")
            self._dimensions_label.setText("")

    def _compress(self) -> None:
        if not self._input_path:
            return

        # Suggest same extension as input
        ext = Path(self._input_path).suffix
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Compressed Image",
            "",
            f"Image (*{ext});;JPEG (*.jpg);;PNG (*.png);;WebP (*.webp);;TIFF (*.tiff)",
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
        QMessageBox.critical(self, "Compression Error", f"Failed to compress image:\n{message}")
