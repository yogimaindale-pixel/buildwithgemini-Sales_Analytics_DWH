# Line-by-Line Breakdown: main.py

- **L1-L32**: Import logging, database connection, schema migration runner, and ETL loaders.
- **L33-L45**: Define `run_pipeline()`. Initialize database connection and run schema migrations from `sql/migrations/`.
- **L46-L55**: Execute `load_all_dimensions()`, populating Date, Location, Customer, Manager, and Product dimensions.
- **L56-L65**: Execute `load_bridge()`, `load_customer_visits()`, and `load_sales_order_lines()`.
- **L66-L72**: Execute `refresh_monthly_aggregates()` and invoke `reconcile_atomic_and_aggregate()` to audit metrics.
- **L75-L108**: Define `main()` CLI entrypoint supporting `--reconcile` and `--reset-db` flags.
