# FastAPI Best Practices Pattern
**KAPI Quality Baseline for All Python/FastAPI Blueprints**

_Comprehensive production-ready practices for FastAPI applications_

---

## Overview

This document defines the quality baseline that **every KAPI FastAPI blueprint must meet**. These practices ensure production-ready Python applications from day one.

**Purpose**: Ensure all KAPI-generated FastAPI code follows industry-standard best practices.

---

## 1. Project Structure (6 Practices)

### 1.1 Domain-Centric Organization
**Rule**: Structure by business domains, not technical layers.

```
src/
├── auth/
│   ├── router.py          # HTTP interface
│   ├── schemas.py         # Pydantic models
│   ├── models.py          # SQLModel/SQLAlchemy
│   ├── service.py         # Business logic
│   ├── dependencies.py    # FastAPI Depends
│   ├── constants.py       # Error codes
│   ├── config.py          # Domain settings
│   └── exceptions.py      # Domain errors
├── users/
├── orders/
├── database.py            # Connection factory
├── config.py              # Global settings
└── main.py                # App wiring
```

**Why**: Clear boundaries, easier scaling, reduced cognitive load.

**KAPI Validation**: `❌ Technical folders at root (controllers/, models/)`

---

### 1.2 Shared Infrastructure at Root
**Rule**: Database connectors, pagination, global exceptions at `src/` root.

**KAPI Validation**: `❌ Duplicate infrastructure code across domains`

---

### 1.3 Mirror Tests to Source
**Rule**: `tests/` structure matches `src/` domains.

```
tests/
├── auth/
│   ├── test_router.py
│   ├── test_service.py
├── users/
```

**KAPI Validation**: `❌ Flat test structure`

---

### 1.4 Environment-Aware Config
**Rule**: Use Pydantic `BaseSettings` with `.env` support.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**KAPI Validation**: `❌ No config validation on startup`

---

### 1.5 Dependency Management
**Rule**: Use Poetry or pip-tools. Lock all dependencies.

**KAPI Validation**: `❌ No poetry.lock or requirements.txt`

---

### 1.6 Type Hints Everywhere
**Rule**: All functions have complete type annotations. Use MyPy/Pyright.

**KAPI Validation**: `❌ Missing type hints`

---

## 2. Async Patterns (5 Practices)

### 2.1 Default to Async Routes
**Rule**: Use `async def` for all routes unless library forces sync.

```python
# ✅ Do
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User))
    return users.scalars().all()

# ❌ Avoid
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

**KAPI Validation**: `❌ Sync routes when async possible`

---

### 2.2 Offload Blocking Calls
**Rule**: Use `run_in_threadpool` for sync libraries.

```python
from fastapi.concurrency import run_in_threadpool

async def process_file(file: bytes):
    return await run_in_threadpool(legacy_sync_processor, file)
```

**KAPI Validation**: `⚠️ Blocking calls in async routes`

---

### 2.3 No CPU-Bound Work in Routes
**Rule**: Offload to Celery/RQ/separate service.

**KAPI Validation**: `❌ Heavy computation in request path`

---

### 2.4 Use Async Database Drivers
**Rule**: asyncpg (PostgreSQL), aiomysql (MySQL), motor (MongoDB).

**KAPI Validation**: `❌ Sync database drivers`

---

### 2.5 Proper Async Context Managers
**Rule**: Use `async with` for sessions, connections, files.

**KAPI Validation**: `❌ Missing async context managers`

---

## 3. Pydantic & Validation (8 Practices)

### 3.1 Model All Payloads
**Rule**: Every request/response uses Pydantic models.

```python
class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
```

**KAPI Validation**: `❌ Raw dict usage in routes`

---

### 3.2 Shared BaseModel
**Rule**: Extend common base for serialization rules.

```python
class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
```

**KAPI Validation**: `❌ Inconsistent model config`

---

### 3.3 Split Settings from Request Models
**Rule**: `BaseSettings` separate from `BaseModel`.

**KAPI Validation**: `❌ Settings mixed with schemas`

---

### 3.4 Use Field Validators
**Rule**: Pydantic validators for complex validation.

```python
from pydantic import field_validator

