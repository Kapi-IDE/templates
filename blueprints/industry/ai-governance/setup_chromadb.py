#!/usr/bin/env python3
"""
ChromaDB Setup Script for AI Governance Pod (Pod4)
Initializes ChromaDB with AI governance knowledge and regulatory frameworks
"""

import os
import sys
import logging

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database.chromadb_manager import GovernanceKnowledgeStore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Initialize ChromaDB with AI governance knowledge"""
    try:
        logger.info("Initializing AI Governance Knowledge Store...")
        
        # Create data directory
        os.makedirs('./data/chromadb', exist_ok=True)
        
        # Initialize knowledge store
        knowledge_store = GovernanceKnowledgeStore('./data/chromadb')
        
        # Get collection statistics
        stats = knowledge_store.get_collection_stats()
        
        logger.info("✅ ChromaDB knowledge store initialized successfully!")
        
        # Display summary
        print("\n" + "="*60)
        print("📚 AI GOVERNANCE KNOWLEDGE STORE SETUP COMPLETE")
        print("="*60)
        print(f"📋 Regulatory Frameworks: {stats.get('regulatory_frameworks', 0)} documents")
        print(f"📜 Governance Policies: {stats.get('governance_policies', 0)} documents")
        print(f"✅ Compliance Requirements: {stats.get('compliance_requirements', 0)} documents")
        print(f"🎯 Best Practices: {stats.get('best_practices', 0)} documents")
        print(f"📊 Case Studies: {stats.get('case_studies', 0)} documents")
        print(f"📝 Audit Templates: {stats.get('audit_templates', 0)} documents")
        print("="*60)
        print("🌐 Knowledge Base Includes:")
        print("   • EU AI Act 2024 (Complete regulatory text)")
        print("   • NIST AI Risk Management Framework 1.0")
        print("   • ISO/IEC 42001:2023 AI Management System")
        print("   • GDPR AI-specific requirements")
        print("   • AI Ethics and Bias Mitigation Policies")
        print("   • Governance Best Practices")
        print("="*60)
        print("📍 ChromaDB Location: ./data/chromadb/")
        print("🔍 Vector Embeddings: sentence-transformers/all-MiniLM-L6-v2")
        print("="*60)
        print("🚀 Ready for AI Governance Knowledge Search!")
        
    except Exception as e:
        logger.error(f"❌ ChromaDB setup failed: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)