# Module 01: Project and Business Overview

## Business Purpose
The Enterprise Sales Analytics Data Warehouse aggregates operational sales data across regional sales offices, warehouses, manufacturing facilities, customer accounts, and business manager divisions into a unified Kimball analytical warehouse.

## Key Business Concepts
1. **Sales Order vs. Fulfillment**: Orders originate at a sales office or channel, but must be fulfilled by an eligible warehouse or manufacturing facility.
2. **Business Manager Division Assignments**: Customers are assigned to business managers across specific divisions. These relationships evolve over time and are modeled using a temporal assignment bridge.
3. **Revenue Definitions**:
   - `Gross Revenue`: Total sales price before discounts (`Quantity * Unit Price`).
   - `Net Revenue`: Actual revenue realized (`Gross Revenue - Discount Amount`).
4. **Fulfillment Policy**: Orders cannot be fulfilled directly from sales offices. Any order attempting fulfillment from a non-warehouse/non-manufacturing location must be quarantined in `ETL_REJECT_LOG`.
