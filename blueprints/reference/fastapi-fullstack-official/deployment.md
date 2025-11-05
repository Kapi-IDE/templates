# FastAPI Fullstack Starter – Deployment Checklist

## 1. Provision Infrastructure
- Ubuntu/Debian host or cloud VM with Docker Engine + Compose installed.
- DNS records pointing `api.yourdomain.com` and `dashboard.yourdomain.com` (or a single domain behind a proxy) to the server.
- Optional: external reverse proxy (Nginx, Traefik, Caddy) terminating TLS.

## 2. Prepare Application Secrets
1. Copy `.env.example` to `.env` and update every `changeme` value:
   - `SECRET_KEY`, `POSTGRES_PASSWORD`, `FIRST_SUPERUSER_PASSWORD`
   - `FRONTEND_HOST`, `BACKEND_CORS_ORIGINS`
   - SMTP credentials if you need password recovery emails
   - `VITE_API_URL=https://api.yourdomain.com`
2. Copy the project and `.env` to the server (`rsync` or `scp`).

## 3. Deploy with Docker Compose
```bash
ssh user@server
cd /path/to/fastapi-fullstack-official
cp .env.example .env  # if not copied already
# edit .env as described above
docker compose up --build -d
```

The `prestart` task runs migrations and seeds the admin user on the first boot. Subsequent `docker compose up -d` commands skip the bootstrap step.

## 4. Expose the Services
- If you already run a reverse proxy, route traffic to:
  - Backend container → `localhost:8000`
  - Frontend container → `localhost:5173`
- Without an external proxy you can use an Nginx server block or Caddyfile on the host to provide HTTPS termination.

## 5. Operations
- View logs: `docker compose logs -f backend` (or `frontend`, `db`).
- Apply migrations after code updates: `docker compose run --rm prestart`.
- Update images/config:
  ```bash
  git pull
  docker compose build
  docker compose up -d
  ```
- Backup Postgres data by copying the `app-db-data` volume or running `pg_dump` via `docker compose exec db pg_dump ...`.

## 6. Hardening Tips
- Create a dedicated Postgres user/password per deployment.
- Configure SMTP + Sentry DSN for production observability.
- Rotate the first superuser password and create named accounts for real users.
- Automate deployments with CI (GitHub Actions, GitLab CI) running the commands above.

You're ready to plug this blueprint into KAPI's catalog or adapt it for custom SaaS starters.
