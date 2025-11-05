# Agent Foundation

Shared base class that encapsulates prompt scaffolding, LLM interaction, logging, and safety checks for conversational healthcare agents.

## Features
- Base safety prompt helper with domain-specific extensions
- Text/JSON generation helpers (Gemini by default) with fallbacks
- Audit logging via the reusable `interaction_logger`
- Urgency assessment utilities
- Health check aggregator across the LLM + backing stores

## Usage
```python
from components.backend.agent_base.agent_foundation import AgentFoundation
from components.backend.llm_wrapper.gemini_client import GeminiClient

foundation = AgentFoundation(
    knowledge_store=my_knowledge_store,
    patient_db=my_patient_db,
    agent_type="triage",
    llm_client=GeminiClient(),
)
```

See `example/app/main.py` for a FastAPI demo that exposes a `/triage` endpoint.
