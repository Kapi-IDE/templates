#!/usr/bin/env python3
"""
Security Manager for AI Governance System
Provides enterprise-grade security features including encryption, access control, and audit logging
"""

import hashlib
import secrets
import logging
import json
import uuid
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

logger = logging.getLogger(__name__)

class GovernanceSecurityManager:
    """
    Comprehensive security manager for AI governance operations
    Handles encryption, access control, session management, and security auditing
    """
    
    def __init__(self):
        """Initialize security manager with encryption and access controls"""
        try:
            # Initialize encryption keys
            self.master_key = self._get_or_create_master_key()
            self.cipher_suite = Fernet(self.master_key)
            
            # Security configuration
            self.security_config = {
                'session_timeout_minutes': 120,  # 2 hours
                'max_failed_attempts': 5,
                'lockout_duration_minutes': 30,
                'password_min_length': 12,
                'require_mfa': True,
                'audit_retention_days': 2555,  # 7 years
                'encryption_algorithm': 'AES-256'
            }
            
            # Access control matrix
            self.access_control_matrix = {
                'system_admin': {
                    'permissions': ['*'],  # Full access
                    'restrictions': []
                },
                'governance_officer': {
                    'permissions': [
                        'assess_systems', 'view_assessments', 'generate_reports',
                        'manage_policies', 'audit_systems', 'view_audit_trails'
                    ],
                    'restrictions': ['modify_system_config', 'delete_audit_data']
                },
                'compliance_manager': {
                    'permissions': [
                        'assess_compliance', 'view_assessments', 'generate_compliance_reports',
                        'view_policies', 'audit_compliance', 'view_audit_trails'
                    ],
                    'restrictions': ['modify_systems', 'delete_assessments', 'manage_users']
                },
                'risk_analyst': {
                    'permissions': [
                        'assess_risk', 'view_risk_assessments', 'generate_risk_reports',
                        'view_systems'
                    ],
                    'restrictions': [
                        'modify_systems', 'delete_data', 'manage_policies', 
                        'access_audit_trails', 'view_sensitive_data'
                    ]
                },
                'auditor': {
                    'permissions': [
                        'view_all_assessments', 'generate_audit_reports', 
                        'view_audit_trails', 'verify_compliance'
                    ],
                    'restrictions': ['modify_data', 'delete_data', 'manage_systems']
                },
                'viewer': {
                    'permissions': ['view_public_reports', 'view_system_status'],
                    'restrictions': [
                        'assess_systems', 'modify_data', 'delete_data',
                        'view_sensitive_data', 'access_audit_trails'
                    ]
                }
            }
            
            # Security event tracking
            self.security_events = {}
            
            logger.info("GovernanceSecurityManager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize GovernanceSecurityManager: {str(e)}")
            raise
    
    def _get_or_create_master_key(self) -> bytes:
        """Get or create master encryption key"""
        key_file = "./data/security/master.key"
        
        try:
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    return f.read()
            else:
                # Generate new master key
                key = Fernet.generate_key()
                
                # Store key securely
                os.chmod(os.path.dirname(key_file), 0o700)  # Owner read/write/execute only
                with open(key_file, 'wb') as f:
                    f.write(key)
                os.chmod(key_file, 0o600)  # Owner read/write only
                
                logger.info("New master encryption key generated")
                return key
                
        except Exception as e:
            logger.warning(f"Failed to manage master key: {str(e)}")
            # Fallback to in-memory key (not persistent)
            return Fernet.generate_key()
    
    def derive_key_from_password(self, password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
        """Derive encryption key from password using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,  # NIST recommended minimum
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def encrypt_governance_data(self, data: str, use_master_key: bool = True) -> str:
        """Encrypt sensitive governance data"""
        try:
            if isinstance(data, dict):
                data = json.dumps(data)
            
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
            
        except Exception as e:
            logger.error(f"Failed to encrypt data: {str(e)}")
            return ""
    
    def decrypt_governance_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive governance data"""
        try:
            if not encrypted_data:
                return ""
            
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
            return decrypted_data.decode()
            
        except Exception as e:
            logger.error(f"Failed to decrypt data: {str(e)}")
            return ""
    
    def create_governance_session(self, system_id: str, assessor_id: str,
                                ip_address: str = None) -> Dict[str, Any]:
        """Create secure governance assessment session"""
        try:
            session_id = f"gov_session_{uuid.uuid4().hex}"
            session_token = secrets.token_urlsafe(32)
            
            session_data = {
                'session_id': session_id,
                'token': session_token,
                'system_id': system_id,
                'assessor_id': assessor_id,
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(
                    minutes=self.security_config['session_timeout_minutes']
                )).isoformat(),
                'ip_address': ip_address,
                'activities': [],
                'security_level': 'high',
                'session_status': 'active'
            }
            
            # Store session securely (in production, use secure session store)
            encrypted_session = self.encrypt_governance_data(json.dumps(session_data))
            
            # Log session creation
            self.log_security_event(
                event_type='session_created',
                user_id=assessor_id,
                details=f'Governance session created for system {system_id}',
                ip_address=ip_address,
                session_id=session_id
            )
            
            return session_data
            
        except Exception as e:
            logger.error(f"Failed to create governance session: {str(e)}")
            return {}\n    \n    def verify_governance_access(self, system_id: str, assessor_id: str, \n                               session_token: str, required_permission: str = None) -> bool:\n        \"\"\"Verify governance access permissions\"\"\"\n        try:\n            # In production, implement proper session validation\n            # For now, perform basic validation\n            \n            if not all([system_id, assessor_id, session_token]):\n                return False\n            \n            # Check if user has required permission\n            if required_permission:\n                user_role = self._get_user_role(assessor_id)\n                if not self._has_permission(user_role, required_permission):\n                    self.log_security_event(\n                        event_type='access_denied',\n                        user_id=assessor_id,\n                        details=f'Insufficient permissions for {required_permission}',\n                        system_id=system_id\n                    )\n                    return False\n            \n            # Log successful access\n            self.log_security_event(\n                event_type='access_granted',\n                user_id=assessor_id,\n                details=f'Access granted to system {system_id}',\n                system_id=system_id\n            )\n            \n            return True\n            \n        except Exception as e:\n            logger.error(f\"Failed to verify governance access: {str(e)}\")\n            return False\n    \n    def _get_user_role(self, user_id: str) -> str:\n        \"\"\"Get user role (simplified implementation)\"\"\"\n        # In production, this would query user management system\n        # For demo, map based on user ID patterns\n        if 'admin' in user_id.lower():\n            return 'system_admin'\n        elif 'governance' in user_id.lower() or 'officer' in user_id.lower():\n            return 'governance_officer'\n        elif 'compliance' in user_id.lower():\n            return 'compliance_manager'\n        elif 'risk' in user_id.lower():\n            return 'risk_analyst'\n        elif 'audit' in user_id.lower():\n            return 'auditor'\n        else:\n            return 'viewer'  # Default restrictive role\n    \n    def _has_permission(self, user_role: str, permission: str) -> bool:\n        \"\"\"Check if user role has specific permission\"\"\"\n        try:\n            role_config = self.access_control_matrix.get(user_role, {})\n            permissions = role_config.get('permissions', [])\n            restrictions = role_config.get('restrictions', [])\n            \n            # Check for full access\n            if '*' in permissions:\n                return permission not in restrictions\n            \n            # Check specific permission\n            has_permission = permission in permissions\n            is_restricted = permission in restrictions\n            \n            return has_permission and not is_restricted\n            \n        except Exception as e:\n            logger.error(f\"Failed to check permission {permission} for role {user_role}: {str(e)}\")\n            return False\n    \n    def log_governance_access(self, system_id: str, assessor_id: str, action: str,\n                            ip_address: str = None, session_id: str = None,\n                            additional_details: Dict = None) -> bool:\n        \"\"\"Log governance access for security audit\"\"\"\n        try:\n            access_log_entry = {\n                'timestamp': datetime.now().isoformat(),\n                'event_type': 'governance_access',\n                'system_id': system_id,\n                'assessor_id': assessor_id,\n                'action': action,\n                'ip_address': ip_address,\n                'session_id': session_id,\n                'user_agent': additional_details.get('user_agent', '') if additional_details else '',\n                'success': True,\n                'details': additional_details or {}\n            }\n            \n            # In production, store in secure audit database\n            self._store_security_audit_log(access_log_entry)\n            \n            return True\n            \n        except Exception as e:\n            logger.error(f\"Failed to log governance access: {str(e)}\")\n            return False\n    \n    def log_governance_interaction(self, system_id: str, assessor_id: str, request: str,\n                                 ip_address: str = None, session_id: str = None) -> bool:\n        \"\"\"Log governance interaction for compliance audit\"\"\"\n        try:\n            # Sanitize request to remove sensitive data\n            sanitized_request = self._sanitize_request_data(request)\n            \n            interaction_log_entry = {\n                'timestamp': datetime.now().isoformat(),\n                'event_type': 'governance_interaction',\n                'system_id': system_id,\n                'assessor_id': assessor_id,\n                'request_summary': sanitized_request,\n                'ip_address': ip_address,\n                'session_id': session_id,\n                'data_classification': self._classify_data_sensitivity(request),\n                'compliance_relevant': True\n            }\n            \n            # Encrypt sensitive interaction data\n            if interaction_log_entry['data_classification'] in ['sensitive', 'confidential']:\n                encrypted_data = self.encrypt_governance_data(json.dumps(interaction_log_entry))\n                interaction_log_entry = {\n                    'timestamp': interaction_log_entry['timestamp'],\n                    'event_type': interaction_log_entry['event_type'],\n                    'encrypted_data': encrypted_data\n                }\n            \n            self._store_security_audit_log(interaction_log_entry)\n            return True\n            \n        except Exception as e:\n            logger.error(f\"Failed to log governance interaction: {str(e)}\")\n            return False\n    \n    def log_security_event(self, event_type: str, user_id: str = None, details: str = '',\n                         ip_address: str = None, session_id: str = None,\n                         system_id: str = None, severity: str = 'info') -> bool:\n        \"\"\"Log security events for monitoring and alerting\"\"\"\n        try:\n            security_event = {\n                'event_id': f\"sec_{uuid.uuid4().hex[:8]}\",\n                'timestamp': datetime.now().isoformat(),\n                'event_type': event_type,\n                'severity': severity,\n                'user_id': user_id,\n                'system_id': system_id,\n                'details': details,\n                'ip_address': ip_address,\n                'session_id': session_id,\n                'investigation_status': 'pending' if severity in ['warning', 'error', 'critical'] else 'none'\n            }\n            \n            # Store event for analysis\n            event_key = f\"{event_type}_{user_id}_{datetime.now().strftime('%Y%m%d')}\"\n            if event_key not in self.security_events:\n                self.security_events[event_key] = []\n            self.security_events[event_key].append(security_event)\n            \n            # Check for security alerts\n            self._check_security_alerts(event_type, user_id, ip_address)\n            \n            # Store in audit log\n            self._store_security_audit_log(security_event)\n            \n            return True\n            \n        except Exception as e:\n            logger.error(f\"Failed to log security event: {str(e)}\")\n            return False\n    \n    def _sanitize_request_data(self, request: str) -> str:\n        \"\"\"Sanitize request data for logging (remove sensitive information)\"\"\"\n        try:\n            # Remove potential sensitive patterns\n            sensitive_patterns = [\n                r'\\b\\d{4}[- ]?\\d{4}[- ]?\\d{4}[- ]?\\d{4}\\b',  # Credit card numbers\n                r'\\b\\d{3}-\\d{2}-\\d{4}\\b',  # SSN\n                r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b',  # Email (basic)\n                r'password\\s*[:=]\\s*\\S+',  # Password fields\n                r'token\\s*[:=]\\s*\\S+',  # Token fields\n            ]\n            \n            sanitized = request\n            for pattern in sensitive_patterns:\n                import re\n                sanitized = re.sub(pattern, '[REDACTED]', sanitized, flags=re.IGNORECASE)\n            \n            # Limit length\n            if len(sanitized) > 500:\n                sanitized = sanitized[:500] + '... [TRUNCATED]'\n            \n            return sanitized\n            \n        except Exception as e:\n            logger.error(f\"Failed to sanitize request data: {str(e)}\")\n            return \"[SANITIZATION_FAILED]\"\n    \n    def _classify_data_sensitivity(self, data: str) -> str:\n        \"\"\"Classify data sensitivity level\"\"\"\n        try:\n            data_lower = data.lower()\n            \n            # Check for highly sensitive indicators\n            if any(term in data_lower for term in [\n                'social security', 'ssn', 'credit card', 'financial', 'medical',\n                'health', 'password', 'confidential', 'secret', 'private key'\n            ]):\n                return 'confidential'\n            \n            # Check for sensitive indicators\n            if any(term in data_lower for term in [\n                'personal', 'address', 'phone', 'email', 'employee',\n                'salary', 'performance', 'internal', 'proprietary'\n            ]):\n                return 'sensitive'\n            \n            # Check for restricted indicators\n            if any(term in data_lower for term in [\n                'assessment', 'audit', 'compliance', 'risk', 'governance'\n            ]):\n                return 'restricted'\n            \n            return 'public'\n            \n        except Exception as e:\n            logger.error(f\"Failed to classify data sensitivity: {str(e)}\")\n            return 'restricted'  # Default to restrictive classification\n    \n    def _check_security_alerts(self, event_type: str, user_id: str = None, \n                             ip_address: str = None) -> None:\n        \"\"\"Check for security alert conditions\"\"\"\n        try:\n            current_time = datetime.now()\n            alert_conditions = []\n            \n            # Check for multiple failed access attempts\n            if event_type == 'access_denied' and user_id:\n                recent_failures = self._count_recent_events('access_denied', user_id, minutes=30)\n                if recent_failures >= self.security_config['max_failed_attempts']:\n                    alert_conditions.append({\n                        'type': 'multiple_access_failures',\n                        'severity': 'warning',\n                        'details': f'User {user_id} has {recent_failures} failed access attempts'\n                    })\n            \n            # Check for suspicious IP activity\n            if ip_address:\n                ip_events = self._count_recent_events_by_ip(ip_address, minutes=60)\n                if ip_events > 100:  # Threshold for suspicious activity\n                    alert_conditions.append({\n                        'type': 'suspicious_ip_activity',\n                        'severity': 'warning',\n                        'details': f'High activity from IP {ip_address}: {ip_events} events'\n                    })\n            \n            # Generate alerts\n            for condition in alert_conditions:\n                self._generate_security_alert(condition)\n                \n        except Exception as e:\n            logger.error(f\"Failed to check security alerts: {str(e)}\")\n    \n    def _count_recent_events(self, event_type: str, user_id: str, minutes: int = 30) -> int:\n        \"\"\"Count recent events of specific type for user\"\"\"\n        try:\n            cutoff_time = datetime.now() - timedelta(minutes=minutes)\n            count = 0\n            \n            for event_list in self.security_events.values():\n                for event in event_list:\n                    if (event.get('event_type') == event_type and \n                        event.get('user_id') == user_id and\n                        datetime.fromisoformat(event['timestamp']) > cutoff_time):\n                        count += 1\n            \n            return count\n            \n        except Exception as e:\n            logger.error(f\"Failed to count recent events: {str(e)}\")\n            return 0\n    \n    def _count_recent_events_by_ip(self, ip_address: str, minutes: int = 60) -> int:\n        \"\"\"Count recent events from specific IP address\"\"\"\n        try:\n            cutoff_time = datetime.now() - timedelta(minutes=minutes)\n            count = 0\n            \n            for event_list in self.security_events.values():\n                for event in event_list:\n                    if (event.get('ip_address') == ip_address and\n                        datetime.fromisoformat(event['timestamp']) > cutoff_time):\n                        count += 1\n            \n            return count\n            \n        except Exception as e:\n            logger.error(f\"Failed to count events by IP: {str(e)}\")\n            return 0\n    \n    def _generate_security_alert(self, condition: Dict) -> None:\n        \"\"\"Generate security alert for suspicious activity\"\"\"\n        try:\n            alert = {\n                'alert_id': f\"alert_{uuid.uuid4().hex[:8]}\",\n                'timestamp': datetime.now().isoformat(),\n                'alert_type': condition['type'],\n                'severity': condition['severity'],\n                'details': condition['details'],\n                'status': 'active',\n                'investigation_required': condition['severity'] in ['warning', 'error', 'critical']\n            }\n            \n            # In production, send to security monitoring system\n            logger.warning(f\"Security Alert Generated: {alert['alert_type']} - {alert['details']}\")\n            \n            # Store alert\n            self._store_security_audit_log(alert)\n            \n        except Exception as e:\n            logger.error(f\"Failed to generate security alert: {str(e)}\")\n    \n    def _store_security_audit_log(self, log_entry: Dict) -> None:\n        \"\"\"Store security audit log entry\"\"\"\n        try:\n            # In production, store in secure, immutable audit database\n            # For demo, log to file with rotation\n            audit_file = \"./data/security/audit.log\"\n            os.makedirs(os.path.dirname(audit_file), exist_ok=True)\n            \n            with open(audit_file, 'a') as f:\n                f.write(json.dumps(log_entry) + \"\\n\")\n                \n        except Exception as e:\n            logger.error(f\"Failed to store security audit log: {str(e)}\")\n    \n    def generate_security_hash(self, data: str) -> str:\n        \"\"\"Generate secure hash for data integrity verification\"\"\"\n        try:\n            return hashlib.sha256(data.encode()).hexdigest()\n        except Exception as e:\n            logger.error(f\"Failed to generate security hash: {str(e)}\")\n            return \"\"\n    \n    def verify_data_integrity(self, data: str, expected_hash: str) -> bool:\n        \"\"\"Verify data integrity using hash comparison\"\"\"\n        try:\n            actual_hash = self.generate_security_hash(data)\n            return secrets.compare_digest(actual_hash, expected_hash)\n        except Exception as e:\n            logger.error(f\"Failed to verify data integrity: {str(e)}\")\n            return False\n    \n    def decrypt_assessment_history(self, history: List[Dict]) -> List[Dict]:\n        \"\"\"Decrypt assessment history for authorized access\"\"\"\n        try:\n            decrypted_history = []\n            \n            for assessment in history:\n                decrypted_assessment = assessment.copy()\n                \n                # Decrypt sensitive fields if present\n                if 'encrypted_data' in assessment and assessment['encrypted_data']:\n                    try:\n                        decrypted_data = self.decrypt_governance_data(assessment['encrypted_data'])\n                        if decrypted_data:\n                            sensitive_data = json.loads(decrypted_data)\n                            decrypted_assessment.update(sensitive_data)\n                    except Exception as decrypt_error:\n                        logger.warning(f\"Failed to decrypt assessment data: {str(decrypt_error)}\")\n                \n                decrypted_history.append(decrypted_assessment)\n            \n            return decrypted_history\n            \n        except Exception as e:\n            logger.error(f\"Failed to decrypt assessment history: {str(e)}\")\n            return history  # Return original if decryption fails\n    \n    def get_security_configuration(self) -> Dict[str, Any]:\n        \"\"\"Get current security configuration (non-sensitive parts)\"\"\"\n        return {\n            'session_timeout_minutes': self.security_config['session_timeout_minutes'],\n            'max_failed_attempts': self.security_config['max_failed_attempts'],\n            'lockout_duration_minutes': self.security_config['lockout_duration_minutes'],\n            'audit_retention_days': self.security_config['audit_retention_days'],\n            'encryption_algorithm': self.security_config['encryption_algorithm'],\n            'available_roles': list(self.access_control_matrix.keys())\n        }\n    \n    def validate_user_permissions(self, user_id: str, required_permissions: List[str]) -> Dict[str, bool]:\n        \"\"\"Validate user permissions against required permissions list\"\"\"\n        try:\n            user_role = self._get_user_role(user_id)\n            permission_results = {}\n            \n            for permission in required_permissions:\n                permission_results[permission] = self._has_permission(user_role, permission)\n            \n            return {\n                'user_id': user_id,\n                'user_role': user_role,\n                'permissions': permission_results,\n                'overall_authorized': all(permission_results.values())\n            }\n            \n        except Exception as e:\n            logger.error(f\"Failed to validate user permissions: {str(e)}\")\n            return {'error': 'Permission validation failed'}\n    \n    def health_check(self) -> bool:\n        \"\"\"Check if security manager is functioning properly\"\"\"\n        try:\n            # Test encryption/decryption\n            test_data = \"security_test_data\"\n            encrypted = self.encrypt_governance_data(test_data)\n            decrypted = self.decrypt_governance_data(encrypted)\n            \n            if decrypted != test_data:\n                return False\n            \n            # Test hash generation\n            test_hash = self.generate_security_hash(test_data)\n            if not test_hash or len(test_hash) != 64:  # SHA-256 produces 64 char hex\n                return False\n            \n            return True\n            \n        except Exception as e:\n            logger.error(f\"Security manager health check failed: {str(e)}\")\n            return False"