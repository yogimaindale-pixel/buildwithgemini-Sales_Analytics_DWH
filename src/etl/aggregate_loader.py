# Module docstring explaining monthly business aggregate refresh ETL logic
"""Aggregate Loader Module handling pre-computed monthly business sales aggregate summary tables."""

# Import datetime module for generating refresh timestamps
import datetime
# Import DatabaseConnection wrapper class
from src.database.connection import DatabaseConnection
# Import logger setup helper to log aggregate loading progress
from src.utils.logger import setup_logger

# Initialize logger instance for aggregate loader module
logger = setup_logger("AggregateLoader")

# Function executing idempotent full refresh of FACT_SALES_MONTHLY_AGG data mart
def refresh_monthly_aggregates(db: DatabaseConnection):
    """Rebuild monthly sales aggregate summary table from atomic transactional order lines.

    Args:
        db (DatabaseConnection): Active database connection instance.
    """
    logger.info("Refreshing FACT_SALES_MONTHLY_AGG from atomic facts...")
    
    # Clear existing aggregate records to guarantee idempotent full refresh
    db.execute_query("DELETE FROM FACT_SALES_MONTHLY_AGG;")

    # SQL query aggregating atomic order line facts by Year-Month, Order Region, Product, and Fulfillment Location Type
    query = """
    SELECT 
        d.year_month,
        loc_ord.region,
        f.product_key,
        loc_ful.location_type,
        SUM(f.quantity) as total_quantity,
        SUM(f.net_revenue) as total_net_revenue,
        COUNT(f.fact_id) as order_line_count
    FROM FACT_SALES_ORDER_LINE f
    JOIN DIM_DATE d ON f.order_date_key = d.date_key
    JOIN DIM_LOCATION loc_ord ON f.order_location_key = loc_ord.location_key
    JOIN DIM_LOCATION loc_ful ON f.fulfillment_location_key = loc_ful.location_key
    GROUP BY d.year_month, loc_ord.region, f.product_key, loc_ful.location_type
    ORDER BY d.year_month, loc_ord.region;
    """
    
    # Execute aggregate SQL query and retrieve aggregated summary rows
    rows = db.execute_query(query)
    # Current timestamp string for tracking refresh lineage
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Iterate through aggregated summary rows and insert into FACT_SALES_MONTHLY_AGG mart
    for idx, r in enumerate(rows, start=1):
        year_month, region, product_key, location_type, total_qty, total_net_rev, line_cnt = r
        insert_q = """
        INSERT INTO FACT_SALES_MONTHLY_AGG (
            agg_id, year_month, region, product_key, location_type,
            total_quantity, total_net_revenue, order_line_count, refresh_timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        db.execute_query(insert_q, (
            idx, year_month, region, product_key, location_type,
            total_qty, total_net_rev, line_cnt, now_str
        ))

    # Commit pending write transactions
    db.commit()
    logger.info(f"FACT_SALES_MONTHLY_AGG refreshed with {len(rows)} aggregate groups.")

