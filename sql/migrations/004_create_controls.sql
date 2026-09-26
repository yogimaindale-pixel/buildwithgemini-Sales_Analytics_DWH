-- Migration 004: Create Audit and Quarantine Control Tables

CREATE TABLE IF NOT EXISTS ETL_PIPELINE_RUNS (
    run_id VARCHAR(50) PRIMARY KEY,
    pipeline_name VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status VARCHAR(20) NOT NULL, -- 'RUNNING', 'SUCCESS', 'FAILED'
    records_processed INTEGER DEFAULT 0,
    records_rejected INTEGER DEFAULT 0,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS ETL_REJECT_LOG (
    reject_id INTEGER PRIMARY KEY,
    run_id VARCHAR(50) NOT NULL,
    source_entity VARCHAR(100) NOT NULL,
    record_identifier VARCHAR(100),
    reject_reason VARCHAR(255) NOT NULL,
    raw_record_json TEXT,
    rejected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
