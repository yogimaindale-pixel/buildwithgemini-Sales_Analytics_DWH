"""Unit tests for main.py CLI pipeline execution."""

import unittest
import tempfile
import shutil
import sys
from pathlib import Path
from unittest.mock import patch
from main import run_pipeline, main as main_cli

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = str(Path(self.temp_dir) / "test_sales_warehouse.db")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_run_pipeline_full_run(self):
        recon = run_pipeline(db_path=self.db_path, use_duckdb=False)
        self.assertTrue(recon["reconciled"])
        self.assertGreater(recon["atomic_totals"]["total_quantity"], 0)

    def test_cli_migrate_action(self):
        test_args = ["main.py", "--action", "migrate", "--db", self.db_path]
        with patch.object(sys, "argv", test_args):
            main_cli()
        self.assertTrue(Path(self.db_path).exists())

    def test_cli_reconcile_action(self):
        # Run pipeline first to populate DB
        run_pipeline(db_path=self.db_path)
        test_args = ["main.py", "--action", "reconcile", "--db", self.db_path]
        with patch.object(sys, "argv", test_args):
            main_cli()

    def test_cli_report_action(self):
        run_pipeline(db_path=self.db_path)
        test_args = ["main.py", "--action", "report", "--db", self.db_path]
        with patch.object(sys, "argv", test_args):
            main_cli()

if __name__ == "__main__":
    unittest.main()
