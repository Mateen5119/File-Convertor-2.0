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
            self._send(500, {"error": "CONVERSION_FAILED", "message": f"Conversion failed: {str(e)}. Try the desktop app."})

    def _send(self, status: int, data: dict):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
