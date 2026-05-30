export const WEB_FILE_SIZE_LIMIT_BYTES = 3_400_000; // 3.3MB — base64 inflates ~33%
export const WEB_FILE_SIZE_LIMIT_LABEL = "3.3MB";
export const DESKTOP_DOWNLOAD_URL = "https://github.com/Mateen5119/File-Convertor-2.0/releases";

// Formats that need binaries not available on Vercel — show DesktopCTA
export const WEB_UNSUPPORTED_FORMATS = new Set<string>([
  // Audio/Video — require ffmpeg
  "mp4", "mov", "mkv", "webm", "gif", "wav", "m4a",
  // Documents — require LibreOffice
  "docx", "pptx",
  // PDF renderers — require weasyprint (C lib)
  "epub", "mobi",
  // Images — require C libs (pillow-heif / cairosvg)
  "heic", "svg",
  // Archives/CAD — require unrar / LibreOffice
  "rar", "dwg",
]);

// source ext → valid targets ON WEB (empty array = desktop-only → shows DesktopCTA)
export const CONVERSION_TARGETS: Record<string, string[]> = {
  // Documents
  pdf:   ["docx", "xlsx"],
  md:    ["html"],
  // Images
  png:   ["jpg"],
  jpg:   ["png"],
  jpeg:  ["png"],
  webp:  ["png", "jpg"],
  tiff:  ["jpg"],
  // Data
  csv:   ["xlsx"],
  json:  ["csv"],
  xml:   ["json"],
  yaml:  ["json"],
  yml:   ["json"],
  // Fonts
  ttf:   ["woff2"],
  otf:   ["woff2"],
  // Security
  pem:   ["crt"],
  // Desktop-only (empty = DesktopCTA)
  heic: [], svg: [], docx: [], pptx: [],
  epub: [], mobi: [], mp4: [], mov: [],
  mkv:  [], webm: [], gif: [], wav: [],
  m4a:  [], rar: [], dwg: [],
};