class User(BaseModel):
    email: str
    
    @field_validator('email')
    def validate_email(cls, v):
        if not v.endswith('@company.com'):
            raise ValueError('Must use company email')
        return v
```

**KAPI Validation**: `⚠️ Manual validation without Pydantic`

---

### 3.5 Explicit Serialization Modes
**Rule**: Use `model_dump(mode='json')` for JSON responses.

**KAPI Validation**: `⚠️ Implicit serialization`

---

### 3.6 Validation for Environment Variables
**Rule**: All env vars validated through Pydantic.

**KAPI Validation**: `❌ os.getenv without validation`

---

### 3.7 Use Constrained Types
**Rule**: `conint`, `constr`, `EmailStr`, etc. for constraints.

**KAPI Validation**: `⚠️ Basic types without constraints`

---

### 3.8 Reuse Models Across Layers
**Rule**: Avoid duplication between schemas and ORM models.

```python
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
```

**KAPI Validation**: `⚠️ Duplicate model definitions`

---

## 4. Error Handling (12 Practices)

### 4.1 Custom Exception Hierarchy
**Rule**: Domain-specific exceptions extending base classes.

```python
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code

class NotFoundError(AppException):
    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", 404)

class ValidationError(AppException):
    def __init__(self, message: str):
        super().__init__(message, 422)
```

**KAPI Validation**: `❌ Generic exceptions only`

---

### 4.2 Centralized Exception Handler
**Rule**: Single handler for all custom exceptions.

```python
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
```

**KAPI Validation**: `❌ No centralized error handling`

---

### 4.3 Distinguish Operational vs System Errors
**Rule**: Handle expected errors gracefully, crash on unexpected.

**KAPI Validation**: `❌ No error classification`

---

### 4.4 Structured Error Responses
**Rule**: Consistent error format with error codes.

```python
class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: dict | None = None
```

**KAPI Validation**: `❌ Inconsistent error formats`

---

### 4.5 Log All Errors
**Rule**: Structured logging with correlation IDs.

**KAPI Validation**: `❌ No error logging`

---

### 4.6 Never Expose Stack Traces
**Rule**: Generic messages in production.

**KAPI Validation**: `❌ Stack traces in responses`

---

### 4.7 Validate Early, Fail Fast
**Rule**: Pydantic validation at request boundary.

**KAPI Validation**: `❌ Late validation in business logic`

---

### 4.8 Handle Database Errors
**Rule**: Catch IntegrityError, OperationalError explicitly.

**KAPI Validation**: `❌ No DB error handling`

---

### 4.9 Async Exception Handling
**Rule**: Use `async def` in exception handlers.

**KAPI Validation**: `⚠️ Sync exception handlers`

---

### 4.10 HTTP Exception for API Errors
**Rule**: Use `HTTPException` with proper status codes.

**KAPI Validation**: `❌ Raising generic exceptions in routes`

---

### 4.11 Request Validation Errors
**Rule**: Custom handler for RequestValidationError.

**KAPI Validation**: `⚠️ Default validation error format`

---

### 4.12 Global Error Middleware
**Rule**: Catch-all for unexpected errors.

```python
@app.middleware("http")
async def error_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception("Unhandled error")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
```

**KAPI Validation**: `❌ No global error middleware`

---

## 5. Security (25 Practices)

### 5.1 Input Validation with Pydantic
**Rule**: Never trust raw input. Validate everything.

**KAPI Validation**: `❌ Missing input validation`

---

### 5.2 Password Hashing
**Rule**: Use bcrypt or argon2, never plain text.

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
```

**KAPI Validation**: `❌ Weak password hashing`

---

### 5.3 Secrets Management
**Rule**: Use environment variables, never hardcode.

**KAPI Validation**: `❌ Secrets in code`

---

### 5.4 CORS Configuration
**Rule**: Explicit allowed origins, not "*" in production.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

**KAPI Validation**: `❌ CORS allow_origins=["*"]`

---

### 5.5 Rate Limiting
**Rule**: Use slowapi or nginx for rate limiting.

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/data")
@limiter.limit("5/minute")
async def get_data():
    return {"data": "value"}
