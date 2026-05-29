"""Document conversion module.

Handles: pdf→docx, docx→pdf, md→html, md→pdf, pptx→pdf, epub→pdf, mobi→epub
"""

import subprocess
import tempfile
import os
from pathlib import Path
from .validator import validate


def pdf_to_docx(data: bytes, is_web: bool = False) -> bytes:
    validate(data, "pdf", is_web=is_web)
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.pdf"
        dst = Path(tmp) / "output.docx"
        src.write_bytes(data)
        from pdf2docx import Converter
        cv = Converter(str(src))
        cv.convert(str(dst), start=0, end=None)
        cv.close()
        return dst.read_bytes()


def docx_to_pdf(data: bytes, is_web: bool = False) -> bytes:
    """Uses LibreOffice Portable (desktop-only path). Set LO_BIN env var."""
    validate(data, "docx", is_web=is_web)
    if is_web:
        raise ValueError("docx→pdf is a premium feature and requires LibreOffice. Please use the Desktop app.")
    lo_bin = os.environ.get("LO_BIN", "soffice")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.docx"
        src.write_bytes(data)
        # ISS-019: Strict 45s timeout gate prevents infinite hangs
        subprocess.run(
            [lo_bin, "--headless", "--invisible", "--convert-to", "pdf",
             "--outdir", tmp, str(src)],
            check=True,
            timeout=45,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        out = Path(tmp) / "input.pdf"
        return out.read_bytes()


def md_to_html(data: bytes, is_web: bool = False) -> bytes:
    validate(data, "md", is_web=is_web)
    import markdown
    html = markdown.markdown(data.decode("utf-8"), extensions=["tables", "fenced_code"])
    return html.encode("utf-8")


def md_to_pdf(data: bytes, is_web: bool = False) -> bytes:
    validate(data, "md", is_web=is_web)
    if is_web:
        raise ValueError("md→pdf requires system binary libraries (WeasyPrint). Please download the Desktop app.")
    with tempfile.TemporaryDirectory() as tmp:
        html_bytes = md_to_html(data, is_web=is_web)
        src = Path(tmp) / "input.html"
        dst = Path(tmp) / "output.pdf"
        src.write_bytes(html_bytes)
        from weasyprint import HTML
        HTML(filename=str(src)).write_pdf(str(dst))
        return dst.read_bytes()


def pptx_to_pdf(data: bytes, is_web: bool = False) -> bytes:
    """LibreOffice Portable (desktop-only). Set LO_BIN env var."""
    validate(data, "pptx", is_web=is_web)
    if is_web:
        raise ValueError("pptx→pdf conversion is desktop-only.")
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


def epub_to_pdf(data: bytes, is_web: bool = False) -> bytes:
    validate(data, "epub", is_web=is_web)
    if is_web:
        raise ValueError("epub→pdf requires WeasyPrint and is desktop-only.")
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


def mobi_to_epub(data: bytes, is_web: bool = False) -> bytes:
    """Unpacks MOBI and repackages to EPUB (desktop only)."""
    validate(data, "mobi", is_web=is_web)
    if is_web:
        raise ValueError("MOBI conversions are premium desktop-only features.")
    import mobi
    import shutil
    with tempfile.TemporaryDirectory() as tmp_dir:
        input_file = Path(tmp_dir) / "input.mobi"
        input_file.write_bytes(data)
        # Unpack Kindle MOBI file programmatically
        extracted_dir, filepath = mobi.extract(str(input_file))
        try:
            out_path = Path(filepath)
            if out_path.exists():
                return out_path.read_bytes()
            else:
                raise ValueError("MOBI Unpacker failed to extract a valid EPUB structure.")
        finally:
            if os.path.exists(extracted_dir):
                shutil.rmtree(extracted_dir)
