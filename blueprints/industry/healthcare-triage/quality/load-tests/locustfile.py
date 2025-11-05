"""
Load testing for Healthcare Triage System
Tests system performance under various load conditions
"""

from locust import HttpUser, task, between
import random
import json
from datetime import datetime

class TriageSystemUser(HttpUser):
    wait_time = between(1, 5)  # Wait 1-5 seconds between requests
    
    def on_start(self):
        """Setup for each user session"""
        self.patient_id = None
        self.session_id = None
        self.auth_token = "test_load_token"  # In real testing, implement proper auth
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }

    @task(3)
    def create_patient(self):
        """Create a new patient (high frequency task)"""
        patient_data = {
            "name": f"Patient_{random.randint(1000, 9999)}",
            "age": random.randint(18, 90),
            "gender": random.choice(["male", "female", "other"]),
            "phone": f"555-{random.randint(1000, 9999)}",
            "emergency_contact": f"555-{random.randint(1000, 9999)}"
        }
        
        with self.client.post("/api/patients", 
                             json=patient_data, 
                             headers=self.headers,
                             catch_response=True) as response:
            if response.status_code == 201:
                self.patient_id = response.json()["id"]
                response.success()
            else:
                response.failure(f"Failed to create patient: {response.status_code}")

    @task(5)
    def complete_triage_workflow(self):
        """Complete full triage workflow (most common scenario)"""
        if not self.patient_id:
            self.create_patient()
        
        # Step 1: Start triage session
        triage_data = {
            "patient_id": self.patient_id,
            "chief_complaint": random.choice([
                "Chest pain and shortness of breath",
                "Abdominal pain",
                "Headache and nausea", 
                "Fever and cough",
                "Back pain",
                "Ankle injury"
            ]),
            "provider_id": f"provider_{random.randint(100, 999)}"
        }
        
        with self.client.post("/api/triage/start",
                             json=triage_data,
                             headers=self.headers,
                             catch_response=True) as response:
            if response.status_code == 201:
                self.session_id = response.json()["session_id"]
                response.success()
            else:
                response.failure(f"Failed to start triage: {response.status_code}")
                return
        
        # Step 2: Submit symptoms
        symptoms = self._generate_random_symptoms()
        symptoms_data = {
            "session_id": self.session_id,
            "symptoms": symptoms
        }
        
        with self.client.post("/api/triage/symptoms",
                             json=symptoms_data,
                             headers=self.headers,
                             catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to submit symptoms: {response.status_code}")
                return
        
        # Step 3: Submit vital signs
        vitals_data = {
            "session_id": self.session_id,
            "blood_pressure_systolic": random.randint(90, 180),
            "blood_pressure_diastolic": random.randint(60, 110),
            "heart_rate": random.randint(60, 120),
            "temperature": round(random.uniform(97.0, 102.0), 1),
            "oxygen_saturation": random.randint(90, 100),
            "respiratory_rate": random.randint(12, 25)
        }
        
        with self.client.post("/api/triage/vitals",
                             json=vitals_data,
                             headers=self.headers,
                             catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to submit vitals: {response.status_code}")
                return
        
        # Step 4: Submit medical history
        history_data = {
            "session_id": self.session_id,
            "medical_history": random.sample([
                "hypertension", "diabetes", "asthma", "heart_disease", 
                "cancer", "mental_health", "pregnancy"
            ], random.randint(0, 3)),
            "current_medications": random.sample([
                "lisinopril", "metformin", "aspirin", "ibuprofen",
                "prednisone", "insulin", "albuterol"
            ], random.randint(0, 4)),
            "allergies": random.sample([
                "penicillin", "latex", "shellfish", "peanuts", "sulfa"
            ], random.randint(0, 2))
        }
        
        with self.client.post("/api/triage/history",
                             json=history_data,
                             headers=self.headers,
                             catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to submit history: {response.status_code}")
                return
        
        # Step 5: Get AI assessment (performance critical)
        assess_start = datetime.now()
        with self.client.post("/api/triage/assess",
                             json={"session_id": self.session_id},
                             headers=self.headers,
                             catch_response=True) as response:
            assess_time = (datetime.now() - assess_start).total_seconds()
            
            if response.status_code == 200:
                if assess_time > 10:  # Fail if assessment takes > 10 seconds
                    response.failure(f"AI assessment too slow: {assess_time}s")
                else:
                    response.success()
            else:
                response.failure(f"Failed AI assessment: {response.status_code}")
                return
        
        # Step 6: Complete triage
        completion_data = {
            "session_id": self.session_id,
            "provider_notes": f"Load test triage completed at {datetime.now()}",
            "assigned_provider": f"provider_{random.randint(100, 999)}"
        }
        
        with self.client.post("/api/triage/complete",
                             json=completion_data,
                             headers=self.headers,
                             catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to complete triage: {response.status_code}")

    @task(1)
    def emergency_triage_workflow(self):
        """High-priority emergency workflow"""
        if not self.patient_id:
            self.create_patient()
        
        # Critical case with minimal data collection
        triage_data = {
            "patient_id": self.patient_id,
            "chief_complaint": "EMERGENCY: " + random.choice([
                "Severe chest pain, difficulty breathing",
                "Major trauma, loss of consciousness", 
                "Severe allergic reaction",
                "Stroke symptoms",
                "Cardiac arrest"
            ]),
            "provider_id": f"emergency_provider_{random.randint(100, 999)}",
            "priority": "EMERGENCY"
        }
        
        with self.client.post("/api/triage/start",
                             json=triage_data,
                             headers=self.headers,
                             catch_response=True) as response:
            if response.status_code == 201:
                session_id = response.json()["session_id"]
                
                # Critical vitals only
                vitals_data = {
                    "session_id": session_id,
                    "blood_pressure_systolic": random.randint(180, 220),
                    "blood_pressure_diastolic": random.randint(100, 130),
                    "heart_rate": random.randint(120, 160),
                    "oxygen_saturation": random.randint(80, 90)
                }
                
                self.client.post("/api/triage/vitals", json=vitals_data, headers=self.headers)
                
                # Emergency assessment should be very fast
                assess_start = datetime.now()
                with self.client.post("/api/triage/assess",
                                     json={"session_id": session_id, "priority": "EMERGENCY"},
                                     headers=self.headers,
                                     catch_response=True) as assess_response:
                    assess_time = (datetime.now() - assess_start).total_seconds()
                    
                    if assess_response.status_code == 200 and assess_time < 5:
                        assess_response.success()
                    else:
                        assess_response.failure(f"Emergency assessment failed or too slow: {assess_time}s")

    @task(2)
    def provider_dashboard_access(self):
        """Provider accessing dashboard and patient queue"""
        with self.client.get("/api/provider/dashboard",
                            headers=self.headers,
                            catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Dashboard access failed: {response.status_code}")
        
        # Get patient queue
        with self.client.get("/api/provider/queue",
                            headers=self.headers,
                            catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Queue access failed: {response.status_code}")

    @task(1)
    def admin_analytics_access(self):
        """Admin accessing analytics and reports"""
        with self.client.get("/api/admin/analytics",
                            headers=self.headers,
                            catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Analytics access failed: {response.status_code}")

    @task(1)
    def health_check(self):
        """System health check"""
        with self.client.get("/api/health",
                            catch_response=True) as response:
            if response.status_code == 200:
                health_data = response.json()
                if health_data.get("status") == "healthy":
                    response.success()
                else:
                    response.failure("System reported unhealthy")
            else:
                response.failure(f"Health check failed: {response.status_code}")

    def _generate_random_symptoms(self):
        """Generate realistic random symptoms for load testing"""
        symptom_types = [
            "chest_pain", "shortness_of_breath", "abdominal_pain",
            "headache", "nausea", "fever", "cough", "fatigue",
            "dizziness", "back_pain", "joint_pain", "rash"
        ]
        
        num_symptoms = random.randint(1, 4)
        selected_symptoms = random.sample(symptom_types, num_symptoms)
        
        symptoms = []
        for symptom in selected_symptoms:
            symptoms.append({
                "symptom": symptom,
                "severity": random.randint(1, 10),
                "duration": random.choice([
                    "30_minutes", "1_hour", "2_hours", "4_hours",
                    "1_day", "2_days", "1_week", "1_month"
                ])
            })
        
        return symptoms


class EmergencyRoomStressTest(HttpUser):
    """Stress test simulating emergency room peak load"""
    wait_time = between(0.1, 0.5)  # Very rapid requests
    
    def on_start(self):
        self.auth_token = "stress_test_token"
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }

    @task
    def rapid_patient_creation(self):
        """Rapidly create patients to test throughput"""
        patient_data = {
            "name": f"Stress_{random.randint(10000, 99999)}",
            "age": random.randint(18, 90),
            "gender": random.choice(["male", "female"]),
            "phone": f"555-{random.randint(1000, 9999)}"
        }
        
        self.client.post("/api/patients", json=patient_data, headers=self.headers)

    @task
    def concurrent_assessments(self):
        """Test concurrent AI assessments"""
        session_data = {
            "session_id": f"stress_session_{random.randint(1000, 9999)}",
            "mock_data": True  # Flag for load testing
        }
        
        self.client.post("/api/triage/assess", json=session_data, headers=self.headers)


class DatabaseStressTest(HttpUser):
    """Test database performance under load"""
    wait_time = between(0.1, 1)
    
    def on_start(self):
        self.headers = {"Authorization": "Bearer db_stress_token"}

    @task
    def database_read_operations(self):
        """Test database read performance"""
        # Search patients
        self.client.get(f"/api/patients/search?q=test_{random.randint(1, 100)}", 
                       headers=self.headers)
        
        # Get triage history
        self.client.get(f"/api/triage/history?limit=50&offset={random.randint(0, 500)}", 
                       headers=self.headers)

    @task
    def database_write_operations(self):
        """Test database write performance"""
        # Create audit log entry
        audit_data = {
            "action": "READ",
            "resource_type": "patient",
            "resource_id": random.randint(1, 1000),
            "user_id": f"load_user_{random.randint(1, 100)}"
        }
        
        self.client.post("/api/audit", json=audit_data, headers=self.headers)

# Custom load test scenarios
class LoadTestScenarios:
    """Pre-configured load test scenarios for different situations"""
    
    NORMAL_OPERATIONS = {
        "users": 50,
        "spawn_rate": 5,
        "duration": "10m"
    }
    
    PEAK_HOURS = {
        "users": 200,
        "spawn_rate": 20,
        "duration": "30m"
    }
    
    EMERGENCY_SURGE = {
        "users": 500,
        "spawn_rate": 50,
        "duration": "15m"
    }
    
    STRESS_LIMIT = {
        "users": 1000,
        "spawn_rate": 100,
        "duration": "5m"
    }

if __name__ == "__main__":
    import os
    print("Healthcare Triage Load Test")
    print("Available scenarios:")
    for name, config in LoadTestScenarios.__dict__.items():
        if not name.startswith('_'):
            print(f"  {name}: {config}")
    print("\nRun with: locust -f locustfile.py --host=http://localhost:5000")