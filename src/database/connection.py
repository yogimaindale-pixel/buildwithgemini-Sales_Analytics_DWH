# Module docstring explaining database connection management and abstraction layer
"""Database Connection Abstraction supporting SQLite and DuckDB engines."""

# Import built-in sqlite3 database module for standard lightweight SQL storage
import sqlite3
# Import os module for file path operations
import os

# Safely import duckdb module if available in environment; flag HAS_DUCKDB = False if missing
try:
    import duckdb
    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False

# Import logger setup helper to output database connection logs
from src.utils.logger import setup_logger

# Initialize logger instance for connection operations
logger = setup_logger("DatabaseConnection")

# Class encapsulating database connection lifecycle, script execution, and query execution
class DatabaseConnection:
    """Database Connection Manager providing unified interface for SQLite and DuckDB engines."""
    
    # Constructor initializing target database file path and engine preference
    def __init__(self, db_path: str = "sales_warehouse.db", use_duckdb: bool = True):
        self.db_path = db_path
        # Enable DuckDB only if requested AND duckdb library is installed in environment
        self.use_duckdb = use_duckdb and HAS_DUCKDB
        self.conn = None

    # Connect method establishing database connection based on active engine selection
    def connect(self):
        """Open database connection to target database file."""
        if self.use_duckdb:
            logger.info(f"Connecting to DuckDB at {self.db_path}")
            self.conn = duckdb.connect(self.db_path)
        else:
            logger.info(f"Connecting to SQLite database at {self.db_path}")
            self.conn = sqlite3.connect(self.db_path)
            # Enable SQLite foreign key constraint enforcement explicitly
            self.conn.execute("PRAGMA foreign_keys = ON;")
        return self.conn

    # Execute SQL script string containing multiple DDL/DML statements separated by semicolons
    def execute_script(self, script_content: str):
        """Execute multi-statement SQL migration script."""
        if not self.conn:
            self.connect()
        if self.use_duckdb:
            # DuckDB requires splitting multi-statement scripts into individual statements
            statements = [stmt.strip() for stmt in script_content.split(";") if stmt.strip()]
            for stmt in statements:
                self.conn.execute(stmt)
        else:
            # SQLite supports executing multi-statement scripts natively via executescript()
            self.conn.executescript(script_content)

    # Execute parameterized SQL query string and return all fetched result rows
    def execute_query(self, query: str, params=None):
        """Execute SQL query with parameters and return list of result tuples."""
        if not self.conn:
            self.connect()
        params = params or ()
        if self.use_duckdb:
            # Execute and fetch all matching rows using DuckDB cursor interface
            return self.conn.execute(query, params).fetchall()
        else:
            # Execute and fetch all matching rows using SQLite cursor interface
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    # Commit pending database transactions for engines requiring manual commit (SQLite)
    def commit(self):
        """Commit pending write transactions."""
        if self.conn and not self.use_duckdb:
            self.conn.commit()

    # Close active database connection cleanly and reset connection state
    def close(self):
        """Close active database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

