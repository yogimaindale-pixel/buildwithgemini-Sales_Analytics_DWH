# Module docstring explaining business analytics reporting and data reconciliation functions
"""Analytics & Reporting Module providing detailed sales queries and atomic-to-aggregate reconciliation."""

# Import DatabaseConnection wrapper class
from src.database.connection import DatabaseConnection
# Import logger setup helper to log report execution
from src.utils.logger import setup_logger

# Initialize logger instance for reports engine
logger = setup_logger("ReportsEngine")

# Function querying detailed monthly transactional sales line items joined across dimensions
def get_detailed_monthly_sales_report(db: DatabaseConnection):
    """Retrieve line-item detailed sales report with customer, date, pricing, location, and manager details.

    Columns returned:
        0: customer_name
        1: order_date
        2: total_quantity
        3: total_revenue (net_revenue)
        4: sales_location (order_location_name)
        5: location_type
        6: business_manager_name
        7: order_number
    """
    # Query joining FACT_SALES_ORDER_LINE with DIM_CUSTOMER, DIM_DATE, DIM_LOCATION, and DIM_BUSINESS_MANAGER
    query = """
    SELECT 
        c.customer_name,
        d.full_date as order_date,
        f.quantity as total_quantity,
        f.net_revenue as total_revenue,
        loc_ord.location_name as sales_location,
        loc_ord.location_type as location_type,
        m.manager_name as business_manager_name,
        f.order_number
    FROM FACT_SALES_ORDER_LINE f
    JOIN DIM_CUSTOMER c ON f.customer_key = c.customer_key
    JOIN DIM_DATE d ON f.order_date_key = d.date_key
    JOIN DIM_LOCATION loc_ord ON f.order_location_key = loc_ord.location_key
    JOIN DIM_BUSINESS_MANAGER m ON f.business_manager_key = m.manager_key
    ORDER BY d.full_date ASC, f.order_number ASC;
    """
    return db.execute_query(query)

# Function querying monthly aggregated sales trends from FACT_SALES_MONTHLY_AGG
def get_monthly_sales_trend(db: DatabaseConnection):
    """Retrieve monthly sales performance metrics aggregated by year-month.

    Columns returned:
        0: year_month
        1: total_quantity
        2: total_net_revenue
        3: order_line_count
    """
    # Query summarizing FACT_SALES_MONTHLY_AGG data mart by year_month
    query = """
    SELECT 
        year_month,
        SUM(total_quantity) as total_quantity,
        SUM(total_net_revenue) as total_net_revenue,
        SUM(order_line_count) as order_line_count
    FROM FACT_SALES_MONTHLY_AGG
    GROUP BY year_month
    ORDER BY year_month ASC;
    """
    return db.execute_query(query)

# Function performing reconciliation check between atomic order lines and monthly aggregate mart
def reconcile_atomic_and_aggregate(db: DatabaseConnection) -> dict:
    """Reconcile total quantity, net revenue, and row counts between atomic and aggregate tables.

    Returns:
        dict: Reconciliation result dictionary containing 'reconciled' boolean flag and totals.
    """
    # Atomic query summing quantity, net revenue, and counting line records in FACT_SALES_ORDER_LINE
    atomic_q = "SELECT SUM(quantity), SUM(net_revenue), COUNT(fact_id) FROM FACT_SALES_ORDER_LINE;"
    # Aggregate query summing total_quantity, total_net_revenue, and order_line_count in FACT_SALES_MONTHLY_AGG
    agg_q = "SELECT SUM(total_quantity), SUM(total_net_revenue), SUM(order_line_count) FROM FACT_SALES_MONTHLY_AGG;"
    
    # Execute reconciliation queries
    atomic_res = db.execute_query(atomic_q)[0]
    agg_res = db.execute_query(agg_q)[0]

    # Evaluate exact equality for quantity and row count, and float delta < $0.01 for revenue
    reconciled = (
        atomic_res[0] == agg_res[0] and
        abs(float(atomic_res[1] or 0) - float(agg_res[1] or 0)) < 0.01 and
        atomic_res[2] == agg_res[2]
    )

    # Return structured dictionary report
    return {
        "reconciled": reconciled,
        "atomic_totals": {
            "total_quantity": atomic_res[0],
            "total_net_revenue": float(atomic_res[1] or 0),
            "order_line_count": atomic_res[2]
        },
        "aggregate_totals": {
            "total_quantity": agg_res[0],
            "total_net_revenue": float(agg_res[1] or 0),
            "order_line_count": agg_res[2]
        }
    }

