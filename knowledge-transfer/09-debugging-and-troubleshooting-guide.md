# Module 09: Debugging and Troubleshooting Guide

## Common Issues & Diagnoses

### Issue 1: Order lines missing from `FACT_SALES_ORDER_LINE`
- **Symptom**: Expected order lines are not in the atomic fact table.
- **Cause**: The fulfillment location type for that order line is set to `'Sales Office'`.
- **Diagnosis**: Query `ETL_REJECT_LOG`:
  ```sql
  SELECT * FROM ETL_REJECT_LOG WHERE source_entity = 'FACT_SALES_ORDER_LINE';
  ```
- **Remediation**: Correct source system fulfillment location to an eligible Warehouse or Manufacturing facility.

### Issue 2: Reconciliation Mismatch Error
- **Symptom**: `reconcile_atomic_and_aggregate()` returns `reconciled = False`.
- **Cause**: Manual edits or partial ETL runs modified `FACT_SALES_ORDER_LINE` without refreshing `FACT_SALES_MONTHLY_AGG`.
- **Remediation**: Run `refresh_monthly_aggregates(db)` or `python3 main.py --action full-run`.
