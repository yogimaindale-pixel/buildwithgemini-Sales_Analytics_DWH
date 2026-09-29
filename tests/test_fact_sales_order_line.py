# Module docstring explaining sales order line transactional fact calculation test suite
"""Unit test suite verifying FACT_SALES_ORDER_LINE calculation accuracy (Gross & Net Revenue)."""

# Import standard unittest framework
import unittest
# Import tempfile module for creating temporary database instances
import tempfile
# Import os module for file deletion cleanup
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

# Test class testing sales order line revenue calculation accuracy
class TestFactSalesOrderLine(unittest.TestCase):
    """Test suite verifying transactional order line revenue metrics."""

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

    # Clean up temporary database file after each test execution
    def tearDown(self):
        """Close connection and clean up temporary database file."""
        self.db.close()
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    # Test verifying mathematical accuracy of gross_revenue and net_revenue metrics across all order line facts
    def test_fact_revenue_calculations(self):
        """Verify gross revenue (qty * price) and net revenue (gross - discount) calculations."""
        lines = self.db.execute_query("SELECT quantity, unit_price, discount_amount, gross_revenue, net_revenue FROM FACT_SALES_ORDER_LINE;")
        # Assert at least 1 valid order line fact record was loaded
        self.assertGreater(len(lines), 0)

        # Iterate through loaded order line facts and verify revenue equations
        for qty, price, disc, gross, net in lines:
            # Assert Gross Revenue = Quantity * Unit Price
            self.assertEqual(float(gross), float(qty) * float(price))
            # Assert Net Revenue = Gross Revenue - Discount Amount
            self.assertEqual(float(net), float(gross) - float(disc))

# Run unittest main runner if script is executed directly
if __name__ == "__main__":
    unittest.main()

