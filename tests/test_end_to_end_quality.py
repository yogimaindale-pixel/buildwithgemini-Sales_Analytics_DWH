# Module docstring explaining end-to-end integration test suite
"""Unit test suite verifying complete end-to-end ETL execution and report generation."""

# Import standard unittest framework
import unittest
# Import tempfile module for creating temporary test database files
import tempfile
# Import os module for clean temporary file deletion
import os

# Import DatabaseConnection wrapper class
from src.database.connection import DatabaseConnection
# Import run_pipeline master orchestration function
from main import run_pipeline
# Import detailed sales report generator function
from src.analytics.reports import get_detailed_monthly_sales_report

# Test class testing complete end-to-end data pipeline quality and integrity
class TestEndToEndQuality(unittest.TestCase):
    """Test suite verifying end-to-end pipeline execution from migration to report generation."""

    # Set up temporary database file before each test execution
    def setUp(self):
        """Initialize temporary database file path."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()

    # Clean up temporary database file after test execution
    def tearDown(self):
        """Remove temporary test database file from disk."""
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    # Test executing full pipeline and verifying report generation
    def test_full_pipeline_execution(self):
        """Verify full pipeline run populates tables, passes reconciliation, and renders report rows."""
        # Execute master ETL pipeline on temporary database
        recon = run_pipeline(db_path=self.temp_db.name, use_duckdb=False)
        # Assert reconciliation status flag is True
        self.assertTrue(recon["reconciled"])

        # Open database connection and generate detailed monthly sales report
        db = DatabaseConnection(db_path=self.temp_db.name, use_duckdb=False)
        report = get_detailed_monthly_sales_report(db)
        # Assert sales report contains at least 1 valid detailed row
        self.assertGreater(len(report), 0)
        # Close database connection
        db.close()

# Run unittest main runner if script is executed directly
if __name__ == "__main__":
    unittest.main()

