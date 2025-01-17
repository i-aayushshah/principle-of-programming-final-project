import pytest
from models.nav_sys import NavSys
from utils.file_handler import StockFileHandler
from utils.exceptions import FileOperationError, StockError
from utils.logger import setup_logger

logger = setup_logger(__name__)

class TestOperations:
    """Comprehensive test suite for integrated operations."""

    def test_basic_operations(self):
        """TC-IT-01: Basic integrated operations."""
        try:
            file_handler = StockFileHandler()

            # Create and save item
            nav = NavSys("NS101", 10, 199.99, "TomTom")
            saved, _ = file_handler.save_item(nav)
            assert saved

            # Load and verify
            loaded_nav = file_handler.get_item("NS101")
            assert loaded_nav.stock_code == "NS101"
            assert loaded_nav.quantity == 10
            assert loaded_nav.price == 199.99
            assert loaded_nav.brand == "TomTom"

            logger.info("Basic operations test passed")
        except Exception as e:
            logger.error(f"Basic operations test failed: {str(e)}")
            raise

    def test_complex_operations(self):
        """TC-IT-02: Complex operation sequences."""
        try:
            file_handler = StockFileHandler()

            # Multiple items
            items = [
                NavSys("NS101", 10, 199.99, "TomTom"),
                NavSys("NS102", 15, 299.99, "Garmin"),
                NavSys("NS103", 20, 249.99, "GeoVision")
            ]

            # Save all items
            for item in items:
                file_handler.save_item(item)

            # Modify and update
            for item in items:
                item.increase_stock(5)
                item.price *= 1.1  # 10% price increase
                file_handler.save_item(item)

            # Verify updates
            loaded_items = file_handler.load_items()
            assert len(loaded_items) >= len(items)

            logger.info("Complex operations test passed")
        except Exception as e:
            logger.error(f"Complex operations test failed: {str(e)}")
            raise

    def test_lifecycle_operations(self):
        """TC-IT-03: Complete lifecycle operations."""
        try:
            file_handler = StockFileHandler()

            # Create
            nav = NavSys("NS104", 10, 199.99, "TomTom")
            file_handler.save_item(nav)

            # Update stock
            nav.increase_stock(20)
            file_handler.save_item(nav)

            # Update price
            nav.price = 249.99
            file_handler.save_item(nav)

            # Sell stock
            nav.sell_stock(15)
            file_handler.save_item(nav)

            # Update brand
            nav.brand = "Garmin"
            file_handler.save_item(nav)

            # Delete
            result = file_handler.delete_item("NS104")
            assert result

            logger.info("Lifecycle operations test passed")
        except Exception as e:
            logger.error(f"Lifecycle operations test failed: {str(e)}")
            raise

    def test_error_handling(self):
        """TC-IT-04: Error handling and recovery."""
        try:
            file_handler = StockFileHandler()

            # Invalid save attempts
            with pytest.raises(StockError):
                nav = NavSys("", 10, 199.99, "TomTom")

            with pytest.raises(StockError):
                nav = NavSys("NS105", -5, 199.99, "TomTom")

            # Recovery after errors
            nav = NavSys("NS105", 10, 199.99, "TomTom")
            file_handler.save_item(nav)

            # Test invalid operations
            with pytest.raises(StockError):
                nav.increase_stock(-1)

            with pytest.raises(StockError):
                nav.increase_stock(91)  # Would exceed 100

            # Verify object still valid
            assert nav.quantity == 10

            logger.info("Error handling test passed")
        except Exception as e:
            logger.error(f"Error handling test failed: {str(e)}")
            raise

    def test_bulk_operations(self):
        """TC-IT-05: Bulk operations and performance."""
        try:
            file_handler = StockFileHandler()

            # Create multiple items
            items = []
            for i in range(50):
                nav = NavSys(f"NS{i+200}", 10, 199.99, "TomTom")
                items.append(nav)
                file_handler.save_item(nav)

            # Bulk updates
            for item in items:
                item.increase_stock(5)
                item.price *= 1.1
                file_handler.save_item(item)

            # Bulk loading
            loaded_items = file_handler.load_items()
            assert len(loaded_items) >= len(items)

            # Bulk deletion
            for item in items:
                file_handler.delete_item(item.stock_code)

            logger.info("Bulk operations test passed")
        except Exception as e:
            logger.error(f"Bulk operations test failed: {str(e)}")
            raise

    def test_boundary_operations(self):
        """Additional boundary condition tests."""
        try:
            file_handler = StockFileHandler()

            # Test maximum stock limit
            nav = NavSys("NS301", 90, 199.99, "TomTom")
            file_handler.save_item(nav)

            nav.increase_stock(10)  # Should reach exactly 100
            assert nav.quantity == 100

            with pytest.raises(StockError):
                nav.increase_stock(1)  # Should fail

            # Test minimum price
            nav.price = 0.01
            assert nav.price == 0.01

            # Test maximum price
            nav.price = 999999.99
            assert nav.price == 999999.99

            file_handler.save_item(nav)

            logger.info("Boundary operations test passed")
        except Exception as e:
            logger.error(f"Boundary operations test failed: {str(e)}")
            raise

    def test_data_persistence(self):
        """Test data persistence and file operations."""
        try:
            file_handler = StockFileHandler()

            # Create and save item
            nav = NavSys("NS401", 10, 199.99, "TomTom")
            file_handler.save_item(nav)

            # Modify and save
            nav.increase_stock(5)
            nav.price = 249.99
            nav.brand = "Garmin"
            file_handler.save_item(nav)

            # Load and verify
            loaded_nav = file_handler.get_item("NS401")
            assert loaded_nav.quantity == 15
            assert loaded_nav.price == 249.99
            assert loaded_nav.brand == "Garmin"

            # Delete and verify
            file_handler.delete_item("NS401")
            assert file_handler.get_item("NS401") is None

            logger.info("Data persistence test passed")
        except Exception as e:
            logger.error(f"Data persistence test failed: {str(e)}")
            raise
