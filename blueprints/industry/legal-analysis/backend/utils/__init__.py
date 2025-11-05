#!/usr/bin/env python3
"""
Legal AI Utilities Module
Provides security, ethics compliance, and monitoring utilities for legal AI system
"""

from .legal_security import AttorneyClientPrivilegeManager
from .legal_ethics import LegalEthicsComplianceManager

__all__ = [
    'AttorneyClientPrivilegeManager',
    'LegalEthicsComplianceManager'
]