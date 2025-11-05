#!/usr/bin/env python3
"""
Escalation Agent - Manages handoffs to human providers
Simple implementation that students can build upon
"""

from .base_agent import BaseAgent
import logging
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class EscalationAgent(BaseAgent):
    """
    Escalation Agent manages patient handoffs to healthcare providers
    This is a barebones implementation - students should enhance it
    """
    
    def __init__(self, knowledge_store, patient_db):
        super().__init__(knowledge_store, patient_db, "escalation")
    
    def check_escalation_needed(self, urgency_score: int, symptoms: List[Dict], 
                               patient_context: Dict = None) -> Dict[str, Any]:
        """
        Determine if escalation to human provider is needed
        TODO for students: Implement sophisticated escalation logic
        """
        try:
            # Check urgency-based escalation
            urgency_escalation = self._check_urgency_escalation(urgency_score)
            
            # Check symptom-based escalation
            symptom_escalation = self._check_symptom_escalation(symptoms)
            
            # Check context-based escalation
            context_escalation = self._check_context_escalation(patient_context or {})
            
            # Determine overall escalation need
            escalation_required = (
                urgency_escalation['required'] or 
                symptom_escalation['required'] or 
                context_escalation['required']
            )
            
            # Determine escalation level
            escalation_level = self._determine_escalation_level(
                urgency_escalation, symptom_escalation, context_escalation
            )
            
            # Get escalation instructions
            instructions = self._get_escalation_instructions(escalation_level, symptoms)
            
            return {
                'required': escalation_required,
                'level': escalation_level,
                'reasons': {
                    'urgency': urgency_escalation,
                    'symptoms': symptom_escalation,
                    'context': context_escalation
                },
                'instructions': instructions,
                'estimated_wait_time': self._estimate_wait_time(escalation_level),
                'provider_type': self._determine_provider_type(escalation_level, symptoms)
            }
            
        except Exception as e:
            logger.error(f"Escalation check failed: {str(e)}")
            return {
                'required': True,  # Default to safe escalation
                'level': 'urgent',
                'reasons': {'error': str(e)},
                'instructions': 'System error - please contact healthcare provider',
                'estimated_wait_time': 'unknown'
            }
    
    def _check_urgency_escalation(self, urgency_score: int) -> Dict[str, Any]:
        """
        Check if urgency score triggers escalation
        TODO for students: Implement hospital-specific thresholds
        """
        if urgency_score >= 8:
            return {
                'required': True,
                'reason': f'Critical urgency score: {urgency_score}/10',
                'priority': 'immediate'
            }
        elif urgency_score >= 6:
            return {
                'required': True,
                'reason': f'High urgency score: {urgency_score}/10',
                'priority': 'urgent'
            }
        else:
            return {
                'required': False,
                'reason': f'Moderate urgency score: {urgency_score}/10',
                'priority': 'routine'
            }
    
    def _check_symptom_escalation(self, symptoms: List[Dict]) -> Dict[str, Any]:
        """
        Check if specific symptoms trigger escalation
        TODO for students: Use comprehensive medical escalation protocols
        """
        high_priority_symptoms = [
            'chest pain', 'shortness of breath', 'severe pain', 
            'difficulty breathing', 'stroke symptoms', 'heart attack'
        ]
        
        escalation_symptoms = []
        for symptom in symptoms:
            symptom_name = symptom.get('name', '').lower()
            if any(priority in symptom_name for priority in high_priority_symptoms):
                escalation_symptoms.append(symptom_name)
        
        if escalation_symptoms:
            return {
                'required': True,
                'reason': f'High-priority symptoms detected: {", ".join(escalation_symptoms)}',
                'symptoms': escalation_symptoms
            }
        else:
            return {
                'required': False,
                'reason': 'No high-priority symptoms detected',
                'symptoms': []
            }
    
    def _check_context_escalation(self, patient_context: Dict) -> Dict[str, Any]:
        """
        Check if patient context triggers escalation
        TODO for students: Add comprehensive risk factor analysis
        """
        escalation_factors = []
        
        # Age-based escalation
        age = patient_context.get('age')
        if age and (age < 2 or age > 75):
            escalation_factors.append(f'Age factor: {age} years')
        
        # Medical history escalation
        medical_history = patient_context.get('medical_history', {})
        high_risk_conditions = ['heart disease', 'diabetes', 'cancer', 'immunocompromised']
        
        for condition in high_risk_conditions:
            if condition in str(medical_history).lower():
                escalation_factors.append(f'High-risk condition: {condition}')
        
        # Multiple symptoms
        symptoms_count = len(patient_context.get('symptoms', []))
        if symptoms_count >= 5:
            escalation_factors.append(f'Multiple symptoms: {symptoms_count}')
        
        if escalation_factors:
            return {
                'required': True,
                'reason': f'Context factors: {"; ".join(escalation_factors)}',
                'factors': escalation_factors
            }
        else:
            return {
                'required': False,
                'reason': 'No high-risk context factors',
                'factors': []
            }
    
    def _determine_escalation_level(self, urgency: Dict, symptoms: Dict, context: Dict) -> str:
        """
        Determine overall escalation level
        TODO for students: Implement weighted scoring system
        """
        if urgency.get('priority') == 'immediate' or any('chest pain' in str(symptoms).lower() for _ in [1]):
            return 'emergency'
        elif urgency.get('priority') == 'urgent' or symptoms.get('required'):
            return 'urgent'
        elif context.get('required'):
            return 'priority'
        else:
            return 'routine'
    
    def _get_escalation_instructions(self, level: str, symptoms: List[Dict]) -> List[str]:
        """
        Get specific instructions for escalation level
        TODO for students: Create detailed protocol-based instructions
        """
        instructions = {
            'emergency': [
                'Call 911 immediately',
                'Do not drive yourself to the hospital',
                'Stay on the line with emergency dispatcher',
                'Have someone stay with you if possible'
            ],
            'urgent': [
                'Go to the nearest emergency department',
                'Call ahead if possible to notify them',
                'Bring your medication list and ID',
                'Have someone drive you or call an ambulance'
            ],
            'priority': [
                'Contact your primary care provider today',
                'If unavailable, consider urgent care',
                'Monitor symptoms closely',
                'Seek immediate care if symptoms worsen'
            ],
            'routine': [
                'Schedule appointment with healthcare provider',
                'Continue current care if any',
                'Call if symptoms worsen',
                'Follow up within recommended timeframe'
            ]
        }
        
        return instructions.get(level, instructions['routine'])
    
    def _estimate_wait_time(self, level: str) -> str:
        """
        Estimate wait time for different escalation levels
        TODO for students: Connect to real-time hospital data
        """
        wait_times = {
            'emergency': 'Immediate',
            'urgent': '30-60 minutes',
            'priority': '2-4 hours',
            'routine': '1-3 days'
        }
        
        return wait_times.get(level, 'Unknown')
    
    def _determine_provider_type(self, level: str, symptoms: List[Dict]) -> str:
        """
        Determine appropriate provider type
        TODO for students: Add specialty-specific routing
        """
        symptom_names = ' '.join([s.get('name', '') for s in symptoms]).lower()
        
        if level in ['emergency', 'urgent']:
            if 'chest pain' in symptom_names or 'heart' in symptom_names:
                return 'Emergency Department (Cardiology)'
            elif 'breathing' in symptom_names or 'breath' in symptom_names:
                return 'Emergency Department (Pulmonology)'
            else:
                return 'Emergency Department'
        elif level == 'priority':
            return 'Urgent Care or Primary Care'
        else:
            return 'Primary Care Provider'
    
    def create_handoff_summary(self, patient_id: str, escalation_info: Dict) -> Dict[str, Any]:
        """
        Create summary for provider handoff
        TODO for students: Generate comprehensive clinical handoff
        """
        try:
            # Get patient history
            history = self.patient_db.get_patient_history(patient_id, limit=5)
            
            # Extract key information
            symptoms_summary = []
            triage_scores = []
            
            for conversation in history:
                ai_response = conversation.get('ai_response', {})
                if 'extracted_symptoms' in ai_response:
                    symptoms = ai_response['extracted_symptoms']
                    symptoms_summary.extend([s.get('name', '') for s in symptoms])
                
                if 'urgency_assessment' in ai_response:
                    score = ai_response['urgency_assessment'].get('score', 0)
                    triage_scores.append(score)
            
            return {
                'patient_id': patient_id,
                'escalation_level': escalation_info.get('level', 'unknown'),
                'chief_complaint': list(set(symptoms_summary))[:5],
                'urgency_trend': triage_scores,
                'escalation_reason': escalation_info.get('instructions', ['No specific reason']),
                'interaction_count': len(history),
                'handoff_time': datetime.now().isoformat(),
                'recommended_provider': escalation_info.get('provider_type', 'Primary Care')
            }
            
        except Exception as e:
            logger.error(f"Failed to create handoff summary: {str(e)}")
            return {
                'patient_id': patient_id,
                'error': str(e),
                'handoff_time': datetime.now().isoformat()
            }
    
    def track_escalation_outcome(self, patient_id: str, outcome: str, 
                                provider_feedback: str = None) -> Dict[str, Any]:
        """
        Track outcomes of escalation decisions
        TODO for students: Implement feedback loop for system improvement
        """
        try:
            outcome_data = {
                'patient_id': patient_id,
                'outcome': outcome,  # 'appropriate', 'unnecessary', 'delayed', etc.
                'provider_feedback': provider_feedback,
                'timestamp': datetime.now().isoformat()
            }
            
            # Log outcome for quality improvement
            self.patient_db.log_audit_event(
                patient_id=patient_id,
                action='escalation_outcome',
                details=json.dumps(outcome_data)
            )
            
            return {
                'success': True,
                'message': 'Escalation outcome recorded',
                'data': outcome_data
            }
            
        except Exception as e:
            logger.error(f"Failed to track escalation outcome: {str(e)}")
            return {'success': False, 'error': str(e)}