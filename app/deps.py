from typing import AsyncGenerator, Optional
from fastapi import Header, HTTPException
from .db import get_session
from .auth import decode_token

async def get_db() -> AsyncGenerator:
    async with get_session() as session:
        yield session

async def get_current_principal(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload
