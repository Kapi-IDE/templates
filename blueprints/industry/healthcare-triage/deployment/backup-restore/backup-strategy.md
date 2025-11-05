# Healthcare Triage System - Backup and Recovery Strategy

## Table of Contents
1. [Backup Overview](#backup-overview)
2. [Database Backup](#database-backup)
3. [Application Backup](#application-backup)
4. [Configuration Backup](#configuration-backup)
5. [Recovery Procedures](#recovery-procedures)
6. [Disaster Recovery](#disaster-recovery)
7. [Testing and Validation](#testing-and-validation)
8. [Compliance Requirements](#compliance-requirements)

---

## Backup Overview

### Backup Objectives
- **Recovery Time Objective (RTO)**: Maximum 4 hours for full system recovery
- **Recovery Point Objective (RPO)**: Maximum 15 minutes of data loss
- **Data Retention**: 7 years for patient data, 1 year for system logs
- **Compliance**: HIPAA-compliant encrypted backups
- **Availability**: 99.9% system uptime including during backup operations

### Backup Types
1. **Full Backups**: Complete system backup (weekly)
2. **Incremental Backups**: Changed data only (daily)
3. **Transaction Log Backups**: Database transaction logs (every 15 minutes)
4. **Configuration Backups**: System and application configurations (daily)
5. **Critical Data Backups**: Real-time replication of critical patient data

### Storage Locations
- **Primary**: Local storage for immediate recovery
- **Secondary**: Offsite cloud storage for disaster recovery
- **Archive**: Long-term storage for compliance (7+ years)

---

## Database Backup

### PostgreSQL Backup Configuration

#### Full Database Backup (Daily)
```bash
#!/bin/bash
# /opt/scripts/db-backup-full.sh

# Configuration
DB_NAME="healthcare_triage"
DB_USER="backup_user"
DB_HOST="localhost"
BACKUP_DIR="/backup/database"
RETENTION_DAYS=30
ENCRYPTION_KEY="/etc/backup/encryption.key"

# Create backup directory
mkdir -p $BACKUP_DIR

# Generate timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/full_backup_$TIMESTAMP.sql"

# Perform backup
echo "Starting full database backup at $(date)"
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME \
    --verbose \
    --no-password \
    --format=custom \
    --compress=9 \
    --file=$BACKUP_FILE

# Verify backup integrity
echo "Verifying backup integrity..."
pg_restore --list $BACKUP_FILE > /dev/null
if [ $? -eq 0 ]; then
    echo "Backup verification successful"
else
    echo "Backup verification failed!"
    exit 1
fi

# Encrypt backup
echo "Encrypting backup..."
gpg --cipher-algo AES256 \
    --compress-algo 1 \
    --s2k-mode 3 \
    --s2k-digest-algo SHA512 \
    --s2k-count 65536 \
    --symmetric \
    --passphrase-file $ENCRYPTION_KEY \
    --output $BACKUP_FILE.gpg \
    $BACKUP_FILE

# Remove unencrypted backup
rm $BACKUP_FILE

# Upload to cloud storage
echo "Uploading to cloud storage..."
aws s3 cp $BACKUP_FILE.gpg \
    s3://healthcare-triage-backups/database/full/ \
    --storage-class STANDARD_IA \
    --server-side-encryption AES256

# Cleanup old backups
find $BACKUP_DIR -name "full_backup_*.sql.gpg" -mtime +$RETENTION_DAYS -delete

# Log backup completion
echo "Full database backup completed successfully at $(date)"
echo "Backup size: $(du -h $BACKUP_FILE.gpg | cut -f1)"

# Update monitoring
curl -X POST http://prometheus-pushgateway:9091/metrics/job/backup_job/instance/database \
    -d "backup_last_success_timestamp $(date +%s)"
```

#### Incremental Backup with WAL Archiving
```bash
#!/bin/bash
# /opt/scripts/db-backup-incremental.sh

# WAL archiving configuration
WAL_ARCHIVE_DIR="/backup/wal"
CLOUD_WAL_DIR="s3://healthcare-triage-backups/wal"

# Archive WAL file
WAL_FILE=$1
WAL_PATH=$2

# Copy to local archive
cp $WAL_PATH $WAL_ARCHIVE_DIR/$WAL_FILE

# Encrypt WAL file
gpg --cipher-algo AES256 \
    --symmetric \
    --passphrase-file /etc/backup/encryption.key \
    --output $WAL_ARCHIVE_DIR/$WAL_FILE.gpg \
    $WAL_ARCHIVE_DIR/$WAL_FILE

# Upload to cloud
aws s3 cp $WAL_ARCHIVE_DIR/$WAL_FILE.gpg $CLOUD_WAL_DIR/

# Remove unencrypted file
rm $WAL_ARCHIVE_DIR/$WAL_FILE

# Log WAL archiving
echo "$(date): WAL file $WAL_FILE archived successfully" >> /var/log/backup/wal-archive.log
```

### Database Configuration for Backup
```sql
-- PostgreSQL configuration for backup (postgresql.conf)
wal_level = replica
archive_mode = on
archive_command = '/opt/scripts/db-backup-incremental.sh %f %p'
archive_timeout = 900  -- 15 minutes
checkpoint_timeout = 5min
checkpoint_completion_target = 0.9
max_wal_size = 4GB
min_wal_size = 1GB

-- Backup monitoring views
CREATE VIEW backup_status AS
SELECT 
    pg_is_in_backup() as in_backup,
    pg_backup_start_time() as backup_start_time,
    pg_current_wal_lsn() as current_wal_lsn,
    pg_last_wal_replay_lsn() as last_replay_lsn;

-- Backup user with minimal privileges
CREATE ROLE backup_user WITH LOGIN;
GRANT CONNECT ON DATABASE healthcare_triage TO backup_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO backup_user;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO backup_user;
```

---

## Application Backup

### Application Code and Assets
```bash
#!/bin/bash
# /opt/scripts/app-backup.sh

APP_DIR="/opt/healthcare-triage"
BACKUP_DIR="/backup/application"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create application backup
echo "Starting application backup at $(date)"

# Backup application code
tar -czf $BACKUP_DIR/app_code_$TIMESTAMP.tar.gz \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='node_modules' \
    --exclude='.git' \
    $APP_DIR/

# Backup uploaded files and media
tar -czf $BACKUP_DIR/app_media_$TIMESTAMP.tar.gz \
    /var/lib/healthcare-triage/uploads/ \
    /var/lib/healthcare-triage/media/

# Backup logs (recent only)
tar -czf $BACKUP_DIR/app_logs_$TIMESTAMP.tar.gz \
    --newer-mtime="7 days ago" \
    /var/log/healthcare-triage/

# Encrypt backups
for file in $BACKUP_DIR/*_$TIMESTAMP.tar.gz; do
    gpg --cipher-algo AES256 \
        --symmetric \
        --passphrase-file /etc/backup/encryption.key \
        --output $file.gpg \
        $file
    rm $file
done

# Upload to cloud
aws s3 sync $BACKUP_DIR/ s3://healthcare-triage-backups/application/ \
    --exclude "*" \
    --include "*_$TIMESTAMP.tar.gz.gpg"

echo "Application backup completed at $(date)"
```

### Container Images Backup
```bash
#!/bin/bash
# /opt/scripts/container-backup.sh

REGISTRY="ghcr.io/healthcare-triage"
BACKUP_DIR="/backup/containers"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# List of images to backup
IMAGES=(
    "healthcare-triage-web:latest"
    "healthcare-triage-worker:latest"
    "healthcare-triage-ai:latest"
    "postgres:13"
    "redis:6"
    "nginx:alpine"
)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup each image
for image in "${IMAGES[@]}"; do
    echo "Backing up $image..."
    
    # Save image as tar
    docker save $REGISTRY/$image | gzip > $BACKUP_DIR/${image//\//_}_$TIMESTAMP.tar.gz
    
    # Encrypt image backup
    gpg --cipher-algo AES256 \
        --symmetric \
        --passphrase-file /etc/backup/encryption.key \
        --output $BACKUP_DIR/${image//\//_}_$TIMESTAMP.tar.gz.gpg \
        $BACKUP_DIR/${image//\//_}_$TIMESTAMP.tar.gz
    
    # Remove unencrypted file
    rm $BACKUP_DIR/${image//\//_}_$TIMESTAMP.tar.gz
done

# Upload to cloud storage
aws s3 sync $BACKUP_DIR/ s3://healthcare-triage-backups/containers/ \
    --include "*_$TIMESTAMP.tar.gz.gpg"

echo "Container backup completed at $(date)"
```

---

## Configuration Backup

### System Configuration Backup
```bash
#!/bin/bash
# /opt/scripts/config-backup.sh

CONFIG_DIRS=(
    "/etc/healthcare-triage"
    "/etc/nginx/sites-available"
    "/etc/systemd/system"
    "/etc/postgresql"
    "/etc/redis"
    "/etc/ssl/certs"
    "/etc/letsencrypt"
)

BACKUP_DIR="/backup/configuration"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create configuration backup
echo "Starting configuration backup at $(date)"

# Backup system configurations
tar -czf $BACKUP_DIR/system_config_$TIMESTAMP.tar.gz \
    "${CONFIG_DIRS[@]}" \
    2>/dev/null

# Backup Kubernetes configurations
kubectl get all,configmaps,secrets,ingress,pv,pvc \
    --all-namespaces \
    -o yaml > $BACKUP_DIR/k8s_config_$TIMESTAMP.yaml

# Backup Docker Compose files
cp -r /opt/healthcare-triage/docker-compose*.yml $BACKUP_DIR/
tar -czf $BACKUP_DIR/docker_config_$TIMESTAMP.tar.gz \
    $BACKUP_DIR/docker-compose*.yml

# Encrypt configuration backups
for file in $BACKUP_DIR/*_$TIMESTAMP.*; do
    gpg --cipher-algo AES256 \
        --symmetric \
        --passphrase-file /etc/backup/encryption.key \
        --output $file.gpg \
        $file
    rm $file
done

# Upload to cloud
aws s3 sync $BACKUP_DIR/ s3://healthcare-triage-backups/configuration/ \
    --include "*_$TIMESTAMP.*.gpg"

echo "Configuration backup completed at $(date)"
```

### Environment and Secrets Backup
```bash
#!/bin/bash
# /opt/scripts/secrets-backup.sh

SECRETS_DIR="/backup/secrets"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
VAULT_ADDR="https://vault.healthcare-triage.com"

# Create secrets backup directory
mkdir -p $SECRETS_DIR

# Backup from HashiCorp Vault
vault kv get -format=json secret/healthcare-triage > $SECRETS_DIR/vault_secrets_$TIMESTAMP.json

# Backup Kubernetes secrets
kubectl get secrets --all-namespaces -o yaml > $SECRETS_DIR/k8s_secrets_$TIMESTAMP.yaml

# Backup environment files (sanitized)
cp /opt/healthcare-triage/.env.production $SECRETS_DIR/env_production_$TIMESTAMP
cp /opt/healthcare-triage/.env.staging $SECRETS_DIR/env_staging_$TIMESTAMP

# Encrypt secrets (double encryption for extra security)
for file in $SECRETS_DIR/*_$TIMESTAMP*; do
    # First encryption with primary key
    gpg --cipher-algo AES256 \
        --symmetric \
        --passphrase-file /etc/backup/encryption.key \
        --output $file.gpg1 \
        $file
    
    # Second encryption with secondary key
    gpg --cipher-algo AES256 \
        --symmetric \
        --passphrase-file /etc/backup/encryption2.key \
        --output $file.gpg \
        $file.gpg1
    
    # Remove intermediate files
    rm $file $file.gpg1
done

# Store in highly secure cloud storage
aws s3 cp $SECRETS_DIR/ s3://healthcare-triage-secrets-backup/secrets/ \
    --recursive \
    --storage-class GLACIER \
    --server-side-encryption aws:kms \
    --ssm-kms-key-id alias/healthcare-triage-backup-key

echo "Secrets backup completed at $(date)"
```

---

## Recovery Procedures

### Database Recovery

#### Point-in-Time Recovery
```bash
#!/bin/bash
# /opt/scripts/db-recovery-pit.sh

TARGET_TIME="$1"  # Format: 2024-01-15 14:30:00
RECOVERY_DIR="/recovery/database"
BASE_BACKUP_FILE="$2"

if [ -z "$TARGET_TIME" ] || [ -z "$BASE_BACKUP_FILE" ]; then
    echo "Usage: $0 'YYYY-MM-DD HH:MM:SS' /path/to/base/backup.sql.gpg"
    exit 1
fi

echo "Starting point-in-time recovery to $TARGET_TIME"

# Stop PostgreSQL
systemctl stop postgresql

# Create recovery directory
mkdir -p $RECOVERY_DIR
chown postgres:postgres $RECOVERY_DIR

# Decrypt and restore base backup
gpg --decrypt --passphrase-file /etc/backup/encryption.key \
    $BASE_BACKUP_FILE | pg_restore \
    --dbname=healthcare_triage_recovery \
    --create \
    --verbose

# Download and decrypt WAL files
aws s3 sync s3://healthcare-triage-backups/wal/ /tmp/wal_recovery/
for file in /tmp/wal_recovery/*.gpg; do
    gpg --decrypt --passphrase-file /etc/backup/encryption.key \
        --output ${file%.gpg} $file
done

# Configure recovery
cat > $RECOVERY_DIR/recovery.conf << EOF
restore_command = 'cp /tmp/wal_recovery/%f %p'
recovery_target_time = '$TARGET_TIME'
recovery_target_timeline = 'latest'
EOF

# Start recovery
sudo -u postgres pg_ctl start -D $RECOVERY_DIR

echo "Point-in-time recovery initiated. Monitor logs for completion."
```

#### Full Database Recovery
```bash
#!/bin/bash
# /opt/scripts/db-recovery-full.sh

BACKUP_FILE="$1"
TARGET_DB="healthcare_triage"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 /path/to/backup.sql.gpg"
    exit 1
fi

echo "Starting full database recovery from $BACKUP_FILE"

# Create recovery database
sudo -u postgres createdb ${TARGET_DB}_recovery

# Decrypt and restore backup
gpg --decrypt --passphrase-file /etc/backup/encryption.key \
    $BACKUP_FILE | pg_restore \
    --dbname=${TARGET_DB}_recovery \
    --verbose \
    --no-owner \
    --no-acl

# Verify recovery
sudo -u postgres psql -d ${TARGET_DB}_recovery -c "\dt"

echo "Database recovery completed. Review and promote when ready."
echo "To promote: ALTER DATABASE ${TARGET_DB}_recovery RENAME TO ${TARGET_DB};"
```

### Application Recovery
```bash
#!/bin/bash
# /opt/scripts/app-recovery.sh

BACKUP_DATE="$1"
RECOVERY_DIR="/recovery/application"

if [ -z "$BACKUP_DATE" ]; then
    echo "Usage: $0 YYYYMMDD_HHMMSS"
    exit 1
fi

echo "Starting application recovery for backup date: $BACKUP_DATE"

# Create recovery directory
mkdir -p $RECOVERY_DIR

# Download backups from cloud
aws s3 cp s3://healthcare-triage-backups/application/app_code_${BACKUP_DATE}.tar.gz.gpg \
    $RECOVERY_DIR/
aws s3 cp s3://healthcare-triage-backups/application/app_media_${BACKUP_DATE}.tar.gz.gpg \
    $RECOVERY_DIR/

# Decrypt and extract backups
for file in $RECOVERY_DIR/*.gpg; do
    gpg --decrypt --passphrase-file /etc/backup/encryption.key \
        --output ${file%.gpg} $file
    
    # Extract tar file
    tar -xzf ${file%.gpg} -C $RECOVERY_DIR/
done

# Stop application services
systemctl stop healthcare-triage
systemctl stop celery-worker

# Restore application code
cp -r $RECOVERY_DIR/opt/healthcare-triage/* /opt/healthcare-triage/

# Restore media files
cp -r $RECOVERY_DIR/var/lib/healthcare-triage/* /var/lib/healthcare-triage/

# Set proper permissions
chown -R healthcare-triage:healthcare-triage /opt/healthcare-triage/
chown -R healthcare-triage:healthcare-triage /var/lib/healthcare-triage/

# Install dependencies
cd /opt/healthcare-triage
pip install -r requirements.txt
npm install

# Start services
systemctl start healthcare-triage
systemctl start celery-worker

echo "Application recovery completed"
```

---

## Disaster Recovery

### Disaster Recovery Plan

#### RTO/RPO Targets
- **Critical Systems**: RTO 2 hours, RPO 15 minutes
- **Non-Critical Systems**: RTO 8 hours, RPO 4 hours
- **Archive Data**: RTO 24 hours, RPO 24 hours

#### DR Site Configuration
```bash
#!/bin/bash
# /opt/scripts/dr-site-setup.sh

DR_REGION="us-west-2"
PRIMARY_REGION="us-east-1"

echo "Setting up disaster recovery site in $DR_REGION"

# Create DR infrastructure
terraform apply -var-file="dr-$DR_REGION.tfvars" \
    -target=module.dr_infrastructure

# Configure database replication
aws rds create-db-cluster-snapshot \
    --db-cluster-identifier healthcare-triage-primary \
    --db-cluster-snapshot-identifier dr-snapshot-$(date +%Y%m%d)

aws rds restore-db-cluster-from-snapshot \
    --db-cluster-identifier healthcare-triage-dr \
    --snapshot-identifier dr-snapshot-$(date +%Y%m%d) \
    --region $DR_REGION

# Set up cross-region replication for backups
aws s3api put-bucket-replication \
    --bucket healthcare-triage-backups \
    --replication-configuration file://replication-config.json

echo "DR site setup completed"
```

#### Failover Procedure
```bash
#!/bin/bash
# /opt/scripts/disaster-failover.sh

DR_ENDPOINT="https://dr.healthcare-triage.com"
DNS_RECORD="healthcare-triage.com"

echo "DISASTER RECOVERY FAILOVER INITIATED"
echo "Time: $(date)"

# 1. Verify primary site is down
if curl -f --max-time 10 https://healthcare-triage.com/api/health; then
    echo "Primary site appears to be operational. Aborting failover."
    exit 1
fi

# 2. Activate DR database
aws rds modify-db-cluster \
    --db-cluster-identifier healthcare-triage-dr \
    --apply-immediately

# 3. Update DNS to point to DR site
aws route53 change-resource-record-sets \
    --hosted-zone-id Z123456789 \
    --change-batch file://dr-dns-change.json

# 4. Start DR application services
kubectl apply -f k8s/dr-deployment.yaml

# 5. Verify DR site functionality
sleep 60
if curl -f $DR_ENDPOINT/api/health; then
    echo "DR site is operational"
else
    echo "DR site health check failed!"
    exit 1
fi

# 6. Notify stakeholders
curl -X POST $SLACK_WEBHOOK \
    -H 'Content-type: application/json' \
    --data '{"text":"🚨 DISASTER RECOVERY ACTIVATED - Primary site failure detected, failed over to DR site"}'

echo "Disaster recovery failover completed successfully"
```

#### Failback Procedure
```bash
#!/bin/bash
# /opt/scripts/disaster-failback.sh

echo "DISASTER RECOVERY FAILBACK INITIATED"
echo "Time: $(date)"

# 1. Verify primary site is restored
if ! curl -f --max-time 10 https://primary.healthcare-triage.com/api/health; then
    echo "Primary site is not ready for failback"
    exit 1
fi

# 2. Sync data from DR to primary
pg_dump -h dr-database-endpoint healthcare_triage | \
    psql -h primary-database-endpoint healthcare_triage

# 3. Update DNS back to primary
aws route53 change-resource-record-sets \
    --hosted-zone-id Z123456789 \
    --change-batch file://primary-dns-change.json

# 4. Gracefully shutdown DR services
kubectl delete -f k8s/dr-deployment.yaml

# 5. Verify primary site functionality
sleep 60
if curl -f https://healthcare-triage.com/api/health; then
    echo "Primary site is operational"
else
    echo "Primary site health check failed!"
    exit 1
fi

echo "Disaster recovery failback completed successfully"
```

---

## Testing and Validation

### Backup Validation Scripts
```bash
#!/bin/bash
# /opt/scripts/backup-validation.sh

BACKUP_DIR="/backup"
TEST_DB="healthcare_triage_test"

echo "Starting backup validation at $(date)"

# Test database backup integrity
LATEST_DB_BACKUP=$(ls -t $BACKUP_DIR/database/full_backup_*.sql.gpg | head -1)

if [ -n "$LATEST_DB_BACKUP" ]; then
    echo "Testing database backup: $LATEST_DB_BACKUP"
    
    # Decrypt and test restore
    gpg --decrypt --passphrase-file /etc/backup/encryption.key \
        $LATEST_DB_BACKUP | pg_restore \
        --dbname=$TEST_DB \
        --create \
        --verbose \
        --exit-on-error
    
    if [ $? -eq 0 ]; then
        echo "✓ Database backup validation successful"
        
        # Test data integrity
        RECORD_COUNT=$(psql -d $TEST_DB -t -c "SELECT COUNT(*) FROM patients;")
        echo "Test database contains $RECORD_COUNT patient records"
        
        # Cleanup test database
        dropdb $TEST_DB
    else
        echo "✗ Database backup validation failed"
        exit 1
    fi
fi

# Test application backup integrity
LATEST_APP_BACKUP=$(ls -t $BACKUP_DIR/application/app_code_*.tar.gz.gpg | head -1)

if [ -n "$LATEST_APP_BACKUP" ]; then
    echo "Testing application backup: $LATEST_APP_BACKUP"
    
    # Decrypt and extract to test directory
    TEST_DIR="/tmp/backup_test_$(date +%s)"
    mkdir -p $TEST_DIR
    
    gpg --decrypt --passphrase-file /etc/backup/encryption.key \
        $LATEST_APP_BACKUP | tar -xz -C $TEST_DIR
    
    if [ -f "$TEST_DIR/opt/healthcare-triage/app.py" ]; then
        echo "✓ Application backup validation successful"
        rm -rf $TEST_DIR
    else
        echo "✗ Application backup validation failed"
        rm -rf $TEST_DIR
        exit 1
    fi
fi

echo "Backup validation completed successfully at $(date)"
```

### Recovery Testing
```bash
#!/bin/bash
# /opt/scripts/recovery-test.sh

TEST_ENV="test-recovery"
BACKUP_DATE="$1"

if [ -z "$BACKUP_DATE" ]; then
    echo "Usage: $0 YYYYMMDD_HHMMSS"
    exit 1
fi

echo "Starting recovery test for backup date: $BACKUP_DATE"

# Create isolated test environment
docker-compose -f docker-compose.recovery-test.yml up -d

# Wait for services to start
sleep 30

# Perform recovery test
./db-recovery-full.sh /backup/database/full_backup_${BACKUP_DATE}.sql.gpg
./app-recovery.sh $BACKUP_DATE

# Run functional tests
cd /opt/healthcare-triage
python -m pytest tests/functional/ -v

# Generate recovery test report
cat > /tmp/recovery-test-report.txt << EOF
Recovery Test Report
Date: $(date)
Backup Date: $BACKUP_DATE
Test Environment: $TEST_ENV

Database Recovery: $([ $? -eq 0 ] && echo "PASSED" || echo "FAILED")
Application Recovery: $([ $? -eq 0 ] && echo "PASSED" || echo "FAILED")
Functional Tests: $([ $? -eq 0 ] && echo "PASSED" || echo "FAILED")

EOF

# Cleanup test environment
docker-compose -f docker-compose.recovery-test.yml down

echo "Recovery test completed. Report available at /tmp/recovery-test-report.txt"
```

---

## Compliance Requirements

### HIPAA Compliance for Backups

#### Encryption Requirements
- **At Rest**: AES-256 encryption for all backup files
- **In Transit**: TLS 1.3 for all data transfers
- **Key Management**: HSM-backed key storage and rotation

#### Access Controls
```bash
# Backup access control script
#!/bin/bash
# /opt/scripts/backup-access-control.sh

# Create backup user with minimal privileges
useradd -r -s /bin/false backup_user

# Set up backup directory permissions
chown root:backup_user /backup
chmod 750 /backup

# Configure sudo access for backup operations only
echo "backup_user ALL=(postgres) NOPASSWD: /usr/bin/pg_dump, /usr/bin/pg_restore" >> /etc/sudoers.d/backup

# Set up encryption key permissions
chown root:backup_user /etc/backup/encryption.key
chmod 640 /etc/backup/encryption.key
```

#### Audit Requirements
```bash
#!/bin/bash
# /opt/scripts/backup-audit.sh

AUDIT_LOG="/var/log/backup/audit.log"

# Log backup operations
log_backup_event() {
    local operation="$1"
    local result="$2"
    local details="$3"
    
    echo "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ) | $USER | $operation | $result | $details" >> $AUDIT_LOG
}

# Monitor backup access
auditctl -w /backup -p rwxa -k backup_access
auditctl -w /etc/backup -p rwxa -k backup_config
```

### Data Retention Policy Implementation
```sql
-- Database views for retention policy enforcement
CREATE VIEW data_retention_status AS
SELECT 
    'patients' as table_name,
    COUNT(*) as total_records,
    COUNT(*) FILTER (WHERE created_at < NOW() - INTERVAL '7 years') as overdue_records,
    MIN(created_at) as oldest_record,
    MAX(created_at) as newest_record
FROM patients
UNION ALL
SELECT 
    'audit_logs' as table_name,
    COUNT(*) as total_records,
    COUNT(*) FILTER (WHERE timestamp < NOW() - INTERVAL '7 years') as overdue_records,
    MIN(timestamp) as oldest_record,
    MAX(timestamp) as newest_record
FROM audit_logs;

-- Automated data archival
CREATE OR REPLACE FUNCTION archive_old_data()
RETURNS void AS $$
BEGIN
    -- Archive patients older than 7 years
    INSERT INTO patients_archive 
    SELECT * FROM patients 
    WHERE last_activity < NOW() - INTERVAL '7 years';
    
    DELETE FROM patients 
    WHERE last_activity < NOW() - INTERVAL '7 years';
    
    -- Archive audit logs older than 7 years  
    INSERT INTO audit_logs_archive
    SELECT * FROM audit_logs
    WHERE timestamp < NOW() - INTERVAL '7 years';
    
    DELETE FROM audit_logs
    WHERE timestamp < NOW() - INTERVAL '7 years';
    
    -- Log archival operation
    INSERT INTO data_retention_log (operation, timestamp, records_archived)
    VALUES ('automated_archive', NOW(), ROW_COUNT());
END;
$$ LANGUAGE plpgsql;

-- Schedule automated archival
SELECT cron.schedule('archive-old-data', '0 2 * * 0', 'SELECT archive_old_data();');
```

---

## Monitoring and Alerting

### Backup Monitoring
```yaml
# Prometheus rules for backup monitoring
groups:
  - name: backup_monitoring
    rules:
      - alert: BackupFailure
        expr: time() - backup_last_success_timestamp > 86400
        for: 0m
        labels:
          severity: critical
        annotations:
          summary: "Backup has failed"
          description: "No successful backup in the last 24 hours"

      - alert: BackupSizeAnomaly
        expr: backup_size_bytes < 0.8 * backup_size_bytes offset 1d
        for: 0m
        labels:
          severity: warning
        annotations:
          summary: "Backup size significantly smaller than expected"
          description: "Current backup size is {{ $value }} bytes, expected around {{ $value | offset 1d }} bytes"
```

Remember: Regular testing of backup and recovery procedures is essential for ensuring system reliability and compliance with healthcare data protection requirements.