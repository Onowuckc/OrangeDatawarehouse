import os
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Department, Role, User, UserDepartmentLink, Report
from app.auth import create_access_token
from app.routers.reports import submit_report, list_reports


def test_department_user_cannot_submit_other_dept(tmp_path):
    # Setup sync DB for table creation
    db_file = tmp_path / "test_reports.db"
    sync_url = f"sqlite:///{db_file}"
    async_url = f"sqlite+aiosqlite:///{db_file}"

    sync_engine = create_engine(sync_url)
    SQLModel.metadata.create_all(sync_engine)

    with Session(sync_engine) as s:
        d1 = Department(code='FIN', name='Finance')
        d2 = Department(code='SAL', name='Sales')
        s.add_all([d1, d2])
        s.commit()

        # create user with access to FIN
        r = Role(name='DepartmentUser')
        s.add(r)
        s.commit()
        u = User(username='alice', hashed_password='x', role_id=r.id)
        s.add(u)
        s.commit()
        link = UserDepartmentLink(user_id=u.id, department_id=d1.id)
        s.add(link)
        s.commit()

    # create a dept token for SAL (mismatched)
    token = create_access_token('dept-lazy', extra_claims={'dept': 'SAL', 'role': 'DepartmentUser'})

    # Prepare async session
    async_engine = create_async_engine(async_url, echo=False)
    AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    async def _run():
        async with AsyncSessionLocal() as db:
            class P:  # principal stub (from token)
                user_id = None
                role = 'DepartmentUser'
                dept = 'SAL'
            # building a payload wrapper similar to ReportSubmit
            class Payload:
                department_code = 'FIN'
                payload = {'k': 'v'}
                filename = None
                report_date = None
                version = None

            try:
                await submit_report(Payload(), db, principal={'dept':'SAL','role':'DepartmentUser'})
                assert False, "Expected 403"
            except Exception as e:
                assert 'Not authorized' in str(e)

    import asyncio
    asyncio.run(_run())
