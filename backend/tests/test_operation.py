# backend/tests/test_operations.py

import sys
import os
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from utils import setup_logger, StockFileHandler, StockError
from models.nav_sys import NavSys

logger = setup_logger(__name__)

def test_stock_operations():
    """Test basic stock operations"""
    try:
        file_handler = StockFileHandler()

        # Create test items
        nav1 = NavSys("NS101", 10, 199.99, "TomTom")
        nav2 = NavSys("NS102", 15, 299.99, "Garmin")

        # Test saving items
        file_handler.save_item(nav1)
        file_handler.save_item(nav2)

        # Test loading items
        items = file_handler.load_items()
        logger.info(f"Loaded {len(items)} items")

        # Test stock increase
        nav1.increase_stock(5)
        assert nav1.quantity == 15, "Stock increase failed"

        # Test stock sale
        success = nav1.sell_stock(3)
        assert success and nav1.quantity == 12, "Stock sale failed"

        # Test price update
        nav1.price = 249.99
        assert nav1.price == 249.99, "Price update failed"

        # Save updated items
        file_handler.save_item(nav1)

        logger.info("Basic operations test completed successfully")

    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

def test_error_scenarios():
    """Test various error scenarios"""
    try:
        # Test invalid stock creation
        try:
            invalid_nav = NavSys("", -5, -100, "")  # Should raise error
        except StockError as e:
            logger.info(f"Successfully caught invalid creation: {str(e)}")

        nav = NavSys("NS103", 10, 199.99, "GeoVision")

        # Test invalid stock increase
        try:
            nav.increase_stock(-1)  # Should raise error
        except StockError as e:
            logger.info(f"Successfully caught invalid stock increase: {str(e)}")

        # Test stock limit
        try:
            nav.increase_stock(200)  # Should raise error (exceed 100)
        except StockError as e:
            logger.info(f"Successfully caught stock limit exceed: {str(e)}")

        # Test invalid price
        try:
            nav.price = -50  # Should raise error
        except ValueError as e:
            logger.info(f"Successfully caught invalid price: {str(e)}")

        # Test selling more than available
        result = nav.sell_stock(20)  # Should return False
        assert not result, "Overselling should return False"

        logger.info("Error scenarios test completed successfully")

    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_stock_operations()
    test_error_scenarios()
