"""PDF Editor widget – view, reorder, rotate, and delete pages.

Uses PyMuPDF (fitz) for PDF manipulation. Falls back gracefully when the
library is not installed.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QImage, QIcon, QAction
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QToolBar,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QFileDialog,
    QMessageBox,
    QSplitter,
    QComboBox,
    QSizePolicy,
    QAbstractItemView,
)

# ---------------------------------------------------------------------------
# Graceful import
# ---------------------------------------------------------------------------
try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False


# ---------------------------------------------------------------------------
# Constants – Stitch design tokens
# ---------------------------------------------------------------------------
_SURFACE = "#131315"
_ON_SURFACE = "#e4e2e4"
_PRIMARY = "#adc6ff"
_TERTIARY = "#47e266"
_ERROR = "#ffb4ab"
_OUTLINE = "#8b90a0"
_THUMB_SIZE = QSize(140, 200)
_PREVIEW_DPI = 150
_THUMB_DPI = 72


# ---------------------------------------------------------------------------
# Worker: render thumbnails in background
# ---------------------------------------------------------------------------
class _ThumbnailWorker(QThread):
    """Renders page thumbnails off the main thread."""

    thumbnails_ready = pyqtSignal(list)  # list[(int, QPixmap)]

    def __init__(self, pdf_path: str, dpi: int = _THUMB_DPI) -> None:
        super().__init__()
        self._pdf_path = pdf_path
        self._dpi = dpi

    def run(self) -> None:
        if not HAS_FITZ:
            return
        try:
            doc = fitz.open(self._pdf_path)
            results: list[tuple[int, QPixmap]] = []
            for i in range(len(doc)):
                page = doc[i]
                mat = fitz.Matrix(self._dpi / 72, self._dpi / 72)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                qimg = QImage(
                    pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888
                )
                results.append((i, QPixmap.fromImage(qimg)))
            doc.close()
            self.thumbnails_ready.emit(results)
        except Exception:
            self.thumbnails_ready.emit([])


# ---------------------------------------------------------------------------
# Worker: save PDF (may be slow for large files)
# ---------------------------------------------------------------------------
class _SaveWorker(QThread):
    """Saves the modified PDF to disk in a background thread."""

    finished = pyqtSignal(str)  # saved path
    error = pyqtSignal(str)

    def __init__(self, doc_bytes: bytes, save_path: str) -> None:
        super().__init__()
        self._doc_bytes = doc_bytes
        self._save_path = save_path

    def run(self) -> None:
        try:
            with open(self._save_path, "wb") as f:
                f.write(self._doc_bytes)
            self.finished.emit(self._save_path)
        except Exception as e:
            self.error.emit(str(e))


# ---------------------------------------------------------------------------
# Main widget
# ---------------------------------------------------------------------------
class PDFEditorWidget(QWidget):
    """A page-level PDF editor with thumbnail sidebar and page preview."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("glassCard")
        self._doc: Optional["fitz.Document"] = None
        self._current_path: Optional[str] = None
        self._workers: list[QThread] = []
        self._build_ui()

    # ---- UI Construction ---------------------------------------------------

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # Dependency-missing banner
        if not HAS_FITZ:
            banner = QLabel(
                "⚠️  PyMuPDF is not installed. Run  pip install pymupdf  to enable PDF editing."
            )
            banner.setObjectName("labelError")
            banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
            banner.setWordWrap(True)
            root.addWidget(banner)
            return

        # Toolbar
        self._toolbar = self._create_toolbar()
        root.addWidget(self._toolbar)

        # Splitter: thumbnails | preview
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setObjectName("glassCardRow")

        # -- Thumbnail sidebar -----------------------------------------------
        self._thumb_list = QListWidget()
        self._thumb_list.setObjectName("glassCard")
        self._thumb_list.setIconSize(_THUMB_SIZE)
        self._thumb_list.setViewMode(QListWidget.ViewMode.IconMode)
        self._thumb_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self._thumb_list.setMovement(QListWidget.Movement.Static)
        self._thumb_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._thumb_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self._thumb_list.setSpacing(6)
        self._thumb_list.setMinimumWidth(170)
        self._thumb_list.setMaximumWidth(220)
        self._thumb_list.currentRowChanged.connect(self._on_page_selected)
        splitter.addWidget(self._thumb_list)

        # -- Preview panel ---------------------------------------------------
        preview_container = QWidget()
        preview_container.setObjectName("glassCard")
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(8, 8, 8, 8)

        self._preview_label = QLabel("Open a PDF to get started")
        self._preview_label.setObjectName("labelOutline")
        self._preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._preview_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        preview_layout.addWidget(self._preview_label)

        self._page_info = QLabel("")
        self._page_info.setObjectName("labelPrimary")
        self._page_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self._page_info)

        splitter.addWidget(preview_container)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        root.addWidget(splitter)

    def _create_toolbar(self) -> QToolBar:
        tb = QToolBar("PDF Editor")
        tb.setMovable(False)
        tb.setObjectName("glassCardRow")

        self._act_open = tb.addAction("📂 Open")
        self._act_open.triggered.connect(self._open_file)

        self._act_save = tb.addAction("💾 Save")
        self._act_save.setEnabled(False)
        self._act_save.triggered.connect(self._save_file)

        tb.addSeparator()

        self._act_delete = tb.addAction("🗑️ Delete Page")
        self._act_delete.setEnabled(False)
        self._act_delete.triggered.connect(self._delete_page)

        tb.addSeparator()

        # Rotation combo
        rot_label = QLabel("  Rotate: ")
        rot_label.setObjectName("labelOutline")
        tb.addWidget(rot_label)

        self._rot_combo = QComboBox()
        self._rot_combo.addItems(["90°", "180°", "270°"])
        self._rot_combo.setObjectName("glassCard")
        tb.addWidget(self._rot_combo)

        self._act_rotate = tb.addAction("🔄 Rotate")
        self._act_rotate.setEnabled(False)
        self._act_rotate.triggered.connect(self._rotate_page)

        tb.addSeparator()

        self._act_move_up = tb.addAction("⬆️ Move Up")
        self._act_move_up.setEnabled(False)
        self._act_move_up.triggered.connect(self._move_page_up)

        self._act_move_down = tb.addAction("⬇️ Move Down")
        self._act_move_down.setEnabled(False)
        self._act_move_down.triggered.connect(self._move_page_down)

        return tb

    # ---- Actions -----------------------------------------------------------

    def _set_editing_enabled(self, enabled: bool) -> None:
        for act in (
            self._act_save,
            self._act_delete,
            self._act_rotate,
            self._act_move_up,
            self._act_move_down,
        ):
            act.setEnabled(enabled)

    def _open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Open PDF", "", "PDF Files (*.pdf)"
        )
        if not path:
            return
        self._load_pdf(path)

    def _load_pdf(self, path: str) -> None:
        try:
            self._doc = fitz.open(path)
            self._current_path = path
            self._set_editing_enabled(True)
            self._refresh_thumbnails()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open PDF:\n{e}")

    def _refresh_thumbnails(self) -> None:
        self._thumb_list.clear()
        if self._doc is None:
            return
        # Render in-memory (fast enough for moderate docs; worker for very large)
        for i in range(len(self._doc)):
            page = self._doc[i]
            mat = fitz.Matrix(_THUMB_DPI / 72, _THUMB_DPI / 72)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            qimg = QImage(
                pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888
            )
            pm = QPixmap.fromImage(qimg)
            item = QListWidgetItem(QIcon(pm), f"Page {i + 1}")
            item.setSizeHint(QSize(_THUMB_SIZE.width() + 10, _THUMB_SIZE.height() + 28))
            item.setData(Qt.ItemDataRole.UserRole, i)
            self._thumb_list.addItem(item)
        if self._thumb_list.count():
            self._thumb_list.setCurrentRow(0)

    def _on_page_selected(self, row: int) -> None:
        if self._doc is None or row < 0 or row >= len(self._doc):
            return
        page = self._doc[row]
        mat = fitz.Matrix(_PREVIEW_DPI / 72, _PREVIEW_DPI / 72)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        qimg = QImage(
            pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888
        )
        pm = QPixmap.fromImage(qimg)

        # Scale to fit preview area
        available = self._preview_label.size()
        scaled = pm.scaled(
            available,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._preview_label.setPixmap(scaled)
        self._page_info.setText(f"Page {row + 1} of {len(self._doc)}")

    def _delete_page(self) -> None:
        row = self._thumb_list.currentRow()
        if self._doc is None or row < 0:
            return
        if len(self._doc) <= 1:
            QMessageBox.warning(self, "Cannot Delete", "A PDF must have at least one page.")
            return
        reply = QMessageBox.question(
            self,
            "Delete Page",
            f"Delete page {row + 1}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._doc.delete_page(row)
            self._refresh_thumbnails()

    def _rotate_page(self) -> None:
        row = self._thumb_list.currentRow()
        if self._doc is None or row < 0:
            return
        angle_map = {"90°": 90, "180°": 180, "270°": 270}
        angle = angle_map.get(self._rot_combo.currentText(), 90)
        page = self._doc[row]
        page.set_rotation((page.rotation + angle) % 360)
        self._refresh_thumbnails()
        self._thumb_list.setCurrentRow(row)

    def _move_page_up(self) -> None:
        row = self._thumb_list.currentRow()
        if self._doc is None or row <= 0:
            return
        self._doc.move_page(row, row - 1)
        self._refresh_thumbnails()
        self._thumb_list.setCurrentRow(row - 1)

    def _move_page_down(self) -> None:
        row = self._thumb_list.currentRow()
        if self._doc is None or row < 0 or row >= len(self._doc) - 1:
            return
        self._doc.move_page(row, row + 2)
        self._refresh_thumbnails()
        self._thumb_list.setCurrentRow(row + 1)

    def _save_file(self) -> None:
        if self._doc is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", self._current_path or "", "PDF Files (*.pdf)"
        )
        if not path:
            return
        try:
            doc_bytes = self._doc.tobytes(garbage=4, deflate=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to serialise PDF:\n{e}")
            return

        worker = _SaveWorker(doc_bytes, path)
        worker.finished.connect(lambda p: self._on_save_finished(p))
        worker.error.connect(lambda e: QMessageBox.critical(self, "Save Error", e))
        self._workers.append(worker)
        worker.start()

    def _on_save_finished(self, path: str) -> None:
        self._current_path = path
        self._page_info.setText(f"Saved  ✓  {Path(path).name}")

    # ---- Public API --------------------------------------------------------

    def load(self, path: str) -> None:
        """Programmatically open a PDF file."""
        if HAS_FITZ:
            self._load_pdf(path)
