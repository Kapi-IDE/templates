# Healthcare Triage System - API Documentation

## Table of Contents
1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [Patient Management](#patient-management)
4. [Triage Operations](#triage-operations)
5. [Provider Management](#provider-management)
6. [Administrative Functions](#administrative-functions)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)

---

## API Overview

### Base URL
```
Production: https://api.healthcare-triage.com/v1
Staging: https://staging-api.healthcare-triage.com/v1
Development: http://localhost:5000/api
```

### Request/Response Format
- **Content-Type**: `application/json`
- **Character Encoding**: UTF-8
- **Date Format**: ISO 8601 (`YYYY-MM-DDTHH:mm:ssZ`)

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Rate Limited
- `500` - Internal Server Error

---

## Authentication

### JWT Token Authentication

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "user@hospital.com",
  "password": "secure_password",
  "mfa_token": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4...",
  "expires_in": 3600,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "user@hospital.com",
    "role": "nurse",
    "permissions": ["patient.read", "triage.create"]
  }
}
```

#### Token Refresh
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..."
}
```

#### Logout
```http
POST /auth/logout
Authorization: Bearer {access_token}
```

### API Key Authentication (for integrations)
```http
GET /api/patients
X-API-Key: your-api-key-here
```

---

## Patient Management

### Create Patient
```http
POST /patients
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "John Doe",
  "age": 45,
  "gender": "male",
  "phone": "555-123-4567",
  "email": "john.doe@email.com",
  "emergency_contact": "555-987-6543",
  "insurance_id": "INS123456789",
  "allergies": ["penicillin", "shellfish"]
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "John Doe",
  "age": 45,
  "gender": "male",
  "phone": "***-***-4567",
  "created_at": "2024-01-15T10:30:00Z",
  "status": "active"
}
```

### Get Patient
```http
GET /patients/{patient_id}
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "John Doe",
  "age": 45,
  "gender": "male",
  "phone": "***-***-4567",
  "emergency_contact": "***-***-6543",
  "medical_history": [
    {
      "condition": "hypertension",
      "diagnosed_date": "2020-03-15",
      "status": "active"
    }
  ],
  "allergies": ["penicillin", "shellfish"],
  "created_at": "2024-01-15T10:30:00Z",
  "last_visit": "2024-01-15T10:30:00Z"
}
```

### Update Patient
```http
PUT /patients/{patient_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "phone": "555-123-4567",
  "emergency_contact": "555-987-6543"
}
```

### Search Patients
```http
GET /patients/search?q=john&limit=10&offset=0
Authorization: Bearer {token}
```

**Query Parameters:**
- `q` - Search query (name, phone, ID)
- `limit` - Number of results (max 100)
- `offset` - Pagination offset
- `gender` - Filter by gender
- `age_min` - Minimum age
- `age_max` - Maximum age

---

## Triage Operations

### Start Triage Session
```http
POST /triage/start
Authorization: Bearer {token}
Content-Type: application/json

{
  "patient_id": "550e8400-e29b-41d4-a716-446655440001",
  "chief_complaint": "Chest pain and shortness of breath",
  "provider_id": "dr_smith_123",
  "priority": "normal"
}
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440002",
  "patient_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "in_progress",
  "created_at": "2024-01-15T10:35:00Z",
  "estimated_completion": "2024-01-15T11:05:00Z"
}
```

### Submit Symptoms
```http
POST /triage/symptoms
Authorization: Bearer {token}
Content-Type: application/json

{
  "session_id": "550e8400-e29b-41d4-a716-446655440002",
  "symptoms": [
    {
      "symptom": "chest_pain",
      "severity": 8,
      "duration": "2_hours",
      "location": "center",
      "character": "sharp"
    },
    {
      "symptom": "shortness_of_breath",
      "severity": 7,
      "duration": "2_hours",
      "triggers": ["exertion"]
    }
  ]
}
```

### Submit Vital Signs
```http
POST /triage/vitals
Authorization: Bearer {token}
Content-Type: application/json

{
  "session_id": "550e8400-e29b-41d4-a716-446655440002",
  "blood_pressure_systolic": 160,
  "blood_pressure_diastolic": 95,
  "heart_rate": 105,
  "temperature": 98.6,
  "temperature_unit": "fahrenheit",
  "oxygen_saturation": 96,
  "respiratory_rate": 22,
  "pain_scale": 8,
  "measured_at": "2024-01-15T10:40:00Z"
}
```

### Submit Medical History
```http
POST /triage/history
Authorization: Bearer {token}
Content-Type: application/json

{
  "session_id": "550e8400-e29b-41d4-a716-446655440002",
  "medical_history": ["hypertension", "diabetes"],
  "current_medications": [
    {
      "name": "lisinopril",
      "dosage": "10mg",
      "frequency": "daily"
    },
    {
      "name": "metformin",
      "dosage": "500mg",
      "frequency": "twice_daily"
    }
  ],
  "allergies": ["penicillin"],
  "surgical_history": [],
  "family_history": ["heart_disease", "diabetes"]
}
```

### Get AI Assessment
```http
POST /triage/assess
Authorization: Bearer {token}
Content-Type: application/json

{
  "session_id": "550e8400-e29b-41d4-a716-446655440002"
}
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440002",
  "triage_level": "HIGH",
  "confidence_score": 92,
  "risk_factors": [
    "elevated_blood_pressure",
    "chest_pain_with_exertion",
    "diabetes_history"
  ],
  "recommendations": [
    "Immediate medical evaluation required",
    "Consider cardiac monitoring",
    "Obtain 12-lead EKG",
    "Check cardiac biomarkers"
  ],
  "differential_diagnosis": [
    {
      "condition": "acute_coronary_syndrome",
      "probability": 0.75,
      "reasoning": "Chest pain with cardiovascular risk factors"
    },
    {
      "condition": "hypertensive_emergency",
      "probability": 0.15,
      "reasoning": "Significantly elevated blood pressure"
    }
  ],
  "ai_agent_used": "diagnostic_specialist",
  "processing_time_ms": 1250,
  "assessed_at": "2024-01-15T10:45:00Z"
}
```

### Complete Triage
```http
POST /triage/complete
Authorization: Bearer {token}
Content-Type: application/json

{
  "session_id": "550e8400-e29b-41d4-a716-446655440002",
  "provider_notes": "Patient presents with acute chest pain, elevated BP, concerning for ACS",
  "assigned_provider": "dr_johnson_456",
  "disposition": "admit",
  "follow_up_instructions": "Cardiology consultation, serial cardiac enzymes"
}
```

### Get Triage Session
```http
GET /triage/sessions/{session_id}
Authorization: Bearer {token}
```

### List Triage Sessions
```http
GET /triage/sessions?status=in_progress&limit=20&offset=0
Authorization: Bearer {token}
```

**Query Parameters:**
- `status` - Filter by status (in_progress, completed, cancelled)
- `provider_id` - Filter by provider
- `triage_level` - Filter by triage level
- `date_from` - Start date filter
- `date_to` - End date filter
- `limit` - Number of results
- `offset` - Pagination offset

---

## Provider Management

### Get Provider Dashboard
```http
GET /provider/dashboard
Authorization: Bearer {token}
```

**Response:**
```json
{
  "provider_id": "dr_smith_123",
  "active_patients": 5,
  "pending_assignments": 3,
  "completed_today": 12,
  "queue": [
    {
      "session_id": "550e8400-e29b-41d4-a716-446655440002",
      "patient_name": "John Doe",
      "triage_level": "HIGH",
      "wait_time_minutes": 15,
      "chief_complaint": "Chest pain"
    }
  ],
  "performance_metrics": {
    "average_time_per_patient": 25,
    "patient_satisfaction": 4.7
  }
}
```

### Get Patient Queue
```http
GET /provider/queue?triage_level=HIGH&limit=10
Authorization: Bearer {token}
```

### Accept Patient Assignment
```http
POST /provider/assignments
Authorization: Bearer {token}
Content-Type: application/json

{
  "session_id": "550e8400-e29b-41d4-a716-446655440002",
  "estimated_duration": 30
}
```

### Update Patient Status
```http
PUT /provider/patients/{session_id}/status
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "in_treatment",
  "notes": "Patient stabilized, continuing evaluation"
}
```

---

## Administrative Functions

### User Management

#### Create User
```http
POST /admin/users
Authorization: Bearer {token}
Content-Type: application/json

{
  "username": "new.user@hospital.com",
  "password": "temporary_password_123",
  "role": "nurse",
  "first_name": "Jane",
  "last_name": "Smith",
  "department": "Emergency",
  "license_number": "RN123456"
}
```

#### Update User Permissions
```http
PUT /admin/users/{user_id}/permissions
Authorization: Bearer {token}
Content-Type: application/json

{
  "permissions": ["patient.read", "triage.create", "triage.update"]
}
```

#### Deactivate User
```http
DELETE /admin/users/{user_id}
Authorization: Bearer {token}
```

### System Analytics

#### Get System Metrics
```http
GET /admin/metrics?period=24h
Authorization: Bearer {token}
```

**Response:**
```json
{
  "period": "24h",
  "total_patients": 145,
  "total_triages": 132,
  "average_wait_time": 23.5,
  "triage_distribution": {
    "CRITICAL": 5,
    "HIGH": 25,
    "MEDIUM": 67,
    "LOW": 35
  },
  "ai_performance": {
    "accuracy_rate": 0.94,
    "average_processing_time": 1.2
  },
  "user_activity": {
    "active_users": 42,
    "total_sessions": 156
  }
}
```

#### Get Audit Logs
```http
GET /admin/audit?user_id={user_id}&start_date=2024-01-01&end_date=2024-01-15
Authorization: Bearer {token}
```

### System Configuration

#### Get Configuration
```http
GET /admin/config
Authorization: Bearer {token}
```

#### Update Configuration
```http
PUT /admin/config
Authorization: Bearer {token}
Content-Type: application/json

{
  "ai_settings": {
    "confidence_threshold": 0.85,
    "auto_assign_low_priority": true
  },
  "alert_settings": {
    "critical_patient_notification": true,
    "system_health_alerts": true
  }
}
```

### Reports

#### Generate Report
```http
POST /admin/reports
Authorization: Bearer {token}
Content-Type: application/json

{
  "report_type": "compliance",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "format": "pdf",
  "include_phi": false
}
```

**Response:**
```json
{
  "report_id": "report_550e8400_20240115",
  "status": "generating",
  "estimated_completion": "2024-01-15T11:00:00Z",
  "download_url": null
}
```

#### Get Report Status
```http
GET /admin/reports/{report_id}
Authorization: Bearer {token}
```

---

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "age",
      "issue": "Age must be between 0 and 150"
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_550e8400_123"
  }
}
```

### Common Error Codes

#### Authentication Errors
- `INVALID_CREDENTIALS` - Username or password incorrect
- `TOKEN_EXPIRED` - Access token has expired
- `TOKEN_INVALID` - Access token is malformed or invalid
- `MFA_REQUIRED` - Multi-factor authentication required
- `INSUFFICIENT_PERMISSIONS` - User lacks required permissions

#### Validation Errors
- `VALIDATION_ERROR` - Request data validation failed
- `MISSING_REQUIRED_FIELD` - Required field not provided
- `INVALID_FORMAT` - Field format is incorrect
- `VALUE_OUT_OF_RANGE` - Numeric value outside acceptable range

#### Business Logic Errors
- `PATIENT_NOT_FOUND` - Patient ID does not exist
- `SESSION_NOT_FOUND` - Triage session ID does not exist
- `SESSION_ALREADY_COMPLETED` - Cannot modify completed session
- `PROVIDER_UNAVAILABLE` - Assigned provider is not available

#### System Errors
- `AI_SERVICE_UNAVAILABLE` - AI assessment service is down
- `DATABASE_ERROR` - Database connection or query error
- `RATE_LIMIT_EXCEEDED` - API rate limit exceeded
- `MAINTENANCE_MODE` - System is in maintenance mode

---

## Rate Limiting

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642248600
```

