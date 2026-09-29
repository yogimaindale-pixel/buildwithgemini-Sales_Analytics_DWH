# Module docstring explaining Slowly Changing Dimension (SCD Type 2) test suite
"""Unit test suite verifying dimension table row population and SCD Type 2 date validity."""

# Import standard unittest framework
import unittest
# Import tempfile module for creating temporary test databases
import tempfile
# Import os module for clean temporary file deletion
import os

# Import DatabaseConnection wrapper class
from src.database.connection import DatabaseConnection
# Import schema migrations runner
from src.database.schema import run_migrations
# Import dimensions loader module under test
from src.etl.dimensions_loader import load_all_dimensions

# Test class testing dimension table population and SCD Type 2 integrity
class TestDimensionsSCD(unittest.TestCase):
    """Test suite verifying dimension record counts and SCD Type 2 start/end date ranges."""

    # Set up temporary database before each test execution
    def setUp(self):
        """Initialize temporary database, execute schema migrations, and load all dimensions."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = DatabaseConnection(db_path=self.temp_db.name, use_duckdb=False)
        run_migrations(self.db)
        load_all_dimensions(self.db)

    # Clean up database connection and delete temporary file after test execution
    def tearDown(self):
        """Close connection and clean up temporary database file."""
        self.db.close()
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    # Test verifying dimension tables contain expected minimum entity record counts
    def test_dimensions_loaded(self):
        """Verify DIM_LOCATION, DIM_CUSTOMER, DIM_BUSINESS_MANAGER, and DIM_PRODUCT records exist."""
        loc_count = self.db.execute_query("SELECT COUNT(*) FROM DIM_LOCATION;")[0][0]
        cust_count = self.db.execute_query("SELECT COUNT(*) FROM DIM_CUSTOMER;")[0][0]
        mgr_count = self.db.execute_query("SELECT COUNT(*) FROM DIM_BUSINESS_MANAGER;")[0][0]
        prod_count = self.db.execute_query("SELECT COUNT(*) FROM DIM_PRODUCT;")[0][0]

        # Assert minimum expected record counts across all 4 dimension tables
        self.assertGreaterEqual(loc_count, 6)
        self.assertGreaterEqual(cust_count, 4)
        self.assertGreaterEqual(mgr_count, 3)
        self.assertGreaterEqual(prod_count, 4)

    # Test verifying effective_start_date is less than or equal to effective_end_date across all SCD2 records
    def test_scd2_date_ranges(self):
        """Verify zero records exist with invalid effective start date > effective end date."""
        invalid_locs = self.db.execute_query("SELECT COUNT(*) FROM DIM_LOCATION WHERE effective_start_date > effective_end_date;")
        # Assert invalid date range count is strictly 0
        self.assertEqual(invalid_locs[0][0], 0)

# Run unittest main runner if script is executed directly
if __name__ == "__main__":
    unittest.main()

