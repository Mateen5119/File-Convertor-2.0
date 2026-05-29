"""Font conversion module.

Handles: ttf→woff2, otf→woff2
"""

import io


def ttf_to_woff2(data: bytes) -> bytes:
    """Convert TrueType font to WOFF2 format."""
    from fontTools.ttLib import TTFont
    font = TTFont(io.BytesIO(data))
    out = io.BytesIO()
    font.flavor = "woff2"
    font.save(out)
    return out.getvalue()


def otf_to_woff2(data: bytes) -> bytes:
    """Convert OpenType font to WOFF2 format (same process as TTF)."""
    return ttf_to_woff2(data)
