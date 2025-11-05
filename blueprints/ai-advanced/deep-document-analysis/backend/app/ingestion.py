import tempfile
import uuid
from pathlib import Path
from typing import List

from fastapi import UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredURLLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from .config import get_settings


settings = get_settings()

def _create_vector_store(collection: str) -> Chroma:
    return Chroma(
        collection_name=collection,
        embedding_function=HuggingFaceEmbeddings(model_name=settings.embedding_model),
        persist_directory=str(settings.chroma_persist_directory),
    )


def _split_documents(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    return splitter.split_documents(documents)


def ingest_file(upload: UploadFile, collection: str = "default") -> int:
    suffix = Path(upload.filename or "document").suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(upload.file.read())
        tmp_path = Path(tmp.name)

    try:
        if suffix == ".pdf":
            loader = PyPDFLoader(str(tmp_path))
        else:
            loader = TextLoader(str(tmp_path), encoding="utf-8")
        documents = loader.load()
    finally:
        tmp_path.unlink(missing_ok=True)

    chunks = _split_documents(documents)
    store = _create_vector_store(collection)
    store.add_documents(chunks, ids=[str(uuid.uuid4()) for _ in chunks])
    store.persist()
    return len(chunks)


def ingest_text(text: str, title: str | None = None, collection: str = "default") -> int:
    document = Document(page_content=text, metadata={"source": title or "direct-input"})
    chunks = _split_documents([document])
    store = _create_vector_store(collection)
    store.add_documents(chunks, ids=[str(uuid.uuid4()) for _ in chunks])
    store.persist()
    return len(chunks)


def ingest_urls(urls: List[str], collection: str = "default") -> int:
    loader = UnstructuredURLLoader(urls)
    documents = loader.load()
    chunks = _split_documents(documents)
    store = _create_vector_store(collection)
    store.add_documents(chunks, ids=[str(uuid.uuid4()) for _ in chunks])
    store.persist()
    return len(chunks)
