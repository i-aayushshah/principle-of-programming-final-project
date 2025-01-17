# backend/tests/test_operations.py

import sys
import os
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from utils import setup_logger, StockFileHandler, StockError
from models.nav_sys import NavSys
from models.stock_item import StockItem

logger = setup_logger(__name__)

def test_stock_item_operations():
    """Test StockItem class operations"""
    try:
        # Test initialization
        item = StockItem("W101", 10, 99.99)
        assert item.stock_code == "W101", "Stock code initialization failed"
        assert item.quantity == 10, "Quantity initialization failed"
        assert item.price == 99.99, "Price initialization failed"

        # Test stock operations
        item.increase_stock(5)
        assert item.quantity == 15, "Stock increase failed"

        success = item.sell_stock(3)
        assert success and item.quantity == 12, "Stock sale failed"

        # Test VAT calculations
        assert item.get_VAT() == 17.5, "VAT rate incorrect"
        expected_vat_price = 99.99 * (1 + 17.5/100)
        assert item.get_price_with_VAT() == expected_vat_price, "VAT calculation failed"

        logger.info("StockItem operations test completed successfully")

    except Exception as e:
        logger.error(f"StockItem test failed: {str(e)}")
        raise

def test_nav_sys_operations():
    """Test NavSys class operations"""
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

        # Test brand operations
        assert nav1.brand == "TomTom", "Brand getter failed"
        nav1.brand = "Garmin"
        assert nav1.brand == "Garmin", "Brand setter failed"

        # Save updated items
        file_handler.save_item(nav1)

        logger.info("NavSys operations test completed successfully")

    except Exception as e:
        logger.error(f"NavSys test failed: {str(e)}")
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

        # Test invalid brand
        try:
            nav.brand = ""  # Should raise error
        except StockError as e:
            logger.info(f"Successfully caught invalid brand: {str(e)}")

        logger.info("Error scenarios test completed successfully")

    except Exception as e:
        logger.error(f"Error scenarios test failed: {str(e)}")
        raise

def test_file_operations():
    """Test file handling operations"""
    try:
        file_handler = StockFileHandler()

        # Test file creation
        assert os.path.exists(file_handler.file_path), "CSV file not created"

        # Test saving and loading
        nav = NavSys("NS104", 10, 299.99, "GeoVision")
        file_handler.save_item(nav)

        items = file_handler.load_items()
        assert len(items) > 0, "Failed to load items"

        # Test item deletion
        result = file_handler.delete_item("NS104")
        assert result, "Failed to delete item"

        logger.info("File operations test completed successfully")

    except Exception as e:
        logger.error(f"File operations test failed: {str(e)}")
        raise

def run_all_tests():
    """Run all test cases"""
    try:
        print("\n=== Running StockItem Tests ===")
        test_stock_item_operations()

        print("\n=== Running NavSys Tests ===")
        test_nav_sys_operations()

        print("\n=== Running Error Scenario Tests ===")
        test_error_scenarios()

        print("\n=== Running File Operation Tests ===")
        test_file_operations()

        print("\n✅ All tests completed successfully!")

    except Exception as e:
        print(f"\n❌ Tests failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_all_tests()
