import pytest
from decimal import Decimal
from models.stock_item import StockItem
from utils.exceptions import StockError
from utils.logger import setup_logger

logger = setup_logger(__name__)

class TestStockItem:
    """Comprehensive test suite for StockItem base class."""

    def test_basic_functionality(self):
        """TC-BF: Basic functionality tests."""
        try:
            # TC-BF-01: Valid initialization
            item = StockItem("W101", 10, 99.99)
            assert item.stock_code == "W101"
            assert item.quantity == 10
            assert item.price == 99.99

            # TC-BF-02: Get stock name
            assert item.get_stock_name() == "Unknown Stock Name"

            # TC-BF-03: Get stock description
            assert item.get_stock_description() == "Unknown Stock Description"

            # TC-BF-04: Get VAT rate
            assert item.get_VAT() == 17.5

            # TC-BF-05: Get price with VAT
            expected_vat_price = 99.99 * (1 + 17.5/100)
            assert item.get_price_with_VAT() == expected_vat_price

            logger.info("Basic functionality tests passed")
        except Exception as e:
            logger.error(f"Basic functionality tests failed: {str(e)}")
            raise

    def test_validation(self):
        """TC-VL: Validation tests."""
        try:
            # TC-VL-01: Empty stock code
            with pytest.raises(StockError) as exc_info:
                StockItem("", 10, 99.99)
            assert "Stock code must be a non-empty string" in str(exc_info.value)

            # TC-VL-02: Negative quantity
            with pytest.raises(StockError) as exc_info:
                StockItem("W101", -5, 99.99)
            assert "Quantity must be a non-negative integer" in str(exc_info.value)

            # TC-VL-03: Negative price
            with pytest.raises(StockError) as exc_info:
                StockItem("W101", 10, -99.99)
            assert "Price must be a non-negative number" in str(exc_info.value)

            # TC-VL-04: Non-string stock code
            with pytest.raises(StockError):
                StockItem(123, 10, 99.99)

            # TC-VL-05: Non-numeric quantity
            with pytest.raises(StockError):
                StockItem("W101", "ten", 99.99)

            logger.info("Validation tests passed")
        except Exception as e:
            logger.error(f"Validation tests failed: {str(e)}")
            raise

    def test_stock_operations(self):
        """TC-SO: Stock operation tests."""
        try:
            item = StockItem("W101", 10, 99.99)

            # TC-SO-01: Valid stock increase
            item.increase_stock(10)
            assert item.quantity == 20

            # TC-SO-02: Exceed stock limit
            with pytest.raises(StockError) as exc_info:
                item.increase_stock(81)
            assert "Stock cannot exceed 100 items" in str(exc_info.value)

            # TC-SO-03: Valid stock sale
            assert item.sell_stock(5)
            assert item.quantity == 15

            # TC-SO-04: Overselling attempt
            assert not item.sell_stock(20)
            assert item.quantity == 15

            # TC-SO-05: Zero quantity sale
            with pytest.raises(StockError):
                item.sell_stock(0)

            logger.info("Stock operation tests passed")
        except Exception as e:
            logger.error(f"Stock operation tests failed: {str(e)}")
            raise

    def test_price_operations(self):
        """TC-UO: Update operation tests."""
        try:
            item = StockItem("W101", 10, 99.99)

            # TC-UO-01: Valid price update
            item.price = 149.99
            assert item.price == 149.99

            # TC-UO-02: Invalid price update
            with pytest.raises(ValueError):
                item.price = 0

            # TC-UO-03: Negative price update
            with pytest.raises(ValueError):
                item.price = -99.99

            # TC-UO-04: Large price value
            item.price = 999999.99
            assert item.price == 999999.99

            # TC-UO-05: Small price value
            item.price = 0.01
            assert item.price == 0.01

            logger.info("Price operation tests passed")
        except Exception as e:
            logger.error(f"Price operation tests failed: {str(e)}")
            raise

    def test_data_conversion(self):
        """TC-DC: Data conversion tests."""
        try:
            item = StockItem("W101", 10, 99.99)

            # TC-DC-01: String representation
            str_repr = str(item)
            assert "Stock Category: Car accessories" in str_repr
            assert "StockCode: W101" in str_repr
            assert "PriceWithoutVAT: 99.99" in str_repr

            # TC-DC-02: Dictionary conversion
            data = item.to_dict()
            assert data['stock_code'] == "W101"
            assert data['quantity'] == 10
            assert data['price'] == 99.99

            # TC-DC-03: Stock category access
            assert item._stock_category == "Car accessories"

            # TC-DC-04: Price string format
            assert f"{item.price:.2f}" == "99.99"

            # TC-DC-05: VAT price string format
            vat_price = item.get_price_with_VAT()
            assert f"{vat_price:.2f}" == "117.49"

            logger.info("Data conversion tests passed")
        except Exception as e:
            logger.error(f"Data conversion tests failed: {str(e)}")
            raise

    def test_edge_cases(self):
        """TC-EC: Edge case tests."""
        try:
            # TC-EC-01: Minimum valid values
            item = StockItem("W101", 0, 0.01)
            assert item.quantity == 0
            assert item.price == 0.01

            # TC-EC-02: Maximum valid values
            item = StockItem("W101", 100, 999999.99)
            assert item.quantity == 100
            assert item.price == 999999.99

            # TC-EC-03: Special characters in stock code
            item = StockItem("W-101_A/B", 10, 99.99)
            assert item.stock_code == "W-101_A/B"

            # TC-EC-04: Price precision edge cases
            item = StockItem("W101", 10, 1/3)
            assert abs(item.price - 0.33) < 0.01

            # TC-EC-05: Quantity limits
            item = StockItem("W101", 100, 99.99)
            with pytest.raises(StockError):
                item.increase_stock(1)

            logger.info("Edge case tests passed")
        except Exception as e:
            logger.error(f"Edge case tests failed: {str(e)}")
            raise

    def test_boundary_conditions(self):
        """Additional boundary condition tests."""
        try:
            item = StockItem("W101", 10, 99.99)

            # Test maximum quantity using proper method
            item = StockItem("W101", 0, 99.99)
            item.increase_stock(100)
            assert item.quantity == 100

            # Test minimum price
            item.price = 0.01
            assert item.price == 0.01

            # Test price rounding using exact values
            item.price = 123.45
            assert item.price == 123.45

            # Test consecutive operations
            item = StockItem("W101", 50, 99.99)
            item.increase_stock(25)
            item.sell_stock(15)
            assert item.quantity == 60

            logger.info("Boundary condition tests passed")
        except Exception as e:
            logger.error(f"Boundary condition tests failed: {str(e)}")
            raise
