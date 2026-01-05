from fastapi import FastAPI

app = FastAPI(title="Internal Data Warehouse - Minimal")


@app.get("/health")
async def health():
    return {"status": "ok"}
