# Architecture Notes

## High-Level Flow
1. **Ingestion**
   - PDF / text uploads handled via `/ingest/file`
   - URLs processed by `/ingest/url` using `UnstructuredURLLoader`
   - Raw text accepted via `/ingest/text`
2. **Chunking & Embeddings**
   - RecursiveCharacterTextSplitter (1200/150) slices documents
   - HuggingFace `all-MiniLM-L6-v2` embeddings persisted to Chroma
3. **Retrieval + LLM**
   - RetrievalQA (LangChain) pulls top-k chunks
   - Universal LLM wrapper spins up ChatGroq, ChatOpenAI, Claude, Gemini, or Ollama clients
4. **Presentation**
   - FastAPI returns synthesized answer + supporting chunks
   - Streamlit UI handles provider selection, ingestion status, and response display

## Key Decisions
- **Chroma** selected for local persistence + compatibility with LangChain.
- **Universal LLM client** centralises authentication + pricing to ease provider comparisons.
- **Streamlit** chosen for analyst-friendly UI with minimal setup.
- Providers + models configurable via environment or UI; defaults favour low-cost options.

## Environment Variables
- `GROQ_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, optional `OLLAMA_BASE_URL`.
- Backend reads `.env`; Streamlit uses `DEEP_DOC_API_URL` to locate API.

## Scaling Considerations
- Swap Chroma for managed vector DB via LangChain adapters if needed (Pinecone, Weaviate, LanceDB).
- Frontend can be ported to React using the existing `llm-selector` component for production dashboards.
- Add async task queue (Celery) for heavy ingestion.
