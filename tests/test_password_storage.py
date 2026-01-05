import asyncio
from sqlmodel import SQLModel, create_engine, Session
from app.auth import hash_password, verify_password
from app.models import User, Role


def test_passwords_are_hashed(tmp_path):
    db_file = tmp_path / "test_pw.db"
    sync_url = f"sqlite:///{db_file}"

    # Create tables
    engine = create_engine(sync_url)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as s:
        role = Role(name="DepartmentUser")
        s.add(role)
        s.commit()

        plain = "s3cret"
        hpw = hash_password(plain)
        user = User(username="pwuser", hashed_password=hpw, role_id=role.id)
        s.add(user)
        s.commit()

        stored = s.exec(User.select().where(User.username == "pwuser")).one()
        assert stored.hashed_password != plain
        assert verify_password(plain, stored.hashed_password) is True
