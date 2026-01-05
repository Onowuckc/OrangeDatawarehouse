# Database Schema (high level)

- `users` (table `user`)
  - `id`, `username`, `hashed_password`, `role_id`
  - Passwords are stored **hashed** (bcrypt). Do not store plain text.

- `departments` (table `department`)
  - `id`, `code`, `name`

- `user_department_access` (table `user_department_access`)
  - mapping table that defines which departments a user can access

- `reports_staging` (table `stagingreport`)
  - `id`, `department_id`, `uploader_id`, `raw_payload` (JSON), `filename`, `uploaded_at`, `status`
  - Designed to keep the original submitted payload for auditing and retry

- `reports` (table `report`)
  - `id`, `department_id`, `uploader_id`, `report_date`, `version`, `status`, `normalized` (JSON), `created_at`
  - Normalized JSON contains canonical fields used for analytics; JSONB is recommended in Postgres for indexing and querying

Notes:
- Use JSONB (Postgres) for `raw_payload` / `normalized` to allow indexing (GIN) and efficient querying.
- Keep a clear separation between immutable staging raw payloads and the canonical normalized warehouse records.
