import unittest
import tempfile
import os
from src.database.connection import DatabaseConnection
from src.database.schema import run_migrations
from src.etl.dimensions_loader import load_all_dimensions

class TestDimensionsSCD(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = DatabaseConnection(db_path=self.temp_db.name, use_duckdb=False)
        run_migrations(self.db)
        load_all_dimensions(self.db)

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_dimensions_loaded(self):
        loc_count = self.db.execute_query("SELECT COUNT(*) FROM DIM_LOCATION;")[0][0]
        cust_count = self.db.execute_query("SELECT COUNT(*) FROM DIM_CUSTOMER;")[0][0]
        mgr_count = self.db.execute_query("SELECT COUNT(*) FROM DIM_BUSINESS_MANAGER;")[0][0]
        prod_count = self.db.execute_query("SELECT COUNT(*) FROM DIM_PRODUCT;")[0][0]

        self.assertGreaterEqual(loc_count, 6)
        self.assertGreaterEqual(cust_count, 4)
        self.assertGreaterEqual(mgr_count, 3)
        self.assertGreaterEqual(prod_count, 4)

    def test_scd2_date_ranges(self):
        invalid_locs = self.db.execute_query("SELECT COUNT(*) FROM DIM_LOCATION WHERE effective_start_date > effective_end_date;")
        self.assertEqual(invalid_locs[0][0], 0)

if __name__ == "__main__":
    unittest.main()
