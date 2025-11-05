#!/usr/bin/env python3
"""
ChromaDB Manager for AI Governance System
Manages regulatory knowledge and policy documents using vector search
"""

import chromadb
import logging
import os
import json
from typing import Dict, List, Any, Optional
from sentence_transformers import SentenceTransformer
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class GovernanceKnowledgeStore:
    """
    Manages AI governance knowledge using ChromaDB for efficient vector search
    Stores regulatory documents, policies, best practices, and compliance frameworks
    """
    
    def __init__(self, persist_directory: str = "./data/chromadb"):
        """Initialize ChromaDB client and collections"""
        try:
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(path=persist_directory)
            
            # Initialize sentence transformer for embeddings
            self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            
            # Create collections for different types of governance knowledge
            self.collections = {
                'regulatory_frameworks': self._get_or_create_collection('regulatory_frameworks'),
                'governance_policies': self._get_or_create_collection('governance_policies'),  
                'compliance_requirements': self._get_or_create_collection('compliance_requirements'),
                'best_practices': self._get_or_create_collection('best_practices'),
                'case_studies': self._get_or_create_collection('case_studies'),
                'audit_templates': self._get_or_create_collection('audit_templates')
            }
            
            # Initialize with default governance knowledge
            self._initialize_governance_knowledge()
            
            logger.info("GovernanceKnowledgeStore initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize GovernanceKnowledgeStore: {str(e)}")
            raise
    
    def _get_or_create_collection(self, name: str):
        """Get or create a ChromaDB collection"""
        try:
            return self.client.get_collection(name=name)
        except:
            return self.client.create_collection(
                name=name,
                embedding_function=None  # We'll handle embeddings manually
            )
    
    def _initialize_governance_knowledge(self):
        """Initialize collections with essential governance knowledge"""
        try:
            # Initialize regulatory frameworks
            self._populate_regulatory_frameworks()
            
            # Initialize governance policies
            self._populate_governance_policies()
            
            # Initialize compliance requirements
            self._populate_compliance_requirements()
            
            # Initialize best practices
            self._populate_best_practices()
            
            logger.info("Governance knowledge collections initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize governance knowledge: {str(e)}")
    
    def _populate_regulatory_frameworks(self):
        """Populate regulatory frameworks collection"""
        frameworks = [
            {
                'id': 'eu_ai_act_2024',
                'title': 'European Union AI Act 2024',
                'type': 'regulatory_framework',
                'jurisdiction': 'European Union',
                'content': """
                The EU AI Act establishes a comprehensive regulatory framework for AI systems.
                Key provisions include:
                - Risk-based approach with four categories: prohibited, high-risk, limited risk, minimal risk
                - Conformity assessment requirements for high-risk AI systems
                - CE marking obligations for certain AI systems
                - Transparency requirements for AI systems that interact with humans
                - Data governance and quality requirements
                - Human oversight and control measures
                - Accuracy, robustness and cybersecurity requirements
                - Post-market monitoring and reporting obligations
                """,
                'risk_categories': ['prohibited', 'high_risk', 'limited_risk', 'minimal_risk'],
                'compliance_requirements': [
                    'risk_assessment', 'conformity_assessment', 'ce_marking',
                    'technical_documentation', 'quality_management_system'
                ]
            },
            {
                'id': 'nist_ai_rmf_1_0',
                'title': 'NIST AI Risk Management Framework 1.0',
                'type': 'regulatory_framework',
                'jurisdiction': 'United States',
                'content': """
                NIST AI RMF provides a structured approach to AI risk management.
                Core functions:
                - GOVERN: Establish governance structures and processes
                - MAP: Identify and categorize AI risks
                - MEASURE: Analyze and assess AI risks
                - MANAGE: Respond to and monitor AI risks
                Key principles include human-centricity, fairness, accountability, and transparency
                Emphasizes stakeholder engagement and continuous improvement
                """,
                'functions': ['govern', 'map', 'measure', 'manage'],
                'principles': ['human_centricity', 'fairness', 'accountability', 'transparency']
            },
            {
                'id': 'iso_42001_2023',
                'title': 'ISO/IEC 42001:2023 AI Management System',
                'type': 'international_standard',
                'jurisdiction': 'International',
                'content': """
                ISO 42001 specifies requirements for establishing, implementing, maintaining
                and continually improving an AI management system.
                Key requirements:
                - AI policy and objectives
                - Risk management for AI systems
                - Competence and awareness programs
                - Operational planning and control
                - Performance evaluation and monitoring
                - Management review and continuous improvement
                """,
                'management_system_requirements': [
                    'policy', 'risk_management', 'competence', 'operations',
                    'performance_evaluation', 'improvement'
                ]
            }
        ]
        
        self._add_documents_to_collection('regulatory_frameworks', frameworks)
    
    def _populate_governance_policies(self):
        """Populate governance policies collection"""
        policies = [
            {
                'id': 'ai_ethics_policy',
                'title': 'AI Ethics and Responsible AI Policy',
                'type': 'internal_policy',
                'content': """
                Enterprise AI Ethics Policy establishes principles for responsible AI development.
                Core principles:
                - Fairness: AI systems should not discriminate or create unfair bias
                - Accountability: Clear responsibility for AI system decisions
                - Transparency: AI systems should be explainable and interpretable
                - Privacy: Protect individual privacy and data rights
                - Human oversight: Maintain meaningful human control over AI systems
                - Safety and reliability: Ensure AI systems operate safely and reliably
                """,
                'principles': ['fairness', 'accountability', 'transparency', 'privacy', 'human_oversight', 'safety']
            },
            {
                'id': 'bias_mitigation_policy',
                'title': 'AI Bias Detection and Mitigation Policy',
                'type': 'technical_policy',
                'content': """
                Policy for preventing and addressing bias in AI systems.
                Requirements:
                - Pre-deployment bias testing across protected groups
                - Regular bias monitoring and drift detection
                - Bias mitigation techniques implementation
                - Fairness metrics reporting and documentation
                - Stakeholder engagement in bias assessment
                - Remediation procedures for identified bias
                """,
                'protected_groups': ['race', 'gender', 'age', 'disability', 'religion', 'sexual_orientation'],
                'fairness_metrics': ['demographic_parity', 'equal_opportunity', 'equalized_odds']
            }
        ]
        
        self._add_documents_to_collection('governance_policies', policies)
    
    def _populate_compliance_requirements(self):
        """Populate compliance requirements collection"""
        requirements = [
            {
                'id': 'eu_ai_act_high_risk_requirements',
                'title': 'EU AI Act High-Risk System Requirements',
                'framework': 'EU_AI_Act',
                'risk_level': 'high_risk',
                'content': """
                Requirements for high-risk AI systems under EU AI Act:
                - Risk management system throughout AI system lifecycle
                - Data governance measures ensuring training data quality
                - Technical documentation demonstrating compliance
                - Record keeping for automatic logging of operations
                - Transparency and information provision to users
                - Human oversight measures ensuring meaningful control
                - Accuracy, robustness and cybersecurity measures
                - Quality management system for compliance processes
                - Conformity assessment before market placement
                - Post-market monitoring and reporting of serious incidents
                """,
                'mandatory_requirements': [
                    'risk_management_system', 'data_governance', 'technical_documentation',
                    'record_keeping', 'transparency', 'human_oversight',
                    'accuracy_robustness', 'quality_management', 'conformity_assessment'
                ]
            },
            {
                'id': 'gdpr_automated_decision_making',
                'title': 'GDPR Automated Decision-Making Requirements',
                'framework': 'GDPR',
                'content': """
                GDPR requirements for automated decision-making and profiling:
                - Right not to be subject to solely automated decision-making
                - Right to explanation for automated decisions
                - Explicit consent or legal basis required
                - Data protection impact assessment for high-risk processing
                - Privacy by design and by default principles
                - Data subject rights (access, rectification, erasure, portability)
                - Notification of data breaches within 72 hours
                """,
                'data_subject_rights': ['access', 'rectification', 'erasure', 'portability', 'objection']
            }
        ]
        
        self._add_documents_to_collection('compliance_requirements', requirements)
    
    def _populate_best_practices(self):
        """Populate AI governance best practices collection"""
        best_practices = [
            {
                'id': 'ai_governance_framework',
                'title': 'Enterprise AI Governance Framework Best Practices',
                'category': 'governance_structure',
                'content': """
                Best practices for establishing AI governance:
                - Establish AI governance committee with cross-functional representation
                - Define clear roles and responsibilities for AI oversight
                - Implement AI risk assessment processes
                - Create AI ethics review boards for high-risk applications
                - Establish AI incident response procedures
                - Implement continuous monitoring and auditing processes
                - Provide AI literacy training for all stakeholders
                - Maintain AI system inventory and classification
                - Regular governance framework review and updates
                """,
                'implementation_steps': [
                    'governance_committee', 'roles_responsibilities', 'risk_assessment',
                    'ethics_review', 'incident_response', 'monitoring', 'training'
                ]
            },
            {
                'id': 'bias_testing_methodology',
                'title': 'AI Bias Testing and Fairness Assessment Methodology',
                'category': 'bias_testing',
                'content': """
                Comprehensive methodology for AI bias testing:
                - Pre-deployment bias analysis across protected groups
                - Multiple fairness metrics evaluation (demographic parity, equal opportunity)
                - Intersectional bias analysis for multiple protected attributes
                - Bias impact assessment for affected communities
                - Mitigation strategy development and implementation
                - Post-deployment bias monitoring and drift detection
                - Regular bias audits with external validation
                - Stakeholder engagement and feedback collection
                """,
                'testing_phases': ['pre_deployment', 'deployment', 'post_deployment'],
                'metrics': ['demographic_parity', 'equal_opportunity', 'equalized_odds', 'calibration']
            }
        ]
        
        self._add_documents_to_collection('best_practices', best_practices)
    
    def _add_documents_to_collection(self, collection_name: str, documents: List[Dict]):
        """Add documents to a specific collection"""
        try:
            collection = self.collections[collection_name]
            
            # Prepare documents for ChromaDB
            ids = []
            embeddings = []
            metadatas = []
            documents_content = []
            
            for doc in documents:
                doc_id = doc['id']
                content = doc['content']
                
                # Generate embedding
                embedding = self.embedding_model.encode(content).tolist()
                
                # Prepare metadata (exclude content to avoid duplication)
                metadata = {k: v for k, v in doc.items() if k not in ['id', 'content']}
                metadata['created_at'] = datetime.now().isoformat()
                
                ids.append(doc_id)
                embeddings.append(embedding)
                metadatas.append(metadata)
                documents_content.append(content)
            
            # Add to collection (check if documents already exist)
            try:
                existing_docs = collection.get(ids=ids)
                if existing_docs['ids']:
                    logger.info(f"Documents already exist in {collection_name}, skipping...")
                    return
            except:
                pass  # Collection might be empty
            
            collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents_content
            )
            
            logger.info(f"Added {len(documents)} documents to {collection_name}")
            
        except Exception as e:
            logger.error(f"Failed to add documents to {collection_name}: {str(e)}")
    
    def search_regulatory_knowledge(self, query: str, framework: str = None, 
                                  n_results: int = 5) -> List[Dict]:
        """Search regulatory frameworks knowledge"""
        return self._search_collection('regulatory_frameworks', query, 
                                     filter_metadata={'framework': framework} if framework else None,
                                     n_results=n_results)
    
    def search_policies(self, query: str, policy_type: str = None, 
                       n_results: int = 5) -> List[Dict]:
        """Search governance policies"""
        return self._search_collection('governance_policies', query,
                                     filter_metadata={'type': policy_type} if policy_type else None,
                                     n_results=n_results)
    
    def search_compliance_requirements(self, query: str, framework: str = None,
                                     n_results: int = 5) -> List[Dict]:
        """Search compliance requirements"""
        return self._search_collection('compliance_requirements', query,
                                     filter_metadata={'framework': framework} if framework else None,
                                     n_results=n_results)
    
    def search_best_practices(self, query: str, category: str = None,
                            n_results: int = 5) -> List[Dict]:
        """Search best practices"""
        return self._search_collection('best_practices', query,
                                     filter_metadata={'category': category} if category else None,
                                     n_results=n_results)
    
    def search_all_knowledge(self, query: str, n_results: int = 10) -> Dict[str, List[Dict]]:
        """Search across all knowledge collections"""
        results = {}
        
        for collection_name in self.collections.keys():
            collection_results = self._search_collection(collection_name, query, n_results=n_results//2)
            if collection_results:
                results[collection_name] = collection_results
        
        return results
    
    def _search_collection(self, collection_name: str, query: str, 
                          filter_metadata: Dict = None, n_results: int = 5) -> List[Dict]:
        """Search a specific collection"""
        try:
            collection = self.collections[collection_name]
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Perform search
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_metadata,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Format results
            formatted_results = []
            if results['ids'] and results['ids'][0]:  # Check if results exist
                for i in range(len(results['ids'][0])):
                    formatted_result = {
                        'id': results['ids'][0][i],
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'score': 1 - results['distances'][0][i],  # Convert distance to similarity
                        'collection': collection_name
                    }
                    formatted_results.append(formatted_result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search {collection_name}: {str(e)}")
            return []
    
    def add_custom_policy(self, policy_id: str, title: str, content: str, 
                         policy_type: str, metadata: Dict = None) -> bool:
        """Add a custom governance policy"""
        try:
            policy_doc = {
                'id': policy_id,
                'title': title,
                'content': content,
                'type': policy_type
            }
            
            if metadata:
                policy_doc.update(metadata)
            
            self._add_documents_to_collection('governance_policies', [policy_doc])
            return True
            
        except Exception as e:
            logger.error(f"Failed to add custom policy: {str(e)}")
            return False
    
    def add_compliance_requirement(self, requirement_id: str, title: str, content: str,
                                 framework: str, metadata: Dict = None) -> bool:
        """Add a custom compliance requirement"""
        try:
            requirement_doc = {
                'id': requirement_id,
                'title': title,
                'content': content,
                'framework': framework
            }
            
            if metadata:
                requirement_doc.update(metadata)
            
            self._add_documents_to_collection('compliance_requirements', [requirement_doc])
            return True
            
        except Exception as e:
            logger.error(f"Failed to add compliance requirement: {str(e)}")
            return False
    
    def get_framework_details(self, framework_id: str) -> Optional[Dict]:
        """Get detailed information about a specific regulatory framework"""
        try:
            collection = self.collections['regulatory_frameworks']
            result = collection.get(ids=[framework_id])
            
            if result['ids']:
                return {
                    'id': result['ids'][0],
                    'content': result['documents'][0],
                    'metadata': result['metadatas'][0]
                }
            return None
            
        except Exception as e:
            logger.error(f"Failed to get framework details for {framework_id}: {str(e)}")
            return None
    
    def get_all_frameworks(self) -> List[Dict]:
        """Get list of all available regulatory frameworks"""
        try:
            collection = self.collections['regulatory_frameworks']
            results = collection.get()
            
            frameworks = []
            if results['ids']:
                for i in range(len(results['ids'])):
                    framework = {
                        'id': results['ids'][i],
                        'title': results['metadatas'][i].get('title', ''),
                        'jurisdiction': results['metadatas'][i].get('jurisdiction', ''),
                        'type': results['metadatas'][i].get('type', '')
                    }
                    frameworks.append(framework)
            
            return frameworks
            
        except Exception as e:
            logger.error(f"Failed to get all frameworks: {str(e)}")
            return []
    
    def update_document(self, collection_name: str, document_id: str, 
                       content: str = None, metadata: Dict = None) -> bool:
        """Update an existing document in a collection"""
        try:
            collection = self.collections[collection_name]
            
            update_data = {}
            
            if content:
                embedding = self.embedding_model.encode(content).tolist()
                update_data['embeddings'] = [embedding]
                update_data['documents'] = [content]
            
            if metadata:
                metadata['updated_at'] = datetime.now().isoformat()
                update_data['metadatas'] = [metadata]
            
            if update_data:
                collection.update(ids=[document_id], **update_data)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to update document {document_id} in {collection_name}: {str(e)}")
            return False
    
    def delete_document(self, collection_name: str, document_id: str) -> bool:
        """Delete a document from a collection"""
        try:
            collection = self.collections[collection_name]
            collection.delete(ids=[document_id])
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete document {document_id} from {collection_name}: {str(e)}")
            return False
    
    def get_collection_stats(self) -> Dict[str, int]:
        """Get statistics for all collections"""
        stats = {}
        
        for name, collection in self.collections.items():
            try:
                count = collection.count()
                stats[name] = count
            except Exception as e:
                logger.error(f"Failed to get stats for {name}: {str(e)}")
                stats[name] = 0
        
        return stats
    
    def health_check(self) -> bool:
        """Check if the knowledge store is functioning properly"""
        try:
            # Test basic functionality
            test_query = "AI governance"
            results = self.search_all_knowledge(test_query, n_results=1)
            
            # Check if we got results from at least one collection
            return len(results) > 0
            
        except Exception as e:
            logger.error(f"GovernanceKnowledgeStore health check failed: {str(e)}")
            return False
    
    def __del__(self):
        """Cleanup on destruction"""
        try:
            # ChromaDB handles cleanup automatically
            pass
        except:
            pass