### Rate Limits by Endpoint

| Endpoint Category | Limit | Window |
|------------------|-------|---------|
| Authentication | 10 requests | 1 minute |
| Patient Operations | 100 requests | 1 minute |
| Triage Operations | 50 requests | 1 minute |
| AI Assessments | 20 requests | 1 minute |
| Administrative | 200 requests | 1 minute |

### Rate Limit Exceeded Response
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API rate limit exceeded",
    "details": {
      "limit": 100,
      "window": "1 minute",
      "retry_after": 45
    }
  }
}
```

---

## Webhooks

### Webhook Events

#### Patient Events
- `patient.created` - New patient registered
- `patient.updated` - Patient information modified

#### Triage Events
- `triage.started` - New triage session begun
- `triage.completed` - Triage session finished
- `triage.critical` - Critical patient identified

#### System Events
- `system.alert` - System alert generated
- `system.maintenance` - Maintenance mode activated

### Webhook Payload Example
```json
{
  "event": "triage.critical",
  "timestamp": "2024-01-15T10:45:00Z",
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440002",
    "patient_id": "550e8400-e29b-41d4-a716-446655440001",
    "triage_level": "CRITICAL",
    "confidence_score": 95,
    "chief_complaint": "Severe chest pain"
  },
  "signature": "sha256=5d41402abc4b2a76b9719d911017c592"
}
```

### Webhook Configuration
```http
POST /admin/webhooks
Authorization: Bearer {token}
Content-Type: application/json

