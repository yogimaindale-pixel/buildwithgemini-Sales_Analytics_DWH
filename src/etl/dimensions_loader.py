# Module docstring explaining dimensional loading ETL operations for all warehouse master entities
"""Dimensions Loader Module for Enterprise Sales Analytics Data Warehouse.

This module populates all dimensional tables in the data warehouse:
  - DIM_DATE: Static calendar dimension for time-series analysis.
  - DIM_LOCATION: Slowly Changing Dimension (SCD Type 2) tracking regional sales offices and warehouses.
  - DIM_CUSTOMER: SCD Type 2 dimension maintaining customer history.
  - DIM_BUSINESS_MANAGER: SCD Type 2 dimension tracking sales managers.
  - DIM_PRODUCT: SCD Type 2 dimension tracking product catalog and pricing.
"""

# Import DatabaseConnection wrapper class
from src.database.connection import DatabaseConnection
# Import raw mock seed data retrieval helper functions
from src.etl.seed_data import (
    get_raw_dates,
    get_raw_locations,
    get_raw_customers,
    get_raw_managers,
    get_raw_products
)
# Import logger setup helper to output dimensional ETL execution progress
from src.utils.logger import setup_logger

# Initialize logger instance for dimensions loader module
logger = setup_logger("DimensionsLoader")

