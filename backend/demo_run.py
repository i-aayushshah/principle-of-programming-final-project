# backend/demo_run.py

from models.nav_sys import NavSys
from utils.file_handler import StockFileHandler
from utils.logger import setup_logger
import sys
import io
import locale

logger = setup_logger(__name__)

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def run_demo():
    """Demonstrate basic operations of the car parts shop system"""
    try:
        # Initialize file handler
        file_handler = StockFileHandler()

        print("\n=== Car Parts Shop Demo ===\n")

        # Create some navigation systems with ASCII-only brands for demo
        nav1 = NavSys("NS101", 10, 199.99, "TomTom")
        nav2 = NavSys("NS102", 15, 299.99, "Garmin")

        print("Created navigation systems:")
        print(f"1. {nav1}")
        print(f"\n2. {nav2}")

        # Save items to file
        try:
            file_handler.save_item(nav1)
            file_handler.save_item(nav2)
            print("\nSaved items to file.")
        except UnicodeEncodeError as e:
            print(f"\nWarning: Unable to save items due to encoding issue: {str(e)}")
        except Exception as e:
            print(f"\nError saving items: {str(e)}")

        # Load and display all items with encoding error handling
        try:
            items = file_handler.load_items()
            print("\nLoaded items from file:")
            for item in items:
                try:
                    print(f"\n{item}")
                except UnicodeEncodeError:
                    print(f"\nWarning: Unable to display item due to encoding issue")
        except Exception as e:
            print(f"\nError loading items: {str(e)}")

        # Demonstrate stock operations
        print("\n=== Stock Operations ===")

        # Increase stock
        nav1.increase_stock(5)
        print(f"\nIncreased NS101 stock by 5. New quantity: {nav1.quantity}")

        # Sell stock
        nav1.sell_stock(3)
        print(f"Sold 3 units of NS101. Remaining quantity: {nav1.quantity}")

        # Try to exceed stock limit (should raise error)
        print("\n=== Testing Stock Limits ===")
        try:
            nav1.increase_stock(95)
            print("Increased stock (shouldn't see this)")
        except Exception as e:
            print(f"Error (expected): {str(e)}")

        # Display final state
        print("\n=== Final State ===")
        try:
            items = file_handler.load_items()
            for item in items:
                try:
                    print(f"\n{item}")
                except UnicodeEncodeError:
                    print(f"\nWarning: Unable to display item with stock code: {item.stock_code}")
        except Exception as e:
            print(f"\nError loading final state: {str(e)}")

    except Exception as e:
        logger.error(f"Error in demo: {str(e)}")
        print(f"\nError in demo: {str(e)}")

if __name__ == "__main__":
    run_demo()
