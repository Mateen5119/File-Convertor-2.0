# Audit Report — SwiftConvert

## Severity Legend
- **[CRITICAL]** — Will cause runtime crash, data loss, or security breach
- **[HIGH]** — Will cause feature failure or broken behavior in production
- **[MEDIUM]** — Will cause degraded UX, partial failure, or technical debt
- **[LOW]** — Style, naming, or minor inconsistency

---

## 1. File Structure Issues

### 1.1 Brand & Project Naming Inconsistency [MEDIUM]
There is a major naming conflict between the roadmap files and the actual codebase:
- The roadmap describes the application as **SwiftConvert** (e.g., `ROADMAP_PART2.md` line 555: `Get SwiftConvert for Desktop`).
- The actual codebase has implemented the branding and labels as **File Harbor** (e.g., `web/app/page.tsx` line 15: `<span className="text-headline-md font-bold">File Harbor</span>`, `web/app/layout.tsx` line 6: `title: "File Harbor - Effortless File Conversion"`, `desktop/ui/main_window.py` line 51: `title = QLabel("File Harbor")`).

### 1.2 Binary Executable Naming Conflict [MEDIUM]
- In `ROADMAP.md` (lines 855 & 865), the PyInstaller configuration defines the output executable name as `name='Convert'` and output directory as `'Convert'`.
- In `desktop/build.spec` (lines 32 & 52), the actual implementation uses `name='FileHarbor'` and output directory `'FileHarbor'`. This causes a mismatch with the `setup.iss` script if developers expect the roadmap names.

### 1.3 Missing Assets Directory in Desktop Project [HIGH]
- In `desktop/build.spec` (line 11), the PyInstaller spec defines an asset bundling entry: `('assets/*', 'assets')`.
- However, there is **no `assets` directory** inside the `desktop/` workspace folder. This missing folder will cause PyInstaller to throw a build-time crash or compilation error, blocking the generation of the standalone bundle.

### 1.4 Broken Init Copy Reference in Phase 0 [LOW]
- In `ROADMAP.md` (line 178), the Phase 0 bootstrap script instructs the developer to execute: `cp GUIDELINES.md .antigravity/GUIDELINES.md`.
- However, there is **no `GUIDELINES.md` file** in the repository root. The only copy of `GUIDELINES.md` is already inside `.antigravity/`, making this command redundant and prone to throwing a `FileNotFoundError`.

---

## 2. Python Engine Issues

### 2.1 Missing `validate()` Safety Gates [HIGH]
The magic-byte and file size checks are completely bypassed in **17 out of 27** conversion functions. While the modules import `validate` from `.validator`, the function is never invoked at all inside the following modules:
1. `shared/engine/audio.py` — Bypassed in `wav_to_mp3` and `m4a_to_mp3`.
2. `shared/engine/video.py` — Bypassed in `mp4_to_mp3`, `mov_to_mp4`, `mkv_to_mp4`, and `webm_to_mp4`.
3. `shared/engine/cad.py` — Bypassed in `dwg_to_pdf`.
4. `shared/engine/data.py` — Bypassed in `csv_to_xlsx`, `json_to_csv`, `xml_to_json`, and `yaml_to_json`. (Only `pdf_to_xlsx` invokes it).
5. `shared/engine/image.py` — Bypassed in `svg_to_png`, `tiff_to_jpg`, `tiff_to_pdf`, and `gif_to_mp4`.
6. `shared/engine/security.py` — Bypassed in `pem_to_pfx` and `pem_to_crt`.
7. `shared/engine/font.py` — Bypassed in `ttf_to_woff2` and `otf_to_woff2`.

This bypass exposes the engine to malformed file processing, buffer overflows, and platform denial of service (DoS).

### 2.2 Lost `is_web` Parameter in Router Dispatcher [HIGH]
- In `shared/engine/__init__.py`, the entrypoint function is defined as:
  ```python
  def convert(data: bytes, source_fmt: str, target_fmt: str, is_web: bool = False) -> bytes:
      ...
      return handler(data)
  ```
- The `is_web` parameter is completely dropped and never passed to the underlying handlers.
- Since handlers internally call `validate(data, "format")` (when they call it at all), `validate()` defaults to `is_web = False`.
- This means the web-specific 4MB file size restriction (`MAX_FILE_SIZE_WEB_BYTES`) is **never enforced** during engine routing, falling back to the 2GB desktop limit.

