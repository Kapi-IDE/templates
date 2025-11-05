# Legal Analysis Suite

Multi-agent legal intelligence blueprint delivering research, document analysis, case management, privileged chat, and ethics auditing out of the box. Built with Flask + shared legal components on the backend and a React operations console on the frontend.

## Backwards Build Status
- **Spec** – Remediation spec, API contract, architecture, and UI flows (see `specification/`)
- **Architecture** – Agents reuse shared components, SQLite/Chroma persistence wired in `backend/`
- **Tests** – Backend pytest suite + CRA Jest smoke test
- **Code** – Production-ready Flask routes and React glassmorphism UI
- **Sync** – Usage guide, metadata, and seed scripts updated

## Key Features
- Natural-language legal research with cited authorities and ethics disclosure checks
- Contract/brief analysis that surfaces risk indicators and related templates
- Case management with automated strategy analysis and precedent discovery
- Privileged attorney-client chat with encrypted logging and compliance telemetry
- Ethics dashboard summarising privilege events, disclosures, and compliance scores

## Architecture Snapshot
- **Backend**: Flask REST API (`backend/app.py`) orchestrating shared agents (`templates/components/backend/legal-ai`).
  - LegalResearchAgent, DocumentReviewAgent, CaseAnalysisAgent, PrecedentMiningAgent, PrivilegedChatAgent
  - SQLite legal data manager + ChromaDB knowledge store + privilege/ethics managers
  - `LEGAL_BLUEPRINT_UNIT_TEST=true` enables stub mode for deterministic tests
- **Frontend**: React 18 console (`frontend/src`) with tabbed navigation, fetch-based API service, PropTypes components
- **Data**: `backend/database/` seeds legal cases, statutes, and precedent embeddings

## Setup & Usage

### Backend
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill GOOGLE_API_KEY, SECRET_KEY, LEGAL_ENCRYPTION_KEY
python setup_legal_database.py  # seeds SQLite + ChromaDB
flask run  # or python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```
Set `REACT_APP_API_BASE_URL=http://localhost:5000` if the backend runs on a different origin.

### Testing
```bash
# Backend (uses stub mode automatically)
cd backend
python -m pytest

# Frontend
d cd frontend
npm test
```
Both suites default to stubbed dependencies to avoid live Gemini calls.

## Directory Guide
```
backend/
  app.py                  # Flask API with stub support for tests
  agents/                 # Multi-agent orchestration using shared components
  database/               # SQLite + Chroma managers and seed scripts
  tests/                  # Pytest API smoke tests
frontend/
  src/components/         # Research, documents, cases, chat, ethics panels
  src/services/api.js     # Fetch wrapper for REST endpoints
  src/App.js              # Tabbed operations console
specification/
  api-contracts.yaml      # OpenAPI summary for endpoints
  technical-architecture.md
  ui-flows.md
scripts/
  run_legal_ai_pod.py     # Legacy helper preserved for compatibility
```

## Next Steps
- [ ] Add Docker Compose definition bundling backend + frontend + Chroma volume
- [ ] Expand pytest coverage to privileged chat edge cases and ethics logging
- [ ] Integrate real LLM fixtures for offline regression (`tests/fixtures/agents/legal`)
- [ ] Build deployment runbook in `documentation/`

