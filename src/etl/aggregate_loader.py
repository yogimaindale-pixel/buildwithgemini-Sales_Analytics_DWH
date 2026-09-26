import datetime
from src.database.connection import DatabaseConnection
from src.utils.logger import setup_logger

logger = setup_logger("AggregateLoader")

def refresh_monthly_aggregates(db: DatabaseConnection):
    logger.info("Refreshing FACT_SALES_MONTHLY_AGG from atomic facts...")
    
    # Delete existing aggregate rows to make refresh idempotent
    db.execute_query("DELETE FROM FACT_SALES_MONTHLY_AGG;")

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
    
    rows = db.execute_query(query)
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

    db.commit()
    logger.info(f"FACT_SALES_MONTHLY_AGG refreshed with {len(rows)} aggregate groups.")
