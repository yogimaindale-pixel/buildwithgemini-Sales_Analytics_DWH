import unittest
import tempfile
import os
from src.database.connection import DatabaseConnection
from src.database.schema import run_migrations
from src.etl.dimensions_loader import load_all_dimensions
from src.etl.bridge_loader import load_bridge

class TestBridgeAssignments(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = DatabaseConnection(db_path=self.temp_db.name, use_duckdb=False)
        run_migrations(self.db)
        load_all_dimensions(self.db)
        load_bridge(self.db)

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_bridge_loaded(self):
        count = self.db.execute_query("SELECT COUNT(*) FROM BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT;")[0][0]
        self.assertGreaterEqual(count, 4)

    def test_bridge_referential_integrity(self):
        orphans = self.db.execute_query("""
            SELECT COUNT(*) 
            FROM BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT b
            LEFT JOIN DIM_CUSTOMER c ON b.customer_key = c.customer_key
            LEFT JOIN DIM_BUSINESS_MANAGER m ON b.manager_key = m.manager_key
            WHERE c.customer_key IS NULL OR m.manager_key IS NULL;
        """)
        self.assertEqual(orphans[0][0], 0)

if __name__ == "__main__":
    unittest.main()
