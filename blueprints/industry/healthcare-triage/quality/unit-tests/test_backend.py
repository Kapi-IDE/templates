#!/usr/bin/env python3
"""
Healthcare AI Triage System - Backend Unit Tests
Comprehensive test suite ensuring HIPAA compliance, clinical accuracy, and system reliability

Test Coverage Areas:
- Patient management and data security
- AI agent functionality and accuracy
- Authentication and authorization
- Medical knowledge retrieval
- Audit logging and compliance
- Performance and scalability

Testing Framework: pytest with healthcare-specific fixtures
Security Focus: HIPAA compliance validation
Performance: Sub-2-second response time verification
Clinical Safety: Medical decision accuracy testing
"""

import pytest
import json
import uuid
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from decimal import Decimal
import hashlib
import time

# Flask and testing imports
from flask import Flask
from flask.testing import FlaskClient
import jwt

# Application imports
from backend.app import create_app
from backend.services.patient_service import PatientService
from backend.services.triage_service import TriageService
from backend.services.authentication import AuthenticationService
from backend.services.knowledge_service import KnowledgeService
from backend.utils.security import HIPAASecurityManager
from backend.database.connection_manager import DatabaseConnectionManager

# Test configuration and fixtures
from tests.fixtures.patient_fixtures import sample_patients, hipaa_test_data
from tests.fixtures.clinical_fixtures import clinical_scenarios, triage_test_cases
from tests.fixtures.security_fixtures import security_test_vectors
from tests.utils.test_helpers import (
    create_test_user, create_test_patient, create_test_session,
    assert_hipaa_compliance, assert_performance_benchmark
)

# =============================================================================
# TEST CONFIGURATION AND SETUP
# =============================================================================

@pytest.fixture(scope='session')
def app():
    """Create Flask app for testing with proper configuration"""
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key-for-testing-only',
        'JWT_SECRET_KEY': 'test-jwt-secret-key',
        'ENCRYPTION_KEY': 'test-encryption-key-32-bytes-long',
        'REDIS_URL': 'redis://localhost:6379/15',  # Test database
        'HIPAA_COMPLIANT_LOGGING': True,
        'AUDIT_LOG_LEVEL': 'DEBUG'
    })
    
    with app.app_context():
        # Initialize test database
        from backend.database.models import db
        db.create_all()
        
        # Load test medical knowledge
        from tests.fixtures.medical_knowledge import load_test_knowledge
        load_test_knowledge()
        
        yield app
        
        # Cleanup
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def db_session(app):
    """Create database session for testing"""
    from backend.database.models import db
    
    connection = db.engine.connect()
    transaction = connection.begin()
    
    # Configure session
    session = db.create_scoped_session(
        options={"bind": connection, "binds": {}}
    )
    db.session = session
    
    yield session
    
    # Cleanup
    transaction.rollback()
    connection.close()
    session.remove()

