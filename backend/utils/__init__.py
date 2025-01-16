# utils/__init__.py

from .exceptions import (
    StockError,
    FileOperationError,
    ValidationError,
    DatabaseError,
    ConfigurationError
)
from .logger import setup_logger
from .file_handler import StockFileHandler

# Export commonly used functions and classes
__all__ = [
    'StockError',
    'FileOperationError',
    'ValidationError',
    'DatabaseError',
    'ConfigurationError',
    'setup_logger',
    'StockFileHandler'
]

# Initialize logger for the utils package
logger = setup_logger(__name__)

# Log utils package initialization
logger.info("Utils package initialized")
