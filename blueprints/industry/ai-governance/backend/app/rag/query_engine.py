"""Query engine for RAG-based question answering."""

from typing import Dict, Any
from openai import AsyncOpenAI
from app.core.config import settings
from app.rag.vector_store import vector_store


class QueryEngine:
    """RAG query engine using OpenAI and ChromaDB."""

    def __init__(self):
        """Initialize query engine."""
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    async def query(
        self,
        question: str,
        n_results: int = 3,
        system_prompt: str | None = None
    ) -> Dict[str, Any]:
        """Answer a question using RAG.

        Args:
            question: User's question
            n_results: Number of context chunks to retrieve
            system_prompt: Optional system prompt override

        Returns:
            Dictionary with answer and sources
        """
        # Retrieve relevant context
        search_results = vector_store.search(question, n_results=n_results)

        # Extract context from search results
        contexts = search_results.get("documents", [[]])[0]
        metadatas = search_results.get("metadatas", [[]])[0]

        if not contexts:
            return {
                "answer": "I don't have enough information to answer that question.",
                "sources": [],
                "context_used": []
            }

        # Build context string
        context_str = "\n\n".join([
            f"[Source {i+1}]: {ctx}"
            for i, ctx in enumerate(contexts)
        ])

        # Build prompt
        default_system_prompt = (
            "You are a helpful assistant that answers questions based on the provided context. "
            "If the answer cannot be found in the context, say so. "
            "Always cite your sources using [Source N] notation."
        )

        user_prompt = f"""Context information:
{context_str}

Question: {question}

Answer based on the context above:"""

        # Generate answer using OpenAI
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt or default_system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        answer = response.choices[0].message.content

        # Format sources
        sources = [
            {
                "source": meta.get("source", "Unknown"),
                "chunk_index": meta.get("chunk_index", 0),
                "file_path": meta.get("file_path", "")
            }
            for meta in metadatas
        ]

        return {
            "answer": answer,
            "sources": sources,
            "context_used": contexts
        }

    async def stream_query(
        self,
        question: str,
        n_results: int = 3,
        system_prompt: str | None = None
    ):
        """Stream answer to a question using RAG.

        Args:
            question: User's question
            n_results: Number of context chunks to retrieve
            system_prompt: Optional system prompt override

        Yields:
            Answer chunks as they're generated
        """
        # Retrieve relevant context
        search_results = vector_store.search(question, n_results=n_results)

        # Extract context from search results
        contexts = search_results.get("documents", [[]])[0]

        if not contexts:
            yield "I don't have enough information to answer that question."
            return

        # Build context string
        context_str = "\n\n".join([
            f"[Source {i+1}]: {ctx}"
            for i, ctx in enumerate(contexts)
        ])

        # Build prompt
        default_system_prompt = (
            "You are a helpful assistant that answers questions based on the provided context. "
            "If the answer cannot be found in the context, say so. "
            "Always cite your sources using [Source N] notation."
        )

        user_prompt = f"""Context information:
{context_str}

Question: {question}

Answer based on the context above:"""

        # Stream answer using OpenAI
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt or default_system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500,
            stream=True
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


# Global instance
query_engine = QueryEngine()
