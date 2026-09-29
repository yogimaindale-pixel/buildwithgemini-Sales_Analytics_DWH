# 💡 03. Core Engineering Concepts & Pattern Cards

### Concept 1: Many-to-Many Bridge Table Pattern
- **What is it?**: A table that connects a dimension and fact table when one record in table A maps to multiple records in table B.
- **Why needed?**: Allows splitting revenue attribution across multiple business managers without duplicating fact order lines.
- **Repository Implementation**: `src/etl/bridge_loader.py` (`BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT`).

### Concept 2: Fulfillment Location Business Firewall
- **What is it?**: Isolating order lines originating from ineligible location types (`Sales Office`) into quarantine before landing into atomic fact tables.
- **Repository Implementation**: `src/etl/facts_loader.py`.

### Concept 3: Atomic vs Aggregate Metric Reconciliation
- **What is it?**: Automated cross-table validation comparing `SUM(NET_REVENUE)` between atomic fact lines and monthly aggregate marts.
- **Repository Implementation**: `src/analytics/reports.py` (`reconcile_atomic_and_aggregate`).
