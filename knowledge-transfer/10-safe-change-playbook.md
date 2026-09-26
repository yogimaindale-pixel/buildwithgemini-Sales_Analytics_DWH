# Module 10: Safe Change Playbook

## How to Make Schema & ETL Changes Safely

### Workflow: Adding a New Attribute to a Dimension

1. **Step 1: Update DDL Migration File**:
   Add new column to `sql/migrations/001_create_dimensions.sql` (or add new migration file `005_add_column.sql`).

2. **Step 2: Update Seed Data Generator**:
   Include new attribute in `src/etl/seed_data.py`.

3. **Step 3: Update Loader Module**:
   Modify insert/update SQL statements in `src/etl/dimensions_loader.py`.

4. **Step 4: Update Unit Tests**:
   Add assertions in `tests/test_dimensions_scd.py`.

5. **Step 5: Run Pipeline & Test Suite**:
   ```bash
   python3 main.py --action full-run
   python3 -m unittest discover -s tests -p "test_*.py"
   ```
