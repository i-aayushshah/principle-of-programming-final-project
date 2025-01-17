# models/nav_sys.py

import logging
from .stock_item import StockItem
from utils.exceptions import StockError

logger = logging.getLogger(__name__)

class NavSys(StockItem):
    """Navigation system stock item."""

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

    def _validate_brand(self, brand: str) -> None:
        """Validate brand parameter."""
        if not isinstance(brand, str) or not brand.strip():
            raise StockError("Brand must be a non-empty string")
        try:
            # Validate that the brand can be properly encoded/decoded
            brand.encode('utf-8').decode('utf-8')
        except UnicodeError:
            raise StockError("Invalid brand name encoding")

    @property
    def brand(self) -> str:
        """Get nav system brand."""
        return self._brand

    @brand.setter
    def brand(self, new_brand: str) -> None:
        """Set new brand."""
        try:
            self._validate_brand(new_brand)
            self._brand = new_brand
            logger.info(f"Updated brand for {self.stock_code} to {new_brand}")
        except ValueError as e:
            logger.error(f"Error setting brand: {str(e)}")
            raise StockError(f"Invalid brand: {str(e)}")

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
