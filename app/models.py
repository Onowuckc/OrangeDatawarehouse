from typing import Optional
from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime, timezone

USER_FK = "user.id"
DEPT_FK = "department.id"
ROLE_FK = "role.id"

class Department(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)
    name: str

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    role_id: int = Field(foreign_key=ROLE_FK, index=True)

class UserDepartmentLink(SQLModel, table=True):
    __tablename__ = "user_department_access"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key=USER_FK, index=True)
    department_id: int = Field(foreign_key=DEPT_FK, index=True)

class StagingReport(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    department_id: int = Field(foreign_key=DEPT_FK, index=True)
    uploader_id: Optional[int] = Field(default=None, foreign_key=USER_FK)
    raw_payload: dict = Field(sa_column=Column(JSON))
    filename: Optional[str] = None
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc), index=True)
    status: str = Field(default="received")

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    department_id: int = Field(foreign_key=DEPT_FK, index=True)
    uploader_id: Optional[int] = Field(default=None, foreign_key=USER_FK)
    report_date: Optional[datetime] = Field(default=None, index=True)
    version: Optional[str] = None
    status: str = Field(default="active")
    normalized: dict = Field(sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc), index=True)
