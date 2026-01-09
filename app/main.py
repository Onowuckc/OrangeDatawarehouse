from fastapi import FastAPI
from .routers import auth, reports, departments

app = FastAPI(title="Internal Data Warehouse - Minimal")

app.include_router(auth.router)
app.include_router(reports.router)
app.include_router(departments.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
