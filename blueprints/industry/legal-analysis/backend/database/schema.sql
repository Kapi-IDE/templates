-- Sample schema excerpt
CREATE TABLE case_law (
    case_id TEXT PRIMARY KEY,
    case_name TEXT NOT NULL,
    court TEXT,
    jurisdiction TEXT,
    decision_date DATE,
    legal_issues TEXT,
    holding TEXT,
    citation TEXT,
    full_text TEXT
);

CREATE TABLE legal_precedents (
    precedent_id TEXT PRIMARY KEY,
    case_id TEXT,
    legal_principle TEXT,
    binding_authority TEXT,
    jurisdiction TEXT,
    precedent_weight INTEGER,
    related_statutes TEXT
);
