# 📌 01. Enterprise Sales Analytics DWH - Repository Overview

## 🎯 Business Problem & Architectural Goal
Enterprise sales organizations manage complex relationships between corporate customers, business managers, multi-line sales orders, fulfillment locations, and monthly revenue targets. Measuring sales velocity, manager attribution, and order line fulfillment accuracy requires a robust Kimball Star Schema warehouse.

The **Enterprise Sales Analytics Data Warehouse (`buildwithgemini-Sales_Analytics_DWH`)** implements a production-grade dimensional warehouse complete with SCD Type 2 dimensions, many-to-many bridge tables, fulfillment location business rules, pre-calculated monthly aggregations, and automated cross-layer reconciliation.

---

## 🏗️ Core Architecture & Component Map

- **Schema Migration Engine (`src/database/schema.py`)**: Runs SQL migration DDLs in sequence (`sql/migrations/001_create_dimensions.sql` through `004_create_controls.sql`).
- **Dimensions Loader (`src/etl/dimensions_loader.py`)**: Loads `DIM_DATE`, `DIM_LOCATION`, `DIM_CUSTOMER`, `DIM_BUSINESS_MANAGER`, and `DIM_PRODUCT` with SCD Type 2 tracking (`EFFECTIVE_FROM`, `EFFECTIVE_TO`, `IS_CURRENT`).
- **Bridge Loader (`src/etl/bridge_loader.py`)**: Populates `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT` to resolve many-to-many relationships between corporate customers and business managers.
- **Facts Loader (`src/etl/facts_loader.py`)**: Populates `FACT_CUSTOMER_VISIT` and atomic order lines `FACT_SALES_ORDER_LINE`, enforcing fulfillment location validation (isolating non-Warehouse/Manufacturing locations to quarantine).
- **Aggregate Loader (`src/etl/aggregate_loader.py`)**: Pre-computes monthly summary metrics into `FACT_SALES_MONTHLY_AGG`.
- **Reconciliation Engine (`src/analytics/reports.py`)**: Verifies 100% metric fidelity between atomic sales order lines and monthly aggregate marts.

---

## 🛠️ Technology Stack & Dependencies
- **Core Language**: Python 3.10+
- **Database**: SQLite 3 (`sales_warehouse.db`) with `PRAGMA foreign_keys = ON`
- **Dashboard UI**: HTML5 / CSS3 / JavaScript (`reports/dashboard/index.html`)
- **Testing**: `pytest` (13 unit & integration tests in `tests/`)
