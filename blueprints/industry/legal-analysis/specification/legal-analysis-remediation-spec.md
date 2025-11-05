# Legal Analysis Blueprint Remediation Spec

| Field | Value |
| :-- | :-- |
| **Blueprint** | `industry/legal-analysis` |
| **Status** | `SPEC DRAFT` |
| **Author** | Codex Agent |
| **Last Updated** | 2025-10-08 |
| **Goal** | Close blueprint gaps so the Legal Analysis application ships production-ready artifacts consistent with `FEAT-SPEC-007` |

---

## 1. Situation Overview

- The quick wins catalog and blueprint spec require complete, installable apps with API, frontend, data, docs, and deployment recipes.
- Current legal blueprint only ships agent backbones and sample data. Flask app and React client are placeholders. Requirements, deployment, and tests are missing.
- This spec outlines the remediation scope so we can move through **spec → architecture → tests → code → sync** without vibe coding.

### 1.1 Success Definition

We consider the blueprint production-ready when:
- Backend exposes documented REST endpoints for legal research, document analysis, case management, privileged chat, and ethics compliance.
- Requirements, environment variables, and sample data install via a single recipe.
- React frontend renders working flows for research, document uploads, case boards, and privileged messaging.
- Automated tests cover critical paths (≥90% coverage target) with fixtures for legal agents.
- Docker + docs enable local and cloud deployment without manual guesswork.
- Living specs, API contracts, and runbooks live inside the blueprint for future students.

---

## 2. Gap Analysis

| Area | Expected (per `blueprint-quickwins.md` + `07-blueprint.spec.md`) | Current State | Severity |
| :-- | :-- | :-- | :-- |
| **Backend API** | Flask/FastAPI service with full endpoints, auth, agent orchestration | `app.py` returns "Flask backend is running" | 🔴 Critical |
| **Dependencies** | Complete `requirements.txt` with agents, DB, auth, security | Only `Flask>=2.0` | 🔴 Critical |
| **Agent Integration** | REST routes call legal agents + ChromaDB knowledge | Agents exist but unused | 🔴 Critical |
| **Database** | Automated migration + seed scripts executed via recipe | Scripts exist but not wired to app | 🟡 Major |
| **Frontend UI** | React components implementing research, analysis, case views | Skeleton only | 🔴 Critical |
| **API Client Layer** | Typed client/React query wrappers | Missing | 🟡 Major |
| **Deployment** | Dockerfile, docker-compose, `.env.example`, runbooks | Not present | 🔴 Critical |
| **Testing** | Unit + integration tests with fixtures, ≥90% coverage | None | 🔴 Critical |
| **Docs** | Living spec, API contract, setup guide, troubleshooting | README over-promises; no detailed specs | 🟡 Major |

---

## 3. Remediation Backlog (Spec → Architecture → Tests → Code → Sync)

### 3.1 Phase 0 – Spec Assets (This document)
- [x] Readiness spec describing gaps, success criteria, and backlog.
- [ ] Draft API contract (OpenAPI) covering all REST endpoints.
- [ ] Draft system architecture diagram + component responsibilities.
- [ ] Draft UX flows + screen outlines for React app.

### 3.2 Phase 1 – Architecture & Recipes
- Backend
  - Define service layer contracts for Research, Document, Case, Ethics modules.
  - Specify dependency list (`Flask`, `Flask-CORS`, `Pydantic`, `SQLAlchemy`, `ChromaDB`, `langchain`, `redis` for rate limiting, etc.).
  - Describe background tasks / async strategy for long-running analysis.
  - Connect to existing SQLite/Chroma DB scripts; ensure idempotent bootstrap.
- Frontend
  - Choose stack (React + Vite + TypeScript). Document state management (React Query + Zustand) and component hierarchy.
  - Define API client + hooks per endpoint.
- Deployment
  - Plan Docker images (backend, frontend, vector DB), docker-compose, and `.env.example` coverage.
  - Recipe YAML enumerating install steps used by blueprint installer.

### 3.3 Phase 2 – Test Plans
- Backend tests
  - Unit tests for agent orchestrators with stubbed LLM responses (fixtures under `tests/fixtures/agents/legal`).
  - Integration tests hitting REST endpoints with SQLite + Chroma test DB.
- Frontend tests
  - Component tests using Vitest/React Testing Library for core flows.
  - Cypress/Playwright smoke for E2E legal workflow.
- Non-functional
  - Security tests for privilege enforcement routes.
  - Performance baseline for long-running research jobs.

### 3.4 Phase 3 – Implementation Tasks
- Backend
  1. Build Flask blueprint modules: `research`, `document_analysis`, `case_management`, `privileged_chat`, `ethics`.
  2. Wire agents + knowledge store with proper error handling, auth, and logging.
  3. Provide async/job handling via Celery/RQ (documented) or synchronous fallback with streaming responses.
  4. Implement middleware for API keys, rate limiting, audit trails.
