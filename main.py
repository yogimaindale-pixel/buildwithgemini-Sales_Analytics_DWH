import argparse
import sys
import json
from src.database.connection import DatabaseConnection
from src.database.schema import run_migrations
from src.etl.dimensions_loader import load_all_dimensions
from src.etl.bridge_loader import load_bridge
from src.etl.facts_loader import load_customer_visits, load_sales_order_lines
from src.etl.aggregate_loader import refresh_monthly_aggregates
from src.analytics.reports import (
    get_detailed_monthly_sales_report,
    get_monthly_sales_trend,
    reconcile_atomic_and_aggregate
)
from src.utils.logger import setup_logger

logger = setup_logger("MainRunner")

def run_pipeline(db_path: str = "sales_warehouse.db", use_duckdb: bool = False):
    logger.info("Initializing Enterprise Sales Analytics Pipeline...")
    db = DatabaseConnection(db_path=db_path, use_duckdb=use_duckdb)
    
    # Step 1: Run Migrations
    run_migrations(db)

    # Step 2: Load Dimensions
    load_all_dimensions(db)

    # Step 3: Load Bridge
    load_bridge(db)

    # Step 4: Load Facts
    load_customer_visits(db)
    load_sales_order_lines(db)

    # Step 5: Refresh Monthly Aggregates
    refresh_monthly_aggregates(db)

    # Step 6: Reconcile Data
    recon = reconcile_atomic_and_aggregate(db)
    logger.info(f"Reconciliation Status: {'SUCCESS (PASS)' if recon['reconciled'] else 'FAILED'}")
    logger.info(f"Atomic Totals: {recon['atomic_totals']}")
    logger.info(f"Aggregate Totals: {recon['aggregate_totals']}")

    db.close()
    return recon

def main():
    parser = argparse.ArgumentParser(description="Enterprise Sales Analytics Warehouse CLI")
    parser.add_argument("--action", choices=["full-run", "migrate", "reconcile", "report"], default="full-run")
    parser.add_argument("--db", default="sales_warehouse.db")
    parser.add_argument("--duckdb", action="store_true")
    args = parser.parse_args()

    db = DatabaseConnection(db_path=args.db, use_duckdb=args.duckdb)

    if args.action == "full-run":
        run_pipeline(args.db, args.duckdb)
    elif args.action == "migrate":
        run_migrations(db)
    elif args.action == "reconcile":
        recon = reconcile_atomic_and_aggregate(db)
        print(json.dumps(recon, indent=2))
    elif args.action == "report":
        report = get_detailed_monthly_sales_report(db)
        print("\n--- DETAILED MONTHLY SALES REPORT ---")
        for row in report:
            print(f"Customer: {row[0]} | Date: {row[1]} | Qty: {row[2]} | Net Revenue: ${row[3]:,.2f} | Location: {row[4]} ({row[5]}) | Manager: {row[6]}")
    db.close()

if __name__ == "__main__":
    main()
