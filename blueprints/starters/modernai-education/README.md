# ModernAI Education Platform Starter

Full-stack starter that marries a FastAPI backend with a React + Chakra UI frontend for building modern education experiences (quizzes, live sessions, onboarding, dashboards).

## Stack
- **Backend**: FastAPI, SQLAlchemy, Alembic, SQLAdmin
- **Frontend**: React, Chakra UI, React Router
- **Database**: PostgreSQL

## Getting Started
### Backend
```bash
cd backend
poetry install
export SECRET_KEY="replace-with-strong-secret"
poetry run uvicorn app.main:app --reload --port 8001
```

> The API will refuse to start if `SECRET_KEY` is missing.

### Frontend
```bash
cd frontend
npm install
npm start
```

The frontend expects the API at `http://localhost:8001`—adjust constants in `frontend/src/Constants.js` if needed.

## Features
- Quiz engine with celebratory animations
- Onboarding forms and pair programming UX
- Admin dashboard via SQLAdmin (`/admin`)
- React components for live classes, recordings, learning paths, and surveys

## Deployment
- Containerize both services or deploy separately (e.g., Render + Vercel)
- Configure environment variables/tweak CORS in `backend/app/main.py`

## Next Steps
- Seed quiz content via Alembic or SQL scripts
- Integrate real auth providers, analytics, and notifications as needed
