# Module 07: Local Setup, Configuration, and Execution Guide

## Prerequisites
- Python 3.10+
- SQLite3 or DuckDB Python package

## Step-by-Step Setup

1. **Navigate to project directory**:
   ```bash
   cd /config/Desktop/Session3
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run full ETL pipeline & initial setup**:
   ```bash
   python3 main.py --action full-run
   ```

4. **Verify reconciliation gate**:
   ```bash
   python3 main.py --action reconcile
   ```

5. **Generate detailed sales CLI report**:
   ```bash
   python3 main.py --action report
   ```

6. **Launch consumption web dashboard**:
   Open `reports/dashboard/index.html` in your web browser.
