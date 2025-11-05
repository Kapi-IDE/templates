#!/usr/bin/env python3
"""
SQLite Manager for Legal AI System
Handles legal data, attorney-client privileged communications, and compliance audit logs
"""

import sqlite3
import json
import logging
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import uuid
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class LegalDataManager:
    """
    Manages legal data and privileged communications in SQLite database
    Ensures attorney-client privilege protection with encryption and compliance audit logging
    """
    
    def __init__(self, db_path: str = "./legal_data.db"):
        """Initialize SQLite database and create legal tables"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable dict-like access
        
        # Initialize encryption for privileged communications
        self.encryption_key = os.getenv('LEGAL_ENCRYPTION_KEY')
        if not self.encryption_key:
            # Generate key for demo (DO NOT do this in production)
            self.encryption_key = Fernet.generate_key()
            logger.warning("Generated encryption key for demo - use proper key management in production")
        
        self.cipher = Fernet(self.encryption_key)
        
        self._create_legal_tables()
        logger.info("Legal SQLite database initialized successfully")
    
    def _create_legal_tables(self):
        """Create database tables for legal data management"""
        try:
            # Attorneys table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS attorneys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    attorney_id TEXT UNIQUE NOT NULL,
                    bar_number TEXT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    law_firm TEXT,
                    email TEXT,
                    phone TEXT,
                    practice_areas TEXT,
                    jurisdiction TEXT,
                    bar_admission_date DATE,
                    active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Clients table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id TEXT UNIQUE NOT NULL,
                    client_type TEXT DEFAULT 'individual', -- individual, corporate, government
                    first_name TEXT,
                    last_name TEXT,
                    company_name TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    case_matter_type TEXT,
                    retainer_status TEXT DEFAULT 'pending',
                    conflict_checked BOOLEAN DEFAULT 0,
                    privilege_waived BOOLEAN DEFAULT 0,
                    active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Attorney-Client Relationships table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS attorney_client_relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    relationship_id TEXT UNIQUE NOT NULL,
                    attorney_id TEXT NOT NULL,
                    client_id TEXT NOT NULL,
                    matter_description TEXT,
                    engagement_date DATE,
                    termination_date DATE,
                    relationship_status TEXT DEFAULT 'active', -- active, terminated, suspended
                    privilege_status TEXT DEFAULT 'privileged',
                    retainer_amount DECIMAL(10,2),
                    billing_rate DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (attorney_id) REFERENCES attorneys (attorney_id),
                    FOREIGN KEY (client_id) REFERENCES clients (client_id),
                    UNIQUE(attorney_id, client_id)
                )
            ''')
            
            # Legal Cases table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS legal_cases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id TEXT UNIQUE NOT NULL,
                    attorney_id TEXT NOT NULL,
                    client_id TEXT NOT NULL,
                    case_number TEXT,
                    case_title TEXT,
                    case_type TEXT, -- litigation, transactional, advisory, etc.
                    jurisdiction TEXT,
                    court_name TEXT,
                    case_status TEXT DEFAULT 'active',
                    filed_date DATE,
                    statute_of_limitations DATE,
                    encrypted_case_summary TEXT,
                    practice_area TEXT,
                    opposing_party TEXT,
                    opposing_counsel TEXT,
                    estimated_value DECIMAL(15,2),
                    priority_level TEXT DEFAULT 'medium',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (attorney_id) REFERENCES attorneys (attorney_id),
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
                )
            ''')
            
            # Privileged Communications table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS privileged_communications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    communication_id TEXT UNIQUE NOT NULL,
                    attorney_id TEXT NOT NULL,
                    client_id TEXT NOT NULL,
                    case_id TEXT,
                    communication_type TEXT, -- email, phone, meeting, document_review, legal_advice
                    encrypted_content TEXT NOT NULL,
                    communication_date TIMESTAMP NOT NULL,
                    duration_minutes INTEGER,
                    participants TEXT, -- JSON array of participants
                    privilege_level TEXT DEFAULT 'full_privilege',
                    work_product_protection BOOLEAN DEFAULT 1,
                    confidentiality_level TEXT DEFAULT 'attorney_client',
                    retention_policy TEXT DEFAULT 'client_relationship_plus_7_years',
                    access_log TEXT, -- JSON log of who accessed this communication
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (attorney_id) REFERENCES attorneys (attorney_id),
                    FOREIGN KEY (client_id) REFERENCES clients (client_id),
                    FOREIGN KEY (case_id) REFERENCES legal_cases (case_id)
                )
            ''')
            
            # Legal Documents table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS legal_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id TEXT UNIQUE NOT NULL,
                    attorney_id TEXT NOT NULL,
                    client_id TEXT,
                    case_id TEXT,
                    document_type TEXT, -- contract, brief, motion, discovery, correspondence
                    document_title TEXT NOT NULL,
                    document_status TEXT DEFAULT 'draft', -- draft, review, final, executed
                    encrypted_content TEXT,
                    document_hash TEXT, -- for integrity verification
                    version_number INTEGER DEFAULT 1,
                    privilege_protected BOOLEAN DEFAULT 1,
                    work_product BOOLEAN DEFAULT 0,
                    confidential BOOLEAN DEFAULT 1,
                    file_path TEXT,
                    file_size INTEGER,
                    mime_type TEXT,
                    created_by TEXT,
                    reviewed_by TEXT,
                    approved_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (attorney_id) REFERENCES attorneys (attorney_id),
                    FOREIGN KEY (client_id) REFERENCES clients (client_id),
                    FOREIGN KEY (case_id) REFERENCES legal_cases (case_id)
                )
            ''')
            
            # Case Law Database table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS case_law (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_law_id TEXT UNIQUE NOT NULL,
                    case_name TEXT NOT NULL,
                    citation TEXT NOT NULL,
                    court TEXT,
                    jurisdiction TEXT,
                    decision_date DATE,
                    judge_name TEXT,
                    legal_issues TEXT, -- JSON array
                    holding TEXT,
                    key_facts TEXT,
                    legal_reasoning TEXT,
                    precedent_type TEXT DEFAULT 'binding', -- binding, persuasive
                    overruled BOOLEAN DEFAULT 0,
                    overruled_by TEXT,
                    citation_count INTEGER DEFAULT 0,
                    relevance_keywords TEXT, -- JSON array
                    practice_areas TEXT, -- JSON array
                    full_text TEXT,
                    summary TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Statutes table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS statutes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    statute_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    citation TEXT NOT NULL,
                    jurisdiction TEXT,
                    chapter TEXT,
                    section TEXT,
                    effective_date DATE,
                    amendment_date DATE,
                    statute_text TEXT,
                    summary TEXT,
                    keywords TEXT, -- JSON array
                    practice_areas TEXT, -- JSON array
                    related_regulations TEXT, -- JSON array
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Legal Precedents table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS legal_precedents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    precedent_id TEXT UNIQUE NOT NULL,
                    case_law_id TEXT,
                    legal_principle TEXT NOT NULL,
                    precedent_weight INTEGER DEFAULT 5, -- 1-10 scale
                    binding_authority TEXT,
                    jurisdiction TEXT,
                    practice_area TEXT,
                    fact_pattern TEXT,
                    legal_standard TEXT,
                    exceptions TEXT,
                    related_precedents TEXT, -- JSON array
                    overruled BOOLEAN DEFAULT 0,
                    limited_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (case_law_id) REFERENCES case_law (case_law_id)
                )
            ''')
            
            # Contract Templates table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS contract_templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    template_id TEXT UNIQUE NOT NULL,
                    template_name TEXT NOT NULL,
                    contract_type TEXT,
                    jurisdiction TEXT,
                    practice_area TEXT,
                    template_content TEXT,
                    template_variables TEXT, -- JSON array of variables
                    standard_clauses TEXT, -- JSON array
                    optional_clauses TEXT, -- JSON array
                    risk_level TEXT DEFAULT 'medium',
                    complexity_level TEXT DEFAULT 'medium',
                    usage_count INTEGER DEFAULT 0,
                    last_updated DATE,
                    created_by TEXT,
                    approved_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Ethics Compliance Audit Log table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS ethics_audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    audit_id TEXT UNIQUE NOT NULL,
                    attorney_id TEXT,
                    client_id TEXT,
                    action_type TEXT NOT NULL, -- privilege_access, conflict_check, disclosure, billing
                    action_description TEXT,
                    compliance_rule TEXT, -- specific ethics rule or regulation
                    compliance_status TEXT, -- compliant, violation, warning, review_required
                    privilege_impact BOOLEAN DEFAULT 0,
                    confidentiality_impact BOOLEAN DEFAULT 0,
                    conflict_impact BOOLEAN DEFAULT 0,
                    audit_details TEXT, -- JSON with detailed audit information
                    remedial_action TEXT,
                    responsible_attorney TEXT,
                    review_required BOOLEAN DEFAULT 0,
                    resolved BOOLEAN DEFAULT 0,
                    ip_address TEXT,
                    user_agent TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (attorney_id) REFERENCES attorneys (attorney_id),
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
                )
            ''')
            
            # Legal AI Interactions table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS ai_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    interaction_id TEXT UNIQUE NOT NULL,
                    attorney_id TEXT,
                    client_id TEXT,
                    case_id TEXT,
                    agent_type TEXT, -- research, case_analysis, document_review, precedent_mining
                    interaction_type TEXT,
                    encrypted_query TEXT,
                    encrypted_response TEXT,
                    confidence_score DECIMAL(3,2),
                    processing_time_seconds DECIMAL(8,3),
                    privilege_protected BOOLEAN DEFAULT 1,
                    ethical_review_required BOOLEAN DEFAULT 0,
                    human_oversight_required BOOLEAN DEFAULT 0,
                    session_id TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (attorney_id) REFERENCES attorneys (attorney_id),
                    FOREIGN KEY (client_id) REFERENCES clients (client_id),
                    FOREIGN KEY (case_id) REFERENCES legal_cases (case_id)
                )
            ''')
            
            # Create indexes for better performance
            indexes = [
                'CREATE INDEX IF NOT EXISTS idx_attorney_client_rel_attorney ON attorney_client_relationships(attorney_id)',
                'CREATE INDEX IF NOT EXISTS idx_attorney_client_rel_client ON attorney_client_relationships(client_id)',
                'CREATE INDEX IF NOT EXISTS idx_legal_cases_attorney ON legal_cases(attorney_id)',
                'CREATE INDEX IF NOT EXISTS idx_legal_cases_client ON legal_cases(client_id)',
                'CREATE INDEX IF NOT EXISTS idx_privileged_comm_attorney ON privileged_communications(attorney_id)',
                'CREATE INDEX IF NOT EXISTS idx_privileged_comm_client ON privileged_communications(client_id)',
                'CREATE INDEX IF NOT EXISTS idx_privileged_comm_case ON privileged_communications(case_id)',
                'CREATE INDEX IF NOT EXISTS idx_privileged_comm_date ON privileged_communications(communication_date)',
                'CREATE INDEX IF NOT EXISTS idx_legal_docs_attorney ON legal_documents(attorney_id)',
                'CREATE INDEX IF NOT EXISTS idx_legal_docs_client ON legal_documents(client_id)',
                'CREATE INDEX IF NOT EXISTS idx_legal_docs_case ON legal_documents(case_id)',
                'CREATE INDEX IF NOT EXISTS idx_case_law_jurisdiction ON case_law(jurisdiction)',
                'CREATE INDEX IF NOT EXISTS idx_case_law_date ON case_law(decision_date)',
                'CREATE INDEX IF NOT EXISTS idx_case_law_citation ON case_law(citation)',
                'CREATE INDEX IF NOT EXISTS idx_statutes_jurisdiction ON statutes(jurisdiction)',
                'CREATE INDEX IF NOT EXISTS idx_statutes_citation ON statutes(citation)',
                'CREATE INDEX IF NOT EXISTS idx_precedents_jurisdiction ON legal_precedents(jurisdiction)',
                'CREATE INDEX IF NOT EXISTS idx_precedents_practice ON legal_precedents(practice_area)',
                'CREATE INDEX IF NOT EXISTS idx_ethics_audit_attorney ON ethics_audit_log(attorney_id)',
                'CREATE INDEX IF NOT EXISTS idx_ethics_audit_timestamp ON ethics_audit_log(timestamp)',
                'CREATE INDEX IF NOT EXISTS idx_ai_interactions_attorney ON ai_interactions(attorney_id)',
                'CREATE INDEX IF NOT EXISTS idx_ai_interactions_timestamp ON ai_interactions(timestamp)'
            ]
            
            for index_sql in indexes:
                self.conn.execute(index_sql)
            
            self.conn.commit()
            logger.info("Legal database tables created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create legal database tables: {str(e)}")
            raise
    
    def _encrypt_privileged_data(self, data: str) -> str:
        """Encrypt privileged attorney-client data"""
        try:
            if isinstance(data, dict) or isinstance(data, list):
                data = json.dumps(data)
            return self.cipher.encrypt(data.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt privileged data: {str(e)}")
            raise
    
    def _decrypt_privileged_data(self, encrypted_data: str) -> str:
        """Decrypt privileged attorney-client data"""
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to decrypt privileged data: {str(e)}")
            raise
    
    def create_attorney(self, attorney_data: Dict[str, Any]) -> bool:
        """Create a new attorney record"""
        try:
            attorney_id = attorney_data.get('attorney_id', str(uuid.uuid4()))
            
            self.conn.execute('''
                INSERT OR REPLACE INTO attorneys 
                (attorney_id, bar_number, first_name, last_name, law_firm, email, phone,
                 practice_areas, jurisdiction, bar_admission_date, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                attorney_id,
                attorney_data.get('bar_number'),
                attorney_data.get('first_name'),
                attorney_data.get('last_name'),
                attorney_data.get('law_firm'),
                attorney_data.get('email'),
                attorney_data.get('phone'),
                json.dumps(attorney_data.get('practice_areas', [])),
                attorney_data.get('jurisdiction'),
                attorney_data.get('bar_admission_date')
            ))
            
            self.conn.commit()
            
            # Log attorney creation
            self.log_ethics_audit_event(
                attorney_id=attorney_id,
                action_type='attorney_created',
                action_description='New attorney record created',
                compliance_status='compliant'
            )
            
            logger.info(f"Attorney {attorney_id} created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create attorney: {str(e)}")
            self.conn.rollback()
            return False
    
    def create_client(self, client_data: Dict[str, Any]) -> bool:
        """Create a new client record"""
        try:
            client_id = client_data.get('client_id', str(uuid.uuid4()))
            
            self.conn.execute('''
                INSERT OR REPLACE INTO clients 
                (client_id, client_type, first_name, last_name, company_name, email, phone,
                 address, case_matter_type, retainer_status, conflict_checked, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                client_id,
                client_data.get('client_type', 'individual'),
                client_data.get('first_name'),
                client_data.get('last_name'),
                client_data.get('company_name'),
                client_data.get('email'),
                client_data.get('phone'),
                client_data.get('address'),
                client_data.get('case_matter_type'),
                client_data.get('retainer_status', 'pending'),
                client_data.get('conflict_checked', False)
            ))
            
            self.conn.commit()
            
            # Log client creation
            self.log_ethics_audit_event(
                client_id=client_id,
                action_type='client_created',
                action_description='New client record created',
                compliance_status='compliant'
            )
            
            logger.info(f"Client {client_id} created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create client: {str(e)}")
            self.conn.rollback()
            return False
    
    def create_attorney_client_relationship(self, attorney_id: str, client_id: str,
                                          relationship_data: Dict[str, Any]) -> str:
        """Create attorney-client relationship with privilege protection"""
        try:
            relationship_id = str(uuid.uuid4())
            
            # Verify attorney and client exist
            if not self.get_attorney(attorney_id) or not self.get_client(client_id):
                raise ValueError("Attorney or client not found")
            
            # Check for conflicts of interest
            conflict_check_result = self.check_conflicts_of_interest(attorney_id, client_id)
            if not conflict_check_result['can_represent']:
                raise ValueError(f"Conflict of interest detected: {conflict_check_result['conflict_reason']}")
            
            self.conn.execute('''
                INSERT INTO attorney_client_relationships 
                (relationship_id, attorney_id, client_id, matter_description, engagement_date,
                 relationship_status, privilege_status, retainer_amount, billing_rate, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                relationship_id,
                attorney_id,
                client_id,
                relationship_data.get('matter_description'),
                relationship_data.get('engagement_date', datetime.now().date()),
                relationship_data.get('relationship_status', 'active'),
                relationship_data.get('privilege_status', 'privileged'),
                relationship_data.get('retainer_amount'),
                relationship_data.get('billing_rate')
            ))
            
            self.conn.commit()
            
            # Log relationship creation
            self.log_ethics_audit_event(
                attorney_id=attorney_id,
                client_id=client_id,
                action_type='attorney_client_relationship_created',
                action_description=f'Attorney-client relationship established: {relationship_id}',
                compliance_status='compliant',
                privilege_impact=True
            )
            
            logger.info(f"Attorney-client relationship {relationship_id} created successfully")
            return relationship_id
            
        except Exception as e:
            logger.error(f"Failed to create attorney-client relationship: {str(e)}")
            self.conn.rollback()
            raise
    
    def verify_attorney_client_relationship(self, attorney_id: str, client_id: str) -> bool:
        """Verify if valid attorney-client relationship exists"""
        try:
            cursor = self.conn.execute('''
                SELECT relationship_status, privilege_status FROM attorney_client_relationships
                WHERE attorney_id = ? AND client_id = ? 
                AND relationship_status = 'active'
                AND privilege_status IN ('privileged', 'limited_privilege')
            ''', (attorney_id, client_id))
            
            relationship = cursor.fetchone()
            
            # Log access attempt
            self.log_ethics_audit_event(
                attorney_id=attorney_id,
                client_id=client_id,
                action_type='privilege_access_verification',
                action_description='Verified attorney-client relationship for privileged access',
                compliance_status='compliant' if relationship else 'violation',
                privilege_impact=True
            )
            
            return relationship is not None
            
        except Exception as e:
            logger.error(f"Failed to verify attorney-client relationship: {str(e)}")
            return False
    
    def store_privileged_communication(self, attorney_id: str, client_id: str,
                                     communication_data: Dict[str, Any]) -> str:
        """Store privileged attorney-client communication"""
        try:
            # Verify attorney-client relationship
            if not self.verify_attorney_client_relationship(attorney_id, client_id):
                raise PermissionError("No valid attorney-client relationship found")
            
            communication_id = str(uuid.uuid4())
            
            # Encrypt the communication content
            encrypted_content = self._encrypt_privileged_data(communication_data.get('content', ''))
            
            self.conn.execute('''
                INSERT INTO privileged_communications 
                (communication_id, attorney_id, client_id, case_id, communication_type,
                 encrypted_content, communication_date, duration_minutes, participants,
                 privilege_level, work_product_protection, confidentiality_level,
                 retention_policy, access_log)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                communication_id,
                attorney_id,
                client_id,
                communication_data.get('case_id'),
                communication_data.get('communication_type', 'legal_advice'),
                encrypted_content,
                communication_data.get('communication_date', datetime.now()),
                communication_data.get('duration_minutes'),
                json.dumps(communication_data.get('participants', [])),
                communication_data.get('privilege_level', 'full_privilege'),
                communication_data.get('work_product_protection', True),
                communication_data.get('confidentiality_level', 'attorney_client'),
                communication_data.get('retention_policy', 'client_relationship_plus_7_years'),
                json.dumps([{
                    'timestamp': datetime.now().isoformat(),
                    'action': 'created',
                    'user': attorney_id
                }])
            ))
            
            self.conn.commit()
            
            # Log privileged communication storage
            self.log_ethics_audit_event(
                attorney_id=attorney_id,
                client_id=client_id,
                action_type='privileged_communication_stored',
                action_description=f'Privileged communication stored: {communication_id}',
                compliance_status='compliant',
                privilege_impact=True,
                confidentiality_impact=True
            )
            
            logger.info(f"Privileged communication {communication_id} stored successfully")
            return communication_id
            
        except Exception as e:
            logger.error(f"Failed to store privileged communication: {str(e)}")
            self.conn.rollback()
            raise
    
    def get_privileged_communications(self, attorney_id: str, client_id: str,
                                    case_id: str = None, limit: int = 50) -> List[Dict]:
        """Retrieve privileged communications with proper access control"""
        try:
            # Verify attorney-client relationship
            if not self.verify_attorney_client_relationship(attorney_id, client_id):
                raise PermissionError("No valid attorney-client relationship found")
            
            query = '''
                SELECT communication_id, communication_type, communication_date,
                       duration_minutes, participants, privilege_level,
                       encrypted_content, confidentiality_level
                FROM privileged_communications
                WHERE attorney_id = ? AND client_id = ?
            '''
            params = [attorney_id, client_id]
            
            if case_id:
                query += ' AND case_id = ?'
                params.append(case_id)
            
            query += ' ORDER BY communication_date DESC LIMIT ?'
            params.append(limit)
            
            cursor = self.conn.execute(query, params)
            communications = []
            
            for row in cursor.fetchall():
                communication = dict(row)
                
                # Decrypt content for authorized access
                try:
                    decrypted_content = self._decrypt_privileged_data(communication['encrypted_content'])
                    communication['content'] = json.loads(decrypted_content)
                except Exception as e:
                    logger.error(f"Failed to decrypt communication {communication['communication_id']}: {str(e)}")
                    continue
                
                # Remove encrypted field from response
                del communication['encrypted_content']
                
                # Update access log
                self._log_privileged_access(communication['communication_id'], attorney_id)
                
                communications.append(communication)
            
            # Log privileged access
            self.log_ethics_audit_event(
                attorney_id=attorney_id,
                client_id=client_id,
                action_type='privileged_communications_accessed',
                action_description=f'Retrieved {len(communications)} privileged communications',
                compliance_status='compliant',
                privilege_impact=True
            )
            
            return communications
            
        except Exception as e:
            logger.error(f"Failed to retrieve privileged communications: {str(e)}")
            if "No valid attorney-client relationship" in str(e):
                # Log privilege violation
                self.log_ethics_audit_event(
                    attorney_id=attorney_id,
                    client_id=client_id,
                    action_type='privileged_access_denied',
                    action_description='Attempted access to privileged communications without valid relationship',
                    compliance_status='violation',
                    privilege_impact=True
                )
            raise
    
    def _log_privileged_access(self, communication_id: str, accessing_attorney_id: str):
        """Log access to privileged communication"""
        try:
            # Get current access log
            cursor = self.conn.execute('''
                SELECT access_log FROM privileged_communications 
                WHERE communication_id = ?
            ''', (communication_id,))
            
            result = cursor.fetchone()
            if result:
                access_log = json.loads(result[0] or '[]')
                access_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'action': 'accessed',
                    'user': accessing_attorney_id
                })
                
                # Update access log
                self.conn.execute('''
                    UPDATE privileged_communications 
                    SET access_log = ?
                    WHERE communication_id = ?
                ''', (json.dumps(access_log), communication_id))
                
                self.conn.commit()
                
        except Exception as e:
            logger.error(f"Failed to log privileged access: {str(e)}")
    
    def check_conflicts_of_interest(self, attorney_id: str, new_client_id: str) -> Dict[str, Any]:
        """Check for conflicts of interest before establishing attorney-client relationship"""
        try:
            # Get existing clients for this attorney
            cursor = self.conn.execute('''
                SELECT c.client_id, c.first_name, c.last_name, c.company_name,
                       r.matter_description, r.relationship_status
                FROM clients c
                JOIN attorney_client_relationships r ON c.client_id = r.client_id
                WHERE r.attorney_id = ? AND r.relationship_status = 'active'
            ''', (attorney_id,))
            
            existing_clients = cursor.fetchall()
            
            # Get new client information
            new_client = self.get_client(new_client_id)
            if not new_client:
                return {'can_represent': False, 'conflict_reason': 'Client not found'}
            
            # Basic conflict checking logic (would be more sophisticated in production)
            conflicts = []
            
            for existing_client in existing_clients:
                # Check for same client (should not be a conflict, but worth noting)
                if existing_client[0] == new_client_id:
                    conflicts.append({
                        'type': 'existing_client',
                        'description': 'Client relationship already exists'
                    })
                
                # Check for potential business conflicts (same company name)
                if (new_client.get('company_name') and 
                    existing_client[3] and 
                    new_client['company_name'].lower() == existing_client[3].lower()):
                    conflicts.append({
                        'type': 'potential_business_conflict',
                        'description': f'Same company name as existing client: {existing_client[3]}'
                    })
            
            # Log conflict check
            self.log_ethics_audit_event(
                attorney_id=attorney_id,
                client_id=new_client_id,
                action_type='conflict_check_performed',
                action_description=f'Conflict check completed: {len(conflicts)} potential conflicts found',
                compliance_status='compliant',
                conflict_impact=True,
                audit_details=json.dumps({
                    'conflicts_found': len(conflicts),
                    'conflict_details': conflicts
                })
            )
            
            can_represent = len(conflicts) == 0 or all(c['type'] == 'existing_client' for c in conflicts)
            
            return {
                'can_represent': can_represent,
                'conflicts_found': conflicts,
                'conflict_reason': conflicts[0]['description'] if conflicts and not can_represent else None,
                'requires_waiver': len(conflicts) > 0 and can_represent
            }
            
        except Exception as e:
            logger.error(f"Failed to check conflicts of interest: {str(e)}")
            return {'can_represent': False, 'conflict_reason': f'Error checking conflicts: {str(e)}'}
    
    def store_ai_interaction(self, attorney_id: str, client_id: str, interaction_data: Dict[str, Any]) -> str:
        """Store AI interaction with privilege protection"""
        try:
            # Verify attorney-client relationship if both IDs provided
            if attorney_id and client_id:
                if not self.verify_attorney_client_relationship(attorney_id, client_id):
                    raise PermissionError("No valid attorney-client relationship found")
            
            interaction_id = str(uuid.uuid4())
            
            # Encrypt query and response
            encrypted_query = self._encrypt_privileged_data(interaction_data.get('query', ''))
            encrypted_response = self._encrypt_privileged_data(interaction_data.get('response', ''))
            
            self.conn.execute('''
                INSERT INTO ai_interactions 
                (interaction_id, attorney_id, client_id, case_id, agent_type, interaction_type,
                 encrypted_query, encrypted_response, confidence_score, processing_time_seconds,
                 privilege_protected, ethical_review_required, human_oversight_required, session_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                interaction_id,
                attorney_id,
                client_id,
                interaction_data.get('case_id'),
                interaction_data.get('agent_type'),
                interaction_data.get('interaction_type'),
                encrypted_query,
                encrypted_response,
                interaction_data.get('confidence_score'),
                interaction_data.get('processing_time_seconds'),
                interaction_data.get('privilege_protected', True),
                interaction_data.get('ethical_review_required', False),
                interaction_data.get('human_oversight_required', False),
                interaction_data.get('session_id')
            ))
            
            self.conn.commit()
            
            # Log AI interaction
            self.log_ethics_audit_event(
                attorney_id=attorney_id,
                client_id=client_id,
                action_type='ai_interaction_logged',
                action_description=f'AI interaction recorded: {interaction_data.get("agent_type")}',
                compliance_status='compliant',
                privilege_impact=True
            )
            
            return interaction_id
            
        except Exception as e:
            logger.error(f"Failed to store AI interaction: {str(e)}")
            self.conn.rollback()
            raise
    
    def log_ethics_audit_event(self, action_type: str, action_description: str,
                             compliance_status: str, attorney_id: str = None,
                             client_id: str = None, **kwargs) -> str:
        """Log ethics compliance audit event"""
        try:
            audit_id = str(uuid.uuid4())
            
            audit_details = {
                'privilege_impact': kwargs.get('privilege_impact', False),
                'confidentiality_impact': kwargs.get('confidentiality_impact', False),
                'conflict_impact': kwargs.get('conflict_impact', False),
                'additional_details': kwargs.get('audit_details', {}),
                'timestamp': datetime.now().isoformat()
            }
            
            self.conn.execute('''
                INSERT INTO ethics_audit_log 
                (audit_id, attorney_id, client_id, action_type, action_description,
                 compliance_rule, compliance_status, privilege_impact, confidentiality_impact,
                 conflict_impact, audit_details, remedial_action, responsible_attorney,
                 review_required, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                audit_id,
                attorney_id,
                client_id,
                action_type,
                action_description,
                kwargs.get('compliance_rule'),
                compliance_status,
                kwargs.get('privilege_impact', False),
                kwargs.get('confidentiality_impact', False),
                kwargs.get('conflict_impact', False),
                json.dumps(audit_details),
                kwargs.get('remedial_action'),
                kwargs.get('responsible_attorney', attorney_id),
                kwargs.get('review_required', compliance_status == 'violation'),
                kwargs.get('ip_address'),
                kwargs.get('user_agent')
            ))
            
            self.conn.commit()
            return audit_id
            
        except Exception as e:
            logger.error(f"Failed to log ethics audit event: {str(e)}")
            return None
    
    def get_attorney(self, attorney_id: str) -> Optional[Dict]:
        """Retrieve attorney information"""
        try:
            cursor = self.conn.execute('''
                SELECT * FROM attorneys WHERE attorney_id = ? AND active = 1
            ''', (attorney_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            attorney = dict(row)
            
            # Parse JSON fields
            if attorney['practice_areas']:
                try:
                    attorney['practice_areas'] = json.loads(attorney['practice_areas'])
                except:
                    attorney['practice_areas'] = []
            
            return attorney
            
        except Exception as e:
            logger.error(f"Failed to retrieve attorney {attorney_id}: {str(e)}")
            return None
    
    def get_client(self, client_id: str) -> Optional[Dict]:
        """Retrieve client information"""
        try:
            cursor = self.conn.execute('''
                SELECT * FROM clients WHERE client_id = ? AND active = 1
            ''', (client_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return dict(row)
            
        except Exception as e:
            logger.error(f"Failed to retrieve client {client_id}: {str(e)}")
            return None
    
    def search_case_law(self, query: str, jurisdiction: str = None, limit: int = 20) -> List[Dict]:
        """Search case law database"""
        try:
            base_query = '''
                SELECT case_law_id, case_name, citation, court, jurisdiction,
                       decision_date, legal_issues, holding, key_facts, 
                       precedent_type, citation_count, summary
                FROM case_law
                WHERE 1=1
            '''
            params = []
            
            # Add text search conditions
            search_conditions = []
            query_words = query.lower().split()
            
            for word in query_words:
                search_conditions.append('''
                    (LOWER(case_name) LIKE ? OR 
                     LOWER(holding) LIKE ? OR 
                     LOWER(key_facts) LIKE ? OR 
                     LOWER(legal_issues) LIKE ? OR
                     LOWER(summary) LIKE ?)
                ''')
                params.extend([f'%{word}%'] * 5)
            
            if search_conditions:
                base_query += ' AND (' + ' AND '.join(search_conditions) + ')'
            
            # Add jurisdiction filter
            if jurisdiction:
                base_query += ' AND LOWER(jurisdiction) LIKE ?'
                params.append(f'%{jurisdiction.lower()}%')
            
            # Order by relevance (citation count and recency)
            base_query += ' ORDER BY citation_count DESC, decision_date DESC LIMIT ?'
            params.append(limit)
            
            cursor = self.conn.execute(base_query, params)
            
            results = []
            for row in cursor.fetchall():
                case = dict(row)
                
                # Parse JSON fields
                if case['legal_issues']:
                    try:
                        case['legal_issues'] = json.loads(case['legal_issues'])
                    except:
                        case['legal_issues'] = [case['legal_issues']]
                
                results.append(case)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search case law: {str(e)}")
            return []
    
    def search_statutes(self, query: str, jurisdiction: str = None, limit: int = 10) -> List[Dict]:
        """Search statutes database"""
        try:
            base_query = '''
                SELECT statute_id, title, citation, jurisdiction, chapter, section,
                       effective_date, statute_text, summary, keywords, practice_areas
                FROM statutes
                WHERE 1=1
            '''
            params = []
            
            # Add text search conditions
            search_conditions = []
            query_words = query.lower().split()
            
            for word in query_words:
                search_conditions.append('''
                    (LOWER(title) LIKE ? OR 
                     LOWER(statute_text) LIKE ? OR 
                     LOWER(summary) LIKE ? OR 
                     LOWER(keywords) LIKE ?)
                ''')
                params.extend([f'%{word}%'] * 4)
            
            if search_conditions:
                base_query += ' AND (' + ' AND '.join(search_conditions) + ')'
            
            # Add jurisdiction filter
            if jurisdiction:
                base_query += ' AND LOWER(jurisdiction) LIKE ?'
                params.append(f'%{jurisdiction.lower()}%')
            
            base_query += ' ORDER BY effective_date DESC LIMIT ?'
            params.append(limit)
            
            cursor = self.conn.execute(base_query, params)
            
            results = []
            for row in cursor.fetchall():
                statute = dict(row)
                
                # Parse JSON fields
                for field in ['keywords', 'practice_areas']:
                    if statute[field]:
                        try:
                            statute[field] = json.loads(statute[field])
                        except:
                            statute[field] = [statute[field]]
                
                results.append(statute)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search statutes: {str(e)}")
            return []
    
    def search_precedents(self, query: str, jurisdiction: str = None, limit: int = 15) -> List[Dict]:
        """Search legal precedents database"""
        try:
            base_query = '''
                SELECT p.precedent_id, p.legal_principle, p.precedent_weight,
                       p.binding_authority, p.jurisdiction, p.practice_area,
                       p.fact_pattern, p.legal_standard, c.case_name, c.citation
                FROM legal_precedents p
                LEFT JOIN case_law c ON p.case_law_id = c.case_law_id
                WHERE p.overruled = 0
            '''
            params = []
            
            # Add text search conditions
            search_conditions = []
            query_words = query.lower().split()
            
            for word in query_words:
                search_conditions.append('''
                    (LOWER(p.legal_principle) LIKE ? OR 
                     LOWER(p.fact_pattern) LIKE ? OR 
                     LOWER(p.legal_standard) LIKE ? OR 
                     LOWER(c.case_name) LIKE ?)
                ''')
                params.extend([f'%{word}%'] * 4)
            
            if search_conditions:
                base_query += ' AND (' + ' AND '.join(search_conditions) + ')'
            
            # Add jurisdiction filter
            if jurisdiction:
                base_query += ' AND LOWER(p.jurisdiction) LIKE ?'
                params.append(f'%{jurisdiction.lower()}%')
            
            base_query += ' ORDER BY p.precedent_weight DESC LIMIT ?'
            params.append(limit)
            
            cursor = self.conn.execute(base_query, params)
            
            results = []
            for row in cursor.fetchall():
                precedent = dict(row)
                results.append(precedent)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search precedents: {str(e)}")
            return []
    
    def get_ethics_audit_summary(self, attorney_id: str = None, days: int = 30) -> Dict[str, Any]:
        """Get ethics compliance audit summary"""
        try:
            since_date = datetime.now() - timedelta(days=days)
            
            base_query = 'SELECT * FROM ethics_audit_log WHERE timestamp > ?'
            params = [since_date]
            
            if attorney_id:
                base_query += ' AND attorney_id = ?'
                params.append(attorney_id)
            
            cursor = self.conn.execute(base_query, params)
            audit_logs = cursor.fetchall()
            
            # Analyze audit logs
            summary = {
                'total_events': len(audit_logs),
                'compliance_violations': len([log for log in audit_logs if dict(log)['compliance_status'] == 'violation']),
                'privilege_impacts': len([log for log in audit_logs if dict(log)['privilege_impact']]),
                'confidentiality_impacts': len([log for log in audit_logs if dict(log)['confidentiality_impact']]),
                'conflict_impacts': len([log for log in audit_logs if dict(log)['conflict_impact']]),
                'events_requiring_review': len([log for log in audit_logs if dict(log)['review_required']]),
                'date_range': f"{since_date.strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}"
            }
            
            # Calculate compliance score
            if summary['total_events'] > 0:
                compliance_score = ((summary['total_events'] - summary['compliance_violations']) / 
                                  summary['total_events']) * 100
                summary['compliance_score'] = round(compliance_score, 2)
            else:
                summary['compliance_score'] = 100.0
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get ethics audit summary: {str(e)}")
            return {}
    
    def health_check(self) -> bool:
        """Verify database is working properly"""
        try:
            cursor = self.conn.execute('SELECT 1')
            cursor.fetchone()
            return True
        except Exception as e:
            logger.error(f"Legal database health check failed: {str(e)}")
            return False
    
    def get_database_stats(self) -> Dict[str, int]:
        """Get legal database statistics"""
        try:
            stats = {}
            
            tables = [
                'attorneys', 'clients', 'attorney_client_relationships', 'legal_cases',
                'privileged_communications', 'legal_documents', 'case_law', 'statutes',
                'legal_precedents', 'contract_templates', 'ethics_audit_log', 'ai_interactions'
            ]
            
            for table in tables:
                cursor = self.conn.execute(f'SELECT COUNT(*) FROM {table}')
                stats[table] = cursor.fetchone()[0]
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get legal database stats: {str(e)}")
            return {}
    
    # Additional methods needed by the main app
    def store_legal_research(self, attorney_id: str, client_id: str, query: str, 
                           research_result: Dict[str, Any], jurisdiction: str) -> bool:
        """Store legal research results"""
        try:
            interaction_data = {
                'agent_type': 'legal_research',
                'interaction_type': 'research_query',
                'query': query,
                'response': research_result,
                'jurisdiction': jurisdiction
            }
            
            self.store_ai_interaction(attorney_id, client_id, interaction_data)
            return True
            
        except Exception as e:
            logger.error(f"Failed to store legal research: {str(e)}")
            return False
    
    def store_case_analysis(self, attorney_id: str, client_id: str, case_facts: str, 
                          analysis_result: Dict[str, Any], privileged: bool = True) -> bool:
        """Store case analysis results"""
        try:
            interaction_data = {
                'agent_type': 'case_analysis',
                'interaction_type': 'case_strength_analysis',
                'query': case_facts,
                'response': analysis_result,
                'privilege_protected': privileged
            }
            
            self.store_ai_interaction(attorney_id, client_id, interaction_data)
            return True
            
        except Exception as e:
            logger.error(f"Failed to store case analysis: {str(e)}")
            return False
    
    def store_document_review(self, attorney_id: str, client_id: str, document_text: str, 
                            review_result: Dict[str, Any], privileged: bool = True) -> bool:
        """Store document review results"""
        try:
            # Don't store full document text for security, just summary
            query_summary = f"Document review: {len(document_text)} characters"
            
            interaction_data = {
                'agent_type': 'document_review',
                'interaction_type': 'document_analysis',
                'query': query_summary,
                'response': review_result,
                'privilege_protected': privileged
            }
            
            self.store_ai_interaction(attorney_id, client_id, interaction_data)
            return True
            
        except Exception as e:
            logger.error(f"Failed to store document review: {str(e)}")
            return False
    
    def store_precedent_research(self, attorney_id: str, client_id: str, legal_issue: str, 
                               precedent_result: Dict[str, Any], jurisdiction: str) -> bool:
        """Store precedent research results"""
        try:
            interaction_data = {
                'agent_type': 'precedent_mining',
                'interaction_type': 'precedent_search',
                'query': legal_issue,
                'response': precedent_result,
                'jurisdiction': jurisdiction
            }
            
            self.store_ai_interaction(attorney_id, client_id, interaction_data)
            return True
            
        except Exception as e:
            logger.error(f"Failed to store precedent research: {str(e)}")
            return False
    
    def store_comprehensive_analysis(self, attorney_id: str, client_id: str, legal_matter: str, 
                                   analysis_result: Dict[str, Any], privileged: bool = True) -> bool:
        """Store comprehensive legal analysis results"""
        try:
            interaction_data = {
                'agent_type': 'multi_agent_analysis',
                'interaction_type': 'comprehensive_legal_analysis',
                'query': legal_matter,
                'response': analysis_result,
                'privilege_protected': privileged
            }
            
            self.store_ai_interaction(attorney_id, client_id, interaction_data)
            return True
            
        except Exception as e:
            logger.error(f"Failed to store comprehensive analysis: {str(e)}")
            return False
    
    def get_attorney_case_history(self, attorney_id: str, client_id: str = None) -> List[Dict]:
        """Get attorney's case history with privilege protection"""
        try:
            base_query = '''
                SELECT interaction_id, agent_type, interaction_type, timestamp,
                       confidence_score, privilege_protected, case_id
                FROM ai_interactions
                WHERE attorney_id = ?
            '''
            params = [attorney_id]
            
            if client_id:
                base_query += ' AND client_id = ?'
                params.append(client_id)
            
            base_query += ' ORDER BY timestamp DESC LIMIT 100'
            
            cursor = self.conn.execute(base_query, params)
            history = []
            
            for row in cursor.fetchall():
                history.append(dict(row))
            
            return history
            
        except Exception as e:
            logger.error(f"Failed to get attorney case history: {str(e)}")
            return []

    # ------------------------------------------------------------------
    # Case management helpers used by the Flask API
    # ------------------------------------------------------------------
    def create_legal_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new legal case record with privilege-aware summary handling."""
        try:
            case_id = case_data.get('case_id') or str(uuid.uuid4())

            # If a summary is provided, encrypt before persisting
            encrypted_summary = None
            summary_text = case_data.get('case_summary') or case_data.get('summary')
            if summary_text:
                encrypted_summary = self._encrypt_privileged_data(summary_text)

            self.conn.execute(
                '''
                INSERT INTO legal_cases (
                    case_id, attorney_id, client_id, case_number, case_title,
                    case_type, jurisdiction, court_name, case_status, filed_date,
                    statute_of_limitations, encrypted_case_summary, practice_area,
                    opposing_party, opposing_counsel, estimated_value, priority_level
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    case_id,
                    case_data.get('attorney_id'),
                    case_data.get('client_id'),
                    case_data.get('case_number'),
                    case_data.get('case_title'),
                    case_data.get('case_type'),
                    case_data.get('jurisdiction'),
                    case_data.get('court_name'),
                    case_data.get('case_status', 'active'),
                    case_data.get('filed_date'),
                    case_data.get('statute_of_limitations'),
                    encrypted_summary,
                    case_data.get('practice_area'),
                    case_data.get('opposing_party'),
                    case_data.get('opposing_counsel'),
                    case_data.get('estimated_value'),
                    case_data.get('priority_level', 'medium'),
                ),
            )
            self.conn.commit()
            return self.get_legal_case(case_id) or {"case_id": case_id}

        except Exception as e:
            logger.error(f"Failed to create legal case: {str(e)}")
            self.conn.rollback()
            raise

    def update_legal_case(self, case_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update mutable fields on a legal case record."""
        try:
            if not updates:
                return self.get_legal_case(case_id) or {}

            fields = []
            values: List[Any] = []

            for key, value in updates.items():
                if key in {'case_summary', 'summary'}:
                    encrypted = self._encrypt_privileged_data(value)
                    fields.append('encrypted_case_summary = ?')
                    values.append(encrypted)
                elif key in {
                    'case_number', 'case_title', 'case_type', 'jurisdiction',
                    'court_name', 'case_status', 'filed_date', 'statute_of_limitations',
                    'practice_area', 'opposing_party', 'opposing_counsel',
                    'estimated_value', 'priority_level', 'attorney_id', 'client_id'
                }:
                    fields.append(f"{key} = ?")
                    values.append(value)

            if not fields:
                return self.get_legal_case(case_id) or {}

            fields.append('updated_at = CURRENT_TIMESTAMP')
            values.append(case_id)

            query = f"UPDATE legal_cases SET {', '.join(fields)} WHERE case_id = ?"
            self.conn.execute(query, values)
            self.conn.commit()
            return self.get_legal_case(case_id) or {}

        except Exception as e:
            logger.error(f"Failed to update legal case {case_id}: {str(e)}")
            self.conn.rollback()
            raise

    def list_legal_cases(
        self,
        *,
        attorney_id: Optional[str] = None,
        client_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Return cases filtered by attorney/client for dashboard views."""
        try:
            base_query = '''
                SELECT case_id, attorney_id, client_id, case_number, case_title,
                       case_type, jurisdiction, court_name, case_status,
                       filed_date, statute_of_limitations, practice_area,
                       opposing_party, opposing_counsel, estimated_value,
                       priority_level, created_at, updated_at
                FROM legal_cases
                WHERE 1=1
            '''
            params: List[Any] = []

            if attorney_id:
                base_query += ' AND attorney_id = ?'
                params.append(attorney_id)
            if client_id:
                base_query += ' AND client_id = ?'
                params.append(client_id)

            base_query += ' ORDER BY updated_at DESC LIMIT ?'
            params.append(limit)

            cursor = self.conn.execute(base_query, params)
            return [dict(row) for row in cursor.fetchall()]

        except Exception as e:
            logger.error(f"Failed to list legal cases: {str(e)}")
            return []

    def get_legal_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single legal case record."""
        try:
            cursor = self.conn.execute(
                '''
                SELECT case_id, attorney_id, client_id, case_number, case_title,
                       case_type, jurisdiction, court_name, case_status,
                       filed_date, statute_of_limitations, practice_area,
                       opposing_party, opposing_counsel, estimated_value,
                       priority_level, encrypted_case_summary, created_at, updated_at
                FROM legal_cases
                WHERE case_id = ?
                ''',
                (case_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None

            case_data = dict(row)
            encrypted = case_data.pop('encrypted_case_summary', None)
            if encrypted:
                try:
                    case_data['case_summary'] = self._decrypt_privileged_data(encrypted)
                except Exception:
                    case_data['case_summary'] = None

            return case_data

        except Exception as e:
            logger.error(f"Failed to retrieve legal case {case_id}: {str(e)}")
            return None

    def log_privileged_audit_event(self, attorney_id: str, client_id: str, action: str, 
                                 details: str, privileged: bool = True) -> bool:
        """Log privileged audit event"""
        try:
            return self.log_ethics_audit_event(
                action_type=action,
                action_description=details,
                compliance_status='compliant',
                attorney_id=attorney_id,
                client_id=client_id,
                privilege_impact=privileged
            ) is not None
            
        except Exception as e:
            logger.error(f"Failed to log privileged audit event: {str(e)}")
            return False

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Legal database connection closed")
