# backend/tests/test_stock_item.py

import pytest
import sys
import os
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from models.stock_item import StockItem
from utils import setup_logger
from utils.exceptions import StockError

logger = setup_logger(__name__)

class TestStockItem:
    def test_initialization(self):
        """Test stock item initialization"""
        try:
            # Test valid initialization
            item = StockItem("W101", 10, 99.99)
            assert item.stock_code == "W101"
            assert item.quantity == 10
            assert item.price == 99.99
            logger.info("Valid initialization test passed")

            # Test invalid initializations
            with pytest.raises(StockError):
                StockItem("", 10, 99.99)  # Empty stock code

            with pytest.raises(StockError):
                StockItem("W101", -5, 99.99)  # Negative quantity

            with pytest.raises(StockError):
                StockItem("W101", 10, -99.99)  # Negative price

            logger.info("Invalid initialization tests passed")

        except Exception as e:
            logger.error(f"Initialization test failed: {str(e)}")
            raise

    def test_stock_operations(self):
        """Test stock increase and decrease operations"""
        try:
            item = StockItem("W101", 10, 99.99)

            # Test stock increase
            item.increase_stock(5)
            assert item.quantity == 15

            # Test selling stock
            assert item.sell_stock(3)
            assert item.quantity == 12

            # Test invalid operations
            with pytest.raises(StockError):
                item.increase_stock(-1)  # Negative increase

            with pytest.raises(StockError):
                item.increase_stock(90)  # Exceeds limit

            assert not item.sell_stock(20)  # Try to sell more than available

            logger.info("Stock operations tests passed")

        except Exception as e:
            logger.error(f"Stock operations test failed: {str(e)}")
            raise

    def test_price_operations(self):
        """Test price-related operations"""
        try:
            item = StockItem("W101", 10, 99.99)

            # Test VAT calculation
            assert item.get_VAT() == 17.5
            expected_vat_price = 99.99 * (1 + 17.5/100)
            assert item.get_price_with_VAT() == expected_vat_price

            # Test price update
            item.price = 149.99
            assert item.price == 149.99

            # Test invalid price
            with pytest.raises(ValueError):
                item.price = -50

            logger.info("Price operations tests passed")

        except Exception as e:
            logger.error(f"Price operations test failed: {str(e)}")
            raise

    def test_string_representation(self):
        """Test string representation of stock item"""
        try:
            item = StockItem("W101", 10, 99.99)
            str_repr = str(item)

            assert "Stock Category: Car accessories" in str_repr
            assert "StockCode: W101" in str_repr
            assert "Unknown Stock Name" in str_repr
            assert "Unknown Stock Description" in str_repr

            logger.info("String representation test passed")

        except Exception as e:
            logger.error(f"String representation test failed: {str(e)}")
            raise

    def test_data_conversion(self):
        """Test conversion to dictionary"""
        try:
            item = StockItem("W101", 10, 99.99)
            data = item.to_dict()

            assert data['stock_code'] == "W101"
            assert data['quantity'] == 10
            assert data['price'] == 99.99
            assert 'stock_category' in data
            assert 'stock_name' in data
            assert 'description' in data

            logger.info("Data conversion test passed")

        except Exception as e:
            logger.error(f"Data conversion test failed: {str(e)}")
            raise
