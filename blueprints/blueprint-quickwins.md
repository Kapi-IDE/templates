# Blueprint Quick Wins Catalog

**28 production-ready applications for KAPI students** - Node.js/TypeScript focused, 8-45 min setup

_Last updated: October 2025_

---

## Overview

This catalog prioritizes **immediate value** for mid-senior enterprise developers learning AI-assisted development. Each app demonstrates KAPI's backwards build methodology while solving real problems.

**Organization:**
1. **Gateway Apps** (3) - <15 min, instant gratification
2. **Core Applications** (20) - 15-40 min, enterprise use cases
3. **AI Class Specials** (5) - 35-45 min, ML/AI training projects

---

## Gateway Apps (Hook Students Fast)

**Goal: First win in <15 minutes**

| # | App | Stack | Time | LOC | Key Value |
|---|-----|-------|------|-----|-----------|
| 1 | **URL Shortener** | Express + Redis + Analytics | 10 min | 1.2K | Custom slugs, click tracking, QR codes, expiration |
| 2 | **Meme Generator** | Next.js + Cloudinary | 8 min | 1K | Templates, text overlay, instant share, viral potential |
| 3 | **Markdown Blog** | Next.js + MDX | 12 min | 1.5K | Write & publish immediately, syntax highlighting, RSS |

**Why these work:**
- Under 15 minutes from zero to deployed
- Shareable output (students show friends/colleagues)
- Simple enough to understand the full stack
- Foundation for learning composition

---

## Core Applications (Enterprise Use Cases)

**Goal: Solve real problems, demonstrate methodology**

### AI & Search (5 apps)

| # | App | Stack | Time | LOC | Key Value |
|---|-----|-------|------|-----|-----------|
| 4 | **AI Chat Interface** | Next.js + OpenAI + Prisma | 15 min | 2K | Streaming responses, conversation history, share links |
| 5 | **RAG Document Q&A** | Express + ChromaDB + OpenAI | 25 min | 2.5K | PDF upload, semantic search, cited answers |
| 6 | **Perplexity Clone** | Next.js + OpenAI + Brave Search | 20 min | 2.1K | Multi-source search, cited answers, follow-up questions |
| 7 | **SQL Query Builder** | Next.js + Monaco Editor + OpenAI | 22 min | 2K | Natural language to SQL, query validation, visualization |
| 8 | **E-commerce with Hybrid RAG** | Next.js + PostgreSQL + Pinecone + Stripe | 40 min | 3.5K | SQL inventory + vector search, semantic discovery, recommendations |

### Productivity & Tools (7 apps)

| # | App | Stack | Time | LOC | Key Value |
|---|-----|-------|------|-----|-----------|
| 9 | **Meeting Transcriber** | React + Whisper API + Prisma | 20 min | 2.2K | Audio upload, transcription, action items extraction |
| 10 | **Code Review Bot** | Express + GitHub API + OpenAI | 18 min | 1.8K | PR analysis, standards checking, auto-comments |
| 11 | **Email Classifier** | Fastify + Gmail API + OpenAI | 15 min | 1.5K | Auto-categorize, priority scoring, suggested responses |
| 12 | **API Documentation Generator** | Next.js + MDX + OpenAPI | 18 min | 1.7K | Auto-generate from code, interactive examples, search |
| 13 | **Expense Tracker** | Next.js + Prisma + Recharts | 20 min | 2.3K | Receipt OCR, categorization, budget alerts, reports |
| 14 | **Habit Tracker** | Next.js + Prisma + Charts | 18 min | 2K | Streaks, reminders, goal setting, progress visualization |
| 15 | **Team Wiki** | Next.js + Markdown + Search | 22 min | 2.5K | WYSIWYG editor, version history, permissions, search |

### Business & Enterprise (5 apps)