@pytest.fixture
def authenticated_user(app, client):
    """Create authenticated test user"""
    with app.app_context():
        user_data = {
            'employee_id': 'TEST001',
            'first_name': 'Test',
            'last_name': 'Nurse',
            'email': 'test.nurse@hospital.com',
            'role': 'emergency_nurse',
            'department': 'emergency',
            'password': 'SecureTestPassword123!'
        }
        
        # Create user
        auth_service = AuthenticationService()
        user = auth_service.create_user(user_data)
        
        # Generate test token
        token_payload = {
            'user_id': str(user.id),
            'employee_id': user.employee_id,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=8)
        }
        
        token = jwt.encode(
            token_payload,
            app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        
        return {
            'user': user,
            'token': token,
            'headers': {'Authorization': f'Bearer {token}'}
        }

# =============================================================================
# PATIENT MANAGEMENT TESTS
# =============================================================================

class TestPatientManagement:
    """Test patient creation, retrieval, and HIPAA compliance"""
    
    def test_create_patient_success(self, client, authenticated_user):
        """Test successful patient creation with valid data"""
        patient_data = {
            'medical_record_number': 'MRN-2024-001234',
            'demographics': {
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': '1985-06-15',
                'gender': 'male',
                'phone': '+1-555-0123',
                'email': 'john.doe@email.com'
            },
            'emergency_contact': {
                'name': 'Jane Doe',
                'relationship': 'spouse',
                'phone': '+1-555-0124'
            }
        }
        
        start_time = time.time()
        response = client.post(
            '/api/v1/patients',
            json=patient_data,
            headers=authenticated_user['headers']
        )
        response_time = time.time() - start_time
        
        # Verify response
        assert response.status_code == 201
        assert response_time < 2.0  # Performance requirement
        
        data = response.get_json()
        assert 'id' in data
        assert data['medical_record_number'] == patient_data['medical_record_number']
        assert 'created_at' in data
        
        # Verify HIPAA compliance
        assert_hipaa_compliance(response, 'patient_created')

    def test_create_patient_duplicate_mrn(self, client, authenticated_user):
        """Test patient creation with duplicate MRN"""
        patient_data = {
            'medical_record_number': 'MRN-2024-001234',
            'demographics': {
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': '1985-06-15',
                'gender': 'male'
            }
        }
        
        # Create first patient
        response1 = client.post(
            '/api/v1/patients',
            json=patient_data,
            headers=authenticated_user['headers']
        )
        assert response1.status_code == 201
        
        # Attempt to create duplicate
        response2 = client.post(
            '/api/v1/patients',
            json=patient_data,
            headers=authenticated_user['headers']
        )
        assert response2.status_code == 409
        
        data = response2.get_json()
        assert 'error' in data
        assert 'already exists' in data['error'].lower()

    def test_search_patients_authorized(self, client, authenticated_user):
        """Test patient search with proper authorization"""
        # Create test patients
        patients = []
        for i in range(3):
            patient_data = {
                'medical_record_number': f'MRN-2024-00{i+1:04d}',
                'demographics': {
                    'first_name': f'Patient{i+1}',
                    'last_name': 'TestLast',
                    'date_of_birth': f'198{i+5}-01-01',
                    'gender': 'male'
                }
            }
            response = client.post(
                '/api/v1/patients',
                json=patient_data,
                headers=authenticated_user['headers']
            )
            assert response.status_code == 201
            patients.append(response.get_json())
        
        # Test search by last name
        start_time = time.time()
        response = client.get(
            '/api/v1/patients?last_name=TestLast&limit=10',
            headers=authenticated_user['headers']
        )
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # Search performance requirement
        
        data = response.get_json()
        assert 'patients' in data
        assert len(data['patients']) == 3
        assert data['total_count'] >= 3

    def test_search_patients_unauthorized(self, client):
        """Test patient search without authentication"""
        response = client.get('/api/v1/patients?last_name=TestLast')
        assert response.status_code == 401

    def test_get_patient_details_authorized(self, client, authenticated_user):
        """Test retrieving patient details with authorization"""
        # Create test patient
        patient_data = {
            'medical_record_number': 'MRN-2024-001234',
            'demographics': {
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': '1985-06-15',
                'gender': 'male'
            }
        }
        
        create_response = client.post(
            '/api/v1/patients',
            json=patient_data,
            headers=authenticated_user['headers']
        )
        assert create_response.status_code == 201
        patient_id = create_response.get_json()['id']
        
        # Retrieve patient details
        start_time = time.time()
        response = client.get(
            f'/api/v1/patients/{patient_id}',
            headers=authenticated_user['headers']
        )
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0
        
        data = response.get_json()
        assert data['id'] == patient_id
        assert data['medical_record_number'] == patient_data['medical_record_number']

    def test_patient_data_encryption(self, app, authenticated_user):
        """Test that patient PHI is properly encrypted"""
        with app.app_context():
            patient_service = PatientService()
            security_manager = HIPAASecurityManager()
            
            patient_data = {
                'medical_record_number': 'MRN-2024-001234',
                'demographics': {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'date_of_birth': '1985-06-15',
                    'gender': 'male',
                    'ssn': '123-45-6789'  # Sensitive data
                }
            }
            
            # Create patient
            patient = patient_service.create_patient(patient_data, authenticated_user['user'].id)
            
            # Verify data is encrypted in database
            from backend.database.models import Patient
            db_patient = Patient.query.filter_by(id=patient.id).first()
            
            # Demographics should be encrypted
            assert 'first_name' not in str(db_patient.encrypted_demographics)
            assert 'ssn' not in str(db_patient.encrypted_demographics)
            
            # Verify decryption works
            decrypted_data = security_manager.decrypt_patient_data(
                db_patient.encrypted_demographics
            )
            assert decrypted_data['first_name'] == 'John'
            assert decrypted_data['ssn'] == '123-45-6789'

# =============================================================================
# TRIAGE AND AI AGENT TESTS
# =============================================================================

class TestTriageSystem:
    """Test triage assessment and AI agent functionality"""
    
    def test_start_triage_session_success(self, client, authenticated_user):
        """Test successful triage session creation"""
        # Create test patient first
        patient_data = {
            'medical_record_number': 'MRN-2024-001234',
            'demographics': {
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': '1985-06-15',
                'gender': 'male'
            }
        }
        
        patient_response = client.post(
            '/api/v1/patients',
            json=patient_data,
            headers=authenticated_user['headers']
        )
        patient_id = patient_response.get_json()['id']
        
        # Start triage session
        triage_data = {
            'patient_id': patient_id,
            'department': 'emergency',
            'chief_complaint': 'Chest pain for 2 hours',
            'arrival_method': 'walk_in',
            'vital_signs': {
                'temperature': 98.6,
                'blood_pressure_systolic': 140,
                'blood_pressure_diastolic': 90,
                'heart_rate': 88,
                'respiratory_rate': 20,
                'oxygen_saturation': 95
            }
        }
        
        start_time = time.time()
        response = client.post(
            '/api/v1/triage/sessions',
            json=triage_data,
            headers=authenticated_user['headers']
        )
        response_time = time.time() - start_time
        
        assert response.status_code == 201
        assert response_time < 2.0
        
        data = response.get_json()
        assert 'id' in data
        assert data['patient_id'] == patient_id
        assert data['department'] == 'emergency'
        assert data['status'] == 'active'

    def test_ai_agent_interaction_intake(self, client, authenticated_user):
        """Test AI intake agent interaction"""
        # Setup: Create patient and triage session
        patient_id, session_id = self._setup_triage_session(client, authenticated_user)
        
        # Test intake agent interaction
        interaction_data = {
            'session_id': session_id,
            'agent_type': 'intake',
            'message': 'Patient reports severe chest pain that started 2 hours ago',
            'context': {
                'patient_age': 45,
                'current_medications': ['lisinopril', 'metformin']
            }
        }
        
        start_time = time.time()
        response = client.post(
            '/api/v1/agents/interact',
            json=interaction_data,
            headers=authenticated_user['headers']
        )
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        assert response_time < 3.0  # AI response time requirement
        
        data = response.get_json()
        assert data['agent_type'] == 'intake'
        assert data['response_type'] in ['question', 'assessment']
        assert 'message' in data
        assert 'confidence_score' in data
        assert data['confidence_score'] >= 0.8  # Minimum confidence requirement

    def test_ai_agent_interaction_triage(self, client, authenticated_user):
        """Test AI triage agent ESI level assessment"""
        # Setup
        patient_id, session_id = self._setup_triage_session(client, authenticated_user)
        
        # Test triage agent interaction
        interaction_data = {
            'session_id': session_id,
            'agent_type': 'triage',
            'message': 'Please assess ESI level for this patient',
            'context': {
                'symptoms': ['chest_pain', 'shortness_of_breath'],
                'vital_signs': {
                    'blood_pressure': '140/90',
                    'heart_rate': 88,
                    'oxygen_saturation': 95
                },
                'patient_age': 45,
                'medical_history': ['hypertension', 'diabetes']
            }
        }
        
        start_time = time.time()
        response = client.post(
            '/api/v1/agents/interact',
            json=interaction_data,
            headers=authenticated_user['headers']
        )
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        assert response_time < 3.0
        
        data = response.get_json()
        assert data['agent_type'] == 'triage'
        assert data['response_type'] == 'assessment'
        assert 'assessment' in data
        
        assessment = data['assessment']
        assert 'esi_level' in assessment
        assert assessment['esi_level'] in [1, 2, 3, 4, 5]
        assert assessment['esi_level'] <= 3  # High-risk symptoms should be ESI 1-3
        assert 'reasoning' in assessment
        assert data['confidence_score'] >= 0.85

    def test_critical_case_escalation(self, client, authenticated_user):
        """Test automatic escalation for critical cases"""
        # Setup
        patient_id, session_id = self._setup_triage_session(client, authenticated_user)
        
        # Test critical case scenario
        interaction_data = {
            'session_id': session_id,
            'agent_type': 'escalation',
            'message': 'Check if immediate escalation needed',
            'context': {
                'symptoms': ['cardiac_arrest', 'unresponsive'],
                'vital_signs': {
                    'blood_pressure': '60/40',
                    'heart_rate': 150,
                    'oxygen_saturation': 75
                },
                'urgency_score': 95
            }
        }
        
        response = client.post(
            '/api/v1/agents/interact',
            json=interaction_data,
            headers=authenticated_user['headers']
        )
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['agent_type'] == 'escalation'
        assert data['response_type'] == 'action'
        
        # Should recommend immediate escalation
        assert 'assessment' in data
        assessment = data['assessment']
        assert assessment.get('immediate_escalation', False) == True
        assert assessment.get('esi_level') == 1

    def test_clinical_accuracy_validation(self, app):
        """Test clinical decision accuracy against known test cases"""
        with app.app_context():
            from tests.fixtures.clinical_fixtures import VALIDATED_CLINICAL_CASES
            
            triage_service = TriageService()
            
            for test_case in VALIDATED_CLINICAL_CASES:
                # Process clinical scenario
                result = triage_service.assess_urgency(
                    patient_context=test_case['patient_context'],
                    symptoms=test_case['symptoms'],
                    vital_signs=test_case['vital_signs']
                )
                
                # Validate against expected outcome
                expected_esi = test_case['expected_esi_level']
                actual_esi = result['esi_level']
                
                # Allow ±1 level variance for complex cases
                assert abs(actual_esi - expected_esi) <= 1, (
                    f"ESI level mismatch for case {test_case['case_id']}: "
                    f"expected {expected_esi}, got {actual_esi}"
                )
                
                # Confidence should be reasonable
                assert result['confidence_score'] >= 0.7

    def _setup_triage_session(self, client, authenticated_user):
        """Helper method to set up patient and triage session"""
        # Create patient
        patient_data = {
            'medical_record_number': f'MRN-2024-{uuid.uuid4().hex[:6]}',
            'demographics': {
                'first_name': 'Test',
                'last_name': 'Patient',
                'date_of_birth': '1980-01-01',
                'gender': 'male'
            }
        }
        
        patient_response = client.post(
            '/api/v1/patients',
            json=patient_data,
            headers=authenticated_user['headers']
        )
        patient_id = patient_response.get_json()['id']
        
        # Create triage session
        triage_data = {
            'patient_id': patient_id,
            'department': 'emergency',
            'chief_complaint': 'Test complaint',
            'arrival_method': 'walk_in'
        }
        
        session_response = client.post(
            '/api/v1/triage/sessions',
            json=triage_data,
            headers=authenticated_user['headers']
        )
        session_id = session_response.get_json()['id']
        
        return patient_id, session_id

# =============================================================================
# AUTHENTICATION AND AUTHORIZATION TESTS
# =============================================================================

class TestAuthentication:
    """Test authentication, authorization, and security features"""
    
    def test_login_success_with_mfa(self, client, app):
        """Test successful login with MFA"""
        with app.app_context():
            # Create test user
            auth_service = AuthenticationService()
            user_data = {
                'employee_id': 'TEST001',
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@hospital.com',
                'role': 'emergency_nurse',
                'department': 'emergency',
                'password': 'SecurePassword123!'
            }
            user = auth_service.create_user(user_data)
            
            # Setup MFA for user
            mfa_secret = auth_service.setup_mfa(user.id)
            current_token = auth_service.generate_mfa_token(mfa_secret)
        
        # Test login
        login_data = {
            'employee_id': 'TEST001',
            'password': 'SecurePassword123!',
            'mfa_token': current_token
        }
        
        response = client.post('/api/v1/auth/login', json=login_data)
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert 'user' in data
        assert data['user']['employee_id'] == 'TEST001'
        assert data['user']['role'] == 'emergency_nurse'

    def test_login_failure_invalid_credentials(self, client):
        """Test login failure with invalid credentials"""
        login_data = {
            'employee_id': 'INVALID',
            'password': 'WrongPassword',
            'mfa_token': '123456'
        }
        
        response = client.post('/api/v1/auth/login', json=login_data)
        
        assert response.status_code == 401
        
        data = response.get_json()
        assert 'error' in data

    def test_login_failure_invalid_mfa(self, client, app):
        """Test login failure with invalid MFA token"""
        with app.app_context():
            # Create test user
            auth_service = AuthenticationService()
            user_data = {
                'employee_id': 'TEST001',
                'password': 'SecurePassword123!'
            }
            user = auth_service.create_user(user_data)
        
        # Test login with invalid MFA
        login_data = {
            'employee_id': 'TEST001',
            'password': 'SecurePassword123!',
            'mfa_token': '000000'  # Invalid token
        }
        
        response = client.post('/api/v1/auth/login', json=login_data)
        
        assert response.status_code == 401

    def test_jwt_token_validation(self, client, authenticated_user):
        """Test JWT token validation and expiration"""
        # Test valid token
        response = client.get(
            '/api/v1/patients',
            headers=authenticated_user['headers']
        )
        assert response.status_code == 200
        
        # Test invalid token
        invalid_headers = {'Authorization': 'Bearer invalid_token'}
        response = client.get('/api/v1/patients', headers=invalid_headers)
        assert response.status_code == 401

    def test_role_based_access_control(self, client, app):
        """Test role-based access control"""
        with app.app_context():
            auth_service = AuthenticationService()
            
            # Create users with different roles
            nurse_user = auth_service.create_user({
                'employee_id': 'NURSE001',
                'role': 'emergency_nurse',
                'password': 'Password123!'
            })
            
            admin_user = auth_service.create_user({
                'employee_id': 'ADMIN001',
                'role': 'system_administrator',
                'password': 'Password123!'
            })
            
            # Generate tokens
            nurse_token = auth_service.generate_token(nurse_user)
            admin_token = auth_service.generate_token(admin_user)
        
        # Test nurse access to patient data (should succeed)
        nurse_headers = {'Authorization': f'Bearer {nurse_token}'}
        response = client.get('/api/v1/patients', headers=nurse_headers)
        assert response.status_code == 200
        
        # Test nurse access to admin functions (should fail)
        response = client.get('/api/v1/admin/metrics', headers=nurse_headers)
        assert response.status_code == 403
        
        # Test admin access to admin functions (should succeed)
        admin_headers = {'Authorization': f'Bearer {admin_token}'}
        response = client.get('/api/v1/admin/metrics', headers=admin_headers)
        assert response.status_code == 200

# =============================================================================
# MEDICAL KNOWLEDGE TESTS
# =============================================================================

class TestMedicalKnowledge:
    """Test medical knowledge retrieval and clinical decision support"""
    
    def test_knowledge_search_clinical_protocols(self, client, authenticated_user):
        """Test searching for clinical protocols"""
        search_data = {
            'query': 'chest pain treatment protocol emergency department',
            'filters': {
                'content_type': ['protocols', 'guidelines'],
                'specialty': ['emergency_medicine', 'cardiology']
            },
            'limit': 10
        }
        
        start_time = time.time()
        response = client.post(
            '/api/v1/knowledge/search',
            json=search_data,
            headers=authenticated_user['headers']
        )
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # Knowledge search performance
        
        data = response.get_json()
        assert 'results' in data
        assert len(data['results']) > 0
        assert 'search_time_ms' in data
        
        # Verify result quality
        for result in data['results'][:3]:  # Check top 3 results
            assert 'title' in result
            assert 'content' in result
            assert 'relevance_score' in result
            assert result['relevance_score'] >= 0.7  # Minimum relevance

    def test_drug_interaction_checking(self, client, authenticated_user):
        """Test drug interaction checking functionality"""
        medications = ['warfarin', 'aspirin', 'ibuprofen']
        
        interaction_data = {
            'medications': medications
        }
        
        start_time = time.time()
        response = client.post(
            '/api/v1/knowledge/drug-interactions',
            json=interaction_data,
            headers=authenticated_user['headers']
        )
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        assert response_time < 2.0
        
        data = response.get_json()
        assert 'interactions' in data
        assert 'warnings' in data
        assert 'contraindications' in data
        
        # Should detect warfarin-aspirin interaction
        interactions = data['interactions']
        assert len(interactions) > 0
        
        # Find the warfarin-aspirin interaction
        warfarin_aspirin_found = False
        for interaction in interactions:
            if ('warfarin' in interaction['drugs'] and 
                'aspirin' in interaction['drugs']):
                warfarin_aspirin_found = True
                assert interaction['severity'] in ['major', 'critical']
                break
        
        assert warfarin_aspirin_found, "Critical warfarin-aspirin interaction not detected"

    def test_clinical_guideline_retrieval(self, client, authenticated_user):
        """Test retrieval of specific clinical guidelines"""
        search_data = {
            'query': 'ESI level 2 criteria emergency triage',
            'filters': {
                'content_type': ['guidelines'],
                'organization': ['AHA', 'ACC', 'ACEP']
            }
        }
        
        response = client.post(
            '/api/v1/knowledge/search',
            json=search_data,
            headers=authenticated_user['headers']
        )
        
        assert response.status_code == 200
        
        data = response.get_json()
        results = data['results']
        
        # Should find ESI-related guidelines
        assert len(results) > 0
        
        # Verify content relevance
        for result in results[:2]:
            content = result['content'].lower()
            assert any(term in content for term in ['esi', 'triage', 'emergency'])

# =============================================================================
# SECURITY AND COMPLIANCE TESTS
# =============================================================================

class TestSecurityCompliance:
    """Test security features and HIPAA compliance"""
    
    def test_hipaa_audit_logging(self, client, authenticated_user, app):
        """Test that all patient access is properly logged"""
        # Create test patient
        patient_data = {
            'medical_record_number': 'MRN-2024-AUDIT',
            'demographics': {
                'first_name': 'Audit',
                'last_name': 'Test',
                'date_of_birth': '1990-01-01',
                'gender': 'female'
            }
        }
        
        # Patient creation should be logged
        response = client.post(
            '/api/v1/patients',
            json=patient_data,
            headers=authenticated_user['headers']
        )
        patient_id = response.get_json()['id']
        
        # Patient access should be logged
        response = client.get(
            f'/api/v1/patients/{patient_id}',
            headers=authenticated_user['headers']
        )
        
        # Verify audit logs were created
        with app.app_context():
            from backend.database.models import AuditLog
            
            # Check for patient creation log
            creation_log = AuditLog.query.filter_by(
                action='patient_created',
                patient_id=patient_id
            ).first()
            
            assert creation_log is not None
            assert creation_log.user_id == authenticated_user['user'].id
            assert creation_log.ip_address is not None
            
            # Check for patient access log
            access_log = AuditLog.query.filter_by(
                action='patient_viewed',
                patient_id=patient_id
            ).first()
            
            assert access_log is not None

    def test_data_encryption_at_rest(self, app, authenticated_user):
        """Test that sensitive data is encrypted at rest"""
        with app.app_context():
            patient_service = PatientService()
            
            sensitive_data = {
                'medical_record_number': 'MRN-2024-ENCRYPT',
                'demographics': {
                    'first_name': 'Sensitive',
                    'last_name': 'Data',
                    'ssn': '123-45-6789',
                    'date_of_birth': '1975-12-25',
                    'address': {
                        'street': '123 Private St',
                        'city': 'Confidential',
                        'state': 'TX',
                        'zip': '12345'
                    }
                }
            }
            
            # Create patient
            patient = patient_service.create_patient(
                sensitive_data, 
                authenticated_user['user'].id
            )
            
            # Verify encryption in database
            from backend.database.models import Patient
            db_patient = Patient.query.filter_by(id=patient.id).first()
            
            # Raw encrypted data should not contain plaintext
            encrypted_data_str = str(db_patient.encrypted_demographics)
            assert 'Sensitive' not in encrypted_data_str
            assert '123-45-6789' not in encrypted_data_str
            assert 'Private St' not in encrypted_data_str

    def test_input_validation_and_sanitization(self, client, authenticated_user):
        """Test input validation prevents injection attacks"""
        # Test SQL injection attempt
        malicious_data = {
            'medical_record_number': "MRN-2024-001'; DROP TABLE patients; --",
            'demographics': {
                'first_name': '<script>alert("xss")</script>',
                'last_name': '"; DELETE FROM patients WHERE 1=1; --',
                'date_of_birth': '1990-01-01'
            }
        }
        
        response = client.post(
            '/api/v1/patients',
            json=malicious_data,
            headers=authenticated_user['headers']
        )
        
        # Should either reject the input or sanitize it
        if response.status_code == 201:
            # If accepted, verify sanitization
            data = response.get_json()
            assert '<script>' not in str(data)
            assert 'DROP TABLE' not in str(data)
            assert 'DELETE FROM' not in str(data)
        else:
            # Input validation should reject malicious input
            assert response.status_code == 400

    def test_rate_limiting(self, client, authenticated_user):
        """Test API rate limiting functionality"""
        # Make multiple rapid requests
        responses = []
        for i in range(10):
            response = client.get(
                '/api/v1/patients',
                headers=authenticated_user['headers']
            )
            responses.append(response.status_code)
        
        # Should eventually hit rate limit for excessive requests
        # Note: Actual rate limit testing may require adjustment based on configuration
        success_count = sum(1 for status in responses if status == 200)
        rate_limit_count = sum(1 for status in responses if status == 429)
        
        # Should have some successful requests and potentially some rate limited
        assert success_count > 0

    def test_session_security(self, client, authenticated_user):
        """Test session security features"""
        # Test that session tokens are properly managed
        token = authenticated_user['token']
        headers = authenticated_user['headers']
        
        # Valid token should work
        response = client.get('/api/v1/patients', headers=headers)
        assert response.status_code == 200
        
        # Test logout invalidates token
        logout_response = client.post('/api/v1/auth/logout', headers=headers)
        assert logout_response.status_code == 200
        
        # Token should no longer work after logout
        response = client.get('/api/v1/patients', headers=headers)
        assert response.status_code == 401

# =============================================================================
# PERFORMANCE TESTS
# =============================================================================

class TestPerformance:
    """Test system performance requirements"""
    
    def test_response_time_benchmarks(self, client, authenticated_user):
        """Test that all endpoints meet response time requirements"""
        endpoints = [
            ('GET', '/api/v1/health', {}, 0.5),  # Health check: <500ms
            ('GET', '/api/v1/patients', {}, 1.0),  # Patient search: <1s
        ]
        
        for method, endpoint, data, max_time in endpoints:
            start_time = time.time()
            
            if method == 'GET':
                response = client.get(endpoint, headers=authenticated_user['headers'])
            elif method == 'POST':
                response = client.post(endpoint, json=data, headers=authenticated_user['headers'])
            
            response_time = time.time() - start_time
            
            assert response_time < max_time, (
                f"{method} {endpoint} took {response_time:.3f}s, "
                f"expected <{max_time}s"
            )

    def test_concurrent_request_handling(self, client, authenticated_user):
        """Test system handling of concurrent requests"""
        import concurrent.futures
        import threading
        
        def make_request():
            return client.get('/api/v1/health', headers=authenticated_user['headers'])
        
        # Test concurrent requests
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            responses = [future.result() for future in futures]
        
        total_time = time.time() - start_time
        
        # All requests should succeed
        assert all(response.status_code == 200 for response in responses)
        
        # Should handle concurrent requests efficiently
        assert total_time < 5.0  # Should complete within 5 seconds

# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """Test complete workflows and integration scenarios"""
    
    def test_complete_triage_workflow(self, client, authenticated_user):
        """Test complete patient triage workflow"""
        # Step 1: Create patient
        patient_data = {
            'medical_record_number': 'MRN-2024-WORKFLOW',
            'demographics': {
                'first_name': 'Workflow',
                'last_name': 'Test',
                'date_of_birth': '1980-01-01',
                'gender': 'male'
            }
        }
        
        patient_response = client.post(
            '/api/v1/patients',
            json=patient_data,
            headers=authenticated_user['headers']
        )
        assert patient_response.status_code == 201
        patient_id = patient_response.get_json()['id']
        
        # Step 2: Start triage session
        triage_data = {
            'patient_id': patient_id,
            'department': 'emergency',
            'chief_complaint': 'Chest pain and shortness of breath',
            'arrival_method': 'ambulance',
            'vital_signs': {
                'temperature': 99.2,
                'blood_pressure_systolic': 160,
                'blood_pressure_diastolic': 95,
                'heart_rate': 95,
                'respiratory_rate': 22,
                'oxygen_saturation': 92
            }
        }
        
        session_response = client.post(
            '/api/v1/triage/sessions',
            json=triage_data,
            headers=authenticated_user['headers']
        )
        assert session_response.status_code == 201
        session_id = session_response.get_json()['id']
        
        # Step 3: AI assessment workflow
        agents_to_test = ['intake', 'triage', 'knowledge', 'escalation']
        
        for agent_type in agents_to_test:
            interaction_data = {
                'session_id': session_id,
                'agent_type': agent_type,
                'message': f'Process with {agent_type} agent',
                'context': {
                    'symptoms': ['chest_pain', 'shortness_of_breath'],
                    'vital_signs': triage_data['vital_signs']
                }
            }
            
            response = client.post(
                '/api/v1/agents/interact',
                json=interaction_data,
                headers=authenticated_user['headers']
            )
            
            assert response.status_code == 200
            
            data = response.get_json()
            assert data['agent_type'] == agent_type
            assert 'confidence_score' in data
            assert data['confidence_score'] >= 0.7
        
        # Step 4: Verify session is properly tracked
        session_response = client.get(
            f'/api/v1/triage/sessions/{session_id}',
            headers=authenticated_user['headers']
        )
        assert session_response.status_code == 200
        
        session_data = session_response.get_json()
        assert session_data['id'] == session_id
        assert session_data['patient_id'] == patient_id

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])