```

**KAPI Validation**: `❌ No rate limiting`

---

### 5.6 SQL Injection Prevention
**Rule**: Use ORM parameterized queries, never string concat.

```python
# ✅ Do
result = await db.execute(
    select(User).where(User.email == email)
)

# ❌ Never
query = f"SELECT * FROM users WHERE email = '{email}'"
```

**KAPI Validation**: `❌ String concatenation in queries`

---

### 5.7 JWT Best Practices
**Rule**: Short expiration, refresh tokens, secure signing.

```python
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

**KAPI Validation**: `❌ Long-lived tokens`

---

### 5.8 HTTPS Only
**Rule**: Redirect HTTP to HTTPS in production.

**KAPI Validation**: `❌ HTTP allowed in production`

---

### 5.9 Secure Headers
**Rule**: Security headers middleware.

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)
```

**KAPI Validation**: `❌ No security headers`

---

### 5.10 OAuth2 with Password Flow
**Rule**: Use FastAPI's OAuth2PasswordBearer for auth.

**KAPI Validation**: `⚠️ Custom auth without standards`

---

### 5.11 CSRF Protection
**Rule**: CSRF tokens for state-changing operations.

**KAPI Validation**: `❌ No CSRF protection`

---

### 5.12 Dependency Scanning
**Rule**: Use safety or pip-audit in CI.

**KAPI Validation**: `❌ No vulnerability scanning`

---

### 5.13 Path Traversal Prevention
**Rule**: Validate file paths, use pathlib.

**KAPI Validation**: `❌ Unsafe file path handling`

---

### 5.14 Content Security Policy
**Rule**: CSP headers for web endpoints.

**KAPI Validation**: `⚠️ No CSP headers`

---

### 5.15 API Key Security
**Rule**: Use API keys in headers, not query params.

**KAPI Validation**: `❌ API keys in query strings`

---

### 5.16 Limit Request Size
**Rule**: Max request body size to prevent DoS.

**KAPI Validation**: `❌ No request size limits`

---

### 5.17 XML/JSON Bomb Prevention
**Rule**: Limit nesting depth and array sizes.

**KAPI Validation**: `⚠️ No depth/size validation`

---

### 5.18 Clickjacking Prevention
**Rule**: X-Frame-Options header.

**KAPI Validation**: `⚠️ No X-Frame-Options`

---

### 5.19 Session Security
**Rule**: Secure, HttpOnly cookies.

**KAPI Validation**: `❌ Insecure session cookies`

---

### 5.20 Least Privilege Principle
**Rule**: Database user has minimal permissions.

**KAPI Validation**: `⚠️ Database user has admin rights`

---

### 5.21 API Versioning
**Rule**: Version APIs to prevent breaking changes.

**KAPI Validation**: `⚠️ No API versioning`

---

### 5.22 Audit Logging
**Rule**: Log security-relevant events.

**KAPI Validation**: `❌ No audit trail`

---

### 5.23 Regex DoS Prevention
**Rule**: Timeout for regex operations.

**KAPI Validation**: `⚠️ Unsafe regex patterns`

---

### 5.24 Secrets Rotation
**Rule**: Document rotation process.

**KAPI Validation**: `⚠️ No rotation strategy`

---

### 5.25 2FA for Admin
**Rule**: Multi-factor for privileged operations.

**KAPI Validation**: `⚠️ No 2FA implementation`

---

## 6. Testing (13 Practices)

### 6.1 Async Test Client
**Rule**: Use httpx.AsyncClient for integration tests.

```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users", json={...})
        assert response.status_code == 201
```

**KAPI Validation**: `❌ Sync test client for async app`

---

### 6.2 Test Database Isolation
**Rule**: Transactional tests with rollback.

```python
@pytest.fixture
async def db_session():
    async with async_session() as session:
        async with session.begin():
            yield session
            await session.rollback()
```

**KAPI Validation**: `❌ Tests sharing database state`

---

### 6.3 Factory Pattern for Test Data
**Rule**: Use factory_boy or custom factories.

```python
class UserFactory:
    @staticmethod
    def create(**kwargs):
        defaults = {"email": "test@example.com", "password": "hashed"}
        return User(**(defaults | kwargs))
