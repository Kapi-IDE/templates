from fastapi import FastAPI, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings, Settings
from . import ingestion
from .models import (
    IngestionResponse,
    TextIngestionRequest,
    URLIngestionRequest,
    QueryRequest,
    QueryResponse,
)
from .retriever import answer_question


app = FastAPI(title="Deep Document Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def get_app_settings() -> Settings:
    return get_settings()


@app.get("/healthz")
def health(settings: Settings = Depends(get_app_settings)):
    return {"status": "ok", "embedding_model": settings.embedding_model}


@app.post("/ingest/file", response_model=IngestionResponse)
async def ingest_document(upload: UploadFile, collection: str = "default"):
    if upload.content_type not in {"application/pdf", "text/plain", "text/markdown"}:
        raise HTTPException(status_code=400, detail="Only PDF or text files are supported")
    chunks = ingestion.ingest_file(upload, collection=collection)
    return IngestionResponse(document_id=upload.filename or "document", chunks_indexed=chunks, sources=[upload.filename or "upload"])


@app.post("/ingest/text", response_model=IngestionResponse)
async def ingest_text(payload: TextIngestionRequest):
    chunks = ingestion.ingest_text(payload.text, title=payload.title, collection=payload.collection)
    return IngestionResponse(document_id=payload.title or "direct-input", chunks_indexed=chunks, sources=[payload.title or "direct-input"])


@app.post("/ingest/url", response_model=IngestionResponse)
async def ingest_url(payload: URLIngestionRequest):
    chunks = ingestion.ingest_urls([str(payload.url)], collection=payload.collection)
    return IngestionResponse(document_id=str(payload.url), chunks_indexed=chunks, sources=[str(payload.url)])


@app.post("/query", response_model=QueryResponse)
async def query_documents(payload: QueryRequest):
    answer, context, pricing = answer_question(
        question=payload.question,
        provider=payload.provider,
        model=payload.model,
        temperature=payload.temperature,
        k=payload.k,
        collection=payload.collection,
    )
    return QueryResponse(
        answer=answer,
        context=context,
        provider=payload.provider,
        model=payload.model or "auto",
        price_estimate=pricing,
    )


__all__ = ["app"]
