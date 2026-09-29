# Module docstring explaining business rule verification test suite for order fulfillment locations
"""Unit test suite verifying fulfillment location eligibility rules and ETL reject log population."""

# Import standard unittest framework
import unittest
# Import tempfile module for creating temporary test database files
import tempfile
# Import os module for clean temporary file deletion
import os

# Import DatabaseConnection wrapper class
from src.database.connection import DatabaseConnection
# Import schema migrations runner
from src.database.schema import run_migrations
# Import dimensions loader
from src.etl.dimensions_loader import load_all_dimensions
# Import bridge loader
from src.etl.bridge_loader import load_bridge
# Import sales order line fact loader module under test
from src.etl.facts_loader import load_sales_order_lines

# Test class testing fulfillment location eligibility rules and quarantine log population
class TestFulfillmentRules(unittest.TestCase):
    """Test suite verifying orders are fulfilled exclusively from Warehouse or Manufacturing facilities."""

    # Set up temporary database before each test execution
    def setUp(self):
        """Initialize temporary database and run complete ETL sequence up to fact loading."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = DatabaseConnection(db_path=self.temp_db.name, use_duckdb=False)
        run_migrations(self.db)
        load_all_dimensions(self.db)
        load_bridge(self.db)
        load_sales_order_lines(self.db)

    # Clean up database connection and delete temporary file after test execution
    def tearDown(self):
        """Close database connection and remove temporary database file."""
        self.db.close()
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    # Test verifying zero order lines exist in FACT_SALES_ORDER_LINE with ineligible fulfillment types
    def test_fulfillment_eligibility_enforcement(self):
        """Verify zero order lines fulfilled from Sales Offices exist in target fact table."""
        invalid_facts = self.db.execute_query("""
            SELECT COUNT(*)
            FROM FACT_SALES_ORDER_LINE f
            JOIN DIM_LOCATION l ON f.fulfillment_location_key = l.location_key
            WHERE l.location_type NOT IN ('Warehouse', 'Manufacturing');
        """)
        # Assert invalid fact count is strictly 0
        self.assertEqual(invalid_facts[0][0], 0)

    # Test verifying rejected order lines (such as ORD-2024-005) were logged into ETL_REJECT_LOG
    def test_reject_log_populated(self):
        """Verify ineligible fulfillment order lines are written to ETL_REJECT_LOG quarantine table."""
        rejects = self.db.execute_query("SELECT COUNT(*) FROM ETL_REJECT_LOG WHERE source_entity = 'FACT_SALES_ORDER_LINE';")
        # Assert reject count is at least 1
        self.assertGreaterEqual(rejects[0][0], 1)

# Run unittest main runner if script is executed directly
if __name__ == "__main__":
    unittest.main()

