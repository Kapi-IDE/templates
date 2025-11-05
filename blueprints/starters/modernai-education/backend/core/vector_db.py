import chromadb
from core.models import Models
from typing import List
import numpy as np

class VectorDB:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorDB, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.models = Models()
            self.setup_chroma()
            self._initialized = True  

    def setup_chroma(self):
        self.chroma_client = chromadb.PersistentClient(path="db/modernaipro")
        # Get existing collection or create a new one if it doesn't exist
        try:
            self.chroma_collection = self.chroma_client.get_collection(name="modernaipro")
            print("Found existing collection: modernaipro")
        except Exception:
            self.chroma_collection = self.chroma_client.create_collection(name="modernaipro")
            print("Created new collection: modernaipro") 

    def generate_embeddings(self, documents: List[str]) -> np.ndarray:
        embeddings = self.models.embeddings_model.embed_documents(documents)
        return np.array(embeddings)
    
    def add_to_chroma(self, document: str, id: int, embeddings: np.ndarray, metadata: dict):
        self.chroma_collection.add(
            ids=[str(id)],
            documents=[document],
            embeddings=embeddings,
            metadatas=[metadata]
        )
    
    def delete_chroma(self):
        all_ids = self.chroma_collection.get()["ids"]
        if all_ids:
            self.chroma_collection.delete(ids=all_ids)
            print(f"Deleted all {len(all_ids)} documents in collection")
        else:
            print("Collection is already empty")

    def search(self, query: str):
        prompt = "Rewrite the following query to be used in a vector database search: " + query
        rewritten_query = self.models.groq_fast_llm.invoke(prompt).content
        query_embedding = self.models.embeddings_model.embed_documents([rewritten_query])
        results = self.chroma_collection.query(
            query_embeddings=query_embedding,
            n_results=5
        )  
        return results
    
    def get_embeddings_from_chroma(self):
        """
        Retrieve all embeddings and documents from ChromaDB
        """
        results = self.chroma_collection.get(
            include=["embeddings", "documents", "metadatas"]
        )
        
        # Debug information
        print(f"Results keys: {list(results.keys() if isinstance(results, dict) else [])}")
        
        # Check if we have embeddings
        if not isinstance(results, dict) or "embeddings" not in results or len(results["embeddings"]) == 0:
            print("No embeddings found in collection")
            return {
                "embeddings": [],  # Empty list instead of numpy array
                "documents": [],
                "ids": [],
                "metadatas": []
            }
        
        # Convert embeddings to list instead of numpy array
        embeddings = results["embeddings"]
        print(f"Retrieved {len(embeddings)} embeddings")
        
        # Get documents and IDs
        documents = results.get("documents", [])
        ids = results.get("ids", [])
        metadatas = results.get("metadatas", [None] * len(ids))
        
        print(f"Retrieved {len(documents)} documents, {len(ids)} IDs")
        
        return {
            "embeddings": embeddings,  # Already a list from ChromaDB
            "documents": documents,
            "ids": ids,
            "metadatas": metadatas
        }
    
if __name__ == "__main__":
    vector_db = VectorDB()
    results = vector_db.search("Tell me about machine learning")
    print(results)

    test_documents = [
        "Machine learning is a subset of artificial intelligence that focuses on training models to learn from data.",
        "Deep learning uses neural networks with multiple layers to automatically learn representations of data.",
        "Natural Language Processing (NLP) enables computers to understand, interpret and generate human language.",
        "Computer vision systems use AI to analyze and understand visual information from images and videos.",
        "Reinforcement learning is a type of machine learning where agents learn optimal actions through trial and error."
    ]
    metadata = [
        {"source": "Wikipedia"},
        {"source": "Wikipedia"},
        {"source": "Wikipedia"},
        {"source": "Wikipedia"},
        {"source": "Wikipedia"}
    ]

    count = 0
    for document in test_documents:
        embeddings = vector_db.generate_embeddings([document])
        vector_db.add_to_chroma(document, count, embeddings, metadata[count])
        count += 1
    results = vector_db.search("Tell me about machine learning")
    print(results)

    vector_db.delete_chroma()
    
    