import os
from glob import glob
from src.database.connection import DatabaseConnection
from src.utils.logger import setup_logger

logger = setup_logger("SchemaRunner")

def run_migrations(db_conn: DatabaseConnection, migrations_dir: str = "sql/migrations"):
    if not os.path.exists(migrations_dir):
        # Fall back to repo root relative to this file
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        alt_dir = os.path.join(base_dir, migrations_dir)
        if os.path.exists(alt_dir):
            migrations_dir = alt_dir

    logger.info(f"Running schema migrations from {migrations_dir}...")
    migration_files = sorted(glob(os.path.join(migrations_dir, "*.sql")))
    for file_path in migration_files:
        logger.info(f"Applying migration: {os.path.basename(file_path)}")
        with open(file_path, "r", encoding="utf-8") as f:
            script = f.read()
            db_conn.execute_script(script)
    db_conn.commit()
    logger.info("All schema migrations applied successfully.")
