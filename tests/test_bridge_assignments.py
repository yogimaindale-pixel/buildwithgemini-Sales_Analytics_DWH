# Module docstring explaining customer-manager bridge assignment test suite
"""Unit test suite verifying BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT loading and referential integrity."""

# Import standard unittest framework
import unittest
# Import tempfile module to create isolated temporary database instances for tests
import tempfile
# Import os module for clean temporary file deletion
import os

# Import DatabaseConnection wrapper class
from src.database.connection import DatabaseConnection
# Import schema migrations runner
from src.database.schema import run_migrations
# Import dimensions loader
from src.etl.dimensions_loader import load_all_dimensions
# Import bridge loader module under test
from src.etl.bridge_loader import load_bridge

# Test class testing bridge assignment table populating and integrity constraints
class TestBridgeAssignments(unittest.TestCase):
    """Test suite for customer-manager bridge table loading and referential integrity."""

    # Set up isolated temporary SQLite database before each test execution
    def setUp(self):
        """Initialize temporary database, execute migrations, and load dimensions and bridge tables."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = DatabaseConnection(db_path=self.temp_db.name, use_duckdb=False)
        run_migrations(self.db)
        load_all_dimensions(self.db)
        load_bridge(self.db)

    # Clean up database connection and delete temporary file after each test execution
    def tearDown(self):
        """Close database connection and remove temporary test database file."""
        self.db.close()
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    # Test verifying bridge table contains expected minimum assignment record count
    def test_bridge_loaded(self):
        """Verify bridge table contains expected number of assignment records."""
        count = self.db.execute_query("SELECT COUNT(*) FROM BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT;")[0][0]
        self.assertGreaterEqual(count, 4)

    # Test verifying referential integrity: zero orphaned records exist in bridge table
    def test_bridge_referential_integrity(self):
        """Verify zero orphan records exist linking invalid customer or manager surrogate keys."""
        orphans = self.db.execute_query("""
            SELECT COUNT(*) 
            FROM BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT b
            LEFT JOIN DIM_CUSTOMER c ON b.customer_key = c.customer_key
            LEFT JOIN DIM_BUSINESS_MANAGER m ON b.manager_key = m.manager_key
            WHERE c.customer_key IS NULL OR m.manager_key IS NULL;
        """)
        # Assert orphan record count is strictly 0
        self.assertEqual(orphans[0][0], 0)

# Run unittest main runner if script is executed directly
if __name__ == "__main__":
    unittest.main()

