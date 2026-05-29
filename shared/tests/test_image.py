import pytest
from engine.image import png_to_jpg, webp_to_png, webp_to_jpg, heic_to_jpg, svg_to_png, tiff_to_jpg, tiff_to_pdf

def test_png_to_jpg(sample_png):
    result = png_to_jpg(sample_png)
    assert result.startswith(b'\xff\xd8\xff')  # JPEG magic bytes

def test_webp_to_png(sample_webp):
    result = webp_to_png(sample_webp)
    assert result.startswith(b'\x89PNG\r\n\x1a\n')  # PNG magic bytes

def test_webp_to_jpg(sample_webp):
    result = webp_to_jpg(sample_webp)
    assert result.startswith(b'\xff\xd8\xff')

def test_svg_to_png(sample_svg):
    result = svg_to_png(sample_svg)
    assert result.startswith(b'\x89PNG\r\n\x1a\n')

def test_tiff_to_jpg(sample_tiff):
    result = tiff_to_jpg(sample_tiff)
    assert result.startswith(b'\xff\xd8\xff')

def test_tiff_to_pdf(sample_tiff):
    result = tiff_to_pdf(sample_tiff)
    assert result.startswith(b'%PDF-')
