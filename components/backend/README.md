# Backend Components

Reusable backend modules for building AI-powered applications across any domain.

---

## 📦 Available Components

### 1. Agent Framework
**Location:** `/components/backend/agent_framework/`

**Purpose:** Domain-agnostic foundation for building conversational AI agents with LLM integration, logging, and structured data extraction.

**What's Included:**
- `agent/base.py` - `AgentFoundation` base class
- `llm/gemini_client.py` - Gemini LLM client (swappable)
- `logging/interaction_logger.py` - Audit logging utilities

**Key Features:**
- ✅ LLM-agnostic architecture (Gemini by default, easily swap to OpenAI/Anthropic)
- ✅ Structured data extraction from AI responses
- ✅ Comprehensive audit logging for compliance
- ✅ Health check and monitoring
- ✅ Fallback handling for API failures
- ✅ Context-aware response generation

**Usage:**
```python
from components.backend.agent_framework.agent.base import AgentFoundation

class MyCustomAgent(AgentFoundation):
    # Override BASE_PROMPT for your domain
    BASE_PROMPT = """
    You are a financial advisor AI assistant...
    """

    def __init__(self, knowledge_store, data_store):
        super().__init__(
            knowledge_store=knowledge_store,
            data_store=data_store,
            agent_type="financial_advisor"
        )

    def fallback_response(self):
        # Domain-specific fallback
        return "Please consult with a licensed financial advisor."
```

**Metrics:**
- **Lines of Code:** ~400 (272 base + 71 LLM + 51 logging)
- **Setup Time:** 2 minutes
- **Token Savings:** 300+ tokens per blueprint
- **Complexity:** Moderate

---

### 2. AI Integrations
**Location:** `/components/backend/ai-integrations/`

**Purpose:** Production-ready clients for major AI/LLM providers with standardized interfaces and security-first design.

**What's Included:**
- `gemini/client.py` - Google Gemini with OpenAI-compatible interface
- `azure-openai/client.py` - Enterprise Azure OpenAI with DeepSeek support
- `anthropic-bedrock/client.py` - Claude via AWS Bedrock

**Key Features:**
- ✅ Environment variable based authentication (NO hardcoded secrets)
- ✅ Consistent interfaces across providers for easy switching
- ✅ Token usage tracking and cost estimation
- ✅ Health check functions for monitoring
- ✅ Advanced features (reasoning, tool calling, embeddings)
- ✅ Production error handling and retry logic

**Quick Start:**
```python
# Gemini
from components.backend.ai_integrations.gemini import chat_completion
response = chat_completion(messages=[{"role": "user", "content": "Hello!"}])

# Azure OpenAI
from components.backend.ai_integrations.azure_openai import create_azure_openai_client, chat_completion
client = create_azure_openai_client()
result = chat_completion(client, "gpt-4", messages=[...])

# Claude (Bedrock)
from components.backend.ai_integrations.anthropic_bedrock import create_bedrock_client, invoke_claude
client = create_bedrock_client()
response = invoke_claude(client, "Explain quantum computing")
```

**Metrics:**
- **Lines of Code:** ~780 (240 Gemini + 280 Azure + 260 Claude)
- **Setup Time:** 1-3 minutes per provider
- **Token Savings:** 300-350 tokens per integration
- **Complexity:** Low-Moderate

---

### 3. Task Queue (Celery)
**Location:** `/components/backend/task-queue/`

**Purpose:** Production-ready async task processing with Celery and Redis/RabbitMQ.

**What's Included:**
- `celery_config.py` - Celery app factory with production settings

**Key Features:**
- ✅ Environment-based broker/backend configuration
- ✅ Retry logic with exponential backoff
- ✅ Task time limits and soft limits
- ✅ Worker optimization settings
- ✅ Progress tracking support

