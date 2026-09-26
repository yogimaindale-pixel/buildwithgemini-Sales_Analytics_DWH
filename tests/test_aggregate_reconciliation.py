import unittest
import tempfile
import os
from src.database.connection import DatabaseConnection
from src.database.schema import run_migrations
from src.etl.dimensions_loader import load_all_dimensions
from src.etl.bridge_loader import load_bridge
from src.etl.facts_loader import load_sales_order_lines
from src.etl.aggregate_loader import refresh_monthly_aggregates
from src.analytics.reports import reconcile_atomic_and_aggregate

class TestAggregateReconciliation(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = DatabaseConnection(db_path=self.temp_db.name, use_duckdb=False)
        run_migrations(self.db)
        load_all_dimensions(self.db)
        load_bridge(self.db)
        load_sales_order_lines(self.db)
        refresh_monthly_aggregates(self.db)

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_aggregate_reconciliation(self):
        recon = reconcile_atomic_and_aggregate(self.db)
        self.assertTrue(recon["reconciled"])
        self.assertEqual(recon["atomic_totals"]["total_quantity"], recon["aggregate_totals"]["total_quantity"])
        self.assertAlmostEqual(recon["atomic_totals"]["total_net_revenue"], recon["aggregate_totals"]["total_net_revenue"], places=2)

if __name__ == "__main__":
    unittest.main()
