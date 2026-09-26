# Module 06: Source Code Walkthrough

## Primary Python Modules

### 1. `src/database/connection.py`
- `DatabaseConnection`: Dual-engine database connection wrapper supporting DuckDB and SQLite. Handles SQL execution, parameters, and transaction commits.

### 2. `src/database/schema.py`
- `run_migrations()`: Iterates over SQL files in `sql/migrations/*.sql` in alphanumeric order to apply DDL schemas idempotently.

### 3. `src/etl/dimensions_loader.py`
- Contains `load_dates()`, `load_locations()`, `load_customers()`, `load_managers()`, `load_products()`. Guarantees surrogate keys are populated with proper Type 2 effective dates.

### 4. `src/etl/bridge_loader.py`
- `load_bridge()`: Connects customer surrogate keys to business manager surrogate keys and location keys over effective date ranges.

### 5. `src/etl/facts_loader.py`
- `load_sales_order_lines()`: Implements fulfillment eligibility quarantine logic, date-versioned dimension key resolution, and revenue metrics calculation.

### 6. `src/etl/aggregate_loader.py`
- `refresh_monthly_aggregates()`: Truncates and rebuilds `FACT_SALES_MONTHLY_AGG` directly from `FACT_SALES_ORDER_LINE`.

### 7. `src/analytics/reports.py`
- Provides analytical reporting helper queries and `reconcile_atomic_and_aggregate()` verification function.
