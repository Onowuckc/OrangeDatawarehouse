# Security notes

- Password storage
  - We use `passlib` with `bcrypt` to hash passwords before storing in DB (`User.hashed_password`).
  - Never log or expose the hashed password externally.

- Tokens
  - Dev uses a symmetric JWT secret; in production use a strong secret or an asymmetric key pair and rotate regularly.

- RBAC
  - Role-based filtering is implemented at repository level (`list_reports_for_user`) and enforced in endpoints that return report data.
  - Consider adding Postgres RLS policies as an additional enforcement layer for defense-in-depth.

- Data classification
  - Raw payloads are stored in `stagingreport.raw_payload` and should be treated as PII if incoming payloads may contain it.
  - Apply appropriate encryption/retention policies as required by compliance.
