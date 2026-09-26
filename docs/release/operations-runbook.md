# Operational Runbook - Enterprise Sales Analytics Data Warehouse

## System Overview
- **System**: Enterprise Sales Analytics Data Warehouse
- **Engine**: DuckDB / SQLite SQL Engine
- **Orchestrator**: `main.py`
- **Audit Logs**: `ETL_PIPELINE_RUNS`, `ETL_REJECT_LOG`

---

## Daily Operational Procedures

### 1. Execute Full Daily ETL Run
```bash
python3 main.py --action full-run
```
Expected output:
- Schema migrations applied / verified.
- Dimensions (`DIM_DATE`, `DIM_LOCATION`, `DIM_CUSTOMER`, `DIM_BUSINESS_MANAGER`, `DIM_PRODUCT`) loaded.
- `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT` loaded.
- `FACT_SALES_ORDER_LINE` loaded (invalid fulfillment locations quarantined in `ETL_REJECT_LOG`).
- `FACT_SALES_MONTHLY_AGG` refreshed.
- Reconciliation status: `SUCCESS (PASS)`.

### 2. Verify Atomic-to-Aggregate Reconciliation
```bash
python3 main.py --action reconcile
```

### 3. Generate Detailed Sales Report
```bash
python3 main.py --action report
```

---

## Troubleshooting & Emergency Procedures

| Symptom | Root Cause | Remediation Command |
| :--- | :--- | :--- |
| Fulfillment location rejection warning | Order contains fulfillment location type 'Sales Office' | Inspect `ETL_REJECT_LOG` for `reject_reason` |
| Reconciliation failure | Atomic facts and aggregate table totals out of sync | Run `python3 main.py --action full-run` to force full aggregate refresh |
| Lock error on database file | Concurrent access to `.db` file | Ensure previous process terminated: `pkill -f main.py` |
