#!/usr/bin/env python3
"""
Models package for AI Governance System
Contains data models for AI systems, assessments, and governance entities
"""

from .ai_system import AISystem, SystemStatus, RiskCategory
from .risk_assessment import RiskAssessment, RiskLevel, RiskDimension
from .policy_compliance import PolicyCompliance, ComplianceStatus, ComplianceFramework
from .bias_assessment import BiasAssessment, BiasLevel, FairnessMetric
from .audit_documentation import AuditDocumentation, DocumentType, AuditStandard

__all__ = [
    'AISystem', 'SystemStatus', 'RiskCategory',
    'RiskAssessment', 'RiskLevel', 'RiskDimension',
    'PolicyCompliance', 'ComplianceStatus', 'ComplianceFramework',
    'BiasAssessment', 'BiasLevel', 'FairnessMetric',
    'AuditDocumentation', 'DocumentType', 'AuditStandard'
]

__version__ = '1.0.0'