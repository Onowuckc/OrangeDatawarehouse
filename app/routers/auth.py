from fastapi import APIRouter, HTTPException
from ..auth import create_access_token
from ..schemas import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def token(form: UserCreate):
    # Minimal: accept any credentials and return a token (dev only)
    token = create_access_token(form.username)
    return {"access_token": token, "token_type": "bearer"}
