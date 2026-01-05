from fastapi import APIRouter, Depends, HTTPException
from ..schemas import ReportSubmit, ReportOut
from ..deps import get_db
from ..services.ftl import process_report

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/submit", response_model=ReportOut)
async def submit_report(payload: ReportSubmit, db=Depends(get_db)):
    # minimal pipeline: normalize and return result as if saved
    normalized = process_report(payload)
    # In a full implementation we'd persist to staging and enqueue background job.
    return {
        "id": 1,
        "department_id": 1,
        "uploader_id": 1,
        "report_date": payload.report_date,
        "version": payload.version,
        "status": "ready",
        "normalized": normalized["normalized"],
        "created_at": "1970-01-01T00:00:00",
    }

@router.get("/", response_model=list[ReportOut])
async def list_reports(db=Depends(get_db)):
    # Return empty list for now
    return []
