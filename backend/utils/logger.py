# utils/logger.py

import logging
import os
from datetime import datetime
from typing import Optional

class LoggerSetup:
    """Configure and manage application logging."""

    _instance: Optional['LoggerSetup'] = None

    def __new__(cls):
        """Implement singleton pattern for logger setup."""
        if cls._instance is None:
            cls._instance = super(LoggerSetup, cls).__new__(cls)
            cls._instance._configure_logger()
        return cls._instance

    def _configure_logger(self):
        """Configure the logger with file and console handlers."""
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Generate log filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(log_dir, f'app_{timestamp}.log')

        # Configure root logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # Clear any existing handlers
        logger.handlers.clear()

        # Create file handler with UTF-8 encoding
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

        # Create console handler with UTF-8 encoding
        import sys
        console_handler = logging.StreamHandler(
            stream=open(os.devnull, 'w') if not sys.stderr.encoding else sys.stderr
        )
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

        # Log initialization
        logger.info(f"Logger initialized. Log file: {log_file}")

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger instance with the specified name.

        Args:
            name (str): Name for the logger, typically __name__ of the module

        Returns:
            logging.Logger: Configured logger instance
        """
        # Ensure logger is configured
        LoggerSetup()
        return logging.getLogger(name)

def setup_logger(name: str) -> logging.Logger:
    """
    Convenience function to get a configured logger.

    Args:
        name (str): Name for the logger

    Returns:
        logging.Logger: Configured logger instance
    """
    return LoggerSetup.get_logger(name)