```

**KAPI Validation**: `❌ Manual test data creation`

---

### 6.4 AAA Pattern
**Structure**: Arrange, Act, Assert.

**KAPI Validation**: `❌ Tests not structured as AAA`

---

### 6.5 Test Coverage > 90%
**Rule**: Enforce with pytest-cov.

```bash
pytest --cov=src --cov-fail-under=90
```

**KAPI Validation**: `❌ Coverage below 90%`

---

### 6.6 Mock External Services
**Rule**: Use responses or httpx-mock.

**KAPI Validation**: `❌ Tests hitting real external APIs`

---

### 6.7 Test Error Scenarios
**Rule**: Test both success and failure paths.

**KAPI Validation**: `❌ Only happy path tests`

---

### 6.8 Parametrized Tests
**Rule**: Use @pytest.mark.parametrize for variants.

**KAPI Validation**: `⚠️ Duplicate test code`

---

### 6.9 Integration Tests with Docker
**Rule**: Real PostgreSQL/Redis in docker-compose.

**KAPI Validation**: `❌ Mocked database in integration tests`

---

### 6.10 API Contract Testing
**Rule**: Test request/response schemas match docs.

**KAPI Validation**: `⚠️ No schema validation tests`

---

### 6.11 Performance Testing
**Rule**: Baseline with locust or k6.

**KAPI Validation**: `⚠️ No performance benchmarks`

---

### 6.12 Test Fixtures Organization
**Rule**: conftest.py per domain.

**KAPI Validation**: `❌ Flat fixture structure`

---

### 6.13 Async Fixtures
**Rule**: Use pytest-asyncio for async setup.

**KAPI Validation**: `❌ Sync fixtures for async code`

---

## 7. Production (19 Practices)

### 7.1 Structured Logging
**Rule**: JSON logs with correlation IDs.

```python
import structlog

logger = structlog.get_logger()
logger.info("user_created", user_id=123, email="user@example.com")
```

**KAPI Validation**: `❌ Unstructured print statements`

---

### 7.2 Health Check Endpoint
**Rule**: `/health` with dependency checks.

```python
@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception:
        raise HTTPException(status_code=503, detail="Unhealthy")
```

**KAPI Validation**: `❌ No health check endpoint`

---

### 7.3 Graceful Shutdown
**Rule**: Handle SIGTERM, close connections.

```python
@app.on_event("shutdown")
async def shutdown_event():
    await db_engine.dispose()
    logger.info("Application shutdown complete")
```

**KAPI Validation**: `❌ No shutdown handlers`

---

### 7.4 Database Connection Pooling
**Rule**: Configure pool size and timeouts.

**KAPI Validation**: `⚠️ No connection pooling`

---

### 7.5 Alembic Migrations
**Rule**: Version all schema changes.

**KAPI Validation**: `❌ No migration system`

---

### 7.6 Environment-Based Config
**Rule**: Different settings per environment.

**KAPI Validation**: `❌ Single config for all environments`

---

### 7.7 Monitoring with APM
**Rule**: Integrate Datadog, New Relic, or Sentry.

**KAPI Validation**: `⚠️ No APM integration`

---

### 7.8 Request ID Middleware
**Rule**: Correlation ID per request.

```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.request_id = str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        return response
```

**KAPI Validation**: `❌ No request correlation`

---

### 7.9 Metrics Collection
**Rule**: Prometheus metrics for key operations.

**KAPI Validation**: `⚠️ No metrics collection`

---

### 7.10 Dependency Locking
**Rule**: Commit poetry.lock or requirements.txt.

**KAPI Validation**: `❌ No lockfile in repo`

---

### 7.11 Background Tasks
**Rule**: Use Celery/RQ for long-running jobs.

**KAPI Validation**: `❌ Long tasks blocking requests`

---

### 7.12 Database Indexing
**Rule**: Index all foreign keys and query columns.

**KAPI Validation**: `⚠️ Missing database indexes`

---

### 7.13 Response Caching
**Rule**: Cache expensive queries with Redis.

**KAPI Validation**: `⚠️ No caching layer`

---

### 7.14 OpenAPI Documentation
**Rule**: Complete API docs with examples.

**KAPI Validation**: `❌ Incomplete OpenAPI specs`

---

### 7.15 Uvicorn Production Config
**Rule**: Multiple workers, proper logging.

```bash
uvicorn main:app --workers 4 --log-config logging.yaml
```

**KAPI Validation**: `❌ Development server in production`

---

### 7.16 Static Type Checking
**Rule**: MyPy or Pyright in CI.

**KAPI Validation**: `❌ No static type checking`

---

### 7.17 Linting with Ruff
**Rule**: Fast Python linter in CI.

**KAPI Validation**: `❌ No linting configured`

---

### 7.18 Database Connection Retry
**Rule**: Exponential backoff on connection failures.

**KAPI Validation**: `❌ No retry logic`

---

### 7.19 Timeout Configuration
**Rule**: Timeouts for all external calls.

**KAPI Validation**: `❌ No timeout settings`

---

## 8. Docker (12 Practices)

### 8.1 Multi-Stage Builds
**Rule**: Separate build and runtime stages.

```dockerfile
FROM python:3.11-slim as builder
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt > requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
```

**KAPI Validation**: `❌ Single-stage Dockerfile`

---

### 8.2 Non-Root User
**Rule**: Create and use app user.

```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

