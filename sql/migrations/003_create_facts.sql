-- Migration 003: Create Fact Tables (Customer Visits, Atomic Sales Order Lines, Monthly Aggregates)

CREATE TABLE IF NOT EXISTS FACT_CUSTOMER_VISIT (
    visit_id INTEGER PRIMARY KEY,
    customer_key INTEGER NOT NULL,
    division_visited VARCHAR(50) NOT NULL,
    visit_date_key INTEGER NOT NULL,
    assisting_manager_key INTEGER NOT NULL,
    visit_count INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (customer_key) REFERENCES DIM_CUSTOMER(customer_key),
    FOREIGN KEY (visit_date_key) REFERENCES DIM_DATE(date_key),
    FOREIGN KEY (assisting_manager_key) REFERENCES DIM_BUSINESS_MANAGER(manager_key)
);

CREATE TABLE IF NOT EXISTS FACT_SALES_ORDER_LINE (
    fact_id INTEGER PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL,
    line_number INTEGER NOT NULL,
    order_date_key INTEGER NOT NULL,
    order_location_key INTEGER NOT NULL,
    fulfillment_location_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    business_manager_key INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(12, 2) NOT NULL,
    discount_amount DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    gross_revenue DECIMAL(12, 2) NOT NULL,
    net_revenue DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_date_key) REFERENCES DIM_DATE(date_key),
    FOREIGN KEY (order_location_key) REFERENCES DIM_LOCATION(location_key),
    FOREIGN KEY (fulfillment_location_key) REFERENCES DIM_LOCATION(location_key),
    FOREIGN KEY (customer_key) REFERENCES DIM_CUSTOMER(customer_key),
    FOREIGN KEY (product_key) REFERENCES DIM_PRODUCT(product_key),
    FOREIGN KEY (business_manager_key) REFERENCES DIM_BUSINESS_MANAGER(manager_key)
);

CREATE TABLE IF NOT EXISTS FACT_SALES_MONTHLY_AGG (
    agg_id INTEGER PRIMARY KEY,
    year_month VARCHAR(7) NOT NULL,
    region VARCHAR(50) NOT NULL,
    product_key INTEGER NOT NULL,
    location_type VARCHAR(50) NOT NULL,
    total_quantity INTEGER NOT NULL,
    total_net_revenue DECIMAL(14, 2) NOT NULL,
    order_line_count INTEGER NOT NULL,
    refresh_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_key) REFERENCES DIM_PRODUCT(product_key)
);
