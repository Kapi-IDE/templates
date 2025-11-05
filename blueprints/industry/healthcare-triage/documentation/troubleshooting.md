# Healthcare Triage System - Troubleshooting Guide

## Table of Contents
1. [Common Issues](#common-issues)
2. [System Performance](#system-performance)
3. [Authentication Problems](#authentication-problems)
4. [AI Assessment Issues](#ai-assessment-issues)
5. [Database Problems](#database-problems)
6. [Integration Issues](#integration-issues)
7. [Emergency Procedures](#emergency-procedures)
8. [Diagnostic Tools](#diagnostic-tools)

---

## Common Issues

### Issue: Patient Data Not Saving

**Symptoms:**
- Error message when clicking "Save" or "Continue"
- Form data disappears after submission
- "Network Error" or "Server Error" messages

**Troubleshooting Steps:**
1. **Check Network Connection**
   ```bash
   # Test connectivity
   curl -I https://api.healthcare-triage.com/health
   ping api.healthcare-triage.com
   ```

2. **Verify Form Completion**
   - Ensure all required fields (marked with *) are filled
   - Check for special characters in name fields
   - Verify phone number format (e.g., 555-123-4567)

3. **Browser Issues**
   ```javascript
   // Check console for JavaScript errors
   // Press F12 and look at Console tab
   console.log("Check for errors here");
   ```
   - Clear browser cache (Ctrl+Shift+Delete)
   - Disable browser extensions temporarily
   - Try incognito/private browsing mode

4. **Session Timeout**
   - Check if login session has expired
   - Look for "401 Unauthorized" errors
   - Re-login and try again

**Resolution:**
- If network is down, contact IT support
- If validation errors, correct the data and retry
- If browser issues persist, try different browser
- If session expired, login again

### Issue: Slow System Performance

**Symptoms:**
- Pages take more than 10 seconds to load
- Timeout errors
- AI assessments taking over 2 minutes

**Troubleshooting Steps:**
1. **Check System Resources**
   ```bash
   # On server
   top
   free -h
   df -h
   iotop
   ```

2. **Network Performance**
   ```bash
   # Test network speed
   speedtest-cli
   # Check latency
   ping -c 10 api.healthcare-triage.com
   ```

3. **Database Performance**
   ```sql
   -- Check for slow queries
   SELECT query, calls, total_time, mean_time 
   FROM pg_stat_statements 
   WHERE mean_time > 1000 
   ORDER BY mean_time DESC LIMIT 10;
   
   -- Check active connections
   SELECT count(*) FROM pg_stat_activity;
   ```

4. **Application Performance**
   ```bash
   # Check application logs
   tail -f /var/log/healthcare-triage/app.log | grep -i "slow\|timeout\|error"
   
   # Monitor memory usage
   ps aux | grep healthcare-triage
   ```

**Resolution:**
- If high CPU/memory usage, restart services
- If database issues, run maintenance scripts
- If network issues, contact network team
- If persistent issues, scale resources

### Issue: Login Problems

**Symptoms:**
- "Invalid credentials" despite correct password
- Login page not loading
- Two-factor authentication not working

**Troubleshooting Steps:**
1. **Verify Credentials**
   - Check caps lock is off
   - Verify username format (email address)
   - Try password reset if uncertain

2. **Account Status**
   ```sql
   -- Check user account status
   SELECT username, is_active, locked_at, failed_login_attempts 
   FROM users 
   WHERE username = 'user@hospital.com';
   ```

3. **Two-Factor Authentication**
   - Ensure device time is synchronized
   - Try backup codes if available
   - Check for MFA app updates

4. **Browser/Cookies**
   - Clear cookies for the site
   - Disable ad blockers
   - Try different browser

**Resolution:**
- If account locked, contact administrator
- If MFA issues, use backup method or contact IT
- If browser issues, clear data and retry

---

## System Performance

### Memory Issues

**Symptoms:**
- OutOfMemory errors in logs
- Application crashes
- Slow response times

**Diagnosis:**
```bash
# Check memory usage
free -h
cat /proc/meminfo

# Check application memory
ps aux --sort=-%mem | head -10

# Check for memory leaks
valgrind --tool=memcheck --leak-check=full python app.py
```

**Resolution:**
```bash
# Restart services to free memory
systemctl restart healthcare-triage
systemctl restart redis
systemctl restart postgresql

# Increase memory limits
# Edit /etc/systemd/system/healthcare-triage.service
[Service]
MemoryLimit=4G

# Reload and restart
systemctl daemon-reload
systemctl restart healthcare-triage
```

### CPU Issues

**Symptoms:**
- High CPU usage (>90%)
- System responsiveness poor
- Timeout errors

**Diagnosis:**
```bash
# Monitor CPU usage
top -p $(pgrep healthcare-triage)

# Check CPU-intensive processes
ps aux --sort=-%cpu | head -10

# Profile application
python -m cProfile -o profile.out app.py
python -c "import pstats; pstats.Stats('profile.out').sort_stats('cumulative').print_stats(20)"
```

**Resolution:**
```bash
# Scale horizontally
docker-compose up --scale web=3

# Optimize database queries
# Add indexes for frequently queried columns
CREATE INDEX CONCURRENTLY idx_patients_name ON patients(name);
CREATE INDEX CONCURRENTLY idx_triage_timestamp ON triage_sessions(created_at);

# Enable caching
redis-cli FLUSHALL  # Clear and restart Redis caching
```

### Database Performance

**Symptoms:**
- Slow query responses
- Connection timeouts
- Database locks

**Diagnosis:**
```sql
-- Check slow queries
SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements
WHERE mean_time > 100
ORDER BY mean_time DESC;

-- Check active connections
SELECT pid, usename, application_name, state, query_start, query
FROM pg_stat_activity
WHERE state = 'active';

-- Check for locks
SELECT blocked_locks.pid AS blocked_pid,
       blocked_activity.usename AS blocked_user,
       blocking_locks.pid AS blocking_pid,
       blocking_activity.usename AS blocking_user,
       blocked_activity.query AS blocked_statement,
       blocking_activity.query AS current_statement_in_blocking_process
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

**Resolution:**
```sql
-- Kill problematic queries
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE query LIKE '%slow_query%';

-- Update table statistics
ANALYZE;

-- Vacuum tables
VACUUM ANALYZE patients;
VACUUM ANALYZE triage_sessions;
VACUUM ANALYZE audit_logs;

-- Add missing indexes
CREATE INDEX CONCURRENTLY idx_triage_patient_id ON triage_sessions(patient_id);
CREATE INDEX CONCURRENTLY idx_audit_timestamp ON audit_logs(timestamp);
```

---

## Authentication Problems

### Token Expiration Issues

**Symptoms:**
- Frequent login prompts
- "Token expired" errors
- Session timeouts

**Diagnosis:**
```python
# Check token configuration
import jwt
import datetime

def debug_token(token):
    try:
        payload = jwt.decode(token, verify=False)
        exp = datetime.datetime.fromtimestamp(payload['exp'])
        print(f"Token expires at: {exp}")
        print(f"Current time: {datetime.datetime.now()}")
        print(f"Time remaining: {exp - datetime.datetime.now()}")
    except Exception as e:
        print(f"Token error: {e}")
```

**Resolution:**
```python
# Adjust token expiration settings
JWT_CONFIG = {
    'access_token_expires': timedelta(hours=8),  # Extend from 1 hour to 8 hours
    'refresh_token_expires': timedelta(days=30),
    'auto_refresh': True  # Enable automatic token refresh
}

# Implement token refresh middleware
@app.before_request
def refresh_token_if_needed():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if token and is_token_expiring_soon(token):
        new_token = refresh_access_token(token)
        response.headers['X-New-Token'] = new_token
```

### MFA Configuration Issues

**Symptoms:**
- MFA codes not working
- Backup codes invalid
- Cannot disable MFA

**Diagnosis:**
```python
# Check MFA configuration
def check_mfa_status(user_id):
    user = User.query.get(user_id)
    mfa_settings = user.mfa_settings
    
    print(f"MFA enabled: {mfa_settings.get('enabled', False)}")
    print(f"MFA methods: {mfa_settings.get('methods', [])}")
    print(f"Backup codes remaining: {len(mfa_settings.get('backup_codes', []))}")
    print(f"Last used: {mfa_settings.get('last_used_at')}")
```

**Resolution:**
```python
# Reset MFA for user
def reset_user_mfa(user_id):
    user = User.query.get(user_id)
    user.mfa_settings = {
        'enabled': False,
        'secret': None,
        'backup_codes': generate_backup_codes(),
        'setup_complete': False
    }
    db.session.commit()
    
    # Log security event
    log_security_event('MFA_RESET', user_id=user_id, admin_id=current_user.id)

# Generate new backup codes
def generate_backup_codes():
    return [secrets.token_hex(4).upper() for _ in range(10)]
```

### Permission Errors

**Symptoms:**
- "Access denied" for normal operations
- Features not visible to users
- API endpoints returning 403 errors

**Diagnosis:**
```python
# Check user permissions
def debug_user_permissions(user_id):
    user = User.query.get(user_id)
    role = Role.query.get(user.role_id)
    
    print(f"User: {user.username}")
    print(f"Role: {role.name}")
    print(f"Permissions: {[p.name for p in role.permissions]}")
    
    # Check specific permission
    def has_permission(permission_name):
        return permission_name in [p.name for p in role.permissions]
    
    print(f"Can create patients: {has_permission('patient.create')}")
    print(f"Can update triage: {has_permission('triage.update')}")
```

**Resolution:**
```python
# Fix user permissions
def fix_user_permissions(user_id, correct_role):
    user = User.query.get(user_id)
    role = Role.query.filter_by(name=correct_role).first()
    
    if role:
        user.role_id = role.id
        db.session.commit()
        
        # Clear cached permissions
        cache.delete(f"user_permissions_{user_id}")
        
        print(f"Updated {user.username} to {correct_role} role")
    else:
        print(f"Role {correct_role} not found")
```

---

## AI Assessment Issues

### AI Service Unavailable

**Symptoms:**
- "AI service temporarily unavailable" messages
- Assessments timing out after 30 seconds
- Error code 503 (Service Unavailable)

**Diagnosis:**
```python
# Check AI service health
import requests

def check_ai_services():
    services = {
        'openai': 'https://api.openai.com/v1/models',
        'anthropic': 'https://api.anthropic.com/v1/health',
        'google': 'https://ai.googleapis.com/v1/models'
    }
    
    for service, url in services.items():
        try:
            response = requests.get(url, timeout=10)
            print(f"{service}: {response.status_code}")
        except Exception as e:
            print(f"{service}: ERROR - {e}")
```

**Resolution:**
```python
# Implement fallback AI providers
AI_PROVIDERS = [
    {'name': 'openai', 'priority': 1, 'enabled': True},
    {'name': 'anthropic', 'priority': 2, 'enabled': True},
    {'name': 'google', 'priority': 3, 'enabled': True}
]

def get_ai_assessment_with_fallback(session_data):
    for provider in sorted(AI_PROVIDERS, key=lambda x: x['priority']):
        if not provider['enabled']:
            continue
            
        try:
            return get_ai_assessment(session_data, provider['name'])
        except Exception as e:
            logger.warning(f"AI provider {provider['name']} failed: {e}")
            continue
    
    # If all AI providers fail, use rule-based assessment
    return get_rule_based_assessment(session_data)
```

### Inaccurate AI Assessments

**Symptoms:**
- AI consistently over/under-triaging patients
- Confidence scores unusually low
- Provider disagreement with AI recommendations

**Diagnosis:**
```python
# Analyze AI performance
def analyze_ai_performance(days=30):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    sessions = TriageSession.query.filter(
        TriageSession.completed_at.between(start_date, end_date),
        TriageSession.ai_assessment.isnot(None),
        TriageSession.provider_final_triage.isnot(None)
    ).all()
    
    accurate = 0
    total = len(sessions)
    
    for session in sessions:
        ai_level = session.ai_assessment['triage_level']
        provider_level = session.provider_final_triage
        
        if ai_level == provider_level:
            accurate += 1
    
    accuracy = accurate / total if total > 0 else 0
    print(f"AI Accuracy: {accuracy:.2%} ({accurate}/{total})")
    
    return accuracy
```

**Resolution:**
```python
# Retrain AI model with recent data
def retrain_ai_model():
    # Collect training data from recent accurate assessments
    training_data = []
    
    accurate_sessions = TriageSession.query.filter(
        TriageSession.ai_assessment['triage_level'] == TriageSession.provider_final_triage,
        TriageSession.completed_at >= datetime.utcnow() - timedelta(days=90)
    ).all()
    
    for session in accurate_sessions:
        training_data.append({
            'symptoms': session.symptoms,
            'vitals': session.vitals,
            'history': session.medical_history,
            'triage_level': session.provider_final_triage
        })
    
    # Send to AI training pipeline
    retrain_request = {
        'training_data': training_data,
        'model_version': 'healthcare_triage_v2',
        'validation_split': 0.2
    }
    
    response = requests.post(
        'https://ai-training.healthcare-triage.com/retrain',
        json=retrain_request
    )
    
    return response.json()

# Adjust AI confidence thresholds
def adjust_confidence_thresholds():
    AI_CONFIG['confidence_thresholds'] = {
        'CRITICAL': 0.95,  # Increased from 0.90
        'HIGH': 0.85,      # Increased from 0.80
        'MEDIUM': 0.70,    # Increased from 0.65
        'LOW': 0.50        # Increased from 0.45
    }
```

### AI Processing Delays

**Symptoms:**
- AI assessments taking over 30 seconds
- Timeout errors during peak hours
- Queue buildup for AI processing

**Diagnosis:**
```python
# Monitor AI processing times
def monitor_ai_performance():
    recent_assessments = AIAssessmentLog.query.filter(
        AIAssessmentLog.created_at >= datetime.utcnow() - timedelta(hours=1)
    ).all()
    
    times = [a.processing_time_ms for a in recent_assessments]
    
    print(f"Average processing time: {sum(times)/len(times):.0f}ms")
    print(f"Max processing time: {max(times)}ms")
    print(f"Min processing time: {min(times)}ms")
    print(f"Total assessments: {len(times)}")
```

**Resolution:**
```python
# Implement AI assessment queue with workers
import celery

@celery.task
def process_ai_assessment(session_id):
    session = TriageSession.query.get(session_id)
    
    try:
        assessment = get_ai_assessment(session.to_dict())
        session.ai_assessment = assessment
        session.ai_processed_at = datetime.utcnow()
        db.session.commit()
        
        # Notify frontend via WebSocket
        socketio.emit('ai_assessment_complete', {
            'session_id': session_id,
            'assessment': assessment
        }, room=f"session_{session_id}")
        
    except Exception as e:
        logger.error(f"AI assessment failed for session {session_id}: {e}")
        
        # Use fallback assessment
        fallback_assessment = get_rule_based_assessment(session.to_dict())
        session.ai_assessment = fallback_assessment
        session.ai_processed_at = datetime.utcnow()
        db.session.commit()

# Scale AI workers based on queue size
def scale_ai_workers():
    queue_size = process_ai_assessment.queue_length()
    
    if queue_size > 50:
        # Scale up workers
        subprocess.run(['docker-compose', 'up', '--scale', 'ai-worker=5'])
    elif queue_size < 10:
        # Scale down workers
        subprocess.run(['docker-compose', 'up', '--scale', 'ai-worker=2'])
```

---

## Database Problems

### Connection Issues

**Symptoms:**
- "Database connection failed" errors
- Connection timeouts
- "Too many connections" errors

**Diagnosis:**
```sql
-- Check connection count
SELECT count(*) as connection_count FROM pg_stat_activity;

-- Check connection limits
SHOW max_connections;

-- Check active connections by user
SELECT usename, count(*) 
FROM pg_stat_activity 
GROUP BY usename;

-- Check idle connections
SELECT count(*) 
FROM pg_stat_activity 
WHERE state = 'idle';
```

**Resolution:**
```python
# Configure connection pooling
DATABASE_CONFIG = {
    'pool_size': 20,
    'max_overflow': 0,
    'pool_pre_ping': True,
    'pool_recycle': 3600,  # 1 hour
    'echo': False
}

# Close idle connections
def cleanup_idle_connections():
    db.session.execute("""
        SELECT pg_terminate_backend(pid) 
        FROM pg_stat_activity 
        WHERE state = 'idle' 
        AND state_change < now() - interval '10 minutes'
        AND usename = 'healthcare_triage_user'
    """)
    db.session.commit()
```

### Data Integrity Issues

**Symptoms:**
- Foreign key constraint errors
- Duplicate records
- Missing required data

**Diagnosis:**
```sql
-- Check for orphaned records
SELECT p.id, p.name 
FROM patients p 
LEFT JOIN triage_sessions ts ON p.id = ts.patient_id 
WHERE ts.patient_id IS NULL 
AND p.created_at < NOW() - INTERVAL '1 day';

-- Check for duplicate patients
SELECT name, phone, count(*) 
FROM patients 
GROUP BY name, phone 
HAVING count(*) > 1;

-- Check for incomplete triage sessions
SELECT id, patient_id, created_at 
FROM triage_sessions 
WHERE status = 'in_progress' 
AND created_at < NOW() - INTERVAL '2 hours';
```

**Resolution:**
```sql
-- Clean up orphaned records
DELETE FROM audit_logs 
WHERE resource_type = 'patient' 
AND resource_id NOT IN (SELECT id FROM patients);

-- Merge duplicate patients
UPDATE triage_sessions 
SET patient_id = 'correct_patient_id' 
WHERE patient_id = 'duplicate_patient_id';

DELETE FROM patients 
WHERE id = 'duplicate_patient_id';

-- Mark stale sessions as completed
UPDATE triage_sessions 
SET status = 'timeout', 
    completed_at = NOW() 
WHERE status = 'in_progress' 
AND created_at < NOW() - INTERVAL '4 hours';
```

### Performance Degradation

**Symptoms:**
- Slow query performance
- High disk I/O
- Table bloat

**Diagnosis:**
```sql
-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) as index_size
FROM pg_tables 
WHERE schemaname = 'public' 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check index usage
SELECT 
    indexrelname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

**Resolution:**
```sql
-- Rebuild indexes
REINDEX INDEX CONCURRENTLY idx_patients_name;
REINDEX INDEX CONCURRENTLY idx_triage_sessions_created_at;

-- Update table statistics
ANALYZE patients;
ANALYZE triage_sessions;
ANALYZE audit_logs;

-- Vacuum tables
VACUUM (VERBOSE, ANALYZE) patients;
VACUUM (VERBOSE, ANALYZE) triage_sessions;
```

---

## Integration Issues

### EHR Integration Problems

**Symptoms:**
- Patient data not syncing to EHR
- "Integration service unavailable" errors
- Duplicate records in EHR

**Diagnosis:**
```python
# Test EHR connectivity
def test_ehr_integration():
    try:
        response = requests.get(
            f"{EHR_BASE_URL}/api/health",
            headers={'Authorization': f'Bearer {EHR_API_TOKEN}'},
            timeout=10
        )
        print(f"EHR Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"EHR Connection Error: {e}")
```

**Resolution:**
```python
# Implement retry mechanism for EHR integration
import backoff

@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=3,
    max_time=300
)
def sync_patient_to_ehr(patient_data):
    response = requests.post(
        f"{EHR_BASE_URL}/api/patients",
        json=patient_data,
        headers={'Authorization': f'Bearer {EHR_API_TOKEN}'}
    )
    response.raise_for_status()
    return response.json()

# Queue failed integrations for retry
def queue_failed_integration(integration_type, data, error):
    FailedIntegration.create(
        integration_type=integration_type,
        data=data,
        error=str(error),
        retry_count=0,
        next_retry=datetime.utcnow() + timedelta(minutes=5)
    )

# Background task to retry failed integrations
@celery.task
def retry_failed_integrations():
    failed_integrations = FailedIntegration.query.filter(
        FailedIntegration.next_retry <= datetime.utcnow(),
        FailedIntegration.retry_count < 5
    ).all()
    
    for integration in failed_integrations:
        try:
            if integration.integration_type == 'ehr_patient':
                sync_patient_to_ehr(integration.data)
            elif integration.integration_type == 'lis_order':
                submit_lab_order(integration.data)
            
            # Mark as successful
            integration.delete()
            
        except Exception as e:
            # Increment retry count
            integration.retry_count += 1
            integration.next_retry = datetime.utcnow() + timedelta(minutes=5 * integration.retry_count)
            integration.last_error = str(e)
            integration.save()
```

### Notification Service Issues

**Symptoms:**
- Providers not receiving alerts
- SMS/email notifications failing
- Notification delays

**Diagnosis:**
```python
# Check notification service health
def check_notification_services():
    services = {
        'email': check_email_service,
        'sms': check_sms_service,
        'slack': check_slack_service
    }
    
    for service_name, check_func in services.items():
        try:
            status = check_func()
            print(f"{service_name}: {'OK' if status else 'FAILED'}")
        except Exception as e:
            print(f"{service_name}: ERROR - {e}")

def check_email_service():
    # Test SMTP connection
    import smtplib
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.quit()
    return True
```

**Resolution:**
```python
# Implement notification fallback
def send_notification_with_fallback(recipient, message, urgency='medium'):
    notification_methods = get_user_notification_preferences(recipient)
    
    if urgency == 'critical':
        # For critical notifications, try all methods
        notification_methods = ['sms', 'email', 'slack', 'pager']
    
    for method in notification_methods:
        try:
            if method == 'sms':
                send_sms(recipient.phone, message)
            elif method == 'email':
                send_email(recipient.email, message)
            elif method == 'slack':
                send_slack_message(recipient.slack_id, message)
            elif method == 'pager':
                send_pager_alert(recipient.pager_id, message)
            
            # Log successful notification
            log_notification_sent(recipient.id, method, message)
            break
            
        except Exception as e:
            logger.warning(f"Notification method {method} failed: {e}")
            continue
    else:
        # All methods failed
        logger.error(f"All notification methods failed for user {recipient.id}")
        raise Exception("All notification methods failed")
```

---

## Emergency Procedures

### System Downtime

When the system is completely unavailable:

1. **Immediate Actions**
   ```bash
   # Switch to paper backup forms
   cp /opt/healthcare-triage/backup-forms/paper-triage-form.pdf /tmp/
   
   # Notify all users
   echo "SYSTEM DOWN - Use paper forms" | wall
   ```

2. **Paper Backup Procedures**
   - Use printed triage forms in emergency kit
   - Document all patient interactions on paper
   - Designate one person to collect all forms
   - Enter data when system returns

3. **Communication Protocol**
   - Notify IT support immediately: ext. 1234
   - Inform clinical supervisor: ext. 3456
   - Update status board: "SYSTEM MAINTENANCE"
   - Set expected restoration time

4. **Data Recovery**
   ```bash
   # When system returns, enter paper data
   python manage.py import-paper-forms --directory /tmp/paper-forms/
   
   # Verify data integrity
   python manage.py verify-data --date $(date +%Y-%m-%d)
   ```

### Critical Patient Protocol

When AI system is down but critical patient arrives:

1. **Manual Triage Process**
   ```
   CRITICAL INDICATORS (Go directly to provider):
   - Cardiac arrest
   - Severe breathing difficulty
   - Uncontrolled bleeding
   - Altered mental status
   - Severe chest pain
   - Stroke symptoms
   ```

2. **Override Procedures**
   ```python
   # Manual triage entry
   def manual_triage_override(patient_id, nurse_id, triage_level, reason):
       session = TriageSession(
           patient_id=patient_id,
           nurse_id=nurse_id,
           triage_level=triage_level,
           ai_assessment=None,
           manual_override=True,
           override_reason=reason,
           status='completed'
       )
       db.session.add(session)
       db.session.commit()
       
       # Log override
       log_manual_override(session.id, nurse_id, reason)
   ```

3. **Documentation Requirements**
   - Record reason for override
   - Document clinical reasoning
   - Get supervisor approval
   - Follow up with AI assessment when available

### Data Loss Prevention

1. **Automatic Backups**
   ```bash
   # Verify backup status
   /opt/healthcare-triage/scripts/check-backups.sh
   
   # Manual backup if needed
   pg_dump healthcare_triage > /backup/manual_backup_$(date +%Y%m%d_%H%M%S).sql
   ```

2. **Real-time Replication**
   ```sql
   -- Check replication status
   SELECT client_addr, state, sync_state 
   FROM pg_stat_replication;
   ```

3. **Recovery Procedures**
   ```bash
   # Point-in-time recovery
   pg_ctl stop -D /var/lib/postgresql/data
   rm -rf /var/lib/postgresql/data/*
   pg_basebackup -D /var/lib/postgresql/data -Fp -P
   
   # Configure recovery
   echo "restore_command = 'cp /backup/wal/%f %p'" >> /var/lib/postgresql/data/recovery.conf
   echo "recovery_target_time = '2024-01-15 10:30:00'" >> /var/lib/postgresql/data/recovery.conf
   
   pg_ctl start -D /var/lib/postgresql/data
   ```

---

## Diagnostic Tools

### Health Check Scripts

```bash
#!/bin/bash
# comprehensive-health-check.sh

echo "=== Healthcare Triage System Health Check ==="

# Check services
echo "Checking services..."
systemctl is-active healthcare-triage && echo "✓ App running" || echo "✗ App down"
systemctl is-active postgresql && echo "✓ Database running" || echo "✗ Database down"
systemctl is-active redis && echo "✓ Redis running" || echo "✗ Redis down"
systemctl is-active nginx && echo "✓ Web server running" || echo "✗ Web server down"

# Check connectivity
echo "Checking connectivity..."
curl -f -s http://localhost:5000/api/health > /dev/null && echo "✓ API responsive" || echo "✗ API not responding"
redis-cli ping > /dev/null && echo "✓ Redis responsive" || echo "✗ Redis not responding"
pg_isready -h localhost && echo "✓ Database responsive" || echo "✗ Database not responding"

# Check resources
echo "Checking resources..."
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -lt 90 ]; then
    echo "✓ Disk usage: ${DISK_USAGE}%"
else
    echo "⚠ Disk usage high: ${DISK_USAGE}%"
fi

MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
if [ $MEMORY_USAGE -lt 90 ]; then
    echo "✓ Memory usage: ${MEMORY_USAGE}%"
else
    echo "⚠ Memory usage high: ${MEMORY_USAGE}%"
fi

# Check logs for errors
echo "Checking recent errors..."
ERROR_COUNT=$(grep -c "ERROR" /var/log/healthcare-triage/app.log | tail -100)
if [ $ERROR_COUNT -eq 0 ]; then
    echo "✓ No recent errors"
else
    echo "⚠ Recent errors found: $ERROR_COUNT"
fi
```

### Performance Monitoring

```python
# performance-monitor.py
import psutil
import requests
import time
import json

def monitor_system():
    metrics = {
        'timestamp': time.time(),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'network_io': psutil.net_io_counters()._asdict(),
        'process_count': len(psutil.pids())
    }
    
    # Check application health
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        metrics['api_status'] = response.status_code
        metrics['api_response_time'] = response.elapsed.total_seconds()
    except Exception as e:
        metrics['api_status'] = 'error'
        metrics['api_error'] = str(e)
    
    # Check database performance
    try:
        response = requests.get('http://localhost:5000/api/health/database', timeout=5)
        db_health = response.json()
        metrics['db_connections'] = db_health.get('active_connections', 0)
        metrics['db_response_time'] = db_health.get('response_time_ms', 0)
    except Exception as e:
        metrics['db_status'] = 'error'
        metrics['db_error'] = str(e)
    
    return metrics

# Save metrics to file for analysis
def save_metrics():
    metrics = monitor_system()
    with open('/var/log/healthcare-triage/performance.jsonl', 'a') as f:
        f.write(json.dumps(metrics) + '\n')

if __name__ == "__main__":
    while True:
        save_metrics()
        time.sleep(60)  # Monitor every minute
```

### Log Analysis Tools

```bash
#!/bin/bash
# log-analyzer.sh

LOG_FILE="/var/log/healthcare-triage/app.log"

echo "=== Log Analysis Report ==="

# Error summary
echo "Error Summary (last 24 hours):"
grep "ERROR" $LOG_FILE | grep "$(date -d '1 day ago' +'%Y-%m-%d')" | \
    awk '{print $5}' | sort | uniq -c | sort -nr

# Response time analysis
echo "API Response Times (last hour):"
grep "api_response_time" $LOG_FILE | grep "$(date +'%Y-%m-%d %H')" | \
    awk '{print $6}' | sort -n | \
    awk '{sum+=$1; count++} END {print "Average:", sum/count, "ms"}'

# Most accessed endpoints
echo "Most Accessed Endpoints (last 24 hours):"
grep "HTTP" $LOG_FILE | grep "$(date -d '1 day ago' +'%Y-%m-%d')" | \
    awk '{print $7}' | sort | uniq -c | sort -nr | head -10

# User activity
echo "Active Users (last hour):"
grep "user_id" $LOG_FILE | grep "$(date +'%Y-%m-%d %H')" | \
    awk '{print $8}' | sort | uniq | wc -l
```

---

## Contact Information

### Emergency Contacts
- **System Down**: IT Support ext. 1234
- **Security Incident**: Security Team ext. 5678
- **Clinical Emergency**: Clinical Supervisor ext. 3456

### Support Escalation
1. **Level 1**: Help Desk (24/7) - ext. 1234
2. **Level 2**: System Administrator - ext. 2345
3. **Level 3**: Development Team - ext. 3456
4. **Level 4**: Vendor Support - 1-800-SUPPORT

### Email Contacts
- General Support: support@healthcare-triage.com
- Security Issues: security@healthcare-triage.com
- System Issues: sysadmin@healthcare-triage.com
- Development: dev-team@healthcare-triage.com

Remember: For patient safety issues, always escalate through clinical channels first, then notify IT support.