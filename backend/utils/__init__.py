# utils/__init__.py

from .logger import setup_logger
from .exceptions import StockError
from .file_handler import StockFileHandler

__all__ = [
    'setup_logger',
    'StockError',
    'StockFileHandler'
]

# Initialize logger for the utils package
logger = setup_logger(__name__)

# Log utils package initialization
logger.info("Utils package initialized")
