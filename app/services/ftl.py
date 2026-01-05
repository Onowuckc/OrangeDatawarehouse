from typing import Any, Dict
from ..schemas import ReportSubmit

# Minimal FTL service placeholder. Replace with full implementation later.

def normalize_payload(payload: Any) -> Dict[str, Any]:
    # Basic normalization: if dict, return as-is; else wrap
    if isinstance(payload, dict):
        return payload
    return {"value": payload}


def process_report(submit: ReportSubmit) -> Dict[str, Any]:
    normalized = normalize_payload(submit.payload)
    # Add minimal metadata
    return {
        "department_code": submit.department_code,
        "uploader": None,
        "report_date": submit.report_date,
        "version": submit.version,
        "normalized": normalized,
        "status": "ready",
    }