{
  "url": "https://your-system.com/webhooks/triage",
  "events": ["triage.critical", "triage.completed"],
  "secret": "your-webhook-secret"
}
```

---

## SDK Examples

### Python SDK
```python
from healthcare_triage import TriageClient

client = TriageClient(
    api_url="https://api.healthcare-triage.com/v1",
    api_key="your-api-key"
)

# Create patient
patient = client.patients.create({
    "name": "John Doe",
    "age": 45,
    "gender": "male"
})

# Start triage
session = client.triage.start({
    "patient_id": patient.id,
    "chief_complaint": "Chest pain"
})

# Get AI assessment
assessment = client.triage.assess(session.id)
print(f"Triage Level: {assessment.triage_level}")
```

### JavaScript SDK
```javascript
import { TriageClient } from '@healthcare-triage/sdk';

const client = new TriageClient({
  apiUrl: 'https://api.healthcare-triage.com/v1',
  apiKey: 'your-api-key'
});

// Create patient
const patient = await client.patients.create({
  name: 'John Doe',
  age: 45,
  gender: 'male'
});

// Start triage
const session = await client.triage.start({
  patientId: patient.id,
  chiefComplaint: 'Chest pain'
});

// Get AI assessment
const assessment = await client.triage.assess(session.id);
console.log(`Triage Level: ${assessment.triageLevel}`);
```

---

For additional API support, contact the development team at api-support@hospital.com or refer to the interactive API documentation at https://api.healthcare-triage.com/docs.