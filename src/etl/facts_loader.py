import json
import uuid
import datetime
from src.database.connection import DatabaseConnection
from src.etl.seed_data import get_raw_visits, get_raw_order_lines
from src.utils.logger import setup_logger

logger = setup_logger("FactsLoader")

def load_customer_visits(db: DatabaseConnection):
    logger.info("Loading FACT_CUSTOMER_VISIT...")
    visits = get_raw_visits()
    for idx, v in enumerate(visits, start=1):
        cust_res = db.execute_query("SELECT customer_key FROM DIM_CUSTOMER WHERE customer_id = ? AND is_current = true", (v["customer_id"],))
        mgr_res = db.execute_query("SELECT manager_key FROM DIM_BUSINESS_MANAGER WHERE manager_id = ? AND is_current = true", (v["assisting_manager_id"],))
        date_key = int(v["visit_date"].replace("-", ""))
        
        if cust_res and mgr_res:
            cust_key = cust_res[0][0]
            mgr_key = mgr_res[0][0]

            check_q = "SELECT visit_id FROM FACT_CUSTOMER_VISIT WHERE visit_id = ?"
            if not db.execute_query(check_q, (idx,)):
                insert_q = """
                INSERT INTO FACT_CUSTOMER_VISIT (visit_id, customer_key, division_visited, visit_date_key, assisting_manager_key, visit_count)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                db.execute_query(insert_q, (idx, cust_key, v["division_visited"], date_key, mgr_key, v["visit_count"]))
    db.commit()
    logger.info("FACT_CUSTOMER_VISIT loaded.")

def load_sales_order_lines(db: DatabaseConnection, run_id: str = None):
    logger.info("Loading FACT_SALES_ORDER_LINE...")
    if not run_id:
        run_id = str(uuid.uuid4())[:8]

    order_lines = get_raw_order_lines()
    fact_id_counter = 1

    for ol in order_lines:
        order_date_key = int(ol["order_date"].replace("-", ""))
        order_date_str = ol["order_date"]

        # Resolve order location & fulfillment location
        order_loc_res = db.execute_query(
            "SELECT location_key, location_type FROM DIM_LOCATION WHERE location_id = ? AND effective_start_date <= ? AND effective_end_date >= ?",
            (ol["order_location_id"], order_date_str, order_date_str)
        )
        fulfil_loc_res = db.execute_query(
            "SELECT location_key, location_type FROM DIM_LOCATION WHERE location_id = ? AND effective_start_date <= ? AND effective_end_date >= ?",
            (ol["fulfillment_location_id"], order_date_str, order_date_str)
        )

        cust_res = db.execute_query(
            "SELECT customer_key FROM DIM_CUSTOMER WHERE customer_id = ? AND effective_start_date <= ? AND effective_end_date >= ?",
            (ol["customer_id"], order_date_str, order_date_str)
        )
        prod_res = db.execute_query(
            "SELECT product_key FROM DIM_PRODUCT WHERE product_id = ? AND effective_start_date <= ? AND effective_end_date >= ?",
            (ol["product_id"], order_date_str, order_date_str)
        )
        mgr_res = db.execute_query(
            "SELECT manager_key FROM DIM_BUSINESS_MANAGER WHERE manager_id = ? AND effective_start_date <= ? AND effective_end_date >= ?",
            (ol["manager_id"], order_date_str, order_date_str)
        )

        # FULFILLMENT ELIGIBILITY RULE CHECK
        if fulfil_loc_res:
            fulfil_loc_key, fulfil_loc_type = fulfil_loc_res[0]
            if fulfil_loc_type not in ("Warehouse", "Manufacturing"):
                reason = f"Ineligible fulfillment location type '{fulfil_loc_type}'. Must be Warehouse or Manufacturing."
                logger.warning(f"Quarantining order line {ol['order_number']}-{ol['line_number']}: {reason}")
                
                # Log quarantine reject
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
                continue

        if order_loc_res and fulfil_loc_res and cust_res and prod_res and mgr_res:
            order_loc_key = order_loc_res[0][0]
            fulfil_loc_key = fulfil_loc_res[0][0]
            cust_key = cust_res[0][0]
            prod_key = prod_res[0][0]
            mgr_key = mgr_res[0][0]

            qty = ol["quantity"]
            price = ol["unit_price"]
            disc = ol["discount_amount"]
            gross_rev = qty * price
            net_rev = gross_rev - disc

            check_q = "SELECT fact_id FROM FACT_SALES_ORDER_LINE WHERE order_number = ? AND line_number = ?"
            if not db.execute_query(check_q, (ol["order_number"], ol["line_number"])):
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

    db.commit()
    logger.info("FACT_SALES_ORDER_LINE loaded.")