### 2.3 `read_epub` Signature Crash in `epub_to_pdf` Roadmap [HIGH]
- In `ROADMAP_PART2.md` (line 836), the suggested code for `epub_to_pdf` is:
  ```python
  book = epub.read_epub(data)
  ```
- This is a direct signature crash. `ebooklib.epub.read_epub()` expects a *string file path*, not raw file `bytes`. Trying to pass raw `bytes` will immediately crash the engine.
*(Note: The actual implementation in `shared/engine/document.py` correctly writes `data` to a temporary file first, but the roadmap document contains the broken code).*

### 2.4 Unimplemented Stub Active in Map [MEDIUM]
- In `shared/engine/document.py` (line 97), `mobi_to_epub` is implemented as:
  ```python
  def mobi_to_epub(data: bytes) -> bytes:
      raise NotImplementedError("mobi→epub requires KindleUnpack — desktop only, no DRM support")
  ```
- However, this function is actively registered in the `CONVERSION_MAP` inside `shared/engine/__init__.py`.
- If a user triggers a `.mobi` to `.epub` conversion, the engine will raise a `NotImplementedError` and throw a 500 error at runtime, despite the UI listing the format pair as supported.

### 2.5 Library Case-Sensitivity Bug [MEDIUM]
- In `ROADMAP_PART2.md` (line 1062), font conversion is written as:
  ```python
  from fonttools.ttLib import TTFont
  ```
- On case-sensitive file systems (like Linux, where Vercel serverless functions execute), this will raise a `ModuleNotFoundError` because the correct package name is `fontTools` (capital 'T'), as implemented in `shared/engine/font.py`.

---

## 3. Vercel Serverless Issues

### 3.1 Binary/System Dependency Crashes on Vercel [CRITICAL]
Several conversion pairs marked as web-supported in `constants.ts` require external C-binaries that are completely missing from Vercel's standard Python serverless environment:
- **`md_to_pdf` & `epub_to_pdf`**: These use `weasyprint`, which requires shared libraries like `pango`, `cairo`, `gobject`, `glib`, and `fontconfig`. Since none of these exist in Vercel's execution containers, calling these functions will throw an `OSError: cannot load library` and crash the function.
- **`svg_to_png`**: This uses `cairosvg`, which requires `libcairo.so.2` (Cairo). This shared library is missing on Vercel, causing the SVG-to-PNG flow to crash.

### 3.2 Transitive Dependency Mismatch (`pymupdf` / `pdf2docx`) [CRITICAL]
- In `web/requirements.txt` (line 18), the developer explicitly excludes `pymupdf` under the assumption that it requires system binaries: `# ── No ffmpeg-python, pydub, rarfile, pymupdf ──────────────────`.
- However, `web/requirements.txt` (line 2) includes `pdf2docx==0.5.8`.
- `pdf2docx` strictly requires `pymupdf` (fitz) to compile and execute. Excluding `pymupdf` means any call to `pdf_to_docx` will throw a `ModuleNotFoundError: No module named 'fitz'` and crash at runtime.

### 3.3 Base64 Request Payload size Limit Bypass (4.5MB Gateway Limit) [CRITICAL]
- Vercel has a strict **4.5MB request body size limit**.
- The client frontend base64-encodes the files before posting. Base64 encoding inflates the file size by **~33%**.
- If a user uploads a file between **3.37MB and 4.0MB**, the client-side validation (`WEB_FILE_SIZE_LIMIT_BYTES = 4MB`) passes.
- However, the base64-encoded request payload will be between **4.49MB and 5.33MB**, exceeding Vercel's 4.5MB HTTP body gateway limit.
- This will cause Vercel to immediately reject the request at the gateway level with a `413 Payload Too Large` error, bypassing the serverless error handler completely. The max safe client file upload limit must be lowered to **3.3MB**.

### 3.4 Non-Standard / Discouraged Serverless Handler Class [HIGH]
- `web/api/convert.py` implements a subclass of `http.server.BaseHTTPRequestHandler`.
- This legacy CGI-like pattern is highly discouraged for modern Vercel Python 3.12 runtimes. It lacks proper async parsing, exhibits slow request body reading, and has concurrency limits compared to modern micro-framework WSGI/ASGI handlers (e.g., using FastAPI or simple lambda function entry points).

