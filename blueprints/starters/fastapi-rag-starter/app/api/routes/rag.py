"""RAG API routes for document upload and querying."""

from typing import Annotated
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pathlib import Path
import tempfile
from pydantic import BaseModel

from app.api.deps import SessionDep, CurrentUser
from app.rag.document_processor import document_processor
from app.rag.vector_store import vector_store
from app.rag.query_engine import query_engine


router = APIRouter()


class QueryRequest(BaseModel):
    """Request model for RAG queries."""
    question: str
    n_results: int = 3


class QueryResponse(BaseModel):
    """Response model for RAG queries."""
    answer: str
    sources: list[dict]
    context_used: list[str] | None = None


class DocumentUploadResponse(BaseModel):
    """Response model for document uploads."""
    message: str
    filename: str
    chunks_created: int


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    session: SessionDep,
    current_user: CurrentUser,
    file: Annotated[UploadFile, File(description="PDF or TXT file to upload")]
) -> DocumentUploadResponse:
    """Upload and process a document for RAG.

    Args:
        session: Database session
        current_user: Current authenticated user
        file: Uploaded file

    Returns:
        Upload confirmation with details
    """
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    allowed_extensions = {".pdf", ".txt"}
    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not supported. Allowed: {allowed_extensions}"
        )

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = Path(tmp_file.name)

    try:
        # Process document
        chunks, metadatas, ids = document_processor.process_document(
            tmp_path,
            metadata={"uploaded_by": current_user.email}
        )

        # Add to vector store
        vector_store.add_documents(chunks, metadatas, ids)

        return DocumentUploadResponse(
            message="Document uploaded and processed successfully",
            filename=file.filename,
            chunks_created=len(chunks)
        )

    finally:
        # Clean up temp file
        tmp_path.unlink(missing_ok=True)


@router.post("/query", response_model=QueryResponse)
async def query_documents(
    session: SessionDep,
    current_user: CurrentUser,
    request: QueryRequest
) -> QueryResponse:
    """Query documents using RAG.

    Args:
        session: Database session
        current_user: Current authenticated user
        request: Query request with question

    Returns:
        Answer with sources
    """
    result = await query_engine.query(
        question=request.question,
        n_results=request.n_results
    )

    return QueryResponse(**result)


@router.post("/query/stream")
async def stream_query_documents(
    session: SessionDep,
    current_user: CurrentUser,
    request: QueryRequest
):
    """Stream query response using RAG.

    Args:
        session: Database session
        current_user: Current authenticated user
        request: Query request with question

    Returns:
        Streaming response with answer chunks
    """
    async def generate():
        async for chunk in query_engine.stream_query(
            question=request.question,
            n_results=request.n_results
        ):
            yield chunk

    return StreamingResponse(generate(), media_type="text/plain")


@router.delete("/reset")
async def reset_vector_store(
    session: SessionDep,
    current_user: CurrentUser
):
    """Reset the vector store (delete all documents).

    Args:
        session: Database session
        current_user: Current authenticated user

    Returns:
        Confirmation message
    """
    # Only allow admins to reset
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Only admins can reset the vector store")

    vector_store.reset()

    return {"message": "Vector store reset successfully"}
