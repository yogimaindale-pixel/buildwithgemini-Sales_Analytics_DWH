# Module 04: Data Model and SCD Policy Guide

## Dimensional Model Design (Kimball Star Schema)

### 1. Dimension Tables
- `DIM_DATE`: Date dimension (Type 0). Granularity: Calendar day. Key: `YYYYMMDD` integer.
- `DIM_LOCATION`: Location dimension (Type 1/2). Attributes: `location_name`, `location_type` ('Sales Office', 'Warehouse', 'Manufacturing'), `region`.
- `DIM_CUSTOMER`: Customer dimension (Type 1/2). Attributes: `customer_name`, `customer_type`, `status`.
- `DIM_BUSINESS_MANAGER`: Business Manager dimension (Type 1/2). Attributes: `manager_name`, `division`.
- `DIM_PRODUCT`: Product dimension (Type 1/2). Attributes: `product_name`, `category`, `unit_price`.

### 2. Slowly Changing Dimension (SCD Type 2) Standard
Every versioned dimension table includes the following tracking columns:
- `effective_start_date`: Date when record version became active.
- `effective_end_date`: Date when record version was superseded (defaults to `9999-12-31` for current version).
- `is_current`: Boolean flag (`TRUE` for active version, `FALSE` for historical versions).
- `version_number`: Incremental integer sequence starting at 1.

### 3. Assignment Bridge Table
- `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT`: Maps customer surrogate keys to business manager surrogate keys and divisions over date ranges (`effective_start_date` to `effective_end_date`).

### 4. Fact Tables
- `FACT_SALES_ORDER_LINE`: Atomic fact table. Grain: One row per order number + line number.
- `FACT_SALES_MONTHLY_AGG`: Monthly aggregated fact table derived strictly from atomic order lines.