**Usage:**
```python
from components.backend.task_queue.celery_config import create_celery_app

celery_app = create_celery_app(app_name="my_app")

@celery_app.task(bind=True, max_retries=3)
def process_data(self, data):
    try:
        # Task logic
        pass
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

**Metrics:**
- **Lines of Code:** ~120
- **Setup Time:** 2 minutes
- **Token Savings:** 200 tokens

---

### 4. Database (PostgreSQL)
**Location:** `/components/backend/database/postgresql/`

**Purpose:** SQLAlchemy database setup with FastAPI dependency injection.

**What's Included:**
- `connection.py` - Database engine, session management, utilities

**Key Features:**
- ✅ Environment variable based connection
- ✅ FastAPI dependency injection ready
- ✅ Connection pooling with health checks
- ✅ Context manager for manual sessions
- ✅ Database health monitoring

**Usage:**
```python
from components.backend.database.postgresql import get_db, Base

# FastAPI dependency injection
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Manual session
from components.backend.database.postgresql import DatabaseSession
with DatabaseSession() as db:
    user = db.query(User).first()
```

**Metrics:**
- **Lines of Code:** ~170
- **Setup Time:** 2 minutes
- **Token Savings:** 250 tokens

---

### 5. Caching (Redis)
**Location:** `/components/backend/caching/redis/`

**Purpose:** Redis client for caching and session management.

**What's Included:**
- `client.py` - Redis client, session manager, cache wrapper

**Key Features:**
- ✅ Environment variable based connection
- ✅ Session management with secure token generation
- ✅ Simple caching wrapper with TTL
- ✅ Health check function
- ✅ Connection pooling and keepalive

**Usage:**
```python
from components.backend.caching.redis import RedisSessionManager, RedisCache

# Session management
session_mgr = RedisSessionManager()
session_id = session_mgr.create_session({"user_id": 123})
data = session_mgr.get_session(session_id)

# Simple caching
cache = RedisCache()
cache.set("user:123", {"name": "John"}, ttl=3600)
user = cache.get("user:123")
```

**Metrics:**
- **Lines of Code:** ~290
- **Setup Time:** 2 minutes
- **Token Savings:** 300 tokens

---

### 6. Database Migrations (Alembic)
**Location:** `/components/backend/database/migrations/`

**Purpose:** Automated Alembic setup for database schema migrations.

**What's Included:**
- `alembic_setup.py` - Auto-generate Alembic configuration

**Key Features:**
- ✅ One-command Alembic initialization
- ✅ Production-ready templates
- ✅ Environment variable based DB connection
- ✅ Auto-generated migration scripts
- ✅ Complete documentation

**Usage:**
```python
from components.backend.database.migrations import setup_alembic

# Initialize Alembic in your project
setup_alembic(project_root="/path/to/project")

# Then use standard Alembic commands:
# alembic revision --autogenerate -m "Add users table"
# alembic upgrade head
```

**Metrics:**
- **Lines of Code:** ~365
- **Setup Time:** 1 minute
- **Token Savings:** 400 tokens

---

## 🔧 Component Standards

Every backend component should have:

### Required Files
- ✅ `README.md` - Setup guide, API docs, examples
- ✅ `metadata.yaml` - LanceDB discovery metadata
- ✅ `__init__.py` - Python package setup
- ✅ Type hints throughout

### Metadata Format
```yaml
component_id: agent-framework
name: Agent Framework
version: 1.0.0
category: backend
subcategory: ai-agents

provides:
  - llm_integration
  - agent_foundation
  - audit_logging

compatible_with:
  - python>=3.9
  - google-generativeai

incompatible_with: []

metrics:
  token_count: 400
  setup_time_minutes: 2
  complexity: moderate

voice_patterns:
  - "agent framework"
  - "LLM integration"
  - "conversational AI base"
  - "agent foundation"
```

---

## 🏗️ Architecture Principles

### 1. Domain Agnostic
- No hardcoded business logic
- Configurable via inheritance
- Generic parameter names (user_id, data_store)

### 2. Swappable Dependencies
```python
# Easy to swap LLM providers
from .llm.gemini_client import GeminiClient
from .llm.openai_client import OpenAIClient  # Future

agent = MyAgent(llm_client=OpenAIClient())  # Just swap!
```

### 3. Progressive Customization
```python
# Level 1: Use as-is
agent = AgentFoundation(...)

# Level 2: Override prompts
class HealthcareAgent(AgentFoundation):
    BASE_PROMPT = "Healthcare-specific prompt..."

