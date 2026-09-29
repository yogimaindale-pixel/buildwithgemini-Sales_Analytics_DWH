# Module docstring explaining command-line interface test suite
"""Unit test suite verifying main.py CLI subcommands and full pipeline orchestration."""

# Import standard unittest framework
import unittest
# Import tempfile module for managing temporary test working directories
import tempfile
# Import shutil module for directory cleanup
import shutil
# Import sys module for patching command line sys.argv arguments
import sys
# Import Path class for object-oriented filesystem path operations
from pathlib import Path
# Import patch helper for mocking sys.argv during CLI subcommand execution
from unittest.mock import patch

# Import run_pipeline master function and main CLI entrypoint from main.py
from main import run_pipeline, main as main_cli

# Test class testing CLI subcommands and full pipeline invocation
class TestCLI(unittest.TestCase):
    """Test suite verifying CLI subcommands: full-run, migrate, reconcile, report."""

    # Set up temporary working directory and database path before each test execution
    def setUp(self):
        """Create temporary directory and construct test database file path."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = str(Path(self.temp_dir) / "test_sales_warehouse.db")

    # Clean up temporary directory after each test execution
    def tearDown(self):
        """Remove temporary test directory tree."""
        shutil.rmtree(self.temp_dir)

    # Test verifying full pipeline execution returns successful reconciliation state
    def test_run_pipeline_full_run(self):
        """Verify run_pipeline executes all steps and returns successful reconciliation."""
        recon = run_pipeline(db_path=self.db_path, use_duckdb=False)
        # Assert reconciliation flag is True
        self.assertTrue(recon["reconciled"])
        # Assert total quantity metric is positive
        self.assertGreater(recon["atomic_totals"]["total_quantity"], 0)

    # Test verifying CLI --action migrate subcommand creates target database file
    def test_cli_migrate_action(self):
        """Verify CLI migrate subcommand creates schema tables."""
        test_args = ["main.py", "--action", "migrate", "--db", self.db_path]
        with patch.object(sys, "argv", test_args):
            main_cli()
        # Assert target database file was created on disk
        self.assertTrue(Path(self.db_path).exists())

    # Test verifying CLI --action reconcile subcommand executes cleanly
    def test_cli_reconcile_action(self):
        """Verify CLI reconcile subcommand outputs reconciliation status JSON."""
        # Populate database first via full pipeline run
        run_pipeline(db_path=self.db_path)
        test_args = ["main.py", "--action", "reconcile", "--db", self.db_path]
        with patch.object(sys, "argv", test_args):
            main_cli()

    # Test verifying CLI --action report subcommand prints sales report stdout output
    def test_cli_report_action(self):
        """Verify CLI report subcommand prints formatted detailed sales report."""
        run_pipeline(db_path=self.db_path)
        test_args = ["main.py", "--action", "report", "--db", self.db_path]
        with patch.object(sys, "argv", test_args):
            main_cli()

# Run unittest main runner if script is executed directly
if __name__ == "__main__":
    unittest.main()