| # | App | Stack | Time | LOC | Key Value |
|---|-----|-------|------|-----|-----------|
| 16 | **Simple CRM** | Next.js + Prisma + Stripe | 35 min | 3K | Contacts, deals, pipeline, invoicing |
| 17 | **Job Board** | Next.js + Prisma + Stripe | 30 min | 2.8K | Listings, applications, employer dashboard, payments |
| 18 | **Landing Page Builder** | Next.js + Tailwind + Forms | 12 min | 1.5K | Drag-drop sections, A/B testing, analytics integration |
| 19 | **Enterprise Analytics Dashboard** | Next.js + Prisma + Recharts + PostgreSQL | 35 min | 3.2K | Real-time KPIs, drill-down reports, role-based access, export |
| 20 | **Customer Feedback Analyzer** | React + Prisma + OpenAI | 25 min | 2.4K | Sentiment analysis, theme extraction, priority ranking |

### Games (2 apps)

| # | App | Stack | Time | LOC | Key Value |
|---|-----|-------|------|-----|-----------|
| 21 | **Three.js Racing Game** | React Three Fiber + Cannon.js | 30 min | 2.5K | Physics-based racing, multiplayer-ready, mobile controls |
| 22 | **Three.js Puzzle Game** | React + Three.js + Zustand | 25 min | 2K | 3D Tetris/2048 hybrid, particle effects, leaderboard |

---

## AI Class Specials (Advanced ML Projects)

**Goal: Teach AI/ML fundamentals with production-quality code**

| # | App | Stack | Time | LOC | Key Value |
|---|-----|-------|------|-----|-----------|
| 23 | **Cancer Detection Trainer** | Python + FastAPI + TensorFlow | 45 min | 3.5K | Histopathology dataset, transfer learning, accuracy dashboard |
| 24 | **NFL Play Predictor** | Python + Pandas + Scikit-learn | 40 min | 3K | NFL tracking data, feature engineering, prediction API |
| 25 | **Fine-tuning Dashboard** | Next.js + OpenAI + Prisma | 35 min | 2.8K | Dataset upload, training jobs, eval metrics, A/B testing |
| 26 | **Prompt Engineering Lab** | React + OpenAI + MongoDB | 22 min | 2.2K | Version control prompts, temperature testing, cost tracking |
| 27 | **Multi-Agent Workflow** | Express + LangChain + Redis | 40 min | 3.2K | Agent orchestration, tool calling, conversation handoffs |
| 28 | **ReAct Stock Trading Agent** | Express + OpenAI + Alpha Vantage | 30 min | 2.8K | Reasoning loop, technical analysis, paper trading, backtesting |

**Note:** #23-24 use Python because ML training requires it. All others are Node.js/TypeScript.

---

## Recipe & Template Library

**Essential scaffolding for backwards build methodology**

### Documentation Templates

| Template | Type | Purpose | Location |
|----------|------|---------|----------|
| **Slidedeck (Reveal.js)** | Component | Modern presentations with dark theme | `components/documentation/` |
| **API Documentation** | Template | OpenAPI + interactive examples | `recipes/docs/` |
| **Technical RFCs** | Template | Decision records with trade-offs | `recipes/docs/` |
| **Architecture Decision Records** | Template | ADR format with context/options/decision | `recipes/docs/` |
| **Incident Post-mortems** | Template | 5-whys, timeline, action items | `recipes/docs/` |

### Development Templates

| Template | Type | Purpose | Location |
|----------|------|---------|----------|
| **User Story Template** | Spec | Given/When/Then format | `recipes/specs/` |
| **Backwards Build Spec** | Spec | Full spec → arch → test → code flow | `recipes/specs/` |
| **Test Plan Template** | Testing | Unit/integration/e2e coverage | `recipes/testing/` |
| **Code Review Checklist** | Process | Standards, security, performance | `recipes/process/` |
| **PR Description Template** | Process | Context, changes, testing, screenshots | `recipes/process/` |

### React Component Recipes

