from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os, logging, traceback
from fastapi.responses import JSONResponse

# Load .env from project root if present (dev convenience). Production should inject envs explicitly.
load_dotenv()

from .routers import auth, reports, departments

# Enable detailed error responses in development by setting FASTAPI_DEBUG=1 in your .env
DEBUG = os.getenv("FASTAPI_DEBUG", "0") == "1"
app = FastAPI(title="Internal Data Warehouse - Minimal", debug=DEBUG)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log full traceback to console for debugging
    logging.exception("Unhandled exception while processing request:")
    if DEBUG:
        tb = traceback.format_exc()
        return JSONResponse(status_code=500, content={"detail": str(exc), "traceback": tb})
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

app.include_router(auth.router)
app.include_router(reports.router)
app.include_router(departments.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
