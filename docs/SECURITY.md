# Security notes

- Password storage
  - We use `passlib` with `bcrypt` to hash passwords before storing in DB (`User.hashed_password`).
  - Never log or expose the hashed password externally.

- Tokens
  - Dev uses a symmetric JWT secret; in production use a strong secret or an asymmetric key pair and rotate regularly.

- RBAC
  - Role-based filtering is implemented at repository level (`list_reports_for_user`) and enforced in endpoints that return report data.
  - Consider adding Postgres RLS policies as an additional enforcement layer for defense-in-depth.
- Department passwords (.env)
  - Department login passwords are read from environment variables in the form `DEPT_PASS_{CODE}` (e.g., `DEPT_PASS_FIN`). For local development you can place them in a `.env` file at the project root (see `.env.example`).
  - Do NOT commit `.env` to source control; `.env` is included in `.gitignore`.
  - For production, use a secrets manager (AWS Secrets Manager, Parameter Store) and inject secrets into your runtime environment instead of using a plaintext `.env`.
- Data classification
  - Raw payloads are stored in `stagingreport.raw_payload` and should be treated as PII if incoming payloads may contain it.
  - Apply appropriate encryption/retention policies as required by compliance.