### 3.5 Missing CORS & OPTIONS preflight Headers [HIGH]
- `web/api/convert.py` does not return any CORS-compliant headers (`Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`) nor does it handle preflight `OPTIONS` requests.
- This will immediately trigger browser CORS blocking in multi-domain or local cross-port deployment setups (e.g., frontend on localhost:3000 calling backend on a different serverless port).

---

## 4. Next.js / TypeScript Issues

### 4.1 React List Keys Index Anti-Pattern [HIGH]
- In `web/components/ConversionQueue.tsx` (line 45), list rendering is mapped using the array index as the unique key:
  ```tsx
  {queue.map((item, i) => (
    <div key={i} ...>
  ```
- Because users can dynamically delete files from the queue (`onRemove(i)` on line 93), using the index as a key is a severe anti-pattern. If a user deletes an item, React will reuse DOM elements incorrectly, leading to UI state bugs (e.g., wrong file labels, incorrect progress bars, or mismatched download links).

### 4.2 Synchronous Loop UI Freeze [HIGH]
- In `web/lib/api.ts` (line 25), base64 decoding is written as a synchronous character-mapping loop:
  ```typescript
  const byteCharacters = atob(data.result);
  const byteNumbers = new Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  ```
- For a 4MB file, this loop runs 4,000,000 times synchronously on the main JavaScript thread.
- This blocks the main thread completely, causing the browser UI to lock up, freeze micro-animations, and stutter, leading to a degraded user experience. It should be replaced with a modern typed array translation: `Uint8Array.from(atob(data.result), c => c.charCodeAt(0))`.

### 4.3 Missing Object URL Revocation (Memory Leak) [MEDIUM]
- In `web/lib/api.ts` (line 40), the converted file is converted to a local Blob URL via `URL.createObjectURL(blob)`.
- This Object URL is passed to the queue, but it is **never revoked** (`URL.revokeObjectURL()`).
- This will slowly leak massive chunks of browser memory, potentially crashing the user's browser tab if they convert multiple files in a single session.

---

## 5. Desktop / PyQt6 Issues

### 5.1 Widget `objectName` Style Mismatch [HIGH]
The desktop app UI contains several object naming mismatches that completely break QSS styling:
1. **DropZone Widget**: In `desktop/ui/drop_zone.py` (line 11), the object name is set as: `self.setObjectName("glassCard")`.
   However, `dark.qss` (line 1187) targets `QWidget#dropZone`. Because the object name is mismatched, the drop zone styles (dashed borders, hover transitions, and drag-active state animations) will **never load**, leaving the drop zone styled as a plain static card.
2. **TitleBar Window Controls**: In `desktop/ui/main_window.py` (lines 30, 35, 40), the controls are named `"macCloseBtn"`, `"macMinBtn"`, and `"macMaxBtn"`.
   However, `dark.qss` (line 1155) targets `QToolButton#btnClose`, `QToolButton#btnMin`, `QToolButton#btnMax`. This breaks the macOS-style traffic light styling, leaving standard unstyled pushbuttons.

### 5.2 Relative Path File I/O Crash on Theme Change [HIGH]
- In `desktop/ui/main_window.py` (line 132), stylesheet loading on toggle is implemented as:
  ```python
  with open(f"ui/styles/{new_theme}.qss", "r", encoding="utf-8") as f:
  ```
- This is a relative path. If the application is launched from a desktop shortcut or the startup folder, the active working directory changes, and toggling the theme will immediately throw a `FileNotFoundError` and crash the application.
- It must be resolved using `os.path.dirname(os.path.abspath(__file__))` or PyInstaller's `sys._MEIPASS`.

### 5.3 Silent User Data Overwrites (Data Loss) [CRITICAL]
- In `desktop/ui/conversion_queue.py` (line 67), the output path is silently set without confirming with the user:
  ```python
  output_path = str(self.file_path.with_suffix(f".{target_fmt}"))
  ```
- If a file with the target name already exists in the folder, it will be **silently overwritten and deleted**, causing catastrophic data loss!
*(Note: `ROADMAP_PART2.md` line 1565 claims that `QFileDialog.getSaveFileName` is used, but the actual implementation in `desktop/ui/conversion_queue.py` lacks this check).*

### 5.4 Synchronous Large File Reads in GUI Thread [HIGH]
- In `desktop/ui/conversion_queue.py` (line 61), the main GUI thread reads the entire source file into memory before spawning the worker thread:
  ```python
  with open(self.file_path, "rb") as f:
      data = f.read()
  ```
