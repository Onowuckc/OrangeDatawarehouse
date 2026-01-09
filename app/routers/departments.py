from fastapi import APIRouter, Depends
from sqlalchemy import select
from ..deps import get_db
from ..models import Department

router = APIRouter(prefix="/departments", tags=["departments"])

@router.get("/", response_model=list[Department])
async def list_departments(db=Depends(get_db)):
    q = await db.execute(select(Department))
    return q.scalars().all()
