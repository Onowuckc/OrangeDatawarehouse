from typing import AsyncGenerator
from .db import get_session

async def get_db() -> AsyncGenerator:
    async with get_session() as session:
        yield session
