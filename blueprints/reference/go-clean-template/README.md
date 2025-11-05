# Go Clean Template (Slim)

Curated version of Evrone's Go Clean Architecture starter. Keeps the production-ready service layout while stripping marketing badges, extra docs, and integration harnesses so you can boot a clean service in minutes.

## What You Get
- Clean Architecture layers (`cmd`, `internal`, `pkg`) with Fiber HTTP endpoints.
- PostgreSQL persistence with migrations under `migrations/`.
- Structured logging (zerolog), validation, Swagger, Prometheus metrics.
- Docker Compose wiring for app + PostgreSQL.

## Quick Start
```bash
cd go-clean-template
cp .env.example .env        # adjust secrets/URLs if needed
make compose-up             # starts PostgreSQL dependency
make run                    # runs migrations and launches the service locally
```

After the service starts:
- REST API → http://localhost:8080 (health check at `/healthz`, Swagger at `/swagger` if enabled)
- PostgreSQL → postgres://user:myAwEsOm3pa55@w0rd@localhost:5432/db

Stop everything with `make compose-down`.

Prefer containers only? Run `docker compose up --build` to launch both the API and database in Docker.

## Project Layout
```
cmd/app/main.go         # entry point (logger + DI wiring)
config/config.go        # env-driven configuration
internal/               # controllers, use cases, entities, repositories
pkg/                    # shared libraries (logger, http server, postgres helpers)
migrations/             # database migrations
Dockerfile              # production build (multi-stage)
docker-compose.yml      # local stack (Postgres dependency + optional app container)
```

## Development Tips
- Use `make test` for unit tests and `make lint` for golangci-lint (config kept in `.golangci.yml`).
- Update env vars in `.env` when running binaries directly (`go run ./cmd/app`).
- Metrics and Swagger can be toggled using `METRICS_ENABLED` and `SWAGGER_ENABLED` env vars.

Ready to slot into the KAPI blueprint catalog as the Go reference implementation.
