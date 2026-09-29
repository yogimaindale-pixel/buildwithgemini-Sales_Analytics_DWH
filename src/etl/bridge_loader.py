# Module docstring explaining customer-manager-location bridge table ETL logic
"""Bridge Loader Module handling many-to-many customer, manager, and location assignments."""

# Import DatabaseConnection wrapper class
from src.database.connection import DatabaseConnection
# Import raw mock seed data assignments retrieval helper
from src.etl.seed_data import get_raw_assignments
# Import logger setup helper to log bridge table loading progress
from src.utils.logger import setup_logger

# Initialize logger instance for bridge table loader
logger = setup_logger("BridgeLoader")

# Function populating BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT table by resolving active surrogate keys
def load_bridge(db: DatabaseConnection):
    """Load customer-to-manager and location relationship bridge table with surrogate keys.

    Args:
        db (DatabaseConnection): Active database connection instance.
    """
    logger.info("Loading BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT...")
    assignments = get_raw_assignments()
    
    # Iterate through assignment records with index-based surrogate assignment_key
    for idx, asgn in enumerate(assignments, start=1):
        # Resolve active customer surrogate key (customer_key) from natural customer_id
        cust_res = db.execute_query("SELECT customer_key FROM DIM_CUSTOMER WHERE customer_id = ? AND is_current = true", (asgn["customer_id"],))
        # Resolve active manager surrogate key (manager_key) from natural manager_id
        mgr_res = db.execute_query("SELECT manager_key FROM DIM_BUSINESS_MANAGER WHERE manager_id = ? AND is_current = true", (asgn["manager_id"],))
        # Resolve active location surrogate key (location_key) from natural location_id
        loc_res = db.execute_query("SELECT location_key FROM DIM_LOCATION WHERE location_id = ? AND is_current = true", (asgn["location_id"],))
        
        # Verify referential integrity: ensure target keys were resolved successfully in dimensions
        if cust_res and mgr_res and loc_res:
            cust_key = cust_res[0][0]
            mgr_key = mgr_res[0][0]
            loc_key = loc_res[0][0]

            # Check if assignment_key already exists to prevent duplicate inserts
            check_q = "SELECT assignment_key FROM BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT WHERE assignment_key = ?"
            if not db.execute_query(check_q, (idx,)):
                # Insert resolved bridge mapping record
                insert_q = """
                INSERT INTO BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT (assignment_key, customer_key, manager_key, division, location_key, effective_start_date, effective_end_date, is_current)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                db.execute_query(insert_q, (
                    idx, cust_key, mgr_key, asgn["division"], loc_key,
                    asgn["effective_start_date"], asgn["effective_end_date"], asgn["is_current"]
                ))
                
    # Commit pending write transactions to database
    db.commit()
    logger.info("BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT loaded.")

