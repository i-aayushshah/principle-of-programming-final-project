import pytest
from models.nav_sys import NavSys
from utils.exceptions import StockError
from utils.logger import setup_logger

logger = setup_logger(__name__)

class TestNavSys:
    """Comprehensive test suite for NavSys class."""

    def test_basic_functionality(self):
        """TC-BF: Basic functionality tests."""
        try:
            # TC-BF-01: Valid initialization
            nav = NavSys("NS101", 10, 199.99, "TomTom")
            assert nav.stock_code == "NS101"
            assert nav.quantity == 10
            assert nav.price == 199.99
            assert nav.brand == "TomTom"

            # TC-BF-02: Get stock name override
            assert nav.get_stock_name() == "Navigation system"

            # TC-BF-03: Get stock description override
            assert nav.get_stock_description() == "GeoVision Sat Nav"

            # TC-BF-04: VAT calculation
            assert nav.get_VAT() == 17.5

            # TC-BF-05: Price with VAT
            expected_vat_price = 199.99 * (1 + 17.5/100)
            assert nav.get_price_with_VAT() == expected_vat_price

            logger.info("Basic functionality tests passed")
        except Exception as e:
            logger.error(f"Basic functionality tests failed: {str(e)}")
            raise

    def test_brand_validation(self):
        """TC-VL: Brand-specific validation tests."""
        try:
            # TC-VL-01: Empty brand
            with pytest.raises(StockError) as exc_info:
                NavSys("NS101", 10, 199.99, "")
            assert "Brand must be a non-empty string" in str(exc_info.value)

            # TC-VL-02: None brand
            with pytest.raises(StockError):
                NavSys("NS101", 10, 199.99, None)

            # TC-VL-03: Non-string brand
            with pytest.raises(StockError):
                NavSys("NS101", 10, 199.99, 123)

            # TC-VL-04: Brand setter with empty string
            nav = NavSys("NS101", 10, 199.99, "TomTom")
            with pytest.raises(StockError):
                nav.brand = ""

            # TC-VL-05: Brand setter with None
            with pytest.raises(StockError):
                nav.brand = None

            logger.info("Brand validation tests passed")
        except Exception as e:
            logger.error(f"Brand validation tests failed: {str(e)}")
            raise

    def test_brand_operations(self):
        """TC-UO: Brand update operation tests."""
        try:
            nav = NavSys("NS101", 10, 199.99, "TomTom")

            # TC-UO-01: Valid brand update
            nav.brand = "Garmin"
            assert nav.brand == "Garmin"

            # TC-UO-02: Brand with special characters
            nav.brand = "Geo-Vision™ 2.0"
            assert nav.brand == "Geo-Vision™ 2.0"

            # TC-UO-03: Brand with leading/trailing spaces
            nav.brand = "  TomTom  "
            assert nav.brand == "  TomTom  "

            # TC-UO-04: Brand with numbers
            nav.brand = "TomTom123"
            assert nav.brand == "TomTom123"

            # TC-UO-05: Brand with Unicode characters
            nav.brand = "导航系统"
            assert nav.brand == "导航系统"

            logger.info("Brand operation tests passed")
        except Exception as e:
            logger.error(f"Brand operation tests failed: {str(e)}")
            raise

    def test_inheritance_behavior(self):
        """Test inheritance-specific behavior."""
        try:
            nav = NavSys("NS101", 10, 199.99, "TomTom")

            # Test inherited stock operations
            nav.increase_stock(5)
            assert nav.quantity == 15

            assert nav.sell_stock(3)
            assert nav.quantity == 12

            # Test inherited price operations
            nav.price = 249.99
            assert nav.price == 249.99
            assert nav.get_price_with_VAT() == 249.99 * (1 + 17.5/100)

            # Test overridden string representation
            str_repr = str(nav)
            assert "Navigation system" in str_repr
            assert "GeoVision Sat Nav" in str_repr
            assert "TomTom" in str_repr

            logger.info("Inheritance behavior tests passed")
        except Exception as e:
            logger.error(f"Inheritance behavior tests failed: {str(e)}")
            raise

    def test_data_conversion(self):
        """TC-DC: Data conversion tests specific to NavSys."""
        try:
            nav = NavSys("NS101", 10, 199.99, "TomTom")

            # TC-DC-01: String representation
            str_repr = str(nav)
            assert all(text in str_repr for text in [
                "Navigation system",
                "GeoVision Sat Nav",
                "NS101",
                "TomTom"
            ])

            # TC-DC-02: Dictionary conversion
            data = nav.to_dict()
            assert data['stock_code'] == "NS101"
            assert data['brand'] == "TomTom"
            assert data['stock_name'] == "Navigation system"
            assert data['description'] == "GeoVision Sat Nav"

            # TC-DC-03: Price formatting
            assert f"{nav.price:.2f}" == "199.99"

            # TC-DC-04: VAT calculation
            vat_price = nav.get_price_with_VAT()
            assert abs(vat_price - (199.99 * 1.175)) < 0.01

            # TC-DC-05: Complete object state
            assert all(hasattr(nav, attr) for attr in [
                '_stock_code', '_quantity', '_price', '_brand'
            ])

            logger.info("Data conversion tests passed")
        except Exception as e:
            logger.error(f"Data conversion tests failed: {str(e)}")
            raise

    def test_edge_cases(self):
        """TC-EC: Edge cases specific to NavSys."""
        try:
            # TC-EC-01: Unicode brand names
            nav = NavSys("NS101", 10, 199.99, "导航系统")
            assert nav.brand == "导航系统"

            # TC-EC-02: Very long brand name
            long_brand = "a" * 1000
            nav = NavSys("NS101", 10, 199.99, long_brand)
            assert nav.brand == long_brand

            # TC-EC-03: Special characters in both stock code and brand
            nav = NavSys("NS-101/A", 10, 199.99, "Geo-Vision™")
            assert nav.stock_code == "NS-101/A"
            assert nav.brand == "Geo-Vision™"

            # TC-EC-04: Price precision
            nav = NavSys("NS101", 10, 100.00, "TomTom")  # Use exact value
            assert nav.price == 100.00

            # TC-EC-05: Zero quantity operations
            nav = NavSys("NS101", 0, 199.99, "TomTom")
            assert not nav.sell_stock(1)

            # TC-EC-06: Boundary price values
            nav = NavSys("NS101", 10, 0.01, "TomTom")  # Minimum price
            assert nav.price == 0.01

            nav.price = 999999.99  # Maximum price
            assert nav.price == 999999.99

            # TC-EC-07: Brand with mixed content
            nav.brand = "TomTom Nav-2023 (™) あ"
            assert nav.brand == "TomTom Nav-2023 (™) あ"

            # TC-EC-08: Brand with only numbers
            nav.brand = "12345"
            assert nav.brand == "12345"

            # TC-EC-09: Maximum quantity operations
            nav = NavSys("NS101", 0, 199.99, "TomTom")
            nav.increase_stock(100)  # Use increase_stock instead of direct assignment
            assert nav.quantity == 100

            # TC-EC-10: Complex mixed operations
            nav = NavSys("NS101", 50, 199.99, "TomTom")
            nav.increase_stock(25)
            nav.sell_stock(15)
            nav.price = 299.99
            nav.brand = "Garmin"
            assert nav.quantity == 60
            assert nav.price == 299.99
            assert nav.brand == "Garmin"

            logger.info("Edge cases tests passed")
        except Exception as e:
            logger.error(f"Edge cases tests failed: {str(e)}")
            raise
