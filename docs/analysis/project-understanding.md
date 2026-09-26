# Project Understanding & Domain Analysis

## Executive Summary
The Enterprise Sales Analytics Data Warehouse provides an end-to-end analytical data architecture for enterprise sales order processing, customer management, location tracking, and business manager performance evaluation. 

The analytical system follows Kimball dimensional modeling principles, incorporating Slowly Changing Dimensions (SCD Type 1 and Type 2), atomic sales order-line fact tracking, temporal bridge relationships for customer-manager assignments, and performance-optimized monthly aggregation layer.

---

## Business Objectives & Key Analytical Requirements
1. **Atomic Sales Performance**: Track individual order lines with granular measures (`Gross_Revenue`, `Net_Revenue`, `Quantity`, `Discount_Amount`) and degenerate order identifiers (`order_number`, `line_number`).
2. **Order vs. Fulfillment Location Tracking**: Differentiate between where an order was originated (`order_location_key`) and where it was fulfilled (`fulfillment_location_key`).
3. **Fulfillment Eligibility Governance**: Enforce business policy that order fulfillment is restricted exclusively to locations with `location_type` in `('Warehouse', 'Manufacturing')`.
4. **Temporal Customer-Manager Relationship**: Track customer assignments across business manager divisions over time using `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT` with effective start/end dates.
5. **Customer Visits**: Record customer division visits and assisting manager activities in `FACT_CUSTOMER_VISIT`.
6. **Monthly Aggregations**: Maintain `FACT_SALES_MONTHLY_AGG` derived strictly from atomic facts to accelerate high-level dashboard queries while ensuring 100% reconciliation with atomic facts.

---

## System Entities & Architecture Scope
- `DIM_DATE` (Type 0)
- `DIM_LOCATION` (Type 1 & 2: `location_name`, `location_type`, `region`)
- `DIM_CUSTOMER` (Type 1 & 2: `customer_name`, `customer_type`, `status`)
- `DIM_BUSINESS_MANAGER` (Type 1 & 2: `manager_name`, `division`)
- `DIM_PRODUCT` (Type 1 & 2: `product_name`, `category`, `unit_price`)
- `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT` (Temporal bridge table)
- `FACT_CUSTOMER_VISIT` (Supporting visit fact table)
- `FACT_SALES_ORDER_LINE` (Atomic fact table)
- `FACT_SALES_MONTHLY_AGG` (Derived aggregate fact table)
- `ETL_PIPELINE_RUNS` & `ETL_REJECT_LOG` (Control and quarantine system)
