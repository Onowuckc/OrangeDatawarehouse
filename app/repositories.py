from typing import List, Optional
from sqlalchemy import select
from .models import Report, StagingReport, User, Role, UserDepartmentLink

# Repository functions with RBAC-aware queries

async def list_reports_for_user(user: User, session, role: Role) -> List[Report]:
    """Return reports visible to `user` according to their `role`.

    - GeneralManager: sees all reports
    - DepartmentUser / SeniorManager: sees reports for departments assigned via UserDepartmentLink
    """
    if role and role.name == "GeneralManager":
        q = await session.execute(select(Report))
        return q.scalars().all()

    # Fetch department ids the user has access to
    q = await session.execute(
        select(UserDepartmentLink.department_id).where(UserDepartmentLink.user_id == user.id)
    )
    rows = q.scalars().all()
    if not rows:
        return []

    q = await session.execute(select(Report).where(Report.department_id.in_(rows)))
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
