from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.models import Department
from app.auth import create_access_token


def test_soft_delete_and_restore(tmp_path):
    db_file = tmp_path / "test_dep_soft.db"
    sync_url = f"sqlite:///{db_file}"

    engine = create_engine(sync_url)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as s:
        d = Department(code='TST', name='Test')
        s.add(d)
        s.commit()

    client = TestClient(app)
    token = create_access_token('admin', extra_claims={'role': 'GeneralManager'})

    # soft-delete
    res = client.delete('/departments/1', headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 202
    assert res.json()['status'] == 'pending_delete'

    # list should not include deleted departments
    res2 = client.get('/departments/')
    codes = [d['code'] for d in res2.json()]
    assert 'TST' not in codes

    # restore
    res3 = client.post('/departments/1/restore', headers={'Authorization': f'Bearer {token}'})
    assert res3.status_code == 200
    # now list should include it
    res4 = client.get('/departments/')
    codes2 = [d['code'] for d in res4.json()]
    assert 'TST' in codes2
