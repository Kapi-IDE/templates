# Usage Guide – Legal Analysis Suite

Follow these steps to install, seed, test, and run the blueprint locally.

## 1. Backend
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Populate GOOGLE_API_KEY, SECRET_KEY, LEGAL_ENCRYPTION_KEY in .env
python setup_legal_database.py  # seeds SQLite + ChromaDB
flask run  # or python app.py
```
- API lives at `http://localhost:5000`
- Set `LEGAL_BLUEPRINT_UNIT_TEST=true` to boot in stub mode (no external LLM calls)

### Backend Tests
```bash
LEGAL_BLUEPRINT_UNIT_TEST=true python -m pytest
```
This hits the Flask endpoints using the stubbed data managers.

## 2. Frontend
```bash
cd frontend
npm install
npm start
```
- Browser launches `http://localhost:3000`
- Overwrite API origin with `REACT_APP_API_BASE_URL` if necessary

### Frontend Tests
```bash
npm test
```
Jest mocks fetch to validate navigation and research flow rendering.

## 3. Verification Checklist
- ✅ `GET /api/health` returns `healthy`
- ✅ Research tab produces memo + authorities for a sample question
- ✅ Document tab surfaces risks for pasted contract text
- ✅ Case tab lists newly created matter and returns strategy analysis
- ✅ Privileged chat establishes a session and echoes compliance-safe response
- ✅ Ethics tab shows compliance metrics

## 4. Deployment Notes
- Bundle backend + frontend via Docker Compose (future work tracked in remediation spec)
- Replace SQLite with managed Postgres and configure persistent Chroma storage for production
- Provide production secrets through environment or secret manager

