# backend/tests/test_operations.py

import pytest
from pathlib import Path
from utils.logger import setup_logger
from utils.file_handler import StockFileHandler
from utils.exceptions import StockError
from models.nav_sys import NavSys

logger = setup_logger(__name__)

def test_stock_item_operations():
    """Test StockItem class operations"""
    try:
        # Test initialization
        nav = NavSys("NS101", 10, 199.99, "TomTom")
        assert nav.stock_code == "NS101", "Stock code initialization failed"
        assert nav.quantity == 10, "Quantity initialization failed"
        assert nav.price == 199.99, "Price initialization failed"

        # Test stock operations
        nav.increase_stock(5)
        assert nav.quantity == 15, "Stock increase failed"

        success = nav.sell_stock(3)
        assert success and nav.quantity == 12, "Stock sale failed"

        # Test VAT calculations
        assert nav.get_VAT() == 17.5, "VAT rate incorrect"
        expected_vat_price = 199.99 * (1 + 17.5/100)
        assert nav.get_price_with_VAT() == expected_vat_price, "VAT calculation failed"

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
        with pytest.raises(StockError) as exc_info:
            invalid_nav = NavSys("", -5, -100, "")
        assert "Stock code must be a non-empty string" in str(exc_info.value)
        logger.info(f"Successfully caught invalid creation: {exc_info.value}")

        nav = NavSys("NS103", 10, 199.99, "GeoVision")

        # Test invalid stock increase
        with pytest.raises(StockError) as exc_info:
            nav.increase_stock(-1)
        assert "must be greater than or equal to one" in str(exc_info.value)
        logger.info(f"Successfully caught invalid stock increase: {exc_info.value}")

        # Test stock limit
        with pytest.raises(StockError) as exc_info:
            nav.increase_stock(200)
        assert "Stock cannot exceed 100 items" in str(exc_info.value)
        logger.info(f"Successfully caught stock limit exceed: {exc_info.value}")

        # Test invalid price
        with pytest.raises(ValueError) as exc_info:
            nav.price = -50
        assert "Price must be greater than 0" in str(exc_info.value)
        logger.info(f"Successfully caught invalid price: {exc_info.value}")

        # Test selling more than available
        result = nav.sell_stock(20)
        assert not result, "Overselling should return False"

        # Test invalid brand
        with pytest.raises(StockError) as exc_info:
            nav.brand = ""
        assert "Brand must be a non-empty string" in str(exc_info.value)
        logger.info(f"Successfully caught invalid brand: {exc_info.value}")

        logger.info("Error scenarios test completed successfully")

    except Exception as e:
        logger.error(f"Error scenarios test failed: {str(e)}")
        raise

def test_file_operations():
    """Test file handling operations"""
    try:
        file_handler = StockFileHandler()

        # Test file creation
        assert file_handler.filename.exists(), "CSV file not created"

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

def test_quantity_limits():
    """Test quantity limit validations"""
    try:
        file_handler = StockFileHandler()

        # Test creating new item with quantity > 100
        nav = NavSys("NS105", 50, 299.99, "GeoVision")
        file_handler.save_item(nav)

        # Try to increase quantity beyond limit
        with pytest.raises(StockError) as exc_info:
            nav.increase_stock(60)  # Would make total 110
        assert "Stock cannot exceed 100 items" in str(exc_info.value)
        logger.info("Successfully caught quantity exceed limit")

        # Verify original quantity unchanged
        assert nav.quantity == 50, "Quantity should remain unchanged after failed increase"

        # Test valid quantity increase
        nav.increase_stock(40)  # Total becomes 90
        assert nav.quantity == 90, "Valid quantity increase failed"

        # Test at limit
        nav.increase_stock(10)  # Total becomes 100
        assert nav.quantity == 100, "Increase to limit failed"

        # Test exceeding limit
        with pytest.raises(StockError) as exc_info:
            nav.increase_stock(1)  # Try to exceed 100
        assert "Stock cannot exceed 100 items" in str(exc_info.value)
        logger.info("Successfully caught quantity exceed at limit")

        logger.info("Quantity limits test completed successfully")

    except Exception as e:
        logger.error(f"Quantity limits test failed: {str(e)}")
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

        print("\n=== Running Quantity Limits Tests ===")
        test_quantity_limits()

        print("\n✅ All tests completed successfully!")

    except Exception as e:
        print(f"\n❌ Tests failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_all_tests()
