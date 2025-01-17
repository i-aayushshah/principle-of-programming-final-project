# models/stock_item.py

import logging
from abc import ABC, abstractmethod
from utils.exceptions import StockError

logger = logging.getLogger(__name__)

class StockItem(ABC):
    """Base class for all stock items in the car parts shop."""

    # Class variable shared by all instances
    _stock_category = "Car accessories"

    def __init__(self, stock_code: str, quantity: int, price: float):
        """
        Initialize a stock item.

        Args:
            stock_code (str): Unique identifier for the stock item
            quantity (int): Initial quantity of the item
            price (float): Price per unit without VAT

        Raises:
            StockError: If any of the input parameters are invalid
        """
        try:
            self._validate_init_params(stock_code, quantity, price)
            self._stock_code = stock_code
            self._quantity = quantity
            self._price = price
            logger.info(f"Created new stock item: {stock_code}")
        except ValueError as e:
            logger.error(f"Error creating stock item: {str(e)}")
            raise StockError(f"Invalid parameters: {str(e)}")

    def _validate_init_params(self, stock_code: str, quantity: int, price: float):
        """Validate initialization parameters."""
        if not isinstance(stock_code, str) or not stock_code:
            raise ValueError("Stock code must be a non-empty string")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number")

    @property
    def stock_code(self) -> str:
        """Get stock code."""
        return self._stock_code

    @property
    def quantity(self) -> int:
        """Get current quantity."""
        return self._quantity

    @property
    def price(self) -> float:
        """Get price without VAT."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """Set new price."""
        try:
            new_price = float(new_price)
            if new_price <= 0:
                raise ValueError("Price must be greater than 0")
            self._price = new_price
            logger.info(f"Updated price to {new_price}")
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid price value: {str(e)}")
            raise ValueError(f"Invalid price value: {str(e)}")


    def increase_stock(self, amount: int) -> None:
        """
        Increase stock level by the given amount.

        Args:
            amount (int): Amount to increase

        Raises:
            StockError: If amount is invalid or would exceed maximum stock
        """
        try:
            if amount < 1:
                raise ValueError("Increased item must be greater than or equal to one")
            if self._quantity + amount > 100:
                raise ValueError("Stock cannot exceed 100 items")
            self._quantity += amount
            logger.info(f"Increased stock for {self._stock_code} by {amount}")
        except ValueError as e:
            logger.error(f"Error increasing stock: {str(e)}")
            raise StockError(f"The error was: {str(e)}")

    def sell_stock(self, amount: int) -> bool:
        """
        Attempt to sell the given amount of stock.

        Args:
            amount (int): Amount to sell

        Returns:
            bool: True if sale successful, False if insufficient stock

        Raises:
            StockError: If amount is invalid
        """
        try:
            if amount < 1:
                raise ValueError("Amount must be greater than zero")
            if amount > self._quantity:
                return False
            self._quantity -= amount
            logger.info(f"Sold {amount} units of {self._stock_code}")
            return True
        except ValueError as e:
            logger.error(f"Error selling stock: {str(e)}")
            raise StockError(f"The error was: {str(e)}")

    def get_VAT(self) -> float:
        """Return standard VAT rate."""
        return 17.5

    def get_price_with_VAT(self) -> float:
        """Calculate price including VAT."""
        return self.price * (1 + self.get_VAT() / 100)

    def get_stock_name(self) -> str:
        """Get stock name - can be overridden by subclasses."""
        return "Unknown Stock Name"

    def get_stock_description(self) -> str:
        """Get stock description - can be overridden by subclasses."""
        return "Unknown Stock Description"

    def __str__(self) -> str:
        """Return string representation of the stock item."""
        return (
            f"Stock Category: {self._stock_category}\n"
            f"Stock Type: {self.get_stock_name()}\n"
            f"Description: {self.get_stock_description()}\n"
            f"StockCode: {self._stock_code}\n"
            f"PriceWithoutVAT: {self.price:.2f}\n"
            f"PriceWithVAT: {self.get_price_with_VAT():.2f}\n"
            f"Total unit in stock: {self._quantity}"
        )

    def to_dict(self) -> dict:
        """Convert stock item to dictionary for serialization."""
        return {
            'stock_category': self._stock_category,
            'stock_code': self._stock_code,
            'stock_name': self.get_stock_name(),
            'description': self.get_stock_description(),
            'quantity': self._quantity,
            'price': self.price,
            'price_with_vat': self.get_price_with_VAT()
        }


