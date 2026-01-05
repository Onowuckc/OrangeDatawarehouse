from fastapi import APIRouter, HTTPException, Depends
from ..auth import create_access_token, hash_password
from ..schemas import UserCreate
from ..deps import get_db
from ..models import Role, User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def token(form: UserCreate):
    # Minimal: accept any credentials and return a token (dev only)
    token = create_access_token(form.username)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", status_code=201)
async def register(form: UserCreate, db=Depends(get_db)):
    # Create or find role
    q = await db.execute(Role.select().where(Role.name == form.role))
    role = q.scalars().one_or_none()
    if not role:
        role = Role(name=form.role)
        db.add(role)
        await db.commit()
        await db.refresh(role)

    user = User(username=form.username, hashed_password=hash_password(form.password), role_id=role.id)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"id": user.id, "username": user.username, "role": role.name}
