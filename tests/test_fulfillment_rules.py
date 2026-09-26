import unittest
import tempfile
import os
from src.database.connection import DatabaseConnection
from src.database.schema import run_migrations
from src.etl.dimensions_loader import load_all_dimensions
from src.etl.bridge_loader import load_bridge
from src.etl.facts_loader import load_sales_order_lines

class TestFulfillmentRules(unittest.TestCase):
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

    def test_fulfillment_eligibility_enforcement(self):
        invalid_facts = self.db.execute_query("""
            SELECT COUNT(*)
            FROM FACT_SALES_ORDER_LINE f
            JOIN DIM_LOCATION l ON f.fulfillment_location_key = l.location_key
            WHERE l.location_type NOT IN ('Warehouse', 'Manufacturing');
        """)
        self.assertEqual(invalid_facts[0][0], 0)

    def test_reject_log_populated(self):
        rejects = self.db.execute_query("SELECT COUNT(*) FROM ETL_REJECT_LOG WHERE source_entity = 'FACT_SALES_ORDER_LINE';")
        self.assertGreaterEqual(rejects[0][0], 1)

if __name__ == "__main__":
    unittest.main()
