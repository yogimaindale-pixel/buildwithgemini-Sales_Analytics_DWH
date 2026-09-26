-- Migration 001: Create Dimension Tables

CREATE TABLE IF NOT EXISTS DIM_DATE (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day_of_month INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    year_month VARCHAR(7) NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS DIM_LOCATION (
    location_key INTEGER PRIMARY KEY,
    location_id VARCHAR(50) NOT NULL,
    location_name VARCHAR(100) NOT NULL,
    location_type VARCHAR(50) NOT NULL, -- 'Sales Office', 'Warehouse', 'Manufacturing'
    region VARCHAR(50) NOT NULL,
    effective_start_date DATE NOT NULL,
    effective_end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL,
    version_number INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS DIM_CUSTOMER (
    customer_key INTEGER PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    customer_type VARCHAR(50) NOT NULL, -- 'Enterprise', 'SMB', 'Government'
    status VARCHAR(20) NOT NULL,        -- 'Active', 'Inactive'
    effective_start_date DATE NOT NULL,
    effective_end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL,
    version_number INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS DIM_BUSINESS_MANAGER (
    manager_key INTEGER PRIMARY KEY,
    manager_id VARCHAR(50) NOT NULL,
    manager_name VARCHAR(100) NOT NULL,
    division VARCHAR(50) NOT NULL,
    effective_start_date DATE NOT NULL,
    effective_end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL,
    version_number INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS DIM_PRODUCT (
    product_key INTEGER PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit_price DECIMAL(12, 2) NOT NULL,
    effective_start_date DATE NOT NULL,
    effective_end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL,
    version_number INTEGER NOT NULL
);