**KAPI Validation**: `❌ Container runs as root`

---

### 8.3 .dockerignore
**Rule**: Exclude venv, __pycache__, .git, tests.

**KAPI Validation**: `❌ No .dockerignore`

---

### 8.4 Minimal Base Image
**Rule**: Use slim or alpine variants.

**KAPI Validation**: `⚠️ Using full Python image`

---

### 8.5 Layer Caching
**Rule**: Copy requirements before source code.

**KAPI Validation**: `❌ Inefficient layer ordering`

---

### 8.6 Health Check
**Rule**: Docker HEALTHCHECK directive.

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"
```

**KAPI Validation**: `⚠️ No Docker health check`

---

### 8.7 Environment Variables
**Rule**: Use ENV for defaults, never secrets.

**KAPI Validation**: `❌ Secrets in ENV`

---

### 8.8 Image Scanning
**Rule**: Trivy or Snyk in CI.

**KAPI Validation**: `❌ No image scanning`

---

### 8.9 Explicit Image Tags
**Rule**: Never use latest, use SHA256.

**KAPI Validation**: `❌ Using latest tag`

---

### 8.10 Clean pip Cache
**Rule**: `--no-cache-dir` flag.

**KAPI Validation**: `⚠️ pip cache in image`

---

### 8.11 Signal Handling
**Rule**: Use exec form for CMD.

```dockerfile
CMD ["uvicorn", "src.main:app"]  # ✅
# Not: CMD uvicorn src.main:app  # ❌
```

**KAPI Validation**: `❌ Shell form in CMD`

---

### 8.12 Build Arguments
**Rule**: ARG for build-time configuration.

**KAPI Validation**: `⚠️ Hardcoded build values`

---

## 9. Performance (8 Practices)

### 9.1 Async Database Sessions
**Rule**: Use asyncpg, aiomysql, motor.

**KAPI Validation**: `❌ Sync database drivers`

---

### 9.2 Connection Pooling
**Rule**: Configure max connections and overflow.

**KAPI Validation**: `⚠️ No connection pooling`

---

### 9.3 Lazy Loading Prevention
**Rule**: Use joinedload/selectinload for relationships.

```python
from sqlalchemy.orm import selectinload

users = await db.execute(
    select(User).options(selectinload(User.posts))
)
```

**KAPI Validation**: `❌ N+1 query problems`

---

### 9.4 Response Compression
**Rule**: GZipMiddleware for large responses.

```python
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

**KAPI Validation**: `⚠️ No response compression`

---

### 9.5 Pagination
**Rule**: Cursor or offset pagination for large datasets.

**KAPI Validation**: `❌ Returning all records`

---

### 9.6 Database Indexing
**Rule**: Index all WHERE/JOIN columns.

**KAPI Validation**: `⚠️ Missing indexes`

---

