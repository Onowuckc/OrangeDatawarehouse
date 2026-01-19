# OrangeDatawarehouse

[![CI](https://github.com/Onowuckc/OrangeDatawarehouse/actions/workflows/ci.yml/badge.svg)](https://github.com/Onowuckc/OrangeDatawarehouse/actions/workflows/ci.yml)

A minimal internal data warehouse platform (FastAPI + SQLModel + Celery). See `frontend/README.md` for frontend run instructions.

## Quick start — after cloning (local dev) ⚙️

1. Clone the repo and enter the directory:
```bash
git clone https://github.com/Onowuckc/OrangeDatawarehouse.git
cd OrangeDatawarehouse
```

2. Create and activate a virtual environment:
- Windows (PowerShell / bash): 
```bash
python -m venv .venv
source .venv/Scripts/activate
```
- macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and set required variables (for example `DATABASE_URL`, `JWT_SECRET`, and `DEPT_PASS_*`). The project loads `.env` automatically in development.

5. Ensure a Postgres database is available. The default `DATABASE_URL` in `.env.example` points to `postgres://postgres:postgres@localhost/dwdb`. Create the database or adjust `DATABASE_URL` as needed.

6. Initialize the database schema:
```bash
python -c "from app.db import init_db; init_db()"
```

7. Start the backend:
```bash
uvicorn app.main:app --reload --port 8000
```

8. Start the frontend (in a separate terminal):
```bash
cd frontend
npm install
npm run dev
```

9. Run the test suite:
```bash
pytest
```

---

## How to use — quick walkthrough ✅

This short guide shows how to log in using a department password (env var `DEPT_PASS_{CODE}`) and submit a report via curl.

### 1) Set a department password (development)
Add a line to your `.env` (or set the env var directly):

```
DEPT_PASS_SAL=sales-secret
```

The app uses `python-dotenv` in development so a `.env` file at the project root will be loaded.

### 2) Log in with the department password
Use the `/auth/login` endpoint. The `role` field is used to pass the department code when authenticating by department password:

```bash
curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"reporter@example.com","password":"sales-secret","role":"SAL"}'
```

A successful response includes an `access_token` (and `dept` and optional `dept_id`):

```json
{"access_token":"<token>","token_type":"bearer","dept":"SAL","dept_id":1}
```

### 3) Submit a report
Use the returned token to POST to `/reports/submit`:

```bash
curl -s -X POST http://localhost:8000/reports/submit \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "department_code":"SAL",
    "payload": {"orders": [{"id": 1, "amount": 123.45}]},
    "filename": "sales-2026-01.json",
    "report_date":"2026-01-12T00:00:00Z",
    "version":"v1"
  }'
```

A successful response will return the saved normalized report object.

### Example: upload CSV / Excel file via curl

```bash
curl -v -X POST http://localhost:8000/reports/submit-file \
  -H "Authorization: Bearer <token>" \
  -F "department_code=SAL" \
  -F "file=@/path/to/sales-2026-01.csv" \
  -F "filename=sales-2026-01.csv"
```

> Tip: To test per-user credentials instead, register a user via `/auth/register` and log in with `/auth/login` using the user's `username` and `password`.

---
