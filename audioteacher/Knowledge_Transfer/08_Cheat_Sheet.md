# ⚡ 08. Enterprise Sales Analytics DWH Cheat Sheet

| Operation | Command | Purpose |
| :--- | :--- | :--- |
| **Run Pipeline** | `python3 main.py` | Executes schema migrations, dimension loading, facts, and reconciliation. |
| **Reset Database** | `python3 main.py --reset-db` | Re-initializes database schema from clean migration state. |
| **Run Unit Tests** | `PYTHONPATH=. pytest tests/` | Runs all 13 automated unit and integration tests. |
