#!/usr/bin/env python3
"""
Triage Agent - Assesses urgency and recommends actions
Simple implementation that students can build upon
"""

from .base_agent import BaseAgent
import logging
import json
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class TriageAgent(BaseAgent):
    """
    Triage Agent assesses patient urgency and recommends appropriate actions
    This is a barebones implementation - students should enhance it
    """
    
    def __init__(self, knowledge_store, patient_db):
        super().__init__(knowledge_store, patient_db, "triage")
    
    def assess_urgency(self, patient_id: str, symptoms: List[Dict], patient_context: Dict) -> Dict[str, Any]:
        """
        Assess urgency level based on symptoms and patient context
        TODO for students: Implement sophisticated medical scoring algorithms
        """
        try:
            # Calculate base urgency score
            base_score = self._calculate_base_urgency(symptoms)
            
            # Apply modifiers based on patient context
            modified_score = self._apply_context_modifiers(base_score, patient_context)
            
            # Determine urgency level and recommended action
            urgency_level = self._get_urgency_level(modified_score)
            recommended_action = self._get_recommended_action(modified_score, symptoms)
            
            # Generate reasoning
            reasoning = self._generate_reasoning(symptoms, patient_context, modified_score)
            
            # Log triage decision
            self._log_interaction(
                patient_id, 
                'urgency_assessment',
                {'symptoms': len(symptoms), 'context': patient_context.keys()},
                {'urgency_score': modified_score, 'level': urgency_level}
            )
            
            return {
                'urgency_score': min(10, max(1, modified_score)),  # Clamp between 1-10
                'urgency_level': urgency_level,
                'recommended_action': recommended_action,
                'reasoning': reasoning,
                'timestamp': self._format_medical_response('', {})['timestamp']
            }
            
        except Exception as e:
            logger.error(f"Triage assessment failed: {str(e)}")
            return {
                'urgency_score': 5,  # Default moderate urgency
                'urgency_level': 'moderate',
                'recommended_action': 'Contact healthcare provider within 24 hours',
                'reasoning': 'Assessment system error - defaulting to moderate urgency',
                'error': str(e)
            }
    
    def _calculate_base_urgency(self, symptoms: List[Dict]) -> int:
        """
        Calculate base urgency score from symptoms
        TODO for students: Use actual medical protocols and scoring systems
        """
        if not symptoms:
            return 2  # Low urgency for no specific symptoms
        
        # Simple scoring based on keyword severity
        high_urgency_symptoms = ['chest pain', 'shortness of breath', 'severe pain', 'bleeding']
        medium_urgency_symptoms = ['fever', 'nausea', 'headache', 'dizzy']
        
        base_score = 3  # Default moderate
        
        for symptom in symptoms:
            symptom_name = symptom.get('name', '').lower()
            
            # Check for high urgency symptoms
            if any(urgent in symptom_name for urgent in high_urgency_symptoms):
                base_score += 3
            elif any(medium in symptom_name for medium in medium_urgency_symptoms):
                base_score += 1
        
        return base_score
    
    def _apply_context_modifiers(self, base_score: int, patient_context: Dict) -> int:
        """
        Apply modifiers based on patient age, medical history, etc.
        TODO for students: Add comprehensive risk factor analysis
        """
        modified_score = base_score
        
        # Age modifiers (simplified)
        age = patient_context.get('age')
        if age:
            if age > 65:
                modified_score += 1  # Elderly patients higher risk
            elif age < 2:
                modified_score += 2  # Infants higher risk
        
        # Medical history modifiers
        medical_history = patient_context.get('medical_history', {})
        high_risk_conditions = ['diabetes', 'heart disease', 'hypertension']
        
        for condition in high_risk_conditions:
            if condition in str(medical_history).lower():
                modified_score += 1
        
        # Urgency indicators from intake
        urgency_indicators = patient_context.get('urgency_indicators', {})
        if urgency_indicators.get('urgency_level') == 'high':
            modified_score += 2
        
        return modified_score
    
    def _get_urgency_level(self, score: int) -> str:
        """
        Convert numeric score to urgency level
        TODO for students: Align with hospital triage protocols
        """
        if score >= 8:
            return 'critical'
        elif score >= 6:
            return 'high'
        elif score >= 4:
            return 'moderate'
        elif score >= 2:
            return 'low'
        else:
            return 'minimal'
    
    def _get_recommended_action(self, score: int, symptoms: List[Dict]) -> str:
        """
        Get recommended action based on urgency score
        TODO for students: Implement evidence-based action protocols
        """
        urgency_level = self._get_urgency_level(score)
        
        actions = {
            'critical': 'Call 911 immediately or go to emergency room',
            'high': 'Seek immediate medical attention within 2 hours',
            'moderate': 'Contact healthcare provider within 24 hours',
            'low': 'Schedule appointment within 1-2 weeks',
            'minimal': 'Monitor symptoms and consider self-care measures'
        }
        
        return actions.get(urgency_level, 'Consult healthcare provider')
    
    def _generate_reasoning(self, symptoms: List[Dict], patient_context: Dict, score: int) -> str:
        """
        Generate human-readable reasoning for triage decision
        TODO for students: Make more detailed and medically accurate
        """
        reasoning_parts = []
        
        # Symptom-based reasoning
        if symptoms:
            symptom_names = [s.get('name', 'unknown') for s in symptoms]
            reasoning_parts.append(f"Based on reported symptoms: {', '.join(symptom_names[:3])}")
        
        # Context-based reasoning
        if score >= 6:
            reasoning_parts.append("Elevated concern due to symptom severity")
        
        urgency_indicators = patient_context.get('urgency_indicators', {})
        if urgency_indicators.get('high_urgency_indicators', 0) > 0:
            reasoning_parts.append("High-urgency language detected in patient description")
        
        # Age or history factors
        if patient_context.get('age', 0) > 65:
            reasoning_parts.append("Age factor increases risk level")
        
        if not reasoning_parts:
            reasoning_parts.append("Standard assessment based on presented information")
        
        return ". ".join(reasoning_parts) + "."
    
    def get_triage_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about triage decisions
        TODO for students: Add comprehensive analytics
        """
        try:
            stats = self.patient_db.get_triage_stats(days=7)
            return stats
        except Exception as e:
            logger.error(f"Failed to get triage statistics: {str(e)}")
            return {'error': str(e)}
    
    def validate_triage_decision(self, urgency_score: int, symptoms: List[Dict]) -> Dict[str, Any]:
        """
        Validate triage decision for quality assurance
        TODO for students: Add medical validation rules
        """
        warnings = []
        
        # Check for score-symptom mismatches
        if urgency_score >= 8 and len(symptoms) == 0:
            warnings.append("High urgency score with no documented symptoms")
        
        # Check for dangerous symptom combinations
        symptom_names = [s.get('name', '').lower() for s in symptoms]
        if 'chest pain' in ' '.join(symptom_names) and urgency_score < 6:
            warnings.append("Chest pain reported but urgency score may be too low")
        
        return {
            'valid': len(warnings) == 0,
            'warnings': warnings,
            'confidence': 0.8 if len(warnings) == 0 else 0.5
        }