# utils/sales_handler.py

import csv
import os
from datetime import datetime
from typing import List, Dict
import logging
from utils.exceptions import FileOperationError

logger = logging.getLogger(__name__)

class SalesHandler:
    def __init__(self, file_path: str = 'data/sales_history.csv'):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create the CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            self._write_headers()

    def _write_headers(self):
        """Write CSV headers."""
        headers = ['date', 'stock_code', 'quantity', 'price', 'brand', 'revenue']
        try:
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
        except IOError as e:
            logger.error(f"Error writing sales headers: {str(e)}")
            raise FileOperationError(f"Failed to write sales headers: {str(e)}")

    def record_sale(self, stock_code: str, quantity: int, price: float, brand: str) -> None:
        """Record a new sale in the CSV file."""
        try:
            revenue = quantity * price
            sale_date = datetime.now().strftime('%Y-%m-%d')

            row = [sale_date, stock_code, quantity, price, brand, revenue]

            with open(self.file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(row)

            logger.info(f"Recorded sale: {stock_code}, {quantity} units")
        except Exception as e:
            logger.error(f"Error recording sale: {str(e)}")
            raise FileOperationError(f"Failed to record sale: {str(e)}")

    def get_sales_history(self) -> Dict:
        """Get formatted sales history for analytics."""
        try:
            daily_sales = {}
            brand_sales = {}

            with open(self.file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Daily sales
                    date = row['date']
                    if date not in daily_sales:
                        daily_sales[date] = {'sales': 0, 'revenue': 0.0}

                    daily_sales[date]['sales'] += int(row['quantity'])
                    daily_sales[date]['revenue'] += float(row['revenue'])

                    # Brand sales
                    brand = row['brand']
                    if brand not in brand_sales:
                        brand_sales[brand] = {'sales': 0, 'revenue': 0.0}

                    brand_sales[brand]['sales'] += int(row['quantity'])
                    brand_sales[brand]['revenue'] += float(row['revenue'])

            # Format data for frontend
            sales_data = {
                'daily': [
                    {'date': date, 'sales': data['sales'], 'revenue': data['revenue']}
                    for date, data in daily_sales.items()
                ],
                'by_brand': [
                    {'brand': brand, 'sales': data['sales'], 'revenue': data['revenue']}
                    for brand, data in brand_sales.items()
                ]
            }

            return sales_data

        except Exception as e:
            logger.error(f"Error getting sales history: {str(e)}")
            raise FileOperationError(f"Failed to get sales history: {str(e)}")

    def get_all_sales(self) -> List[List[str]]:
        """Get all sales data formatted for CSV export."""
        try:
            # First row is headers
            rows = [['Date', 'Stock Code', 'Quantity', 'Price', 'Brand', 'Total Revenue']]

            with open(self.file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rows.append([
                        row['date'],
                        row['stock_code'],
                        row['quantity'],
                        f"${float(row['price']):.2f}",
                        row['brand'],
                        f"${float(row['revenue']):.2f}"
                    ])
            return rows
        except Exception as e:
            logger.error(f"Error getting sales data: {str(e)}")
            raise FileOperationError(f"Failed to get sales data: {str(e)}")
