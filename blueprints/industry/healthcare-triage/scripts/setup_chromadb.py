#!/usr/bin/env python3
"""
ChromaDB Setup Script
Initializes the medical knowledge vector database
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database.chromadb_manager import MedicalKnowledgeStore
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Initialize ChromaDB with medical knowledge"""
    try:
        logger.info("Initializing ChromaDB for medical knowledge...")
        
        # Create knowledge store
        knowledge_store = MedicalKnowledgeStore()
        
        # Load medical data
        logger.info("Loading medical data into ChromaDB...")
        knowledge_store.load_medical_data()
        
        # Get stats
        stats = knowledge_store.get_collection_stats()
        logger.info(f"ChromaDB initialized successfully with {stats} records")
        
        logger.info("ChromaDB setup completed!")
        
    except Exception as e:
        logger.error(f"ChromaDB setup failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())