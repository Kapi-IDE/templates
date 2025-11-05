-- Healthcare AI Triage System - Production Database Schema
-- PostgreSQL 15+ with HIPAA compliance extensions
-- 
-- This schema provides:
-- - Comprehensive patient and triage management
-- - Multi-agent AI interaction tracking
-- - Audit logging for HIPAA compliance
-- - Performance optimization for healthcare workflows
-- - Scalable design for 1000+ concurrent users

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";           -- UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";            -- Encryption functions
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";  -- Query performance tracking
CREATE EXTENSION IF NOT EXISTS "pg_trgm";             -- Text similarity search

-- Create custom types for healthcare-specific data
CREATE TYPE esi_level AS ENUM ('1', '2', '3', '4', '5');
CREATE TYPE gender_type AS ENUM ('male', 'female', 'other', 'unknown');
CREATE TYPE session_status AS ENUM ('active', 'completed', 'escalated', 'transferred', 'cancelled');
CREATE TYPE agent_type AS ENUM ('intake', 'triage', 'knowledge', 'escalation');
CREATE TYPE interaction_type AS ENUM ('question', 'assessment', 'information', 'action', 'error');
CREATE TYPE arrival_method AS ENUM ('walk_in', 'ambulance', 'wheelchair', 'stretcher');
CREATE TYPE department_type AS ENUM ('emergency', 'urgent_care', 'fast_track');
CREATE TYPE user_role AS ENUM ('nurse', 'physician', 'resident', 'tech', 'admin', 'manager');

-- ==============================================================================
-- PATIENT MANAGEMENT TABLES
-- ==============================================================================

-- Core patient information with encrypted sensitive data
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    medical_record_number VARCHAR(50) UNIQUE NOT NULL,
    
    -- Encrypted demographic information (HIPAA compliant)
    encrypted_demographics JSONB NOT NULL,
    
    -- Non-sensitive metadata
    active_status BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_mrn_format CHECK (medical_record_number ~ '^MRN-\d{4}-\d{6}$')
);

-- Patient medical history and ongoing care information
CREATE TABLE patient_medical_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    
    -- Medical information (encrypted)
    encrypted_medical_data JSONB NOT NULL,
    
    -- Metadata
    data_type VARCHAR(50) NOT NULL, -- 'allergies', 'medications', 'conditions', 'procedures'
    effective_date DATE,
    end_date DATE,
    provider_id UUID,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_date_range CHECK (end_date IS NULL OR end_date >= effective_date)
);

-- Emergency contacts for patients
CREATE TABLE patient_emergency_contacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    
    -- Contact information (encrypted)
    encrypted_contact_data JSONB NOT NULL,
    
    -- Priority and relationship
    priority_order INTEGER DEFAULT 1,
    relationship VARCHAR(50) NOT NULL,
    active_status BOOLEAN DEFAULT true,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==============================================================================
-- USER MANAGEMENT AND AUTHENTICATION
-- ==============================================================================

-- Healthcare system users (nurses, doctors, administrators)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    
    -- User identification
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    
    -- Role and permissions
    role user_role NOT NULL,
    department department_type,
    license_number VARCHAR(100),
    
    -- Authentication
    password_hash VARCHAR(255),
    last_login TIMESTAMP WITH TIME ZONE,
    failed_login_attempts INTEGER DEFAULT 0,
    account_locked_until TIMESTAMP WITH TIME ZONE,
    
    -- Status
    active_status BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_email_format CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- User sessions for authentication tracking
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Session information
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    
    -- Timing
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Status
    active_status BOOLEAN DEFAULT true
);

-- ==============================================================================
-- TRIAGE SESSION MANAGEMENT
-- ==============================================================================

-- Core triage sessions
CREATE TABLE triage_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id),
    
    -- Session metadata
    department department_type NOT NULL,
    triage_nurse_id UUID NOT NULL REFERENCES users(id),
    attending_physician_id UUID REFERENCES users(id),
    
    -- Clinical information
    chief_complaint TEXT NOT NULL,
    arrival_method arrival_method NOT NULL,
    esi_level esi_level,
    priority_score INTEGER,
    
    -- Timing
    session_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    session_end TIMESTAMP WITH TIME ZONE,
    estimated_wait_time INTEGER, -- minutes
    
    -- Status
    status session_status DEFAULT 'active',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_session_duration CHECK (session_end IS NULL OR session_end >= session_start),
    CONSTRAINT valid_priority_score CHECK (priority_score IS NULL OR (priority_score >= 1 AND priority_score <= 100))
);

-- Vital signs and physical assessment data
CREATE TABLE vital_signs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES triage_sessions(id) ON DELETE CASCADE,
    
    -- Vital signs measurements
    temperature DECIMAL(4,1),           -- Fahrenheit
    blood_pressure_systolic INTEGER,    -- mmHg
    blood_pressure_diastolic INTEGER,   -- mmHg
    heart_rate INTEGER,                 -- BPM
    respiratory_rate INTEGER,           -- Breaths per minute
    oxygen_saturation INTEGER,          -- Percentage
    pain_scale INTEGER,                 -- 0-10 scale
    
    -- Physical measurements
    weight DECIMAL(5,1),                -- Pounds
    height DECIMAL(4,1),                -- Inches
    
    -- Metadata
    measured_by UUID REFERENCES users(id),
    measurement_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    device_id VARCHAR(100),
    notes TEXT,
    
    -- Constraints
    CONSTRAINT valid_temperature CHECK (temperature IS NULL OR (temperature >= 90.0 AND temperature <= 110.0)),
    CONSTRAINT valid_bp_systolic CHECK (blood_pressure_systolic IS NULL OR (blood_pressure_systolic >= 60 AND blood_pressure_systolic <= 300)),
    CONSTRAINT valid_bp_diastolic CHECK (blood_pressure_diastolic IS NULL OR (blood_pressure_diastolic >= 30 AND blood_pressure_diastolic <= 200)),
    CONSTRAINT valid_heart_rate CHECK (heart_rate IS NULL OR (heart_rate >= 30 AND heart_rate <= 250)),
    CONSTRAINT valid_respiratory_rate CHECK (respiratory_rate IS NULL OR (respiratory_rate >= 8 AND respiratory_rate <= 60)),
    CONSTRAINT valid_oxygen_saturation CHECK (oxygen_saturation IS NULL OR (oxygen_saturation >= 70 AND oxygen_saturation <= 100)),
    CONSTRAINT valid_pain_scale CHECK (pain_scale IS NULL OR (pain_scale >= 0 AND pain_scale <= 10))
);

-- Medical assessments and clinical observations
CREATE TABLE medical_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES triage_sessions(id) ON DELETE CASCADE,
    
    -- Assessment data (structured and encrypted)
    symptoms JSONB,
    medical_history JSONB,
    current_medications JSONB,
    allergies JSONB,
    
    -- Assessment scores and ratings
    assessment_scores JSONB,
    risk_factors JSONB,
    
    -- Clinical notes
    clinical_notes TEXT,
    differential_diagnosis TEXT[],
    
    -- Metadata
    assessed_by UUID NOT NULL REFERENCES users(id),
    assessment_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==============================================================================
-- AI AGENT INTERACTION TRACKING
-- ==============================================================================

-- AI agent interactions and responses
CREATE TABLE agent_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES triage_sessions(id) ON DELETE CASCADE,
    
    -- Agent information
    agent_type agent_type NOT NULL,
    agent_version VARCHAR(50),
    
    -- Interaction data
    input_data JSONB NOT NULL,
    output_data JSONB NOT NULL,
    interaction_type interaction_type NOT NULL,
    
    -- Performance metrics
    processing_time_ms INTEGER NOT NULL,
    confidence_score DECIMAL(3,2),
    tokens_used INTEGER,
    
    -- Context and metadata
    context_data JSONB,
    error_data JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_confidence_score CHECK (confidence_score IS NULL OR (confidence_score >= 0.0 AND confidence_score <= 1.0)),
    CONSTRAINT valid_processing_time CHECK (processing_time_ms > 0)
);

-- Agent performance monitoring and analytics
CREATE TABLE agent_performance_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Time period and agent
    metric_date DATE NOT NULL,
    agent_type agent_type NOT NULL,
    
    -- Performance metrics
    total_interactions INTEGER DEFAULT 0,
    average_response_time_ms INTEGER,
    average_confidence_score DECIMAL(3,2),
    success_rate DECIMAL(5,2),
    error_rate DECIMAL(5,2),
    
    -- Quality metrics
    clinical_accuracy_score DECIMAL(3,2),
    user_satisfaction_score DECIMAL(3,2),
    
    -- Resource usage
    total_tokens_used INTEGER DEFAULT 0,
    total_processing_time_ms BIGINT DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(metric_date, agent_type)
);

-- ==============================================================================
-- CLINICAL PROTOCOLS AND KNOWLEDGE BASE
-- ==============================================================================

-- Clinical protocols and treatment guidelines
CREATE TABLE clinical_protocols (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Protocol identification
    protocol_name VARCHAR(200) NOT NULL,
    protocol_code VARCHAR(50) UNIQUE NOT NULL,
    specialty VARCHAR(100),
    
    -- Protocol content
    description TEXT,
    protocol_steps JSONB NOT NULL,
    decision_criteria JSONB,
    contraindications TEXT[],
    
    -- Metadata
    version VARCHAR(20) NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    evidence_level VARCHAR(10), -- A, B, C, D
    
    -- Source information
    source_organization VARCHAR(200),
    source_url TEXT,
    reference_citations TEXT[],
    
    -- Status
    active_status BOOLEAN DEFAULT true,
    approved_by UUID REFERENCES users(id),
    approval_date DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_date_range CHECK (expiration_date IS NULL OR expiration_date > effective_date)
);

-- Drug interaction database
CREATE TABLE drug_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Drug information
    drug_a_name VARCHAR(200) NOT NULL,
    drug_a_generic VARCHAR(200),
    drug_b_name VARCHAR(200) NOT NULL,
    drug_b_generic VARCHAR(200),
    
    -- Interaction details
    interaction_type VARCHAR(100) NOT NULL, -- contraindicated, major, moderate, minor
    severity_level VARCHAR(20) NOT NULL,    -- critical, high, medium, low
    mechanism TEXT,
    clinical_effect TEXT,
    
    -- Management guidance
    management_recommendation TEXT,
    monitoring_parameters TEXT[],
    alternative_medications TEXT[],
    
    -- Evidence and references
    evidence_level VARCHAR(10),
    reference_citations TEXT[],
    
    -- Metadata
    active_status BOOLEAN DEFAULT true,
    last_reviewed DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Medical knowledge base for AI agents
CREATE TABLE knowledge_base_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Content classification
    content_type VARCHAR(100) NOT NULL, -- protocol, guideline, reference, symptom, diagnosis
    category VARCHAR(100),
    subcategory VARCHAR(100),
    
    -- Content
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    structured_data JSONB,
    
    -- Search and retrieval
    keywords TEXT[],
    tags TEXT[],
    search_vector tsvector,
    
    -- Quality and validation
    accuracy_score DECIMAL(3,2),
    review_status VARCHAR(50) DEFAULT 'pending',
    reviewed_by UUID REFERENCES users(id),
    review_date DATE,
    
    -- Source and metadata
    source_type VARCHAR(100),
    source_reference TEXT,
    version VARCHAR(20),
    
    active_status BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==============================================================================
-- AUDIT LOGGING AND COMPLIANCE
-- ==============================================================================

-- Comprehensive audit log for HIPAA compliance
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- User and session information
    user_id UUID REFERENCES users(id),
    session_id UUID,
    patient_id UUID REFERENCES patients(id),
    
    -- Action details
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    
    -- Request details
    http_method VARCHAR(10),
    endpoint VARCHAR(500),
    ip_address INET,
    user_agent TEXT,
    
    -- Data access details
    data_accessed JSONB,
    data_modified JSONB,
    
    -- Result information
    status_code INTEGER,
    error_message TEXT,
    
    -- Timing
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processing_time_ms INTEGER,
    
    -- Additional metadata
    additional_metadata JSONB
);

-- System security events
CREATE TABLE security_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Event classification
    event_type VARCHAR(100) NOT NULL, -- login_failure, suspicious_access, data_breach, etc.
    severity_level VARCHAR(20) NOT NULL, -- critical, high, medium, low, info
    
    -- Event details
    description TEXT NOT NULL,
    affected_user_id UUID REFERENCES users(id),
    affected_resource VARCHAR(200),
    
    -- Network information
    source_ip INET,
    user_agent TEXT,
    
    -- Response and resolution
    response_action VARCHAR(200),
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by UUID REFERENCES users(id),
    
    -- Metadata
    event_data JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==============================================================================
-- SYSTEM CONFIGURATION AND SETTINGS
-- ==============================================================================

-- System configuration parameters
CREATE TABLE system_configuration (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Configuration identification
    config_key VARCHAR(200) UNIQUE NOT NULL,
    config_value JSONB NOT NULL,
    
    -- Metadata
    description TEXT,
    category VARCHAR(100),
    data_type VARCHAR(50), -- string, integer, boolean, json, array
    
    -- Validation
    validation_rules JSONB,
    is_sensitive BOOLEAN DEFAULT false,
    
    -- Change tracking
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Feature flags for controlled rollouts
CREATE TABLE feature_flags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Flag identification
    flag_name VARCHAR(200) UNIQUE NOT NULL,
    description TEXT,
    
    -- Flag configuration
    is_enabled BOOLEAN DEFAULT false,
    rollout_percentage DECIMAL(5,2) DEFAULT 0.0,
    target_groups TEXT[],
    
    -- Conditions
    conditions JSONB,
    
    -- Metadata
    created_by UUID REFERENCES users(id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_rollout_percentage CHECK (rollout_percentage >= 0.0 AND rollout_percentage <= 100.0)
);

-- ==============================================================================
-- PERFORMANCE OPTIMIZATION INDEXES
-- ==============================================================================

-- Patient table indexes
CREATE INDEX idx_patients_mrn ON patients(medical_record_number);
CREATE INDEX idx_patients_created_at ON patients(created_at);
CREATE INDEX idx_patients_active_status ON patients(active_status) WHERE active_status = true;

-- User table indexes
CREATE INDEX idx_users_employee_id ON users(employee_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role_department ON users(role, department);
CREATE INDEX idx_users_active_status ON users(active_status) WHERE active_status = true;

-- Triage session indexes
CREATE INDEX idx_triage_sessions_patient_id ON triage_sessions(patient_id);
CREATE INDEX idx_triage_sessions_nurse ON triage_sessions(triage_nurse_id);
CREATE INDEX idx_triage_sessions_status ON triage_sessions(status);
CREATE INDEX idx_triage_sessions_department ON triage_sessions(department);
CREATE INDEX idx_triage_sessions_esi_level ON triage_sessions(esi_level);
CREATE INDEX idx_triage_sessions_start_time ON triage_sessions(session_start);
CREATE INDEX idx_triage_sessions_active ON triage_sessions(status, session_start) WHERE status = 'active';

-- Agent interaction indexes
CREATE INDEX idx_agent_interactions_session_id ON agent_interactions(session_id);
CREATE INDEX idx_agent_interactions_agent_type ON agent_interactions(agent_type);
CREATE INDEX idx_agent_interactions_created_at ON agent_interactions(created_at);
CREATE INDEX idx_agent_interactions_performance ON agent_interactions(agent_type, processing_time_ms, confidence_score);

-- Audit log indexes
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_patient_id ON audit_logs(patient_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);

-- Knowledge base indexes
CREATE INDEX idx_knowledge_base_content_type ON knowledge_base_entries(content_type);
CREATE INDEX idx_knowledge_base_search_vector ON knowledge_base_entries USING gin(search_vector);
CREATE INDEX idx_knowledge_base_tags ON knowledge_base_entries USING gin(tags);
CREATE INDEX idx_knowledge_base_active ON knowledge_base_entries(active_status) WHERE active_status = true;

-- Clinical protocol indexes
CREATE INDEX idx_clinical_protocols_code ON clinical_protocols(protocol_code);
CREATE INDEX idx_clinical_protocols_specialty ON clinical_protocols(specialty);
CREATE INDEX idx_clinical_protocols_active ON clinical_protocols(active_status) WHERE active_status = true;

-- Drug interaction indexes
CREATE INDEX idx_drug_interactions_drug_a ON drug_interactions(drug_a_name);
CREATE INDEX idx_drug_interactions_drug_b ON drug_interactions(drug_b_name);
CREATE INDEX idx_drug_interactions_severity ON drug_interactions(severity_level);
CREATE INDEX idx_drug_interactions_active ON drug_interactions(active_status) WHERE active_status = true;

-- Composite indexes for common queries
CREATE INDEX idx_active_sessions_by_nurse ON triage_sessions(triage_nurse_id, status, session_start) 
    WHERE status = 'active';
CREATE INDEX idx_recent_interactions_by_agent ON agent_interactions(agent_type, created_at DESC);
CREATE INDEX idx_patient_sessions_chronological ON triage_sessions(patient_id, session_start DESC);

-- ==============================================================================
-- DATABASE FUNCTIONS AND TRIGGERS
-- ==============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for automatic timestamp updates
CREATE TRIGGER update_patients_updated_at BEFORE UPDATE ON patients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_triage_sessions_updated_at BEFORE UPDATE ON triage_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_medical_assessments_updated_at BEFORE UPDATE ON medical_assessments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_clinical_protocols_updated_at BEFORE UPDATE ON clinical_protocols FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_knowledge_base_entries_updated_at BEFORE UPDATE ON knowledge_base_entries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to maintain search vectors for knowledge base
CREATE OR REPLACE FUNCTION update_knowledge_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.content, '') || ' ' || array_to_string(NEW.keywords, ' '));
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_knowledge_search_vector_trigger 
    BEFORE INSERT OR UPDATE ON knowledge_base_entries 
    FOR EACH ROW EXECUTE FUNCTION update_knowledge_search_vector();

-- Function for audit logging
CREATE OR REPLACE FUNCTION log_data_access()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (
        action,
        resource_type,
        resource_id,
        data_accessed,
        timestamp
    ) VALUES (
        TG_OP,
        TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id),
        CASE 
            WHEN TG_OP = 'DELETE' THEN to_jsonb(OLD)
            ELSE to_jsonb(NEW)
        END,
        NOW()
    );
    
    RETURN COALESCE(NEW, OLD);
END;
$$ language 'plpgsql';

-- Audit triggers for sensitive tables
CREATE TRIGGER audit_patients_trigger AFTER INSERT OR UPDATE OR DELETE ON patients FOR EACH ROW EXECUTE FUNCTION log_data_access();
CREATE TRIGGER audit_medical_assessments_trigger AFTER INSERT OR UPDATE OR DELETE ON medical_assessments FOR EACH ROW EXECUTE FUNCTION log_data_access();

-- ==============================================================================
-- SAMPLE DATA FOR DEVELOPMENT AND TESTING
-- ==============================================================================

-- Insert sample system configuration
INSERT INTO system_configuration (config_key, config_value, description, category, data_type) VALUES
('esi_level_thresholds', '{"1": "life_threatening", "2": "high_risk", "3": "urgent", "4": "less_urgent", "5": "non_urgent"}', 'ESI level definitions', 'clinical', 'json'),
('session_timeout_minutes', '60', 'User session timeout in minutes', 'security', 'integer'),
('max_concurrent_sessions', '1000', 'Maximum concurrent user sessions', 'performance', 'integer'),
('ai_model_endpoints', '{"intake": "gemini-pro", "triage": "gemini-pro", "knowledge": "embeddings-ada-002"}', 'AI model configuration', 'ai_config', 'json');

-- Insert sample feature flags
INSERT INTO feature_flags (flag_name, description, is_enabled, rollout_percentage) VALUES
('multi_language_support', 'Enable multi-language patient interface', false, 0.0),
('advanced_ai_triage', 'Enable advanced AI triage algorithms', true, 100.0),
('real_time_monitoring', 'Enable real-time patient monitoring dashboard', true, 50.0);

-- ==============================================================================
-- VIEWS FOR COMMON QUERIES
-- ==============================================================================

-- Active triage sessions with patient information
CREATE VIEW active_triage_sessions AS
SELECT 
    ts.id as session_id,
    ts.patient_id,
    p.medical_record_number,
    ts.department,
    ts.chief_complaint,
    ts.esi_level,
    ts.session_start,
    ts.triage_nurse_id,
    u.first_name || ' ' || u.last_name as nurse_name,
    EXTRACT(EPOCH FROM (NOW() - ts.session_start))/60 as wait_time_minutes
FROM triage_sessions ts
JOIN patients p ON ts.patient_id = p.id
JOIN users u ON ts.triage_nurse_id = u.id
WHERE ts.status = 'active'
ORDER BY ts.esi_level, ts.session_start;

-- Agent performance summary
CREATE VIEW agent_performance_summary AS
SELECT 
    agent_type,
    COUNT(*) as total_interactions,
    AVG(processing_time_ms) as avg_response_time_ms,
    AVG(confidence_score) as avg_confidence_score,
    COUNT(*) FILTER (WHERE interaction_type = 'error') as error_count,
    (COUNT(*) FILTER (WHERE interaction_type != 'error')::DECIMAL / COUNT(*)) * 100 as success_rate_percent
FROM agent_interactions
WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY agent_type;

-- Daily triage statistics
CREATE VIEW daily_triage_stats AS
SELECT 
    DATE(session_start) as triage_date,
    department,
    COUNT(*) as total_sessions,
    COUNT(*) FILTER (WHERE esi_level = '1') as esi_1_count,
    COUNT(*) FILTER (WHERE esi_level = '2') as esi_2_count,
    COUNT(*) FILTER (WHERE esi_level = '3') as esi_3_count,
    COUNT(*) FILTER (WHERE esi_level = '4') as esi_4_count,
    COUNT(*) FILTER (WHERE esi_level = '5') as esi_5_count,
    AVG(EXTRACT(EPOCH FROM (COALESCE(session_end, NOW()) - session_start))/60) as avg_session_duration_minutes
FROM triage_sessions
WHERE session_start >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(session_start), department
ORDER BY triage_date DESC, department;

-- ==============================================================================
-- SECURITY POLICIES (ROW LEVEL SECURITY)
-- ==============================================================================

-- Enable row level security on sensitive tables
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE medical_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE triage_sessions ENABLE ROW LEVEL SECURITY;

-- Policies for patient data access (implement based on organization's needs)
-- Example: Users can only access patients in their department
-- CREATE POLICY patient_department_access ON patients
--     FOR ALL TO healthcare_users
--     USING (department = current_setting('app.current_user_department'));

-- ==============================================================================
-- MAINTENANCE AND MONITORING
-- ==============================================================================

-- Create partitioned table for audit logs (by month)
CREATE TABLE audit_logs_y2024m01 PARTITION OF audit_logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Add more partitions as needed for better performance

-- ==============================================================================
-- COMMENTS FOR DOCUMENTATION
-- ==============================================================================

COMMENT ON TABLE patients IS 'Core patient information with encrypted demographics for HIPAA compliance';
COMMENT ON TABLE triage_sessions IS 'Individual triage assessment sessions with ESI scoring and clinical data';
COMMENT ON TABLE agent_interactions IS 'AI agent interactions and responses for performance monitoring';
COMMENT ON TABLE audit_logs IS 'Comprehensive audit trail for HIPAA compliance and security monitoring';
COMMENT ON TABLE clinical_protocols IS 'Evidence-based clinical protocols and treatment guidelines';
COMMENT ON TABLE drug_interactions IS 'Drug interaction database for clinical decision support';
COMMENT ON TABLE knowledge_base_entries IS 'Medical knowledge base for AI agent retrieval and clinical reference';

COMMENT ON COLUMN patients.encrypted_demographics IS 'Encrypted patient demographics using AES-256 encryption';
COMMENT ON COLUMN triage_sessions.esi_level IS 'Emergency Severity Index level (1=most urgent, 5=least urgent)';
COMMENT ON COLUMN agent_interactions.confidence_score IS 'AI model confidence score (0.0-1.0) for response quality';
COMMENT ON COLUMN vital_signs.temperature IS 'Body temperature in Fahrenheit';
COMMENT ON COLUMN medical_assessments.assessment_scores IS 'Structured clinical assessment scores and risk calculations';