from typing import Protocol

class StockItemProtocol(Protocol):
    """Protocol defining the interface for stock items"""
    stock_code: str
    quantity: int
    price: float

    def to_dict(self) -> dict:
        """Convert item to dictionary"""
        ...

    def get_stock_name(self) -> str:
        """Get stock name"""
        ...
