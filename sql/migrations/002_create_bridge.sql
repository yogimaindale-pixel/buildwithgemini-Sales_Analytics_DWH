-- Migration 002: Create Customer-Manager Assignment Bridge Table

CREATE TABLE IF NOT EXISTS BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT (
    assignment_key INTEGER PRIMARY KEY,
    customer_key INTEGER NOT NULL,
    manager_key INTEGER NOT NULL,
    division VARCHAR(50) NOT NULL,
    location_key INTEGER NOT NULL,
    effective_start_date DATE NOT NULL,
    effective_end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL,
    FOREIGN KEY (customer_key) REFERENCES DIM_CUSTOMER(customer_key),
    FOREIGN KEY (manager_key) REFERENCES DIM_BUSINESS_MANAGER(manager_key),
    FOREIGN KEY (location_key) REFERENCES DIM_LOCATION(location_key)
);
