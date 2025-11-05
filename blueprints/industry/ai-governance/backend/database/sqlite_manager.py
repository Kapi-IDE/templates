#!/usr/bin/env python3
"""
SQLite Manager for AI Governance System
Manages governance data, assessments, and audit trails with encryption support
"""

import sqlite3
import logging
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import os
import uuid

logger = logging.getLogger(__name__)

class GovernanceDataManager:
    """
    Manages AI governance data using SQLite with encryption for sensitive information
    Handles AI systems registry, assessments, compliance records, and audit trails
    """
    
    def __init__(self, db_path: str = "./data/governance_data.db"):
        """Initialize SQLite database and encryption"""
        try:
            self.db_path = db_path
            
            # Initialize encryption key
            self.encryption_key = self._get_or_create_encryption_key()
            self.cipher_suite = Fernet(self.encryption_key)
            
            # Ensure data directory exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            # Initialize database
            self._initialize_database()
            
            # Populate with sample data
            self._populate_sample_data()
            
            logger.info("GovernanceDataManager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize GovernanceDataManager: {str(e)}")
            raise
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for sensitive data"""
        key_file = "./data/encryption.key"
        
        try:
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    return f.read()
            else:
                key = Fernet.generate_key()
                os.makedirs(os.path.dirname(key_file), exist_ok=True)
                with open(key_file, 'wb') as f:
                    f.write(key)
                return key
        except Exception as e:
            logger.warning(f"Failed to manage encryption key: {str(e)}")
            return Fernet.generate_key()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with proper configuration"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        return conn
    
    def _initialize_database(self):
        """Initialize database schema"""
        with self._get_connection() as conn:
            # AI Systems registry table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS ai_systems (
                    system_id TEXT PRIMARY KEY,
                    system_name TEXT NOT NULL,
                    system_type TEXT,
                    deployment_status TEXT DEFAULT 'development',
                    risk_category TEXT DEFAULT 'unknown',
                    owner_team TEXT,
                    business_unit TEXT,
                    description TEXT,
                    system_architecture TEXT,
                    data_sources TEXT,
                    model_details TEXT,
                    deployment_environment TEXT,
                    user_base_size INTEGER,
                    regulatory_scope TEXT,
                    last_assessment_date TIMESTAMP,
                    last_assessment_id TEXT,
                    governance_score REAL DEFAULT 0,
                    compliance_status TEXT DEFAULT 'unknown',
                    monitoring_status TEXT DEFAULT 'inactive',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT  -- JSON field for additional data
                )
            ''')
            
            # Risk Assessments table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS risk_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    system_id TEXT NOT NULL,
                    assessor_id TEXT NOT NULL,
                    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    assessment_type TEXT DEFAULT 'comprehensive',
                    risk_level TEXT,
                    risk_score REAL,
                    risk_dimensions TEXT,  -- JSON field
                    identified_risks TEXT,  -- JSON field
                    risk_factors TEXT,  -- JSON field
                    mitigation_recommendations TEXT,  -- JSON field
                    mitigation_status TEXT DEFAULT 'pending',
                    confidence_level INTEGER DEFAULT 7,
                    assessment_methodology TEXT,
                    processing_time REAL,
                    encrypted_data TEXT,  -- Encrypted sensitive information
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
                )
            ''')
            
            # Policy Compliance table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS policy_compliance (
                    compliance_id TEXT PRIMARY KEY,
                    system_id TEXT NOT NULL,
                    assessment_id TEXT,
                    assessor_id TEXT NOT NULL,
                    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    overall_status TEXT,
                    compliance_score REAL,
                    framework_compliance TEXT,  -- JSON field
                    compliance_gaps TEXT,  -- JSON field
                    remediation_actions TEXT,  -- JSON field
                    regulatory_requirements TEXT,  -- JSON field
                    next_review_date DATE,
                    compliance_percentage REAL,
                    confidence_level INTEGER DEFAULT 7,
                    processing_time REAL,
                    encrypted_data TEXT,  -- Encrypted sensitive information
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id),
                    FOREIGN KEY (assessment_id) REFERENCES risk_assessments(assessment_id)
                )
            ''')
            
            # Bias Assessments table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS bias_assessments (
                    bias_assessment_id TEXT PRIMARY KEY,
                    system_id TEXT NOT NULL,
                    assessment_id TEXT,
                    assessor_id TEXT NOT NULL,
                    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    bias_level TEXT,
                    bias_risk_score REAL,
                    fairness_metrics TEXT,  -- JSON field
                    bias_dimensions TEXT,  -- JSON field
                    protected_groups_impact TEXT,  -- JSON field
                    discrimination_risks TEXT,  -- JSON field
                    mitigation_strategies TEXT,  -- JSON field
                    monitoring_plan TEXT,  -- JSON field
                    confidence_level INTEGER DEFAULT 7,
                    processing_time REAL,
                    encrypted_data TEXT,  -- Encrypted sensitive information
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id),
                    FOREIGN KEY (assessment_id) REFERENCES risk_assessments(assessment_id)
                )
            ''')
            
            # Audit Trails table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS audit_trails (
                    entry_id TEXT PRIMARY KEY,
                    system_id TEXT,
                    assessment_id TEXT,
                    trail_id TEXT,
                    event_type TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    actor TEXT,
                    action TEXT,
                    details TEXT,
                    before_state TEXT,  -- JSON field
                    after_state TEXT,  -- JSON field
                    ip_address TEXT,
                    session_id TEXT,
                    data_hash TEXT,
                    integrity_verified BOOLEAN DEFAULT TRUE,
                    encrypted_data TEXT,  -- Encrypted sensitive information
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Audit Documentation table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS audit_documentation (
                    documentation_id TEXT PRIMARY KEY,
                    system_id TEXT NOT NULL,
                    assessment_id TEXT,
                    assessor_id TEXT NOT NULL,
                    document_type TEXT DEFAULT 'comprehensive_audit',
                    executive_summary TEXT,  -- JSON field
                    detailed_findings TEXT,  -- JSON field
                    compliance_documentation TEXT,  -- JSON field
                    risk_documentation TEXT,  -- JSON field
                    audit_evidence TEXT,  -- JSON field
                    action_plan TEXT,  -- JSON field
                    audit_metadata TEXT,  -- JSON field
                    next_audit_date DATE,
                    retention_period TEXT,
                    document_version TEXT DEFAULT '1.0',
                    integrity_hash TEXT,
                    access_controls TEXT,  -- JSON field
                    encrypted_data TEXT,  -- Encrypted sensitive information
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
                )
            ''')
            
            # Governance Sessions table for tracking user sessions
            conn.execute('''
                CREATE TABLE IF NOT EXISTS governance_sessions (
                    session_id TEXT PRIMARY KEY,
                    system_id TEXT,
                    assessor_id TEXT NOT NULL,
                    session_token TEXT,
                    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_end TIMESTAMP,
                    session_status TEXT DEFAULT 'active',
                    ip_address TEXT,
                    user_agent TEXT,
                    activities TEXT,  -- JSON field tracking session activities
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Compliance Frameworks reference table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS compliance_frameworks (
                    framework_id TEXT PRIMARY KEY,
                    framework_name TEXT NOT NULL,
                    framework_version TEXT,
                    jurisdiction TEXT,
                    framework_type TEXT,
                    requirements TEXT,  -- JSON field
                    compliance_criteria TEXT,  -- JSON field
                    assessment_methods TEXT,  -- JSON field
                    effective_date DATE,
                    update_frequency TEXT,
                    authority TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # System Monitoring table for continuous governance monitoring
            conn.execute('''
                CREATE TABLE IF NOT EXISTS system_monitoring (
                    monitoring_id TEXT PRIMARY KEY,
                    system_id TEXT NOT NULL,
                    monitoring_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    monitoring_type TEXT,
                    risk_indicators TEXT,  -- JSON field
                    compliance_indicators TEXT,  -- JSON field
                    bias_indicators TEXT,  -- JSON field
                    performance_metrics TEXT,  -- JSON field
                    alert_level TEXT DEFAULT 'low',
                    alerts_generated TEXT,  -- JSON field
                    automated_actions TEXT,  -- JSON field
                    next_monitoring_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (system_id) REFERENCES ai_systems(system_id)
                )
            ''')
            
            # Create indexes for better performance
            conn.execute('CREATE INDEX IF NOT EXISTS idx_ai_systems_status ON ai_systems(deployment_status)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_ai_systems_risk ON ai_systems(risk_category)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_risk_assessments_date ON risk_assessments(assessment_date)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_audit_trails_timestamp ON audit_trails(timestamp)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_audit_trails_system ON audit_trails(system_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_compliance_date ON policy_compliance(assessment_date)')
            
            conn.commit()
            logger.info("Database schema initialized successfully")
    
    def _populate_sample_data(self):
        """Populate database with sample governance data"""
        try:
            with self._get_connection() as conn:
                # Check if data already exists
                cursor = conn.execute("SELECT COUNT(*) FROM ai_systems")
                if cursor.fetchone()[0] > 0:
                    logger.info("Sample data already exists, skipping population")
                    return
                
                # Sample AI systems
                sample_systems = [
                    {
                        'system_id': 'ai_sys_001',
                        'system_name': 'Customer Credit Scoring Model',
                        'system_type': 'machine_learning_model',
                        'deployment_status': 'production',
                        'risk_category': 'high_risk',
                        'owner_team': 'Risk Management Team',
                        'business_unit': 'Financial Services',
                        'description': 'ML model for assessing customer creditworthiness',
                        'system_architecture': 'Ensemble model (Random Forest + Gradient Boosting)',
                        'data_sources': 'Customer financial history, credit bureau data',
                        'model_details': 'Binary classification with fairness constraints',
                        'deployment_environment': 'Production AWS infrastructure',
                        'user_base_size': 50000,
                        'regulatory_scope': 'EU AI Act, GDPR, Fair Credit Reporting Act',
                        'governance_score': 7.2,
                        'compliance_status': 'partially_compliant',
                        'monitoring_status': 'active'
                    },
                    {
                        'system_id': 'ai_sys_002', 
                        'system_name': 'HR Resume Screening Assistant',
                        'system_type': 'natural_language_processing',
                        'deployment_status': 'testing',
                        'risk_category': 'high_risk',
                        'owner_team': 'Human Resources',
                        'business_unit': 'People Operations',
                        'description': 'NLP system for initial resume screening and candidate ranking',
                        'system_architecture': 'Transformer-based language model',
                        'data_sources': 'Historical hiring data, job descriptions, resumes',
                        'model_details': 'Multi-class classification with bias mitigation',
                        'deployment_environment': 'Staging environment',
                        'user_base_size': 50,
                        'regulatory_scope': 'EU AI Act, Equal Employment Opportunity',
                        'governance_score': 6.8,
                        'compliance_status': 'requires_review',
                        'monitoring_status': 'development'
                    },
                    {
                        'system_id': 'ai_sys_003',
                        'system_name': 'Customer Service Chatbot',
                        'system_type': 'conversational_ai',
                        'deployment_status': 'production',
                        'risk_category': 'limited_risk',
                        'owner_team': 'Customer Experience',
                        'business_unit': 'Customer Operations',
                        'description': 'AI chatbot for customer service inquiries',
                        'system_architecture': 'Large language model with retrieval augmentation',
                        'data_sources': 'Customer service logs, FAQ database',
                        'model_details': 'Generative AI with safety filters',
                        'deployment_environment': 'Multi-cloud production',
                        'user_base_size': 100000,
                        'regulatory_scope': 'EU AI Act transparency requirements',
                        'governance_score': 8.1,
                        'compliance_status': 'compliant',
                        'monitoring_status': 'active'
                    }
                ]
                
                # Insert sample systems
                for system in sample_systems:
                    self._insert_ai_system(system)
                
                # Sample compliance frameworks
                sample_frameworks = [
                    {
                        'framework_id': 'EU_AI_Act',
                        'framework_name': 'European Union AI Act',
                        'framework_version': '2024',
                        'jurisdiction': 'European Union',
                        'framework_type': 'regulation',
                        'requirements': json.dumps([
                            'risk_assessment', 'conformity_assessment', 'ce_marking',
                            'technical_documentation', 'quality_management_system'
                        ]),
                        'compliance_criteria': json.dumps({
                            'high_risk_systems': 'Conformity assessment required',
                            'limited_risk_systems': 'Transparency obligations',
                            'prohibited_systems': 'Market placement prohibited'
                        }),
                        'assessment_methods': json.dumps(['technical_assessment', 'third_party_audit']),
                        'effective_date': '2024-08-01',
                        'update_frequency': 'annual',
                        'authority': 'European Commission',
                        'description': 'Comprehensive AI regulation framework'
                    },
                    {
                        'framework_id': 'NIST_AI_RMF',
                        'framework_name': 'NIST AI Risk Management Framework',
                        'framework_version': '1.0',
                        'jurisdiction': 'United States',
                        'framework_type': 'guidance',
                        'requirements': json.dumps([
                            'ai_impact_assessment', 'risk_management_plan', 
                            'continuous_monitoring', 'stakeholder_engagement'
                        ]),
                        'compliance_criteria': json.dumps({
                            'govern': 'Governance structures established',
                            'map': 'AI risks identified and categorized',
                            'measure': 'Risks analyzed and assessed',
                            'manage': 'Risks responded to and monitored'
                        }),
                        'assessment_methods': json.dumps(['self_assessment', 'peer_review']),
                        'effective_date': '2023-01-26',
                        'update_frequency': 'as_needed',
                        'authority': 'NIST',
                        'description': 'Framework for managing AI risks'
                    }
                ]
                
                # Insert sample frameworks
                for framework in sample_frameworks:
                    conn.execute('''
                        INSERT OR REPLACE INTO compliance_frameworks 
                        (framework_id, framework_name, framework_version, jurisdiction, 
                         framework_type, requirements, compliance_criteria, assessment_methods,
                         effective_date, update_frequency, authority, description)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        framework['framework_id'], framework['framework_name'], 
                        framework['framework_version'], framework['jurisdiction'],
                        framework['framework_type'], framework['requirements'],
                        framework['compliance_criteria'], framework['assessment_methods'],
                        framework['effective_date'], framework['update_frequency'],
                        framework['authority'], framework['description']
                    ))
                
                conn.commit()
                logger.info("Sample governance data populated successfully")
                
        except Exception as e:
            logger.error(f"Failed to populate sample data: {str(e)}")
    
    def _insert_ai_system(self, system_data: Dict):
        """Insert AI system into database"""
        with self._get_connection() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO ai_systems 
                (system_id, system_name, system_type, deployment_status, risk_category,
                 owner_team, business_unit, description, system_architecture, data_sources,
                 model_details, deployment_environment, user_base_size, regulatory_scope,
                 governance_score, compliance_status, monitoring_status, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                system_data['system_id'], system_data['system_name'], system_data['system_type'],
                system_data['deployment_status'], system_data['risk_category'], 
                system_data['owner_team'], system_data['business_unit'],
                system_data['description'], system_data['system_architecture'],
                system_data['data_sources'], system_data['model_details'],
                system_data['deployment_environment'], system_data['user_base_size'],
                system_data['regulatory_scope'], system_data['governance_score'],
                system_data['compliance_status'], system_data['monitoring_status'],
                json.dumps({})  # Empty metadata for now
            ))
    
    def _encrypt_sensitive_data(self, data: Dict) -> str:
        """Encrypt sensitive data"""
        try:
            data_json = json.dumps(data)
            return self.cipher_suite.encrypt(data_json.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt data: {str(e)}")
            return ""
    
    def _decrypt_sensitive_data(self, encrypted_data: str) -> Dict:
        """Decrypt sensitive data"""
        try:
            if not encrypted_data:
                return {}
            decrypted_bytes = self.cipher_suite.decrypt(encrypted_data.encode())
            return json.loads(decrypted_bytes.decode())
        except Exception as e:
            logger.error(f"Failed to decrypt data: {str(e)}")
            return {}
    
    # AI Systems management methods
    def get_ai_system(self, system_id: str) -> Optional[Dict]:
        """Get AI system by ID"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM ai_systems WHERE system_id = ?", (system_id,)
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except Exception as e:
            logger.error(f"Failed to get AI system {system_id}: {str(e)}")
            return None
    
    def get_all_ai_systems(self, filters: Dict = None) -> List[Dict]:
        """Get all AI systems with optional filters"""
        try:
            with self._get_connection() as conn:
                query = "SELECT * FROM ai_systems"
                params = []
                
                if filters:
                    conditions = []
                    for key, value in filters.items():
                        if key in ['deployment_status', 'risk_category', 'compliance_status']:
                            conditions.append(f"{key} = ?")
                            params.append(value)
                    
                    if conditions:
                        query += " WHERE " + " AND ".join(conditions)
                
                query += " ORDER BY created_at DESC"
                
                cursor = conn.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get AI systems: {str(e)}")
            return []
    
    def update_ai_system(self, system_id: str, updates: Dict) -> bool:
        """Update AI system information"""
        try:
            with self._get_connection() as conn:
                # Build dynamic update query
                update_fields = []
                params = []
                
                allowed_fields = [
                    'system_name', 'system_type', 'deployment_status', 'risk_category',
                    'owner_team', 'business_unit', 'description', 'governance_score',
                    'compliance_status', 'monitoring_status', 'last_assessment_date',
                    'last_assessment_id'
                ]
                
                for field, value in updates.items():
                    if field in allowed_fields:
                        update_fields.append(f"{field} = ?")
                        params.append(value)
                
                if not update_fields:
                    return False
                
                # Add updated_at timestamp
                update_fields.append("updated_at = CURRENT_TIMESTAMP")
                params.append(system_id)
                
                query = f"UPDATE ai_systems SET {', '.join(update_fields)} WHERE system_id = ?"
                conn.execute(query, params)
                conn.commit()
                
                return conn.total_changes > 0
        except Exception as e:
            logger.error(f"Failed to update AI system {system_id}: {str(e)}")
            return False
    
    # Assessment storage methods
    def store_risk_assessment(self, assessment_data: Dict) -> bool:
        """Store risk assessment results"""
        try:
            with self._get_connection() as conn:
                # Encrypt sensitive assessment data
                sensitive_data = {
                    'detailed_risks': assessment_data.get('identified_risks', []),
                    'sensitive_context': assessment_data.get('system_context', {}),
                    'internal_notes': assessment_data.get('internal_notes', '')
                }
                encrypted_data = self._encrypt_sensitive_data(sensitive_data)
                
                conn.execute('''
                    INSERT INTO risk_assessments 
                    (assessment_id, system_id, assessor_id, risk_level, risk_score,
                     risk_dimensions, identified_risks, risk_factors, 
                     mitigation_recommendations, confidence_level, assessment_methodology,
                     processing_time, encrypted_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    assessment_data['assessment_id'], assessment_data['system_id'],
                    assessment_data.get('assessor_id', ''), assessment_data['risk_level'],
                    assessment_data['risk_score'], 
                    json.dumps(assessment_data.get('risk_dimensions', {})),
                    json.dumps(assessment_data['identified_risks']),
                    json.dumps(assessment_data.get('risk_factors', [])),
                    json.dumps(assessment_data.get('mitigation_recommendations', [])),
                    assessment_data.get('confidence_level', 7),
                    assessment_data.get('assessment_methodology', ''),
                    assessment_data.get('processing_time', 0),
                    encrypted_data
                ))
                
                # Update AI system with latest assessment info
                self.update_ai_system(assessment_data['system_id'], {
                    'last_assessment_date': datetime.now().isoformat(),
                    'last_assessment_id': assessment_data['assessment_id'],
                    'risk_category': assessment_data['risk_level']
                })
                
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to store risk assessment: {str(e)}")
            return False
    
    def store_compliance_assessment(self, compliance_data: Dict) -> bool:
        """Store policy compliance assessment results"""
        try:
            with self._get_connection() as conn:
                # Encrypt sensitive compliance data
                sensitive_data = {
                    'detailed_gaps': compliance_data.get('gaps', []),
                    'internal_findings': compliance_data.get('internal_findings', {}),
                    'regulatory_analysis': compliance_data.get('regulatory_analysis', {})
                }
                encrypted_data = self._encrypt_sensitive_data(sensitive_data)
                
                conn.execute('''
                    INSERT INTO policy_compliance
                    (compliance_id, system_id, assessment_id, assessor_id, overall_status,
                     compliance_score, framework_compliance, compliance_gaps, 
                     remediation_actions, regulatory_requirements, next_review_date,
                     compliance_percentage, confidence_level, processing_time, encrypted_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    compliance_data['assessment_id'], compliance_data['system_id'],
                    compliance_data.get('risk_assessment_id', ''),
                    compliance_data.get('assessor_id', ''),
                    compliance_data['status'], compliance_data['compliance_score'],
                    json.dumps(compliance_data.get('frameworks', {})),
                    json.dumps(compliance_data.get('gaps', [])),
                    json.dumps(compliance_data.get('remediation_actions', [])),
                    json.dumps(compliance_data.get('regulatory_requirements', {})),
                    compliance_data.get('next_review_date', ''),
                    compliance_data.get('compliance_percentage', 0),
                    compliance_data.get('confidence_level', 7),
                    compliance_data.get('processing_time', 0),
                    encrypted_data
                ))
                
                # Update AI system compliance status
                self.update_ai_system(compliance_data['system_id'], {
                    'compliance_status': compliance_data['status']
                })
                
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to store compliance assessment: {str(e)}")
            return False
    
    def store_bias_assessment(self, bias_data: Dict) -> bool:
        """Store bias assessment results"""
        try:
            with self._get_connection() as conn:
                # Encrypt sensitive bias data
                sensitive_data = {
                    'detailed_bias_analysis': bias_data.get('detailed_analysis', {}),
                    'protected_group_details': bias_data.get('protected_groups_analysis', {}),
                    'fairness_test_results': bias_data.get('test_results', {})
                }
                encrypted_data = self._encrypt_sensitive_data(sensitive_data)
                
                conn.execute('''
                    INSERT INTO bias_assessments
                    (bias_assessment_id, system_id, assessment_id, assessor_id, bias_level,
                     bias_risk_score, fairness_metrics, bias_dimensions, 
                     protected_groups_impact, discrimination_risks, mitigation_strategies,
                     monitoring_plan, confidence_level, processing_time, encrypted_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    bias_data['assessment_id'], bias_data['system_id'],
                    bias_data.get('risk_assessment_id', ''),
                    bias_data.get('assessor_id', ''),
                    bias_data['bias_level'], bias_data['bias_risk_score'],
                    json.dumps(bias_data.get('fairness_metrics', {})),
                    json.dumps(bias_data.get('bias_dimensions', {})),
                    json.dumps(bias_data.get('protected_groups_impact', {})),
                    json.dumps(bias_data.get('discrimination_risks', {})),
                    json.dumps(bias_data.get('mitigation_strategies', [])),
                    json.dumps(bias_data.get('continuous_monitoring_plan', {})),
                    bias_data.get('confidence_level', 7),
                    bias_data.get('processing_time', 0),
                    encrypted_data
                ))
                
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to store bias assessment: {str(e)}")
            return False
    
    def store_audit_documentation(self, audit_data: Dict) -> bool:
        """Store audit documentation"""
        try:
            with self._get_connection() as conn:
                # Encrypt sensitive audit data
                sensitive_data = {
                    'sensitive_findings': audit_data.get('sensitive_findings', {}),
                    'internal_recommendations': audit_data.get('internal_recommendations', []),
                    'confidential_evidence': audit_data.get('confidential_evidence', {})
                }
                encrypted_data = self._encrypt_sensitive_data(sensitive_data)
                
                conn.execute('''
                    INSERT INTO audit_documentation
                    (documentation_id, system_id, assessment_id, assessor_id, document_type,
                     executive_summary, detailed_findings, compliance_documentation,
                     risk_documentation, audit_evidence, action_plan, audit_metadata,
                     next_audit_date, retention_period, document_version, integrity_hash,
                     access_controls, encrypted_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    audit_data['assessment_id'], audit_data['system_id'],
                    audit_data.get('risk_assessment_id', ''),
                    audit_data['assessor_id'], audit_data.get('document_type', 'comprehensive_audit'),
                    json.dumps(audit_data.get('executive_summary', {})),
                    json.dumps(audit_data.get('detailed_findings', {})),
                    json.dumps(audit_data.get('compliance_documentation', {})),
                    json.dumps(audit_data.get('risk_documentation', {})),
                    json.dumps(audit_data.get('audit_evidence', {})),
                    json.dumps(audit_data.get('action_plan', {})),
                    json.dumps(audit_data.get('audit_metadata', {})),
                    audit_data.get('next_audit_date', ''),
                    audit_data.get('document_retention_period', '7 years'),
                    audit_data.get('document_version', '1.0'),
                    audit_data.get('integrity_hash', ''),
                    json.dumps(audit_data.get('access_controls', {})),
                    encrypted_data
                ))
                
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to store audit documentation: {str(e)}")
            return False
    
    # Audit trail methods
    def log_audit_event(self, system_id: str, action: str, details: str,
                       actor: str = None, assessment_id: str = None,
                       before_state: Dict = None, after_state: Dict = None,
                       ip_address: str = None, session_id: str = None) -> bool:
        """Log governance audit event"""
        try:
            with self._get_connection() as conn:
                entry_id = f"audit_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"
                
                # Calculate data hash for integrity
                hash_data = {
                    'system_id': system_id,
                    'action': action,
                    'details': details,
                    'timestamp': datetime.now().isoformat(),
                    'actor': actor
                }
                data_hash = hashlib.sha256(json.dumps(hash_data, sort_keys=True).encode()).hexdigest()
                
                # Encrypt sensitive audit data
                sensitive_data = {
                    'before_state': before_state or {},
                    'after_state': after_state or {},
                    'session_details': {'ip_address': ip_address, 'session_id': session_id}
                }
                encrypted_data = self._encrypt_sensitive_data(sensitive_data)
                
                conn.execute('''
                    INSERT INTO audit_trails
                    (entry_id, system_id, assessment_id, event_type, actor, action, 
                     details, before_state, after_state, ip_address, session_id,
                     data_hash, encrypted_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    entry_id, system_id, assessment_id, 'governance_action',
                    actor, action, details,
                    json.dumps(before_state or {}), json.dumps(after_state or {}),
                    ip_address, session_id, data_hash, encrypted_data
                ))
                
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to log audit event: {str(e)}")
            return False
    
    def get_system_audit_trail(self, system_id: str, limit: int = 100) -> List[Dict]:
        """Get audit trail for a specific system"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute('''
                    SELECT * FROM audit_trails 
                    WHERE system_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (system_id, limit))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get audit trail for {system_id}: {str(e)}")
            return []
    
    # Assessment retrieval methods
    def get_assessment_history(self, system_id: str) -> List[Dict]:
        """Get comprehensive assessment history for a system"""
        try:
            with self._get_connection() as conn:
                # Get risk assessments
                risk_cursor = conn.execute('''
                    SELECT assessment_id, assessment_date, risk_level, risk_score, confidence_level
                    FROM risk_assessments 
                    WHERE system_id = ? 
                    ORDER BY assessment_date DESC
                ''', (system_id,))
                risk_assessments = [dict(row) for row in risk_cursor.fetchall()]
                
                # Get compliance assessments  
                compliance_cursor = conn.execute('''
                    SELECT compliance_id, assessment_date, overall_status, compliance_score, confidence_level
                    FROM policy_compliance 
                    WHERE system_id = ? 
                    ORDER BY assessment_date DESC
                ''', (system_id,))
                compliance_assessments = [dict(row) for row in compliance_cursor.fetchall()]
                
                # Get bias assessments
                bias_cursor = conn.execute('''
                    SELECT bias_assessment_id, assessment_date, bias_level, bias_risk_score, confidence_level
                    FROM bias_assessments 
                    WHERE system_id = ? 
                    ORDER BY assessment_date DESC
                ''', (system_id,))
                bias_assessments = [dict(row) for row in bias_cursor.fetchall()]
                
                return {
                    'risk_assessments': risk_assessments,
                    'compliance_assessments': compliance_assessments,
                    'bias_assessments': bias_assessments
                }
        except Exception as e:
            logger.error(f"Failed to get assessment history for {system_id}: {str(e)}")
            return {}
    
    def get_system_current_state(self, system_id: str) -> Dict:
        """Get current state of AI system for monitoring"""
        try:
            with self._get_connection() as conn:
                # Get latest monitoring data
                cursor = conn.execute('''
                    SELECT * FROM system_monitoring 
                    WHERE system_id = ? 
                    ORDER BY monitoring_date DESC 
                    LIMIT 1
                ''', (system_id,))
                
                row = cursor.fetchone()
                if row:
                    return dict(row)
                
                # If no monitoring data, return basic system info
                system = self.get_ai_system(system_id)
                return system or {}
        except Exception as e:
            logger.error(f"Failed to get current state for {system_id}: {str(e)}")
            return {}
    
    def get_bias_assessment_history(self, system_id: str) -> List[Dict]:
        """Get bias assessment history for monitoring"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute('''
                    SELECT * FROM bias_assessments 
                    WHERE system_id = ? 
                    ORDER BY assessment_date DESC
                ''', (system_id,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get bias history for {system_id}: {str(e)}")
            return []
    
    def get_bias_history(self, system_id: str) -> List[Dict]:
        """Alias for get_bias_assessment_history for compatibility"""
        return self.get_bias_assessment_history(system_id)
    
    # Session management
    def create_governance_session(self, system_id: str, assessor_id: str, 
                                ip_address: str = None) -> Dict:
        """Create governance assessment session"""
        try:
            with self._get_connection() as conn:
                session_id = f"session_{uuid.uuid4().hex[:8]}"
                session_token = f"token_{uuid.uuid4().hex}"
                
                conn.execute('''
                    INSERT INTO governance_sessions
                    (session_id, system_id, assessor_id, session_token, ip_address, activities)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (session_id, system_id, assessor_id, session_token, ip_address, '[]'))
                
                conn.commit()
                
                return {
                    'session_id': session_id,
                    'session_token': session_token,
                    'system_id': system_id,
                    'assessor_id': assessor_id
                }
        except Exception as e:
            logger.error(f"Failed to create governance session: {str(e)}")
            return {}
    
    def verify_governance_session(self, session_id: str, session_token: str) -> bool:
        """Verify governance session is valid"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute('''
                    SELECT COUNT(*) FROM governance_sessions 
                    WHERE session_id = ? AND session_token = ? AND session_status = 'active'
                ''', (session_id, session_token))
                
                return cursor.fetchone()[0] > 0
        except Exception as e:
            logger.error(f"Failed to verify session: {str(e)}")
            return False
    
    # Analytics and reporting methods
    def get_governance_dashboard_data(self) -> Dict:
        """Get data for governance dashboard"""
        try:
            with self._get_connection() as conn:
                # System counts by status
                status_cursor = conn.execute('''
                    SELECT deployment_status, COUNT(*) as count 
                    FROM ai_systems 
                    GROUP BY deployment_status
                ''')
                status_counts = {row['deployment_status']: row['count'] for row in status_cursor.fetchall()}
                
                # Risk category distribution
                risk_cursor = conn.execute('''
                    SELECT risk_category, COUNT(*) as count 
                    FROM ai_systems 
                    GROUP BY risk_category
                ''')
                risk_distribution = {row['risk_category']: row['count'] for row in risk_cursor.fetchall()}
                
                # Compliance status distribution
                compliance_cursor = conn.execute('''
                    SELECT compliance_status, COUNT(*) as count 
                    FROM ai_systems 
                    GROUP BY compliance_status
                ''')
                compliance_distribution = {row['compliance_status']: row['count'] for row in compliance_cursor.fetchall()}
                
                # Recent assessments count
                week_ago = (datetime.now() - timedelta(days=7)).isoformat()
                recent_cursor = conn.execute('''
                    SELECT COUNT(*) FROM risk_assessments 
                    WHERE assessment_date > ?
                ''', (week_ago,))
                recent_assessments = recent_cursor.fetchone()[0]
                
                return {
                    'total_systems': sum(status_counts.values()),
                    'status_distribution': status_counts,
                    'risk_distribution': risk_distribution,
                    'compliance_distribution': compliance_distribution,
                    'recent_assessments': recent_assessments,
                    'last_updated': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Failed to get dashboard data: {str(e)}")
            return {}
    
    def get_governance_metrics(self) -> Dict:
        """Get system-wide governance metrics"""
        try:
            with self._get_connection() as conn:
                # Average governance scores
                avg_cursor = conn.execute('''
                    SELECT AVG(governance_score) as avg_score FROM ai_systems 
                    WHERE governance_score > 0
                ''')
                avg_score = avg_cursor.fetchone()['avg_score'] or 0
                
                # Assessment volumes
                assessment_cursor = conn.execute('''
                    SELECT 
                        COUNT(*) as total_assessments,
                        COUNT(DISTINCT system_id) as systems_assessed
                    FROM risk_assessments
                ''')
                assessment_metrics = dict(assessment_cursor.fetchone())
                
                # Compliance metrics
                compliance_cursor = conn.execute('''
                    SELECT 
                        AVG(compliance_score) as avg_compliance_score,
                        COUNT(*) as total_compliance_checks
                    FROM policy_compliance
                    WHERE compliance_score > 0
                ''')
                compliance_metrics = dict(compliance_cursor.fetchone())
                
                return {
                    'average_governance_score': round(avg_score, 2),
                    'assessment_metrics': assessment_metrics,
                    'compliance_metrics': compliance_metrics,
                    'generated_at': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Failed to get governance metrics: {str(e)}")
            return {}
    
    def health_check(self) -> bool:
        """Check if database connection and basic operations work"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM ai_systems")
                cursor.fetchone()
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return False
    
    def __del__(self):
        """Cleanup on destruction"""
        try:
            # SQLite connections are automatically cleaned up
            pass
        except:
            pass