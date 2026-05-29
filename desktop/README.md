# File Harbor Desktop

The cross-platform desktop application for File Harbor, built with PyQt6.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python main.py
   ```

## Development

- **UI**: Located in `ui/`. Uses QSS (`ui/styles/`) for styling matching the web design tokens.
- **Features**: Editor and compressor modules in `features/`.
- **Engine**: A copy of the shared conversion engine lives in `engine/`.

## Dependencies & LibreOffice

Most conversions are handled by Python packages (Pillow, pdf2docx, etc.) or external APIs. 
However, **DOCX -> PDF** and **PPTX -> PDF** require LibreOffice to be installed on the system.

- On Windows, you can download LibreOffice Portable and extract it to the root directory, or point the `LO_BIN` environment variable in your `.env` file to its executable.

## Packaging

The app is packaged using PyInstaller.

### Windows
```bash
pyinstaller build.spec
```
Then use Inno Setup (`installer/setup.iss`) to create the installer.

### macOS
```bash
bash installer/build_macos.sh
```

### Linux
```bash
bash installer/build_linux.sh
```
