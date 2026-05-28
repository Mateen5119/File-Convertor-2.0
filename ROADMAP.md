# Convert App — Full Development Roadmap

> **Stack:** Next.js (web frontend) · Vercel Serverless Python (web backend) · PyQt6 (desktop) · Shared Python conversion engine · Inno Setup (installer)
> **Projects:** `web/` (Vercel-deployed) · `desktop/` (standalone, treated as a separate project)
> **AI IDE:** Google Antigravity — reads `.antigravity/GUIDELINES.md` as pinned context

---

## Table of Contents

1. [Monorepo Structure](#1-monorepo-structure)
2. [Phase 0 — Repo & Environment Setup](#2-phase-0--repo--environment-setup)
3. [Phase 1 — Design System & Shared Assets](#3-phase-1--design-system--shared-assets)
4. [Phase 2 — Shared Conversion Engine](#4-phase-2--shared-conversion-engine)
5. [Phase 3 — Web App](#5-phase-3--web-app)
6. [Phase 4 — Desktop App](#6-phase-4--desktop-app)
7. [Phase 5 — Desktop Extra Features (Editor & Compressor)](#7-phase-5--desktop-extra-features-editor--compressor)
8. [Phase 6 — Packaging & Distribution (Inno Setup)](#8-phase-6--packaging--distribution-inno-setup)
9. [Phase 7 — CI/CD (GitHub Actions)](#9-phase-7--cicd-github-actions)
10. [Phase 8 — Testing](#10-phase-8--testing)
11. [Appendix A — Conversion Library Reference](#11-appendix-a--conversion-library-reference)
12. [Appendix B — Vercel Platform Constraints & Mitigations](#12-appendix-b--vercel-platform-constraints--mitigations)
13. [Appendix C — Design Tokens (from Stitch)](#13-appendix-c--design-tokens-from-stitch)

---

## 1. Monorepo Structure

```
convert-app/
├── .antigravity/
│   ├── GUIDELINES.md           ← Pinned AI IDE context (copy from repo root)
│   └── config.json             ← Agent runtime config
├── .github/
│   └── workflows/
│       ├── web-ci.yml
│       └── desktop-ci.yml
├── shared/                     ← Shared Python conversion engine (used by both projects)
│   └── engine/
│       ├── __init__.py
│       ├── document.py         ← pdf↔docx, md→html/pdf, pptx→pdf, epub→pdf, mobi→epub
│       ├── image.py            ← heic→jpg, webp→png/jpg, png→jpg, svg→png, tiff→jpg/pdf, gif→mp4
│       ├── video.py            ← mp4→mp3, mov→mp4, mkv→mp4, webm→mp4
│       ├── audio.py            ← wav→mp3, m4a→mp3
│       ├── data.py             ← csv→xlsx, pdf→xlsx, json→csv, xml→json, yaml→json
│       ├── security.py         ← pem→pfx/crt
│       ├── font.py             ← ttf/otf→woff2
│       ├── archive.py          ← rar→zip
│       ├── cad.py              ← dwg→pdf
│       └── validator.py        ← Magic-byte validation for all formats
├── web/                        ← Vercel project root
│   ├── .env.local              ← Local secrets (never commit)
│   ├── .env.example            ← Committed template
│   ├── next.config.ts
│   ├── vercel.json
│   ├── requirements.txt        ← Python deps for serverless functions
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── api/                    ← Vercel Python serverless functions
│   │   ├── convert.py          ← Main conversion endpoint
│   │   └── health.py
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── DropZone.tsx
│   │   ├── ConversionQueue.tsx
│   │   ├── FormatSelector.tsx
│   │   ├── ProgressBar.tsx
│   │   ├── DesktopCTA.tsx      ← "Download Desktop App" promo banner
│   │   ├── AdSlot.tsx          ← Left/right sidebar ad placeholders
│   │   └── ui/                 ← Glass design system components
│   │       ├── GlassCard.tsx
│   │       ├── GlassButton.tsx
│   │       └── FileChip.tsx
│   ├── lib/
│   │   ├── constants.ts        ← FILE_SIZE_LIMIT, SUPPORTED_FORMATS
│   │   ├── validate.ts         ← Client-side pre-upload checks
│   │   └── api.ts              ← Fetch wrappers for /api/convert
│   └── public/
│       └── fonts/
├── desktop/                    ← Standalone desktop project (Python)
│   ├── .env                    ← Local config (never commit)
│   ├── .env.example
│   ├── requirements.txt
│   ├── main.py                 ← Entry point (no console window)
│   ├── build.spec              ← PyInstaller spec (--noconsole)
│   ├── ui/
│   │   ├── main_window.py      ← QMainWindow
│   │   ├── drop_zone.py        ← QWidget drag-and-drop
│   │   ├── conversion_queue.py
│   │   ├── format_selector.py
│   │   └── styles/
│   │       ├── dark.qss        ← QSS dark theme (mirrors Stitch dark tokens)
│   │       └── light.qss       ← QSS light theme
│   ├── engine/                 ← Copy of shared/engine/ (treated independently)
│   │   └── ...                 ← Same structure as shared/engine/
│   ├── features/
│   │   ├── editor/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_editor.py   ← pypdf + pymupdf
│   │   │   └── docx_editor.py  ← python-docx
│   │   └── compressor/
│   │       ├── __init__.py
│   │       ├── pdf_compress.py ← ghostscript / pikepdf
│   │       └── img_compress.py ← Pillow
│   ├── assets/
│   │   ├── icon.ico
│   │   ├── icon.png
│   │   └── fonts/
│   │       └── Inter-*.ttf
│   ├── libreoffice_portable/   ← LibreOffice Portable (bundled, not committed to git)
│   │   └── ...
│   └── installer/
│       └── setup.iss           ← Inno Setup script
└── README.md
```

---

## 2. Phase 0 — Repo & Environment Setup

### Step 1: Initialize Git repository

```bash
git init convert-app
cd convert-app
git checkout -b main
```

Create `.gitignore` at root:

```
# Python
__pycache__/
*.pyc
*.pyo
.venv/
*.egg-info/

# Env files
.env
.env.local
.env.production
*.pem
*.pfx
*.key

# Node
node_modules/
.next/
out/

# Build artifacts
dist/
build/
*.exe
*.zip

# LibreOffice Portable (too large for git)
desktop/libreoffice_portable/

# Temp conversion dirs
tmp/
temp_conversions/

# OS
.DS_Store
Thumbs.db
```

### Step 2: Configure `.antigravity/`

```bash
mkdir .antigravity
cp GUIDELINES.md .antigravity/GUIDELINES.md
```

`config.json`:
```json
{
  "agent_runtime": {
    "memory_layer": "hybrid",
    "pinned_context_files": [".antigravity/GUIDELINES.md"],
    "token_guardrails": {
      "max_context_tokens": 32768,
      "prevent_recursive_loops": true,
      "suppress_redundant_logs": true
    }
  }
}
```

### Step 3: Web project bootstrap

```bash
cd web
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir no --import-alias "@/*"
```

Pin exact Next.js version in `package.json` after creation.

Install additional web dependencies:
```bash
npm install --save-exact zod
npm install --save-exact @types/node
```

### Step 4: Desktop Python environment

```bash
cd desktop
python -m venv .venv
# Windows activation:
.venv\Scripts\activate
pip install --upgrade pip
```

Create `desktop/requirements.txt` (see Appendix A for full list).

### Step 5: Branch protection (GitHub)

After pushing to GitHub:
- Protect `main` branch: require PR + 1 review, require status checks to pass
- Enable Dependabot for both `web/package.json` and `desktop/requirements.txt`
- Add `CODEOWNERS` at root:

```
* @your-username
```

### Step 6: Conventional Commits setup (web)

```bash
cd web
npm install --save-exact --save-dev @commitlint/cli @commitlint/config-conventional husky lint-staged
npx husky init
```

`commitlint.config.js`:
```js
module.exports = { extends: ['@commitlint/config-conventional'] };
```

---

## 3. Phase 1 — Design System & Shared Assets

### Design Token Summary (from Stitch DESIGN.md)

- **Font:** Inter (all weights) — load via `next/font` on web, bundle `.ttf` files in desktop
- **Grid:** 8px base unit
- **Max container width:** 1200px
- **Dark mode background:** `#131315` (60–70% opacity on glass layers)
- **Primary:** `#adc6ff` (Electric Blue)
- **Secondary:** `#c2c1ff` (Indigo)
- **Tertiary (success):** `#47e266` (Emerald)
- **Error:** `#ffb4ab`
- **Glass blur:** `backdrop-filter: blur(20px); saturate(180%)`
- **Borders:** Dark: `rgba(255,255,255,0.1)` / Light: `rgba(0,0,0,0.08)`
- **Corner radii:** Cards `24px`, buttons/inputs `16px`, progress bars `9999px`
- **Full token reference:** `desktop/ui/styles/dark.qss` + `web/app/globals.css`

See Appendix C for complete token mapping.

### Web Design Implementation

`web/app/globals.css` — define all CSS variables from Stitch tokens, implement glass utility classes:

```css
:root {
  --surface: #131315;
  --primary: #adc6ff;
  --secondary: #c2c1ff;
  --tertiary: #47e266;
  --error: #ffb4ab;
  --on-surface: #e4e2e4;
  --outline: #8b90a0;
  --glass-border-dark: rgba(255, 255, 255, 0.1);
  --glass-bg-dark: rgba(28, 28, 30, 0.7);
  --glass-bg-light: rgba(255, 255, 255, 0.8);
  --blur: blur(20px) saturate(180%);
  --radius-card: 1.5rem;
  --radius-btn: 1rem;
}

.glass-card {
  background: var(--glass-bg-dark);
  backdrop-filter: var(--blur);
  border: 1px solid var(--glass-border-dark);
  border-radius: var(--radius-card);
}
```

`tailwind.config.ts` — extend with all Stitch spacing, color, and rounded tokens.

### Desktop Theme (QSS)

`desktop/ui/styles/dark.qss` mirrors the same dark token palette using Qt Style Sheets. Apply via:

```python
# main.py
with open("ui/styles/dark.qss", "r") as f:
    app.setStyleSheet(f.read())
```

---

## 4. Phase 2 — Shared Conversion Engine

> **Note:** The `shared/engine/` directory is the source of truth. After changes, manually copy it to `desktop/engine/`. The web serverless functions import from the same engine via relative paths inside `web/api/`.

### Step 1: Magic-byte file validator

`shared/engine/validator.py`

Every conversion must call this before processing:

```python
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
```

### Step 2: Conversion modules

Each module follows this pattern:

```python
# shared/engine/image.py
import tempfile
import os
from pathlib import Path
from .validator import validate

def png_to_jpg(data: bytes, quality: int = 90) -> bytes:
    validate(data, "png")
    with tempfile.TemporaryDirectory() as tmp:
        try:
            src = Path(tmp) / "input.png"
            dst = Path(tmp) / "output.jpg"
            src.write_bytes(data)
            from PIL import Image
            img = Image.open(src).convert("RGB")
            img.save(dst, "JPEG", quality=quality)
            return dst.read_bytes()
        finally:
            pass  # TemporaryDirectory cleans up automatically
```

**All modules must:**
- Call `validate()` as first operation
- Use `tempfile.TemporaryDirectory()` as context manager for isolation
- Return `bytes` — never write to permanent paths
- Never catch exceptions silently — let them propagate to caller

### Step 3: Conversion router

`shared/engine/__init__.py` — maps `(source_ext, target_ext)` tuples to handler functions:

```python
from .document import pdf_to_docx, docx_to_pdf, md_to_html, md_to_pdf, pptx_to_pdf, epub_to_pdf, mobi_to_epub
from .image    import heic_to_jpg, webp_to_png, webp_to_jpg, png_to_jpg, svg_to_png, tiff_to_jpg, tiff_to_pdf, gif_to_mp4
from .video    import mp4_to_mp3, mov_to_mp4, mkv_to_mp4, webm_to_mp4
from .audio    import wav_to_mp3, m4a_to_mp3
from .data     import csv_to_xlsx, pdf_to_xlsx, json_to_csv, xml_to_json, yaml_to_json
from .security import pem_to_pfx, pem_to_crt
from .font     import ttf_to_woff2, otf_to_woff2
from .archive  import rar_to_zip
from .cad      import dwg_to_pdf

CONVERSION_MAP: dict[tuple[str, str], callable] = {
    ("pdf",  "docx"): pdf_to_docx,
    ("docx", "pdf"):  docx_to_pdf,
    ("heic", "jpg"):  heic_to_jpg,
    ("webp", "png"):  webp_to_png,
    ("webp", "jpg"):  webp_to_jpg,
    ("png",  "jpg"):  png_to_jpg,
    ("mp4",  "mp3"):  mp4_to_mp3,
    ("mov",  "mp4"):  mov_to_mp4,
    ("csv",  "xlsx"): csv_to_xlsx,
    ("pdf",  "xlsx"): pdf_to_xlsx,
    ("svg",  "png"):  svg_to_png,
    ("mkv",  "mp4"):  mkv_to_mp4,
    ("epub", "pdf"):  epub_to_pdf,
    ("json", "csv"):  json_to_csv,
    ("wav",  "mp3"):  wav_to_mp3,
    ("pptx", "pdf"):  pptx_to_pdf,
    ("xml",  "json"): xml_to_json,
    ("gif",  "mp4"):  gif_to_mp4,
    ("webm", "mp4"):  webm_to_mp4,
    ("m4a",  "mp3"):  m4a_to_mp3,
    ("md",   "html"): md_to_html,
    ("md",   "pdf"):  md_to_pdf,
    ("ttf",  "woff2"): ttf_to_woff2,
    ("otf",  "woff2"): otf_to_woff2,
    ("pem",  "pfx"):  pem_to_pfx,
    ("pem",  "crt"):  pem_to_crt,
    ("yaml", "json"): yaml_to_json,
    ("mobi", "epub"): mobi_to_epub,
    ("tiff", "jpg"):  tiff_to_jpg,
    ("tiff", "pdf"):  tiff_to_pdf,
    ("rar",  "zip"):  rar_to_zip,
    ("dwg",  "pdf"):  dwg_to_pdf,
}

def convert(data: bytes, source_fmt: str, target_fmt: str, is_web: bool = False) -> bytes:
    key = (source_fmt.lower(), target_fmt.lower())
    handler = CONVERSION_MAP.get(key)
    if not handler:
        raise ValueError(f"Unsupported conversion: {source_fmt} → {target_fmt}")
    return handler(data)
```

---

## 5. Phase 3 — Web App

### Step 1: Vercel configuration

`web/vercel.json`:
```json
{
  "functions": {
    "api/convert.py": {
      "runtime": "python3.12",
      "maxDuration": 60,
      "memory": 1024
    }
  },
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/$1" }
  ]
}
```

> **Constraint:** Vercel Hobby plan caps body size at 4.5MB and execution at 10s. Pro plan allows up to 4.5MB body and 60s execution. Upgrade to Pro for production.

### Step 2: Serverless conversion endpoint

`web/api/convert.py`:

```python
import sys
import os
import base64
import json

# Add shared engine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

from engine import convert, CONVERSION_MAP
from engine.validator import MAX_FILE_SIZE_WEB_BYTES
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            payload = json.loads(body)
            file_b64:   str = payload["file"]
            source_fmt: str = payload["source_fmt"].lower().strip(".")
            target_fmt: str = payload["target_fmt"].lower().strip(".")

            file_bytes = base64.b64decode(file_b64)

            if len(file_bytes) > MAX_FILE_SIZE_WEB_BYTES:
                self._send(400, {"error": "FILE_TOO_LARGE", "message": "File exceeds 4MB. Download the desktop app for large files."})
                return

            result_bytes = convert(file_bytes, source_fmt, target_fmt, is_web=True)
            result_b64   = base64.b64encode(result_bytes).decode()

            self._send(200, {"result": result_b64, "target_fmt": target_fmt})

        except ValueError as e:
            self._send(400, {"error": "VALIDATION_ERROR", "message": str(e)})
        except Exception as e:
            self._send(500, {"error": "CONVERSION_FAILED", "message": "Conversion failed. Try the desktop app."})

    def _send(self, status: int, data: dict):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
```

### Step 3: Client-side file size enforcement

`web/lib/constants.ts`:
```ts
export const WEB_FILE_SIZE_LIMIT_BYTES = 4 * 1024 * 1024; // 4MB
export const WEB_FILE_SIZE_LIMIT_LABEL = "4MB";
export const DESKTOP_DOWNLOAD_URL = "https://your-site.com/download"; // Update post-release
```

`web/lib/validate.ts`:
```ts
import { WEB_FILE_SIZE_LIMIT_BYTES, WEB_FILE_SIZE_LIMIT_LABEL } from "./constants";

export function checkFileSizeLimit(file: File): { valid: boolean; showDesktopCTA: boolean } {
  if (file.size > WEB_FILE_SIZE_LIMIT_BYTES) {
    return { valid: false, showDesktopCTA: true };
  }
  return { valid: true, showDesktopCTA: false };
}
```

### Step 4: DropZone component

`web/components/DropZone.tsx` — key behaviors:

- Accept drag-and-drop and click-to-upload
- On file selection, immediately call `checkFileSizeLimit()`
- If `showDesktopCTA === true`: do **not** upload; instead render `<DesktopCTA />` inline with a clear message: *"This file exceeds 4MB. Download the desktop app for unlimited file sizes."*
- Show dashed border with `--primary` color (2px dashed), transition to blue tint on hover/dragover
- Display `<FileChip>` badges per queued file showing format and size

### Step 5: DesktopCTA component

`web/components/DesktopCTA.tsx` — positioned near the upload zone per Stitch design:

- Glass card style
- Text: *"No Ads. No File Size Limits."*
- CTA button: *"Download Desktop App"* → `DESKTOP_DOWNLOAD_URL`
- Show permanently in sidebar on desktop viewport; show inline when file size limit is hit

### Step 6: Ad slots

`web/components/AdSlot.tsx` — left and right sidebar placeholders:

- Render empty glass-bordered containers at design spec dimensions
- Add `data-ad-slot` attributes for future ad network integration
- These are **not visible on desktop app** — only web layout includes them

### Step 7: Page layout

`web/app/page.tsx` — layout structure:
```
[ Header: nav + branding ]
[ Left AdSlot ] [ Main: DropZone + Queue + DesktopCTA ] [ Right AdSlot ]
[ Footer ]
```

On mobile: sidebars collapse, DropZone becomes full-width bottom-sheet trigger.

### Step 8: Dark/Light mode

Implement via `next-themes`. Follow Stitch token split:
- Dark: `--glass-bg: rgba(28,28,30,0.7)`
- Light: `--glass-bg: rgba(255,255,255,0.8)`

Toggle in header. Persist choice to `localStorage`.

### Step 9: Environment config

`web/.env.local` (never commit):
```
# Add any future API keys here
# NEXT_PUBLIC_AD_CLIENT_ID=
```

`web/.env.example` (commit this):
```
# NEXT_PUBLIC_AD_CLIENT_ID=your_ad_client_id
```

---

## 6. Phase 4 — Desktop App

> Desktop is treated as a **fully independent project** inside `desktop/`. It has its own `requirements.txt`, its own copy of the engine, and its own CI pipeline.

### Step 1: Entry point — no console window

`desktop/main.py`:
```python
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Convert")
    app.setOrganizationName("YourOrg")

    # Load dark theme QSS
    with open("ui/styles/dark.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

**No console window** is enforced at two levels:

1. **PyInstaller build spec** (`build.spec`):
   ```python
   exe = EXE(
       pyz,
       a.scripts,
       console=False,     # ← suppresses terminal window
       windowed=True,
       ...
   )
   ```

2. **Inno Setup** — application type is `GUI`, no `AllocConsole` call.
3. **Local dev:** Run with `pythonw.exe main.py` instead of `python.exe main.py`.

### Step 2: Main window

`desktop/ui/main_window.py`:
- `QMainWindow` with custom title bar (macOS-style window controls via QSS)
- Central widget: `DropZone` component
- Side panel: `ConversionQueue`
- Top bar: dark/light mode toggle, settings icon
- Bottom bar: status label

### Step 3: DropZone widget

`desktop/ui/drop_zone.py`:
- Subclass `QWidget`, override `dragEnterEvent`, `dragMoveEvent`, `dropEvent`
- Accept `QUrl` list from drop events, extract local file paths
- No file size restriction on desktop — process all sizes
- On file drop: validate magic bytes, add to queue, start conversion in `QThread`

### Step 4: Conversion threading

All conversion must run in a `QThread` to avoid blocking the UI:

```python
from PyQt6.QtCore import QThread, pyqtSignal

class ConversionWorker(QThread):
    progress = pyqtSignal(int)         # 0–100
    finished = pyqtSignal(bytes, str)  # result bytes, output path
    error    = pyqtSignal(str)

    def __init__(self, data: bytes, source_fmt: str, target_fmt: str, output_path: str):
        super().__init__()
        self.data        = data
        self.source_fmt  = source_fmt
        self.target_fmt  = target_fmt
        self.output_path = output_path

    def run(self) -> None:
        try:
            from engine import convert
            result = convert(self.data, self.source_fmt, self.target_fmt, is_web=False)
            with open(self.output_path, "wb") as f:
                f.write(result)
            self.finished.emit(result, self.output_path)
        except Exception as e:
            self.error.emit(str(e))
```

### Step 5: QSS dark theme

`desktop/ui/styles/dark.qss` — mirrors Stitch dark tokens:

```css
QMainWindow, QWidget#centralWidget {
    background-color: #131315;
    color: #e4e2e4;
    font-family: "Inter";
    font-size: 14px;
}

QWidget#glassCard {
    background-color: rgba(28, 28, 30, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
}

QPushButton#primaryBtn {
    background-color: #adc6ff;
    color: #002e69;
    border-radius: 16px;
    padding: 8px 24px;
    font-weight: 600;
}

QPushButton#primaryBtn:hover {
    background-color: #4b8eff;
}

QProgressBar {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 9999px;
    height: 8px;
}

QProgressBar::chunk {
    background-color: #adc6ff;
    border-radius: 9999px;
}
```

`desktop/ui/styles/light.qss` — same structure with light tokens:
- Background: `#f5f5f7`
- Glass: `rgba(255, 255, 255, 0.8)`
- Border: `rgba(0, 0, 0, 0.08)`

### Step 6: Format selector

`desktop/ui/format_selector.py`:
- `QComboBox` populated from `CONVERSION_MAP` keys
- Auto-detect source format from file extension on drop
- Filter available targets based on source

### Step 7: Settings & config persistence

Use `QSettings` to persist:
- Theme preference (dark/light)
- Last output directory
- Default target format per source format

```python
from PyQt6.QtCore import QSettings

settings = QSettings("YourOrg", "Convert")
settings.setValue("theme", "dark")
theme = settings.value("theme", "dark")
```

---

## 7. Phase 5 — Desktop Extra Features (Editor & Compressor)

### Editor

`desktop/features/editor/pdf_editor.py` — wraps `pymupdf` (fitz):
- Open PDF, render pages to QPixmap for preview
- Annotate, delete pages, reorder pages
- Save back to PDF via `fitz.Document.save()`

`desktop/features/editor/docx_editor.py` — wraps `python-docx`:
- Load `.docx`, display paragraphs/tables in a `QTextEdit`
- Allow text edits, save back to `.docx`

**LibreOffice Portable** (`desktop/libreoffice_portable/`) — used for:
- `.docx` → `.pdf` conversion (headless mode)
- `.pptx` → `.pdf` conversion
- `.dwg` → `.pdf` (via LibreOffice Draw)

Invoke headlessly — never show LibreOffice UI:
```python
import subprocess

def libreoffice_convert(input_path: str, output_dir: str, target_fmt: str) -> None:
    lo_bin = r"libreoffice_portable\App\libreoffice\program\soffice.exe"
    subprocess.run(
        [lo_bin, "--headless", "--invisible", f"--convert-to", target_fmt, "--outdir", output_dir, input_path],
        check=True,
        creationflags=subprocess.CREATE_NO_WINDOW,  # ← suppresses any console flash
    )
```

> `CREATE_NO_WINDOW` is Windows-only. This is correct for this project (Windows target via Inno Setup).

### Compressor

`desktop/features/compressor/pdf_compress.py` — uses `pikepdf`:
```python
import pikepdf

def compress_pdf(input_path: str, output_path: str, level: int = 6) -> None:
    with pikepdf.open(input_path) as pdf:
        pdf.save(output_path, compress_streams=True, recompress_flate=True, stream_decode_level=pikepdf.StreamDecodeLevel.generalized)
```

`desktop/features/compressor/img_compress.py` — uses `Pillow`:
```python
from PIL import Image

def compress_image(input_path: str, output_path: str, quality: int = 75) -> None:
    img = Image.open(input_path)
    img.save(output_path, optimize=True, quality=quality)
```

### UI integration

Add tabs or sidebar panel in `MainWindow`:
- **Convert** tab — default, DropZone + Queue
- **Edit** tab — open file picker → load into editor
- **Compress** tab — drag file → choose compression level → save

---

## 8. Phase 6 — Packaging & Distribution (Inno Setup)

### Step 1: PyInstaller bundle

`desktop/build.spec`:

```python
# build.spec
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[
        ('libreoffice_portable', 'libreoffice_portable'),
    ],
    datas=[
        ('ui/styles', 'ui/styles'),
        ('assets', 'assets'),
        ('engine', 'engine'),
        ('features', 'features'),
    ],
    hiddenimports=['PIL._tkinter_finder'],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name='Convert',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,        # ← no terminal window
    windowed=True,        # ← Windows GUI subsystem
    icon='assets/icon.ico',
)

coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, name='Convert')
```

Build command:
```bash
pyinstaller build.spec --clean --distpath dist/
```

### Step 2: Inno Setup script

`desktop/installer/setup.iss`:

```iss
[Setup]
AppName=Convert
AppVersion=1.0.0
AppPublisher=YourOrg
DefaultDirName={autopf}\Convert
DefaultGroupName=Convert
OutputDir=..\releases
OutputBaseFilename=ConvertSetup-1.0.0
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
; GUI app — no console window allocation
AppType=gui

[Files]
; Include full PyInstaller output
Source: "..\dist\Convert\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Convert"; Filename: "{app}\Convert.exe"
Name: "{commondesktop}\Convert"; Filename: "{app}\Convert.exe"

[Run]
Filename: "{app}\Convert.exe"; Description: "Launch Convert"; Flags: nowait postinstall skipifsilent
```

Compile via:
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\setup.iss
```

---

## 9. Phase 7 — CI/CD (GitHub Actions)

### Web CI

`.github/workflows/web-ci.yml`:

```yaml
name: Web CI
on:
  push:
    branches: [main]
    paths: ['web/**']
  pull_request:
    paths: ['web/**']

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: web
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
          cache-dependency-path: web/package-lock.json
      - run: npm ci
      - run: npm run lint
      - run: npm run build
      - name: Python serverless lint
        run: |
          pip install ruff
          ruff check api/
```

Deployment: connect `web/` directory to Vercel via Vercel GitHub integration. Vercel auto-deploys on push to `main`.

### Desktop CI

`.github/workflows/desktop-ci.yml`:

```yaml
name: Desktop CI
on:
  push:
    branches: [main]
    paths: ['desktop/**', 'shared/**']
  pull_request:
    paths: ['desktop/**', 'shared/**']

jobs:
  test:
    runs-on: windows-latest
    defaults:
      run:
        working-directory: desktop
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
          cache-dependency-path: desktop/requirements.txt
      - run: pip install -r requirements.txt
      - run: pip install pytest ruff
      - run: ruff check .
      - run: pytest tests/ -v
```

> **Note:** Desktop build (PyInstaller + Inno Setup) is **not** automated in CI at this stage. Run manually for releases. Add it to CI later using a self-hosted Windows runner.

---

## 10. Phase 8 — Testing

### Web

- **Unit:** `vitest` — test `validate.ts`, `api.ts` fetch wrappers, `constants.ts`
- **Component:** `@testing-library/react` — test DropZone file rejection, DesktopCTA render
- **API:** test `/api/convert` with `pytest` + real file fixtures for each of the 27 conversion types

### Desktop

- **Unit:** `pytest` — test each engine module independently using binary file fixtures
- **GUI:** `pytest-qt` — test main window renders, queue state updates, worker signals

### Shared Engine

`shared/tests/` — one test per conversion pair:
```python
def test_png_to_jpg():
    with open("fixtures/sample.png", "rb") as f:
        data = f.read()
    result = convert(data, "png", "jpg")
    assert result[:3] == b"\xff\xd8\xff"  # JPEG magic bytes
    assert len(result) > 0
```

Fixtures: keep small binary samples (<100KB each) in `shared/tests/fixtures/`.

---

## 11. Appendix A — Conversion Library Reference

| Category | Source → Target | Library | Notes |
|----------|----------------|---------|-------|
| Document | pdf → docx | `pdf2docx` | Pure Python |
| Document | docx → pdf | LibreOffice Portable | Headless subprocess |
| Document | md → html | `markdown` | Pure Python |
| Document | md → pdf | `weasyprint` | CSS-based renderer |
| Document | pptx → pdf | LibreOffice Portable | Headless subprocess |
| Document | epub → pdf | `ebooklib` + `weasyprint` | |
| Document | mobi → epub | `ebooklib` | Limited support; flag unsupported DRM |
| Image | heic → jpg | `pillow-heif` | Wraps libheif |
| Image | webp → png/jpg | `Pillow` | Built-in |
| Image | png → jpg | `Pillow` | Convert mode to RGB first |
| Image | svg → png | `cairosvg` | Requires cairo |
| Image | tiff → jpg/pdf | `Pillow` | |
| Image | gif → mp4 | `imageio[ffmpeg]` | |
| Video | mp4/mov/mkv/webm → mp4/mp3 | `ffmpeg-python` | **Vercel: flag as unsupported on web** (binary size + timeout) |
| Audio | wav/m4a → mp3 | `pydub` + `ffmpeg` | **Vercel: flag as unsupported on web** |
| Data | csv → xlsx | `openpyxl` | |
| Data | pdf → xlsx | `pdfplumber` + `openpyxl` | |
| Data | json → csv | stdlib `json` + `csv` | |
| Data | xml → json | `xmltodict` | |
| Data | yaml → json | `pyyaml` | |
| Security | pem → pfx/crt | `cryptography` | |
| Font | ttf/otf → woff2 | `fonttools` + `brotli` | |
| Archive | rar → zip | `rarfile` + stdlib `zipfile` | Requires `unrar` binary on desktop |
| CAD | dwg → pdf | LibreOffice Portable | Desktop only |

> **Web unsupported conversions:** Video and audio conversions require `ffmpeg` binary which exceeds Vercel's function size limits and execution timeout. When these formats are selected on the web, show the DesktopCTA immediately and block the upload.

`web/lib/constants.ts` — add:
```ts
export const WEB_UNSUPPORTED_FORMATS = new Set([
  "mp4", "mov", "mkv", "webm", "wav", "m4a", "mobi", "dwg", "rar"
]);
```

### `desktop/requirements.txt`

```
PyQt6==6.7.1
Pillow==10.4.0
pillow-heif==0.18.0
pdf2docx==0.5.8
pymupdf==1.24.11
python-docx==1.1.2
pdfplumber==0.11.4
openpyxl==3.1.5
pandas==2.2.3
cairosvg==2.7.1
imageio==2.35.1
imageio[ffmpeg]==2.35.1
ffmpeg-python==0.2.0
pydub==0.25.1
xmltodict==0.13.0
pyyaml==6.0.2
cryptography==43.0.3
fonttools==4.54.1
brotli==1.1.0
rarfile==4.2
pikepdf==9.3.0
ebooklib==0.18
markdown==3.7
weasyprint==62.3
ruff==0.6.9
pytest==8.3.3
pytest-qt==4.4.0
pyinstaller==6.11.0
```

---

## 12. Appendix B — Vercel Platform Constraints & Mitigations

| Constraint | Limit | Mitigation |
|------------|-------|------------|
| Request body size | 4.5MB | Enforce 4MB client-side; show DesktopCTA on exceed |
| Serverless execution timeout | 10s (Hobby) / 60s (Pro) | Use Pro plan; flag slow conversions (pdf→xlsx) with warning |
| Function memory | 1024MB (Pro) | Set in `vercel.json`; avoid loading entire file into memory when possible |
| ffmpeg binary | Not supported (too large) | Mark video/audio as desktop-only; block on web |
| LibreOffice binary | Not supported | Mark docx→pdf, pptx→pdf, dwg→pdf as desktop-only |
| No persistent storage | — | All conversions stateless; output returned as base64 in response |
| Cold starts | ~500ms–2s | No mitigation needed for file conversion use case |
| Concurrent function limit | 1000 (Pro) | Sufficient for expected traffic |

**Unsupported on web — show DesktopCTA instead:**
- mp4, mov, mkv, webm, gif → mp4
- wav, m4a → mp3
- mp4 → mp3
- mobi → epub
- dwg → pdf
- rar → zip (unrar binary)
- docx → pdf (LibreOffice)
- pptx → pdf (LibreOffice)

---

## 13. Appendix C — Design Tokens (from Stitch)

### Colors (dark mode)

| Token | Value |
|-------|-------|
| `surface` | `#131315` |
| `surface-container-low` | `#1b1b1d` |
| `surface-container` | `#1f1f21` |
| `surface-bright` | `#39393b` |
| `on-surface` | `#e4e2e4` |
| `on-surface-variant` | `#c1c6d7` |
| `primary` | `#adc6ff` |
| `primary-container` | `#4b8eff` |
| `on-primary` | `#002e69` |
| `secondary` | `#c2c1ff` |
| `secondary-container` | `#3834b6` |
| `tertiary` | `#47e266` |
| `error` | `#ffb4ab` |
| `outline` | `#8b90a0` |
| `outline-variant` | `#414755` |

### Typography

| Role | Font | Size | Weight | Line Height |
|------|------|------|--------|-------------|
| Display | Inter | 48px | 700 | 56px |
| Headline LG | Inter | 32px | 600 | 40px |
| Headline LG Mobile | Inter | 24px | 600 | 32px |
| Headline MD | Inter | 20px | 600 | 28px |
| Body LG | Inter | 18px | 400 | 28px |
| Body MD | Inter | 16px | 400 | 24px |
| Label MD | Inter | 14px | 500 | 20px |
| Label SM | Inter | 12px | 600 | 16px |

### Spacing

| Token | Value |
|-------|-------|
| `xs` | 4px |
| `sm` | 12px |
| `base` | 8px |
| `md` | 24px |
| `lg` | 48px |
| `xl` | 80px |
| `gutter` | 24px |
| `margin` | 32px |

### Rounded corners

| Token | Value |
|-------|-------|
| `sm` | 4px |
| `DEFAULT` | 8px |
| `md` | 12px |
| `lg` | 16px |
| `xl` | 24px |
| `full` | 9999px |

---

## Setup Execution Order

```
1. Phase 0  → Repo, Git, .antigravity/, branch protection
2. Phase 1  → Design tokens, CSS variables, QSS themes
3. Phase 2  → Shared engine (validator first, then all converters, then router)
4. Phase 3  → Web app (serverless endpoint, DropZone, size enforcement, DesktopCTA)
5. Phase 4  → Desktop app (main window, threading, QSS, format selector)
6. Phase 5  → Desktop editor + compressor features
7. Phase 7  → CI/CD pipelines (set up early, run on every PR)
8. Phase 8  → Tests (write alongside each module, not after)
9. Phase 6  → Packaging (last, once features are stable)
```
