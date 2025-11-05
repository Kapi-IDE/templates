# API Reference

Base URL: `http://localhost:8000`

## `GET /healthz`
Health probe. Returns status + embedding model.

## `POST /ingest/file`
- Multipart upload (`upload` field)
- Optional `collection` query param
- Response: `{ document_id, chunks_indexed, sources }`

## `POST /ingest/text`
```json
{
  "text": "string",
  "title": "optional",
  "collection": "default"
}
```

## `POST /ingest/url`
```json
{
  "url": "https://example.com",
  "collection": "default"
}
```

## `POST /query`
```json
{
  "question": "Who are the stakeholders?",
  "provider": "groq|openai|anthropic|gemini|ollama",
  "model": "optional",
  "temperature": 0.2,
  "k": 4,
  "collection": "default"
}
```
Response contains synthesized answer, supporting context chunks, provider metadata, and pricing hint when available.
