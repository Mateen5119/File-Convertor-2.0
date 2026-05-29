from fastapi import FastAPI

app = FastAPI(title="File Harbor Health API")

@app.get("/api/health")
async def health():
    return {"status": "ok"}
