# 🧠 Deep Document Analysis Blueprint

Multi-provider document analysis workbench that lets teams ingest PDFs, URLs, and pasted text, store them in a vector database, and interrogate the corpus with the LLM of their choice. Ships with a FastAPI backend, Streamlit analyst UI, and the universal multi-LLM selector component.

## Architecture Overview
- **FastAPI backend** handles ingestion (PDF, URL, manual text) and querying over a Chroma vector store.
- **Universal LLM client** (copied from `components/backend/universal-llm-client`) unifies Groq, OpenAI, Anthropic, Gemini, and Ollama providers.
- **HuggingFace sentence transformer** (`all-MiniLM-L6-v2`) generates embeddings stored in Chroma.
- **Streamlit front-end** wraps the `llm-selector` component pattern to toggle providers, upload documents, and run deep question answering.

```
deep-document-analysis/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entrypoint
│   │   ├── ingestion.py         # PDF/URL/text ingestion pipeline
│   │   ├── retriever.py         # RetrievalQA chain wiring
│   │   ├── models.py            # Pydantic contracts
│   │   └── universal_llm.py     # Multi-provider LLM adapter
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app.py                   # Streamlit analyst console
│   ├── requirements.txt
│   └── components/llm_selector.py
└── docs/
    ├── architecture.md
    └── api.md
```

## Quick Start

### 1. Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add LLM API keys
uvicorn app.main:app --reload
```

### 2. Frontend
```bash
cd frontend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DEEP_DOC_API_URL="http://localhost:8000"
streamlit run app.py
```

### 3. Usage Flow
1. Upload PDFs, paste long text, or ingest URLs from the Streamlit sidebar.
2. Choose a provider (Groq, OpenAI, Anthropic, Gemini, or Ollama) and optional custom model.
3. Ask deep-dive questions—responses include the synthesized answer and the supporting chunks.

## Components Reused
- `components/backend/universal-llm-client` for provider abstraction + pricing metadata.
- Applies the `llm-selector` UX pattern (ported to Streamlit) from `components/frontend/llm-selector`.
- Vector database guidance follows `recipes/ai-specific/vector-database-blueprint.yaml` and uses Chroma as in the RAG starter.

## Next Steps
- Add background ingestion workers for large corpora.
- Layer in evaluation metrics (map accuracy, hallucination checks) via LangChain evaluators.
- Package with Docker Compose (API + Streamlit + Ollama) for single-command deploy.