# Level 3: Custom methods
class FinanceAgent(AgentFoundation):
    def calculate_risk_score(self, data):
        # Domain-specific logic
```

### 4. Fail-Safe Design
- Graceful degradation on API failures
- Fallback responses
- Comprehensive error logging
- Health checks

---

## 📊 Integration Examples

### Healthcare Blueprint
```python
from components.backend.agent_framework.agent.base import AgentFoundation

class BaseAgent(AgentFoundation):
    BASE_PROMPT = """
    You are a healthcare AI assistant designed for patient triage...
    """

    def fallback_response(self):
        return "Please contact a healthcare professional directly."
```

### Finance Blueprint
```python
from components.backend.agent_framework.agent.base import AgentFoundation

class FinancialBaseAgent(AgentFoundation):
    BASE_PROMPT = """
    You are a professional financial AI assistant specializing in investment research...
    """

    def fallback_response(self):
        return "Please consult with a qualified financial advisor."
```

### Legal Blueprint
```python
from components.backend.agent_framework.agent.base import AgentFoundation

class LegalBaseAgent(AgentFoundation):
    BASE_PROMPT = """
    You are a legal research AI assistant...
    """

    def fallback_response(self):
        return "Please consult with a licensed attorney."
```

---

## 🚀 Getting Started

### Installation
```bash
# Copy component to your project
cp -r templates/components/backend/agent-framework your-project/backend/

# Install dependencies
pip install google-generativeai  # or your LLM provider
```

### Quick Start
```python
from agent_framework.agent.base import AgentFoundation

# Extend for your domain
class MyAgent(AgentFoundation):
    BASE_PROMPT = "Your domain-specific prompt here..."

# Initialize
agent = MyAgent(
    knowledge_store=my_vector_db,
    data_store=my_database,
    agent_type="my_agent"
)

# Generate responses
response = agent.generate_response(
    prompt="User query here",
    context={"user_profile": {...}}
)
```

---

## 🔐 Security & Compliance

### Audit Logging
- All interactions logged with timestamps
- Input/output summaries (not full content for privacy)
- Processing time tracking
- Success/failure status

### Data Privacy
- Generic parameter names (user_id vs patient_id)
- Configurable logging depth
- Support for HIPAA, SOC2, FINRA compliance

### API Key Management
- Environment variable based (GOOGLE_API_KEY)
- Never hardcoded
- Validation on initialization

---

## 🧪 Testing

### Component Tests
```python
# Test base agent
def test_agent_initialization():
    agent = AgentFoundation(
        knowledge_store=mock_store,
        data_store=mock_db,
        agent_type="test"
    )
    assert agent.agent_type == "test"

# Test LLM client
def test_gemini_client():
    client = GeminiClient()
    response = client.generate_text("Test prompt")
    assert len(response) > 0
```

### Integration Tests
```python
# Test in blueprint context
def test_healthcare_agent():
    agent = HealthcareAgent(...)
    response = agent.generate_response("chest pain symptoms")
    assert "medical professional" in response.lower()
```

---

## 📈 Metrics & Performance

| Component | LOC | Setup Time | Token Savings | Reusability |
|-----------|-----|------------|---------------|-------------|
| Agent Framework | 400 | 2 min | 300+ tokens | High (3+ blueprints) |

**Token Efficiency:**
- Without component: ~500 tokens per blueprint
- With component: ~200 tokens per blueprint
- **Savings: 60% reduction** ✅

---

## 🛠️ Future Components

### Planned
- `/authentication/` - JWT, OAuth, session management
- `/database/` - PostgreSQL, ChromaDB, Redis utilities
- `/rag/` - Retrieval-augmented generation framework
- `/monitoring/` - Health checks, metrics, alerting

### LLM Providers
- `llm/openai_client.py` - OpenAI integration
- `llm/anthropic_client.py` - Claude integration
- `llm/azure_openai_client.py` - Azure OpenAI

---

## 📚 Resources

- [Agent Framework API Docs](./agent-framework/README.md)
- [LLM Client Guide](./agent-framework/llm/README.md)
- [Logging Best Practices](./agent-framework/logging/README.md)

---

**Last Updated:** October 2025
**Maintainers:** KAPI Team
**Status:** Production Ready
