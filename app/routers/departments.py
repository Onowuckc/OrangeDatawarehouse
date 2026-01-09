from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from ..deps import get_db, get_current_principal
from ..models import Department

router = APIRouter(prefix="/departments", tags=["departments"])

@router.get("/", response_model=list[Department])
async def list_departments(db=Depends(get_db)):
    q = await db.execute(select(Department))
    return q.scalars().all()

@router.post("/", status_code=201)
async def create_department(dep: Department, db=Depends(get_db), principal=Depends(get_current_principal)):
    role = principal.get("role")
    if role not in ("GeneralManager", "CEO"):
        raise HTTPException(status_code=403, detail="Only admins can create departments")
    db.add(dep)
    await db.commit()
    await db.refresh(dep)
    return dep

@router.delete("/{dep_id}", status_code=202)
async def delete_department(dep_id: int, db=Depends(get_db), principal=Depends(get_current_principal)):
    """Soft-delete department (mark deleted + timestamp).
    Deletion is soft to allow undo within a short grace window."""
    role = principal.get("role")
    if role not in ("GeneralManager", "CEO"):
        raise HTTPException(status_code=403, detail="Only admins can delete departments")
    q = await db.execute(select(Department).where(Department.id == dep_id))
    d = q.scalars().one_or_none()
    if not d:
        raise HTTPException(status_code=404, detail="Department not found")
    d.deleted = True
    from datetime import datetime
    d.deleted_at = datetime.utcnow()
    db.add(d)
    await db.commit()
    await db.refresh(d)
    return {"status": "pending_delete", "id": d.id}

@router.post("/{dep_id}/restore", status_code=200)
async def restore_department(dep_id: int, db=Depends(get_db), principal=Depends(get_current_principal)):
    role = principal.get("role")
    if role not in ("GeneralManager", "CEO"):
        raise HTTPException(status_code=403, detail="Only admins can restore departments")
    q = await db.execute(select(Department).where(Department.id == dep_id))
    d = q.scalars().one_or_none()
    if not d:
        raise HTTPException(status_code=404, detail="Department not found")
    d.deleted = False
    d.deleted_at = None
    db.add(d)
    await db.commit()
    await db.refresh(d)
    return d