- Frontend
  1. Implement dashboard shell, navigation, and layout.
  2. Create feature pages: Research workspace, Document analyzer with upload, Case board with status columns, Privileged chat UI, Ethics dashboard.
  3. Connect to backend using typed clients; handle loading/error states.
  4. Add file upload + result viewers (PDF preview, highlight matches).
- Deployment & Ops
  1. Author Dockerfiles and compose stack.
  2. Provide `Makefile` or npm scripts for dev/prod.
  3. Document environment variables, secrets management, and sample `.env`.
  4. Create `USAGE.md` update with install + verify steps.

### 3.5 Phase 4 – Sync & Validation
- Update README to reflect actual capabilities (no aspirational claims without implementation).
- Capture ADR summarizing architecture decisions and stored in `docs/03-technical/` per repo protocol.
- Generate installation logs + screenshots for blueprint catalog.
- Run lint/test/coverage, document outputs in PR template.

---

## 4. API Surface (Draft)

| Endpoint | Method | Purpose | Notes |
| :-- | :-- | :-- | :-- |
| `/api/research/query` | POST | Run natural-language legal query, return cited research packets | Accepts question + jurisdiction + filters; streams results |
| `/api/analyze-document` | POST | Upload document, run risk + clause extraction | Supports PDF/docx; returns structured findings + highlights |
| `/api/cases` | GET/POST/PUT | Manage legal cases, strategy summaries, task lists | CRUD with role-based access |
| `/api/privileged-chat` | POST | Secure attorney-client conversation with privilege logging | Requires session token + encryption |
| `/api/ethics/audit` | GET | Run ethics compliance audit on recent interactions | Summaries + actionable steps |
| `/api/health` | GET | System health status for monitoring | Reuse baseline from healthcare blueprint |

Detailed contract to be captured in `specification/api-contracts.yaml` (Phase 1 deliverable).

---

## 5. Dependencies & Environment

- Python 3.11+, Node.js 20+.
- Backend dependencies (initial list): `Flask`, `Flask-CORS`, `Flask-RESTful`, `pydantic`, `SQLAlchemy`, `alembic`, `python-dotenv`, `langchain`, `chromadb`, `openai`, `tiktoken`, `redis`, `celery`, `pillow`, `pdfminer.six`, `python-docx`.
- Frontend dependencies: `react`, `typescript`, `vite`, `react-router`, `@tanstack/react-query`, `axios`, `tailwindcss`, `radix-ui`, `zod`, `react-hook-form`, `recharts`.
- Tooling/test: `pytest`, `pytest-cov`, `httpx`, `pytest-asyncio` (if async), `pytest-mock`, `faker`, `vitest`, `@testing-library/react`, `msw`.
- Environment variables to define: OpenAI/Gemini API keys, Chroma path, encryption secrets, Redis URL, database urls, compliance toggles.

---

## 6. Testing Strategy

| Layer | Tests | Tools |
| :-- | :-- | :-- |
| Backend unit | Agent orchestrator outputs, data mappers, ethics engine | `pytest`, fixtures, golden files |
| Backend integration | REST endpoints with sqlite + chroma fixtures, permission checks | `pytest`, `httpx`, local DB seeds |
| Frontend unit | Component render, input validation, error states | `vitest`, `testing-library/react` |
| Frontend integration | API hooks + state management | `msw`, `react-query` tests |
| E2E | Research → document analysis → case update → privileged chat | `playwright` (headless) |
| Security | Privilege enforcement, logging, rate limits | targeted pytest suites |

Coverage target ≥90%; document coverage report under `quality/coverage.md`.

---

## 7. Documentation & Recipes

- `specification/api-contracts.yaml` – OpenAPI contracts (Phase 1).
- `specification/technical-architecture.md` – context, diagrams, data flow.
- `specification/ui-flows.md` – annotated screen flows.
- `documentation/setup-guide.md` – environment, install commands, verification tests.
- `documentation/runbook.md` – operating procedures, troubleshooting.
- `recipes/install.yaml` – blueprint installer recipe referencing backend/fronted/deployment steps.

---

## 8. Risks & Open Questions

1. **Agent Latency**: Running multi-agent workflows may exceed HTTP timeouts. Decision: adopt async job queue or chunked streaming? (Requires architecture answer.)
2. **Sensitive Data Handling**: Need encryption-at-rest for privileged chat transcripts. Determine whether to bundle Vault/KMS or document integration.
3. **LLM Provider Variability**: Provide provider-agnostic abstraction? Minimum requirement is OpenAI; consider Azure/Anthropic toggles.
4. **Document Processing Limits**: Confirm maximum file size for PDF/DOCX and fallback for unsupported formats.
5. **Dev Experience**: Should blueprint bundle mock LLM responses for offline use? (Impacts test fixtures.)

---

## 9. Next Steps

1. Socialize this spec with blueprint owners for sign-off.
2. Fill missing Phase 0 artifacts (API contract, architecture, UI flow docs).
3. Kick off architecture sprint per backlog and assign owners.
4. Track progress against blueprint checklist in `quality/status.md` once implementation starts.

