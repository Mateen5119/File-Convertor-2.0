"""CAD conversion module.

Handles: dwg→pdf
Requires LibreOffice Portable — desktop only.
"""

import subprocess
import tempfile
import os
from pathlib import Path
from .validator import validate


def dwg_to_pdf(data: bytes, is_web: bool = False) -> bytes:
    """Convert DWG to PDF via LibreOffice Draw (desktop-only). Set LO_BIN env var."""
    validate(data, "dwg", is_web=is_web)
    if is_web:
        raise ValueError("DWG CAD conversion requires LibreOffice and is desktop-only.")
        
    lo_bin = os.environ.get("LO_BIN", "soffice")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.dwg"
        src.write_bytes(data)
        
        # ISS-019: Execute subprocess with absolute timeout parameters to prevent infinite hangs
        subprocess.run(
            [lo_bin, "--headless", "--invisible", "--convert-to", "pdf",
             "--outdir", tmp, str(src)],
            check=True,
            timeout=45,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        return (Path(tmp) / "input.pdf").read_bytes()
