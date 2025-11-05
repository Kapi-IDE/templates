#!/usr/bin/env python3
"""
SQLite Manager for Healthcare AI System
Handles patient data, conversations, and audit logs
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

class PatientDataManager:
    """
    Manages patient data and conversations in SQLite database
    Ensures HIPAA compliance with encryption and audit logging
    """
    
    def __init__(self, db_path: str = "./patient_data.db"):
        """Initialize SQLite database and create tables"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable dict-like access
        
        # Initialize encryption (in production, load from secure key management)
        self.encryption_key = os.getenv('ENCRYPTION_KEY')
        if not self.encryption_key:
            # Generate key for demo (DO NOT do this in production)
            self.encryption_key = Fernet.generate_key()
            logger.warning("Generated encryption key for demo - use proper key management in production")
        
        self.cipher = Fernet(self.encryption_key)
        
        self._create_tables()
        logger.info("SQLite database initialized successfully")
    
    def _create_tables(self):
        """Create database tables for patient data"""
        try:
            # Patients table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT UNIQUE NOT NULL,
                    encrypted_medical_history TEXT,
                    age_range TEXT,
                    gender TEXT,
                    risk_factors TEXT,
                    allergies TEXT,
                    medications TEXT,
                    emergency_contact TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Conversations table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT UNIQUE NOT NULL,
                    patient_id TEXT NOT NULL,
                    encrypted_user_message TEXT NOT NULL,
                    encrypted_ai_response TEXT NOT NULL,
                    urgency_score INTEGER,
                    escalation_triggered BOOLEAN DEFAULT 0,
                    agent_workflow TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_id TEXT,
                    ip_address TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            ''')
            
            # Sessions table for tracking active sessions
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    patient_id TEXT NOT NULL,
                    session_token TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    active BOOLEAN DEFAULT 1,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            ''')
            
            # Audit log table for HIPAA compliance
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT,
                    action TEXT NOT NULL,
                    details TEXT,
                    user_id TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success BOOLEAN DEFAULT 1
                )
            ''')
            
            # Triage history table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS triage_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    conversation_id TEXT NOT NULL,
                    symptoms TEXT NOT NULL,
                    urgency_score INTEGER NOT NULL,
                    urgency_level TEXT NOT NULL,
                    reasoning TEXT,
                    recommended_action TEXT,
                    escalation_triggered BOOLEAN DEFAULT 0,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                    FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id)
                )
            ''')
            
            # Create indexes for better performance
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_conversations_patient_id ON conversations(patient_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_patient_id ON sessions(patient_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_audit_log_patient_id ON audit_log(patient_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_triage_patient_id ON triage_history(patient_id)')
            
            self.conn.commit()
            logger.info("Database tables created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create database tables: {str(e)}")
            raise
    
    def _encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            if isinstance(data, dict) or isinstance(data, list):
                data = json.dumps(data)
            return self.cipher.encrypt(data.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt data: {str(e)}")
            raise
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to decrypt data: {str(e)}")
            raise
    
    def create_patient(self, patient_id: str, medical_history: Dict = None, 
                      demographics: Dict = None) -> bool:
        """Create a new patient record"""
        try:
            # Encrypt medical history
            encrypted_history = None
            if medical_history:
                encrypted_history = self._encrypt_data(medical_history)
            
            # Insert patient record
            self.conn.execute('''
                INSERT OR REPLACE INTO patients 
                (patient_id, encrypted_medical_history, age_range, gender, risk_factors, 
                 allergies, medications, emergency_contact, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                patient_id,
                encrypted_history,
                demographics.get('age_range') if demographics else None,
                demographics.get('gender') if demographics else None,
                json.dumps(demographics.get('risk_factors', [])) if demographics else None,
                json.dumps(demographics.get('allergies', [])) if demographics else None,
                json.dumps(demographics.get('medications', [])) if demographics else None,
                json.dumps(demographics.get('emergency_contact')) if demographics else None
            ))
            
            self.conn.commit()
            
            # Log patient creation
            self.log_audit_event(
                patient_id=patient_id,
                action='patient_created',
                details='New patient record created'
            )
            
            logger.info(f"Patient {patient_id} created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create patient {patient_id}: {str(e)}")
            self.conn.rollback()
            return False
    
    def get_patient(self, patient_id: str) -> Optional[Dict]:
        """Retrieve patient information"""
        try:
            cursor = self.conn.execute('''
                SELECT * FROM patients WHERE patient_id = ? AND active = 1
            ''', (patient_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Convert to dict and decrypt sensitive data
            patient = dict(row)
            if patient['encrypted_medical_history']:
                try:
                    patient['medical_history'] = json.loads(
                        self._decrypt_data(patient['encrypted_medical_history'])
                    )
                except:
                    patient['medical_history'] = {}
            
            # Parse JSON fields
            for field in ['risk_factors', 'allergies', 'medications', 'emergency_contact']:
                if patient[field]:
                    try:
                        patient[field] = json.loads(patient[field])
                    except:
                        pass
            
            # Remove encrypted field from response
            del patient['encrypted_medical_history']
            
            return patient
            
        except Exception as e:
            logger.error(f"Failed to retrieve patient {patient_id}: {str(e)}")
            return None
    
    def create_session(self, patient_id: str, session_token: str, 
                      expires_at: datetime, ip_address: str = None, 
                      user_agent: str = None) -> str:
        """Create a new patient session"""
        try:
            session_id = str(uuid.uuid4())
            
            self.conn.execute('''
                INSERT INTO sessions 
                (session_id, patient_id, session_token, expires_at, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (session_id, patient_id, session_token, expires_at, ip_address, user_agent))
            
            self.conn.commit()
            
            self.log_audit_event(
                patient_id=patient_id,
                action='session_created',
                details=f'New session created: {session_id}',
                ip_address=ip_address
            )
            
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to create session for patient {patient_id}: {str(e)}")
            raise
    
    def verify_session(self, patient_id: str, session_token: str) -> bool:
        """Verify if a session is valid and active"""
        try:
            cursor = self.conn.execute('''
                SELECT * FROM sessions 
                WHERE patient_id = ? AND session_token = ? 
                AND active = 1 AND expires_at > CURRENT_TIMESTAMP
            ''', (patient_id, session_token))
            
            return cursor.fetchone() is not None
            
        except Exception as e:
            logger.error(f"Failed to verify session: {str(e)}")
            return False
    
    def store_conversation(self, patient_id: str, conversation_id: str,
                          user_message: str, ai_response: Dict,
                          urgency_score: int, session_id: str = None,
                          ip_address: str = None) -> bool:
        """Store a conversation exchange"""
        try:
            # Encrypt sensitive data
            encrypted_message = self._encrypt_data(user_message)
            encrypted_response = self._encrypt_data(ai_response)
            
            # Determine if escalation was triggered
            escalation_triggered = ai_response.get('escalation', {}).get('required', False)
            
            # Store conversation
            self.conn.execute('''
                INSERT INTO conversations 
                (conversation_id, patient_id, encrypted_user_message, encrypted_ai_response,
                 urgency_score, escalation_triggered, agent_workflow, session_id, ip_address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                conversation_id, patient_id, encrypted_message, encrypted_response,
                urgency_score, escalation_triggered, 
                json.dumps(ai_response.get('agent_workflow', {})),
                session_id, ip_address
            ))
            
            # Store triage information separately
            self.conn.execute('''
                INSERT INTO triage_history 
                (patient_id, conversation_id, symptoms, urgency_score, urgency_level,
                 reasoning, recommended_action, escalation_triggered)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient_id, conversation_id,
                json.dumps(ai_response.get('urgency_assessment', {}).get('symptoms', [])),
                urgency_score,
                ai_response.get('urgency_assessment', {}).get('level', 'unknown'),
                ai_response.get('urgency_assessment', {}).get('reasoning', ''),
                ai_response.get('urgency_assessment', {}).get('recommended_action', ''),
                escalation_triggered
            ))
            
            self.conn.commit()
            
            # Log conversation storage
            self.log_audit_event(
                patient_id=patient_id,
                action='conversation_stored',
                details=f'Conversation {conversation_id} stored',
                ip_address=ip_address
            )
            
            logger.info(f"Conversation {conversation_id} stored successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store conversation: {str(e)}")
            self.conn.rollback()
            return False
    
    def get_patient_history(self, patient_id: str, limit: int = 50) -> List[Dict]:
        """Retrieve patient's conversation history"""
        try:
            cursor = self.conn.execute('''
                SELECT conversation_id, encrypted_user_message, encrypted_ai_response,
                       urgency_score, escalation_triggered, timestamp
                FROM conversations
                WHERE patient_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (patient_id, limit))
            
            conversations = []
            for row in cursor.fetchall():
                conversation = dict(row)
                
                # Decrypt messages
                try:
                    conversation['user_message'] = self._decrypt_data(conversation['encrypted_user_message'])
                    conversation['ai_response'] = json.loads(
                        self._decrypt_data(conversation['encrypted_ai_response'])
                    )
                except Exception as e:
                    logger.error(f"Failed to decrypt conversation data: {str(e)}")
                    continue
                
                # Remove encrypted fields
                del conversation['encrypted_user_message']
                del conversation['encrypted_ai_response']
                
                conversations.append(conversation)
            
            return conversations
            
        except Exception as e:
            logger.error(f"Failed to get patient history: {str(e)}")
            return []
    
    def get_triage_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get triage statistics for dashboard"""
        try:
            since_date = datetime.now() - timedelta(days=days)
            
            # Total interactions
            cursor = self.conn.execute('''
                SELECT COUNT(*) as total FROM conversations 
                WHERE timestamp > ?
            ''', (since_date,))
            total_interactions = cursor.fetchone()[0]
            
            # Urgency level distribution
            cursor = self.conn.execute('''
                SELECT urgency_level, COUNT(*) as count 
                FROM triage_history 
                WHERE timestamp > ?
                GROUP BY urgency_level
            ''', (since_date,))
            urgency_distribution = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Escalations
            cursor = self.conn.execute('''
                SELECT COUNT(*) as escalations FROM triage_history
                WHERE escalation_triggered = 1 AND timestamp > ?
            ''', (since_date,))
            total_escalations = cursor.fetchone()[0]
            
            # Average urgency score
            cursor = self.conn.execute('''
                SELECT AVG(urgency_score) as avg_score FROM triage_history
                WHERE timestamp > ?
            ''', (since_date,))
            avg_urgency = cursor.fetchone()[0] or 0
            
            return {
                'total_interactions': total_interactions,
                'urgency_distribution': urgency_distribution,
                'total_escalations': total_escalations,
                'escalation_rate': (total_escalations / max(total_interactions, 1)) * 100,
                'average_urgency_score': round(avg_urgency, 2),
                'date_range': f"{since_date.strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}"
            }
            
        except Exception as e:
            logger.error(f"Failed to get triage stats: {str(e)}")
            return {}
    
    def log_audit_event(self, action: str, patient_id: str = None, 
                       details: str = None, user_id: str = None,
                       ip_address: str = None, user_agent: str = None,
                       success: bool = True):
        """Log audit event for HIPAA compliance"""
        try:
            self.conn.execute('''
                INSERT INTO audit_log 
                (patient_id, action, details, user_id, ip_address, user_agent, success)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (patient_id, action, details, user_id, ip_address, user_agent, success))
            
            self.conn.commit()
            
        except Exception as e:
            logger.error(f"Failed to log audit event: {str(e)}")
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        try:
            cursor = self.conn.execute('''
                UPDATE sessions SET active = 0 
                WHERE expires_at < CURRENT_TIMESTAMP AND active = 1
            ''')
            
            expired_count = cursor.rowcount
            self.conn.commit()
            
            if expired_count > 0:
                logger.info(f"Cleaned up {expired_count} expired sessions")
                
        except Exception as e:
            logger.error(f"Failed to cleanup expired sessions: {str(e)}")
    
    def health_check(self) -> bool:
        """Verify database is working properly"""
        try:
            cursor = self.conn.execute('SELECT 1')
            cursor.fetchone()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return False
    
    def get_database_stats(self) -> Dict[str, int]:
        """Get database statistics"""
        try:
            stats = {}
            
            tables = ['patients', 'conversations', 'sessions', 'audit_log', 'triage_history']
            for table in tables:
                cursor = self.conn.execute(f'SELECT COUNT(*) FROM {table}')
                stats[table] = cursor.fetchone()[0]
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get database stats: {str(e)}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")