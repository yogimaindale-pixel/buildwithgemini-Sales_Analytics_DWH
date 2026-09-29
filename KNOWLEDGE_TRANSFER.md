# Sales Analytics Data Warehouse — Knowledge Transfer (KT) Guide

> **Beginner-Friendly Onboarding, Core Concepts Explained, Codebase Sitemap, & Hands-On Tutorials**

---

## 🎯 Welcome to the Knowledge Transfer Guide

This document is specifically written for junior developers, data engineers, and analysts onboarding to the **Sales Analytics Data Warehouse** project. It explains key concepts, code structure, execution flow, and step-by-step tutorials to help you understand and contribute to this repository with confidence.

---

## 💡 Core Data Warehousing Concepts Simplified

### 1. What is a Star Schema?
In operational databases (OLTP), data is spread across many normalized tables to avoid duplication. In data warehousing (OLAP), we organize data into a **Star Schema** for fast analytical queries:
- **Fact Tables** (In the center): Contain numerical measurement metrics (e.g., `quantity`, `unit_price`, `gross_revenue`, `net_revenue`).
- **Dimension Tables** (Surrounding the center): Contain descriptive context attributes (e.g., `customer_name`, `location_name`, `region`, `product_name`).

### 2. What is SCD Type 2 (Slowly Changing Dimensions)?
Customers change tiers, business managers change titles, and locations change names over time. 
In **SCD Type 2**, when an attribute changes, we **do not overwrite** the old row. Instead, we:
1. Close the previous record by setting `effective_end_date` to the change date and `is_current = false`.
2. Insert a brand new row with a new surrogate key (`customer_key`), `effective_start_date = change_date`, `effective_end_date = '9999-12-31'`, and `is_current = true`.

This preserves full historical accuracy when analyzing past sales!

### 3. What is a Bridge Table?
Sometimes entities have a **many-to-many relationship**. For example, one customer may be served by multiple business managers across different regional divisions. A **Bridge Table** (`BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT`) sits between dimension tables to resolve many-to-many linkages cleanly.

### 4. What is Atomic-to-Aggregate Data Reconciliation?
Data warehouses store two levels of data:
1. **Atomic Data** (`FACT_SALES_ORDER_LINE`): Detailed line-item order rows.
2. **Aggregate Data** (`FACT_SALES_MONTHLY_AGG`): Pre-computed monthly revenue summaries.

**Reconciliation** runs automated checks (`reconcile_atomic_and_aggregate`) to ensure that $\sum(\text{Atomic Net Revenue}) = \sum(\text{Aggregate Net Revenue})$. If they don't match, an alert is triggered!

---

## 🗺️ Codebase Sitemap & File Guide

| File Path | Role & Purpose | Key Functions / Classes |
| :--- | :--- | :--- |
| `main.py` | CLI Entrypoint & Pipeline Orchestrator | `run_pipeline()`, `main()` |
| `src/database/connection.py` | Database abstraction layer for SQLite & DuckDB | `DatabaseConnection` |
| `src/database/schema.py` | Executes SQL schema DDL migrations | `run_migrations()` |
| `src/etl/seed_data.py` | Generates realistic mock seed data | `get_raw_locations()`, `get_raw_order_lines()` |
| `src/etl/dimensions_loader.py` | Populates SCD Type 2 dimension tables | `load_all_dimensions()`, `load_locations()` |
| `src/etl/bridge_loader.py` | Populates customer-manager bridge mapping | `load_bridge()` |
| `src/etl/facts_loader.py` | Ingests order lines & visits with fulfillment checks | `load_sales_order_lines()`, `load_customer_visits()` |
| `src/etl/aggregate_loader.py` | Refreshes monthly summary data mart | `refresh_monthly_aggregates()` |
| `src/analytics/reports.py` | Generates reports & performs reconciliation | `get_detailed_monthly_sales_report()`, `reconcile_atomic_and_aggregate()` |
| `src/utils/logger.py` | Configures structured logging output | `setup_logger()` |

---

## 📖 Step-by-Step Hands-On Tutorials

### Tutorial 1: Run the Complete Pipeline Locally
1. Activate your Python virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Run the main script:
   ```bash
   python main.py --db sales_warehouse.db
   ```
3. Observe the console output logs showing step-by-step progress from schema migration to reconciliation confirmation!

---

### Tutorial 2: Query the Database directly using Python
Create a quick scratch script `inspect_db.py`:

```python
from src.database.connection import DatabaseConnection

# Connect to database
db = DatabaseConnection(db_path="sales_warehouse.db", use_duckdb=False)

# Query rejected quarantined orders
rejects = db.execute_query("SELECT reject_id, record_identifier, reject_reason FROM ETL_REJECT_LOG;")
print("--- QUARANTINED ORDERS ---")
for r in rejects:
    print(r)

# Close connection
db.close()
```

Run it with:
```bash
python inspect_db.py
```

---

### Tutorial 3: Run the PyTest Suite
Run all 13 unit and integration tests to verify pipeline health:
```bash
PYTHONPATH=. pytest -v
```

---

## ❓ Frequently Asked Questions (FAQ)

#### Q1: Why were some order lines rejected into `ETL_REJECT_LOG`?
**A**: Order `ORD-2024-005` attempted to fulfill items from `Sales Office London` (`LOC-003`). Our business rule mandates that order fulfillment must occur from a `Warehouse` or `Manufacturing` facility. The pipeline quarantined this row into `ETL_REJECT_LOG` without halting execution!

#### Q2: How do I switch from SQLite to DuckDB?
**A**: Simply pass `--engine duckdb` when running `main.py`:
```bash
python main.py --db sales_warehouse.duckdb --engine duckdb
```

---

## 🏁 Summary Checklist for Developers

When making changes to this codebase:
- [ ] Maintain line-by-line comments for junior developer clarity.
- [ ] Run `PYTHONPATH=. pytest -v` before committing code to verify all 13 tests pass.
- [ ] Check `ETL_REJECT_LOG` for unexpected quarantined records when adding new mock data.
