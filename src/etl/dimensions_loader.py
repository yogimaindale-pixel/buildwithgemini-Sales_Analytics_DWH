from src.database.connection import DatabaseConnection
from src.etl.seed_data import (
    get_raw_dates,
    get_raw_locations,
    get_raw_customers,
    get_raw_managers,
    get_raw_products
)
from src.utils.logger import setup_logger

logger = setup_logger("DimensionsLoader")

def load_dates(db: DatabaseConnection):
    logger.info("Loading DIM_DATE...")
    dates = get_raw_dates()
    for d in dates:
        query = """
        INSERT INTO DIM_DATE (date_key, full_date, year, quarter, month, month_name, day_of_month, day_of_week, day_name, year_month, is_weekend)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (date_key) DO NOTHING;
        """
        try:
            db.execute_query(query, (
                d["date_key"], d["full_date"], d["year"], d["quarter"], d["month"],
                d["month_name"], d["day_of_month"], d["day_of_week"], d["day_name"],
                d["year_month"], d["is_weekend"]
            ))
        except Exception:
            # Fallback for sqlite/duckdb without ON CONFLICT syntax
            check_q = "SELECT date_key FROM DIM_DATE WHERE date_key = ?"
            if not db.execute_query(check_q, (d["date_key"],)):
                insert_q = """
                INSERT INTO DIM_DATE (date_key, full_date, year, quarter, month, month_name, day_of_month, day_of_week, day_name, year_month, is_weekend)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                db.execute_query(insert_q, (
                    d["date_key"], d["full_date"], d["year"], d["quarter"], d["month"],
                    d["month_name"], d["day_of_month"], d["day_of_week"], d["day_name"],
                    d["year_month"], d["is_weekend"]
                ))
    db.commit()
    logger.info("DIM_DATE loaded.")

def load_locations(db: DatabaseConnection):
    logger.info("Loading DIM_LOCATION...")
    locations = get_raw_locations()
    for idx, loc in enumerate(locations, start=1):
        check_q = "SELECT location_key FROM DIM_LOCATION WHERE location_id = ? AND version_number = ?"
        res = db.execute_query(check_q, (loc["location_id"], loc["version_number"]))
        if not res:
            insert_q = """
            INSERT INTO DIM_LOCATION (location_key, location_id, location_name, location_type, region, effective_start_date, effective_end_date, is_current, version_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(insert_q, (
                idx, loc["location_id"], loc["location_name"], loc["location_type"],
                loc["region"], loc["effective_start_date"], loc["effective_end_date"],
                loc["is_current"], loc["version_number"]
            ))
    db.commit()
    logger.info("DIM_LOCATION loaded.")

def load_customers(db: DatabaseConnection):
    logger.info("Loading DIM_CUSTOMER...")
    customers = get_raw_customers()
    for idx, cust in enumerate(customers, start=1):
        check_q = "SELECT customer_key FROM DIM_CUSTOMER WHERE customer_id = ? AND version_number = ?"
        res = db.execute_query(check_q, (cust["customer_id"], cust["version_number"]))
        if not res:
            insert_q = """
            INSERT INTO DIM_CUSTOMER (customer_key, customer_id, customer_name, customer_type, status, effective_start_date, effective_end_date, is_current, version_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(insert_q, (
                idx, cust["customer_id"], cust["customer_name"], cust["customer_type"],
                cust["status"], cust["effective_start_date"], cust["effective_end_date"],
                cust["is_current"], cust["version_number"]
            ))
    db.commit()
    logger.info("DIM_CUSTOMER loaded.")

def load_managers(db: DatabaseConnection):
    logger.info("Loading DIM_BUSINESS_MANAGER...")
    managers = get_raw_managers()
    for idx, mgr in enumerate(managers, start=1):
        check_q = "SELECT manager_key FROM DIM_BUSINESS_MANAGER WHERE manager_id = ? AND version_number = ?"
        res = db.execute_query(check_q, (mgr["manager_id"], mgr["version_number"]))
        if not res:
            insert_q = """
            INSERT INTO DIM_BUSINESS_MANAGER (manager_key, manager_id, manager_name, division, effective_start_date, effective_end_date, is_current, version_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(insert_q, (
                idx, mgr["manager_id"], mgr["manager_name"], mgr["division"],
                mgr["effective_start_date"], mgr["effective_end_date"],
                mgr["is_current"], mgr["version_number"]
            ))
    db.commit()
    logger.info("DIM_BUSINESS_MANAGER loaded.")

def load_products(db: DatabaseConnection):
    logger.info("Loading DIM_PRODUCT...")
    products = get_raw_products()
    for idx, prod in enumerate(products, start=1):
        check_q = "SELECT product_key FROM DIM_PRODUCT WHERE product_id = ? AND version_number = ?"
        res = db.execute_query(check_q, (prod["product_id"], prod["version_number"]))
        if not res:
            insert_q = """
            INSERT INTO DIM_PRODUCT (product_key, product_id, product_name, category, unit_price, effective_start_date, effective_end_date, is_current, version_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(insert_q, (
                idx, prod["product_id"], prod["product_name"], prod["category"],
                prod["unit_price"], prod["effective_start_date"], prod["effective_end_date"],
                prod["is_current"], prod["version_number"]
            ))
    db.commit()
    logger.info("DIM_PRODUCT loaded.")

def load_all_dimensions(db: DatabaseConnection):
    load_dates(db)
    load_locations(db)
    load_customers(db)
    load_managers(db)
    load_products(db)
