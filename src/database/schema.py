# Module docstring explaining database DDL schema migration execution logic
"""Schema migration runner executing sequential SQL scripts."""

# Import os module for file path checking and directory resolution
import os
# Import glob function from standard library for wildcard file matching
from glob import glob

# Import DatabaseConnection wrapper class
from src.database.connection import DatabaseConnection
# Import logger setup helper to output migration execution progress
from src.utils.logger import setup_logger

# Initialize logger instance for schema migration runner
logger = setup_logger("SchemaRunner")

# Function executing all sorted SQL migration scripts in specified migrations directory
def run_migrations(db_conn: DatabaseConnection, migrations_dir: str = "sql/migrations"):
    """Discover, load, and execute DDL migration scripts in alphabetical order.
    
    Args:
        db_conn (DatabaseConnection): Open database connection manager.
        migrations_dir (str): Relative or absolute path to migration directory containing .sql files.
    """
    # Check if relative migrations directory exists; resolve fallback relative to repository root if missing
    if not os.path.exists(migrations_dir):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        alt_dir = os.path.join(base_dir, migrations_dir)
        if os.path.exists(alt_dir):
            migrations_dir = alt_dir

    logger.info(f"Running schema migrations from {migrations_dir}...")
    
    # Discover all .sql files in migrations directory and sort them alphabetically (e.g. 001_, 002_, 003_)
    migration_files = sorted(glob(os.path.join(migrations_dir, "*.sql")))
    
    # Iterate through each migration script file sequentially
    for file_path in migration_files:
        logger.info(f"Applying migration: {os.path.basename(file_path)}")
        # Open and read full SQL script contents
        with open(file_path, "r", encoding="utf-8") as f:
            script = f.read()
            # Execute multi-statement SQL migration script via database connection abstraction
            db_conn.execute_script(script)
            
    # Commit pending write transactions cleanly
    db_conn.commit()
    logger.info("All schema migrations applied successfully.")

