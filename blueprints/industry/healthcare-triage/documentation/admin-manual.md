# Healthcare Triage System - Administrator Manual

## Table of Contents
1. [System Administration](#system-administration)
2. [User Management](#user-management)
3. [Security Administration](#security-administration)
4. [Database Management](#database-management)
5. [System Monitoring](#system-monitoring)
6. [Backup and Recovery](#backup-and-recovery)
7. [Compliance Management](#compliance-management)
8. [Integration Management](#integration-management)

---

## System Administration

### System Architecture Overview
The Healthcare Triage System consists of:
- **Frontend**: React-based web application
- **Backend**: Flask API server with Redis caching
- **Database**: PostgreSQL with encrypted PHI storage
- **AI Engine**: Multi-agent orchestration system
- **Security**: Multi-layer authentication and authorization
- **Monitoring**: Prometheus metrics with Grafana dashboards

### Environment Configuration

#### Production Environment
```bash
# Environment Variables
DATABASE_URL=postgresql://user:pass@localhost:5432/healthcare_triage
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here
AI_API_KEY=your-ai-provider-key
HIPAA_COMPLIANCE_MODE=true
LOG_LEVEL=INFO
```

#### Development Environment
```bash
# Development overrides
DEBUG=true
LOG_LEVEL=DEBUG
HIPAA_COMPLIANCE_MODE=false
DATABASE_URL=postgresql://dev:dev@localhost:5432/triage_dev
```

### Application Startup

#### Standard Startup
```bash
# Start all services
docker-compose up -d

# Verify services
docker-compose ps
docker-compose logs -f web
```

#### Manual Startup (Development)
```bash
# Start database
systemctl start postgresql
systemctl start redis

# Start application
cd /opt/healthcare-triage
source venv/bin/activate
python app.py

# Start background workers
celery -A app.celery worker --loglevel=info
```

### Configuration Management

#### Database Configuration
```sql
-- Create primary database
CREATE DATABASE healthcare_triage;
CREATE USER triage_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE healthcare_triage TO triage_user;

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
```

#### Redis Configuration
```bash
# Redis configuration for session management
# /etc/redis/redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

#### AI Model Configuration
```python
# AI Agent Configuration
AI_AGENTS = {
    'evidence_collector': {
        'model': 'gpt-4',
        'temperature': 0.1,
        'max_tokens': 1000
    },
    'diagnostic_specialist': {
        'model': 'claude-3-opus',
        'temperature': 0.2,
        'max_tokens': 1500
    },
    'triage_coordinator': {
        'model': 'gpt-4-turbo',
        'temperature': 0.0,
        'max_tokens': 500
    }
}
```

---

## User Management

### User Roles and Permissions

#### Role Hierarchy
```
Administrator
├── System Admin (Full access)
├── Clinical Admin (Clinical settings only)
└── Security Admin (Security and audit only)

Provider
├── Attending Physician (All patients)
├── Resident (Supervised access)
├── Nurse Practitioner (Limited prescribing)
└── Physician Assistant (Limited prescribing)

Nurse
├── Charge Nurse (Administrative functions)
├── Triage Nurse (Triage functions only)
└── Staff Nurse (Basic access)

Support
├── IT Support (Technical access only)
└── Registration (Patient data entry only)
```

### User Creation and Management

#### Creating New Users
```bash
# Command line user creation
python manage.py create-user \
  --username "john.doe@hospital.com" \
  --password "temp_password_123" \
  --role "nurse" \
  --first-name "John" \
  --last-name "Doe" \
  --department "Emergency" \
  --license-number "RN123456"
```

#### Bulk User Import
```csv
# users_import.csv format
username,password,role,first_name,last_name,department,license_number
jane.smith@hospital.com,temp_pass_456,provider,Jane,Smith,Emergency,MD789012
bob.jones@hospital.com,temp_pass_789,nurse,Bob,Jones,ICU,RN345678
```

```bash
# Import users from CSV
python manage.py import-users --file users_import.csv
```

#### User Deactivation
```python
# Secure user deactivation process
def deactivate_user(user_id):
    user = User.query.get(user_id)
    user.is_active = False
    user.deactivated_at = datetime.utcnow()
    user.deactivated_by = current_user.id
    
    # Revoke all active sessions
    UserSession.query.filter_by(user_id=user_id).update({'is_active': False})
    
    # Log security event
    log_security_event('USER_DEACTIVATED', user_id=user_id)
    
    db.session.commit()
```

### Access Control Management

#### Permission Matrix
```python
ROLE_PERMISSIONS = {
    'administrator': [
        'user.create', 'user.read', 'user.update', 'user.delete',
        'patient.create', 'patient.read', 'patient.update', 'patient.delete',
        'triage.create', 'triage.read', 'triage.update', 'triage.delete',
        'system.configure', 'audit.read', 'reports.all'
    ],
    'provider': [
        'patient.read', 'patient.update',
        'triage.read', 'triage.update', 'triage.complete',
        'orders.create', 'prescriptions.create'
    ],
    'nurse': [
        'patient.create', 'patient.read', 'patient.update',
        'triage.create', 'triage.read', 'triage.update',
        'vitals.create', 'vitals.read'
    ]
}
```

#### Session Management
```python
# Session configuration
SESSION_CONFIG = {
    'timeout_minutes': 30,
    'max_concurrent_sessions': 3,
    'require_mfa_for_admin': True,
    'session_encryption': True,
    'secure_cookies': True
}
```

---

## Security Administration

### Authentication Configuration

#### Multi-Factor Authentication Setup
```python
# MFA Configuration
MFA_CONFIG = {
    'enabled': True,
    'methods': ['totp', 'sms', 'email'],
    'backup_codes': True,
    'grace_period_hours': 24,
    'required_for_roles': ['administrator', 'provider']
}
```

#### Password Policy
```python
PASSWORD_POLICY = {
    'min_length': 12,
    'require_uppercase': True,
    'require_lowercase': True,
    'require_numbers': True,
    'require_symbols': True,
    'max_age_days': 90,
    'history_count': 12,
    'lockout_attempts': 5,
    'lockout_duration_minutes': 30
}
```

### Encryption Management

#### Data Encryption at Rest
```python
# PHI Encryption Configuration
ENCRYPTION_CONFIG = {
    'algorithm': 'AES-256-GCM',
    'key_rotation_days': 90,
    'encrypted_fields': [
        'patients.ssn',
        'patients.date_of_birth',
        'patients.phone',
        'patients.address',
        'patients.insurance_id',
        'triage_sessions.chief_complaint',
        'triage_sessions.provider_notes'
    ]
}
```

#### Key Management
```bash
# Generate new encryption key
python manage.py generate-encryption-key

# Rotate encryption keys
python manage.py rotate-encryption-keys --backup-old

# Verify key integrity
python manage.py verify-encryption-keys
```

### Security Monitoring

#### Failed Login Monitoring
```python
# Security event monitoring
def monitor_failed_logins():
    threshold = 5  # Failed attempts
    window_minutes = 15
    
    recent_failures = SecurityEvent.query.filter(
        SecurityEvent.event_type == 'LOGIN_FAILED',
        SecurityEvent.timestamp >= datetime.utcnow() - timedelta(minutes=window_minutes)
    ).group_by(SecurityEvent.ip_address).all()
    
    for failure_group in recent_failures:
        if failure_group.count >= threshold:
            block_ip_address(failure_group.ip_address)
            send_security_alert(f"IP blocked: {failure_group.ip_address}")
```

#### Anomaly Detection
```python
# Unusual access pattern detection
def detect_anomalies():
    users = User.query.filter_by(is_active=True).all()
    
    for user in users:
        # Check unusual login times
        recent_logins = get_recent_logins(user.id, days=7)
        if has_unusual_time_pattern(recent_logins):
            create_security_alert(user.id, 'UNUSUAL_LOGIN_TIME')
        
        # Check unusual IP addresses
        recent_ips = get_recent_login_ips(user.id, days=30)
        if has_new_location(recent_ips):
            create_security_alert(user.id, 'NEW_LOGIN_LOCATION')
```

---

## Database Management

### Database Maintenance

#### Regular Maintenance Tasks
```sql
-- Weekly maintenance script
-- Update table statistics
ANALYZE;

-- Rebuild indexes if needed
REINDEX INDEX CONCURRENTLY idx_patients_created_at;
REINDEX INDEX CONCURRENTLY idx_triage_sessions_timestamp;

-- Clean up old sessions
DELETE FROM user_sessions 
WHERE last_activity < NOW() - INTERVAL '30 days';

-- Archive old audit logs
INSERT INTO audit_logs_archive 
SELECT * FROM audit_logs 
WHERE timestamp < NOW() - INTERVAL '7 years';

DELETE FROM audit_logs 
WHERE timestamp < NOW() - INTERVAL '7 years';
```

#### Performance Monitoring
```sql
-- Monitor slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
WHERE mean_time > 1000  -- Queries taking more than 1 second
ORDER BY mean_time DESC;

-- Monitor table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Data Retention Policies

#### Automated Data Retention
```python
def apply_retention_policies():
    """Apply data retention policies per HIPAA requirements"""
    
    # Archive patients after 7 years of inactivity
    inactive_patients = Patient.query.filter(
        Patient.last_activity < datetime.utcnow() - timedelta(days=2555)  # 7 years
    ).all()
    
    for patient in inactive_patients:
        archive_patient_data(patient.id)
        
    # Delete test/demo data after 30 days
    test_data = Patient.query.filter(
        Patient.is_test_data == True,
        Patient.created_at < datetime.utcnow() - timedelta(days=30)
    ).all()
    
    for test_record in test_data:
        delete_patient_data(test_record.id)
```

### Database Security

#### Access Control
```sql
-- Create read-only reporting user
CREATE ROLE reporting_user WITH LOGIN PASSWORD 'secure_reporting_pass';
GRANT CONNECT ON DATABASE healthcare_triage TO reporting_user;
GRANT USAGE ON SCHEMA public TO reporting_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reporting_user;

-- Revoke sensitive table access
REVOKE SELECT ON patients FROM reporting_user;
REVOKE SELECT ON audit_logs FROM reporting_user;
```

#### Audit Configuration
```sql
-- Enable audit logging for all PHI tables
ALTER TABLE patients ADD COLUMN audit_log_id UUID;
ALTER TABLE triage_sessions ADD COLUMN audit_log_id UUID;

-- Create audit trigger function
CREATE OR REPLACE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (
        table_name, operation, old_values, new_values, 
        user_id, timestamp, ip_address
    ) VALUES (
        TG_TABLE_NAME, TG_OP, 
        row_to_json(OLD), row_to_json(NEW),
        current_user_id(), NOW(), current_client_ip()
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

---

## System Monitoring

### Application Monitoring

#### Health Check Endpoints
```python
@app.route('/api/health')
def health_check():
    """Comprehensive health check"""
    checks = {}
    
    # Database connectivity
    try:
        db.session.execute('SELECT 1')
        checks['database'] = 'healthy'
    except Exception as e:
        checks['database'] = f'unhealthy: {str(e)}'
    
    # Redis connectivity
    try:
        redis_client.ping()
        checks['redis'] = 'healthy'
    except Exception as e:
        checks['redis'] = f'unhealthy: {str(e)}'
    
    # AI service connectivity
    try:
        test_ai_connection()
        checks['ai_service'] = 'healthy'
    except Exception as e:
        checks['ai_service'] = f'unhealthy: {str(e)}'
    
    # Disk space check
    disk_usage = get_disk_usage()
    if disk_usage > 90:
        checks['disk_space'] = f'warning: {disk_usage}% used'
    else:
        checks['disk_space'] = 'healthy'
    
    overall_status = 'healthy' if all('healthy' in v for v in checks.values()) else 'unhealthy'
    
    return jsonify({
        'status': overall_status,
        'checks': checks,
        'timestamp': datetime.utcnow().isoformat()
    })
```

#### Performance Metrics
```python
# Prometheus metrics configuration
from prometheus_client import Counter, Histogram, Gauge

# Application metrics
request_count = Counter('http_requests_total', 'HTTP requests', ['method', 'endpoint', 'status'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
active_sessions = Gauge('active_user_sessions', 'Number of active user sessions')
triage_processing_time = Histogram('triage_processing_seconds', 'Time to process triage')
ai_agent_response_time = Histogram('ai_agent_response_seconds', 'AI agent response time', ['agent_type'])

# Business metrics
patients_triaged_today = Gauge('patients_triaged_today', 'Patients triaged today')
critical_patients_waiting = Gauge('critical_patients_waiting', 'Critical patients in queue')
average_wait_time = Gauge('average_wait_time_minutes', 'Average patient wait time')
```

### Log Management

#### Log Configuration
```python
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
        },
        'json': {
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(name)s"}'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/healthcare-triage/app.log',
            'maxBytes': 50000000,  # 50MB
            'backupCount': 10,
            'formatter': 'json'
        },
        'security': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/healthcare-triage/security.log',
            'maxBytes': 50000000,
            'backupCount': 20,  # Keep more security logs
            'formatter': 'json'
        }
    },
    'loggers': {
        'app': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False
        },
        'security': {
            'handlers': ['security'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
```

#### Log Analysis
```bash
# Common log analysis commands

# Check for errors in the last hour
tail -n 1000 /var/log/healthcare-triage/app.log | jq 'select(.level == "ERROR")'

# Monitor failed logins
tail -f /var/log/healthcare-triage/security.log | jq 'select(.event_type == "LOGIN_FAILED")'

# Check AI processing times
grep "ai_processing_time" /var/log/healthcare-triage/app.log | awk '{print $5}' | sort -n

# Monitor database performance
grep "database_query" /var/log/healthcare-triage/app.log | jq '.query_time' | sort -n
```

### Alert Configuration

#### Critical Alerts
```python
ALERT_CONFIG = {
    'critical': {
        'system_down': {
            'condition': 'health_check_failures > 3',
            'notification': ['email', 'sms', 'slack'],
            'recipients': ['admin@hospital.com', 'oncall@hospital.com']
        },
        'database_down': {
            'condition': 'database_connection_failures > 1',
            'notification': ['email', 'sms'],
            'recipients': ['dba@hospital.com', 'admin@hospital.com']
        },
        'security_breach': {
            'condition': 'failed_login_attempts > 20 in 5min',
            'notification': ['email', 'sms', 'security_team'],
            'recipients': ['security@hospital.com', 'admin@hospital.com']
        }
    },
    'warning': {
        'high_response_time': {
            'condition': 'avg_response_time > 5000ms for 10min',
            'notification': ['email'],
            'recipients': ['devops@hospital.com']
        },
        'disk_space_low': {
            'condition': 'disk_usage > 85%',
            'notification': ['email'],
            'recipients': ['sysadmin@hospital.com']
        }
    }
}
```

---

## Backup and Recovery

### Backup Strategy

#### Database Backups
```bash
#!/bin/bash
# Database backup script
BACKUP_DIR="/backup/database"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="healthcare_triage"

# Full backup (daily)
pg_dump -h localhost -U postgres -d $DB_NAME -f $BACKUP_DIR/full_backup_$DATE.sql

# Incremental backup using WAL archiving
pg_basebackup -D $BACKUP_DIR/base_backup_$DATE -Ft -z -P

# Clean up old backups (keep 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "base_backup_*" -mtime +30 -exec rm -rf {} \;
```

#### Application Backups
```bash
#!/bin/bash
# Application and configuration backup
BACKUP_DIR="/backup/application"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup application code
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz /opt/healthcare-triage/

# Backup configuration files
tar -czf $BACKUP_DIR/config_backup_$DATE.tar.gz \
    /etc/healthcare-triage/ \
    /etc/nginx/sites-available/healthcare-triage \
    /etc/systemd/system/healthcare-triage.service

# Backup logs
tar -czf $BACKUP_DIR/logs_backup_$DATE.tar.gz /var/log/healthcare-triage/
```

### Disaster Recovery

#### Recovery Procedures
```bash
# Database Recovery Procedure

# 1. Stop application services
systemctl stop healthcare-triage
systemctl stop nginx

# 2. Restore database from backup
pg_restore -h localhost -U postgres -d healthcare_triage_restore backup_file.sql

# 3. Point-in-time recovery (if needed)
pg_ctl stop -D /var/lib/postgresql/data
rm -rf /var/lib/postgresql/data/*
pg_basebackup -D /var/lib/postgresql/data -Fp -P
# Configure recovery.conf for target time
pg_ctl start -D /var/lib/postgresql/data

# 4. Restart services
systemctl start healthcare-triage
systemctl start nginx
```

#### Testing Recovery
```bash
# Monthly disaster recovery test
#!/bin/bash

# Create test environment
docker run -d --name postgres-test postgres:13
docker run -d --name redis-test redis:6

# Restore from backup
pg_restore -h postgres-test -U postgres -d test_db latest_backup.sql

# Run smoke tests
python test_recovery.py --database postgres-test

# Cleanup test environment
docker stop postgres-test redis-test
docker rm postgres-test redis-test
```

---

## Compliance Management

### HIPAA Compliance Monitoring

#### Audit Trail Management
```python
def generate_hipaa_audit_report(start_date, end_date):
    """Generate comprehensive HIPAA audit report"""
    
    report = {
        'period': f"{start_date} to {end_date}",
        'phi_access_events': [],
        'user_activities': [],
        'security_incidents': [],
        'policy_violations': []
    }
    
    # PHI access events
    phi_access = AuditLog.query.filter(
        AuditLog.table_name.in_(['patients', 'triage_sessions']),
        AuditLog.timestamp >= start_date,
        AuditLog.timestamp <= end_date
    ).all()
    
    for access in phi_access:
        report['phi_access_events'].append({
            'timestamp': access.timestamp,
            'user_id': access.user_id,
            'action': access.action,
            'resource': f"{access.table_name}:{access.resource_id}",
            'ip_address': access.ip_address
        })
    
    # Security incidents
    incidents = SecurityEvent.query.filter(
        SecurityEvent.timestamp >= start_date,
        SecurityEvent.timestamp <= end_date,
        SecurityEvent.severity.in_(['HIGH', 'CRITICAL'])
    ).all()
    
    for incident in incidents:
        report['security_incidents'].append({
            'timestamp': incident.timestamp,
            'event_type': incident.event_type,
            'severity': incident.severity,
            'description': incident.description,
            'resolved': incident.resolved
        })
    
    return report
```

#### Privacy Impact Assessment
```python
def conduct_privacy_assessment():
    """Automated privacy impact assessment"""
    
    assessment = {
        'data_collection': analyze_data_collection(),
        'data_storage': analyze_data_storage(),
        'data_access': analyze_data_access(),
        'data_sharing': analyze_data_sharing(),
        'data_retention': analyze_data_retention(),
        'risk_score': 0,
        'recommendations': []
    }
    
    # Calculate risk score based on findings
    risk_factors = [
        assessment['data_collection']['risk_level'],
        assessment['data_storage']['risk_level'],
        assessment['data_access']['risk_level']
    ]
    
    assessment['risk_score'] = sum(risk_factors) / len(risk_factors)
    
    # Generate recommendations
    if assessment['risk_score'] > 7:
        assessment['recommendations'].append("Implement additional encryption")
        assessment['recommendations'].append("Restrict data access permissions")
    
    return assessment
```

### Regulatory Reporting

#### Automated Compliance Reports
```python
def generate_regulatory_reports():
    """Generate required regulatory reports"""
    
    reports = {}
    
    # HIPAA Security Report
    reports['hipaa_security'] = {
        'encryption_status': check_encryption_compliance(),
        'access_controls': check_access_controls(),
        'audit_logs': check_audit_log_completeness(),
        'incident_reports': get_security_incidents(),
        'training_records': get_training_compliance()
    }
    
    # Quality Assurance Report
    reports['quality_assurance'] = {
        'ai_accuracy_metrics': get_ai_accuracy_metrics(),
        'clinical_outcomes': get_clinical_outcomes(),
        'patient_satisfaction': get_satisfaction_scores(),
        'error_rates': get_error_rates()
    }
    
    # Usage Statistics Report
    reports['usage_statistics'] = {
        'total_patients': get_patient_count(),
        'triage_volume': get_triage_volume(),
        'user_adoption': get_user_adoption_metrics(),
        'system_uptime': get_uptime_statistics()
    }
    
    return reports
```

---

## Integration Management

### Electronic Health Record (EHR) Integration

#### HL7 FHIR Integration
```python
from fhirclient import client
from fhirclient.models import patient, observation, encounter

class EHRIntegration:
    def __init__(self, fhir_base_url, credentials):
        self.settings = {
            'app_id': 'healthcare-triage',
            'api_base': fhir_base_url,
            'redirect_uri': 'https://triage.hospital.com/auth/callback'
        }
        self.client = client.FHIRClient(settings=self.settings)
    
    def create_patient_record(self, triage_data):
        """Create FHIR patient record from triage data"""
        
        # Create Patient resource
        patient_resource = patient.Patient()
        patient_resource.name = [patient.HumanName({
            'given': [triage_data['first_name']],
            'family': triage_data['last_name']
        })]
        patient_resource.gender = triage_data['gender']
        patient_resource.birthDate = triage_data['date_of_birth']
        
        # Create patient in EHR
        patient_resource.create(self.client.server)
        
        return patient_resource.id
    
    def create_encounter(self, patient_id, triage_session):
        """Create encounter record for triage session"""
        
        encounter_resource = encounter.Encounter()
        encounter_resource.status = 'in-progress'
        encounter_resource.class_fhir = 'emergency'
        encounter_resource.subject = patient.Reference(f"Patient/{patient_id}")
        encounter_resource.reasonCode = [{
            'text': triage_session['chief_complaint']
        }]
        
        encounter_resource.create(self.client.server)
        return encounter_resource.id
    
    def send_vital_signs(self, patient_id, vitals):
        """Send vital signs as FHIR observations"""
        
        observations = []
        
        # Blood pressure
        bp_obs = observation.Observation()
        bp_obs.status = 'final'
        bp_obs.code = {'coding': [{'system': 'http://loinc.org', 'code': '85354-9'}]}
        bp_obs.subject = patient.Reference(f"Patient/{patient_id}")
        bp_obs.component = [
            {
                'code': {'coding': [{'system': 'http://loinc.org', 'code': '8480-6'}]},
                'valueQuantity': {'value': vitals['systolic'], 'unit': 'mmHg'}
            },
            {
                'code': {'coding': [{'system': 'http://loinc.org', 'code': '8462-4'}]},
                'valueQuantity': {'value': vitals['diastolic'], 'unit': 'mmHg'}
            }
        ]
        
        observations.append(bp_obs)
        
        # Heart rate
        hr_obs = observation.Observation()
        hr_obs.status = 'final'
        hr_obs.code = {'coding': [{'system': 'http://loinc.org', 'code': '8867-4'}]}
        hr_obs.subject = patient.Reference(f"Patient/{patient_id}")
        hr_obs.valueQuantity = {'value': vitals['heart_rate'], 'unit': '/min'}
        
        observations.append(hr_obs)
        
        # Create all observations
        for obs in observations:
            obs.create(self.client.server)
```

### Laboratory System Integration

#### Laboratory Information System (LIS) Integration
```python
class LISIntegration:
    def __init__(self, lis_endpoint, api_key):
        self.endpoint = lis_endpoint
        self.api_key = api_key
    
    def order_lab_tests(self, patient_id, tests, priority='routine'):
        """Order laboratory tests based on triage assessment"""
        
        order_data = {
            'patient_id': patient_id,
            'tests': tests,
            'priority': priority,
            'ordering_provider': current_user.provider_id,
            'clinical_indication': 'Emergency department triage'
        }
        
        response = requests.post(
            f"{self.endpoint}/orders",
            json=order_data,
            headers={'Authorization': f'Bearer {self.api_key}'}
        )
        
        return response.json()
    
    def get_results(self, order_id):
        """Retrieve laboratory results"""
        
        response = requests.get(
            f"{self.endpoint}/orders/{order_id}/results",
            headers={'Authorization': f'Bearer {self.api_key}'}
        )
        
        return response.json()
```

### Notification System Integration

#### Multi-channel Notification Setup
```python
class NotificationManager:
    def __init__(self):
        self.channels = {
            'email': EmailChannel(),
            'sms': SMSChannel(),
            'slack': SlackChannel(),
            'pager': PagerChannel()
        }
    
    def send_critical_alert(self, message, recipients):
        """Send critical alerts via multiple channels"""
        
        # Send via all configured channels for critical alerts
        for channel_name, channel in self.channels.items():
            try:
                if channel.is_configured():
                    channel.send(message, recipients)
                    log_notification(channel_name, message, recipients)
            except Exception as e:
                logger.error(f"Failed to send via {channel_name}: {str(e)}")
    
    def send_provider_notification(self, provider_id, patient_info, urgency='medium'):
        """Send provider notification based on preferences"""
        
        provider = Provider.query.get(provider_id)
        preferred_channels = provider.notification_preferences.get(urgency, ['email'])
        
        message = f"New patient assignment: {patient_info['name']} - {patient_info['triage_level']} priority"
        
        for channel_name in preferred_channels:
            if channel_name in self.channels:
                self.channels[channel_name].send(message, [provider.contact_info[channel_name]])
```

---

## Maintenance and Updates

### Routine Maintenance Schedule

#### Daily Tasks
- Monitor system health and performance
- Review security alerts and failed login attempts
- Check backup completion status
- Monitor disk space and system resources

#### Weekly Tasks
- Review user access reports
- Analyze AI model performance metrics
- Update virus definitions and security patches
- Clean up temporary files and logs

#### Monthly Tasks
- Generate compliance reports
- Review and update user permissions
- Perform disaster recovery testing
- Update system documentation

#### Quarterly Tasks
- Security vulnerability assessment
- AI model retraining and optimization
- Performance optimization review
- Compliance audit preparation

### System Updates

#### Application Updates
```bash
#!/bin/bash
# Application update procedure

# 1. Backup current version
cp -r /opt/healthcare-triage /opt/healthcare-triage.backup.$(date +%Y%m%d)

# 2. Stop services
systemctl stop healthcare-triage
systemctl stop celery-worker

# 3. Update application
cd /opt/healthcare-triage
git pull origin main
pip install -r requirements.txt

# 4. Run database migrations
python manage.py db upgrade

# 5. Update static files
python manage.py collectstatic

# 6. Restart services
systemctl start healthcare-triage
systemctl start celery-worker

# 7. Verify health
curl -f http://localhost:5000/api/health || exit 1
```

#### Security Updates
```bash
#!/bin/bash
# Security update procedure

# Update system packages
apt update && apt upgrade -y

# Update Python packages
pip install --upgrade -r requirements.txt

# Update Node.js packages (if applicable)
npm audit fix

# Restart services
systemctl restart healthcare-triage
systemctl restart nginx
```

---

For technical support or escalation, contact the Healthcare IT department at ext. 1234 or healthcare-it@hospital.com.