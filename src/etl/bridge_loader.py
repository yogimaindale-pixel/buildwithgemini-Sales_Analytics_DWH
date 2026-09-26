from src.database.connection import DatabaseConnection
from src.etl.seed_data import get_raw_assignments
from src.utils.logger import setup_logger

logger = setup_logger("BridgeLoader")

def load_bridge(db: DatabaseConnection):
    logger.info("Loading BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT...")
    assignments = get_raw_assignments()
    for idx, asgn in enumerate(assignments, start=1):
        # Resolve surrogate keys
        cust_res = db.execute_query("SELECT customer_key FROM DIM_CUSTOMER WHERE customer_id = ? AND is_current = true", (asgn["customer_id"],))
        mgr_res = db.execute_query("SELECT manager_key FROM DIM_BUSINESS_MANAGER WHERE manager_id = ? AND is_current = true", (asgn["manager_id"],))
        loc_res = db.execute_query("SELECT location_key FROM DIM_LOCATION WHERE location_id = ? AND is_current = true", (asgn["location_id"],))
        
        if cust_res and mgr_res and loc_res:
            cust_key = cust_res[0][0]
            mgr_key = mgr_res[0][0]
            loc_key = loc_res[0][0]

            check_q = "SELECT assignment_key FROM BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT WHERE assignment_key = ?"
            if not db.execute_query(check_q, (idx,)):
                insert_q = """
                INSERT INTO BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT (assignment_key, customer_key, manager_key, division, location_key, effective_start_date, effective_end_date, is_current)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                db.execute_query(insert_q, (
                    idx, cust_key, mgr_key, asgn["division"], loc_key,
                    asgn["effective_start_date"], asgn["effective_end_date"], asgn["is_current"]
                ))
    db.commit()
    logger.info("BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT loaded.")
