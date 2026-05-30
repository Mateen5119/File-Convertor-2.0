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
# Convert App — Roadmap Part 2
## Implementations, Components, Configs, READMEs, Release Checklist

> Continuation of `ROADMAP.md`. Read Part 1 first.

---

## Table of Contents

14. [Exact CSS & Tailwind Config (from Stitch)](#14-exact-css--tailwind-config-from-stitch)
15. [Web Components — Full Implementations](#15-web-components--full-implementations)
16. [Engine Module Implementations](#16-engine-module-implementations)
17. [web/requirements.txt for Vercel](#17-webrequirementstxt-for-vercel)
18. [Desktop QSS — Complete Themes](#18-desktop-qss--complete-themes)
19. [Desktop UI — Complete Widgets](#19-desktop-ui--complete-widgets)
20. [Error Handling Catalog](#20-error-handling-catalog)
21. [README Templates](#21-readme-templates)
22. [Release Checklist](#22-release-checklist)

---

## 14. Exact CSS & Tailwind Config (from Stitch)

### `web/app/globals.css`

This is the **exact** implementation derived from Stitch's exported HTML. Use verbatim.

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ── Ambient Background (Level 0) ─────────────────────────────── */
body::before {
  content: "";
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background-image:
    linear-gradient(to right, rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  z-index: -2;
  pointer-events: none;
}

/* ── Ambient Blobs ────────────────────────────────────────────── */
.ambient-blob {
  position: fixed;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.1;
  z-index: -1;
  pointer-events: none;
}
.blob-1 { top: -10%; left: -10%; width: 50vw; height: 50vw; background: #4b8eff; }
.blob-2 { bottom: -20%; right: -10%; width: 60vw; height: 60vw; background: #c2c1ff; }

/* ── Glass System (Dark Mode default) ───────────────────────────
   Level 1 — Main pane / nav                                      */
.glass-pane {
  background: rgba(30, 30, 32, 0.7);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
/* Level 2 — Cards / queue rows */
.glass-card {
  background: rgba(40, 40, 42, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
/* Level 3 — Dropdowns / tooltips */
.glass-popover {
  background: rgba(50, 50, 52, 0.95);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

/* ── Glass System (Light Mode) ──────────────────────────────────*/
.light .glass-pane {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}
.light .glass-card {
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

/* ── Buttons ────────────────────────────────────────────────────*/
.glass-button-primary {
  background: rgba(75, 142, 255, 0.15);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(75, 142, 255, 0.3);
  color: #adc6ff;
  transition: all 0.2s ease;
  border-radius: 1rem;
  padding: 0.5rem 1.5rem;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}
.glass-button-primary:hover {
  background: rgba(75, 142, 255, 0.25);
  border-color: rgba(75, 142, 255, 0.5);
  transform: translateY(-1px);
}
.glass-button-primary:active {
  transform: scale(0.98);
}

/* ── Drop Zone ──────────────────────────────────────────────────*/
.drop-zone {
  border: 2px dashed rgba(173, 198, 255, 0.3);
  transition: all 0.3s ease;
  border-radius: 1.5rem;
}
.drop-zone:hover,
.drop-zone.drag-active {
  border-color: #adc6ff;
  background: rgba(173, 198, 255, 0.05);
}

/* ── Inputs ─────────────────────────────────────────────────────*/
.sleek-input {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  color: #e4e2e4;
  padding: 0.5rem 1rem;
  transition: all 0.2s ease;
}
.sleek-input:focus {
  border-color: #4b8eff;
  box-shadow: inset 0 2px 4px rgba(75, 142, 255, 0.1);
  outline: none;
}
.sleek-input option {
  background: #131315;
  color: #e4e2e4;
}

/* ── Custom Scrollbar ───────────────────────────────────────────*/
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.2); }
```

---

### `web/tailwind.config.ts`

```ts
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // ── Stitch exact tokens ───────────────────────────────
        "surface":                  "#131315",
        "surface-dim":              "#131315",
        "surface-bright":           "#39393b",
        "surface-container-lowest": "#0e0e10",
        "surface-container-low":    "#1b1b1d",
        "surface-container":        "#1f1f21",
        "surface-container-high":   "#2a2a2c",
        "surface-container-highest":"#353437",
        "on-surface":               "#e4e2e4",
        "on-surface-variant":       "#c1c6d7",
        "inverse-surface":          "#e4e2e4",
        "inverse-on-surface":       "#303032",
        "outline":                  "#8b90a0",
        "outline-variant":          "#414755",
        "surface-tint":             "#adc6ff",
        "primary":                  "#adc6ff",
        "on-primary":               "#002e69",
        "primary-container":        "#4b8eff",
        "on-primary-container":     "#00285c",
        "inverse-primary":          "#005bc1",
        "secondary":                "#c2c1ff",
        "on-secondary":             "#1c0b9f",
        "secondary-container":      "#3834b6",
        "on-secondary-container":   "#b2b1ff",
        "tertiary":                 "#47e266",
        "on-tertiary":              "#003910",
        "tertiary-container":       "#00a73e",
        "on-tertiary-container":    "#00320d",
        "error":                    "#ffb4ab",
        "on-error":                 "#690005",
        "error-container":          "#93000a",
        "on-error-container":       "#ffdad6",
        "background":               "#131315",
        "on-background":            "#e4e2e4",
        "surface-variant":          "#353437",
      },
      fontFamily: {
        "display":           ["Inter", "sans-serif"],
        "headline-lg":       ["Inter", "sans-serif"],
        "headline-lg-mobile":["Inter", "sans-serif"],
        "headline-md":       ["Inter", "sans-serif"],
        "body-lg":           ["Inter", "sans-serif"],
        "body-md":           ["Inter", "sans-serif"],
        "label-md":          ["Inter", "sans-serif"],
        "label-sm":          ["Inter", "sans-serif"],
      },
      fontSize: {
        "display":            ["48px", { lineHeight: "56px",  letterSpacing: "-0.02em", fontWeight: "700" }],
        "headline-lg":        ["32px", { lineHeight: "40px",  letterSpacing: "-0.01em", fontWeight: "600" }],
        "headline-lg-mobile": ["24px", { lineHeight: "32px",  letterSpacing: "-0.01em", fontWeight: "600" }],
        "headline-md":        ["20px", { lineHeight: "28px",  fontWeight: "600" }],
        "body-lg":            ["18px", { lineHeight: "28px",  fontWeight: "400" }],
        "body-md":            ["16px", { lineHeight: "24px",  fontWeight: "400" }],
        "label-md":           ["14px", { lineHeight: "20px",  letterSpacing: "0.01em", fontWeight: "500" }],
        "label-sm":           ["12px", { lineHeight: "16px",  letterSpacing: "0.05em", fontWeight: "600" }],
      },
      borderRadius: {
        "sm":  "0.25rem",
        "DEFAULT": "0.5rem",
        "md":  "0.75rem",
        "lg":  "1rem",
        "xl":  "1.5rem",
        "full":"9999px",
      },
      spacing: {
        "xs":     "4px",
        "sm":     "12px",
        "base":   "8px",
        "md":     "24px",
        "lg":     "48px",
        "xl":     "80px",
        "gutter": "24px",
        "margin": "32px",
      },
      maxWidth: {
        "app": "1200px",
      },
    },
  },
  plugins: [],
};

export default config;
```

---

## 15. Web Components — Full Implementations

### `web/components/DropZone.tsx`

```tsx
"use client";

import { useCallback, useRef, useState } from "react";
import { checkFileSizeLimit } from "@/lib/validate";
import { WEB_UNSUPPORTED_FORMATS, WEB_FILE_SIZE_LIMIT_LABEL } from "@/lib/constants";
import DesktopCTA from "./DesktopCTA";
import FileChip from "./ui/FileChip";

type QueuedFile = {
  file: File;
  sourceExt: string;
  targetExt: string;
  status: "pending" | "converting" | "done" | "error";
  resultUrl?: string;
  error?: string;
};

export default function DropZone() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragActive, setDragActive] = useState(false);
  const [showSizeCTA, setShowSizeCTA] = useState(false);
  const [queue, setQueue] = useState<QueuedFile[]>([]);

  const addFiles = useCallback((files: FileList | File[]) => {
    const arr = Array.from(files);
    setShowSizeCTA(false);

    for (const file of arr) {
      const ext = file.name.split(".").pop()?.toLowerCase() ?? "";

      // Block unsupported-on-web formats immediately
      if (WEB_UNSUPPORTED_FORMATS.has(ext)) {
        setShowSizeCTA(true);
        continue;
      }

      // Block oversized files
      const { valid, showDesktopCTA } = checkFileSizeLimit(file);
      if (!valid) {
        setShowSizeCTA(showDesktopCTA);
        continue;
      }

      setQueue((prev) => [
        ...prev,
        { file, sourceExt: ext, targetExt: "", status: "pending" },
      ]);
    }
  }, []);

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files.length) addFiles(e.dataTransfer.files);
  };

  const onDragOver = (e: React.DragEvent) => { e.preventDefault(); setDragActive(true); };
  const onDragLeave = () => setDragActive(false);
  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) addFiles(e.target.files);
  };

  const updateTarget = (index: number, targetExt: string) => {
    setQueue((prev) => prev.map((item, i) => i === index ? { ...item, targetExt } : item));
  };

  const removeFromQueue = (index: number) => {
    setQueue((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="flex flex-col gap-md w-full">
      {/* Drop Zone */}
      <div
        className={`drop-zone glass-card flex flex-col items-center justify-center
          min-h-[250px] cursor-pointer p-md select-none
          ${dragActive ? "drag-active" : ""}`}
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onClick={() => inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          multiple
          className="hidden"
          onChange={onInputChange}
        />
        <span className="material-symbols-outlined text-primary text-5xl mb-sm">
          upload_file
        </span>
        <p className="text-body-lg text-on-surface font-semibold">
          Drag &amp; Drop files here
        </p>
        <p className="text-label-md text-outline mt-xs">
          or click to browse &mdash; max {WEB_FILE_SIZE_LIMIT_LABEL} per file
        </p>
      </div>

      {/* Desktop CTA (shown on size limit hit or unsupported format) */}
      {showSizeCTA && <DesktopCTA />}

      {/* Queue */}
      {queue.length > 0 && (
        <ConversionQueue
          queue={queue}
          onUpdateTarget={updateTarget}
          onRemove={removeFromQueue}
          onConvertAll={() => {/* trigger conversion loop */}}
        />
      )}
    </div>
  );
}
```

---

### `web/components/ConversionQueue.tsx`

```tsx
"use client";

import FormatSelector from "./FormatSelector";
import ProgressBar from "./ProgressBar";
import FileChip from "./ui/FileChip";

type QueuedFile = {
  file: File;
  sourceExt: string;
  targetExt: string;
  status: "pending" | "converting" | "done" | "error";
  progress?: number;
  resultUrl?: string;
  error?: string;
};

type Props = {
  queue: QueuedFile[];
  onUpdateTarget: (index: number, targetExt: string) => void;
  onRemove: (index: number) => void;
  onConvertAll: () => void;
};

export default function ConversionQueue({ queue, onUpdateTarget, onRemove, onConvertAll }: Props) {
  return (
    <div className="glass-card rounded-xl p-md flex flex-col gap-sm">
      <div className="flex items-center justify-between">
        <p className="text-label-md text-on-surface-variant uppercase tracking-wider">
          Queue ({queue.length})
        </p>
        <button className="glass-button-primary text-label-md" onClick={onConvertAll}>
          Convert All
          <span className="material-symbols-outlined text-base ml-xs align-middle">
            arrow_forward
          </span>
        </button>
      </div>

      {queue.map((item, i) => (
        <div
          key={i}
          className="glass-card rounded-lg p-sm flex items-center gap-sm"
        >
          {/* File type chip */}
          <FileChip ext={item.sourceExt} status={item.status} />

          {/* File name + progress */}
          <div className="flex-grow min-w-0">
            <p className="text-body-md text-on-surface truncate">{item.file.name}</p>
            <p className="text-label-sm text-outline">
              {(item.file.size / 1024).toFixed(0)} KB
            </p>
            {item.status === "converting" && (
              <ProgressBar value={item.progress ?? 0} />
            )}
            {item.status === "done" && (
              <p className="text-label-sm text-tertiary mt-xs">
                ✓ Ready to download
              </p>
            )}
            {item.status === "error" && (
              <p className="text-label-sm text-error mt-xs">{item.error}</p>
            )}
          </div>

          {/* Format selector */}
          {item.status === "pending" && (
            <FormatSelector
              sourceExt={item.sourceExt}
              value={item.targetExt}
              onChange={(ext) => onUpdateTarget(i, ext)}
            />
          )}

          {/* Download or close */}
          {item.status === "done" && item.resultUrl ? (
            <a
              href={item.resultUrl}
              download
              className="glass-button-primary text-label-md"
            >
              Download
            </a>
          ) : (
            <button
              className="text-outline hover:text-error transition-colors"
              onClick={() => onRemove(i)}
            >
              <span className="material-symbols-outlined text-base">close</span>
            </button>
          )}
        </div>
      ))}
    </div>
  );
}
```

---

### `web/components/FormatSelector.tsx`

```tsx
"use client";

import { CONVERSION_TARGETS } from "@/lib/constants";

type Props = {
  sourceExt: string;
  value: string;
  onChange: (ext: string) => void;
};

export default function FormatSelector({ sourceExt, value, onChange }: Props) {
  const targets = CONVERSION_TARGETS[sourceExt] ?? [];

  if (targets.length === 0) {
    return <span className="text-label-sm text-error">Unsupported on web</span>;
  }

  return (
    <select
      className="sleek-input text-label-md min-w-[80px]"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    >
      <option value="" disabled>to</option>
      {targets.map((t) => (
        <option key={t} value={t}>{t.toUpperCase()}</option>
      ))}
    </select>
  );
}
```

---

### `web/components/ProgressBar.tsx`

```tsx
type Props = { value: number }; // 0–100

export default function ProgressBar({ value }: Props) {
  return (
    <div className="w-full bg-surface-container rounded-full h-1.5 mt-xs overflow-hidden">
      <div
        className="bg-primary h-full rounded-full transition-all duration-300 ease-linear"
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  );
}
```

---

### `web/components/DesktopCTA.tsx`

```tsx
import { DESKTOP_DOWNLOAD_URL } from "@/lib/constants";

export default function DesktopCTA() {
  return (
    <div className="glass-card rounded-xl p-md flex items-center justify-between gap-md">
      <div className="flex items-center gap-sm">
        <span className="material-symbols-outlined text-primary text-3xl">desktop_mac</span>
        <div>
          <p className="text-headline-md text-on-surface">
            Get SwiftConvert for Desktop
          </p>
          <p className="text-label-md text-outline">
            No ads, unlimited file sizes, offline processing.
          </p>
        </div>
      </div>
      <a href={DESKTOP_DOWNLOAD_URL} className="glass-button-primary whitespace-nowrap">
        Download Free
        <span className="material-symbols-outlined text-base ml-xs align-middle">
          download
        </span>
      </a>
    </div>
  );
}
```

---

### `web/components/ui/FileChip.tsx`

```tsx
type Status = "pending" | "converting" | "done" | "error";

const COLOR: Record<Status, string> = {
  pending:    "bg-primary/10 text-primary border border-primary/30",
  converting: "bg-secondary-container/20 text-secondary border border-secondary/30",
  done:       "bg-tertiary-container/20 text-tertiary border border-tertiary/30",
  error:      "bg-error-container/30 text-error border border-red-500/30",
};

type Props = { ext: string; status: Status };

export default function FileChip({ ext, status }: Props) {
  return (
    <span className={`text-label-sm px-2 py-0.5 rounded-md uppercase tracking-widest
      flex-shrink-0 ${COLOR[status]}`}>
      {ext}
    </span>
  );
}
```

---

### `web/components/AdSlot.tsx`

```tsx
type Props = { size: "300x250" | "160x600" };

export default function AdSlot({ size }: Props) {
  const [w, h] = size.split("x").map(Number);
  return (
    <div
      data-ad-slot={size}
      className="glass-card rounded-xl flex items-center justify-center
        text-outline text-label-sm flex-shrink-0"
      style={{ width: w, height: h }}
    >
      <div className="flex flex-col items-center gap-xs opacity-40">
        <span className="material-symbols-outlined">campaign</span>
        Advertisement
      </div>
    </div>
  );
}
```

---

### `web/app/page.tsx`

```tsx
import DropZone from "@/components/DropZone";
import AdSlot from "@/components/AdSlot";
import DesktopCTA from "@/components/DesktopCTA";

export default function Home() {
  return (
    <>
      {/* Ambient blobs (behind everything) */}
      <div className="ambient-blob blob-1" />
      <div className="ambient-blob blob-2" />

      {/* Nav */}
      <header className="glass-pane sticky top-0 z-10 px-margin py-sm flex items-center justify-between">
        <span className="text-headline-md text-on-surface font-bold">SwiftConvert</span>
        <nav className="flex gap-md text-label-md text-outline">
          <a href="#" className="hover:text-on-surface transition-colors">Tools</a>
          <a href="#" className="hover:text-on-surface transition-colors">Pricing</a>
          <a href="#" className="hover:text-on-surface transition-colors">Help</a>
        </nav>
        <button className="glass-button-primary">Sign In</button>
      </header>

      {/* Hero */}
      <main className="max-w-app mx-auto px-gutter py-lg">
        <div className="text-center mb-lg">
          <h1 className="text-display text-on-surface mb-sm">
            Effortless File Conversion.
          </h1>
          <p className="text-body-lg text-outline max-w-xl mx-auto">
            Transform your documents, images, and media instantly.
            Drag, drop, and done — with uncompromising precision.
          </p>
        </div>

        {/* Three-column layout: ad | workspace | ad */}
        <div className="flex items-start gap-gutter justify-center">
          {/* Left ad (hidden on mobile) */}
          <div className="hidden lg:block flex-shrink-0">
            <AdSlot size="160x600" />
          </div>

          {/* Center workspace */}
          <div className="flex-grow max-w-2xl flex flex-col gap-md">
            <DropZone />
            <DesktopCTA />
          </div>

          {/* Right ad (hidden on mobile) */}
          <div className="hidden lg:block flex-shrink-0">
            <AdSlot size="160x600" />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="glass-pane mt-lg px-margin py-md flex items-center
        justify-between text-label-sm text-outline">
        <span>© 2026 SwiftConvert. Precision Processing.</span>
        <div className="flex gap-md">
          <a href="#" className="hover:text-on-surface transition-colors">Privacy Policy</a>
          <a href="#" className="hover:text-on-surface transition-colors">Terms of Service</a>
          <a href="#" className="hover:text-on-surface transition-colors">Contact</a>
        </div>
      </footer>
    </>
  );
}
```

---

### `web/lib/constants.ts`

```ts
export const WEB_FILE_SIZE_LIMIT_BYTES = 4 * 1024 * 1024; // 4MB
export const WEB_FILE_SIZE_LIMIT_LABEL = "4MB";
export const DESKTOP_DOWNLOAD_URL = "https://your-site.com/download"; // Update post-release

// Formats that require binaries (ffmpeg, LibreOffice, unrar) — not supported on web
export const WEB_UNSUPPORTED_FORMATS = new Set([
  "mp4", "mov", "mkv", "webm", "gif",
  "wav", "m4a",
  "mobi",
  "dwg",
  "rar",
  "docx",  // docx→pdf needs LibreOffice
  "pptx",
]);

// Maps source ext → allowed target exts on web
export const CONVERSION_TARGETS: Record<string, string[]> = {
  pdf:   ["docx", "xlsx"],
  docx:  [],          // desktop-only
  png:   ["jpg"],
  jpg:   ["png"],
  heic:  ["jpg"],
  webp:  ["png", "jpg"],
  svg:   ["png"],
  tiff:  ["jpg", "pdf"],
  csv:   ["xlsx"],
  json:  ["csv"],
  xml:   ["json"],
  yaml:  ["json"],
  md:    ["html", "pdf"],
  epub:  ["pdf"],
  pptx:  [],          // desktop-only
  ttf:   ["woff2"],
  otf:   ["woff2"],
  pem:   ["pfx", "crt"],
  mp4:   [],          // desktop-only
  mov:   [],          // desktop-only
  mkv:   [],          // desktop-only
  webm:  [],          // desktop-only
  wav:   [],          // desktop-only
  m4a:   [],          // desktop-only
  gif:   [],          // desktop-only
  rar:   [],          // desktop-only
  dwg:   [],          // desktop-only
  mobi:  [],          // desktop-only
};
```

---

## 16. Engine Module Implementations

### `shared/engine/document.py`

```python
import subprocess
import tempfile
import os
from pathlib import Path
from .validator import validate


def pdf_to_docx(data: bytes) -> bytes:
    validate(data, "pdf")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.pdf"
        dst = Path(tmp) / "output.docx"
        src.write_bytes(data)
        from pdf2docx import Converter
        cv = Converter(str(src))
        cv.convert(str(dst), start=0, end=None)
        cv.close()
        return dst.read_bytes()


def docx_to_pdf(data: bytes) -> bytes:
    """Uses LibreOffice Portable (desktop-only path). Set LO_BIN env var."""
    validate(data, "docx")
    lo_bin = os.environ.get("LO_BIN", "soffice")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.docx"
        src.write_bytes(data)
        subprocess.run(
            [lo_bin, "--headless", "--invisible", "--convert-to", "pdf",
             "--outdir", tmp, str(src)],
            check=True,
            timeout=45,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        out = Path(tmp) / "input.pdf"
        return out.read_bytes()


def md_to_html(data: bytes) -> bytes:
    validate(data, "md")
    import markdown
    html = markdown.markdown(data.decode("utf-8"), extensions=["tables", "fenced_code"])
    return html.encode("utf-8")


def md_to_pdf(data: bytes) -> bytes:
    validate(data, "md")
    with tempfile.TemporaryDirectory() as tmp:
        html_bytes = md_to_html(data)
        src = Path(tmp) / "input.html"
        dst = Path(tmp) / "output.pdf"
        src.write_bytes(html_bytes)
        from weasyprint import HTML
        HTML(filename=str(src)).write_pdf(str(dst))
        return dst.read_bytes()


def pptx_to_pdf(data: bytes) -> bytes:
    """LibreOffice Portable (desktop-only). Set LO_BIN env var."""
    validate(data, "pptx")
    lo_bin = os.environ.get("LO_BIN", "soffice")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.pptx"
        src.write_bytes(data)
        subprocess.run(
            [lo_bin, "--headless", "--invisible", "--convert-to", "pdf",
             "--outdir", tmp, str(src)],
            check=True, timeout=45,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        return (Path(tmp) / "input.pdf").read_bytes()


def epub_to_pdf(data: bytes) -> bytes:
    validate(data, "epub")
    with tempfile.TemporaryDirectory() as tmp:
        from ebooklib import epub
        from weasyprint import HTML
        book = epub.read_epub(data)          # type: ignore[attr-defined]
        html_parts = []
        for item in book.get_items_of_type(9):  # ITEM_DOCUMENT = 9
            html_parts.append(item.get_content().decode("utf-8", errors="ignore"))
        combined = "\n".join(html_parts)
        dst = Path(tmp) / "output.pdf"
        HTML(string=combined).write_pdf(str(dst))
        return dst.read_bytes()


def mobi_to_epub(data: bytes) -> bytes:
    raise NotImplementedError("mobi→epub requires KindleUnpack — desktop only, no DRM support")
```

---

### `shared/engine/image.py`

```python
import io
import tempfile
from pathlib import Path
from .validator import validate


def heic_to_jpg(data: bytes) -> bytes:
    validate(data, "heic")
    from pillow_heif import register_heif_opener
    register_heif_opener()
    from PIL import Image
    img = Image.open(io.BytesIO(data)).convert("RGB")
    out = io.BytesIO()
    img.save(out, "JPEG", quality=90)
    return out.getvalue()


def webp_to_png(data: bytes) -> bytes:
    validate(data, "webp")
    from PIL import Image
    img = Image.open(io.BytesIO(data)).convert("RGBA")
    out = io.BytesIO()
    img.save(out, "PNG")
    return out.getvalue()


def webp_to_jpg(data: bytes) -> bytes:
    validate(data, "webp")
    from PIL import Image
    img = Image.open(io.BytesIO(data)).convert("RGB")
    out = io.BytesIO()
    img.save(out, "JPEG", quality=90)
    return out.getvalue()


def png_to_jpg(data: bytes, quality: int = 90) -> bytes:
    validate(data, "png")
    from PIL import Image
    img = Image.open(io.BytesIO(data)).convert("RGB")
    out = io.BytesIO()
    img.save(out, "JPEG", quality=quality)
    return out.getvalue()


def svg_to_png(data: bytes) -> bytes:
    import cairosvg
    return cairosvg.svg2png(bytestring=data)


def tiff_to_jpg(data: bytes) -> bytes:
    from PIL import Image
    img = Image.open(io.BytesIO(data)).convert("RGB")
    out = io.BytesIO()
    img.save(out, "JPEG", quality=90)
    return out.getvalue()


def tiff_to_pdf(data: bytes) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        from PIL import Image
        from weasyprint import HTML
        img = Image.open(io.BytesIO(data))
        frames = []
        try:
            while True:
                frames.append(img.copy().convert("RGB"))
                img.seek(img.tell() + 1)
        except EOFError:
            pass
        if len(frames) == 1:
            out = io.BytesIO()
            frames[0].save(out, "PDF")
            return out.getvalue()
        else:
            out = io.BytesIO()
            frames[0].save(out, "PDF", save_all=True, append_images=frames[1:])
            return out.getvalue()


def gif_to_mp4(data: bytes) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.gif"
        dst = Path(tmp) / "output.mp4"
        src.write_bytes(data)
        import ffmpeg
        (
            ffmpeg
            .input(str(src))
            .output(str(dst), vcodec="libx264", pix_fmt="yuv420p", movflags="faststart")
            .overwrite_output()
            .run(quiet=True)
        )
        return dst.read_bytes()
```

---

### `shared/engine/data.py`

```python
import io
import json
import csv
import xml.etree.ElementTree as ET
from .validator import validate


def csv_to_xlsx(data: bytes) -> bytes:
    import openpyxl
    reader = csv.reader(io.StringIO(data.decode("utf-8-sig")))
    wb = openpyxl.Workbook()
    ws = wb.active
    for row in reader:
        ws.append(row)
    out = io.BytesIO()
    wb.save(out)
    return out.getvalue()


def pdf_to_xlsx(data: bytes) -> bytes:
    validate(data, "pdf")
    import pdfplumber
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    ws.append([cell or "" for cell in row])
    out = io.BytesIO()
    wb.save(out)
    return out.getvalue()


def json_to_csv(data: bytes) -> bytes:
    rows = json.loads(data.decode("utf-8"))
    if not isinstance(rows, list):
        raise ValueError("JSON must be a top-level array of objects")
    out = io.StringIO()
    if rows:
        writer = csv.DictWriter(out, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return out.getvalue().encode("utf-8")


def xml_to_json(data: bytes) -> bytes:
    import xmltodict
    parsed = xmltodict.parse(data.decode("utf-8"))
    return json.dumps(parsed, indent=2, ensure_ascii=False).encode("utf-8")


def yaml_to_json(data: bytes) -> bytes:
    import yaml
    parsed = yaml.safe_load(data.decode("utf-8"))
    return json.dumps(parsed, indent=2, ensure_ascii=False).encode("utf-8")
```

---

### `shared/engine/security.py`

```python
from .validator import validate


def pem_to_pfx(data: bytes, password: bytes = b"changeme") -> bytes:
    from cryptography.hazmat.primitives.serialization import (
        pkcs12, load_pem_private_key, Encoding, PrivateFormat, NoEncryption
    )
    from cryptography.x509 import load_pem_x509_certificate
    # Expect combined PEM: key + cert
    lines = data.decode().split("-----")
    key_pem = b""
    cert_pem = b""
    for i, chunk in enumerate(lines):
        if "PRIVATE KEY" in chunk:
            key_pem = ("-----" + chunk + "-----").encode()
        if "CERTIFICATE" in chunk and "BEGIN" not in chunk and "END" not in chunk:
            cert_pem = ("-----BEGIN CERTIFICATE-----" + chunk + "-----END CERTIFICATE-----").encode()
    private_key = load_pem_private_key(key_pem, password=None)
    cert = load_pem_x509_certificate(cert_pem)
    pfx = pkcs12.serialize_key_and_certificates(
        name=b"convert", key=private_key, cert=cert, cas=None,
        encryption_algorithm=pkcs12.BestAvailableEncryption(password)
    )
    return pfx


def pem_to_crt(data: bytes) -> bytes:
    # PEM cert is already .crt-compatible — extract and return the cert block only
    import re
    match = re.search(b"(-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----)", data, re.DOTALL)
    if not match:
        raise ValueError("No certificate block found in PEM")
    return match.group(1)
```

---

### `shared/engine/font.py`

```python
def ttf_to_woff2(data: bytes) -> bytes:
    import io
    from fonttools.ttLib import TTFont
    font = TTFont(io.BytesIO(data))
    out = io.BytesIO()
    font.flavor = "woff2"
    font.save(out)
    return out.getvalue()


def otf_to_woff2(data: bytes) -> bytes:
    return ttf_to_woff2(data)  # same process
```

---

### `shared/engine/archive.py`

```python
import io
import zipfile
import tempfile
from pathlib import Path
from .validator import validate


def rar_to_zip(data: bytes) -> bytes:
    validate(data, "rar")
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
```

---

## 17. `web/requirements.txt` for Vercel

Vercel bundles Python dependencies listed in `web/requirements.txt` into each serverless function. Keep this minimal — every package increases cold start time and function size.

```
# ── Core (web-safe only, no ffmpeg/LibreOffice binaries) ──────
pdf2docx==0.5.8
pypdf==4.3.1
pdfplumber==0.11.4
Pillow==10.4.0
pillow-heif==0.18.0
cairosvg==2.7.1
openpyxl==3.1.5
markdown==3.7
weasyprint==62.3
cryptography==43.0.3
fonttools==4.54.1
brotli==1.1.0
xmltodict==0.13.0
pyyaml==6.0.2
ebooklib==0.18

# ── No ffmpeg-python, pydub, rarfile, pymupdf ──────────────────
# These require system binaries not available on Vercel.
# Their format pairs are blocked in WEB_UNSUPPORTED_FORMATS.
```

> **Note:** `cairosvg` requires `libcairo` which is available in Vercel's Python 3.12 runtime. If it fails in deployment, replace with `svglib + reportlab` as a fallback.

---

## 18. Desktop QSS — Complete Themes

### `desktop/ui/styles/dark.qss`

```css
/* ── Base ──────────────────────────────────────────────────── */
QMainWindow, QWidget {
  background-color: #131315;
  color: #e4e2e4;
  font-family: "Inter";
  font-size: 14px;
}

/* ── Title Bar ─────────────────────────────────────────────── */
QWidget#titleBar {
  background-color: rgba(27, 27, 29, 0.95);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  min-height: 38px;
  max-height: 38px;
}

/* macOS-style traffic lights */
QToolButton#btnClose  { background-color: #ff5f56; border-radius: 6px; border: 1px solid #e0443e; }
QToolButton#btnMin    { background-color: #ffbd2e; border-radius: 6px; border: 1px solid #dea123; }
QToolButton#btnMax    { background-color: #27c93f; border-radius: 6px; border: 1px solid #1aab29; }
QToolButton#btnClose, QToolButton#btnMin, QToolButton#btnMax {
  min-width: 12px; max-width: 12px;
  min-height: 12px; max-height: 12px;
}
QToolButton#btnClose:hover { background-color: #ff3b30; }
QToolButton#btnMin:hover   { background-color: #ffcc00; }
QToolButton#btnMax:hover   { background-color: #34c759; }

/* ── Glass Pane (Level 1) ──────────────────────────────────── */
QWidget#glassPane {
  background-color: rgba(27, 27, 29, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 0;
}

/* ── Glass Card (Level 2) ──────────────────────────────────── */
QWidget#glassCard {
  background-color: rgba(42, 42, 44, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
}

QWidget#glassCardRow {
  background-color: rgba(42, 42, 44, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}

/* ── Drop Zone ─────────────────────────────────────────────── */
QWidget#dropZone {
  background-color: rgba(173, 198, 255, 0.02);
  border: 2px dashed rgba(173, 198, 255, 0.3);
  border-radius: 24px;
  min-height: 220px;
}

QWidget#dropZone:hover,
QWidget#dropZone[dragActive="true"] {
  border-color: #adc6ff;
  background-color: rgba(173, 198, 255, 0.05);
}

/* ── Buttons ───────────────────────────────────────────────── */
QPushButton#primaryBtn {
  background-color: rgba(75, 142, 255, 0.15);
  color: #adc6ff;
  border: 1px solid rgba(75, 142, 255, 0.3);
  border-radius: 16px;
  padding: 8px 24px;
  font-size: 14px;
  font-weight: 500;
}

QPushButton#primaryBtn:hover {
  background-color: rgba(75, 142, 255, 0.25);
  border-color: rgba(75, 142, 255, 0.5);
}

QPushButton#primaryBtn:pressed { background-color: rgba(75, 142, 255, 0.35); }

QPushButton#dangerBtn {
  background-color: transparent;
  color: #8b90a0;
  border: none;
  border-radius: 8px;
  padding: 4px;
}
QPushButton#dangerBtn:hover { color: #ffb4ab; }

/* ── ComboBox (Format Selector) ────────────────────────────── */
QComboBox {
  background-color: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  color: #e4e2e4;
  padding: 4px 12px;
  min-width: 80px;
}

QComboBox:focus { border-color: #4b8eff; }

QComboBox::drop-down { border: none; }

QComboBox QAbstractItemView {
  background-color: rgba(50, 50, 52, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  color: #e4e2e4;
  selection-background-color: rgba(75, 142, 255, 0.15);
  selection-color: #adc6ff;
}

/* ── Progress Bar ──────────────────────────────────────────── */
QProgressBar {
  background-color: rgba(255, 255, 255, 0.05);
  border: none;
  border-radius: 9999px;
  max-height: 6px;
  text-align: center;
  color: transparent;
}

QProgressBar::chunk {
  background-color: #adc6ff;
  border-radius: 9999px;
}

/* ── Labels ────────────────────────────────────────────────── */
QLabel#labelOutline  { color: #8b90a0; font-size: 12px; }
QLabel#labelPrimary  { color: #adc6ff; }
QLabel#labelTertiary { color: #47e266; font-size: 12px; }
QLabel#labelError    { color: #ffb4ab; font-size: 12px; }

/* ── Tab Bar ───────────────────────────────────────────────── */
QTabBar::tab {
  background-color: transparent;
  color: #8b90a0;
  border: none;
  padding: 8px 20px;
  font-size: 14px;
  font-weight: 500;
}

QTabBar::tab:selected {
  color: #adc6ff;
  border-bottom: 2px solid #adc6ff;
}

QTabBar::tab:hover { color: #e4e2e4; }

QTabWidget::pane {
  border: none;
  background-color: transparent;
}

/* ── Scrollbar ─────────────────────────────────────────────── */
QScrollBar:vertical {
  background: transparent;
  width: 6px;
  margin: 0;
}

QScrollBar::handle:vertical {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  min-height: 20px;
}

QScrollBar::handle:vertical:hover { background: rgba(255, 255, 255, 0.2); }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
```

### `desktop/ui/styles/light.qss`

Replace the dark values with light equivalents (same structure):

```css
QMainWindow, QWidget { background-color: #f5f5f7; color: #1c1c1e; }
QWidget#glassCard   { background-color: rgba(255, 255, 255, 0.85); border-color: rgba(0,0,0,0.08); }
QWidget#dropZone    { border-color: rgba(0, 93, 193, 0.3); }
QWidget#dropZone:hover, QWidget#dropZone[dragActive="true"] {
  border-color: #005bc1;
  background-color: rgba(0, 93, 193, 0.04);
}
QPushButton#primaryBtn { background-color: rgba(0, 93, 193, 0.1); color: #005bc1; border-color: rgba(0, 93, 193, 0.3); }
QProgressBar::chunk    { background-color: #005bc1; }
QComboBox:focus        { border-color: #005bc1; }
QLabel#labelPrimary    { color: #005bc1; }
```

---

## 19. Desktop UI — Complete Widgets

### `desktop/ui/main_window.py`

```python
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QToolButton, QSizePolicy
)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QIcon

from .drop_zone import DropZone
from .conversion_queue import ConversionQueueWidget
from .format_selector import FormatSelectorWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.settings = QSettings("YourOrg", "Convert")
        self.setWindowTitle("SwiftConvert")
        self.setMinimumSize(900, 620)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # custom title bar
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        central = QWidget()
        central.setObjectName("glassPane")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_title_bar())
        root.addWidget(self._build_tabs())

    def _build_title_bar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("titleBar")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)

        # Traffic lights
        for name, obj_name in [("✕", "btnClose"), ("−", "btnMin"), ("□", "btnMax")]:
            btn = QToolButton()
            btn.setObjectName(obj_name)
            btn.setText("")
            layout.addWidget(btn)

        layout.addStretch()

        title = QLabel("SwiftConvert")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addStretch()

        # Theme toggle
        theme_btn = QToolButton()
        theme_btn.setText("☀" if self._current_theme() == "dark" else "●")
        theme_btn.clicked.connect(self._toggle_theme)
        layout.addWidget(theme_btn)

        return bar

    def _build_tabs(self) -> QTabWidget:
        tabs = QTabWidget()
        tabs.setDocumentMode(True)

        # ── Convert tab ──────────────────────────────────────
        convert_page = QWidget()
        layout = QVBoxLayout(convert_page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.drop_zone = DropZone()
        self.queue_widget = ConversionQueueWidget()
        self.drop_zone.filesDropped.connect(self.queue_widget.add_files)

        layout.addWidget(self.drop_zone)
        layout.addWidget(self.queue_widget)
        tabs.addTab(convert_page, "Convert")

        # ── Edit tab ─────────────────────────────────────────
        from ..features.editor.pdf_editor import PDFEditorWidget
        tabs.addTab(PDFEditorWidget(), "Edit")

        # ── Compress tab ─────────────────────────────────────
        from ..features.compressor import CompressorWidget
        tabs.addTab(CompressorWidget(), "Compress")

        return tabs

    def _current_theme(self) -> str:
        return self.settings.value("theme", "dark")

    def _toggle_theme(self) -> None:
        from PyQt6.QtWidgets import QApplication
        new_theme = "light" if self._current_theme() == "dark" else "dark"
        self.settings.setValue("theme", new_theme)
        with open(f"ui/styles/{new_theme}.qss", "r", encoding="utf-8") as f:
            QApplication.instance().setStyleSheet(f.read())  # type: ignore
```

---

### `desktop/ui/drop_zone.py`

```python
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from pathlib import Path


class DropZone(QWidget):
    filesDropped = pyqtSignal(list)  # emits list[Path]

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("dropZone")
        self.setAcceptDrops(True)
        self.setMinimumHeight(220)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("⬆")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 36px; color: #adc6ff;")

        title = QLabel("Drag & Drop files here")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        subtitle = QLabel("or click to browse — no file size limit on desktop")
        subtitle.setObjectName("labelOutline")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(subtitle)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("dragActive", "true")
            self.style().unpolish(self)
            self.style().polish(self)

    def dragLeaveEvent(self, _) -> None:
        self.setProperty("dragActive", "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def dropEvent(self, event: QDropEvent) -> None:
        self.setProperty("dragActive", "false")
        self.style().unpolish(self)
        self.style().polish(self)
        paths = [Path(url.toLocalFile()) for url in event.mimeData().urls()
                 if url.isLocalFile()]
        if paths:
            self.filesDropped.emit(paths)

    def mousePressEvent(self, _) -> None:
        from PyQt6.QtWidgets import QFileDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Select files")
        if files:
            self.filesDropped.emit([Path(f) for f in files])
```

---

### `desktop/ui/conversion_queue.py`

```python
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QProgressBar, QScrollArea, QComboBox
)
from PyQt6.QtCore import Qt
from pathlib import Path
from .format_selector import FormatSelectorWidget
from ..engine.worker import ConversionWorker


class QueueRow(QWidget):
    def __init__(self, path: Path, parent=None):
        super().__init__(parent)
        self.setObjectName("glassCardRow")
        self.path = path
        self.worker = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        ext = path.suffix.lstrip(".").upper()
        chip = QLabel(ext)
        chip.setFixedWidth(48)
        chip.setObjectName("labelPrimary")
        chip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chip.setStyleSheet("border: 1px solid rgba(173,198,255,0.3); border-radius:8px; padding:2px 4px;")

        info_col = QVBoxLayout()
        self.name_label = QLabel(path.name)
        self.name_label.setStyleSheet("font-size:14px; font-weight:500;")
        size_kb = path.stat().st_size // 1024
        self.meta_label = QLabel(f"{size_kb} KB")
        self.meta_label.setObjectName("labelOutline")
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setVisible(False)
        info_col.addWidget(self.name_label)
        info_col.addWidget(self.meta_label)
        info_col.addWidget(self.progress)

        self.format_sel = FormatSelectorWidget(path.suffix.lstrip(".").lower())

        self.convert_btn = QPushButton("Convert")
        self.convert_btn.setObjectName("primaryBtn")
        self.convert_btn.clicked.connect(self._start_conversion)

        layout.addWidget(chip)
        layout.addLayout(info_col, stretch=1)
        layout.addWidget(self.format_sel)
        layout.addWidget(self.convert_btn)

    def _start_conversion(self) -> None:
        from PyQt6.QtWidgets import QFileDialog
        target_fmt = self.format_sel.current_format()
        if not target_fmt:
            return
        out_path, _ = QFileDialog.getSaveFileName(
            self, "Save as", str(self.path.with_suffix(f".{target_fmt}")),
            f"*.{target_fmt}"
        )
        if not out_path:
            return

        data = self.path.read_bytes()
        source_fmt = self.path.suffix.lstrip(".")
        self.worker = ConversionWorker(data, source_fmt, target_fmt, out_path)
        self.worker.finished.connect(lambda _, p: self._on_done(p))
        self.worker.error.connect(self._on_error)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # indeterminate
        self.convert_btn.setEnabled(False)
        self.worker.start()

    def _on_done(self, out_path: str) -> None:
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        self.meta_label.setText("✓ Done")
        self.meta_label.setObjectName("labelTertiary")
        self.convert_btn.setEnabled(True)

    def _on_error(self, msg: str) -> None:
        self.progress.setVisible(False)
        self.meta_label.setText(f"✗ {msg}")
        self.meta_label.setObjectName("labelError")
        self.meta_label.style().unpolish(self.meta_label)
        self.meta_label.style().polish(self.meta_label)
        self.convert_btn.setEnabled(True)


class ConversionQueueWidget(QWidget):
    def __init__(self):
        super().__init__()
        outer = QVBoxLayout(self)
        header = QHBoxLayout()
        self.count_label = QLabel("Queue (0)")
        self.count_label.setObjectName("labelOutline")
        header.addWidget(self.count_label)
        outer.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(scroll.Shape.NoFrame)
        self.inner = QWidget()
        self.rows_layout = QVBoxLayout(self.inner)
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.setSpacing(8)
        self.rows_layout.addStretch()
        scroll.setWidget(self.inner)
        outer.addWidget(scroll)

    def add_files(self, paths: list[Path]) -> None:
        for p in paths:
            row = QueueRow(p)
            self.rows_layout.insertWidget(self.rows_layout.count() - 1, row)
        count = self.rows_layout.count() - 1  # minus stretch
        self.count_label.setText(f"Queue ({count})")
```

---

### `desktop/engine/worker.py`

```python
from PyQt6.QtCore import QThread, pyqtSignal


class ConversionWorker(QThread):
    finished = pyqtSignal(bytes, str)
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

---

## 20. Error Handling Catalog

### Web — API error responses

All errors from `web/api/convert.py` return JSON:

```json
{ "error": "ERROR_CODE", "message": "Human-readable description" }
```

| HTTP Status | Error Code | Cause | UI Behavior |
|-------------|------------|-------|-------------|
| 400 | `FILE_TOO_LARGE` | >4MB | Show DesktopCTA |
| 400 | `VALIDATION_ERROR` | Bad magic bytes or format mismatch | Show error chip on file row |
| 400 | `UNSUPPORTED_CONVERSION` | Invalid source→target pair | Show "Unsupported" label |
| 413 | (Vercel body limit) | >4.5MB body — caught before API | Show DesktopCTA |
| 500 | `CONVERSION_FAILED` | Library crash during conversion | Show error chip + "Try desktop app" |
| 504 | (Vercel timeout) | >60s execution | Show error + "Large file? Try desktop app" |

### Desktop — Worker error signals

`ConversionWorker.error` emits a string. Map known strings to friendly messages:

```python
ERROR_MESSAGES = {
    "File exceeds size limit":     "File is too large.",
    "File header does not match":  "File appears corrupted or wrong format.",
    "unsupported conversion":      "This conversion isn't supported.",
    "soffice":                     "LibreOffice not found. Check LO_BIN path in settings.",
    "No module named":             "A required library is missing. Reinstall the app.",
}

def friendly_error(raw: str) -> str:
    for key, msg in ERROR_MESSAGES.items():
        if key.lower() in raw.lower():
            return msg
    return f"Conversion failed: {raw}"
```

---

## 21. README Templates

### `README.md` (repo root)

```markdown
# SwiftConvert

File conversion app — web (Vercel) + desktop (Windows/PyQt6).

## Projects

| Directory | Description | Stack |
|-----------|-------------|-------|
| `web/`    | Hosted on Vercel | Next.js 15 + Vercel Python serverless |
| `desktop/`| Windows desktop app | Python 3.12 + PyQt6 |
| `shared/` | Conversion engine | Python 3.12 |

## Quick Start

### Web
```bash
cd web
npm install
npm run dev
```
Open http://localhost:3000

### Desktop
```bash
cd desktop
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
pythonw main.py
```

## Environment Variables

Copy `.env.example` → `.env.local` (web) or `.env` (desktop). Never commit `.env`.

## Supported Conversions

See [`Supported_file_conversion.md`](./Supported_file_conversion.md).

## Contributing

- Branch from `main`, prefix with `feat/`, `fix/`, or `chore/`
- Conventional Commits required
- PR requires 1 review + CI passing
```

---

### `web/README.md`

```markdown
# SwiftConvert — Web

## Stack
- Next.js 15 (App Router)
- TypeScript 5
- Tailwind CSS (Stitch design tokens)
- Vercel Python serverless (`api/`)

## Commands
| Command | Description |
|---------|-------------|
| `npm run dev` | Local dev server |
| `npm run build` | Production build |
| `npm run lint` | ESLint |

## Vercel Platform Limits
- Max file size: **4MB** (enforced client-side before upload)
- Max execution: **60s** (Pro plan)
- Unsupported formats (binary deps): see `lib/constants.ts → WEB_UNSUPPORTED_FORMATS`

## Environment
See `.env.example`.
```

---

### `desktop/README.md`

```markdown
# SwiftConvert — Desktop

## Stack
- Python 3.12
- PyQt6 (UI)
- PyInstaller (bundle)
- Inno Setup (installer)

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run (no console window)
```bash
pythonw main.py
```

## LibreOffice Portable
Required for: `docx→pdf`, `pptx→pdf`, `dwg→pdf`

1. Download [LibreOffice Portable](https://portableapps.com/apps/office/libreoffice_portable)
2. Extract to `desktop/libreoffice_portable/`
3. Set in `.env`: `LO_BIN=libreoffice_portable\App\libreoffice\program\soffice.exe`

`libreoffice_portable/` is in `.gitignore` — do not commit.

## Build Installer
```bash
pyinstaller build.spec --clean
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\setup.iss
```
Output: `installer\releases\ConvertSetup-x.x.x.exe`
```

---

## 22. Release Checklist

### Pre-release

- [ ] All tests passing (`pytest`, `npm run test`)
- [ ] No `ruff` / `eslint` errors
- [ ] `web/requirements.txt` dependencies audited (`pip-audit`)
- [ ] `web/package.json` dependencies audited (`npm audit`)
- [ ] `.env` files: no secrets committed (`git secrets --scan` or `gitleaks`)
- [ ] Vercel Pro plan active (for 60s timeout)
- [ ] `DESKTOP_DOWNLOAD_URL` in `web/lib/constants.ts` updated to real URL
- [ ] Version bumped in `desktop/installer/setup.iss` (`AppVersion=x.x.x`)
- [ ] Version bumped in `web/package.json`

### Web deploy

- [ ] Push to `main` → Vercel auto-deploys
- [ ] Verify preview URL loads without errors
- [ ] Test each supported web conversion pair with a real file
- [ ] Test file >4MB — confirm DesktopCTA appears and upload is blocked
- [ ] Test unsupported format (e.g., `.mp4`) — confirm DesktopCTA appears
- [ ] Check both dark and light mode on web

### Desktop build

- [ ] Activate venv, run `pip install -r requirements.txt --upgrade`
- [ ] Run `pyinstaller build.spec --clean`
- [ ] Test `dist/Convert/Convert.exe` launches with **no console window**
- [ ] Test all 27 conversion pairs with real files
- [ ] Test editor and compressor tabs
- [ ] Test LibreOffice path resolution (docx→pdf, pptx→pdf)
- [ ] Run `ISCC.exe installer/setup.iss`
- [ ] Install `ConvertSetup-x.x.x.exe` on a clean VM — verify install + launch
- [ ] Verify `Convert.exe` shows no console after install
- [ ] Upload installer to release hosting, update `DESKTOP_DOWNLOAD_URL`

### Post-release

- [ ] Tag release in GitHub: `git tag vx.x.x && git push origin vx.x.x`
- [ ] Update `CHANGELOG.md` (Conventional Commits → automated via `conventional-changelog`)
- [ ] Rotate any secrets if exposed during release process
- [ ] Monitor Vercel error dashboard for 24h after deploy
