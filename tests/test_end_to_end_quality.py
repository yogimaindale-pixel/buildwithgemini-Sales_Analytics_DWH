import unittest
import tempfile
import os
from src.database.connection import DatabaseConnection
from main import run_pipeline
from src.analytics.reports import get_detailed_monthly_sales_report

class TestEndToEndQuality(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_full_pipeline_execution(self):
        recon = run_pipeline(db_path=self.temp_db.name, use_duckdb=False)
        self.assertTrue(recon["reconciled"])

        db = DatabaseConnection(db_path=self.temp_db.name, use_duckdb=False)
        report = get_detailed_monthly_sales_report(db)
        self.assertGreater(len(report), 0)
        db.close()

if __name__ == "__main__":
    unittest.main()
