"""Magic-byte file validator for all supported formats.

Every conversion must call validate() before processing.
"""

MAGIC_BYTES: dict[str, list[bytes]] = {
    "pdf":  [b"%PDF"],
    "docx": [b"PK\x03\x04"],
    "xlsx": [b"PK\x03\x04"],
    "pptx": [b"PK\x03\x04"],
    "png":  [b"\x89PNG"],
    "jpg":  [b"\xff\xd8\xff"],
    "gif":  [b"GIF87a", b"GIF89a"],
    "webp": [b"RIFF"],
    "mp4":  [b"\x00\x00\x00\x18ftyp", b"\x00\x00\x00\x20ftyp"],
    "zip":  [b"PK\x03\x04"],
    "rar":  [b"Rar!\x1a\x07"],
}

MAX_FILE_SIZE_WEB_BYTES   = 4 * 1024 * 1024   # 4MB (under Vercel's 4.5MB limit)
MAX_FILE_SIZE_DESKTOP_BYTES = 2 * 1024 ** 3   # 2GB


def validate(data: bytes, fmt: str, is_web: bool = False) -> None:
    """Raises ValueError on failure. Call before any conversion."""
    size_limit = MAX_FILE_SIZE_WEB_BYTES if is_web else MAX_FILE_SIZE_DESKTOP_BYTES
    if len(data) > size_limit:
        raise ValueError(f"File exceeds size limit: {len(data)} bytes")
    magic = MAGIC_BYTES.get(fmt)
    if magic and not any(data.startswith(m) for m in magic):
        raise ValueError(f"File header does not match expected format: {fmt}")
