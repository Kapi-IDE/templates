-- Sample schema excerpt
CREATE TABLE stocks (
    ticker TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    sector TEXT,
    market_cap REAL,
    pe_ratio REAL,
    dividend_yield REAL,
    beta REAL,
    description TEXT
);

CREATE TABLE market_data (
    ticker TEXT,
    date DATE,
    open_price REAL,
    close_price REAL,
    volume INTEGER,
    rsi REAL,
    moving_avg_50 REAL,
    moving_avg_200 REAL
);
