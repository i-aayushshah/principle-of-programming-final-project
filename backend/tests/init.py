# tests/test_operations.py

from utils import setup_logger, StockFileHandler, StockError
from models.nav_sys import NavSys

# Set up logger
logger = setup_logger(__name__)

def test_basic_operations():
    try:
        # Initialize file handler
        logger.info("Initializing file handler...")
        file_handler = StockFileHandler()

        # Create a new navigation system
        nav_sys = NavSys("NS105", 10, 299.99, "Garmin")
        logger.info(f"Created new NavSys: {nav_sys.stock_code}")

        # Save to CSV
        file_handler.save_item(nav_sys)
        logger.info("Saved NavSys to CSV")

        # Load all items
        items = file_handler.load_items()
        logger.info(f"Loaded {len(items)} items from CSV")

        # Try some operations
        nav_sys.increase_stock(5)
        logger.info(f"Increased stock. New quantity: {nav_sys.quantity}")

        # Try an invalid operation to test error handling
        try:
            nav_sys.increase_stock(-1)
        except StockError as e:
            logger.error(f"Stock error occurred: {str(e)}")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    test_basic_operations()
