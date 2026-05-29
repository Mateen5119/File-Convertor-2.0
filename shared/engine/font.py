"""Font conversion module.

Handles: ttf→woff2, otf→woff2
"""

import io
from .validator import validate


def ttf_to_woff2(data: bytes, is_web: bool = False) -> bytes:
    """Convert TrueType font to WOFF2 format."""
    validate(data, "ttf", is_web=is_web)
    
    # Correct capitalization of fontTools for case-sensitive Vercel systems (ISS-025)
    from fontTools.ttLib import TTFont
    font = TTFont(io.BytesIO(data))
    out = io.BytesIO()
    font.flavor = "woff2"
    font.save(out)
    return out.getvalue()


def otf_to_woff2(data: bytes, is_web: bool = False) -> bytes:
    """Convert OpenType font to WOFF2 format (same process as TTF)."""
    validate(data, "otf", is_web=is_web)
    return ttf_to_woff2(data, is_web=is_web)
