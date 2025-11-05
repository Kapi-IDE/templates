# FastAPI Fullstack Starter – Development Guide

## 1. Launch the Full Stack
```bash
# run from repository root
cp .env.example .env  # only first time
docker compose up --build
```

Available endpoints:
- Frontend dashboard → http://localhost:5173
- Backend API + docs → http://localhost:8000 / http://localhost:8000/docs
- PostgreSQL → localhost:5432 (use your favourite DB client)

Use `docker compose logs -f backend` (or `db`, `frontend`) to tail logs. Stop everything with `Ctrl+C` or `docker compose down`.

## 2. Hot-Reload Development
You can run backend or frontend outside Docker while keeping Postgres in the container.

```bash
# Backend
docker compose stop backend
cd backend
uv sync
source .venv/bin/activate
fastapi dev app/main.py

# Frontend
docker compose stop frontend
cd frontend
npm install
npm run dev
```

The local servers reuse the same ports as Docker, so browser URLs stay the same. Restart the containers afterwards with `docker compose up backend frontend`.

## 3. Database & Migrations
- Apply migrations manually with `docker compose run --rm prestart` (it runs `alembic upgrade head` and seeds data).
- To create new migrations:
  ```bash
  cd backend
  uv run alembic revision --autogenerate -m "Add new table"
  uv run alembic upgrade head
  ```

## 4. Testing & Quality Gates
```bash
cd backend
uv run pytest
uv run mypy
uv run ruff check

cd ../frontend
npm run test
npm run lint
```

## 5. Useful Docker Commands
```bash
# rebuild containers after dependency changes
docker compose build backend frontend

# remove containers/volumes
docker compose down -v

# open a shell in the backend container
docker compose run --rm backend bash
```

Keep `.env` in sync across the team (commit a redacted version or share securely). Rotate secrets before staging or production deployments.
