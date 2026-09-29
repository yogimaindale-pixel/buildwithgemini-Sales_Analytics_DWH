# Sales Analytics Data Warehouse Technical Specification & Architecture

> **Technical Requirements, Dimensional Schema Specification, Business Rules, and Data Dictionary**

---

## 1. Architectural System Overview

The **Sales Analytics Data Warehouse** is built following Ralph Kimball's Dimensional Modeling methodology. It transforms raw commercial operational transactions into structured dimensional star schema models optimized for analytical reporting and business intelligence.

```
                    +-------------------+
                    |     DIM_DATE      |
                    +-------------------+
                              |
                              | 1:N
                              v
+-------------------+   +--------------------------+   +-----------------------+
|   DIM_LOCATION    |-->| FACT_SALES_ORDER_LINE    |<--|      DIM_PRODUCT      |
+-------------------+   +--------------------------+   +-----------------------+
        |                     |            |
        | 1:N                 | 1:N        | 1:N
        v                     v            v
+-----------------------+   +----------------------+   +-----------------------+
| BRIDGE_CUSTOMER_      |   |  FACT_CUSTOMER_VISIT |   | DIM_BUSINESS_MANAGER  |
| MANAGER_ASSIGNMENT    |   +----------------------+   +-----------------------+
+-----------------------+                                          |
        ^                                                          | 1:N
        |                                                          v
        +----------------------------------------------------------+
```

---

## 2. Technical Requirements

### 2.1 Database Compatibility
- **Primary Engine**: SQLite 3.x (Zero-configuration file-based storage).
- **High-Performance Engine**: DuckDB 1.x (In-memory/columnar OLAP engine for fast analytics).
- **Interface Protocol**: Parameterized SQL execution driver abstraction provided by `DatabaseConnection` in `src/database/connection.py`.

### 2.2 Data Quality & Validation Rules
1. **Fulfillment Location Rule**: Orders must be fulfilled exclusively from location records where `location_type IN ('Warehouse', 'Manufacturing')`. Orders attempted to be fulfilled from `Sales Office` locations are quarantined into `ETL_REJECT_LOG`.
2. **Financial Revenue Math Rule**:
   - $\text{Gross Revenue} = \text{Quantity} \times \text{Unit Price}$
   - $\text{Net Revenue} = \text{Gross Revenue} - \text{Discount Amount}$
3. **Point-in-Time Dimension Lookup Rule**: Order transactions resolve dimension surrogate keys by matching transaction order date against dimension `effective_start_date` and `effective_end_date`.

---

## 3. Database Table Schemas & Data Dictionary

### 3.1 Dimension Tables

#### `DIM_DATE` (Conformed Date Dimension)
| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `date_key` | INTEGER | PRIMARY KEY | Integer surrogate date key in `YYYYMMDD` format (e.g. 20240315) |
| `full_date` | TEXT/DATE | | ISO date string (`YYYY-MM-DD`) |
| `year` | INTEGER | | Four-digit calendar year (e.g. 2024) |
| `quarter` | INTEGER | | Calendar quarter (1 to 4) |
| `month` | INTEGER | | Calendar month number (1 to 12) |
| `month_name` | TEXT | | Full month name (e.g. 'March') |
| `day` | INTEGER | | Day of month (1 to 31) |
| `day_of_week` | TEXT | | Day name (e.g. 'Friday') |
| `year_month` | TEXT | | Year-Month string (`YYYY-MM`) |

#### `DIM_LOCATION` (SCD Type 2 Location Dimension)
| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `location_key` | INTEGER | PRIMARY KEY | Surrogate location key |
| `location_id` | TEXT | | Natural operational location code (e.g. 'LOC-001') |
| `location_name` | TEXT | | Operational facility name (e.g. 'Chicago Distribution Center') |
| `location_type` | TEXT | | Facility classification: `Warehouse`, `Manufacturing`, `Sales Office` |
| `region` | TEXT | | Geographical sales region (e.g. 'North America', 'Europe') |
| `city` | TEXT | | City location |
| `country` | TEXT | | Country location |
| `effective_start_date` | TEXT | | Effective start date (`YYYY-MM-DD`) |
| `effective_end_date` | TEXT | | Effective end date (`YYYY-MM-DD` or '9999-12-31') |
| `is_current` | BOOLEAN | | Active version indicator (`true`/`false`) |

#### `DIM_CUSTOMER` (SCD Type 2 Customer Dimension)
| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `customer_key` | INTEGER | PRIMARY KEY | Surrogate customer key |
| `customer_id` | TEXT | | Natural customer ID (e.g. 'CUST-101') |
| `customer_name` | TEXT | | Corporate customer name |
| `industry` | TEXT | | Industry sector |
| `tier` | TEXT | | Customer classification tier (e.g. 'Enterprise', 'SMB') |
| `effective_start_date` | TEXT | | Effective start date |
| `effective_end_date` | TEXT | | Effective end date |
| `is_current` | BOOLEAN | | Active version indicator |

#### `DIM_BUSINESS_MANAGER` (SCD Type 2 Sales Manager Dimension)
| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `manager_key` | INTEGER | PRIMARY KEY | Surrogate business manager key |
| `manager_id` | TEXT | | Natural manager ID (e.g. 'MGR-01') |
| `manager_name` | TEXT | | Business manager full name |
| `title` | TEXT | | Corporate title |
| `effective_start_date` | TEXT | | Effective start date |
| `effective_end_date` | TEXT | | Effective end date |
| `is_current` | BOOLEAN | | Active version indicator |

