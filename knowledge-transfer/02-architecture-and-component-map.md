# Module 02: Architecture and Component Map

## Layered System Architecture

```
+-----------------------------------------------------------------------+
|                         CONSUMPTION LAYER                             |
|  - Web Dashboard (reports/dashboard/index.html)                       |
|  - Detailed Monthly Sales Report (src/analytics/reports.py)           |
+-----------------------------------------------------------------------+
                                  ▲
                                  │ SQL / Python API
+-----------------------------------------------------------------------+
|                      ANALYTICAL STORAGE (DuckDB / SQLite)              |
|  - Dimensions: DIM_DATE, DIM_LOCATION, DIM_CUSTOMER, MGR, PRODUCT     |
|  - Bridge: BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT                         |
|  - Facts: FACT_CUSTOMER_VISIT, FACT_SALES_ORDER_LINE                  |
|  - Aggregates: FACT_SALES_MONTHLY_AGG                                 |
|  - Audit/Controls: ETL_PIPELINE_RUNS, ETL_REJECT_LOG                  |
+-----------------------------------------------------------------------+
                                  ▲
                                  │ Load / Refresh
+-----------------------------------------------------------------------+
|                         ETL PROCESSING LAYER                          |
|  - Seed Data Generator (src/etl/seed_data.py)                         |
|  - Dimension Loader (src/etl/dimensions_loader.py)                   |
|  - Bridge Loader (src/etl/bridge_loader.py)                           |
|  - Facts Loader (src/etl/facts_loader.py)                             |
|  - Aggregate Refresh Loader (src/etl/aggregate_loader.py)             |
+-----------------------------------------------------------------------+
```

## Component Boundaries
1. `sql/migrations/`: Physical DDL schemas defining tables, types, keys, and foreign keys.
2. `src/database/`: DB connection handling (`DatabaseConnection`) and schema migration execution (`run_migrations`).
3. `src/etl/`: Business rule transformations, SCD Type 2 dimension versioning, reject quarantine, and fact table construction.
4. `src/analytics/`: High-level summary queries, report formatters, and reconciliation validators.
5. `reports/dashboard/`: Interactive HTML5/JS consumption dashboard.
