from src.database.connection import DatabaseConnection
from src.utils.logger import setup_logger

logger = setup_logger("ReportsEngine")

def get_detailed_monthly_sales_report(db: DatabaseConnection):
    """
    Detailed Monthly Sales Report:
    customer_name, order_date, total_quantity, total_revenue (net_revenue),
    sales_location (order_location_name), location_type, business_manager_name
    """
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

def get_monthly_sales_trend(db: DatabaseConnection):
    """
    Month Sales Trend:
    year_month, total_quantity, total_net_revenue, order_line_count
    """
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

def reconcile_atomic_and_aggregate(db: DatabaseConnection) -> dict:
    """
    Reconciles total net revenue and total quantity between FACT_SALES_ORDER_LINE and FACT_SALES_MONTHLY_AGG
    """
    atomic_q = "SELECT SUM(quantity), SUM(net_revenue), COUNT(fact_id) FROM FACT_SALES_ORDER_LINE;"
    agg_q = "SELECT SUM(total_quantity), SUM(total_net_revenue), SUM(order_line_count) FROM FACT_SALES_MONTHLY_AGG;"
    
    atomic_res = db.execute_query(atomic_q)[0]
    agg_res = db.execute_query(agg_q)[0]

    reconciled = (
        atomic_res[0] == agg_res[0] and
        abs(float(atomic_res[1] or 0) - float(agg_res[1] or 0)) < 0.01 and
        atomic_res[2] == agg_res[2]
    )

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
