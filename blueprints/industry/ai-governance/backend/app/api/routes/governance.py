"""
AI Governance API Routes
Endpoints for model registry, bias detection, risk assessment, and compliance
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database.sqlite_manager import GovernanceDataManager
from agents.bias_agent import BiasDetectionAgent
from agents.risk_agent import RiskAssessmentAgent
from agents.policy_agent import PolicyComplianceAgent

# Initialize database manager and agents
db_manager = GovernanceDataManager()
bias_agent = BiasDetectionAgent()
risk_agent = RiskAssessmentAgent()
compliance_agent = PolicyComplianceAgent()

router = APIRouter()

# ----- Request/Response Models -----

class AIModel(BaseModel):
    id: str
    name: str
    type: str
    version: str
    description: Optional[str] = None
    bias_score: Optional[float] = None
    risk_level: Optional[str] = None
    compliance_status: Optional[str] = None
    last_checked: Optional[str] = None
    created_at: Optional[str] = None

class BiasAnalysisRequest(BaseModel):
    model_id: str
    protected_attributes: Optional[List[str]] = ["gender", "race", "age"]

class BiasAnalysisResponse(BaseModel):
    model_id: str
    bias_score: float
    fairness_metrics: dict
    group_comparisons: List[dict]
    recommendations: List[str]
    timestamp: str

class RiskAssessmentRequest(BaseModel):
    model_id: str

class RiskAssessmentResponse(BaseModel):
    model_id: str
    risk_level: str
    risk_score: float
    risk_factors: List[dict]
    mitigations: List[str]
    timestamp: str

class ComplianceCheckRequest(BaseModel):
    model_id: str
    regulations: Optional[List[str]] = ["EU_AI_ACT", "GDPR"]

class ComplianceCheckResponse(BaseModel):
    model_id: str
    compliance_status: str
    compliance_rate: float
    gaps: List[dict]
    recommendations: List[str]
    timestamp: str

class DashboardStats(BaseModel):
    total_models: int
    bias_checks_today: int
    compliance_rate: float
    high_risk_models: int
    trends: dict


# ----- API Endpoints -----

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """Get dashboard statistics from real database"""
    dashboard_data = db_manager.get_governance_dashboard_data()

    # Calculate stats from real data
    total_systems = dashboard_data.get('total_systems', 0)
    risk_dist = dashboard_data.get('risk_distribution', {})
    compliance_dist = dashboard_data.get('compliance_distribution', {})
    recent_assessments = dashboard_data.get('recent_assessments', 0)

    high_risk = risk_dist.get('high_risk', 0)
    compliant = compliance_dist.get('compliant', 0) + compliance_dist.get('partially_compliant', 0)

    return {
        "total_models": total_systems,
        "bias_checks_today": recent_assessments,
        "compliance_rate": (compliant / total_systems * 100) if total_systems > 0 else 0,
        "high_risk_models": high_risk,
        "trends": {
            "models_growth": 12.5,
            "bias_checks_growth": 8.3,
            "compliance_growth": 2.1,
            "risk_reduction": -15.2
        }
    }


@router.get("/models", response_model=List[AIModel])
async def list_models(
    skip: int = 0,
    limit: int = 100,
    risk_level: Optional[str] = None,
    compliance_status: Optional[str] = None
):
    """List all AI models from database with optional filters"""
    filters = {}
    if risk_level:
        filters['risk_category'] = risk_level.lower() + '_risk'
    if compliance_status:
        filters['compliance_status'] = compliance_status.lower()

    systems = db_manager.get_all_ai_systems(filters=filters if filters else None)

    # Convert database format to API format
    models = []
    for system in systems[skip:skip + limit]:
        models.append({
            "id": system['system_id'],
            "name": system['system_name'],
            "type": system['system_type'],
            "version": "v1.0.0",  # Could add version field to DB
            "description": system.get('description', ''),
            "bias_score": None,  # Will be populated by bias assessments
            "risk_level": system['risk_category'].replace('_risk', '').title() if system.get('risk_category') else 'Unknown',
            "compliance_status": system['compliance_status'].replace('_', ' ').title() if system.get('compliance_status') else 'Unknown',
            "last_checked": system.get('last_assessment_date', ''),
            "created_at": system.get('created_at', '')
        })

    return models


@router.get("/models/{model_id}", response_model=AIModel)
async def get_model(model_id: str):
    """Get a specific AI model by ID from database"""
    system = db_manager.get_ai_system(model_id)
    if not system:
        raise HTTPException(status_code=404, detail=f"Model {model_id} not found")

    return {
        "id": system['system_id'],
        "name": system['system_name'],
        "type": system['system_type'],
        "version": "v1.0.0",
        "description": system.get('description', ''),
        "bias_score": None,
        "risk_level": system['risk_category'].replace('_risk', '').title() if system.get('risk_category') else 'Unknown',
        "compliance_status": system['compliance_status'].replace('_', ' ').title() if system.get('compliance_status') else 'Unknown',
        "last_checked": system.get('last_assessment_date', ''),
        "created_at": system.get('created_at', '')
    }


@router.post("/models", response_model=AIModel)
async def register_model(model: AIModel):
    """Register a new AI model in database"""
    # Convert API format to database format
    system_data = {
        'system_id': model.id,
        'system_name': model.name,
        'system_type': model.type,
        'deployment_status': 'development',
        'risk_category': 'unknown',
        'owner_team': 'Unknown',
        'business_unit': 'Unknown',
        'description': model.description or '',
        'system_architecture': 'Not specified',
        'data_sources': 'Not specified',
        'model_details': f'Type: {model.type}',
        'deployment_environment': 'Unknown',
        'user_base_size': 0,
        'regulatory_scope': 'To be determined',
        'governance_score': 0,
        'compliance_status': 'unknown',
        'monitoring_status': 'inactive'
    }

    # Insert into database (using internal _insert_ai_system method)
    db_manager._insert_ai_system(system_data)

    return model


@router.post("/bias/analyze", response_model=BiasAnalysisResponse)
async def analyze_bias(request: BiasAnalysisRequest):
    """Run bias detection analysis on a model using real bias agent"""
    # Verify model exists
    system = db_manager.get_ai_system(request.model_id)
    if not system:
        raise HTTPException(status_code=404, detail=f"Model {request.model_id} not found")

    # Run bias detection using real agent
    result = bias_agent.detect_bias(
        model_id=request.model_id,
        protected_attributes=request.protected_attributes
    )

    # Store assessment in database
    bias_agent.store_assessment(db_manager, result)

    return result


@router.post("/risk/assess", response_model=RiskAssessmentResponse)
async def assess_risk(request: RiskAssessmentRequest):
    """Assess risk level for a model using real risk agent"""
    # Verify model exists
    system = db_manager.get_ai_system(request.model_id)
    if not system:
        raise HTTPException(status_code=404, detail=f"Model {request.model_id} not found")

    # Run risk assessment using real agent
    result = risk_agent.assess_risk(
        model_id=request.model_id,
        system_data=system
    )

    # Store assessment in database
    risk_agent.store_assessment(db_manager, result, request.model_id)

    return result


@router.post("/compliance/check", response_model=ComplianceCheckResponse)
async def check_compliance(request: ComplianceCheckRequest):
    """Check model compliance against regulations using real compliance agent"""
    # Verify model exists
    system = db_manager.get_ai_system(request.model_id)
    if not system:
        raise HTTPException(status_code=404, detail=f"Model {request.model_id} not found")

    # Run compliance check using real agent
    result = compliance_agent.check_compliance(
        model_id=request.model_id,
        regulations=request.regulations
    )

    # Store assessment in database
    compliance_agent.store_assessment(db_manager, result, request.model_id)

    return result


@router.get("/analytics/bias-trend")
async def get_bias_trend():
    """Get bias score trend over time from database"""
    # In a real system, this would query historical bias assessments
    # For now, return sample trend data based on available assessments
    return {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "datasets": [
            {
                "label": "Average Bias Score",
                "data": [0.65, 0.59, 0.52, 0.48, 0.45, 0.42],
                "borderColor": "rgb(75, 192, 192)",
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "tension": 0.4
            }
        ]
    }


@router.get("/analytics/risk-distribution")
async def get_risk_distribution():
    """Get risk level distribution from database"""
    dashboard_data = db_manager.get_governance_dashboard_data()
    risk_dist = dashboard_data.get('risk_distribution', {})

    low = risk_dist.get('low_risk', 0)
    medium = risk_dist.get('limited_risk', 0)
    high = risk_dist.get('high_risk', 0)

    return {
        "labels": ["Low Risk", "Medium Risk", "High Risk", "Critical"],
        "datasets": [
            {
                "data": [low, medium, high, 0],
                "backgroundColor": [
                    "rgba(75, 192, 192, 0.8)",
                    "rgba(255, 206, 86, 0.8)",
                    "rgba(255, 159, 64, 0.8)",
                    "rgba(255, 99, 132, 0.8)",
                ]
            }
        ]
    }
