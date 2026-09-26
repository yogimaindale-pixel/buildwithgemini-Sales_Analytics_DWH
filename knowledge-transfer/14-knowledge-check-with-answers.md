# Module 14: Knowledge Check Self-Assessment

## Questions & Detailed Answers

### Question 1
What column in `DIM_LOCATION` indicates whether a row represents the currently active state of a location?
- **Answer**: `is_current` (boolean flag). When `TRUE`, the record is current (`effective_end_date = '9999-12-31'`).

### Question 2
What happens if an incoming sales order line specifies a `fulfillment_location_id` associated with a `'Sales Office'`?
- **Answer**: The order line is rejected by `src/etl/facts_loader.py`, quarantined in `ETL_REJECT_LOG`, and NOT loaded into `FACT_SALES_ORDER_LINE`.

### Question 3
How is `FACT_SALES_MONTHLY_AGG` kept consistent with `FACT_SALES_ORDER_LINE`?
- **Answer**: `refresh_monthly_aggregates()` truncates `FACT_SALES_MONTHLY_AGG` and recalculates all aggregates directly from `FACT_SALES_ORDER_LINE`, ensuring 100% reconciliation.
