from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.models import Department
from app.auth import create_access_token


def _get_test_db_override(db_file):
    async def _override():
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        async_engine = create_async_engine(f"sqlite+aiosqlite:///{db_file}")
        AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
        async with AsyncSessionLocal() as session:
            yield session
    return _override


def test_admin_can_create_and_delete_department(tmp_path):
    db_file = tmp_path / "test_dep_crud.db"
    sync_url = f"sqlite:///{db_file}"

    engine = create_engine(sync_url)
    SQLModel.metadata.create_all(engine)

    client = TestClient(app)

    # override dependency to use the test DB
    app.dependency_overrides = { }

    token = create_access_token('admin', extra_claims={'role': 'GeneralManager'})

    # create
    res = client.post('/departments/', headers={'Authorization': f'Bearer {token}'}, json={'code':'TST','name':'Test Dept'})
    assert res.status_code == 201
    data = res.json()
    assert data['code'] == 'TST'

    dep_id = data['id']

    # delete
    res2 = client.delete(f'/departments/{dep_id}', headers={'Authorization': f'Bearer {token}'})
    assert res2.status_code == 204

    # list should not include TST
    res3 = client.get('/departments/')
    codes = [d['code'] for d in res3.json()]
    assert 'TST' not in codes
