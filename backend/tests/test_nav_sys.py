# backend/tests/test_nav_sys.py

import pytest
import sys
import os
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from models.nav_sys import NavSys
from utils import setup_logger
from utils.exceptions import StockError

logger = setup_logger(__name__)

class TestNavSys:
    def test_initialization(self):
        """Test NavSys initialization"""
        try:
            # Test valid initialization
            nav = NavSys("NS101", 10, 199.99, "TomTom")
            assert nav.stock_code == "NS101"
            assert nav.quantity == 10
            assert nav.price == 199.99
            assert nav.brand == "TomTom"
            logger.info("Valid initialization test passed")

            # Test invalid initializations
            with pytest.raises(StockError):
                NavSys("", 10, 199.99, "TomTom")  # Empty stock code

            with pytest.raises(StockError):
                NavSys("NS101", -5, 199.99, "TomTom")  # Negative quantity

            with pytest.raises(StockError):
                NavSys("NS101", 10, -199.99, "TomTom")  # Negative price

            with pytest.raises(StockError):
                NavSys("NS101", 10, 199.99, "")  # Empty brand

            logger.info("Invalid initialization tests passed")

        except Exception as e:
            logger.error(f"Initialization test failed: {str(e)}")
            raise

    def test_stock_operations(self):
        """Test stock management operations"""
        try:
            nav = NavSys("NS101", 10, 199.99, "TomTom")

            # Test stock increase
            nav.increase_stock(5)
            assert nav.quantity == 15

            # Test selling stock
            assert nav.sell_stock(3)
            assert nav.quantity == 12

            # Test invalid operations
            with pytest.raises(StockError):
                nav.increase_stock(-1)  # Negative increase

            with pytest.raises(StockError):
                nav.increase_stock(90)  # Exceeds limit

            assert not nav.sell_stock(20)  # Try to sell more than available

            logger.info("Stock operations tests passed")

        except Exception as e:
            logger.error(f"Stock operations test failed: {str(e)}")
            raise

    def test_price_operations(self):
        """Test price-related operations"""
        try:
            nav = NavSys("NS101", 10, 199.99, "TomTom")

            # Test VAT calculation
            assert nav.get_VAT() == 17.5
            expected_vat_price = 199.99 * (1 + 17.5/100)
            assert nav.get_price_with_VAT() == expected_vat_price

            # Test price update
            nav.price = 249.99
            assert nav.price == 249.99

            # Test invalid price
            with pytest.raises(ValueError):
                nav.price = -50

            logger.info("Price operations tests passed")

        except Exception as e:
            logger.error(f"Price operations test failed: {str(e)}")
            raise

    def test_string_representation(self):
        """Test string representation of NavSys"""
        try:
            nav = NavSys("NS101", 10, 199.99, "TomTom")
            str_repr = str(nav)

            assert "Stock Category: Car accessories" in str_repr
            assert "Stock Type: Navigation system" in str_repr
            assert "Description: GeoVision Sat Nav" in str_repr
            assert "StockCode: NS101" in str_repr
            assert "Brand: TomTom" in str_repr

            logger.info("String representation test passed")

        except Exception as e:
            logger.error(f"String representation test failed: {str(e)}")
            raise

    def test_data_conversion(self):
        """Test conversion to dictionary"""
        try:
            nav = NavSys("NS101", 10, 199.99, "TomTom")
            data = nav.to_dict()

            assert data['stock_code'] == "NS101"
            assert data['quantity'] == 10
            assert data['price'] == 199.99
            assert data['brand'] == "TomTom"
            assert data['stock_name'] == "Navigation system"
            assert data['description'] == "GeoVision Sat Nav"

            logger.info("Data conversion test passed")

        except Exception as e:
            logger.error(f"Data conversion test failed: {str(e)}")
            raise

    def test_brand_operations(self):
        """Test brand-related operations"""
        try:
            nav = NavSys("NS101", 10, 199.99, "TomTom")

            # Test brand getter
            assert nav.brand == "TomTom"

            # Test brand update
            nav._brand = "Garmin"
            assert nav.brand == "Garmin"

            logger.info("Brand operations tests passed")

        except Exception as e:
            logger.error(f"Brand operations test failed: {str(e)}")
            raise
