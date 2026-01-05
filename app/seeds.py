from .models import Department, Role, User
from .auth import hash_password

async def seed(session):
    # Minimal seeding for dev purposes
    deps = [Department(code="FIN", name="Finance"), Department(code="OPS", name="Operations")]
    for d in deps:
        session.add(d)
    roles = [Role(name="DepartmentUser"), Role(name="SeniorManager"), Role(name="GeneralManager")]
    for r in roles:
        session.add(r)
    await session.commit()

    # Create a default user
    user = User(username="admin", password_hash=hash_password("admin"), role_id=1)
    session.add(user)
    await session.commit()
