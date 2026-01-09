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

    # Create a default user (use correct field name `hashed_password`)
    q = await session.execute(Role.select().where(Role.name == "GeneralManager"))
    gm_role = q.scalars().one_or_none()
    role_id = gm_role.id if gm_role else 1

    user = User(username="admin", hashed_password=hash_password("admin"), role_id=role_id)
    session.add(user)
    await session.commit()
