import logging
import sys
from typing import Any

# Create a logger instance
logger = logging.getLogger("api")
logger.setLevel(logging.INFO)

# Create console handler with a higher log level
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create formatter and add it to the handler
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

def log_info(message: Any) -> None:
    """Log info level messages."""
    logger.info(message)

def log_error(message: Any) -> None:
    """Log error level messages."""
    logger.error(message)

def log_warning(message: Any) -> None:
    """Log warning level messages."""
    logger.warning(message)