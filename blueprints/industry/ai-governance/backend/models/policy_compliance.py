#!/usr/bin/env python3
"""
Policy Compliance Model for AI Governance System
"""

from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
import json


class ComplianceStatus(Enum):
    """Compliance status levels"""
    COMPLIANT = "compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"
    REQUIRES_REVIEW = "requires_review"
    UNKNOWN = "unknown"


class ComplianceFramework(Enum):
    """Regulatory compliance frameworks"""
    EU_AI_ACT = "EU_AI_Act"
    NIST_AI_RMF = "NIST_AI_RMF"
    ISO_42001 = "ISO_42001"
    GDPR_AI = "GDPR_AI"


@dataclass
class PolicyCompliance:
    """Policy Compliance Assessment model"""
    assessment_id: str
    system_id: str
    assessor_id: str
    status: ComplianceStatus
    compliance_score: float
    frameworks: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    gaps: List[Dict[str, Any]] = field(default_factory=list)
    remediation_actions: List[Dict[str, Any]] = field(default_factory=list)
    regulatory_requirements: Dict[str, Any] = field(default_factory=dict)
    next_review_date: Optional[str] = None
    compliance_percentage: float = 0.0
    confidence_level: int = 7
    processing_time: float = 0.0
    assessment_date: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'assessment_id': self.assessment_id,
            'system_id': self.system_id,
            'assessor_id': self.assessor_id,
            'status': self.status.value,
            'compliance_score': self.compliance_score,
            'frameworks': self.frameworks,
            'gaps': self.gaps,
            'remediation_actions': self.remediation_actions,
            'regulatory_requirements': self.regulatory_requirements,
            'next_review_date': self.next_review_date,
            'compliance_percentage': self.compliance_percentage,
            'confidence_level': self.confidence_level,
            'processing_time': self.processing_time,
            'assessment_date': self.assessment_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }