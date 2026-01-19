from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy import select
from ..schemas import ReportSubmit, ReportOut
from ..deps import get_db, get_current_principal
from ..services.ftl import process_report
from ..repositories import save_staging, save_report, list_reports_for_user
from ..models import Department, User, UserDepartmentLink, Role, Report
import csv
import io
from openpyxl import load_workbook

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/submit", response_model=ReportOut)
async def submit_report(payload: ReportSubmit, db=Depends(get_db), principal=Depends(get_current_principal)):
    # Resolve department
    q = await db.execute(select(Department).where(Department.code == payload.department_code))
    dept = q.scalars().one_or_none()
    if not dept:
        raise HTTPException(status_code=400, detail="Unknown department")

    # Authorization: general managers or department owners
    role = principal.get("role")
    user_id = principal.get("user_id")
    dept_claim = principal.get("dept")

    allowed = False
    if role in ("GeneralManager", "CEO"):
        allowed = True
    elif dept_claim and dept_claim == payload.department_code:
        allowed = True
    elif user_id:
        # check user's departments
        q = await db.execute(select(UserDepartmentLink.department_id).where(UserDepartmentLink.user_id == user_id))
        allowed_ids = q.scalars().all()
        if dept.id in allowed_ids:
            allowed = True

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized to submit for this department")

    # Persist to staging
    staging_payload = {
        "department_id": dept.id,
        "uploader_id": user_id,
        "raw_payload": payload.payload,
        "filename": payload.filename,
        "status": "received",
    }
    staging = await save_staging(staging_payload, db)

    # Run transform (sync for now)
    normalized = process_report(payload)

    report_payload = {
        "department_id": dept.id,
        "uploader_id": user_id,
        "report_date": payload.report_date,
        "version": payload.version,
        "status": "ready",
        "normalized": normalized["normalized"],
    }
    report = await save_report(report_payload, db)

    return report

@router.post("/submit-file", response_model=ReportOut)
async def submit_report_file(
    department_code: str = Form(...),
    file: UploadFile = File(...),
    filename: str | None = Form(None),
    report_date: str | None = Form(None),
    version: str | None = Form(None),
    db=Depends(get_db),
    principal=Depends(get_current_principal),
):
    # Resolve department
    q = await db.execute(select(Department).where(Department.code == department_code))
    dept = q.scalars().one_or_none()
    if not dept:
        raise HTTPException(status_code=400, detail="Unknown department")

    # Authorization: general managers or department owners
    role = principal.get("role")
    user_id = principal.get("user_id")
    dept_claim = principal.get("dept")

    allowed = False
    if role in ("GeneralManager", "CEO"):
        allowed = True
    elif dept_claim and dept_claim == department_code:
        allowed = True
    elif user_id:
        q = await db.execute(select(UserDepartmentLink.department_id).where(UserDepartmentLink.user_id == user_id))
        allowed_ids = q.scalars().all()
        if dept.id in allowed_ids:
            allowed = True

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized to submit for this department")

    # Parse file: CSV or Excel
    parsed = None
    filename = filename or getattr(file, 'filename', None)
    content_type = (file.content_type or '').lower()

    data = await file.read()

    if 'csv' in content_type or (filename and filename.lower().endswith('.csv')):
        text = data.decode('utf-8')
        reader = csv.DictReader(io.StringIO(text))
        parsed = [row for row in reader]
    elif 'sheet' in content_type or filename and filename.lower().endswith(('.xls', '.xlsx')):
        wb = load_workbook(io.BytesIO(data), read_only=True, data_only=True)
        ws = wb.active
        rows = list(ws.values)
        if not rows:
            parsed = []
        else:
            headers = [str(h) for h in rows[0]]
            parsed = []
            for r in rows[1:]:
                parsed.append({headers[i]: r[i] for i in range(len(headers))})
    else:
        raise HTTPException(status_code=400, detail='Unsupported file type. Please upload CSV or XLSX')

    # Persist to staging
    staging_payload = {
        "department_id": dept.id,
        "uploader_id": user_id,
        "raw_payload": parsed,
        "filename": filename,
        "status": "received",
    }
    staging = await save_staging(staging_payload, db)

    # Run transform (sync for now)
    submit_model = ReportSubmit(department_code=department_code, payload=parsed, filename=filename, report_date=report_date, version=version)
    normalized = process_report(submit_model)

    report_payload = {
        "department_id": dept.id,
        "uploader_id": user_id,
        "report_date": report_date,
        "version": version,
        "status": "ready",
        "normalized": normalized["normalized"],
    }
    report = await save_report(report_payload, db)

    return report

@router.get("/", response_model=list[ReportOut])
async def list_reports(db=Depends(get_db), principal=Depends(get_current_principal)):
    # If GM -> return all
    role = principal.get("role")
    user_id = principal.get("user_id")
    dept_claim = principal.get("dept")

    if role in ("GeneralManager", "CEO"):
        q = await db.execute(select(Report))
        return q.scalars().all()

    # Department claim
    if dept_claim:
        qd = await db.execute(select(Department).where(Department.code == dept_claim))
        d = qd.scalars().one_or_none()
        if not d:
            return []
        q = await db.execute(select(Report).where(Report.department_id == d.id))
        return q.scalars().all()

    # User-based: use repository helper
    if user_id:
        # fetch user & role
        qu = await db.execute(select(User).where(User.id == user_id))
        user = qu.scalars().one_or_none()
        if not user:
            return []
        qr = await db.execute(select(Role).where(Role.id == user.role_id))
        role_obj = qr.scalars().one_or_none()
        reports = await list_reports_for_user(user, db, role_obj)
        return reports

    return []
