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
