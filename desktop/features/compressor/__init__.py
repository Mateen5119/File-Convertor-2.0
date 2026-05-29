"""Compressor feature package – PDF and Image compression widgets.

Exports ``CompressorWidget``, a QTabWidget that holds both the PDF and
Image compression tabs.
"""

from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QTabWidget, QWidget

from .pdf_compress import PDFCompressWidget
from .img_compress import ImageCompressWidget


class CompressorWidget(QTabWidget):
    """Tab container for all compression tools.

    Tabs
    ----
    * **PDF** – Compress PDF files via pikepdf.
    * **Image** – Compress JPEG / PNG / WebP / TIFF images via Pillow.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("glassCard")

        # PDF tab
        self._pdf_tab = PDFCompressWidget()
        self.addTab(self._pdf_tab, "📄  PDF")

        # Image tab
        self._img_tab = ImageCompressWidget()
        self.addTab(self._img_tab, "🖼️  Image")


__all__ = ["CompressorWidget", "PDFCompressWidget", "ImageCompressWidget"]
