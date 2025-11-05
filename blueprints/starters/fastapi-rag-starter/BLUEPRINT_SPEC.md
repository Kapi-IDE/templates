# FastAPI RAG Starter - Blueprint Specification

**Blueprint ID:** `fastapi-rag-starter`
**Version:** 1.0.0
**Status:** Production Ready
**Category:** AI/ML, Backend API
**Priority:** P1 (Python MVP Blueprint)

---

## Overview

Production-ready FastAPI backend with RAG (Retrieval-Augmented Generation) capabilities for document Q&A applications. Built on the official FastAPI full-stack template with ChromaDB vector storage and OpenAI integration.

### Value Proposition

- **Token Savings:** 70% vs building from scratch (~25K saved tokens)
- **Setup Time:** 12-15 minutes from zero to deployed
- **Production Ready:** Battle-tested patterns, security, testing included
- **AI-First:** Optimized for RAG workloads and LLM applications

---

## Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Total Files** | 58 | <100 | ✅ |
| **Code Lines** | 3,190 | <5K | ✅ |
| **Total Tokens** | ~8,519 | 8K-15K | ✅ |
| **Size (MB)** | 0.09 | <0.5 | ✅ |
| **Complexity** | Moderate | Moderate | ✅ |
| **Setup Time** | 12-15 min | <20 min | ✅ |

---

## Technology Stack

### Core Framework
- **FastAPI** 0.114+ - Modern async web framework
- **Python** 3.10+ - Type hints, async/await
- **Uvicorn** - ASGI server
- **Pydantic** 2.0+ - Data validation

### Database & Storage
- **PostgreSQL** 14+ - Relational database
- **SQLModel** - ORM with type hints
- **Alembic** - Database migrations
- **ChromaDB** 0.5+ - Vector database for embeddings

### AI/ML
- **OpenAI** 1.0+ - GPT-4/GPT-3.5 integration
- **LangChain** 0.2+ - LLM orchestration
- **tiktoken** - Token counting
- **pypdf** 4.0+ - PDF text extraction

### Security & Auth
- **JWT** - Token-based authentication
- **Passlib + bcrypt** - Password hashing
- **CORS** - Cross-origin configuration

### Development
- **pytest** - Testing framework
- **mypy** - Static type checking
- **ruff** - Linting and formatting
- **Docker** - Containerization

---

## Features

### Authentication & User Management ✅
- JWT-based authentication
- User registration and login
- Password reset via email
- Role-based access control (admin/user)
- Secure password hashing

### RAG Capabilities ✅
- **Document Upload** - PDF and TXT files
- **Document Processing** - Chunking with overlap
- **Vector Storage** - ChromaDB with cosine similarity
- **Semantic Search** - Context retrieval
- **Answer Generation** - OpenAI GPT integration
- **Streaming Responses** - Real-time answer chunks
- **Source Citations** - Track answer sources

### Database & CRUD ✅
- PostgreSQL with SQLModel ORM
- Alembic migrations
- Generic CRUD operations
- Transaction management
- Connection pooling

### Development & Testing ✅
- Comprehensive test suite
- Type checking with mypy
- Code formatting with ruff
- Docker Compose for local dev
- Hot reload in development

---

## Architecture

### Directory Structure