- If a user attempts to convert a large file (e.g., a 1GB MKV video), this synchronous call will freeze the GUI thread for several seconds, causing Windows to mark the application as "Not Responding".
- Instead of reading bytes in the main thread, the GUI should pass the `Path` to the `ConversionWorker` and let the worker stream the file in a background thread.

### 5.5 Redundant Large Data Signal Emission [MEDIUM]
- In `desktop/engine/worker.py` (line 41), the worker thread emits a signal containing all file bytes back to the main thread:
  ```python
  self.finished.emit(result, self.output_path)
  ```
- Since the worker thread has already written the file to disk (`with open(self.output_path, "wb") as f`), passing megabytes of bytes through Qt's event system serves no purpose, creates duplicate copies of the file data in memory, and causes thread synchronization overhead.

### 5.6 LibreOffice Path Failure (.env Ignored) [HIGH]
- In `shared/engine/document.py` (line 29), LibreOffice is loaded using `os.environ.get("LO_BIN", "soffice")`.
- The desktop app instructs developers to set `LO_BIN` in a `.env` file.
- However, `desktop/main.py` **never imports or calls `dotenv.load_dotenv()`**, and `python-dotenv` is missing from `desktop/requirements.txt`!
- Therefore, the `.env` file is completely ignored, `LO_BIN` is never loaded, and the engine attempts to run `"soffice"`, which will immediately crash on Windows if LibreOffice is not added to the system `PATH`.

---

## 6. Build & Packaging Issues

### 6.1 PyInstaller Missing Transitive Imports [HIGH]
- In `desktop/build.spec` (line 15), several core packages are listed as `hiddenimports`.
- However, transitively compiled dependencies (e.g., `weasyprint` dependencies, `pdf2docx` internal bindings, `cairosvg` helper wrappers) are missing.
- When compiled, these components will throw runtime exceptions because PyInstaller's static analyzer fails to trace these dynamically loaded sub-modules.

### 6.2 Missing `UninstallDisplayIcon` in Inno Setup [LOW]
- In `desktop/installer/setup.iss` (line 1), there is no `UninstallDisplayIcon` set under `[Setup]`.
- This causes the Windows Add/Remove Programs control panel to show a default, low-quality generic system icon next to the application uninstaller instead of the premium brand icon.

### 6.3 Missing Upgrade Lock & Mutex [HIGH]
- `setup.iss` does not define an `AppMutex` check or check if the app is currently running.
- If a user runs an installer upgrade while `FileHarbor.exe` is active, the installer will attempt to overwrite the locked binary files, resulting in an installation crash, file write permissions failure, or a corrupted half-installed state.

### 6.4 Missing Registry & settings Cleanup on Uninstall [MEDIUM]
- The application writes persistent theme preferences and configuration to the registry via `QSettings`.
- `setup.iss` lacks any registry deletion commands (e.g., under `[Registry]` or `UninstallDelete`).
- When a user uninstalls the application, all `QSettings` values written under `HKCU\Software\Web Harbor Solutions` are left behind as orphaned registry bloat.

### 6.5 Packaging Dependency Mismatch on macOS [MEDIUM]
- In `desktop/installer/build_macos.sh` (line 11), the script runs `npm install -g create-dmg` to bundle the application.
- This creates a hard dependency on Node.js/NPM in the macOS build environment, which is undocumented and will immediately fail on a pure Python development machine.

---

## 7. Security Issues

### 7.1 Security Magic-byte Bypass (Extension Spoofing) [CRITICAL]
- `shared/engine/validator.py` defines `MAGIC_BYTES` for only a few formats (e.g., pdf, docx, xlsx, pptx, png, jpg, gif, webp, mp4, zip, rar).
- For all other supported conversion formats (e.g., `heic`, `csv`, `json`, `xml`, `yaml`, `epub`, `mobi`, `wav`, `m4a`, `mp3`, `md`, `ttf`, `otf`, `pem`, `tiff`, `dwg`), **no magic bytes are defined** in the validator!
- If a caller passes `"heic"` or `"epub"`, `validator.py` will retrieve `None` from the dictionary and return silently without throwing an error.
- This allows a malicious attacker to upload a compiled executable renamed as `cert.pem` or `style.md`, bypass the validation check, and feed it straight to backend C-parsers, leading to potential **Remote Code Execution (RCE)** or buffer overflows.

