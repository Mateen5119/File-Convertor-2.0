import pytest
from engine.document import md_to_html, md_to_pdf, pdf_to_docx, docx_to_pdf, pptx_to_pdf, epub_to_pdf, mobi_to_epub
import shutil

def test_md_to_html(sample_md):
    result = md_to_html(sample_md)
    assert b"<h1>Test</h1>" in result

def test_md_to_pdf(sample_md):
    result = md_to_pdf(sample_md)
    assert result.startswith(b'%PDF-')

def test_pdf_to_docx(sample_pdf):
    result = pdf_to_docx(sample_pdf)
    assert result.startswith(b'PK\x03\x04')

@pytest.mark.skipif(shutil.which('soffice') is None, reason="Requires LibreOffice")
def test_docx_to_pdf(sample_docx):
    result = docx_to_pdf(sample_docx)
    assert result.startswith(b'%PDF-')

@pytest.mark.skipif(shutil.which('soffice') is None, reason="Requires LibreOffice")
def test_pptx_to_pdf(sample_pptx):
    result = pptx_to_pdf(sample_pptx)
    assert result.startswith(b'%PDF-')
