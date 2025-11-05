# FastAPI Fullstack Starter (Slim)

Curated version of the official FastAPI full-stack template trimmed for KAPI quick wins. Ships a production-grade FastAPI API, React admin dashboard, and PostgreSQL stack with Docker Compose.

## Stack Overview
- **FastAPI + SQLModel** for the backend REST API and database layer.
- **JWT authentication** with first-superuser bootstrap and password reset flows.
- **React + Vite + Chakra UI** frontend served via Nginx.
- **PostgreSQL 17** database with Alembic migrations.
- **Docker Compose** orchestrating db, backend, and frontend containers.

## Project Layout
```
fastapi-fullstack-official/
├── backend/         # FastAPI application
├── frontend/        # React admin dashboard
├── docker-compose.yml
├── .env.example
├── development.md   # Local workflow tips
└── deployment.md    # Production checklist
```

## Quick Start (Docker Compose)
1. Install Docker Desktop (or Docker Engine + Compose plugin).
2. Copy the sample environment and adjust secrets as needed:
   ```bash
   cp .env.example .env
   ```
3. Launch the stack:
   ```bash
   docker compose up --build
   ```
4. Visit the services:
   - API: http://localhost:8000/docs
   - Frontend: http://localhost:5173
   - PostgreSQL is exposed on port 5432 for local tools.

The `prestart` service runs migrations and seeds the first superuser (`FIRST_SUPERUSER`). Update the password and email before deploying anywhere beyond local.

## Running Services Locally (Optional)
You can stop individual containers and run the apps with hot reload:

```bash
# Backend (requires uv and Python 3.10+)
cd backend
uv sync
source .venv/bin/activate
fastapi dev app/main.py

# Frontend (requires Node 18+)
cd frontend
npm install
npm run dev
```

Keep the database container running with `docker compose up db` when using the local dev servers.

## Production Notes
- Replace default secrets in `.env` (`SECRET_KEY`, `POSTGRES_PASSWORD`, `FIRST_SUPERUSER_PASSWORD`).
- Attach the stack to your ingress/reverse proxy (Nginx, Traefik, Caddy) or configure TLS directly on the host.
- Configure SMTP values if you want password recovery emails.
- Run `docker compose up --build -d` on your server after copying the project and `.env` file.

See `deployment.md` for a concise production checklist and `development.md` for day-to-day workflow tips.
