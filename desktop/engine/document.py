"""Document conversion module.

Handles: pdf→docx, docx→pdf, md→html, md→pdf, pptx→pdf, epub→pdf, mobi→epub
"""

import subprocess
import tempfile
import os
from pathlib import Path
from .validator import validate


def pdf_to_docx(data: bytes) -> bytes:
    validate(data, "pdf")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.pdf"
        dst = Path(tmp) / "output.docx"
        src.write_bytes(data)
        from pdf2docx import Converter
        cv = Converter(str(src))
        cv.convert(str(dst), start=0, end=None)
        cv.close()
        return dst.read_bytes()


def docx_to_pdf(data: bytes) -> bytes:
    """Uses LibreOffice Portable (desktop-only path). Set LO_BIN env var."""
    validate(data, "docx")
    lo_bin = os.environ.get("LO_BIN", "soffice")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.docx"
        src.write_bytes(data)
        subprocess.run(
            [lo_bin, "--headless", "--invisible", "--convert-to", "pdf",
             "--outdir", tmp, str(src)],
            check=True,
            timeout=45,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        out = Path(tmp) / "input.pdf"
        return out.read_bytes()


def md_to_html(data: bytes) -> bytes:
    validate(data, "md")
    import markdown
    html = markdown.markdown(data.decode("utf-8"), extensions=["tables", "fenced_code"])
    return html.encode("utf-8")


def md_to_pdf(data: bytes) -> bytes:
    validate(data, "md")
    with tempfile.TemporaryDirectory() as tmp:
        html_bytes = md_to_html(data)
        src = Path(tmp) / "input.html"
        dst = Path(tmp) / "output.pdf"
        src.write_bytes(html_bytes)
        from weasyprint import HTML
        HTML(filename=str(src)).write_pdf(str(dst))
        return dst.read_bytes()


def pptx_to_pdf(data: bytes) -> bytes:
    """LibreOffice Portable (desktop-only). Set LO_BIN env var."""
    validate(data, "pptx")
    lo_bin = os.environ.get("LO_BIN", "soffice")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.pptx"
        src.write_bytes(data)
        subprocess.run(
            [lo_bin, "--headless", "--invisible", "--convert-to", "pdf",
             "--outdir", tmp, str(src)],
            check=True, timeout=45,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        return (Path(tmp) / "input.pdf").read_bytes()


def epub_to_pdf(data: bytes) -> bytes:
    validate(data, "epub")
    with tempfile.TemporaryDirectory() as tmp:
        from ebooklib import epub
        from weasyprint import HTML
        # Write epub to file first since ebooklib needs a file path
        epub_path = Path(tmp) / "input.epub"
        epub_path.write_bytes(data)
        book = epub.read_epub(str(epub_path))
        html_parts = []
        for item in book.get_items_of_type(9):  # ITEM_DOCUMENT = 9
            html_parts.append(item.get_content().decode("utf-8", errors="ignore"))
        combined = "\n".join(html_parts)
        dst = Path(tmp) / "output.pdf"
        HTML(string=combined).write_pdf(str(dst))
        return dst.read_bytes()


def mobi_to_epub(data: bytes) -> bytes:
    raise NotImplementedError("mobi→epub requires KindleUnpack — desktop only, no DRM support")
