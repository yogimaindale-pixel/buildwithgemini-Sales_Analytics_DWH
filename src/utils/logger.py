# Module docstring explaining standard application logging configuration
"""Standard logging setup utility for Enterprise Sales Analytics Data Warehouse."""

# Import standard library logging module for structuring operational logs
import logging
# Import sys module for directing logs to standard stdout stream
import sys

# Function setting up named logger with configurable log level and formatting
def setup_logger(name: str = "SalesWarehouse", level: str = "INFO") -> logging.Logger:
    """Instantiate and configure a standard logger stream handler.
    
    Args:
        name (str): Component logger identifier (e.g. 'MainRunner', 'ETL').
        level (str): Logging threshold level ('DEBUG', 'INFO', 'WARNING', 'ERROR').
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    
    # Check if handlers are already attached to prevent duplicate log lines
    if not logger.handlers:
        # Set numeric log level from string attribute name (defaults to INFO if invalid)
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        
        # Create stdout stream handler to emit log output to console terminal
        handler = logging.StreamHandler(sys.stdout)
        
        # Define timestamped log format string: [YYYY-MM-DD HH:MM:SS] [LEVEL] [LOGGER_NAME]: MESSAGE
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        # Attach formatter to stdout handler
        handler.setFormatter(formatter)
        
        # Attach handler to logger instance
        logger.addHandler(handler)
        
    return logger