# Function loading static calendar date dimension DIM_DATE
def load_dates(db: DatabaseConnection):
    """Load static calendar dates into DIM_DATE.

    Args:
        db (DatabaseConnection): Active database connection instance.
    """
    logger.info("Loading static calendar dimension DIM_DATE...")
    dates = get_raw_dates()
    
    # Iterate through each generated date record dictionary
    for d in dates:
        # Check if date_key already exists in target table to enforce idempotency
        check_q = "SELECT date_key FROM DIM_DATE WHERE date_key = ?"
        if not db.execute_query(check_q, (d["date_key"],)):
            # Insert new calendar date record if missing
            insert_q = """
            INSERT INTO DIM_DATE (date_key, full_date, year, quarter, month, month_name, day_of_month, day_of_week, day_name, year_month, is_weekend)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(insert_q, (
                d["date_key"], d["full_date"], d["year"], d["quarter"], d["month"],
                d["month_name"], d["day_of_month"], d["day_of_week"], d["day_name"],
                d["year_month"], d["is_weekend"]
            ))
            
    # Commit pending dimension inserts to database
    db.commit()
    logger.info("DIM_DATE loaded successfully.")

# Function loading location entities into DIM_LOCATION with SCD Type 2 attributes
def load_locations(db: DatabaseConnection):
    """Load SCD Type 2 location entities (warehouses, sales offices) into DIM_LOCATION.

    Args:
        db (DatabaseConnection): Active database connection instance.
    """
    logger.info("Loading location dimension DIM_LOCATION...")
    locations = get_raw_locations()
    
    # Enumerate location entity records starting with surrogate key index 1
    for idx, loc in enumerate(locations, start=1):
        # Check if location_id and version_number combination already exists
        check_q = "SELECT location_key FROM DIM_LOCATION WHERE location_id = ? AND version_number = ?"
        res = db.execute_query(check_q, (loc["location_id"], loc["version_number"]))
        if not res:
            # Insert location entity record with effective date range and version number
            insert_q = """
            INSERT INTO DIM_LOCATION (location_key, location_id, location_name, location_type, region, effective_start_date, effective_end_date, is_current, version_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(insert_q, (
                idx, loc["location_id"], loc["location_name"], loc["location_type"],
                loc["region"], loc["effective_start_date"], loc["effective_end_date"],
                loc["is_current"], loc["version_number"]
            ))
            
    # Commit pending inserts
    db.commit()
    logger.info("DIM_LOCATION loaded successfully.")

# Function loading customer profile entities into DIM_CUSTOMER with SCD Type 2 attributes
def load_customers(db: DatabaseConnection):
    """Load SCD Type 2 customer entities into DIM_CUSTOMER.

    Args:
        db (DatabaseConnection): Active database connection instance.
    """
    logger.info("Loading customer dimension DIM_CUSTOMER...")
    customers = get_raw_customers()
    
    # Enumerate customer profile records starting with surrogate key index 1
    for idx, cust in enumerate(customers, start=1):
        # Check if customer_id and version_number combination exists
        check_q = "SELECT customer_key FROM DIM_CUSTOMER WHERE customer_id = ? AND version_number = ?"
        res = db.execute_query(check_q, (cust["customer_id"], cust["version_number"]))
        if not res:
            # Insert customer profile record with status and versioning metadata
            insert_q = """
            INSERT INTO DIM_CUSTOMER (customer_key, customer_id, customer_name, customer_type, status, effective_start_date, effective_end_date, is_current, version_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(insert_q, (
                idx, cust["customer_id"], cust["customer_name"], cust["customer_type"],
                cust["status"], cust["effective_start_date"], cust["effective_end_date"],
                cust["is_current"], cust["version_number"]
            ))
            
    # Commit pending inserts
    db.commit()
    logger.info("DIM_CUSTOMER loaded successfully.")

# Function loading sales business manager entities into DIM_BUSINESS_MANAGER
def load_managers(db: DatabaseConnection):
    """Load SCD Type 2 business manager entities into DIM_BUSINESS_MANAGER.

    Args:
        db (DatabaseConnection): Active database connection instance.
    """
    logger.info("Loading business manager dimension DIM_BUSINESS_MANAGER...")
    managers = get_raw_managers()
    
    # Enumerate manager records starting with surrogate key index 1
    for idx, mgr in enumerate(managers, start=1):
        # Check if manager_id and version_number combination exists
        check_q = "SELECT manager_key FROM DIM_BUSINESS_MANAGER WHERE manager_id = ? AND version_number = ?"
        res = db.execute_query(check_q, (mgr["manager_id"], mgr["version_number"]))
        if not res:
            # Insert sales manager record with assigned business division
            insert_q = """
            INSERT INTO DIM_BUSINESS_MANAGER (manager_key, manager_id, manager_name, division, effective_start_date, effective_end_date, is_current, version_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(insert_q, (
                idx, mgr["manager_id"], mgr["manager_name"], mgr["division"],
                mgr["effective_start_date"], mgr["effective_end_date"],
                mgr["is_current"], mgr["version_number"]
            ))
            
    # Commit pending inserts
    db.commit()
    logger.info("DIM_BUSINESS_MANAGER loaded successfully.")

# Function loading product catalog entities into DIM_PRODUCT
def load_products(db: DatabaseConnection):
    """Load SCD Type 2 product catalog into DIM_PRODUCT.

    Args:
        db (DatabaseConnection): Active database connection instance.
    """
    logger.info("Loading product dimension DIM_PRODUCT...")
    products = get_raw_products()
    
    # Enumerate product catalog records starting with surrogate key index 1
    for idx, prod in enumerate(products, start=1):
        # Check if product_id and version_number combination exists
        check_q = "SELECT product_key FROM DIM_PRODUCT WHERE product_id = ? AND version_number = ?"
        res = db.execute_query(check_q, (prod["product_id"], prod["version_number"]))
        if not res:
            # Insert product catalog record with unit price and category attributes
            insert_q = """
            INSERT INTO DIM_PRODUCT (product_key, product_id, product_name, category, unit_price, effective_start_date, effective_end_date, is_current, version_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(insert_q, (
                idx, prod["product_id"], prod["product_name"], prod["category"],
                prod["unit_price"], prod["effective_start_date"], prod["effective_end_date"],
                prod["is_current"], prod["version_number"]
            ))
            
    # Commit pending inserts
    db.commit()
    logger.info("DIM_PRODUCT loaded successfully.")

# Master orchestrator function loading all dimension tables in sequence
def load_all_dimensions(db: DatabaseConnection):
    """Execute complete dimensional loading sequence.

    Args:
        db (DatabaseConnection): Active database connection instance.
    """
    logger.info("Starting master dimension loading sequence...")
    load_dates(db)
    load_locations(db)
    load_customers(db)
    load_managers(db)
    load_products(db)
    logger.info("All dimensions loaded successfully.")


