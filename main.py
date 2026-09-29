# Import standard library module for parsing command line arguments and flags
import argparse
# Import standard library sys module for execution environment control
import sys
# Import json module for formatting reconciliation output dictionaries
import json

# Import DatabaseConnection wrapper class managing SQLite or DuckDB connection pooling
from src.database.connection import DatabaseConnection
# Import schema migration function to initialize target data warehouse tables and constraints
from src.database.schema import run_migrations
# Import dimension ETL loader function to populate SCD dimensions
from src.etl.dimensions_loader import load_all_dimensions
# Import bridge table loader to maintain many-to-many relationships
from src.etl.bridge_loader import load_bridge
# Import fact table loaders for customer visits and sales order lines
from src.etl.facts_loader import load_customer_visits, load_sales_order_lines
# Import aggregate table refresh function for monthly business summary reporting
from src.etl.aggregate_loader import refresh_monthly_aggregates
# Import analytics functions for sales reporting and atomic-to-aggregate reconciliation checks
from src.analytics.reports import (
    get_detailed_monthly_sales_report,
    get_monthly_sales_trend,
    reconcile_atomic_and_aggregate
)
# Import custom logger setup helper for structured execution logs
from src.utils.logger import setup_logger

# Initialize application logger instance with component tag 'MainRunner'
logger = setup_logger("MainRunner")

# Master pipeline orchestrator function running the 6-step ETL sequence end-to-end
def run_pipeline(db_path: str = "sales_warehouse.db", use_duckdb: bool = False):
    """Orchestrate end-to-end Enterprise Sales Analytics Pipeline execution.
    
    Steps:
      1. Run Database Migrations (DDL setup)
      2. Load Dimension Tables (Customer, Store, Product, Territory, Promotion, Date)
      3. Load Bridge Tables (Customer-Store many-to-many relationship)
      4. Load Fact Tables (Customer Visits, Sales Order Lines)
      5. Refresh Monthly Aggregate Marts
      6. Reconcile Atomic Fact Totals against Aggregate Mart Totals
    """
    logger.info("Initializing Enterprise Sales Analytics Pipeline...")
    # Instantiate database connection manager targeting SQLite or DuckDB based on use_duckdb flag
    db = DatabaseConnection(db_path=db_path, use_duckdb=use_duckdb)
    
    # Step 1: Run DDL migrations to ensure all target schemas and control tables exist
    run_migrations(db)

    # Step 2: Load Slowly Changing Dimensions (SCD Type 2 / Type 1) and lookup dimensions
    load_all_dimensions(db)

    # Step 3: Load customer-store many-to-many bridge mapping table
    load_bridge(db)

    # Step 4: Load granular transactional facts (customer visits and sales order line items)
    load_customer_visits(db)
    load_sales_order_lines(db)

    # Step 5: Refresh monthly aggregated business sales summary data mart
    refresh_monthly_aggregates(db)

    # Step 6: Perform atomic vs aggregate data reconciliation to verify metrics match exactly
    recon = reconcile_atomic_and_aggregate(db)
    logger.info(f"Reconciliation Status: {'SUCCESS (PASS)' if recon['reconciled'] else 'FAILED'}")
    logger.info(f"Atomic Totals: {recon['atomic_totals']}")
    logger.info(f"Aggregate Totals: {recon['aggregate_totals']}")

    # Close database connection cleanly upon completion
    db.close()
    return recon

# Main CLI entrypoint parsing arguments and invoking requested action
def main():
    """CLI entrypoint for managing Enterprise Sales Analytics Data Warehouse operations."""
    parser = argparse.ArgumentParser(description="Enterprise Sales Analytics Warehouse CLI")
    # Define CLI sub-action flag supporting full-run, migrate, reconcile, or report
    parser.add_argument("--action", choices=["full-run", "migrate", "reconcile", "report"], default="full-run")
    # Define database file path argument (defaults to local sales_warehouse.db)
    parser.add_argument("--db", default="sales_warehouse.db")
    # Define flag to toggle DuckDB engine instead of standard SQLite engine
    parser.add_argument("--duckdb", action="store_true")
    args = parser.parse_args()

    # Open database connection for requested CLI subcommand execution
    db = DatabaseConnection(db_path=args.db, use_duckdb=args.duckdb)

    # Branch execution based on chosen CLI action
    if args.action == "full-run":
        # Run complete 6-step pipeline sequence
        run_pipeline(args.db, args.duckdb)
    elif args.action == "migrate":
        # Run DDL schema migrations only
        run_migrations(db)
    elif args.action == "reconcile":
        # Execute reconciliation check and output JSON results
        recon = reconcile_atomic_and_aggregate(db)
        print(json.dumps(recon, indent=2))
    elif args.action == "report":
        # Generate detailed monthly sales report and format stdout output
        report = get_detailed_monthly_sales_report(db)
        print("\n--- DETAILED MONTHLY SALES REPORT ---")
        for row in report:
            print(f"Customer: {row[0]} | Date: {row[1]} | Qty: {row[2]} | Net Revenue: ${row[3]:,.2f} | Location: {row[4]} ({row[5]}) | Manager: {row[6]}")
    
    # Close database connection cleanly
    db.close()

# Execute main() if script is launched directly from command line
if __name__ == "__main__":
    main()