```
fastapi-rag-starter/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── rag.py          # RAG endpoints (upload, query, stream)
│   │   │   ├── users.py        # User management
│   │   │   ├── items.py        # Example CRUD
│   │   │   └── login.py        # Authentication
│   │   ├── deps.py             # Dependency injection
│   │   └── main.py             # API router
│   ├── core/
│   │   ├── config.py           # Settings (env vars)
│   │   ├── db.py               # Database connection
│   │   └── security.py         # Auth utilities
│   ├── rag/
│   │   ├── vector_store.py     # ChromaDB interface
│   │   ├── document_processor.py # PDF/TXT processing
│   │   └── query_engine.py     # RAG query logic
│   ├── models.py               # SQLModel models
│   ├── crud.py                 # Database operations
│   └── main.py                 # FastAPI app
├── tests/                      # Pytest tests
├── alembic/                    # Database migrations
├── scripts/                    # Utility scripts
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

### API Endpoints

#### Authentication
- `POST /api/v1/login/access-token` - Login
- `POST /api/v1/login/test-token` - Test token
- `POST /api/v1/password-recovery` - Request password reset
- `POST /api/v1/reset-password` - Reset password

#### Users
- `GET /api/v1/users/me` - Get current user
- `PATCH /api/v1/users/me` - Update current user
- `POST /api/v1/users/signup` - Register new user
- `GET /api/v1/users/` - List users (admin)
- `POST /api/v1/users/` - Create user (admin)

#### RAG (Core Feature)
- `POST /api/v1/rag/upload` - Upload document (PDF/TXT)
- `POST /api/v1/rag/query` - Query documents
- `POST /api/v1/rag/query/stream` - Stream query response
- `DELETE /api/v1/rag/reset` - Reset vector store (admin)

#### Items (Example CRUD)
- `GET /api/v1/items/` - List items
- `POST /api/v1/items/` - Create item
- `GET /api/v1/items/{id}` - Get item
- `PUT /api/v1/items/{id}` - Update item
- `DELETE /api/v1/items/{id}` - Delete item

---

## Configuration

### Environment Variables

#### Required
```bash
# Database
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changethis
POSTGRES_DB=app

# OpenAI
OPENAI_API_KEY=sk-your-api-key

# First Admin User
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=changethis

# Security
SECRET_KEY=changethis  # Generate: openssl rand -hex 32
```

#### Optional
```bash
# OpenAI
OPENAI_MODEL=gpt-4o-mini  # or gpt-4, gpt-3.5-turbo

# ChromaDB
CHROMA_PERSIST_DIR=./chroma_data
CHROMA_COLLECTION_NAME=documents

# Email (for password reset)
SMTP_HOST=
SMTP_USER=
SMTP_PASSWORD=
EMAILS_FROM_EMAIL=
SMTP_TLS=True
SMTP_PORT=587

# Monitoring
SENTRY_DSN=

# CORS
BACKEND_CORS_ORIGINS=http://localhost,http://localhost:3000

# Environment
ENVIRONMENT=local  # or staging, production
```

---

## Deployment

### Quick Start (5 steps)

1. **Clone and setup**
   ```bash
   git clone <blueprint-url> my-rag-app
   cd my-rag-app
   cp .env.example .env
   # Edit .env with your values
   ```

2. **Install dependencies**
   ```bash
   uv pip install -e .
   ```

3. **Run migrations**
   ```bash
   alembic upgrade head
   python -m app.initial_data
   ```

4. **Start server**
   ```bash
   fastapi dev app/main.py
   ```

5. **Test RAG**
   - Go to http://localhost:8000/docs
   - Login with FIRST_SUPERUSER credentials
   - Upload a document via `/api/v1/rag/upload`
   - Query it via `/api/v1/rag/query`

### Docker Deployment

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f backend

# Services available:
# - API: http://localhost:8000
# - PostgreSQL: localhost:5432
# - Adminer: http://localhost:8080
```

### Production Deployment

1. **Security**
   - Change all default passwords
   - Set `ENVIRONMENT=production`
   - Use strong `SECRET_KEY`
   - Configure HTTPS/TLS

2. **Database**
   - Use managed PostgreSQL (AWS RDS, etc.)
   - Set up backups
   - Configure connection pooling

3. **Scaling**
   - Use Gunicorn with Uvicorn workers
   - Deploy behind reverse proxy (Nginx)
   - Consider Redis for caching
   - Scale ChromaDB separately if needed

4. **Monitoring**
   - Configure Sentry for error tracking
   - Set up application metrics
   - Monitor API performance
   - Track RAG accuracy

---

## Testing

### Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test
pytest tests/api/routes/test_rag.py

# Type checking
mypy app

