"""Tests for shared.engine.validator — magic-byte checking & size limits."""

import sys
import os
import pytest

# Ensure the shared package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.validator import validate, MAGIC_BYTES, MAX_FILE_SIZE_WEB_BYTES, MAX_FILE_SIZE_DESKTOP_BYTES


# ─── magic-byte validation ───────────────────────────────────────────────────

class TestMagicByteValidation:
    """Verify that validate() accepts correct headers and rejects wrong ones."""

    def test_valid_png(self, png_bytes):
        """Valid PNG should pass without error."""
        validate(png_bytes, "png")

    def test_valid_jpg(self, jpg_bytes):
        validate(jpg_bytes, "jpg")

    def test_valid_pdf(self, pdf_bytes):
        validate(pdf_bytes, "pdf")

    def test_valid_gif(self, gif_bytes):
        validate(gif_bytes, "gif")

    def test_valid_webp(self, webp_bytes):
        validate(webp_bytes, "webp")

    def test_invalid_magic_bytes_raises(self):
        """Random bytes must not pass PNG validation."""
        with pytest.raises(ValueError, match="does not match"):
            validate(b"NOT_A_PNG_FILE", "png")

    def test_invalid_jpg_magic_bytes(self):
        with pytest.raises(ValueError, match="does not match"):
            validate(b"\x00\x00\x00\x00", "jpg")

    def test_invalid_pdf_magic_bytes(self):
        with pytest.raises(ValueError, match="does not match"):
            validate(b"<html>not a pdf</html>", "pdf")

    @pytest.mark.parametrize("fmt,header", [
        ("png",  b"\x89PNG"),
        ("jpg",  b"\xff\xd8\xff"),
        ("pdf",  b"%PDF"),
        ("gif",  b"GIF89a"),
        ("gif",  b"GIF87a"),
        ("webp", b"RIFF"),
        ("zip",  b"PK\x03\x04"),
        ("rar",  b"Rar!\x1a\x07"),
    ])
    def test_valid_headers_parametrised(self, fmt, header):
        """All known magic headers must be accepted."""
        # Pad to at least 100 bytes so size check never trips
        data = header + b"\x00" * 100
        validate(data, fmt)

    def test_format_without_magic_always_passes(self):
        """Formats not in MAGIC_BYTES (e.g. csv, md) should pass any data."""
        validate(b"anything goes", "csv")
        validate(b"# markdown", "md")
        validate(b"hello: world", "yaml")


# ─── size-limit validation ───────────────────────────────────────────────────

class TestSizeLimits:
    """Validate web and desktop file-size limits."""

    def test_web_limit_value(self):
        assert MAX_FILE_SIZE_WEB_BYTES == 4 * 1024 * 1024  # 4 MB

    def test_desktop_limit_value(self):
        assert MAX_FILE_SIZE_DESKTOP_BYTES == 2 * 1024 ** 3  # 2 GB

    def test_web_under_limit_passes(self):
        data = b"x" * (MAX_FILE_SIZE_WEB_BYTES - 1)
        validate(data, "txt", is_web=True)

    def test_web_over_limit_raises(self):
        data = b"x" * (MAX_FILE_SIZE_WEB_BYTES + 1)
        with pytest.raises(ValueError, match="exceeds size limit"):
            validate(data, "txt", is_web=True)

    def test_desktop_under_limit_passes(self):
        """Under 2 GB should be fine (we can't allocate 2 GB in CI,
        so just test a small payload)."""
        validate(b"small file", "txt", is_web=False)

    def test_web_exact_limit_passes(self):
        """Exactly at the limit should still pass (≤ check)."""
        data = b"x" * MAX_FILE_SIZE_WEB_BYTES
        validate(data, "txt", is_web=True)


# ─── edge cases ──────────────────────────────────────────────────────────────

class TestEdgeCases:
    """Edge-case behaviour."""

    def test_empty_file(self):
        """Empty data has no magic bytes — should fail for formats with magic."""
        with pytest.raises(ValueError, match="does not match"):
            validate(b"", "png")

    def test_empty_file_no_magic_format(self):
        """Empty data for a format without magic bytes should pass."""
        validate(b"", "csv")

    def test_magic_bytes_dict_not_empty(self):
        assert len(MAGIC_BYTES) > 0, "MAGIC_BYTES should have entries"

    def test_all_magic_entries_are_lists(self):
        for fmt, patterns in MAGIC_BYTES.items():
            assert isinstance(patterns, list), f"{fmt} magic should be a list"
            for p in patterns:
                assert isinstance(p, bytes), f"{fmt} patterns should be bytes"
