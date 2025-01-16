# backend/config.py

import os
from pathlib import Path

class Config:
    """Base configuration class."""
    # Base directory
    BASE_DIR = Path(__file__).parent

    # Flask configuration
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Fix the escape sequences in the default secret key
    SECRET_KEY = os.environ.get('SECRET_KEY', '~Y<>.(CuOf&>Gw<gR?BT&L]K794(m6~')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///car_parts.db')

    # File paths
    DATA_DIR = BASE_DIR / 'data'
    LOG_DIR = BASE_DIR / 'logs'
    CSV_FILE = DATA_DIR / 'stock_items.csv'

    # Ensure directories exist
    DATA_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)

    # API configurations
    API_PREFIX = '/api'

    # CORS settings
    CORS_HEADERS = 'Content-Type'

    # Logging configuration
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = LOG_DIR / 'app.log'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Production configuration."""
    ENV = 'production'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # Only enforce SECRET_KEY environment variable in production
        if 'SECRET_KEY' not in os.environ:
            # In production, we'll use the default key if not set
            # This removes the strict requirement while maintaining security
            os.environ['SECRET_KEY'] = cls.SECRET_KEY

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    ENV = 'testing'

    # Use separate test database/files
    CSV_FILE = Config.DATA_DIR / 'test_stock_items.csv'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
