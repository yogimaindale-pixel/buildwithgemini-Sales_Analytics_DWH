# Rollback Guide

## Purpose & Scope
This guide outlines the procedures for reverting database migrations, ETL code deployments, or configuration updates for the Enterprise Sales Analytics Data Warehouse.

---

## Rollback Procedures

### Procedure 1: Database Migration Rollback
1. Stop any active ETL pipeline execution:
   ```bash
   pkill -f main.py
   ```
2. Restore database from pre-deployment snapshot:
   ```bash
   cp sales_warehouse.db.backup sales_warehouse.db
   ```
3. Verify restored state:
   ```bash
   python3 main.py --action reconcile
   ```

### Procedure 2: Code Version Rollback
1. Checkout target git tag or previous release commit:
   ```bash
   git checkout v1.0.0
   ```
2. Re-run validation test suite:
   ```bash
   python3 -m unittest discover -s tests -p "test_*.py"
   ```
