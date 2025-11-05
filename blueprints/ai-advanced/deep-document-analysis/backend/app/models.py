from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class IngestionResponse(BaseModel):
    document_id: str
    chunks_indexed: int
    sources: List[str]


class URLIngestionRequest(BaseModel):
    url: HttpUrl
    collection: Optional[str] = "default"


class TextIngestionRequest(BaseModel):
    text: str
    title: Optional[str] = None
    collection: Optional[str] = "default"


class QueryRequest(BaseModel):
    question: str
    provider: str
    model: Optional[str] = None
    temperature: float = 0.2
    k: int = 4
    collection: Optional[str] = "default"


class QueryResponse(BaseModel):
    answer: str
    context: List[str]
    provider: str
    model: str
    price_estimate: Optional[str] = None
