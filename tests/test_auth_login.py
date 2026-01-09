import os
from sqlmodel import SQLModel, create_engine, Session
from app.auth import hash_password
from app.models import User, Role
from app.routers.auth import login


def test_department_login_env(tmp_path, monkeypatch):
    db_file = tmp_path / "test_auth.db"
    sync_url = f"sqlite:///{db_file}"

    engine = create_engine(sync_url)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as s:
        r = Role(name="DepartmentUser")
        s.add(r)
        s.commit()

    monkeypatch.setenv('DEPT_PASS_FIN', 'fin-secret')

    class F:
        username = 'deptuser@example.com'
        password = 'fin-secret'
        role = 'FIN'

    res = login(F())
    assert 'access_token' in res
    assert res['dept'] == 'FIN'
