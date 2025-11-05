from typing import List, Tuple

from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from .config import get_settings
from .universal_llm import LLMConfig, PRICING_TABLE, create_llm


settings = get_settings()


def _vector_store(collection: str = "default") -> Chroma:
    return Chroma(
        collection_name=collection,
        embedding_function=HuggingFaceEmbeddings(model_name=settings.embedding_model),
        persist_directory=str(settings.chroma_persist_directory),
    )


def answer_question(question: str, provider: str, model: str | None, temperature: float, k: int, collection: str = "default") -> Tuple[str, List[str], str | None]:
    llm = create_llm(LLMConfig(provider=provider, model=model, temperature=temperature))
    store = _vector_store(collection)
    retriever = store.as_retriever(search_kwargs={"k": k})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
    result = chain.invoke({"query": question})
    answer = result["result"]
    sources = [doc.page_content for doc in result.get("source_documents", [])]

    pricing_key = f"{provider}-{(model or '').replace(':', '').replace('.', '-')}"
    pricing = None
    if pricing_key in PRICING_TABLE:
        info = PRICING_TABLE[pricing_key]
        pricing = f"${info.input_cost_per_1m}/1M input tokens, ${info.output_cost_per_1m}/1M output tokens"
    return answer, sources, pricing