### 7.2 Lack of Input Validation in Modules [CRITICAL]
- As documented in Section 2.1, **17 out of 27** engine modules do not even import or call `validate()`!
- This bypasses all file checks completely, making the backend vulnerable to XML External Entity (XXE) injection via `xmltodict` or YAML deserialization attacks via `pyyaml` (which can lead to file read/write access or RCE).

### 7.3 Infinite Subprocess Hangs (Denial of Service) [HIGH]
- Subprocess and ffmpeg wrappers in `shared/engine/image.py` (`gif_to_mp4`), `audio.py`, and `video.py` are executed without **any timeout constraints**.
- If a user uploads a malformed file that causes `ffmpeg` to enter an infinite loop or wait for standard input, the worker thread will hang indefinitely. This leaks resources and can block all future conversion slots, leading to an easy Denial of Service (DoS) attack.

---

## 8. Integration & Flow Issues

### 8.1 Web Flow Silent Crashes & Degraded UX [HIGH]
During the web flow:
`client drop → validate → encode → POST → serverless → engine → decode → download`
- If a Vercel function runs out of memory or times out (Hobby limit 10s), Vercel will return an HTML gateway error page.
- The frontend `fetch` wrapper immediately calls `res.json()`, which fails to parse the HTML string and throws a generic `SyntaxError`.
- This causes the flow to drop to the generic `catch` block, displaying: `"Network error or unexpected response"`, completely masking the timeout or memory crash from the developer or user.

### 8.2 Desktop Flow GUI Lockup [HIGH]
During the desktop flow:
`drop → QueueRow → ConversionWorker → engine → save`
- Reading the entire file bytes in the main thread (Section 5.4) locks up the UI event loop, preventing progress updates or cancellations.
- Overwriting the files silently (Section 5.3) creates a serious data corruption risk where users lose their original documents if they drop a file and convert it to a format that shares the extension or target.

### 8.3 Manual Engine Copy Sync Operational Risk [HIGH]
- The roadmaps rely on developers manually copying `shared/engine/` to `desktop/engine/`.
- There is no automated synchronization script, verification tool, or CI check to make sure both folders stay in sync.
- This creates a high risk of manual-drift, where developers implement platform-specific fixes in one copy and forget to update the other, leading to silent bugs and incompatible engine behaviors.

---

## 9. Missing Implementations

### 9.1 Mobi-to-Epub Support [HIGH]
- The roadmap lists Mobi-to-Epub conversion in `Supported file conversion.md` and in the engine's `CONVERSION_MAP`.
- However, `shared/engine/document.py` contains only a `NotImplementedError` placeholder, meaning this feature has zero implementation in the code.

### 9.2 Assets Folder [HIGH]
- `desktop/assets/icon.ico` and font directories are referenced in PyInstaller specs and documentation, but are entirely missing from the codebase.

### 9.3 Environment Loading [HIGH]
- The desktop app reads environment variables for paths, but lacks any implementation of `.env` configuration file loading in `main.py`.

---

## 10. Cross-Platform & Environment Issues

### 10.1 Windows-Only Path Hardcoding in LibreOffice [HIGH]
- `desktop/README.md` instructs the user to configure `LO_BIN` using backslashes:
  `LO_BIN=libreoffice_portable\App\libreoffice\program\soffice.exe`
- While this works on Windows, it will fail on macOS and Linux.
- Furthermore, the desktop app has no fallback or dynamic path resolution to find the default installed LibreOffice binary on macOS (`/Applications/LibreOffice.app`) or Linux (`/usr/bin/soffice`), breaking docx/pptx conversions on those OS platforms.

### 10.2 Windows-Only Icons on macOS/Linux Builds [HIGH]
- `desktop/build.spec` hardcodes `icon='assets/icon.ico'`.
- `.ico` icons are Windows-specific. Running the Linux and macOS build scripts (`build_linux.sh`, `build_macos.sh`) will fail or crash during the PyInstaller build because macOS bundles require `.icns` format, and Linux bundles require PNG/SVG icons.

### 10.3 Forward-slash vs Backslash Divergence [MEDIUM]
- The Python engine frequently mixes forward-slashes and backslashes in path operations (e.g., `os.path.join` vs hardcoded strings like `"ui/styles/"`). While Python's `pathlib` mitigates this, raw string manipulation will cause failures when cross-compiling or running on different operating systems.

