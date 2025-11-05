#!/usr/bin/env python3
"""
Bias Assessment Model for AI Governance System
"""

from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
import json


class BiasLevel(Enum):
    """Bias risk levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class FairnessMetric(Enum):
    """Fairness evaluation metrics"""
    DEMOGRAPHIC_PARITY = "demographic_parity"
    EQUAL_OPPORTUNITY = "equal_opportunity"
    EQUALIZED_ODDS = "equalized_odds"
    INDIVIDUAL_FAIRNESS = "individual_fairness"
    CALIBRATION = "calibration"


@dataclass
class BiasAssessment:
    """Bias Assessment model"""
    assessment_id: str
    system_id: str
    assessor_id: str
    bias_level: BiasLevel
    bias_risk_score: float
    fairness_metrics: Dict[str, Any] = field(default_factory=dict)
    bias_dimensions: Dict[str, Any] = field(default_factory=dict)
    protected_groups_impact: Dict[str, Any] = field(default_factory=dict)
    discrimination_risks: Dict[str, Any] = field(default_factory=dict)
    mitigation_strategies: List[Dict[str, Any]] = field(default_factory=list)
    monitoring_plan: Dict[str, Any] = field(default_factory=dict)
    confidence_level: int = 7
    processing_time: float = 0.0
    assessment_date: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'assessment_id': self.assessment_id,
            'system_id': self.system_id,
            'assessor_id': self.assessor_id,
            'bias_level': self.bias_level.value,
            'bias_risk_score': self.bias_risk_score,
            'fairness_metrics': self.fairness_metrics,
            'bias_dimensions': self.bias_dimensions,
            'protected_groups_impact': self.protected_groups_impact,
            'discrimination_risks': self.discrimination_risks,
            'mitigation_strategies': self.mitigation_strategies,
            'monitoring_plan': self.monitoring_plan,
            'confidence_level': self.confidence_level,
            'processing_time': self.processing_time,
            'assessment_date': self.assessment_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }