-- Sample schema excerpt
CREATE TABLE ai_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT,
    risk_category TEXT,
    deployment_status TEXT,
    owner_team TEXT,
    last_assessment_date DATE,
    governance_score REAL
);

CREATE TABLE risk_assessments (
    assessment_id TEXT PRIMARY KEY,
    system_id TEXT,
    assessment_date DATE,
    risk_score REAL,
    risk_factors TEXT,
    mitigation_recommendations TEXT,
    assessor_id TEXT
);
