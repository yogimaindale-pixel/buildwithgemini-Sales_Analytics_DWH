# Module docstring explaining atomic vs aggregate data reconciliation test suite
"""Unit test suite verifying reconciliation between atomic order line facts and monthly aggregate marts."""

# Import standard unittest framework
import unittest
# Import tempfile module for creating isolated temporary test databases
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
# Import sales order line fact loader
from src.etl.facts_loader import load_sales_order_lines
# Import aggregate loader
from src.etl.aggregate_loader import refresh_monthly_aggregates
# Import reconciliation analytics function under test
from src.analytics.reports import reconcile_atomic_and_aggregate

# Test class testing atomic vs aggregate total metric alignment
class TestAggregateReconciliation(unittest.TestCase):
    """Test suite verifying metric totals match exactly between atomic and aggregate summary tables."""

    # Set up temporary database before each test execution
    def setUp(self):
        """Initialize temporary database and run complete end-to-end pipeline up to aggregate refresh."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = DatabaseConnection(db_path=self.temp_db.name, use_duckdb=False)
        run_migrations(self.db)
        load_all_dimensions(self.db)
        load_bridge(self.db)
        load_sales_order_lines(self.db)
        refresh_monthly_aggregates(self.db)

    # Clean up database connection and delete temporary file after test execution
    def tearDown(self):
        """Close connection and clean up temporary database file."""
        self.db.close()
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    # Test verifying reconciliation check passes with matching totals
    def test_aggregate_reconciliation(self):
        """Verify atomic and aggregate totals match for quantity, net revenue, and line item counts."""
        recon = reconcile_atomic_and_aggregate(self.db)
        # Assert reconciliation flag is True
        self.assertTrue(recon["reconciled"])
        # Assert atomic total quantity equals aggregate total quantity
        self.assertEqual(recon["atomic_totals"]["total_quantity"], recon["aggregate_totals"]["total_quantity"])
        # Assert atomic net revenue matches aggregate net revenue to 2 decimal places
        self.assertAlmostEqual(recon["atomic_totals"]["total_net_revenue"], recon["aggregate_totals"]["total_net_revenue"], places=2)

# Run unittest main runner if script is executed directly
if __name__ == "__main__":
    unittest.main()

