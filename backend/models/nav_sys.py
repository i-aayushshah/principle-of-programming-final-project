# models/nav_sys.py

import logging
from models.stock_item import StockItem
from utils.exceptions import StockError

logger = logging.getLogger(__name__)

class NavSys(StockItem):
    """Navigation System class that inherits from StockItem."""

    def __init__(self, stock_code: str, quantity: int, price: float, brand: str):
        """Initialize a navigation system item."""
        super().__init__(stock_code, quantity, price)
        try:
            self._validate_brand(brand)
            self._brand = brand
            logger.info(f"Created new NavSys item: {stock_code}, brand: {brand}")
        except ValueError as e:
            logger.error(f"Error setting brand: {str(e)}")
            raise StockError(f"Invalid brand: {str(e)}")

    def _validate_brand(self, brand: str):
        """Validate brand parameter."""
        if not isinstance(brand, str) or not brand:
            raise ValueError("Brand must be a non-empty string")

    @property
    def brand(self) -> str:
        """Get nav system brand."""
        return self._brand

    @brand.setter
    def brand(self, new_brand: str) -> None:
        """Set new brand."""
        self._validate_brand(new_brand)
        self._brand = new_brand
        logger.info(f"Updated brand for {self.stock_code} to {new_brand}")

    def get_stock_name(self) -> str:
        return "Navigation system"

    def get_stock_description(self) -> str:
        return "GeoVision Sat Nav"

    def __str__(self) -> str:
        return f"{super().__str__()}\nBrand: {self._brand}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['brand'] = self._brand
        return data