# Linting
ruff check app
```

### Test Coverage

Target: 80%+ coverage

Key test areas:
- ✅ Authentication flows
- ✅ User CRUD operations
- ✅ RAG upload and query
- ✅ Vector store operations
- ✅ Document processing
- ✅ API error handling

---

## Customization

### Level 1: Configuration (5 minutes)
Change environment variables:
- Project name
- OpenAI model
- Chunk sizes
- Collection names

### Level 2: Features (30-60 minutes)
Add/modify:
- New API endpoints
- Custom document types
- Different embedding models
- Additional vector stores

### Level 3: Architecture (2-4 hours)
Major changes:
- Switch to different LLM provider
- Add multi-tenancy
- Implement caching layer
- Add async job processing

---

## Compatibility

### Compatible With
- PostgreSQL 14+
- OpenAI API
- ChromaDB
- Docker 20+
- Python 3.10+

### Incompatible With
- SQLite (for production)
- Python <3.10
- Windows without WSL (ChromaDB issues)

### Provides
- REST API endpoints
- JWT authentication
- RAG capabilities
- Vector search
- Document processing
- User management

---

## Metadata

```yaml
blueprint_id: fastapi-rag-starter
version: 1.0.0
category: ["ai-ml", "backend", "rag"]
stack: ["python", "fastapi", "postgresql", "chromadb", "openai"]
setup_time_minutes: 12-15
token_count: 8519
token_savings_percent: 70
complexity: moderate
production_ready: true
includes_tests: true
includes_auth: true
includes_docker: true

provides:
  - rag_capabilities
  - jwt_authentication
  - user_management
  - vector_search
  - document_processing
  - rest_api

compatible_with:
  - postgresql
  - docker
  - openai
  - chromadb

incompatible_with:
  - sqlite_production
  - python_3.9

voice_patterns:
  - "FastAPI RAG"
  - "document Q&A"
  - "RAG application"
  - "PDF question answering"
  - "semantic search"
  - "vector database"
  - "ChromaDB FastAPI"
  - "OpenAI FastAPI"
```

---

## Success Criteria

### Deployment Success
- ✅ API starts on http://localhost:8000
- ✅ Database migrations complete
- ✅ First superuser created
- ✅ Interactive docs accessible (/docs)
- ✅ Can upload and query documents

### Quality Metrics
- ✅ All tests pass
- ✅ Type checking passes (mypy)
- ✅ Linting passes (ruff)
- ✅ 80%+ test coverage
- ✅ No security vulnerabilities

### Performance
- ✅ API response <200ms (non-LLM endpoints)
- ✅ Document upload <5s (10MB PDF)
- ✅ RAG query <3s (with OpenAI)
- ✅ Vector search <100ms

---

## Known Limitations

1. **ChromaDB**
   - In-memory mode not suitable for production
   - Requires persistent storage
   - Windows support limited (use WSL)

2. **OpenAI**
   - Requires API key (costs money)
   - Rate limits apply
   - Network latency affects response time

3. **Document Processing**
   - PDF extraction may be imperfect
   - Complex layouts not fully supported
   - Only PDF and TXT supported (MVP)

4. **Scalability**
   - ChromaDB not designed for massive scale
   - Consider Pinecone/Weaviate for >1M vectors
   - Single instance limits apply

---

## Future Enhancements

### Short-term (Next Version)
- [ ] Support for DOCX, PPTX files
- [ ] Conversation history for RAG
- [ ] Multiple OpenAI model support
- [ ] Batch document upload
- [ ] RAG accuracy metrics

### Long-term (Future Versions)
- [ ] Multi-tenant support
- [ ] Alternative embedding models (local)
- [ ] Hybrid search (keyword + semantic)
- [ ] Document versioning
- [ ] Advanced citation tracking
- [ ] GraphRAG capabilities

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [LangChain Documentation](https://python.langchain.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)

---

## Changelog

### v1.0.0 (2025-10-01)
- Initial release
- Core RAG functionality
- JWT authentication
- PostgreSQL + SQLModel
- ChromaDB integration
- OpenAI GPT integration
- Streaming responses
- PDF/TXT support
- Docker deployment
- Comprehensive tests

---

**Blueprint Status:** ✅ Production Ready
**Recommended for:** AI/ML workloads, document Q&A, semantic search, RAG applications
**Token Efficiency:** 70% savings vs scratch (8.5K tokens vs 25K+ baseline)
