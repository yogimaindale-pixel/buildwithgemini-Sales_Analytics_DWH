# 🏛️ 02. Enterprise Sales Analytics DWH - Architecture Deep Dive

## 1. Dimensional Model Specification

### Dimensions
- `DIM_CUSTOMER`: Customer surrogate key (`CUSTOMER_SK`), business key (`CUSTOMER_ID`), customer name, tier, SCD2 fields (`EFFECTIVE_FROM`, `EFFECTIVE_TO`, `IS_CURRENT`).
- `DIM_PRODUCT`: Product surrogate key (`PRODUCT_SK`), SKU code, category, unit price, SCD2 fields.
- `DIM_LOCATION`: Fulfillment locations with type classification (`Warehouse`, `Manufacturing`, `Sales Office`).
- `DIM_BUSINESS_MANAGER`: Corporate manager directory.

### Bridge Tables
- `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT`: Resolves many-to-many relationships when multiple managers share revenue attribution for a single enterprise customer, tracking allocation weight percentage (`ALLOCATION_WEIGHT`).

### Fact Tables
- `FACT_SALES_ORDER_LINE`: Grain = 1 row per order line. Contains surrogate keys (`CUSTOMER_SK`, `PRODUCT_SK`, `LOCATION_SK`), quantity, gross revenue, discount amount, and net revenue.
- `FACT_SALES_MONTHLY_AGG`: Grain = 1 row per customer/product/month. Pre-aggregated net revenue and order count.
