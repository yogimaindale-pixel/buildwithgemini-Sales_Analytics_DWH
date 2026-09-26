# Module 08: Testing and Validation Guide

## Test Suite Architecture

The test suite in `tests/` covers unit, integration, and data quality requirements:

| Test File | Target Requirement | Scope |
| :--- | :--- | :--- |
| `test_dimensions_scd.py` | Dimension SCD Type 2 | Verifies non-null effective dates and row counts |
| `test_bridge_assignments.py` | Bridge integrity | Verifies no orphaned assignment keys |
| `test_fact_sales_order_line.py` | Atomic fact calculations | Verifies `gross_revenue` and `net_revenue` arithmetic |
| `test_fulfillment_rules.py` | Fulfillment policy | Verifies quarantine of sales office fulfillment attempts |
| `test_aggregate_reconciliation.py` | Data reconciliation | Verifies atomic sum == aggregate sum |
| `test_end_to_end_quality.py` | End-to-end execution | Runs full pipeline and verifies report output |

## Command to Run Tests
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
