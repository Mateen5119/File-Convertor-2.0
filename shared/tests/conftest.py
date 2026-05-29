"""Shared test fixtures — programmatic generation of minimal valid files.

All binary fixtures are generated from raw bytes to avoid shipping
real media files in the repo.  Text fixtures are plain strings.
"""

import io
import json
import struct
import tempfile
import zlib
from pathlib import Path

import pytest


# ─── helpers ──────────────────────────────────────────────────────────────────

def _make_png_1x1(red: int = 255, green: int = 0, blue: int = 0) -> bytes:
    """Create a valid 1×1 pixel 8-bit RGB PNG from scratch."""

    def _chunk(chunk_type: bytes, data: bytes) -> bytes:
        raw = chunk_type + data
        return struct.pack(">I", len(data)) + raw + struct.pack(">I", zlib.crc32(raw) & 0xFFFFFFFF)

    signature = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)  # 1×1, 8-bit, RGB
    ihdr = _chunk(b"IHDR", ihdr_data)
    raw_row = b"\x00" + bytes([red, green, blue])  # filter=None + pixel
    idat = _chunk(b"IDAT", zlib.compress(raw_row))
    iend = _chunk(b"IEND", b"")
    return signature + ihdr + idat + iend


def _make_jpeg_1x1() -> bytes:
    """Create a minimal valid 1×1 JFIF JPEG (grey pixel)."""
    # Minimal valid JPEG: SOI + APP0(JFIF) + DQT + SOF0 + DHT + SOS + scan data + EOI
    # Using a hand-crafted minimal stream.
    try:
        from PIL import Image
        buf = io.BytesIO()
        img = Image.new("RGB", (1, 1), (128, 128, 128))
        img.save(buf, "JPEG")
        return buf.getvalue()
    except ImportError:
        # Absolute minimal JPEG that starts with the right magic bytes
        return (
            b"\xff\xd8\xff\xe0"  # SOI + APP0 marker
            b"\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
            b"\xff\xd9"  # EOI
        )


def _make_webp_1x1() -> bytes:
    """Create a minimal valid 1×1 lossy WebP."""
    try:
        from PIL import Image
        buf = io.BytesIO()
        img = Image.new("RGB", (1, 1), (0, 128, 255))
        img.save(buf, "WEBP")
        return buf.getvalue()
    except ImportError:
        # RIFF header — enough to pass magic-byte validation
        return b"RIFF\x00\x00\x00\x00WEBP"


def _make_gif_1x1() -> bytes:
    """Create a minimal valid 1×1 GIF89a."""
    try:
        from PIL import Image
        buf = io.BytesIO()
        img = Image.new("P", (1, 1))
        img.save(buf, "GIF")
        return buf.getvalue()
    except ImportError:
        return b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x00\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"


def _make_tiff_1x1() -> bytes:
    """Create a minimal 1×1 TIFF via Pillow."""
    from PIL import Image
    buf = io.BytesIO()
    img = Image.new("RGB", (1, 1), (64, 128, 192))
    img.save(buf, "TIFF")
    return buf.getvalue()


def _make_svg_circle() -> bytes:
    """Minimal SVG with a 10×10 red circle."""
    return (
        b'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
        b'<circle cx="5" cy="5" r="5" fill="red"/>'
        b"</svg>"
    )


def _make_pdf_with_table() -> bytes:
    """Create a tiny valid PDF with tabular text (for pdf_to_xlsx tests).

    Uses reportlab if available; otherwise falls back to a hand-crafted
    minimal PDF that at least starts with %PDF for validator tests.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)
        table_data = [
            ["Name", "Age", "City"],
            ["Alice", "30", "London"],
            ["Bob", "25", "Paris"],
        ]
        doc.build([Table(table_data)])
        return buf.getvalue()
    except ImportError:
        # Minimal valid PDF
        return (
            b"%PDF-1.0\n"
            b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
            b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
            b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\n"
            b"xref\n0 4\n"
            b"0000000000 65535 f \n"
            b"0000000009 00000 n \n"
            b"0000000058 00000 n \n"
            b"0000000115 00000 n \n"
            b"trailer<</Size 4/Root 1 0 R>>\n"
            b"startxref\n190\n%%EOF"
        )


def _make_minimal_pdf() -> bytes:
    """Minimal valid %PDF for validator tests."""
    return (
        b"%PDF-1.0\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\n"
        b"xref\n0 4\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"trailer<</Size 4/Root 1 0 R>>\n"
        b"startxref\n190\n%%EOF"
    )


def _make_pem_cert() -> bytes:
    """A self-signed PEM certificate (cert only, no key)."""
    try:
        from cryptography import x509
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.x509.oid import NameOID
        import datetime

        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, "Test"),
        ])
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=1))
            .sign(key, hashes.SHA256())
        )
        cert_pem = cert.public_bytes(serialization.Encoding.PEM)
        key_pem = key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        )
        return key_pem + b"\n" + cert_pem
    except ImportError:
        pytest.skip("cryptography not installed")


# ─── text fixture data ────────────────────────────────────────────────────────

SAMPLE_CSV = "name,age,city\nAlice,30,London\nBob,25,Paris\n"

SAMPLE_JSON = json.dumps([
    {"name": "Alice", "age": 30, "city": "London"},
    {"name": "Bob", "age": 25, "city": "Paris"},
])

SAMPLE_XML = (
    '<?xml version="1.0"?>'
    "<people>"
    "<person><name>Alice</name><age>30</age></person>"
    "<person><name>Bob</name><age>25</age></person>"
    "</people>"
)

SAMPLE_YAML = "name: Alice\nage: 30\ncity: London\n"

SAMPLE_MD = "# Hello\n\nThis is **bold** and *italic*.\n\n- item 1\n- item 2\n"


# ─── pytest fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def png_bytes():
    """Valid 1×1 PNG image bytes."""
    return _make_png_1x1()


@pytest.fixture
def jpg_bytes():
    """Valid 1×1 JPEG image bytes."""
    return _make_jpeg_1x1()


@pytest.fixture
def webp_bytes():
    """Valid 1×1 WebP image bytes."""
    return _make_webp_1x1()


@pytest.fixture
def gif_bytes():
    """Valid 1×1 GIF image bytes."""
    return _make_gif_1x1()


@pytest.fixture
def tiff_bytes():
    """Valid 1×1 TIFF image bytes."""
    return _make_tiff_1x1()


@pytest.fixture
def svg_bytes():
    """Minimal SVG circle."""
    return _make_svg_circle()


@pytest.fixture
def pdf_bytes():
    """Minimal valid PDF bytes."""
    return _make_minimal_pdf()


@pytest.fixture
def pdf_with_table_bytes():
    """PDF with a table (for pdf_to_xlsx)."""
    return _make_pdf_with_table()


@pytest.fixture
def pem_bytes():
    """PEM with self-signed cert + private key."""
    return _make_pem_cert()


@pytest.fixture
def csv_bytes():
    return SAMPLE_CSV.encode("utf-8")


@pytest.fixture
def json_bytes():
    return SAMPLE_JSON.encode("utf-8")


@pytest.fixture
def xml_bytes():
    return SAMPLE_XML.encode("utf-8")


@pytest.fixture
def yaml_bytes():
    return SAMPLE_YAML.encode("utf-8")


@pytest.fixture
def md_bytes():
    return SAMPLE_MD.encode("utf-8")


@pytest.fixture
def tmp_dir():
    """Provide a temporary directory that's cleaned up after the test."""
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)
