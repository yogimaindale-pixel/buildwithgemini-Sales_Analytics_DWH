import unittest
import tempfile
import os
from src.database.connection import DatabaseConnection
from src.database.schema import run_migrations
from src.etl.dimensions_loader import load_all_dimensions
from src.etl.bridge_loader import load_bridge
from src.etl.facts_loader import load_sales_order_lines

class TestFactSalesOrderLine(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = DatabaseConnection(db_path=self.temp_db.name, use_duckdb=False)
        run_migrations(self.db)
        load_all_dimensions(self.db)
        load_bridge(self.db)
        load_sales_order_lines(self.db)

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_fact_revenue_calculations(self):
        lines = self.db.execute_query("SELECT quantity, unit_price, discount_amount, gross_revenue, net_revenue FROM FACT_SALES_ORDER_LINE;")
        self.assertGreater(len(lines), 0)

        for qty, price, disc, gross, net in lines:
            self.assertEqual(float(gross), float(qty) * float(price))
            self.assertEqual(float(net), float(gross) - float(disc))

if __name__ == "__main__":
    unittest.main()
