# Sales Analytics Data Warehouse (Star Schema + SCD Type 2 + Bridge Tables)

> **Junior Developer & Production-Ready Enterprise DWH Reference**  
> A complete, fully documented, and line-by-line commented Python & SQL Data Warehouse pipeline demonstrating enterprise Dimensional Modeling, Slowly Changing Dimensions (SCD Type 2), Many-to-Many Bridge Tables, Fulfillment Rule Quality Control, and Automated Atomic-to-Aggregate Reconciliation.

---

## 📌 Executive Overview

The **Sales Analytics DWH** is an end-to-end data warehousing solution engineered to ingest, model, validate, and aggregate commercial sales and customer visit transactions. It supports both **SQLite** (lightweight file-based engine) and **DuckDB** (high-performance columnar OLAP engine).

### Key Architectural Highlights
- **Star Schema Architecture**: Consists of central fact tables (`FACT_SALES_ORDER_LINE`, `FACT_CUSTOMER_VISIT`), dimension tables (`DIM_DATE`, `DIM_LOCATION`, `DIM_CUSTOMER`, `DIM_BUSINESS_MANAGER`, `DIM_PRODUCT`), and a pre-aggregated monthly summary mart (`FACT_SALES_MONTHLY_AGG`).
- **Slowly Changing Dimensions (SCD Type 2)**: Tracks historical attribute changes for customers, managers, locations, and products with surrogate keys (`*_key`), `effective_start_date`, `effective_end_date`, and `is_current` flags.
- **Many-to-Many Bridge Tables**: Resolves dynamic relationships between Customers, Business Managers, and Geographic Locations via `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT`.
- **Fulfillment Eligibility Rule Enforcement**: Enforces business logic requiring orders to be fulfilled strictly from `Warehouse` or `Manufacturing` facilities. Violations (e.g. Sales Office fulfillment attempts) are quarantined into `ETL_REJECT_LOG`.
- **Automated Data Quality & Reconciliation**: Validates financial revenue equations (`Net Revenue = Gross Revenue - Discount`) and reconciles atomic fact totals against monthly aggregate mart totals down to the cent ($0.01 tolerance).

---

## 📁 Repository Directory Structure

```text
buildwithgemini-Sales_Analytics_DWH/
├── main.py                          # Master CLI orchestrator & pipeline execution engine
├── sql/
│   └── migrations/
│       ├── 001_create_dimensions.sql # DDL for Date, Location, Customer, Manager, Product dimensions
│       ├── 002_create_bridge.sql     # DDL for Customer-Manager-Location bridge table
│       ├── 003_create_facts.sql      # DDL for Order Line, Customer Visit, and Monthly Aggregate tables
│       └── 004_create_controls.sql   # DDL for ETL Quarantine Reject Log table
├── src/
│   ├── analytics/
│   │   └── reports.py               # Detailed sales reporting & reconciliation queries
│   ├── database/
│   │   ├── connection.py            # SQLite & DuckDB abstraction driver wrapper
│   │   └── schema.py                # SQL migration execution engine
│   ├── etl/
│   │   ├── aggregate_loader.py      # Monthly aggregate sales mart loader
│   │   ├── bridge_loader.py         # Customer-Manager-Location bridge table loader
│   │   ├── dimensions_loader.py     # SCD Type 2 dimension population engine
│   │   ├── facts_loader.py          # Transactional order line & visit loader with quality rules
│   │   └── seed_data.py             # Mock transactional seed data generator
│   └── utils/
│       └── logger.py                # Centralized logging utility
├── tests/                           # Exhaustive PyTest unit and integration test suite
│   ├── test_aggregate_reconciliation.py
│   ├── test_bridge_assignments.py
│   ├── test_cli.py
│   ├── test_dimensions_scd.py
│   ├── test_end_to_end_quality.py
│   ├── test_fact_sales_order_line.py
│   └── test_fulfillment_rules.py
├── DOCUMENTATION.md                 # Technical requirements, schemas, and architecture specification
├── KNOWLEDGE_TRANSFER.md            # Beginner-friendly KT guide & step-by-step tutorials
└── README.md                        # Quick-start guide and execution instructions
```

