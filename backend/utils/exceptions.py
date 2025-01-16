# utils/exceptions.py

class StockError(Exception):
    """Custom exception for stock-related errors."""
    pass

class FileOperationError(Exception):
    """Custom exception for file operation errors."""
    pass

class ValidationError(Exception):
    """Custom exception for data validation errors."""
    pass

class DatabaseError(Exception):
    """Custom exception for database operation errors."""
    pass

class ConfigurationError(Exception):
    """Custom exception for configuration-related errors."""
    pass
