# Legal Analysis Blueprint – Technical Architecture

## Overview

The blueprint follows the KAPI backwards-build methodology:

1. **Spec** – Remediation spec + API contracts (this folder)
2. **Architecture** – Shared components + Flask service modules
3. **Tests** – Backend pytest suite and CRA Jest harness
4. **Code** – Flask multi-agent API and React console
5. **Sync** – Scripts (`setup_legal_database.py`) and documentation updates

## System Diagram

```
┌──────────────────────┐      ┌────────────────────────┐
│  React Operations UI │───►  │  Flask REST API        │
│  (tabs: research,    │      │  (app.py)              │
│   documents, cases,  │      │                        │
│   chat, ethics)      │      │  ├─ Research endpoints │
└──────────────────────┘      │  ├─ Document analysis  │
                              │  ├─ Case management    │
                              │  ├─ Privileged chat    │
                              │  └─ Ethics audits      │
                              └──────────┬────────────┘
                                         │
                ┌────────────────────────┼──────────────────────────┐
                │                        │                          │
┌────────────────────────┐   ┌────────────────────────┐   ┌─────────────────────────┐
│ Shared Legal Agents    │   │ Privilege/Ethics       │   │ Data Stores             │
│ (components/backend)   │   │ Managers (components)  │   │                         │
│  - BaseLegalAgent      │   │  - AttorneyClient...   │   │  - SQLite (matters,     │
│  - Research agent      │   │  - LegalEthics...      │   │    communications,      │
│  - Document agent      │   │                         │   │    audit logs)          │
│  - Case agent          │   │                         │   │  - ChromaDB (precedent  │
│  - Precedent agent     │   │                         │   │    embeddings)          │
└────────────────────────┘   └────────────────────────┘   └─────────────────────────┘
```

## Backend Modules

- `app.py` – Flask API with stub mode for unit tests
- `agents/` – Domain-specific agents extending shared components
  - `research_agent.py`
  - `document_agent.py`
  - `case_agent.py`
  - `precedent_agent.py`
  - `privileged_chat_agent.py`
- `database/`
  - `sqlite_legal_manager.py` – persistence + case helpers
  - `chromadb_legal_manager.py` – vector retrieval
- `utils/` – re-exported shared components for privilege + ethics

### Request Flow Example

1. React UI submits `/api/research` with question + filters
2. Flask `run_research` calls `LegalResearchAgent.run_research`
3. Agent pulls authorities from Chroma + structured DB; generates memo via Gemini
4. Results persist through `LegalDataManager.store_legal_research`
5. Response returns memo, citations, and ethics check to UI

## Frontend Modules

- `src/App.js` – Shell with tab navigation
- `src/components/` – Feature panels (research, documents, cases, chat, ethics)
- `src/services/api.js` – Fetch wrapper with base URL configuration
- Styling: `App.css` (glassmorphism dashboard)

## Testing Strategy

- **Backend**: `backend/tests/test_api.py` uses stub mode to exercise endpoints (pytest + Flask test client)
- **Frontend**: `frontend/src/App.test.js` mocks fetch to verify navigation + research flow (Jest + RTL)
- **LLM Isolation**: `LEGAL_BLUEPRINT_UNIT_TEST=true` toggles stub agents to avoid external calls during CI

## Deployment Notes

- `backend/requirements.txt` captures Python deps (Flask, chromadb, google-generativeai, etc.)
- `frontend/package.json` handles CRA build scripts
- `.env.example` enumerates secrets + toggles
- Compose/Docker recipes are future work (tracked in remediation spec Phase 3)

