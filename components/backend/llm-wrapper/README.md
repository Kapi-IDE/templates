# Gemini Client Wrapper

Lightweight wrapper around the Google Gemini SDK that standardises configuration, text generation, and structured JSON output for healthcare agents.

## What It Provides
- Automatic API key discovery (`GOOGLE_API_KEY`)
- Plain-text generation via `generate_text(prompt, context=None)`
- Structured JSON extraction via `generate_json(prompt)`
- Health-check helper for readiness probes

## Usage
```python
from components.backend.llm_wrapper.gemini_client import GeminiClient

client = GeminiClient()
response = client.generate_text("Summarise these symptoms", context={"symptoms": ["dizziness"]})
```

Run `example/use_client.py` after exporting `GOOGLE_API_KEY` to verify the wrapper.
