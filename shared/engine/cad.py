"""CAD conversion module.

Handles: dwg→pdf
Requires LibreOffice Portable — desktop only.
"""

import subprocess
import tempfile
import os
from pathlib import Path


def dwg_to_pdf(data: bytes) -> bytes:
    """Convert DWG to PDF via LibreOffice Draw (desktop-only). Set LO_BIN env var."""
    lo_bin = os.environ.get("LO_BIN", "soffice")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.dwg"
        src.write_bytes(data)
        subprocess.run(
            [lo_bin, "--headless", "--invisible", "--convert-to", "pdf",
             "--outdir", tmp, str(src)],
            check=True,
            timeout=60,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        return (Path(tmp) / "input.pdf").read_bytes()
