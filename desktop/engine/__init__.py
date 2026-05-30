"""Shared conversion engine — router and dispatcher.

Maps (source_ext, target_ext) tuples to handler functions.
"""

from .document import pdf_to_docx, docx_to_pdf, md_to_html, md_to_pdf, pptx_to_pdf, epub_to_pdf, mobi_to_epub
from .image    import heic_to_jpg, webp_to_png, webp_to_jpg, png_to_jpg, svg_to_png, tiff_to_jpg, tiff_to_pdf, gif_to_mp4
from .video    import mp4_to_mp3, mov_to_mp4, mkv_to_mp4, webm_to_mp4
from .audio    import wav_to_mp3, m4a_to_mp3
from .data     import csv_to_xlsx, pdf_to_xlsx, json_to_csv, xml_to_json, yaml_to_json
from .security import pem_to_pfx, pem_to_crt
from .font     import ttf_to_woff2, otf_to_woff2
from .archive  import rar_to_zip
from .cad      import dwg_to_pdf
from typing import Callable, Dict, Tuple

CONVERSION_MAP: Dict[Tuple[str, str], Callable] = {
    ("pdf",  "docx"): pdf_to_docx,
    ("docx", "pdf"):  docx_to_pdf,
    ("heic", "jpg"):  heic_to_jpg,
    ("webp", "png"):  webp_to_png,
    ("webp", "jpg"):  webp_to_jpg,
    ("png",  "jpg"):  png_to_jpg,
    ("mp4",  "mp3"):  mp4_to_mp3,
    ("mov",  "mp4"):  mov_to_mp4,
    ("csv",  "xlsx"): csv_to_xlsx,
    ("pdf",  "xlsx"): pdf_to_xlsx,
    ("svg",  "png"):  svg_to_png,
    ("mkv",  "mp4"):  mkv_to_mp4,
    ("epub", "pdf"):  epub_to_pdf,
    ("json", "csv"):  json_to_csv,
    ("wav",  "mp3"):  wav_to_mp3,
    ("pptx", "pdf"):  pptx_to_pdf,
    ("xml",  "json"): xml_to_json,
    ("gif",  "mp4"):  gif_to_mp4,
    ("webm", "mp4"):  webm_to_mp4,
    ("m4a",  "mp3"):  m4a_to_mp3,
    ("md",   "html"): md_to_html,
    ("md",   "pdf"):  md_to_pdf,
    ("ttf",  "woff2"): ttf_to_woff2,
    ("otf",  "woff2"): otf_to_woff2,
    ("pem",  "pfx"):  pem_to_pfx,
    ("pem",  "crt"):  pem_to_crt,
    ("yaml", "json"): yaml_to_json,
    ("mobi", "epub"): mobi_to_epub,
    ("tiff", "jpg"):  tiff_to_jpg,
    ("tiff", "pdf"):  tiff_to_pdf,
    ("rar",  "zip"):  rar_to_zip,
    ("dwg",  "pdf"):  dwg_to_pdf,
}


def convert(data: bytes, source_fmt: str, target_fmt: str, is_web: bool = False) -> bytes:
    """Main conversion dispatcher.

    Args:
        data: Raw file bytes.
        source_fmt: Source file extension (e.g. "png").
        target_fmt: Target file extension (e.g. "jpg").
        is_web: If True, enforces web file size limits.

    Returns:
        Converted file as bytes.

    Raises:
        ValueError: If conversion pair is unsupported.
    """
    key = (source_fmt.lower(), target_fmt.lower())
    handler = CONVERSION_MAP.get(key)
    if not handler:
        raise ValueError(f"Unsupported conversion: {source_fmt} → {target_fmt}")
        
    # ISS-003: Connect is_web parameter down to handler functions and validator gates
    return handler(data, is_web=is_web)
