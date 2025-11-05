# Blueprint Portfolio Snapshot

Single source of truth for quick-win template sizing and follow-up actions. Updated after each ingestion or cleanup pass.

## Size & Complexity Overview

| Blueprint | Stack | Files | Tokens (≈) | Complexity | Notes |
|-----------|-------|-------|------------|------------|-------|
| go-clean-template | Go | 60 | 9.9K | Moderate | Ideal reference for lean service blueprints. |
| practica-clean-architecture | Node.js / TS | 123 | 23K | Complex | Keep full version for enterprise patterns; extract lean Express variants. |
| fastapi-fullstack-official | Python / TS | 154 | 26K | Complex | Trimmed frontend/scripts; use backend slice for future Python starters. |
| fastapi-rag-starter | FastAPI | 58 | 8.5K | Moderate | Production-ready RAG backend; 12–15 min setup. |
| jason-taylor-clean-architecture | C# | 252 | 41K | Complex | Remove generated API clients before catalog publish. |
| jhipster-sample | Java / Spring | 498 | 87K | Complex | Reference only—mine for patterns, don’t ship whole app. |

_Total footprint across tracked blueprints: ~196K tokens._

## Key Recommendations

1. **FastAPI & Python** – Adopt `fastapi-rag-starter` as the primary Python blueprint. Meets token/time targets; ship with living spec + env guide.
2. **Node.js / Practica** – Retain Practica as enterprise baseline but spin a lean `express-api-starter` (≤8K tokens) for gateway apps.
3. **Go** – Promote `go-clean-template` unchanged; use as benchmark for future clean-architecture ports.
4. **C# / Java** – Strip jason-taylor & JHipster templates down to server essentials before onboarding. Target ≤25K tokens.
5. **Metadata Discipline** – For every template captured above, ensure `setupTime`, `tokenSavings`, `provides`, `compatibleWith`, and `incompatibleWith` fields exist prior to catalog ingestion.

## FastAPI RAG Blueprint Highlights

- **Features:** JWT auth, PostgreSQL + SQLModel, ChromaDB vector store, OpenAI-powered RAG endpoints, streaming responses, optional Streamlit UI.
- **Setup:** Copy `.env.example`, run Alembic migrations, start FastAPI (`fastapi dev app/main.py`), optional `streamlit run app.py` for UI.
- **RAG API:**
  ```
  POST /api/v1/rag/upload      # upload documents
  POST /api/v1/rag/query       # semantic query
  POST /api/v1/rag/query/stream# streaming answers
  DELETE /api/v1/rag/reset     # clear vector store
  ```
- **Dependencies:** `chromadb`, `openai`, `langchain`, `tiktoken`, `pypdf` layered on the official FastAPI stack.

## Next Actions

- [ ] Run `analyze_blueprints.py` after each template trim to keep table up to date.
- [ ] Document compatibility metadata for the Node.js and FastAPI stacks in LanceDB schema.
- [ ] Prepare lean Spring Boot and .NET variants (≤25K tokens) before catalog publish.
