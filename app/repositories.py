from typing import List, Optional
from .models import Report, StagingReport, User, Role

# Minimal repository functions; extend with RBAC-aware queries later

async def list_reports_for_user(user: User, session, role: Role) -> List[Report]:
    # Simplified: return all reports for now; enforce RBAC later
    q = await session.execute(Report.select())
    return q.scalars().all()

async def save_staging(payload: dict, session) -> StagingReport:
    obj = StagingReport(**payload)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def save_report(payload: dict, session) -> Report:
    obj = Report(**payload)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj
