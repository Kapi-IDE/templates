#!/usr/bin/env python3
"""
Legal Database Management Module
Provides database managers for legal data with attorney-client privilege protection
"""

from .sqlite_legal_manager import LegalDataManager
from .chromadb_legal_manager import LegalKnowledgeStore

__all__ = [
    'LegalDataManager',
    'LegalKnowledgeStore'
]