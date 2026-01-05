from typing import Optional, Any
from pydantic import BaseModel
from datetime import datetime

class AuthToken(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class ReportSubmit(BaseModel):
    department_code: str
    payload: Any
    filename: Optional[str] = None
    report_date: Optional[datetime] = None
    version: Optional[str] = None

class ReportOut(BaseModel):
    id: int
    department_id: int
    uploader_id: int
    report_date: Optional[datetime]
    version: Optional[str]
    status: str
    normalized: Any
    created_at: datetime

    class Config:
        orm_mode = True
