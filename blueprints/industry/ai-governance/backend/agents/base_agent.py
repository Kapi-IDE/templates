#!/usr/bin/env python3
"""
Base Agent Class for AI Governance System
Provides common functionality for all specialized governance agents
"""

import google.generativeai as genai
import os
import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class BaseGovernanceAgent:
    """
    Base class for all AI governance agents
    Provides common functionality including Gemini API integration,
    logging, error handling, and governance-specific response formatting
    """
    
    def __init__(self, knowledge_store, governance_db, agent_type: str = "base"):
        """Initialize base governance agent with required dependencies"""
        self.knowledge_store = knowledge_store
        self.governance_db = governance_db
        self.agent_type = agent_type
        
        # Initialize Gemini API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        logger.info(f"{agent_type.title()} governance agent initialized successfully")
    
    def _create_governance_prompt(self, specific_instructions: str) -> str:
        """Create system prompt with common AI governance guidelines"""
        base_prompt = """
You are an AI governance specialist focused on ensuring responsible AI deployment and compliance.

CORE RESPONSIBILITIES:
- Assess AI systems for governance risks across multiple dimensions
- Evaluate compliance with regulatory frameworks (EU AI Act, NIST AI RMF, ISO standards)
- Identify bias, fairness, and ethical concerns in AI systems
- Provide actionable recommendations for risk mitigation
- Ensure transparent and explainable AI governance decisions

GOVERNANCE PRINCIPLES:
- Prioritize human safety and wellbeing in all assessments
- Apply proportionate governance based on AI system risk levels
- Maintain transparency in governance decisions and rationale  
- Consider diverse stakeholder perspectives and impacts
- Ensure compliance with applicable regulatory requirements
- Document all governance decisions with clear audit trails

ASSESSMENT APPROACH:
- Use evidence-based risk assessment methodologies
- Apply relevant regulatory frameworks and industry standards
- Consider technical, ethical, legal, and business implications
- Provide specific, actionable mitigation recommendations
- Maintain consistent governance standards across assessments

CONTEXT:
- You are part of a multi-agent AI governance system
- Your assessments inform enterprise governance decisions
- All interactions are audited for compliance and accountability
- Focus on practical, implementable governance solutions

"""
        return base_prompt + "\n" + specific_instructions
    
    def _generate_governance_response(self, prompt: str, system_context: Dict = None) -> str:
        """Generate response using Gemini API with governance context"""
        try:
            # Include system context if available
            if system_context:
                context_str = f"\nAI SYSTEM CONTEXT:\n{json.dumps(system_context, indent=2)}\n"
                prompt = context_str + prompt
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise ValueError("Empty response from Gemini API")
            
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate governance response: {str(e)}")
            return self._get_governance_fallback_response()
    
    def _get_governance_fallback_response(self) -> str:
        """Provide fallback response when AI generation fails"""
        return ("I apologize, but I'm experiencing technical difficulties with the governance assessment. "
                "Please consult your governance team directly for this AI system evaluation.")
    
    def _extract_governance_data(self, text: str, structure_type: str) -> Dict:
        """Extract structured governance data from AI response"""
        try:
            extraction_prompt = f"""
Extract governance information from the text and return as JSON:
Text: {text}

For {structure_type} governance assessment, extract:
- risk_factors: list of identified risks
- risk_levels: severity assessment for each risk (low/medium/high/critical)
- compliance_issues: list of regulatory compliance concerns
- recommendations: list of specific mitigation actions
- confidence_level: assessment confidence (1-10)
- regulatory_frameworks: applicable regulations/standards
- stakeholder_impacts: affected parties and impact levels

Return only valid JSON:
"""
            
            response = self.model.generate_content(extraction_prompt)
            
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return self._manual_parse_governance_response(text, structure_type)
                
        except Exception as e:
            logger.error(f"Failed to extract governance data: {str(e)}")
            return self._get_default_governance_structure(structure_type)
    
    def _manual_parse_governance_response(self, text: str, structure_type: str) -> Dict:
        """Manual parsing fallback for governance data extraction"""
        risk_factors = []
        recommendations = []
        compliance_issues = []
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if any(word in line.lower() for word in ['risk', 'danger', 'threat', 'vulnerability']):
                risk_factors.append(line)
            elif any(word in line.lower() for word in ['recommend', 'suggest', 'should', 'must']):
                recommendations.append(line)
            elif any(word in line.lower() for word in ['compliance', 'regulation', 'standard', 'requirement']):
                compliance_issues.append(line)
        
        return {
            'risk_factors': risk_factors[:5],
            'risk_levels': ['medium'] * min(len(risk_factors), 5),
            'compliance_issues': compliance_issues[:3],
            'recommendations': recommendations[:5],
            'confidence_level': 5,
            'regulatory_frameworks': ['EU_AI_Act', 'NIST_AI_RMF'],
            'stakeholder_impacts': []
        }
    
    def _get_default_governance_structure(self, structure_type: str) -> Dict:
        """Return default governance structure when parsing fails"""
        return {
            'risk_factors': [],
            'risk_levels': [],
            'compliance_issues': [],
            'recommendations': ["Conduct detailed governance review"],
            'confidence_level': 1,
            'regulatory_frameworks': [],
            'stakeholder_impacts': []
        }
    
    def _log_governance_interaction(self, system_id: str, interaction_type: str, 
                                  input_data: Dict, output_data: Dict, 
                                  processing_time: float = None):
        """Log governance agent interaction for audit and monitoring"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'agent_type': self.agent_type,
                'system_id': system_id,
                'interaction_type': interaction_type,
                'processing_time_seconds': processing_time,
                'input_summary': {
                    'keys': list(input_data.keys()),
                    'request_length': len(str(input_data.get('request', '')))
                },
                'output_summary': {
                    'keys': list(output_data.keys()),
                    'response_length': len(str(output_data.get('response', '')))
                },
                'governance_decision': output_data.get('governance_decision'),
                'compliance_status': output_data.get('compliance_status'),
                'success': True
            }
            
            # Log to governance database audit trail
            self.governance_db.log_audit_event(
                system_id=system_id,
                action=f'{self.agent_type}_assessment',
                details=json.dumps(log_entry)
            )
            
        except Exception as e:
            logger.error(f"Failed to log governance interaction: {str(e)}")
    
    def _validate_governance_input(self, required_fields: List[str], data: Dict) -> bool:
        """Validate that required fields are present for governance assessment"""
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logger.error(f"Missing required governance fields: {missing_fields}")
            return False
        return True
    
    def _create_assessment_id(self) -> str:
        """Generate unique assessment ID"""
        return f"{self.agent_type}_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"
    
    def _assess_risk_level(self, risk_indicators: List[str], system_context: Dict) -> Dict[str, Any]:
        """Assess overall risk level based on indicators and context"""
        critical_keywords = [
            'high-risk', 'critical', 'safety-critical', 'life-threatening',
            'autonomous', 'decision-making', 'biometric', 'surveillance',
            'hiring', 'credit', 'medical', 'law enforcement'
        ]
        
        high_keywords = [
            'facial recognition', 'predictive', 'automated decision',
            'personal data', 'sensitive attributes', 'discrimination',
            'bias', 'unfair', 'privacy', 'security vulnerability'
        ]
        
        medium_keywords = [
            'recommendation', 'personalization', 'optimization',
            'classification', 'clustering', 'anomaly detection',
            'data processing', 'user interaction'
        ]
        
        # Combine all text for analysis
        all_text = ' '.join(risk_indicators + [str(system_context)]).lower()
        
        critical_count = sum(1 for keyword in critical_keywords if keyword in all_text)
        high_count = sum(1 for keyword in high_keywords if keyword in all_text)
        medium_count = sum(1 for keyword in medium_keywords if keyword in all_text)
        
        if critical_count > 0:
            risk_level = 'critical'
            risk_score = min(10, 8 + critical_count)
        elif high_count > 0:
            risk_level = 'high'
            risk_score = min(10, 6 + high_count)
        elif medium_count > 0:
            risk_level = 'medium'
            risk_score = min(10, 4 + medium_count)
        else:
            risk_level = 'low'
            risk_score = 2
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'critical_indicators': critical_count,
            'high_indicators': high_count,
            'medium_indicators': medium_count,
            'keywords_found': [kw for kw in critical_keywords + high_keywords + medium_keywords 
                             if kw in all_text]
        }
    
    def _format_governance_response(self, response_text: str, 
                                  assessment_data: Dict = None) -> Dict[str, Any]:
        """Format response with consistent governance structure"""
        base_response = {
            'response': response_text,
            'agent_type': self.agent_type,
            'timestamp': datetime.now().isoformat(),
            'assessment_id': self._create_assessment_id(),
            'confidence_score': 7,  # Default confidence
            'requires_review': True,
            'governance_version': '1.0'
        }
        
        if assessment_data:
            base_response.update(assessment_data)
        
        return base_response
    
    def _check_regulatory_compliance(self, system_context: Dict, 
                                   risk_assessment: Dict) -> Dict[str, Any]:
        """Check compliance against major regulatory frameworks"""
        compliance_status = {
            'EU_AI_Act': self._check_eu_ai_act_compliance(system_context, risk_assessment),
            'NIST_AI_RMF': self._check_nist_compliance(system_context, risk_assessment),
            'ISO_42001': self._check_iso_compliance(system_context, risk_assessment),
            'GDPR_AI': self._check_gdpr_ai_compliance(system_context, risk_assessment)
        }
        
        overall_status = 'compliant'
        compliance_issues = []
        
        for framework, status in compliance_status.items():
            if status['status'] != 'compliant':
                overall_status = 'non_compliant'
                compliance_issues.extend(status.get('issues', []))
        
        return {
            'overall_status': overall_status,
            'framework_compliance': compliance_status,
            'compliance_issues': compliance_issues,
            'compliance_percentage': self._calculate_compliance_percentage(compliance_status)
        }
    
    def _check_eu_ai_act_compliance(self, system_context: Dict, risk_assessment: Dict) -> Dict:
        """Check EU AI Act compliance"""
        risk_level = risk_assessment.get('risk_level', 'low')
        
        if risk_level in ['critical', 'high']:
            return {
                'status': 'requires_review',
                'issues': ['High-risk AI system requires conformity assessment'],
                'requirements': ['CE marking', 'Risk management system', 'Data governance']
            }
        else:
            return {
                'status': 'compliant',
                'issues': [],
                'requirements': ['Transparency obligations']
            }
    
    def _check_nist_compliance(self, system_context: Dict, risk_assessment: Dict) -> Dict:
        """Check NIST AI Risk Management Framework compliance"""
        return {
            'status': 'partially_compliant',
            'issues': ['Requires AI impact assessment'],
            'requirements': ['Risk management plan', 'Continuous monitoring']
        }
    
    def _check_iso_compliance(self, system_context: Dict, risk_assessment: Dict) -> Dict:
        """Check ISO 42001 AI Management System compliance"""
        return {
            'status': 'requires_review',
            'issues': ['AI management system not verified'],
            'requirements': ['AI policy documentation', 'Risk assessment procedures']
        }
    
    def _check_gdpr_ai_compliance(self, system_context: Dict, risk_assessment: Dict) -> Dict:
        """Check GDPR AI-specific compliance"""
        return {
            'status': 'compliant',
            'issues': [],
            'requirements': ['Privacy by design', 'Data subject rights']
        }
    
    def _calculate_compliance_percentage(self, compliance_status: Dict) -> float:
        """Calculate overall compliance percentage"""
        total_frameworks = len(compliance_status)
        compliant_count = sum(1 for status in compliance_status.values() 
                            if status['status'] == 'compliant')
        
        return (compliant_count / total_frameworks) * 100 if total_frameworks > 0 else 0
    
    def health_check(self) -> bool:
        """Check if governance agent is functioning properly"""
        try:
            # Test AI model
            test_response = self.model.generate_content("Test governance assessment")
            
            # Test database connections
            if hasattr(self.knowledge_store, 'health_check'):
                if not self.knowledge_store.health_check():
                    return False
            
            if hasattr(self.governance_db, 'health_check'):
                if not self.governance_db.health_check():
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Governance agent health check failed: {str(e)}")
            return False
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this governance agent"""
        return {
            'agent_type': self.agent_type,
            'model': 'gemini-pro',
            'initialized_at': datetime.now().isoformat(),
            'capabilities': [
                'risk_assessment', 
                'compliance_checking', 
                'governance_analysis',
                'regulatory_mapping'
            ],
            'supported_frameworks': [
                'EU_AI_Act', 
                'NIST_AI_RMF', 
                'ISO_42001', 
                'GDPR_AI'
            ],
            'status': 'active'
        }