# KAPI Templates Catalog

**Single source of truth for every reusable asset KAPI ships: components, production blueprints, starters, and process guides.**

_Last updated: October 2025_

---

## Directory Map

```
templates/
├── blueprints/            # Full applications (reference, industry, starters)
├── components/            # Reusable UI/backend/devops modules
├── quality-baselines/     # Language and stack best-practice checklists (MD)
└── recipes/               # Process + architecture playbooks (YAML/MD)
```

Use this decision table when adding something new:

| Content type                     | Destination                                      |
|----------------------------------|--------------------------------------------------|
| Single UI/Backend/DevOps module  | `components/{frontend|backend|devops}/`          |
| Complete app for quick launch    | `blueprints/starters/`                           |
| Third-party reference template   | `blueprints/reference/`                          |
| Production-ready KAPI solution   | `blueprints/industry/`                           |
| Quality checklist / guardrail    | `quality-baselines/`                             |
| Process or architecture recipe   | `recipes/` (absorbing former implementation + PM guides)

---

## Category Overviews

### 🧩 Components
Reusable modules with minimal setup (typically ≤10 minutes, ≤10k tokens). Every component includes:
- `metadata.yaml` (capabilities, compatibility, voice patterns)
- `README.md` with setup + examples
- Optional `example/` implementation

**Highlights**
- `frontend/react-chat-ui/` – Onyx-inspired multi-assistant chat
- `frontend/streamlit-components/` – Streamlit chat/upload/auth building blocks
- `backend/authentication/` – JWT + OAuth patterns
- `backend/database/` – PostgreSQL + Chroma foundations
- `devops/docker/` – Compose stacks for app + services

### 📘 Blueprints
Opinionated, end-to-end applications. Split by intent:
- `blueprints/reference/` – Practica, go-clean-template, FastAPI full-stack, etc.
- `blueprints/industry/` – Healthcare triage, legal analysis, finance dashboard, AI governance, team knowledge base
- `blueprints/starters/` – FastAPI RAG starter (more on the way)

Standard blueprint structure:
```
app-name/
├── backend/
├── frontend/
├── docker-compose.yml
├── .env.example
├── README.md
├── DEPLOYMENT.md (or similar)
└── metadata.yaml
```

### 🧭 Quality Baselines
Language and stack-specific best-practice guides. These Markdown checklists back analyzer-style tooling (Autofix, Drift Detection) and should stay atomic (`nodejs-best-practices-pattern.md`, `fastapi-best-practices.md`, etc.).

**Owner actions**
- Keep rules actionable with severity levels (P0/P1/P2)
- Reference upstream sources (e.g., nodebestpractices) for credibility
- Version changes in the filename or front matter when breaking

### 🛠️ Recipes
Process and architecture templates that teach how to execute work the KAPI way. This bucket consolidates the former `implementation-blueprints/` domains and `project-management/` playbooks under a single roof.

**Structure (in flight migration)**
- `recipes/strategic/` – Product vision, problem analysis, tech stack selection
- `recipes/system-design/` – API specs, architecture diagrams, workflow mapping
- `recipes/implementation/` – Testing strategy, AWS setup, monorepo guides
- `recipes/project-management/` – Living specs, roadmaps, collaboration protocols
- `recipes/cross-cutting/` – Security, performance, documentation frameworks

Every recipe should include audience, prerequisites, and Backwards Build phase alignment.

---

## Working Guidelines

- **Naming**: use kebab-case directories (`fastapi-rag-starter`). Keep names descriptive and tech-agnostic when possible.
- **Documentation**: never add code without a `README.md`; blueprints also need deployment notes and `.env.example`.
- **Metadata**: any deployable unit (component or blueprint) must expose `metadata.yaml` for LanceDB search with `provides`, `compatible_with`, `setup_time_minutes`, `token_count`, and `voice_patterns`.
- **Token + Time Budgets**:
  - Components: 3k–10k tokens, ≤10 min setup
  - Starters: 8k–15k tokens, 10–20 min setup
  - Industry blueprints: 15k–40k tokens, up to 45 min setup
  - Reference templates may exceed these but should be trimmed when possible

---

## Contribution Checklist

### Components
- [ ] Single responsibility (UI widget, auth module, etc.)
- [ ] `metadata.yaml` with voice patterns
- [ ] `README.md` (install, usage, compatibility)
- [ ] Example or tests when useful

### Blueprints
- [ ] Backend + frontend + infrastructure assets included
- [ ] Local dev ready (`docker-compose.yml`, `.env.example`)
- [ ] `README.md` (overview + quick start) and `DEPLOYMENT.md`
- [ ] `metadata.yaml` with setup time, token savings, provides/incompatibilities
- [ ] Optional: specs/tests if available

### Implementation & PM Docs
- [ ] Clear audience and objective
- [ ] Actionable steps or templates (YAML/MD)
- [ ] Linked from parent README if new

---

## Fast Navigation

| Need | Go to |
|------|-------|
| UI/backend pieces | `/components/` |
| Launch-ready app | `/blueprints/starters/` |
| Learn from exemplary repo | `/blueprints/reference/` |
| Industry solution | `/blueprints/industry/` |
| Process/architecture guidance | `/recipes/` |
| Best-practice guardrails | `/quality-baselines/` |

---

## Housekeeping

- Combined the previous `DIRECTORY_STRUCTURE.md` and legacy `README.old.md` into this concise README.
- Update this document whenever categories change.
- Questions? Ping the KAPI template maintainers in `#templates`.

**Stop vibe coding. Start engineering.**
