# backend/demo_run.py

from models.nav_sys import NavSys
from utils.file_handler import StockFileHandler
from utils.logger import setup_logger

logger = setup_logger(__name__)

def run_demo():
    """Demonstrate basic operations of the car parts shop system"""
    try:
        # Initialize file handler
        file_handler = StockFileHandler()

        print("\n=== Car Parts Shop Demo ===\n")

        # Create some navigation systems
        nav1 = NavSys("NS101", 10, 199.99, "TomTom")
        nav2 = NavSys("NS102", 15, 299.99, "Garmin")

        print("Created navigation systems:")
        print(f"1. {nav1}")
        print(f"\n2. {nav2}")

        # Save items to file
        file_handler.save_item(nav1)
        file_handler.save_item(nav2)
        print("\nSaved items to file.")

        # Load and display all items
        items = file_handler.load_items()
        print("\nLoaded items from file:")
        for item in items:
            print(f"\n{item}")

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
        items = file_handler.load_items()
        for item in items:
            print(f"\n{item}")

    except Exception as e:
        print(f"\nError in demo: {str(e)}")

if __name__ == "__main__":
    run_demo()
