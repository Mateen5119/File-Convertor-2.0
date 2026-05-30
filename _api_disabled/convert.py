"""
File Harbor — Conversion API
Vercel Python serverless function.
Runtime: python3.12 (standard Vercel runtime — requires BaseHTTPRequestHandler pattern).
DO NOT use FastAPI, Flask, or any ASGI/WSGI framework here without a mangum adapter.
"""

import sys
import os
import json
import base64
from http.server import BaseHTTPRequestHandler

# ── Resolve shared engine path ────────────────────────────────────
# /api/convert.py is one level below the repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ── Constants ────────────────────────────────────────────────────
MAX_WEB_BYTES = 3_400_000  # 3.3MB — base64 inflates ~33%, must stay under Vercel 4.5MB gateway

CORS = {
    "Access-Control-Allow-Origin":  "*",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type":                 "application/json",
}


class handler(BaseHTTPRequestHandler):
    """Vercel Python serverless handler. Class name must be 'handler' (lowercase)."""

    def log_message(self, format, *args):
        pass  # suppress default noisy access logs on Vercel

    def _send_json(self, status: int, data: dict) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        for k, v in CORS.items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        """CORS preflight — required for browser cross-origin POST."""
        self.send_response(204)
        for k, v in CORS.items():
            self.send_header(k, v)
        self.end_headers()

    def do_GET(self):
        self._send_json(200, {"status": "ok", "service": "file-harbor-convert"})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length == 0:
                return self._send_json(400, {
                    "error": "EMPTY_BODY",
                    "message": "Request body is required."
                })

            raw   = self.rfile.read(length)
            body  = json.loads(raw)

            file_b64:   str = body.get("file", "")
            source_fmt: str = body.get("source_fmt", "").lower().strip(".")
            target_fmt: str = body.get("target_fmt", "").lower().strip(".")

            if not file_b64 or not source_fmt or not target_fmt:
                return self._send_json(400, {
                    "error": "MISSING_FIELDS",
                    "message": "file, source_fmt, and target_fmt are all required."
                })

            try:
                file_bytes = base64.b64decode(file_b64)
            except Exception:
                return self._send_json(400, {
                    "error": "INVALID_BASE64",
                    "message": "File payload is not valid base64."
                })

            if len(file_bytes) > MAX_WEB_BYTES:
                return self._send_json(400, {
                    "error": "FILE_TOO_LARGE",
                    "message": (
                        f"File is {len(file_bytes) / 1_000_000:.1f}MB — exceeds the "
                        f"{MAX_WEB_BYTES / 1_000_000:.1f}MB web limit. "
                        "Download File Harbor Desktop for unlimited file sizes."
                    ),
                })

            from shared.engine import convert
            result_bytes = convert(file_bytes, source_fmt, target_fmt, is_web=True)
            result_b64   = base64.b64encode(result_bytes).decode("utf-8")

            return self._send_json(200, {
                "result":     result_b64,
                "target_fmt": target_fmt,
            })

        except ValueError as e:
            return self._send_json(400, {
                "error":   "VALIDATION_ERROR",
                "message": str(e),
            })
        except MemoryError:
            return self._send_json(500, {
                "error":   "OUT_OF_MEMORY",
                "message": "File too large to process in memory. Use the desktop app.",
            })
        except json.JSONDecodeError:
            return self._send_json(400, {
                "error":   "INVALID_JSON",
                "message": "Request body must be valid JSON.",
            })
        except Exception:
            return self._send_json(500, {
                "error":   "CONVERSION_FAILED",
                "message": "Conversion failed. Try the desktop app for more reliable processing.",
            })
