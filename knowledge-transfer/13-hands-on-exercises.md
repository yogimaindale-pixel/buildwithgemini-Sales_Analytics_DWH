# Module 13: Hands-on Exercises for Junior Developers

## Lab 1: Query Quarantined Records
Write a SQL query against `ETL_REJECT_LOG` to extract all rejected order lines from the latest pipeline run.

```sql
SELECT record_identifier, reject_reason, rejected_at 
FROM ETL_REJECT_LOG 
ORDER BY rejected_at DESC;
```

---

## Lab 2: Add a New Product to Seed Data
1. Open `src/etl/seed_data.py`.
2. Add a new product dictionary to `get_raw_products()`.
3. Re-run `python3 main.py --action full-run`.
4. Verify the new product appears in `DIM_PRODUCT`.

---

## Lab 3: Verify Aggregate Reconciliation
Run the reconciliation CLI tool:
```bash
python3 main.py --action reconcile
```
Expected Output: `"reconciled": true`.
