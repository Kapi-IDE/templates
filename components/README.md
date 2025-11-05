# Components Catalogue

Modular building blocks you can compose into new blueprints or quick wins. Every component ships with implementation code, documentation, and metadata. The canonical index lives in [`registry.yaml`](./registry.yaml).

## Backend
- `backend/agent-base` – Python agent foundation with prompt scaffolding, structured extraction, urgency assessment, and health checks.
- `backend/agent_framework` – Domain-agnostic Python framework for multi-agent systems with logging and audit tooling.
- `backend/ai-integrations/{gemini,azure-openai,anthropic-bedrock}` – Production-ready clients for the major LLM providers.
- `backend/authentication/{jwt-express,jwt-fastify,jwt-node}` – JWT verification middleware/plugins for Express, Fastify, and a full Node auth stack.
- `backend/caching/redis` – Redis client + session manager helpers with distributed locking.
- `backend/database/postgresql-prisma` – Prisma + PostgreSQL starter with migrations and type-safe queries.
- `backend/llm-wrapper` – Gemini client wrapper for Python agents.
- `backend/logging` – Agent interaction logger helpers.
- `backend/node-llm-framework` – Unified TypeScript services for Azure OpenAI, Gemini, Claude, and Nova.
- `backend/web-servers/{express-service,fastify-service}` – Hardened HTTP server skeletons with lifecycle helpers.
- `backend/task-queue` – Celery configuration factory with Redis defaults.

## Frontend
- `frontend/react-chat-ui` – Onyx-inspired React chat interface.
- `frontend/forms/react-hook-form-zod` – Form toolkit with Zod validation patterns.
- `frontend/streamlit-rag-ui` – Complete Streamlit RAG console.
- `frontend/streamlit-components/{auth-ui,chat-interface,dark-theme,file-uploader}` – Atomic Streamlit widgets.

## UI Kits
- `ui/3d-visualizations` – Three.js visualisations (Knowledge Galaxy, Digital Twin, etc.).
- `ui/react-dashboard-theme` *(coming soon)* – Converted Maxton dashboard theme.

## Data & Integrations
- `database/prisma-patterns` – Collection of ready-to-use Prisma schema patterns (auth, GraphQL, MongoDB).
- `payments/stripe` – Express payment-intent server with webhook verification and optional Stripe Tax.
- `auth/oidc-provider` – Express OIDC provider bootstrap using `oidc-provider`.
- `email/templates` – Email template renderer with HTML/Text conversion and CSS inlining.
- `testing/data-generation` – Deterministic fake data generator for repeatable test fixtures.

## DevOps & Docs
- `devops/docker/docker-compose-stack` – Compose templates for app + Postgres + Redis + Nginx.
- `documentation/reveal-presentation` – Reveal.js presentation template with theme extensions.

## Using Components
1. Browse `registry.yaml` or the directories above.
2. Copy the component into your project (`cp -r templates/components/backend/web-servers/express-service my-app/backend/web`).
3. Install the dependencies listed in the component README.
4. Follow any configuration notes (environment variables, integration keys, etc.).

> Tip: keep components as Git subtrees/submodules if you want to inherit upstream fixes.

## Maintaining the Registry
- Every component must ship a `metadata.yaml` describing `component_id`, `name`, `category`, and `version`.
- Run `python3 scripts/update_component_registry.py` *(coming soon)* or execute the inline command from the last update to refresh `registry.yaml` after adding metadata changes.
- Update this README when new component categories are introduced.
