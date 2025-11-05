#!/usr/bin/env python3
"""
Intake Agent - Collects patient symptoms and medical history
Simple implementation that students can build upon
"""

from .base_agent import BaseAgent
import logging
from typing import Dict, Any
import json

logger = logging.getLogger(__name__)

class IntakeAgent(BaseAgent):
    """
    Intake Agent handles initial patient interaction and symptom collection
    This is a barebones implementation - students should enhance it
    """
    
    def __init__(self, knowledge_store, patient_db):
        super().__init__(knowledge_store, patient_db, "intake")
    
    def process_message(self, patient_id: str, message: str, context: Dict = None) -> Dict[str, Any]:
        """
        Process patient message and extract symptoms
        TODO for students: Enhance with better NLP and follow-up logic
        """
        try:
            # Create system prompt for medical intake
            system_prompt = self._create_system_prompt("""
            You are a compassionate medical intake specialist. Your role is to:
            
            1. Listen to patient symptoms with empathy
            2. Ask ONE specific follow-up question to better understand their condition
            3. Extract key symptoms mentioned
            4. Identify any urgency indicators
            
            Keep responses warm, professional, and focused on gathering information.
            Never provide medical diagnoses - only ask clarifying questions.
            """)
            
            # Combine system prompt with patient message
            full_prompt = f"{system_prompt}\n\nPatient says: \"{message}\"\n\nProvide a caring response with ONE follow-up question:"
            
            # Generate response using Gemini
            ai_response = self._generate_response(full_prompt, context)
            
            # Extract symptoms (basic implementation)
            symptoms = self._extract_symptoms(message)
            
            # Assess urgency indicators
            urgency_indicators = self._assess_urgency_indicators(message)
            
            # Create patient context for next agents
            patient_context = {
                'patient_id': patient_id,
                'symptoms': symptoms,
                'urgency_indicators': urgency_indicators,
                'medical_history': context.get('medical_history', {}) if context else {}
            }
            
            # Generate follow-up questions
            follow_up_questions = self._generate_follow_up_questions(symptoms)
            
            return self._format_medical_response(ai_response, {
                'extracted_symptoms': symptoms,
                'patient_context': patient_context,
                'follow_up_questions': follow_up_questions,
                'urgency_level': urgency_indicators['urgency_level']
            })
            
        except Exception as e:
            logger.error(f"Intake agent failed: {str(e)}")
            return self._format_medical_response(
                "I'm sorry, I'm having technical difficulties. Can you please repeat your symptoms?",
                {'error': str(e)}
            )
    
    def _extract_symptoms(self, message: str) -> list:
        """
        Extract symptoms from message - basic implementation
        TODO for students: Use advanced NLP, medical entity recognition
        """
        # Simple keyword-based extraction
        symptom_keywords = [
            'pain', 'hurt', 'ache', 'fever', 'nausea', 'vomit', 'dizzy', 
            'tired', 'cough', 'cold', 'headache', 'chest pain', 'shortness of breath',
            'rash', 'swelling', 'bleeding', 'trouble breathing'
        ]
        
        found_symptoms = []
        message_lower = message.lower()
        
        for keyword in symptom_keywords:
            if keyword in message_lower:
                found_symptoms.append({
                    'name': keyword,
                    'mentioned_text': message,
                    'confidence': 0.7  # Basic confidence score
                })
        
        return found_symptoms
    
    def _generate_follow_up_questions(self, symptoms: list) -> list:
        """
        Generate relevant follow-up questions based on symptoms
        TODO for students: Make more sophisticated based on medical protocols
        """
        if not symptoms:
            return ["Can you describe what symptoms you're experiencing?"]
        
        # Basic follow-up questions
        questions = [
            "On a scale of 1-10, how would you rate your discomfort?",
            "How long have you been experiencing these symptoms?",
            "Have you taken any medications for this?"
        ]
        
        # Add symptom-specific questions
        for symptom in symptoms:
            if 'pain' in symptom['name']:
                questions.append("Can you describe the type of pain - sharp, dull, throbbing?")
            elif 'fever' in symptom['name']:
                questions.append("Have you taken your temperature? If so, what was it?")
        
        return questions[:3]  # Limit to 3 questions
    
    def get_intake_summary(self, patient_id: str) -> Dict[str, Any]:
        """
        Get summary of patient intake information
        TODO for students: Add more comprehensive tracking
        """
        try:
            # Get patient conversation history
            history = self.patient_db.get_patient_history(patient_id, limit=10)
            
            # Summarize symptoms collected
            all_symptoms = []
            for conversation in history:
                if 'extracted_symptoms' in conversation.get('ai_response', {}):
                    all_symptoms.extend(conversation['ai_response']['extracted_symptoms'])
            
            return {
                'patient_id': patient_id,
                'total_interactions': len(history),
                'symptoms_collected': len(all_symptoms),
                'unique_symptoms': list(set([s['name'] for s in all_symptoms])),
                'status': 'active' if history else 'new'
            }
            
        except Exception as e:
            logger.error(f"Failed to get intake summary: {str(e)}")
            return {'error': str(e)}
    
    def validate_patient_input(self, message: str) -> Dict[str, Any]:
        """
        Validate patient input for basic checks
        TODO for students: Add medical validation, safety checks
        """
        if len(message.strip()) < 5:
            return {
                'valid': False,
                'message': 'Please provide more details about your symptoms.'
            }
        
        # Check for emergency keywords
        emergency_words = ['emergency', '911', 'heart attack', 'can\'t breathe', 'suicide']
        if any(word in message.lower() for word in emergency_words):
            return {
                'valid': True,
                'urgent': True,
                'message': 'This appears urgent. Please call 911 or go to the nearest emergency room immediately.'
            }
        
        return {'valid': True, 'urgent': False}