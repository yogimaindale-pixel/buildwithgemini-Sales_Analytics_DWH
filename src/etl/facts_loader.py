# Module docstring explaining transactional fact table loading logic for visits and order lines
"""Facts Loader Module handling transactional fact table population and quality validation rules."""

# Import json module for serializing raw rejected records into JSON strings
import json
# Import uuid module for generating unique run execution identifiers
import uuid
# Import datetime module for logging rejection timestamps
import datetime

# Import DatabaseConnection wrapper class
from src.database.connection import DatabaseConnection
# Import raw mock seed data visit and order line retrieval helper functions
from src.etl.seed_data import get_raw_visits, get_raw_order_lines
# Import logger setup helper to log fact ETL progress
from src.utils.logger import setup_logger

# Initialize logger instance for facts loader module
logger = setup_logger("FactsLoader")

# Function populating FACT_CUSTOMER_VISIT table
def load_customer_visits(db: DatabaseConnection):
    """Load customer physical visit events into FACT_CUSTOMER_VISIT.

    Args:
        db (DatabaseConnection): Active database connection instance.
    """
    logger.info("Loading FACT_CUSTOMER_VISIT...")
    visits = get_raw_visits()
    
    # Iterate through visit records with index-based visit_id
    for idx, v in enumerate(visits, start=1):
        # Resolve active customer surrogate key
        cust_res = db.execute_query("SELECT customer_key FROM DIM_CUSTOMER WHERE customer_id = ? AND is_current = true", (v["customer_id"],))
        # Resolve active assisting manager surrogate key
        mgr_res = db.execute_query("SELECT manager_key FROM DIM_BUSINESS_MANAGER WHERE manager_id = ? AND is_current = true", (v["assisting_manager_id"],))
        # Format ISO visit date string ('2024-03-15') into integer date_key (20240315)
        date_key = int(v["visit_date"].replace("-", ""))
        
        # Verify referential integrity before inserting fact record
        if cust_res and mgr_res:
            cust_key = cust_res[0][0]
            mgr_key = mgr_res[0][0]

            # Check if visit_id already exists to prevent duplicate loading
            check_q = "SELECT visit_id FROM FACT_CUSTOMER_VISIT WHERE visit_id = ?"
            if not db.execute_query(check_q, (idx,)):
                # Insert customer visit fact record
                insert_q = """
                INSERT INTO FACT_CUSTOMER_VISIT (visit_id, customer_key, division_visited, visit_date_key, assisting_manager_key, visit_count)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                db.execute_query(insert_q, (idx, cust_key, v["division_visited"], date_key, mgr_key, v["visit_count"]))
                
    # Commit pending visit inserts to database
    db.commit()
    logger.info("FACT_CUSTOMER_VISIT loaded.")

# Function populating granular FACT_SALES_ORDER_LINE table with quality validation & reject logging
def load_sales_order_lines(db: DatabaseConnection, run_id: str = None):
    """Load sales order line items into FACT_SALES_ORDER_LINE with fulfillment eligibility checks.

    Args:
        db (DatabaseConnection): Active database connection instance.
        run_id (str, optional): Unique execution run identifier for audit logging.
    """
    logger.info("Loading FACT_SALES_ORDER_LINE...")
    # Generate random 8-character execution run_id if not provided
    if not run_id:
        run_id = str(uuid.uuid4())[:8]

    order_lines = get_raw_order_lines()
    fact_id_counter = 1

    # Iterate through transactional sales order line items
    for ol in order_lines:
        # Convert transaction order date into integer surrogate key date_key
        order_date_key = int(ol["order_date"].replace("-", ""))
        order_date_str = ol["order_date"]

        # Resolve point-in-time order placement location key based on effective date range
        order_loc_res = db.execute_query(
            "SELECT location_key, location_type FROM DIM_LOCATION WHERE location_id = ? AND effective_start_date <= ? AND effective_end_date >= ?",
            (ol["order_location_id"], order_date_str, order_date_str)
        )
        # Resolve point-in-time fulfillment location key based on effective date range
        fulfil_loc_res = db.execute_query(
            "SELECT location_key, location_type FROM DIM_LOCATION WHERE location_id = ? AND effective_start_date <= ? AND effective_end_date >= ?",
            (ol["fulfillment_location_id"], order_date_str, order_date_str)
        )

        # Resolve point-in-time customer surrogate key
        cust_res = db.execute_query(
            "SELECT customer_key FROM DIM_CUSTOMER WHERE customer_id = ? AND effective_start_date <= ? AND effective_end_date >= ?",
            (ol["customer_id"], order_date_str, order_date_str)
        )
        # Resolve point-in-time product surrogate key
        prod_res = db.execute_query(
            "SELECT product_key FROM DIM_PRODUCT WHERE product_id = ? AND effective_start_date <= ? AND effective_end_date >= ?",
            (ol["product_id"], order_date_str, order_date_str)
        )
        # Resolve point-in-time sales business manager surrogate key
        mgr_res = db.execute_query(
            "SELECT manager_key FROM DIM_BUSINESS_MANAGER WHERE manager_id = ? AND effective_start_date <= ? AND effective_end_date >= ?",
            (ol["manager_id"], order_date_str, order_date_str)
        )

        # BUSINESS RULE ENFORCEMENT: FULFILLMENT LOCATION ELIGIBILITY CHECK
        # Order fulfillment is ONLY permitted from 'Warehouse' or 'Manufacturing' facilities (Sales Offices are ineligible)
        if fulfil_loc_res:
            fulfil_loc_key, fulfil_loc_type = fulfil_loc_res[0]
            if fulfil_loc_type not in ("Warehouse", "Manufacturing"):
                reason = f"Ineligible fulfillment location type '{fulfil_loc_type}'. Must be Warehouse or Manufacturing."
                logger.warning(f"Quarantining order line {ol['order_number']}-{ol['line_number']}: {reason}")
                
                # Log quarantine rejection entry into ETL_REJECT_LOG control table
                reject_q = """
                INSERT INTO ETL_REJECT_LOG (reject_id, run_id, source_entity, record_identifier, reject_reason, raw_record_json, rejected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                rej_count = db.execute_query("SELECT COUNT(*) FROM ETL_REJECT_LOG")[0][0] + 1
                db.execute_query(reject_q, (
                    rej_count, run_id, "FACT_SALES_ORDER_LINE",
                    f"{ol['order_number']}-{ol['line_number']}", reason,
                    json.dumps(ol), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                # Skip loading quarantined record into production fact table
                continue

        # If all dimension surrogate keys resolved successfully, insert order line fact
        if order_loc_res and fulfil_loc_res and cust_res and prod_res and mgr_res:
            order_loc_key = order_loc_res[0][0]
            fulfil_loc_key = fulfil_loc_res[0][0]
            cust_key = cust_res[0][0]
            prod_key = prod_res[0][0]
            mgr_key = mgr_res[0][0]

            # Calculate financial revenue measures
            qty = ol["quantity"]
            price = ol["unit_price"]
            disc = ol["discount_amount"]
            gross_rev = qty * price # Gross Revenue = Quantity * Unit Price
            net_rev = gross_rev - disc # Net Revenue = Gross Revenue - Discount Amount

            # Check if order line fact already exists
            check_q = "SELECT fact_id FROM FACT_SALES_ORDER_LINE WHERE order_number = ? AND line_number = ?"
            if not db.execute_query(check_q, (ol["order_number"], ol["line_number"])):
                # Insert validated transactional order line fact record
                insert_q = """
                INSERT INTO FACT_SALES_ORDER_LINE (
                    fact_id, order_number, line_number, order_date_key, order_location_key,
                    fulfillment_location_key, customer_key, product_key, business_manager_key,
                    quantity, unit_price, discount_amount, gross_revenue, net_revenue
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                db.execute_query(insert_q, (
                    fact_id_counter, ol["order_number"], ol["line_number"], order_date_key,
                    order_loc_key, fulfil_loc_key, cust_key, prod_key, mgr_key,
                    qty, price, disc, gross_rev, net_rev
                ))
                fact_id_counter += 1

    # Commit pending write transactions to database
    db.commit()
    logger.info("FACT_SALES_ORDER_LINE loaded.")