---

## 🚀 Quick-Start Guide

### 1. Prerequisites
- **Python**: Version 3.10+
- **Git**: Installed on your terminal

### 2. Environment Setup
Clone the repository and set up a Python virtual environment:

```bash
git clone git@github.com:yogimaindale-pixel/buildwithgemini-Sales_Analytics_DWH.git
cd buildwithgemini-Sales_Analytics_DWH

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required dependencies
pip install duckdb pytest jinja2
```

---

## 🛠️ Execution Commands & CLI Usage

The master entrypoint `main.py` provides a rich command-line interface supporting multiple execution modes and database backends.

### 1. Run Complete End-to-End Pipeline
Executes schema migrations, loads dimensions, populates bridge tables, ingests fact tables, refreshes monthly aggregates, and runs reconciliation:

```bash
# Run using default SQLite engine
python main.py --db sales_warehouse.db

# Run using high-performance DuckDB columnar engine
python main.py --db sales_warehouse.duckdb --engine duckdb
```

### 2. Run Database Migrations Only
Creates target database tables from DDL files in `sql/migrations/`:

```bash
python main.py --action migrate --db sales_warehouse.db
```

### 3. Run Data Reconciliation Only
Compares total net revenue, quantity, and row counts between atomic fact tables and the monthly aggregate data mart:

```bash
python main.py --action reconcile --db sales_warehouse.db
```

### 4. Print Detailed Sales Report
Executes and prints a formatted monthly sales report to standard output:

```bash
python main.py --action report --db sales_warehouse.db
```

---

## 🧪 Running Unit & Integration Tests

The repository includes 13 unit tests covering dimension SCD2 dates, bridge integrity, revenue math, fulfillment quarantine rules, CLI subcommands, and aggregate reconciliation.

Execute the test suite with `pytest`:

```bash
PYTHONPATH=. pytest -v
```

Expected Output:
```text
============================= test session starts ==============================
collected 13 items                                                             

tests/test_aggregate_reconciliation.py::TestAggregateReconciliation::test_aggregate_reconciliation PASSED
tests/test_bridge_assignments.py::TestBridgeAssignments::test_bridge_loaded PASSED
tests/test_bridge_assignments.py::TestBridgeAssignments::test_bridge_referential_integrity PASSED
tests/test_cli.py::TestCLI::test_cli_migrate_action PASSED
tests/test_cli.py::TestCLI::test_cli_reconcile_action PASSED
tests/test_cli.py::TestCLI::test_cli_report_action PASSED
tests/test_cli.py::TestCLI::test_cli_run_pipeline_full_run PASSED
tests/test_dimensions_scd.py::TestDimensionsSCD::test_dimensions_loaded PASSED
tests/test_dimensions_scd.py::TestDimensionsSCD::test_scd2_date_ranges PASSED
tests/test_end_to_end_quality.py::TestEndToEndQuality::test_full_pipeline_execution PASSED
tests/test_fact_sales_order_line.py::TestFactSalesOrderLine::test_fact_revenue_calculations PASSED
tests/test_fulfillment_rules.py::TestFulfillmentRules::test_fulfillment_eligibility_enforcement PASSED
tests/test_fulfillment_rules.py::TestFulfillmentRules::test_reject_log_populated PASSED

============================== 13 passed in 1.48s ==============================
```

---

## 📚 Further Reading & Documentation

- **[DOCUMENTATION.md](file:///config/Desktop/buildwithgemini-Sales_Analytics_DWH/DOCUMENTATION.md)**: In-depth technical architecture, ER diagram, table schemas, business rules, and quality control specifications.
- **[KNOWLEDGE_TRANSFER.md](file:///config/Desktop/buildwithgemini-Sales_Analytics_DWH/KNOWLEDGE_TRANSFER.md)**: Beginner-friendly guide explaining Kimball Dimensional Modeling, SCD Type 2 history tracking, bridge tables, and hands-on tutorials.