#### `DIM_PRODUCT` (SCD Type 2 Product Dimension)
| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `product_key` | INTEGER | PRIMARY KEY | Surrogate product key |
| `product_id` | TEXT | | Natural product SKU code (e.g. 'PROD-A') |
| `product_name` | TEXT | | Product description |
| `category` | TEXT | | Product category |
| `list_price` | DECIMAL | | Standard catalog unit list price |
| `effective_start_date` | TEXT | | Effective start date |
| `effective_end_date` | TEXT | | Effective end date |
| `is_current` | BOOLEAN | | Active version indicator |

---

### 3.2 Bridge Table

#### `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT`
| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `assignment_key` | INTEGER | PRIMARY KEY | Unique bridge assignment surrogate key |
| `customer_key` | INTEGER | FOREIGN KEY | References `DIM_CUSTOMER(customer_key)` |
| `manager_key` | INTEGER | FOREIGN KEY | References `DIM_BUSINESS_MANAGER(manager_key)` |
| `location_key` | INTEGER | FOREIGN KEY | References `DIM_LOCATION(location_key)` |
| `division` | TEXT | | Business division (e.g. 'Commercial Sales') |
| `effective_start_date` | TEXT | | Relationship effective start date |
| `effective_end_date` | TEXT | | Relationship effective end date |
| `is_current` | BOOLEAN | | Active relationship indicator |

---

### 3.3 Fact Tables & Data Marts

#### `FACT_SALES_ORDER_LINE` (Atomic Fact Table)
| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `fact_id` | INTEGER | PRIMARY KEY | Fact row surrogate identifier |
| `order_number` | TEXT | | Natural order transaction code (e.g. 'ORD-2024-001') |
| `line_number` | INTEGER | | Line item sequence number (1, 2, 3...) |
| `order_date_key` | INTEGER | FOREIGN KEY | References `DIM_DATE(date_key)` |
| `order_location_key` | INTEGER | FOREIGN KEY | Order placement location key in `DIM_LOCATION` |
| `fulfillment_location_key` | INTEGER | FOREIGN KEY | Fulfillment location key in `DIM_LOCATION` |
| `customer_key` | INTEGER | FOREIGN KEY | References `DIM_CUSTOMER(customer_key)` |
| `product_key` | INTEGER | FOREIGN KEY | References `DIM_PRODUCT(product_key)` |
| `business_manager_key` | INTEGER | FOREIGN KEY | References `DIM_BUSINESS_MANAGER(manager_key)` |
| `quantity` | INTEGER | | Volume ordered |
| `unit_price` | DECIMAL | | Unit selling price |
| `discount_amount` | DECIMAL | | Concession discount amount |
| `gross_revenue` | DECIMAL | | Calculated: $\text{quantity} \times \text{unit\_price}$ |
| `net_revenue` | DECIMAL | | Calculated: $\text{gross\_revenue} - \text{discount\_amount}$ |

#### `FACT_CUSTOMER_VISIT` (Physical Visit Event Fact)
| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `visit_id` | INTEGER | PRIMARY KEY | Visit event surrogate key |
| `customer_key` | INTEGER | FOREIGN KEY | References `DIM_CUSTOMER(customer_key)` |
| `division_visited` | TEXT | | Corporate division visited |
| `visit_date_key` | INTEGER | FOREIGN KEY | References `DIM_DATE(date_key)` |
| `assisting_manager_key` | INTEGER | FOREIGN KEY | References `DIM_BUSINESS_MANAGER(manager_key)` |
| `visit_count` | INTEGER | | Visit unit event metric |

#### `FACT_SALES_MONTHLY_AGG` (Monthly Summary Data Mart)
| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `agg_id` | INTEGER | PRIMARY KEY | Aggregate summary row surrogate key |
| `year_month` | TEXT | | Year-month string (`YYYY-MM`) |
| `region` | TEXT | | Order placement region |
| `product_key` | INTEGER | FOREIGN KEY | References `DIM_PRODUCT(product_key)` |
| `location_type` | TEXT | | Fulfillment location facility type |
| `total_quantity` | INTEGER | | Aggregate sum of item quantities |
| `total_net_revenue` | DECIMAL | | Aggregate sum of net revenue |
| `order_line_count` | INTEGER | | Total count of atomic fact line items |
| `refresh_timestamp` | TEXT | | Timestamp when aggregate mart was refreshed |

---

### 3.4 Data Quality Control Table

#### `ETL_REJECT_LOG` (Quarantine Table)
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `reject_id` | INTEGER PRIMARY KEY | Quarantine reject identifier |
| `run_id` | TEXT | Unique pipeline execution run GUID |
| `source_entity` | TEXT | Target entity (e.g. 'FACT_SALES_ORDER_LINE') |
| `record_identifier` | TEXT | Natural order key (e.g. 'ORD-2024-005-1') |
| `reject_reason` | TEXT | Explanation for rejection |
| `raw_record_json` | TEXT | JSON dump of input transactional record |
| `rejected_at` | TEXT | Timestamp when record was quarantined |

---

## 4. End-to-End Execution Flow

```
1. main.py CLI Start
   │
   ├──► 2. Run Database Migrations (sql/migrations/*.sql)
   │
   ├──► 3. Load Conformed & SCD2 Dimensions (src/etl/dimensions_loader.py)
   │
   ├──► 4. Load Customer-Manager Bridge (src/etl/bridge_loader.py)
   │
   ├──► 5. Ingest & Validate Facts (src/etl/facts_loader.py)
   │      ├─ Check Fulfillment Facility Rule
   │      ├─ If Sales Office ──► Write to ETL_REJECT_LOG
   │      └─ If Valid ─────────► Insert into FACT_SALES_ORDER_LINE
   │
   ├──► 6. Refresh Aggregate Mart (src/etl/aggregate_loader.py)
   │
   └──► 7. Perform Reconciliation (src/analytics/reports.py)
```
