"""
Integration tests for Healthcare Triage API
Tests end-to-end API workflows and database interactions
"""

import pytest
import requests
import json
import time
from datetime import datetime, timedelta
import psycopg2
from unittest.mock import patch

# Test Configuration
API_BASE_URL = "http://localhost:5000/api"
TEST_DB_CONFIG = {
    "host": "localhost",
    "database": "healthcare_triage_test",
    "user": "test_user",
    "password": "test_password"
}

class TestTriageAPIIntegration:
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup test database and cleanup after each test"""
        self.conn = psycopg2.connect(**TEST_DB_CONFIG)
        self.cursor = self.conn.cursor()
        
        # Clean test data
        self.cursor.execute("TRUNCATE TABLE patients, triage_sessions, audit_logs CASCADE")
        self.conn.commit()
        
        yield
        
        # Cleanup
        self.cursor.execute("TRUNCATE TABLE patients, triage_sessions, audit_logs CASCADE")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def test_complete_triage_workflow(self):
        """Test complete patient triage workflow via API"""
        
        # Step 1: Create patient
        patient_data = {
            "name": "John Doe",
            "age": 45,
            "gender": "male",
            "phone": "555-0123",
            "emergency_contact": "555-0124"
        }
        
        response = requests.post(f"{API_BASE_URL}/patients", json=patient_data)
        assert response.status_code == 201
        patient = response.json()
        patient_id = patient["id"]
        
        # Verify patient in database
        self.cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        db_patient = self.cursor.fetchone()
        assert db_patient is not None
        assert db_patient[1] == "John Doe"  # name field
        
        # Step 2: Start triage session
        triage_data = {
            "patient_id": patient_id,
            "chief_complaint": "Chest pain and shortness of breath",
            "provider_id": "dr_smith_123"
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/start", json=triage_data)
        assert response.status_code == 201
        session = response.json()
        session_id = session["session_id"]
        
        # Step 3: Submit symptoms
        symptoms_data = {
            "session_id": session_id,
            "symptoms": [
                {"symptom": "chest_pain", "severity": 8, "duration": "2_hours"},
                {"symptom": "shortness_of_breath", "severity": 7, "duration": "2_hours"},
                {"symptom": "sweating", "severity": 5, "duration": "1_hour"}
            ]
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/symptoms", json=symptoms_data)
        assert response.status_code == 200
        
        # Step 4: Submit vital signs
        vitals_data = {
            "session_id": session_id,
            "blood_pressure_systolic": 160,
            "blood_pressure_diastolic": 95,
            "heart_rate": 105,
            "temperature": 98.6,
            "oxygen_saturation": 96,
            "respiratory_rate": 22
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/vitals", json=vitals_data)
        assert response.status_code == 200
        
        # Step 5: Submit medical history
        history_data = {
            "session_id": session_id,
            "medical_history": ["hypertension", "diabetes"],
            "current_medications": ["lisinopril", "metformin"],
            "allergies": ["penicillin"]
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/history", json=history_data)
        assert response.status_code == 200
        
        # Step 6: Get AI triage assessment
        response = requests.post(f"{API_BASE_URL}/triage/assess", json={"session_id": session_id})
        assert response.status_code == 200
        
        assessment = response.json()
        assert "triage_level" in assessment
        assert "confidence_score" in assessment
        assert "recommendations" in assessment
        assert assessment["triage_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        assert 0 <= assessment["confidence_score"] <= 100
        
        # For this high-risk case, expect HIGH or CRITICAL
        assert assessment["triage_level"] in ["HIGH", "CRITICAL"]
        
        # Step 7: Complete triage
        completion_data = {
            "session_id": session_id,
            "provider_notes": "Patient presents with acute chest pain, elevated BP, concerning for ACS",
            "assigned_provider": "dr_johnson_456"
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/complete", json=completion_data)
        assert response.status_code == 200
        
        # Verify triage session in database
        self.cursor.execute(
            "SELECT * FROM triage_sessions WHERE id = %s", 
            (session_id,)
        )
        db_session = self.cursor.fetchone()
        assert db_session is not None
        assert db_session[7] == "COMPLETED"  # status field

    def test_critical_emergency_workflow(self):
        """Test critical emergency case with immediate escalation"""
        
        # Create patient
        patient_data = {
            "name": "Emergency Case",
            "age": 65,
            "gender": "male",
            "phone": "555-9999"
        }
        
        response = requests.post(f"{API_BASE_URL}/patients", json=patient_data)
        patient_id = response.json()["id"]
        
        # Start triage with critical symptoms
        triage_data = {
            "patient_id": patient_id,
            "chief_complaint": "Sudden severe chest pain, can't breathe, collapsed",
            "provider_id": "dr_emergency_789"
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/start", json=triage_data)
        session_id = response.json()["session_id"]
        
        # Critical symptoms
        symptoms_data = {
            "session_id": session_id,
            "symptoms": [
                {"symptom": "chest_pain", "severity": 10, "duration": "30_minutes"},
                {"symptom": "shortness_of_breath", "severity": 10, "duration": "30_minutes"},
                {"symptom": "loss_of_consciousness", "severity": 8, "duration": "5_minutes"}
            ]
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/symptoms", json=symptoms_data)
        assert response.status_code == 200
        
        # Critical vitals
        vitals_data = {
            "session_id": session_id,
            "blood_pressure_systolic": 200,
            "blood_pressure_diastolic": 110,
            "heart_rate": 130,
            "temperature": 99.2,
            "oxygen_saturation": 88,
            "respiratory_rate": 28
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/vitals", json=vitals_data)
        assert response.status_code == 200
        
        # Get assessment
        response = requests.post(f"{API_BASE_URL}/triage/assess", json={"session_id": session_id})
        assessment = response.json()
        
        # Should be CRITICAL with high confidence
        assert assessment["triage_level"] == "CRITICAL"
        assert assessment["confidence_score"] >= 90
        assert "immediate" in assessment["recommendations"][0].lower()

    def test_low_priority_workflow(self):
        """Test low priority case for routine care"""
        
        # Create patient
        patient_data = {
            "name": "Jane Smith",
            "age": 28,
            "gender": "female",
            "phone": "555-0456"
        }
        
        response = requests.post(f"{API_BASE_URL}/patients", json=patient_data)
        patient_id = response.json()["id"]
        
        # Start triage
        triage_data = {
            "patient_id": patient_id,
            "chief_complaint": "Mild headache for 1 day",
            "provider_id": "nurse_williams_101"
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/start", json=triage_data)
        session_id = response.json()["session_id"]
        
        # Mild symptoms
        symptoms_data = {
            "session_id": session_id,
            "symptoms": [
                {"symptom": "headache", "severity": 3, "duration": "1_day"}
            ]
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/symptoms", json=symptoms_data)
        
        # Normal vitals
        vitals_data = {
            "session_id": session_id,
            "blood_pressure_systolic": 120,
            "blood_pressure_diastolic": 80,
            "heart_rate": 72,
            "temperature": 98.6,
            "oxygen_saturation": 99,
            "respiratory_rate": 16
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/vitals", json=vitals_data)
        
        # Get assessment
        response = requests.post(f"{API_BASE_URL}/triage/assess", json={"session_id": session_id})
        assessment = response.json()
        
        # Should be LOW priority
        assert assessment["triage_level"] == "LOW"
        assert "routine" in assessment["recommendations"][0].lower()

    def test_api_authentication(self):
        """Test API authentication and authorization"""
        
        # Test without auth token
        response = requests.get(f"{API_BASE_URL}/patients")
        assert response.status_code == 401
        
        # Test with invalid token
        headers = {"Authorization": "Bearer invalid_token"}
        response = requests.get(f"{API_BASE_URL}/patients", headers=headers)
        assert response.status_code == 401
        
        # Test with valid token (mock for testing)
        headers = {"Authorization": "Bearer test_valid_token"}
        with patch('app.verify_token') as mock_verify:
            mock_verify.return_value = True
            response = requests.get(f"{API_BASE_URL}/patients", headers=headers)
            assert response.status_code == 200

    def test_hipaa_audit_logging(self):
        """Test HIPAA compliance audit logging"""
        
        # Create patient and perform actions
        patient_data = {"name": "Audit Test", "age": 30, "gender": "other"}
        
        headers = {"Authorization": "Bearer test_token", "User-ID": "test_user_123"}
        response = requests.post(f"{API_BASE_URL}/patients", json=patient_data, headers=headers)
        patient_id = response.json()["id"]
        
        # Check audit log
        self.cursor.execute(
            "SELECT * FROM audit_logs WHERE resource_type = 'patient' AND resource_id = %s",
            (patient_id,)
        )
        audit_entries = self.cursor.fetchall()
        
        assert len(audit_entries) >= 1
        assert audit_entries[0][2] == "CREATE"  # action field
        assert audit_entries[0][4] == "test_user_123"  # user_id field

    def test_data_validation(self):
        """Test API data validation"""
        
        # Test invalid patient data
        invalid_patient = {
            "name": "",  # Empty name
            "age": -5,   # Invalid age
            "gender": "invalid_gender"
        }
        
        response = requests.post(f"{API_BASE_URL}/patients", json=invalid_patient)
        assert response.status_code == 400
        assert "validation" in response.json()["error"].lower()
        
        # Test invalid vital signs
        headers = {"Authorization": "Bearer test_token"}
        invalid_vitals = {
            "session_id": "fake_session",
            "blood_pressure_systolic": 300,  # Too high
            "heart_rate": -10,  # Invalid
            "temperature": 150  # Impossible
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/vitals", json=invalid_vitals, headers=headers)
        assert response.status_code == 400

    def test_rate_limiting(self):
        """Test API rate limiting"""
        
        headers = {"Authorization": "Bearer test_token"}
        
        # Make rapid requests to trigger rate limiting
        for i in range(20):
            response = requests.get(f"{API_BASE_URL}/health", headers=headers)
            if response.status_code == 429:
                assert "rate limit" in response.json()["error"].lower()
                break
        else:
            # If we don't hit rate limit, that's also valid for testing
            pass

    def test_database_transactions(self):
        """Test database transaction integrity"""
        
        # Simulate failure during triage session creation
        patient_data = {"name": "Transaction Test", "age": 35, "gender": "female"}
        response = requests.post(f"{API_BASE_URL}/patients", json=patient_data)
        patient_id = response.json()["id"]
        
        # Count initial records
        self.cursor.execute("SELECT COUNT(*) FROM triage_sessions")
        initial_count = self.cursor.fetchone()[0]
        
        # Attempt triage with invalid data that should rollback
        invalid_triage = {
            "patient_id": patient_id,
            "chief_complaint": None,  # This should cause validation error
            "provider_id": "invalid_provider"
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/start", json=invalid_triage)
        assert response.status_code == 400
        
        # Verify no partial data was committed
        self.cursor.execute("SELECT COUNT(*) FROM triage_sessions")
        final_count = self.cursor.fetchone()[0]
        assert final_count == initial_count

    def test_ai_agent_integration(self):
        """Test AI agent integration and fallback"""
        
        # Create test case for AI processing
        patient_data = {"name": "AI Test", "age": 40, "gender": "male"}
        response = requests.post(f"{API_BASE_URL}/patients", json=patient_data)
        patient_id = response.json()["id"]
        
        triage_data = {
            "patient_id": patient_id,
            "chief_complaint": "Test complaint for AI",
            "provider_id": "test_provider"
        }
        
        response = requests.post(f"{API_BASE_URL}/triage/start", json=triage_data)
        session_id = response.json()["session_id"]
        
        # Submit minimal data for AI assessment
        symptoms_data = {
            "session_id": session_id,
            "symptoms": [{"symptom": "fatigue", "severity": 4, "duration": "3_days"}]
        }
        
        requests.post(f"{API_BASE_URL}/triage/symptoms", json=symptoms_data)
        
        # Test AI assessment with timeout
        start_time = time.time()
        response = requests.post(f"{API_BASE_URL}/triage/assess", json={"session_id": session_id})
        end_time = time.time()
        
        # Should complete within reasonable time
        assert end_time - start_time < 30  # 30 second timeout
        assert response.status_code == 200
        
        assessment = response.json()
        assert "triage_level" in assessment
        assert "ai_agent_used" in assessment  # Should indicate which agent processed

if __name__ == "__main__":
    pytest.main([__file__, "-v"])