# utils/file_handler.py

import csv
import logging
from typing import List, Dict, Union, Tuple, Optional
import os
from utils.exceptions import FileOperationError, StockError
from models.types import StockItemProtocol
from pathlib import Path

logger = logging.getLogger(__name__)

class StockFileHandler:
    def __init__(self, filename: str = "stock_items.csv"):
        """Initialize file handler with CSV file path."""
        # Create data directory in backend folder
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.data_dir.mkdir(exist_ok=True)
        self.filename = self.data_dir / filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create the CSV file with headers if it doesn't exist."""
        if not self.filename.exists():
            self._write_headers()
            logger.info(f"Created new stock items file at {self.filename}")

    def _write_headers(self):
        """Write CSV headers."""
        headers = ['item_type', 'stock_code', 'quantity', 'price', 'brand']
        try:
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
        except IOError as e:
            logger.error(f"Error writing headers: {str(e)}")
            raise FileOperationError(f"Failed to write headers: {str(e)}")

    def save_item(self, item: StockItemProtocol) -> Tuple[bool, str]:
        """Save a stock item to CSV file."""
        try:
            data = item.to_dict()
            row = [
                type(item).__name__,
                data['stock_code'],
                data['quantity'],
                data['price'],
                data.get('brand', '')
            ]

            # Read existing data
            existing_data = self.load_all_items()

            # Update or append
            updated = False
            for i, existing_item in enumerate(existing_data):
                if existing_item[1] == data['stock_code']:  # Match stock_code
                    existing_data[i] = row
                    updated = True
                    logger.info(f"Updated existing item: {data['stock_code']}")
                    break

            if not updated:
                existing_data.append(row)
                logger.info(f"Added new item: {data['stock_code']}")

            # Write all data back
            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['item_type', 'stock_code', 'quantity', 'price', 'brand'])
                writer.writerows(existing_data)

            return True, "Item saved successfully"

        except Exception as e:
            logger.error(f"Error saving item: {str(e)}")
            raise FileOperationError(f"Failed to save item: {str(e)}")

    def load_all_items(self) -> List[List[str]]:
        """Load all items from CSV file."""
        try:
            if not os.path.exists(self.filename):
                self._ensure_file_exists()
                return []

            with open(self.filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip headers
                return [row for row in reader]
        except Exception as e:
            logger.error(f"Error loading items: {str(e)}")
            raise FileOperationError(f"Failed to load items: {str(e)}")

    def item_exists(self, stock_code: str) -> bool:
        """Check if an item with given stock code exists."""
        try:
            items = self.load_all_items()
            return any(item[1] == stock_code for item in items)
        except Exception as e:
            logger.error(f"Error checking item existence: {str(e)}")
            raise FileOperationError(f"Failed to check item existence: {str(e)}")

    def create_item_from_row(self, row: List[str]) -> StockItemProtocol:
        """Create appropriate item instance from CSV row."""
        try:
            # Import here to avoid circular imports
            from models.nav_sys import NavSys

            if len(row) < 5:
                raise ValueError("Invalid row format")

            item_type, stock_code, quantity, price, brand = row

            try:
                quantity = int(quantity)
                price = float(price)
            except ValueError:
                raise ValueError("Invalid quantity or price format")

            if quantity < 0:
                raise ValueError("Quantity cannot be negative")
            if price < 0:
                raise ValueError("Price cannot be negative")

            if item_type == 'NavSys':
                return NavSys(stock_code, quantity, price, brand)
            else:
                raise ValueError(f"Unknown item type: {item_type}")

        except Exception as e:
            logger.error(f"Error creating item from row: {str(e)}")
            raise FileOperationError(f"Failed to create item from row: {str(e)}")

    def load_items(self):
        """Load and create all item instances from CSV."""
        try:
            items = []
            for row in self.load_all_items():
                try:
                    item = self.create_item_from_row(row)
                    items.append(item)
                except Exception as e:
                    logger.error(f"Skipping invalid row: {row}. Error: {str(e)}")
            return items
        except Exception as e:
            logger.error(f"Error loading items: {str(e)}")
            raise FileOperationError(f"Failed to load items: {str(e)}")

    def delete_item(self, stock_code: str) -> bool:
        """
        Delete an item from CSV file.

        Returns:
            bool: True if item was deleted, False if not found
        """
        try:
            items = self.load_all_items()
            initial_count = len(items)
            items = [item for item in items if item[1] != stock_code]

            if len(items) == initial_count:
                logger.info(f"Item not found for deletion: {stock_code}")
                return False

            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['item_type', 'stock_code', 'quantity', 'price', 'brand'])
                writer.writerows(items)

            logger.info(f"Successfully deleted item: {stock_code}")
            return True

        except Exception as e:
            logger.error(f"Error deleting item: {str(e)}")
            raise FileOperationError(f"Failed to delete item: {str(e)}")

    def get_item(self, stock_code: str) -> Optional[StockItemProtocol]:
        """Get a specific item by stock code."""
        try:
            items = self.load_items()
            return next((item for item in items if item.stock_code == stock_code), None)
        except Exception as e:
            logger.error(f"Error getting item: {str(e)}")
            raise FileOperationError(f"Failed to get item: {str(e)}")
