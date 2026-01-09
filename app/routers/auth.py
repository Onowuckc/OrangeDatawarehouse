from fastapi import APIRouter, HTTPException, Depends
from ..auth import create_access_token, hash_password, verify_password
from ..schemas import UserCreate
from ..deps import get_db
from ..models import Role, User
import os

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

@router.post('/login')
async def login(form: UserCreate, db=Depends(get_db)):
    """Authenticate by department password (env) OR by per-user credentials.

    - For department logins, provide username (email), password and role "DepartmentUser" and a department code will be provided under `UserCreate.role` for backwards compatibility (we'll reuse the role field to pass department code client-side).
    """
    # Expect role to be department code for department logins, or a real role for user logins
    department_code = form.role

    # Try department password env var first: DEPT_PASS_{CODE}
    env_key = f"DEPT_PASS_{department_code}" if department_code else None
    if env_key and os.getenv(env_key):
        env_pw = os.getenv(env_key)
        if form.password == env_pw:
            # authorized as a department user — create a token with department claim
            token = create_access_token(form.username)
            return {"access_token": token, "token_type": "bearer", "dept": department_code}

    # Fallback to per-user auth
    q = await db.execute(User.select().where(User.username == form.username))
    user = q.scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Successful user login
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}
