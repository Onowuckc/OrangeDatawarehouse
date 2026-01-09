from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.models import Department


def test_departments_list(tmp_path, monkeypatch):
    db_file = tmp_path / "test_departments.db"
    sync_url = f"sqlite:///{db_file}"

    engine = create_engine(sync_url)
    SQLModel.metadata.create_all(engine)

    # Insert departments
    with Session(engine) as s:
        s.add(Department(code="SAL", name="Sales"))
        s.add(Department(code="MKT", name="Marketing"))
        s.add(Department(code="SUP", name="SupplyChain"))
        s.add(Department(code="FIN", name="Finance"))
        s.add(Department(code="PROD", name="Production"))
        s.add(Department(code="ADM", name="Admin"))
        s.commit()

    # Override dependency to use this engine
    async def _get_db_override():
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        async_engine = create_async_engine(f"sqlite+aiosqlite:///{db_file}")
        AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
        async with AsyncSessionLocal() as session:
            yield session

    app.dependency_overrides = { }

    client = TestClient(app)

    res = client.get("/departments/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    codes = [d["code"] for d in data]
    for expected in ("SAL", "MKT", "SUP", "FIN", "PROD", "ADM"):
        assert expected in codes