---

## 11. Summary Table

| Issue ID | Severity | Location | One-line description | Blocking (yes/no) |
|---|---|---|---|---|
| **ISS-001** | **[HIGH]** | `desktop/build.spec` | Missing `assets` directory crashes PyInstaller build. | **Yes** |
| **ISS-002** | **[HIGH]** | `shared/engine/` | `validate()` omitted in 17 out of 27 conversion functions. | **Yes** |
| **ISS-003** | **[HIGH]** | `shared/engine/__init__.py` | `is_web` parameter lost during convert routing. | **Yes** |
| **ISS-004** | **[CRITICAL]** | `web/api/` | `weasyprint` and `cairosvg` crash on Vercel due to missing C-binaries. | **Yes** |
| **ISS-005** | **[CRITICAL]** | `web/requirements.txt` | Missing `pymupdf` transitive dependency crashes `pdf_to_docx`. | **Yes** |
| **ISS-006** | **[CRITICAL]** | `web/lib/constants.ts` | 4MB limit base64 expansion triggers 413 Gateway crashes on Vercel. | **Yes** |
| **ISS-007** | **[HIGH]** | `web/api/convert.py` | Missing CORS and OPTIONS handler blocks cross-port requests. | **Yes** |
| **ISS-008** | **[HIGH]** | `web/components/ConversionQueue.tsx` | Index keys in list rendering cause UI desync upon removals. | **Yes** |
| **ISS-009** | **[HIGH]** | `web/lib/api.ts` | Synchronous base64 decoder blocks main JS thread, freezing UI. | **No** |
| **ISS-010** | **[MEDIUM]** | `web/lib/api.ts` | Object URLs are never revoked, causing browser memory leaks. | **No** |
| **ISS-011** | **[HIGH]** | `desktop/ui/drop_zone.py` | ObjectName mismatch in DropZone (`glassCard` vs `#dropZone`) breaks QSS. | **No** |
| **ISS-012** | **[HIGH]** | `desktop/ui/main_window.py` | ObjectName mismatch in TitleBar buttons breaks traffic light QSS. | **No** |
| **ISS-013** | **[HIGH]** | `desktop/ui/main_window.py` | Relative paths in dynamic stylesheet loading crash app on dynamic toggle. | **Yes** |
| **ISS-014** | **[CRITICAL]** | `desktop/ui/conversion_queue.py` | No save dialog causes silent overwrite and data destruction. | **Yes** |
| **ISS-015** | **[HIGH]** | `desktop/ui/conversion_queue.py` | Synchronous file reads on GUI thread freeze application during large loads. | **Yes** |
| **ISS-016** | **[HIGH]** | `desktop/main.py` | Absence of `.env` loader and `python-dotenv` crashes LibreOffice paths. | **Yes** |
| **ISS-017** | **[HIGH]** | `desktop/installer/setup.iss` | Missing upgrade lock/mutex leads to locked files write errors. | **Yes** |
| **ISS-018** | **[CRITICAL]** | `shared/engine/validator.py` | Missing magic bytes for 16 formats allows extension spoofing / RCE. | **Yes** |
| **ISS-019** | **[HIGH]** | `shared/engine/` | Subprocesses / ffmpeg called without timeouts cause infinite hangs. | **Yes** |
| **ISS-020** | **[HIGH]** | `shared/ → desktop/` | Undocumented manual copying of engine increases drift/divergence risks. | **No** |
| **ISS-021** | **[HIGH]** | `shared/engine/document.py` | `mobi_to_epub` raises `NotImplementedError` but is mapped as active. | **Yes** |
| **ISS-022** | **[HIGH]** | `desktop/build.spec` | Hardcoded `.ico` icon and Windows paths crash macOS/Linux builds. | **Yes** |
| **ISS-023** | **[MEDIUM]** | Monorepo branding | Conflicting names ("SwiftConvert" vs "File Harbor") exist throughout. | **No** |
| **ISS-024** | **[MEDIUM]** | `desktop/engine/worker.py` | Large byte data emitted redundantly over signal causes memory bloat. | **No** |
| **ISS-025** | **[MEDIUM]** | `desktop/installer/setup.iss` | Missing registry cleanup leaves orphaned `QSettings` registry entries. | **No** |
