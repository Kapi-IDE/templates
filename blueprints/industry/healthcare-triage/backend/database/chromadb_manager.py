#!/usr/bin/env python3
"""
ChromaDB Manager for Healthcare AI System
Handles vector storage and retrieval of medical knowledge
"""

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import json
import os
import logging
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import numpy as np

logger = logging.getLogger(__name__)

class MedicalKnowledgeStore:
    """
    Manages medical knowledge in ChromaDB vector database
    Handles symptoms, conditions, treatments, and drug interactions
    """
    
    def __init__(self, db_path: str = "./medical_knowledge_db"):
        """Initialize ChromaDB client and collections"""
        self.db_path = db_path
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB client
        try:
            self.client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=self.db_path,
                anonymized_telemetry=False
            ))
            
            # Create collections for different types of medical data
            self.symptoms_collection = self._get_or_create_collection("symptoms")
            self.conditions_collection = self._get_or_create_collection("conditions")  
            self.treatments_collection = self._get_or_create_collection("treatments")
            self.drugs_collection = self._get_or_create_collection("drugs")
            
            logger.info("ChromaDB initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {str(e)}")
            raise
    
    def _get_or_create_collection(self, name: str):
        """Get existing collection or create new one"""
        try:
            collection = self.client.get_collection(name)
            logger.info(f"Retrieved existing collection: {name}")
            return collection
        except:
            collection = self.client.create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Created new collection: {name}")
            return collection
    
    def load_medical_data(self):
        """Load medical data from JSON files into ChromaDB"""
        try:
            # Load medical knowledge
            with open('../data/medical_knowledge.json', 'r') as f:
                medical_data = json.load(f)
            
            # Load drug interactions
            with open('../data/drug_interactions.json', 'r') as f:
                drug_data = json.load(f)
            
            # Load escalation rules
            with open('../data/escalation_rules.json', 'r') as f:
                escalation_data = json.load(f)
            
            # Process and store symptoms
            self._store_symptoms(medical_data['symptoms'])
            
            # Process and store conditions
            self._store_conditions(medical_data['conditions'])
            
            # Process and store treatments
            self._store_treatments(medical_data['treatments'])
            
            # Process and store drug information
            self._store_drugs(drug_data['medications'])
            
            logger.info("Medical data loaded successfully into ChromaDB")
            
        except Exception as e:
            logger.error(f"Failed to load medical data: {str(e)}")
            raise
    
    def _store_symptoms(self, symptoms: List[Dict]):
        """Store symptom data in ChromaDB"""
        documents = []
        metadatas = []
        ids = []
        
        for symptom in symptoms:
            # Create document text for embedding
            doc_text = f"""
            Symptom: {symptom['name']}
            Description: {symptom['description']}
            Severity: {symptom['severity_base']}
            Red flags: {', '.join(symptom['red_flags'])}
            Associated conditions: {', '.join(symptom['associated_conditions'])}
            """
            
            documents.append(doc_text.strip())
            metadatas.append({
                'id': symptom['id'],
                'name': symptom['name'],
                'severity_base': symptom['severity_base'],
                'type': 'symptom',
                'red_flags': symptom['red_flags'],
                'associated_conditions': symptom['associated_conditions'],
                'triage_modifiers': json.dumps(symptom['triage_modifiers']),
                'questions': symptom['questions']
            })
            ids.append(f"symptom_{symptom['id']}")
        
        self.symptoms_collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Stored {len(symptoms)} symptoms in ChromaDB")
    
    def _store_conditions(self, conditions: List[Dict]):
        """Store medical conditions in ChromaDB"""
        documents = []
        metadatas = []
        ids = []
        
        for condition in conditions:
            doc_text = f"""
            Condition: {condition['name']}
            Description: {condition['description']}
            Severity: {condition['severity']}
            Treatment: {condition['treatment_protocol']}
            Symptoms: {', '.join(condition['symptoms'])}
            Risk factors: {', '.join(condition['risk_factors'])}
            """
            
            documents.append(doc_text.strip())
            metadatas.append({
                'id': condition['id'],
                'name': condition['name'],
                'severity': condition['severity'],
                'type': 'condition',
                'escalation_required': condition['escalation_required'],
                'treatment_protocol': condition['treatment_protocol'],
                'symptoms': condition['symptoms'],
                'risk_factors': condition['risk_factors']
            })
            ids.append(f"condition_{condition['id']}")
        
        self.conditions_collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Stored {len(conditions)} conditions in ChromaDB")
    
    def _store_treatments(self, treatments: List[Dict]):
        """Store treatment protocols in ChromaDB"""
        documents = []
        metadatas = []
        ids = []
        
        for i, treatment in enumerate(treatments):
            doc_text = f"""
            Treatment for: {treatment['condition']}
            Immediate actions: {', '.join(treatment['immediate_actions'])}
            Follow-up care: {', '.join(treatment['follow_up'])}
            """
            
            documents.append(doc_text.strip())
            metadatas.append({
                'condition': treatment['condition'],
                'type': 'treatment',
                'immediate_actions': treatment['immediate_actions'],
                'follow_up': treatment['follow_up']
            })
            ids.append(f"treatment_{i}")
        
        self.treatments_collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Stored {len(treatments)} treatments in ChromaDB")
    
    def _store_drugs(self, medications: List[Dict]):
        """Store drug information in ChromaDB"""
        documents = []
        metadatas = []
        ids = []
        
        for medication in medications:
            # Extract interaction info
            interactions = [f"{int['drug']}: {int['description']}" 
                          for int in medication['interactions']]
            
            doc_text = f"""
            Medication: {medication['name']} ({medication['generic_name']})
            Class: {medication['class']}
            Contraindications: {', '.join(medication['contraindications'])}
            Interactions: {', '.join(interactions)}
            Side effects: {', '.join(medication['side_effects'])}
            Dosage: {medication['dosage_adult']}
            """
            
            documents.append(doc_text.strip())
            metadatas.append({
                'name': medication['name'],
                'generic_name': medication['generic_name'],
                'drug_class': medication['class'],
                'type': 'medication',
                'contraindications': medication['contraindications'],
                'interactions': json.dumps(medication['interactions']),
                'side_effects': medication['side_effects'],
                'dosage_adult': medication['dosage_adult']
            })
            ids.append(f"drug_{medication['name']}")
        
        self.drugs_collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Stored {len(medications)} medications in ChromaDB")
    
    def search_symptoms(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Search for symptoms matching the query"""
        try:
            results = self.symptoms_collection.query(
                query_texts=[query],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            return {
                'query': query,
                'results': results,
                'count': len(results['documents'][0])
            }
        except Exception as e:
            logger.error(f"Failed to search symptoms: {str(e)}")
            raise
    
    def search_conditions(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Search for medical conditions matching the query"""
        try:
            results = self.conditions_collection.query(
                query_texts=[query],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            return {
                'query': query,
                'results': results,
                'count': len(results['documents'][0])
            }
        except Exception as e:
            logger.error(f"Failed to search conditions: {str(e)}")
            raise
    
    def search_treatments(self, condition: str, n_results: int = 3) -> Dict[str, Any]:
        """Search for treatments for a specific condition"""
        try:
            results = self.treatments_collection.query(
                query_texts=[condition],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            return {
                'condition': condition,
                'results': results,
                'count': len(results['documents'][0])
            }
        except Exception as e:
            logger.error(f"Failed to search treatments: {str(e)}")
            raise
    
    def check_drug_interactions(self, medications: List[str]) -> Dict[str, Any]:
        """Check for drug interactions between medications"""
        try:
            interactions_found = []
            
            for med in medications:
                results = self.drugs_collection.query(
                    query_texts=[med],
                    n_results=1,
                    include=['documents', 'metadatas']
                )
                
                if results['documents'][0]:
                    metadata = results['metadatas'][0][0]
                    if 'interactions' in metadata:
                        drug_interactions = json.loads(metadata['interactions'])
                        for interaction in drug_interactions:
                            if interaction['drug'].lower() in [m.lower() for m in medications]:
                                interactions_found.append({
                                    'drug1': med,
                                    'drug2': interaction['drug'],
                                    'severity': interaction['severity'],
                                    'description': interaction['description']
                                })
            
            return {
                'medications': medications,
                'interactions': interactions_found,
                'interaction_count': len(interactions_found)
            }
            
        except Exception as e:
            logger.error(f"Failed to check drug interactions: {str(e)}")
            raise
    
    def hybrid_search(self, query: str, patient_context: Dict = None) -> Dict[str, Any]:
        """Perform comprehensive search across all collections"""
        try:
            # Search all collections
            symptom_results = self.search_symptoms(query, 3)
            condition_results = self.search_conditions(query, 3)
            treatment_results = self.search_treatments(query, 2)
            
            # Combine and rank results
            combined_results = {
                'symptoms': symptom_results['results'],
                'conditions': condition_results['results'],
                'treatments': treatment_results['results'],
                'query': query,
                'patient_context': patient_context
            }
            
            return combined_results
            
        except Exception as e:
            logger.error(f"Failed to perform hybrid search: {str(e)}")
            raise
    
    def get_collection_stats(self) -> Dict[str, int]:
        """Get statistics about stored data"""
        try:
            stats = {
                'symptoms': self.symptoms_collection.count(),
                'conditions': self.conditions_collection.count(),
                'treatments': self.treatments_collection.count(),
                'drugs': self.drugs_collection.count()
            }
            return stats
        except Exception as e:
            logger.error(f"Failed to get collection stats: {str(e)}")
            raise
    
    def health_check(self) -> bool:
        """Verify ChromaDB is working properly"""
        try:
            # Test basic operations
            test_query = "test query"
            self.symptoms_collection.query(query_texts=[test_query], n_results=1)
            return True
        except Exception as e:
            logger.error(f"ChromaDB health check failed: {str(e)}")
            return False
    
    def reset_database(self):
        """Reset all collections - USE WITH CAUTION"""
        try:
            collections = ['symptoms', 'conditions', 'treatments', 'drugs']
            for collection_name in collections:
                try:
                    self.client.delete_collection(collection_name)
                except:
                    pass  # Collection may not exist
            
            # Recreate collections
            self.symptoms_collection = self._get_or_create_collection("symptoms")
            self.conditions_collection = self._get_or_create_collection("conditions")
            self.treatments_collection = self._get_or_create_collection("treatments")
            self.drugs_collection = self._get_or_create_collection("drugs")
            
            logger.info("ChromaDB reset successfully")
            
        except Exception as e:
            logger.error(f"Failed to reset ChromaDB: {str(e)}")
            raise