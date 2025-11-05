#!/usr/bin/env python3
"""
Audit Documentation Model for AI Governance System
"""

from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
import json


class DocumentType(Enum):
    """Audit document types"""
    COMPREHENSIVE_AUDIT = "comprehensive_audit"
    RISK_ASSESSMENT = "risk_assessment"
    COMPLIANCE_REVIEW = "compliance_review"
    BIAS_ANALYSIS = "bias_analysis"
    SECURITY_AUDIT = "security_audit"


class AuditStandard(Enum):
    """Audit standards compliance"""
    ISO_19011 = "ISO_19011"
    SOC2 = "SOC2"
    EU_AI_ACT_AUDIT = "EU_AI_Act_Audit"
    NIST_CSF = "NIST_CSF"


@dataclass
class AuditDocumentation:
    """Audit Documentation model"""
    documentation_id: str
    system_id: str
    assessor_id: str
    document_type: DocumentType = DocumentType.COMPREHENSIVE_AUDIT
    executive_summary: Dict[str, Any] = field(default_factory=dict)
    detailed_findings: Dict[str, Any] = field(default_factory=dict)
    compliance_documentation: Dict[str, Any] = field(default_factory=dict)
    risk_documentation: Dict[str, Any] = field(default_factory=dict)
    audit_evidence: Dict[str, Any] = field(default_factory=dict)
    action_plan: Dict[str, Any] = field(default_factory=dict)
    audit_metadata: Dict[str, Any] = field(default_factory=dict)
    next_audit_date: Optional[str] = None
    retention_period: str = "7 years"
    document_version: str = "1.0"
    integrity_hash: str = ""
    access_controls: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'documentation_id': self.documentation_id,
            'system_id': self.system_id,
            'assessor_id': self.assessor_id,
            'document_type': self.document_type.value,
            'executive_summary': self.executive_summary,
            'detailed_findings': self.detailed_findings,
            'compliance_documentation': self.compliance_documentation,
            'risk_documentation': self.risk_documentation,
            'audit_evidence': self.audit_evidence,
            'action_plan': self.action_plan,
            'audit_metadata': self.audit_metadata,
            'next_audit_date': self.next_audit_date,
            'retention_period': self.retention_period,
            'document_version': self.document_version,
            'integrity_hash': self.integrity_hash,
            'access_controls': self.access_controls,
            'created_at': self.created_at.isoformat()
        }