| Recipe | Type | Purpose | Location |
|--------|------|---------|----------|
| **Dashboard Layouts** | UI | Sidebar, topnav, card grid patterns | `recipes/react/layouts/` |
| **Data Tables** | UI | Filters, sort, pagination, export | `recipes/react/tables/` |
| **Multi-step Forms** | UI | Validation, progress, save/resume | `recipes/react/forms/` |
| **File Upload** | UI | Drag-drop, preview, progress, S3 | `recipes/react/upload/` |
| **Chart Integrations** | UI | Recharts, Chart.js patterns | `recipes/react/charts/` |
| **Auth Flows** | UI | Login, signup, reset, social | `recipes/react/auth/` |

### AI-Specific Recipes

| Recipe | Type | Purpose | Location |
|--------|------|---------|----------|
| **Streaming UI Patterns** | Component | SSE, WebSocket, React hooks | `recipes/ai/streaming/` |
| **Token Counting** | Utility | Cost estimation, limit enforcement | `recipes/ai/tokens/` |
| **Retry Logic** | Utility | Exponential backoff, circuit breaker | `recipes/ai/resilience/` |
| **Cost Tracking** | Middleware | Log tokens, estimate costs, alerts | `recipes/ai/observability/` |
| **RAG Pipeline Patterns** | Architecture | Chunking, embedding, retrieval | `recipes/ai/rag/` |
| **Agent Tool Calling** | Pattern | Function calling, validation, error handling | `recipes/ai/agents/` |

---

## Build Priority (Implementation Order)

### Phase 1: Gateway Apps (Week 1)
**Goal:** Prove instant value

1. URL Shortener (10 min)
2. Meme Generator (8 min)
3. Markdown Blog (12 min)

**Deliverable:** Students get first win in <15 min

### Phase 2: Core AI Apps (Week 2-3)
**Goal:** Demonstrate AI methodology

4. AI Chat Interface (15 min)
5. RAG Document Q&A (25 min)
6. Perplexity Clone (20 min)

**Deliverable:** Complete AI app portfolio

### Phase 3: Enterprise Tools (Week 4-5)
**Goal:** Real business value

7-15. Productivity & tools (18-25 min each)
16-20. Business apps (30-35 min each)

**Deliverable:** Students can build internal tools

### Phase 4: Advanced AI (Week 6-7)
**Goal:** ML fundamentals

23-28. AI class specials (22-45 min)

**Deliverable:** Students understand training, agents, fine-tuning

### Phase 5: Games & Misc (Week 8)
**Goal:** Fun, engagement

21-22. Three.js games (25-30 min)

**Deliverable:** Students can build interactive experiences

### Cross-Stack Expansion Roadmap

| Priority | Stack | Blueprint Template | Why It Matters |
|----------|-------|--------------------|----------------|
| P0 (MVP) | Node.js / TypeScript | Practica clean architecture starter | Aligns with current quick-win apps and our TypeScript-first catalog. |
| P1 | Go | `evrone/go-clean-template` | Minimal friction to adapt, enforces clean architecture, popular for infra teams. |
| P1 | Python | FastAPI best-practices stack | Fastest-growing backend for AI workloads; mirrors our RAG/LLM blueprints. |
| P2 | Java | JHipster | Enterprise-grade scaffolding with Spring, aligns with regulated orgs. |
| P2 | C# | Jason Taylor CleanArchitecture | Widely adopted in .NET shops, clean architecture story matches blueprint philosophy. |

**Implementation Notes:**
- Capture the same metadata (`setupTime`, `tokenSavings`, `provides`, `compatibleWith`, `incompatibleWith`) when onboarding each template so they drop into the LanceDB registry without rework.
- Ship living specs, install scripts, and env guides alongside each new stack to preserve Backwards Build discipline.
- Sequence delivery right after Gateway/Core apps so future sprints can focus on composability without revisiting boilerplate.

---

## Recipe Build Priority

**Build recipes alongside apps, not after**

### Week 1-2: Essential Specs
- User story template
- Backwards build spec template
- Test plan template

### Week 3-4: React Components
- Dashboard layouts
- Data tables
- Multi-step forms
- Auth flows

### Week 5-6: AI Recipes
- Streaming UI patterns
- RAG pipeline patterns
- Token counting utilities
- Cost tracking middleware

### Week 7-8: Documentation
- API documentation template
- ADR template
- RFC template

---

## Success Metrics

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| **Time to First Deploy** | <15 min | Proves instant value |
| **Student Completion Rate** | >85% | Apps are achievable |
| **Code Quality Score** | >90/100 | Methodology works |
| **Token Savings vs Scratch** | 60-80% | Blueprint efficiency |
| **Student NPS** | >50 | Would recommend to peers |

---

## Foundation: Practica as Blueprint Baseline

**Repository:** https://github.com/practicajs/practica

**Why Practica is our foundation:**
- Production-ready Node.js/TypeScript starter (not just documentation)
- Implements industry best practices from https://github.com/goldbergyoni/nodebestpractices
- Microservices architecture with real patterns (~5K LOC)
- Modern stack: Express, PostgreSQL, Docker, OpenTelemetry
- Has testing, monitoring, error handling built-in
- Perfect size for KAPI blueprint templates

**How we use it:**

### 1. Fork as Flagship Blueprint
**Enterprise Node.js API** (Blueprint #0)
- Use Practica as-is for enterprise backend starting point
- 45 min setup time
- Demonstrates all KAPI best practices
- Reference implementation for other blueprints

### 2. Extract Core Components
Break Practica into reusable pieces:
- **Error Handling Middleware** - Structured error responses
- **Logging Setup** - Pino with correlation IDs
- **Testing Patterns** - Jest + Supertest integration
- **Docker Configs** - Multi-stage builds, health checks
- **OpenTelemetry Monitoring** - Distributed tracing
- **Security Middleware** - Helmet, rate limiting, input validation

### 3. Create Lean Variants
Build our 28 blueprints using Practica's patterns:
- **Healthcare Patient Triage** = Practica + HIPAA compliance layer
- **Simple CRM** = Practica - microservices complexity + business logic
- **RAG Document Q&A** = Practica + ChromaDB + OpenAI integration
- **Job Board** = Practica patterns + application-specific features

### 4. Quality Baseline
Every blueprint must meet Practica/nodebestpractices standards:
- **Error Handling** - Async/await error catching (BP 1.4)
- **Security** - Helmet, secrets management (BP 6.1, 6.10)
- **Testing** - 80%+ coverage (BP 4.x)
- **Structure** - Component-based architecture (BP 5.1)
- **Docker** - Production-ready containers (BP 7.x)
- **Monitoring** - Observability from day one (BP 3.x)

### 5. Validation Integration
KAPI's brutal analysis checks against these standards:
```
❌ No helmet middleware (Security 6.10)
❌ Secrets in code, not .env (Security 6.1)
❌ Async errors not caught (Error 1.4)
✅ Component structure follows BP 5.1
✅ 85% test coverage (Testing 4.2)
```

**Result:** Students deploy apps that already follow industry best practices. They learn quality by building with it, not reading documentation.

---

## Reference Repositories (Pattern Extraction)

**Study these for specific patterns - don't fork directly**

- Chatbot patterns: https://github.com/onyx-dot-app/onyx
- Customer service flows: https://github.com/chatwoot/chatwoot
- Text-to-SQL: https://github.com/vanna-ai/vanna-streamlit
- BI dashboards: https://github.com/lightdash/lightdash
- Analytics: https://github.com/metabase/metabase
- CRM patterns: https://github.com/twentyhq/twenty
- Project management: https://github.com/makeplane/plane
- Agent orchestration: https://github.com/activepieces/activepieces

**Usage:** Extract specific UI/UX patterns and architectural decisions. Rebuild as lean components that integrate with Practica foundation.

---

## Next Steps

1. **Build Phase 1** (Gateway Apps) - validate instant value hypothesis
2. **Create essential recipes** - students need specs/templates to apply methodology
3. **Test with beta students** - iterate based on real feedback
4. **Document composition patterns** - show how apps decompose into reusable components
5. **Scale to full catalog** - complete all 28 apps + recipe library

**Goal:** Students should never feel stuck. Every common pattern has a recipe. Every business problem has a starting app.