### 9.7 Query Optimization
**Rule**: Use explain analyze for slow queries.

**KAPI Validation**: `⚠️ No query optimization`

---

### 9.8 Caching Strategy
**Rule**: Redis for hot data, CDN for static assets.

**KAPI Validation**: `⚠️ No caching layer`

---

## KAPI Integration

### Brutal Analysis Checks

**P0 (Critical - Block Deployment)**:
- ❌ Secrets in code
- ❌ SQL injection risk (string concat in queries)
- ❌ No password hashing
- ❌ No input validation
- ❌ Sync database drivers in async app
- ❌ No tests
- ❌ Container runs as root
- ❌ CORS allow_origins=["*"]

**P1 (High - Warn)**:
- ⚠️ No rate limiting
- ⚠️ Coverage < 90%
- ⚠️ No APM integration
- ⚠️ No health check endpoint
- ⚠️ No connection pooling
- ⚠️ Missing database indexes

**P2 (Medium - Suggest)**:
- ℹ️ No API versioning
- ℹ️ Could use smaller Docker image
- ℹ️ No response caching
- ℹ️ Missing request compression

### Blueprint Generation

Every KAPI FastAPI blueprint includes:
1. **Poetry** with locked dependencies
2. **Ruff + MyPy** for code quality
3. **Pydantic models** for all I/O
4. **Alembic** for migrations
5. **Structured logging** with structlog
6. **pytest + httpx** test setup
7. **Multi-stage Dockerfile**
8. **Health check** endpoint
9. **Error handling** middleware
10. **Security headers** middleware

### Living Specifications

Blueprints document compliance:

```markdown
## Best Practices Compliance

✅ 1.1 Domain-centric structure
✅ 2.1 Async-first routes
✅ 3.1 Pydantic validation
✅ 4.2 Centralized error handling
✅ 5.2 Password hashing (bcrypt)
✅ 6.1 httpx AsyncClient tests
✅ 7.2 Health check endpoint
✅ 8.1 Multi-stage Docker build
⚠️  7.7 APM - manual setup required
⚠️  9.8 Caching - Redis optional
```

---

## Quick Reference Checklist

### Essential (Must Have)
- [ ] Domain-centric project structure
- [ ] Async routes with async database drivers
- [ ] Pydantic models for all I/O
- [ ] Custom exception hierarchy
- [ ] Centralized error handler
- [ ] Password hashing (bcrypt/argon2)
- [ ] Input validation with Pydantic
- [ ] SQL injection prevention (ORM)
- [ ] CORS configuration (not "*")
- [ ] Rate limiting
- [ ] pytest with 90%+ coverage
- [ ] Async test client (httpx)
- [ ] Health check endpoint
- [ ] Structured logging (structlog)
- [ ] Alembic migrations
- [ ] Poetry with lock file
- [ ] Multi-stage Dockerfile
- [ ] Non-root Docker user
- [ ] .dockerignore

### Important (Should Have)
- [ ] JWT with short expiration
- [ ] Request ID middleware
- [ ] Graceful shutdown handlers
- [ ] Database connection pooling
- [ ] MyPy/Pyright type checking
- [ ] Ruff linting
- [ ] APM integration (Sentry/Datadog)
- [ ] Security headers middleware
- [ ] Factory pattern for tests
- [ ] Docker health check
- [ ] Image scanning (Trivy)
- [ ] Response compression

### Nice to Have
- [ ] Metrics collection (Prometheus)
- [ ] Caching layer (Redis)
- [ ] Background tasks (Celery)
- [ ] API versioning
- [ ] Performance benchmarks
- [ ] Alpine base image
- [ ] OpenTelemetry tracing

---

## References

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **FastAPI Best Practices**: https://github.com/zhanymkanov/fastapi-best-practices
- **Netflix Dispatch**: https://github.com/Netflix/dispatch
- **SQLModel**: https://sqlmodel.tiangolo.com
- **Pydantic**: https://docs.pydantic.dev
- **KAPI Blueprint Catalog**: [../../../docs-new/02-what/product/04-blueprint-catalog.md]

---

**Last Updated**: January 2025  
**Maintained by**: KAPI Team
