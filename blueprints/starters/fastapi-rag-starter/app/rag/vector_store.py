"""Vector store implementation using ChromaDB."""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from app.core.config import settings


class VectorStore:
    """ChromaDB vector store for document embeddings."""

    def __init__(self):
        """Initialize ChromaDB client."""
        self.client = chromadb.Client(
            Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=settings.CHROMA_PERSIST_DIR,
            )
        )
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ) -> None:
        """Add documents to the vector store.

        Args:
            documents: List of document texts
            metadatas: List of metadata dicts for each document
            ids: List of unique IDs for each document
        """
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def search(
        self,
        query: str,
        n_results: int = 5
    ) -> Dict[str, Any]:
        """Search for similar documents.

        Args:
            query: Search query text
            n_results: Number of results to return

        Returns:
            Dictionary with results, distances, and metadatas
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def delete_collection(self) -> None:
        """Delete the collection."""
        self.client.delete_collection(name=settings.CHROMA_COLLECTION_NAME)

    def reset(self) -> None:
        """Reset the collection by deleting and recreating it."""
        self.delete_collection()
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )


# Global instance
vector_store = VectorStore()
