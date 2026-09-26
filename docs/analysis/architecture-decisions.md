# Architecture Decision Records (ADRs)

## ADR-001: Analytical Database Selection
- **Status**: Approved.
- **Decision**: Select **DuckDB** (and in-memory SQLite fallback) as the core analytical data warehouse engine.
- **Rationale**: DuckDB is a high-performance in-process columnar database optimized for OLAP analytical queries, window functions, and Kimball dimensional schemas.

---

## ADR-002: SCD Strategy & Surrogate Key Management
- **Status**: Approved.
- **Decision**: 
  - `DIM_DATE`: Type 0 (Static).
  - `DIM_LOCATION`, `DIM_CUSTOMER`, `DIM_BUSINESS_MANAGER`, `DIM_PRODUCT`: Combination of Type 1 (overwrite attributes like contact details) and Type 2 (versioned attributes like name, status, unit price, location type, region).
  - Versioned rows maintain `effective_start_date`, `effective_end_date` (defaulting to `9999-12-31`), `is_current` boolean flag, and integer `version_number`.
  - Surrogate keys are generated integer sequences (`INTEGER PRIMARY KEY`).

---

## ADR-003: Fulfillment Eligibility Policy
- **Status**: Approved.
- **Decision**: Enforce strict fulfillment eligibility validation in `src/etl/facts_loader.py`. Orders may only be fulfilled from locations where `location_type IN ('Warehouse', 'Manufacturing')`. Orders attempting fulfillment from 'Sales Office' locations are quarantined in `ETL_REJECT_LOG`.

---

## ADR-004: Revenue Metric Semantics
- **Status**: Approved.
- **Decision**:
  - `Gross_Revenue` = `Quantity * Unit_Price`
  - `Net_Revenue` = `Gross_Revenue - Discount_Amount`
  - Both atomic fact (`FACT_SALES_ORDER_LINE`) and aggregate fact (`FACT_SALES_MONTHLY_AGG`) maintain exact numeric precision.

---

## ADR-005: Temporal Bridge Relationship Model
- **Status**: Approved.
- **Decision**: `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT` maps relationships between Customers, Managers, and Divisions over explicit effective date ranges (`effective_start_date` to `effective_end_date`), allowing multiple manager assignments per customer across different divisions while enforcing single-manager responsibility per atomic order line.
