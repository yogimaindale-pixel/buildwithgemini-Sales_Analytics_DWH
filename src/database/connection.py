import sqlite3
import os
try:
    import duckdb
    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False

from src.utils.logger import setup_logger

logger = setup_logger("DatabaseConnection")

class DatabaseConnection:
    def __init__(self, db_path: str = "sales_warehouse.db", use_duckdb: bool = True):
        self.db_path = db_path
        self.use_duckdb = use_duckdb and HAS_DUCKDB
        self.conn = None

    def connect(self):
        if self.use_duckdb:
            logger.info(f"Connecting to DuckDB at {self.db_path}")
            self.conn = duckdb.connect(self.db_path)
        else:
            logger.info(f"Connecting to SQLite database at {self.db_path}")
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA foreign_keys = ON;")
        return self.conn

    def execute_script(self, script_content: str):
        if not self.conn:
            self.connect()
        if self.use_duckdb:
            statements = [stmt.strip() for stmt in script_content.split(";") if stmt.strip()]
            for stmt in statements:
                self.conn.execute(stmt)
        else:
            self.conn.executescript(script_content)

    def execute_query(self, query: str, params=None):
        if not self.conn:
            self.connect()
        params = params or ()
        if self.use_duckdb:
            return self.conn.execute(query, params).fetchall()
        else:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def commit(self):
        if self.conn and not self.use_duckdb:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
