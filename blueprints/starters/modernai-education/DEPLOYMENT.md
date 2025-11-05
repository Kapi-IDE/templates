# Deployment Guide

## Backend
1. Set environment variables (`DATABASE_URL`, `SECRET_KEY`, etc.) in `backend/.env`.
2. Run migrations: `poetry run alembic upgrade head`.
3. Deploy with Uvicorn/Gunicorn or containerize using the provided scripts.

## Frontend
1. Update API endpoints in `frontend/src/Constants.js`.
2. Build: `npm run build`.
3. Deploy to Netlify/Vercel (static hosting with SPA fallback).

## Docker (example)
- Create docker-compose linking backend, Postgres, and frontend build container.
- Ensure backend exposes API with proper CORS settings.
