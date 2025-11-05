#!/usr/bin/env python3
"""
Knowledge Agent - Retrieves relevant medical information
Simple implementation that students can build upon
"""

from .base_agent import BaseAgent
import logging
import json
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class KnowledgeAgent(BaseAgent):
    """
    Knowledge Agent retrieves and processes medical knowledge
    This is a barebones implementation - students should enhance it
    """
    
    def __init__(self, knowledge_store, patient_db):
        super().__init__(knowledge_store, patient_db, "knowledge")
    
    def retrieve_medical_knowledge(self, symptoms: List[Dict], patient_context: Dict = None) -> Dict[str, Any]:
        """
        Retrieve relevant medical knowledge based on symptoms
        TODO for students: Implement advanced RAG with ranking and filtering
        """
        try:
            # Build search query from symptoms
            query = self._build_search_query(symptoms)
            
            # Search different knowledge collections
            symptom_matches = self._search_symptoms(query)
            condition_matches = self._search_conditions(query)
            treatment_matches = self._search_treatments(query)
            
            # Filter and rank results
            relevant_conditions = self._filter_conditions(condition_matches, symptoms)
            relevant_treatments = self._filter_treatments(treatment_matches, relevant_conditions)
            warning_signs = self._extract_warning_signs(symptom_matches, condition_matches)
            
            return {
                'query': query,
                'conditions': relevant_conditions,
                'treatments': relevant_treatments,
                'warning_signs': warning_signs,
                'confidence_score': self._calculate_confidence(symptom_matches, condition_matches)
            }
            
        except Exception as e:
            logger.error(f"Knowledge retrieval failed: {str(e)}")
            return {
                'query': 'error',
                'conditions': [],
                'treatments': [],
                'warning_signs': [],
                'error': str(e)
            }
    
    def _build_search_query(self, symptoms: List[Dict]) -> str:
        """
        Build search query from symptoms
        TODO for students: Use semantic search and query expansion
        """
        if not symptoms:
            return "general medical information"
        
        # Extract symptom names
        symptom_names = [symptom.get('name', '') for symptom in symptoms]
        
        # Create query
        query = ' '.join(symptom_names)
        return query.strip()
    
    def _search_symptoms(self, query: str) -> Dict[str, Any]:
        """
        Search symptom database
        TODO for students: Optimize vector search parameters
        """
        try:
            return self.knowledge_store.search_symptoms(query, n_results=5)
        except Exception as e:
            logger.error(f"Symptom search failed: {str(e)}")
            return {'results': {'documents': [[]], 'metadatas': [[]]}}
    
    def _search_conditions(self, query: str) -> Dict[str, Any]:
        """
        Search medical conditions database
        TODO for students: Add semantic ranking and filtering
        """
        try:
            return self.knowledge_store.search_conditions(query, n_results=3)
        except Exception as e:
            logger.error(f"Condition search failed: {str(e)}")
            return {'results': {'documents': [[]], 'metadatas': [[]]}}
    
    def _search_treatments(self, query: str) -> Dict[str, Any]:
        """
        Search treatment protocols database
        TODO for students: Context-aware treatment recommendations
        """
        try:
            return self.knowledge_store.search_treatments(query, n_results=3)
        except Exception as e:
            logger.error(f"Treatment search failed: {str(e)}")
            return {'results': {'documents': [[]], 'metadatas': [[]]}}
    
    def _filter_conditions(self, condition_matches: Dict, symptoms: List[Dict]) -> List[Dict]:
        """
        Filter and format condition matches
        TODO for students: Advanced relevance scoring and medical reasoning
        """
        conditions = []
        
        try:
            documents = condition_matches.get('results', {}).get('documents', [[]])
            metadatas = condition_matches.get('results', {}).get('metadatas', [[]])
            
            if documents and documents[0] and metadatas and metadatas[0]:
                for doc, meta in zip(documents[0], metadatas[0]):
                    conditions.append({
                        'name': meta.get('name', 'Unknown'),
                        'description': doc,
                        'severity': meta.get('severity', 5),
                        'requires_escalation': meta.get('escalation_required', False)
                    })
        
        except Exception as e:
            logger.error(f"Failed to filter conditions: {str(e)}")
        
        return conditions[:3]  # Return top 3
    
    def _filter_treatments(self, treatment_matches: Dict, conditions: List[Dict]) -> List[Dict]:
        """
        Filter treatment recommendations based on conditions
        TODO for students: Personalized treatment recommendations
        """
        treatments = []
        
        try:
            documents = treatment_matches.get('results', {}).get('documents', [[]])
            metadatas = treatment_matches.get('results', {}).get('metadatas', [[]])
            
            if documents and documents[0] and metadatas and metadatas[0]:
                for doc, meta in zip(documents[0], metadatas[0]):
                    treatments.append({
                        'condition': meta.get('condition', 'General'),
                        'immediate_actions': meta.get('immediate_actions', []),
                        'follow_up': meta.get('follow_up', []),
                        'description': doc
                    })
                    
        except Exception as e:
            logger.error(f"Failed to filter treatments: {str(e)}")
        
        return treatments[:2]  # Return top 2
    
    def _extract_warning_signs(self, symptom_matches: Dict, condition_matches: Dict) -> List[str]:
        """
        Extract warning signs from matched conditions
        TODO for students: Intelligent warning sign detection
        """
        warning_signs = []
        
        try:
            # From symptom matches
            symptom_metadatas = symptom_matches.get('results', {}).get('metadatas', [[]])
            if symptom_metadatas and symptom_metadatas[0]:
                for meta in symptom_metadatas[0]:
                    red_flags = meta.get('red_flags', [])
                    warning_signs.extend(red_flags)
            
            # Remove duplicates and limit
            warning_signs = list(set(warning_signs))[:5]
            
        except Exception as e:
            logger.error(f"Failed to extract warning signs: {str(e)}")
        
        return warning_signs
    
    def _calculate_confidence(self, symptom_matches: Dict, condition_matches: Dict) -> float:
        """
        Calculate confidence score for knowledge retrieval
        TODO for students: Sophisticated confidence scoring
        """
        try:
            symptom_count = len(symptom_matches.get('results', {}).get('documents', [[]])[0] or [])
            condition_count = len(condition_matches.get('results', {}).get('documents', [[]])[0] or [])
            
            # Simple confidence calculation
            if symptom_count > 0 and condition_count > 0:
                return 0.8
            elif symptom_count > 0 or condition_count > 0:
                return 0.6
            else:
                return 0.3
                
        except Exception as e:
            logger.error(f"Failed to calculate confidence: {str(e)}")
            return 0.5
    
    def search_knowledge_base(self, query: str) -> Dict[str, Any]:
        """
        General knowledge base search
        TODO for students: Multi-modal search across all collections
        """
        try:
            # Perform hybrid search
            results = self.knowledge_store.hybrid_search(query)
            
            return {
                'query': query,
                'results': results,
                'result_count': len(results.get('symptoms', {}).get('documents', [[]])[0] or [])
            }
            
        except Exception as e:
            logger.error(f"Knowledge base search failed: {str(e)}")
            return {'error': str(e), 'query': query}
    
    def check_drug_interactions(self, medications: List[str]) -> Dict[str, Any]:
        """
        Check for drug interactions
        TODO for students: Comprehensive interaction analysis
        """
        try:
            if not medications:
                return {'interactions': [], 'safe': True}
            
            interaction_results = self.knowledge_store.check_drug_interactions(medications)
            
            return {
                'medications': medications,
                'interactions': interaction_results.get('interactions', []),
                'interaction_count': interaction_results.get('interaction_count', 0),
                'safe': interaction_results.get('interaction_count', 0) == 0
            }
            
        except Exception as e:
            logger.error(f"Drug interaction check failed: {str(e)}")
            return {'error': str(e), 'medications': medications}
    
    def get_medical_summary(self, patient_id: str) -> Dict[str, Any]:
        """
        Get comprehensive medical summary for patient
        TODO for students: Advanced patient knowledge aggregation
        """
        try:
            # Get patient history
            history = self.patient_db.get_patient_history(patient_id, limit=10)
            
            # Extract all mentioned symptoms and conditions
            all_symptoms = []
            all_conditions = []
            
            for conversation in history:
                ai_response = conversation.get('ai_response', {})
                if 'medical_knowledge' in ai_response:
                    conditions = ai_response['medical_knowledge'].get('relevant_conditions', [])
                    all_conditions.extend([c.get('name', '') for c in conditions])
                
                if 'extracted_symptoms' in ai_response:
                    symptoms = ai_response['extracted_symptoms']
                    all_symptoms.extend([s.get('name', '') for s in symptoms])
            
            return {
                'patient_id': patient_id,
                'unique_symptoms': list(set(all_symptoms)),
                'potential_conditions': list(set(all_conditions)),
                'interaction_count': len(history),
                'knowledge_confidence': 0.7 if history else 0.1
            }
            
        except Exception as e:
            logger.error(f"Failed to get medical summary: {str(e)}")
            return {'error': str(e), 'patient_id': patient_id}