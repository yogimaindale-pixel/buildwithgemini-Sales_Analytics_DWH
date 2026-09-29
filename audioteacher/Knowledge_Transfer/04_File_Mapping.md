# 🗺️ 04. Master File, Function, and Line Range Mapping Matrix

| Concept | Target File | Class / Function | Start Line | End Line | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Pipeline Runner** | `main.py` | `run_pipeline` | 33 | 72 | Master pipeline orchestrator. |
| **Schema Migrations** | `src/database/schema.py` | `run_migrations` | 18 | 48 | Executes SQL migration DDL scripts in sequence. |
| **Database Wrapper** | `src/database/connection.py` | `DatabaseConnection` | 23 | 86 | Provides thread-safe SQLite connection and cursor contexts. |
| **Dimensions Loader** | `src/etl/dimensions_loader.py`| `load_all_dimensions` | 183 | 195 | Loads master dimensions with SCD Type 2 tracking flags. |
| **Bridge Loader** | `src/etl/bridge_loader.py` | `load_bridge` | 15 | 54 | Loads customer-manager assignment bridge table. |
| **Facts Loader** | `src/etl/facts_loader.py` | `load_sales_order_lines`| 60 | 166 | Populates atomic sales fact lines and isolates non-eligible fulfillment locations. |
| **Aggregate Loader** | `src/etl/aggregate_loader.py` | `refresh_monthly_aggregates`| 15 | 66 | Pre-computes monthly sales summary data marts. |
| **Reconciliation** | `src/analytics/reports.py` | `reconcile_atomic_and_aggregate`| 70 | 105 | Verifies 100% metric alignment between atomic and aggregate facts. |
