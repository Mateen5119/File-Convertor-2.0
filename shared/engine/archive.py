"""Archive conversion module.

Handles: rar→zip
Requires unrar binary — desktop only.
"""

import io
import zipfile
import tempfile
from pathlib import Path
from .validator import validate


def rar_to_zip(data: bytes, is_web: bool = False) -> bytes:
    """Convert RAR archive to ZIP format."""
    validate(data, "rar", is_web=is_web)
    if is_web:
        raise ValueError("RAR conversions require system binaries and are desktop-only.")
        
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.rar"
        src.write_bytes(data)
        import rarfile
        out_buf = io.BytesIO()
        with rarfile.RarFile(str(src)) as rf:
            with zipfile.ZipFile(out_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for member in rf.infolist():
                    zf.writestr(member.filename, rf.read(member.filename))
        return out_buf.getvalue()
