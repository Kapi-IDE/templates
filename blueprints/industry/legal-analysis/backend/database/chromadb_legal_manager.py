#!/usr/bin/env python3
"""
ChromaDB Manager for Legal AI System
Handles legal document embeddings, RAG search, and legal knowledge retrieval
"""

import chromadb
from chromadb.config import Settings
import json
import logging
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class LegalKnowledgeStore:
    """
    Manages legal document embeddings and knowledge retrieval using ChromaDB
    Specialized for legal document RAG with case law, statutes, and legal precedents
    """
    
    def __init__(self, persist_directory: str = "./legal_chroma_db"):
        """Initialize ChromaDB for legal knowledge storage"""
        try:
            # Configure ChromaDB with persistence
            self.persist_directory = persist_directory
            os.makedirs(persist_directory, exist_ok=True)
            
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(
                    allow_reset=True,
                    anonymized_telemetry=False
                )
            )
            
            # Initialize legal embedding model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Create legal document collections
            self._initialize_legal_collections()
            
            logger.info("Legal ChromaDB knowledge store initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize legal knowledge store: {str(e)}")
            raise
    
    def _initialize_legal_collections(self):
        """Initialize specialized collections for legal documents"""
        try:
            # Case Law Collection
            self.case_law_collection = self.client.get_or_create_collection(
                name="legal_case_law",
                metadata={
                    "description": "Legal case law with holdings, facts, and legal reasoning",
                    "type": "case_law",
                    "embedding_model": "all-MiniLM-L6-v2"
                }
            )
            
            # Statutes Collection
            self.statutes_collection = self.client.get_or_create_collection(
                name="legal_statutes",
                metadata={
                    "description": "Federal and state statutes with legal text and interpretations",
                    "type": "statutes",
                    "embedding_model": "all-MiniLM-L6-v2"
                }
            )
            
            # Legal Precedents Collection
            self.precedents_collection = self.client.get_or_create_collection(
                name="legal_precedents",
                metadata={
                    "description": "Legal precedents with principles and fact patterns",
                    "type": "precedents",
                    "embedding_model": "all-MiniLM-L6-v2"
                }
            )
            
            # Contract Templates Collection
            self.contracts_collection = self.client.get_or_create_collection(
                name="legal_contracts",
                metadata={
                    "description": "Contract templates and clauses with legal analysis",
                    "type": "contracts",
                    "embedding_model": "all-MiniLM-L6-v2"
                }
            )
            
            # Legal Documents Collection (for client-specific documents)
            self.documents_collection = self.client.get_or_create_collection(
                name="legal_documents",
                metadata={
                    "description": "Client legal documents with privilege protection",
                    "type": "client_documents",
                    "embedding_model": "all-MiniLM-L6-v2",
                    "privilege_protected": True
                }
            )
            
            # Legal Regulations Collection
            self.regulations_collection = self.client.get_or_create_collection(
                name="legal_regulations",
                metadata={
                    "description": "Federal and state regulations with compliance guidance",
                    "type": "regulations",
                    "embedding_model": "all-MiniLM-L6-v2"
                }
            )
            
            logger.info("Legal ChromaDB collections initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize legal collections: {str(e)}")
            raise
    
    def add_case_law(self, case_data: Dict[str, Any]) -> bool:
        """Add case law to the knowledge base"""
        try:
            case_id = case_data.get('case_id', self._generate_case_id(case_data))
            
            # Create searchable text combining key legal elements
            searchable_text = self._create_case_searchable_text(case_data)
            
            # Generate embeddings
            embedding = self.embedding_model.encode(searchable_text).tolist()
            
            # Prepare metadata
            metadata = {
                'case_name': case_data.get('case_name', ''),
                'citation': case_data.get('citation', ''),
                'court': case_data.get('court', ''),
                'jurisdiction': case_data.get('jurisdiction', ''),
                'decision_date': case_data.get('decision_date', ''),
                'precedent_type': case_data.get('precedent_type', 'binding'),
                'practice_areas': json.dumps(case_data.get('practice_areas', [])),
                'legal_issues': json.dumps(case_data.get('legal_issues', [])),
                'citation_count': case_data.get('citation_count', 0),
                'overruled': case_data.get('overruled', False),
                'document_type': 'case_law',
                'added_date': datetime.now().isoformat()
            }
            
            # Add to collection
            self.case_law_collection.add(
                ids=[case_id],
                documents=[searchable_text],
                embeddings=[embedding],
                metadatas=[metadata]
            )
            
            logger.info(f"Case law {case_id} added successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add case law: {str(e)}")
            return False
    
    def _create_case_searchable_text(self, case_data: Dict[str, Any]) -> str:
        """Create searchable text for case law"""
        elements = []
        
        # Case name and citation
        if case_data.get('case_name'):
            elements.append(f"Case: {case_data['case_name']}")
        
        if case_data.get('citation'):
            elements.append(f"Citation: {case_data['citation']}")
        
        # Legal issues
        if case_data.get('legal_issues'):
            issues = case_data['legal_issues']
            if isinstance(issues, list):
                elements.append(f"Legal Issues: {', '.join(issues)}")
            else:
                elements.append(f"Legal Issues: {issues}")
        
        # Key facts
        if case_data.get('key_facts'):
            elements.append(f"Facts: {case_data['key_facts']}")
        
        # Holding
        if case_data.get('holding'):
            elements.append(f"Holding: {case_data['holding']}")
        
        # Legal reasoning
        if case_data.get('legal_reasoning'):
            elements.append(f"Reasoning: {case_data['legal_reasoning']}")
        
        # Summary
        if case_data.get('summary'):
            elements.append(f"Summary: {case_data['summary']}")
        
        return ' | '.join(elements)
    
    def add_statute(self, statute_data: Dict[str, Any]) -> bool:
        """Add statute to the knowledge base"""
        try:
            statute_id = statute_data.get('statute_id', self._generate_statute_id(statute_data))
            
            # Create searchable text
            searchable_text = self._create_statute_searchable_text(statute_data)
            
            # Generate embeddings
            embedding = self.embedding_model.encode(searchable_text).tolist()
            
            # Prepare metadata
            metadata = {
                'title': statute_data.get('title', ''),
                'citation': statute_data.get('citation', ''),
                'jurisdiction': statute_data.get('jurisdiction', ''),
                'chapter': statute_data.get('chapter', ''),
                'section': statute_data.get('section', ''),
                'effective_date': statute_data.get('effective_date', ''),
                'keywords': json.dumps(statute_data.get('keywords', [])),
                'practice_areas': json.dumps(statute_data.get('practice_areas', [])),
                'document_type': 'statute',
                'added_date': datetime.now().isoformat()
            }
            
            # Add to collection
            self.statutes_collection.add(
                ids=[statute_id],
                documents=[searchable_text],
                embeddings=[embedding],
                metadatas=[metadata]
            )
            
            logger.info(f"Statute {statute_id} added successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add statute: {str(e)}")
            return False
    
    def _create_statute_searchable_text(self, statute_data: Dict[str, Any]) -> str:
        """Create searchable text for statute"""
        elements = []
        
        # Title and citation
        if statute_data.get('title'):
            elements.append(f"Title: {statute_data['title']}")
        
        if statute_data.get('citation'):
            elements.append(f"Citation: {statute_data['citation']}")
        
        # Statute text
        if statute_data.get('statute_text'):
            elements.append(f"Text: {statute_data['statute_text']}")
        
        # Summary
        if statute_data.get('summary'):
            elements.append(f"Summary: {statute_data['summary']}")
        
        # Keywords
        if statute_data.get('keywords'):
            keywords = statute_data['keywords']
            if isinstance(keywords, list):
                elements.append(f"Keywords: {', '.join(keywords)}")
            else:
                elements.append(f"Keywords: {keywords}")
        
        return ' | '.join(elements)
    
    def add_precedent(self, precedent_data: Dict[str, Any]) -> bool:
        """Add legal precedent to the knowledge base"""
        try:
            precedent_id = precedent_data.get('precedent_id', self._generate_precedent_id(precedent_data))
            
            # Create searchable text
            searchable_text = self._create_precedent_searchable_text(precedent_data)
            
            # Generate embeddings
            embedding = self.embedding_model.encode(searchable_text).tolist()
            
            # Prepare metadata
            metadata = {
                'legal_principle': precedent_data.get('legal_principle', ''),
                'precedent_weight': precedent_data.get('precedent_weight', 5),
                'binding_authority': precedent_data.get('binding_authority', ''),
                'jurisdiction': precedent_data.get('jurisdiction', ''),
                'practice_area': precedent_data.get('practice_area', ''),
                'fact_pattern': precedent_data.get('fact_pattern', ''),
                'legal_standard': precedent_data.get('legal_standard', ''),
                'overruled': precedent_data.get('overruled', False),
                'document_type': 'precedent',
                'added_date': datetime.now().isoformat()
            }
            
            # Add to collection
            self.precedents_collection.add(
                ids=[precedent_id],
                documents=[searchable_text],
                embeddings=[embedding],
                metadatas=[metadata]
            )
            
            logger.info(f"Precedent {precedent_id} added successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add precedent: {str(e)}")
            return False
    
    def _create_precedent_searchable_text(self, precedent_data: Dict[str, Any]) -> str:
        """Create searchable text for precedent"""
        elements = []
        
        # Legal principle
        if precedent_data.get('legal_principle'):
            elements.append(f"Principle: {precedent_data['legal_principle']}")
        
        # Fact pattern
        if precedent_data.get('fact_pattern'):
            elements.append(f"Facts: {precedent_data['fact_pattern']}")
        
        # Legal standard
        if precedent_data.get('legal_standard'):
            elements.append(f"Standard: {precedent_data['legal_standard']}")
        
        # Binding authority
        if precedent_data.get('binding_authority'):
            elements.append(f"Authority: {precedent_data['binding_authority']}")
        
        # Practice area
        if precedent_data.get('practice_area'):
            elements.append(f"Practice Area: {precedent_data['practice_area']}")
        
        return ' | '.join(elements)
    
    def add_contract_template(self, contract_data: Dict[str, Any]) -> bool:
        """Add contract template to the knowledge base"""
        try:
            template_id = contract_data.get('template_id', self._generate_template_id(contract_data))
            
            # Create searchable text
            searchable_text = self._create_contract_searchable_text(contract_data)
            
            # Generate embeddings
            embedding = self.embedding_model.encode(searchable_text).tolist()
            
            # Prepare metadata
            metadata = {
                'template_name': contract_data.get('template_name', ''),
                'contract_type': contract_data.get('contract_type', ''),
                'jurisdiction': contract_data.get('jurisdiction', ''),
                'practice_area': contract_data.get('practice_area', ''),
                'risk_level': contract_data.get('risk_level', 'medium'),
                'complexity_level': contract_data.get('complexity_level', 'medium'),
                'standard_clauses': json.dumps(contract_data.get('standard_clauses', [])),
                'optional_clauses': json.dumps(contract_data.get('optional_clauses', [])),
                'document_type': 'contract_template',
                'added_date': datetime.now().isoformat()
            }
            
            # Add to collection
            self.contracts_collection.add(
                ids=[template_id],
                documents=[searchable_text],
                embeddings=[embedding],
                metadatas=[metadata]
            )
            
            logger.info(f"Contract template {template_id} added successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add contract template: {str(e)}")
            return False
    
    def _create_contract_searchable_text(self, contract_data: Dict[str, Any]) -> str:
        """Create searchable text for contract template"""
        elements = []
        
        # Template name and type
        if contract_data.get('template_name'):
            elements.append(f"Template: {contract_data['template_name']}")
        
        if contract_data.get('contract_type'):
            elements.append(f"Type: {contract_data['contract_type']}")
        
        # Template content
        if contract_data.get('template_content'):
            # Truncate very long content
            content = contract_data['template_content']
            if len(content) > 2000:
                content = content[:2000] + "..."
            elements.append(f"Content: {content}")
        
        # Standard clauses
        if contract_data.get('standard_clauses'):
            clauses = contract_data['standard_clauses']
            if isinstance(clauses, list):
                elements.append(f"Clauses: {', '.join(clauses)}")
        
        return ' | '.join(elements)
    
    def add_legal_document(self, document_data: Dict[str, Any], privilege_protected: bool = True) -> bool:
        """Add legal document with privilege protection"""
        try:
            document_id = document_data.get('document_id', self._generate_document_id(document_data))
            
            # Only add if privilege is properly handled
            if privilege_protected and not document_data.get('attorney_id'):
                raise ValueError("Privileged documents require attorney_id")
            
            # Create searchable text
            searchable_text = self._create_document_searchable_text(document_data)
            
            # Generate embeddings
            embedding = self.embedding_model.encode(searchable_text).tolist()
            
            # Prepare metadata with privilege information
            metadata = {
                'document_title': document_data.get('document_title', ''),
                'document_type': document_data.get('document_type', ''),
                'attorney_id': document_data.get('attorney_id', ''),
                'client_id': document_data.get('client_id', ''),
                'case_id': document_data.get('case_id', ''),
                'privilege_protected': privilege_protected,
                'work_product': document_data.get('work_product', False),
                'confidential': document_data.get('confidential', True),
                'document_status': document_data.get('document_status', 'draft'),
                'created_by': document_data.get('created_by', ''),
                'document_type_meta': 'legal_document',
                'added_date': datetime.now().isoformat()
            }
            
            # Add to collection
            self.documents_collection.add(
                ids=[document_id],
                documents=[searchable_text],
                embeddings=[embedding],
                metadatas=[metadata]
            )
            
            logger.info(f"Legal document {document_id} added successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add legal document: {str(e)}")
            return False
    
    def _create_document_searchable_text(self, document_data: Dict[str, Any]) -> str:
        """Create searchable text for legal document"""
        elements = []
        
        # Document title and type
        if document_data.get('document_title'):
            elements.append(f"Title: {document_data['document_title']}")
        
        if document_data.get('document_type'):
            elements.append(f"Type: {document_data['document_type']}")
        
        # Document content (if available and not too sensitive)
        if document_data.get('searchable_content'):
            content = document_data['searchable_content']
            if len(content) > 1500:
                content = content[:1500] + "..."
            elements.append(f"Content: {content}")
        
        return ' | '.join(elements)
    
    def search_case_law(self, query: str, jurisdiction: str = None, limit: int = 10,
                       include_overruled: bool = False) -> List[Dict[str, Any]]:
        """Search case law using RAG"""
        try:
            # Prepare search filters
            where_conditions = {"document_type": "case_law"}
            
            if jurisdiction:
                where_conditions["jurisdiction"] = jurisdiction
            
            if not include_overruled:
                where_conditions["overruled"] = False
            
            # Perform vector search
            results = self.case_law_collection.query(
                query_texts=[query],
                n_results=limit,
                where=where_conditions
            )
            
            # Format results
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    result = {
                        'case_id': results['ids'][0][i],
                        'document': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i],
                        'relevance_score': 1 - results['distances'][0][i]  # Convert distance to similarity
                    }
                    
                    # Parse JSON metadata fields
                    metadata = result['metadata']
                    for field in ['practice_areas', 'legal_issues']:
                        if field in metadata and metadata[field]:
                            try:
                                metadata[field] = json.loads(metadata[field])
                            except:
                                pass
                    
                    formatted_results.append(result)
            
            logger.info(f"Case law search returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search case law: {str(e)}")
            return []
    
    def search_statutes(self, query: str, jurisdiction: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Search statutes using RAG"""
        try:
            # Prepare search filters
            where_conditions = {"document_type": "statute"}
            
            if jurisdiction:
                where_conditions["jurisdiction"] = jurisdiction
            
            # Perform vector search
            results = self.statutes_collection.query(
                query_texts=[query],
                n_results=limit,
                where=where_conditions
            )
            
            # Format results
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    result = {
                        'statute_id': results['ids'][0][i],
                        'document': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i],
                        'relevance_score': 1 - results['distances'][0][i]
                    }
                    
                    # Parse JSON metadata fields
                    metadata = result['metadata']
                    for field in ['keywords', 'practice_areas']:
                        if field in metadata and metadata[field]:
                            try:
                                metadata[field] = json.loads(metadata[field])
                            except:
                                pass
                    
                    formatted_results.append(result)
            
            logger.info(f"Statute search returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search statutes: {str(e)}")
            return []
    
    def search_precedents(self, query: str, jurisdiction: str = None, limit: int = 15,
                         min_weight: int = 3) -> List[Dict[str, Any]]:
        """Search legal precedents using RAG"""
        try:
            # Prepare search filters
            where_conditions = {
                "document_type": "precedent",
                "overruled": False
            }
            
            if jurisdiction:
                where_conditions["jurisdiction"] = jurisdiction
            
            # Perform vector search
            results = self.precedents_collection.query(
                query_texts=[query],
                n_results=limit * 2  # Get more results to filter by weight
            )
            
            # Format and filter results
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    metadata = results['metadatas'][0][i]
                    
                    # Filter by precedent weight
                    if metadata.get('precedent_weight', 0) >= min_weight:
                        result = {
                            'precedent_id': results['ids'][0][i],
                            'document': results['documents'][0][i],
                            'metadata': metadata,
                            'distance': results['distances'][0][i],
                            'relevance_score': 1 - results['distances'][0][i]
                        }
                        formatted_results.append(result)
                    
                    if len(formatted_results) >= limit:
                        break
            
            logger.info(f"Precedent search returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search precedents: {str(e)}")
            return []
    
    def search_contract_templates(self, query: str, contract_type: str = None,
                                limit: int = 10) -> List[Dict[str, Any]]:
        """Search contract templates using RAG"""
        try:
            # Prepare search filters
            where_conditions = {"document_type": "contract_template"}
            
            if contract_type:
                where_conditions["contract_type"] = contract_type
            
            # Perform vector search
            results = self.contracts_collection.query(
                query_texts=[query],
                n_results=limit,
                where=where_conditions
            )
            
            # Format results
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    result = {
                        'template_id': results['ids'][0][i],
                        'document': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i],
                        'relevance_score': 1 - results['distances'][0][i]
                    }
                    
                    # Parse JSON metadata fields
                    metadata = result['metadata']
                    for field in ['standard_clauses', 'optional_clauses']:
                        if field in metadata and metadata[field]:
                            try:
                                metadata[field] = json.loads(metadata[field])
                            except:
                                pass
                    
                    formatted_results.append(result)
            
            logger.info(f"Contract template search returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search contract templates: {str(e)}")
            return []
    
    def search_legal_documents(self, query: str, attorney_id: str, client_id: str = None,
                             limit: int = 10) -> List[Dict[str, Any]]:
        """Search legal documents with privilege protection"""
        try:
            # Prepare search filters with privilege protection
            where_conditions = {
                "document_type_meta": "legal_document",
                "attorney_id": attorney_id
            }
            
            if client_id:
                where_conditions["client_id"] = client_id
            
            # Perform vector search
            results = self.documents_collection.query(
                query_texts=[query],
                n_results=limit,
                where=where_conditions
            )
            
            # Format results
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    result = {
                        'document_id': results['ids'][0][i],
                        'document': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i],
                        'relevance_score': 1 - results['distances'][0][i]
                    }
                    formatted_results.append(result)
            
            logger.info(f"Legal document search returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search legal documents: {str(e)}")
            return []
    
    def hybrid_legal_search(self, query: str, jurisdiction: str = None, limit: int = 20) -> Dict[str, Any]:
        """Perform hybrid search across all legal document types"""
        try:
            search_results = {
                'query': query,
                'jurisdiction': jurisdiction,
                'case_law': self.search_case_law(query, jurisdiction, limit//4),
                'statutes': self.search_statutes(query, jurisdiction, limit//4),
                'precedents': self.search_precedents(query, jurisdiction, limit//4),
                'contract_templates': self.search_contract_templates(query, None, limit//4),
                'total_results': 0
            }
            
            # Calculate total results
            search_results['total_results'] = (
                len(search_results['case_law']) +
                len(search_results['statutes']) +
                len(search_results['precedents']) +
                len(search_results['contract_templates'])
            )
            
            # Rank all results by relevance
            all_results = []
            
            for result in search_results['case_law']:
                result['source_type'] = 'case_law'
                all_results.append(result)
            
            for result in search_results['statutes']:
                result['source_type'] = 'statute'
                all_results.append(result)
            
            for result in search_results['precedents']:
                result['source_type'] = 'precedent'
                all_results.append(result)
            
            for result in search_results['contract_templates']:
                result['source_type'] = 'contract_template'
                all_results.append(result)
            
            # Sort by relevance score
            all_results.sort(key=lambda x: x['relevance_score'], reverse=True)
            search_results['ranked_results'] = all_results[:limit]
            
            logger.info(f"Hybrid legal search returned {search_results['total_results']} results")
            return search_results
            
        except Exception as e:
            logger.error(f"Failed to perform hybrid legal search: {str(e)}")
            return {'query': query, 'total_results': 0, 'error': str(e)}
    
    def find_similar_cases(self, case_facts: str, legal_issues: List[str],
                          jurisdiction: str = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Find cases with similar fact patterns and legal issues"""
        try:
            # Combine facts and issues for search
            search_query = f"Facts: {case_facts} Issues: {', '.join(legal_issues)}"
            
            # Search for similar cases
            similar_cases = self.search_case_law(
                search_query, 
                jurisdiction, 
                limit * 2  # Get more to filter better matches
            )
            
            # Enhanced similarity scoring
            scored_cases = []
            for case in similar_cases:
                similarity_score = self._calculate_case_similarity(
                    case_facts, legal_issues, case
                )
                case['similarity_score'] = similarity_score
                if similarity_score > 0.3:  # Threshold for relevance
                    scored_cases.append(case)
            
            # Sort by similarity and return top results
            scored_cases.sort(key=lambda x: x['similarity_score'], reverse=True)
            return scored_cases[:limit]
            
        except Exception as e:
            logger.error(f"Failed to find similar cases: {str(e)}")
            return []
    
    def _calculate_case_similarity(self, case_facts: str, legal_issues: List[str],
                                 case_result: Dict[str, Any]) -> float:
        """Calculate similarity score between case facts/issues and search result"""
        try:
            base_score = case_result.get('relevance_score', 0)
            
            # Get case metadata
            metadata = case_result.get('metadata', {})
            case_issues = metadata.get('legal_issues', [])
            
            # Parse legal issues if they're in JSON format
            if isinstance(case_issues, str):
                try:
                    case_issues = json.loads(case_issues)
                except:
                    case_issues = [case_issues]
            
            # Issue similarity bonus
            issue_matches = 0
            if case_issues:
                for target_issue in legal_issues:
                    for case_issue in case_issues:
                        if (target_issue.lower() in case_issue.lower() or 
                            case_issue.lower() in target_issue.lower()):
                            issue_matches += 1
                
                issue_similarity = min(1.0, issue_matches / len(legal_issues))
                base_score = (base_score * 0.7) + (issue_similarity * 0.3)
            
            return base_score
            
        except Exception as e:
            logger.error(f"Failed to calculate case similarity: {str(e)}")
            return case_result.get('relevance_score', 0)
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about legal knowledge collections"""
        try:
            stats = {
                'case_law_count': self.case_law_collection.count(),
                'statutes_count': self.statutes_collection.count(),
                'precedents_count': self.precedents_collection.count(),
                'contracts_count': self.contracts_collection.count(),
                'documents_count': self.documents_collection.count(),
                'regulations_count': self.regulations_collection.count(),
                'total_documents': 0,
                'embedding_model': 'all-MiniLM-L6-v2',
                'last_updated': datetime.now().isoformat()
            }
            
            stats['total_documents'] = sum([
                stats['case_law_count'],
                stats['statutes_count'],
                stats['precedents_count'],
                stats['contracts_count'],
                stats['documents_count'],
                stats['regulations_count']
            ])
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get collection stats: {str(e)}")
            return {}
    
    def _generate_case_id(self, case_data: Dict[str, Any]) -> str:
        """Generate unique ID for case law"""
        case_name = case_data.get('case_name', '')
        citation = case_data.get('citation', '')
        content = f"{case_name}_{citation}_{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _generate_statute_id(self, statute_data: Dict[str, Any]) -> str:
        """Generate unique ID for statute"""
        title = statute_data.get('title', '')
        citation = statute_data.get('citation', '')
        content = f"{title}_{citation}_{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _generate_precedent_id(self, precedent_data: Dict[str, Any]) -> str:
        """Generate unique ID for precedent"""
        principle = precedent_data.get('legal_principle', '')
        jurisdiction = precedent_data.get('jurisdiction', '')
        content = f"{principle}_{jurisdiction}_{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _generate_template_id(self, contract_data: Dict[str, Any]) -> str:
        """Generate unique ID for contract template"""
        name = contract_data.get('template_name', '')
        contract_type = contract_data.get('contract_type', '')
        content = f"{name}_{contract_type}_{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _generate_document_id(self, document_data: Dict[str, Any]) -> str:
        """Generate unique ID for legal document"""
        title = document_data.get('document_title', '')
        doc_type = document_data.get('document_type', '')
        attorney = document_data.get('attorney_id', '')
        content = f"{title}_{doc_type}_{attorney}_{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def health_check(self) -> bool:
        """Check if ChromaDB is working properly"""
        try:
            # Test each collection
            collections = [
                self.case_law_collection,
                self.statutes_collection,
                self.precedents_collection,
                self.contracts_collection,
                self.documents_collection,
                self.regulations_collection
            ]
            
            for collection in collections:
                collection.count()  # This will fail if collection is not accessible
            
            return True
            
        except Exception as e:
            logger.error(f"Legal knowledge store health check failed: {str(e)}")
<<<<<<< HEAD
            return False

    # Additional methods needed by agents
    def search_cases_by_issue(self, legal_issue: str, jurisdiction: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search cases by legal issue"""
        return self.search_case_law(legal_issue, jurisdiction, limit)
    
    def search_cases_by_facts(self, case_facts: str, jurisdiction: str, limit: int = 15) -> List[Dict[str, Any]]:
        """Search cases by fact patterns"""
        return self.search_case_law(case_facts, jurisdiction, limit)
    
    def search_by_legal_principle(self, legal_issue: str, jurisdiction: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search by legal principle"""
        return self.search_precedents(legal_issue, jurisdiction, limit)
    
    def search_citation_network(self, cases: List[Dict], limit: int = 10) -> List[Dict[str, Any]]:
        """Search citation network - simplified implementation"""
        if not cases:
            return []
        # For now, return a subset of the input cases as this would require complex citation analysis
        return cases[:limit]
    
    def search_legal_authorities(self, issue: str, jurisdiction: str) -> Dict[str, List]:
        """Search for legal authorities"""
        return {
            'binding_cases': self.search_case_law(issue, jurisdiction, 5),
            'persuasive_cases': self.search_case_law(issue, None, 5),
            'statutes': self.search_statutes(issue, jurisdiction, 3)
        }
    
    def search_regulations(self, query: str, jurisdiction: str = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Search regulations using RAG"""
        try:
            # Prepare search filters
            where_conditions = {"document_type": "regulation"}
            
            if jurisdiction:
                where_conditions["jurisdiction"] = jurisdiction
            
            # Perform vector search
            results = self.regulations_collection.query(
                query_texts=[query],
                n_results=limit,
                where=where_conditions
            )
            
            # Format results
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    result = {
                        'regulation_id': results['ids'][0][i],
                        'document': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i],
                        'relevance_score': 1 - results['distances'][0][i]
                    }
                    formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search regulations: {str(e)}")
            return []
=======
            return False
>>>>>>> 6c3aac01d38711e21958dc83ff6d611bbc727be6
