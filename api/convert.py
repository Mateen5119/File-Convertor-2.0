import sys
import os
import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Add shared engine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))

from engine import convert
from engine.validator import MAX_FILE_SIZE_WEB_BYTES

app = FastAPI(title="File Harbor API")

# ISS-007: Standard Modern CORS & OPTIONS Preflight Support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

class ConvertRequest(BaseModel):
    file: str          # Base64 encoded payload
    source_fmt: str
    target_fmt: str

@app.post("/api/convert")
async def convert_file(payload: ConvertRequest):
    try:
        try:
            file_bytes = base64.b64decode(payload.file)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid Base64 payload")
            
        # Enforce web size limit (3.3MB original size)
        if len(file_bytes) > MAX_FILE_SIZE_WEB_BYTES:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "FILE_TOO_LARGE",
                    "message": "File exceeds 3.3MB limit. Please download File Harbor for Desktop for unlimited sizes."
                }
            )
            
        source_fmt = payload.source_fmt.lower().strip(".")
        target_fmt = payload.target_fmt.lower().strip(".")
        
        # Call conversion router with is_web=True constraint
        result_bytes = convert(file_bytes, source_fmt, target_fmt, is_web=True)
        result_b64 = base64.b64encode(result_bytes).decode("utf-8")
        
        return {
            "result": result_b64,
            "target_fmt": target_fmt
        }
        
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": "VALIDATION_ERROR", "message": str(e)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "CONVERSION_FAILED",
                "message": f"Conversion error: {str(e)}. Try using our standalone Desktop app."
            }
        )

@app.get("/api/health")
async def health():
    return {"status": "healthy"}
