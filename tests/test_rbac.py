import os
import tempfile
import asyncio
import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models import Department, Role, User, UserDepartmentLink, Report
from app.repositories import list_reports_for_user


def test_list_reports_respects_rbac(tmp_path):
    async def _run():
        # Create a temporary sqlite file for the test DB
        db_file = tmp_path / "test_rbac.db"
        sync_url = f"sqlite:///{db_file}"
        async_url = f"sqlite+aiosqlite:///{db_file}"

        # Create tables synchronously
        sync_engine = create_engine(sync_url)
        SQLModel.metadata.create_all(sync_engine)

        # Insert seed data using sync Session for simplicity
        with Session(sync_engine) as s:
            # Departments
            d1 = Department(code="FIN", name="Finance")
            d2 = Department(code="SAL", name="Sales")
            s.add_all([d1, d2])
            s.commit()

            # Roles
            r_dept = Role(name="DepartmentUser")
            r_gm = Role(name="GeneralManager")
            s.add_all([r_dept, r_gm])
            s.commit()

            # Users
            u_dept = User(username="alice", hashed_password="x", role_id=r_dept.id)
            u_gm = User(username="bob", hashed_password="x", role_id=r_gm.id)
            s.add_all([u_dept, u_gm])
            s.commit()

            # Link alice to FIN
            link = UserDepartmentLink(user_id=u_dept.id, department_id=d1.id)
            s.add(link)
            s.commit()

            # Reports
            rep1 = Report(department_id=d1.id, uploader_id=u_dept.id, normalized={"k": "v1"})
            rep2 = Report(department_id=d2.id, uploader_id=u_gm.id, normalized={"k": "v2"})
            s.add_all([rep1, rep2])
            s.commit()

        # Create an async session to run repository queries
        async_engine = create_async_engine(async_url, echo=False)
        AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

        async with AsyncSessionLocal() as async_session:
            # Refresh role/user objects from DB for accurate ids
            q = await async_session.execute(Report.select())
            # Load user & roles
            u_dept_row = (await async_session.execute(User.select().where(User.username == 'alice'))).scalars().one()
            r_dept_row = (await async_session.execute(Role.select().where(Role.name == 'DepartmentUser'))).scalars().one()
            u_gm_row = (await async_session.execute(User.select().where(User.username == 'bob'))).scalars().one()
            r_gm_row = (await async_session.execute(Role.select().where(Role.name == 'GeneralManager'))).scalars().one()

            # Department user should only see FIN report
            dept_reports = await list_reports_for_user(u_dept_row, async_session, r_dept_row)
            assert len(dept_reports) == 1
            assert dept_reports[0].department_id != None

            # General manager should see both
            gm_reports = await list_reports_for_user(u_gm_row, async_session, r_gm_row)
            assert len(gm_reports) >= 2

    asyncio.run(_run())
