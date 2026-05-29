# File Harbor

File Harbor is a robust, cross-platform file conversion utility consisting of a Next.js web application and a PyQt6 desktop application.

## Architecture

This project is structured as a monorepo:

- **`shared/engine/`**: The core Python conversion engine. Contains modules for validating and converting images, documents, audio, video, archives, etc. Used by both the web backend and desktop app.
- **`web/`**: Next.js serverless application deployed on Vercel. Features a sleek, modern UI with drag-and-drop conversion using the `shared/engine/` via an API route.
- **`desktop/`**: PyQt6 desktop application offering limitless file conversion size, plus advanced PDF and DOCX editing, and PDF/image compression. Uses an independent copy of `shared/engine/`.

## Features

- **27+ Conversion Formats**: Everything from PDF to DOCX, PNG to JPG, Markdown to PDF, and more.
- **Cross-Platform Desktop App**: Runs natively on Windows, macOS, and Linux with a frameless "Stitch" design system UI.
- **Advanced Desktop Editor**: Visually edit PDFs (delete, rotate, reorder pages) and DOCX files locally.
- **Local Compression**: Squeeze PDFs and images with adjustable quality sliders.
- **Fast Web Experience**: Instant, client-side validated drag-and-drop.

## Setup

### Web App
```bash
cd web
npm install
npm run dev
```

### Desktop App
```bash
cd desktop
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Testing & CI/CD

- Tests are located in `shared/tests/` and `desktop/tests/` using `pytest`.
- GitHub Actions are configured for automated linting and testing of both web and desktop components (`.github/workflows/`).

## Author

Web Harbor Solutions
