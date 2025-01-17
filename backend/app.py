# backend/app.py

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import csv
import io
from datetime import datetime
from utils import setup_logger, StockFileHandler, StockError
from models.nav_sys import NavSys
from config import DevelopmentConfig
from utils.sale_handler import SalesHandler

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)

logger = setup_logger(__name__)
file_handler = StockFileHandler()
sales_handler = SalesHandler()

@app.route('/api/items', methods=['GET'])
def get_items():
    """Get items with filtering, sorting, and pagination"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search = request.args.get('search', '').lower()
        brand_filter = request.args.get('brand', '').lower()
        sort_by = request.args.get('sort_by', 'stock_code')
        sort_order = request.args.get('sort_order', 'asc')

        # Load all items first
        all_items = file_handler.load_items()

        # Get all available brands
        all_brands = sorted(list(set(
            item.brand for item in all_items
            if hasattr(item, 'brand') and item.brand and item.brand.strip()
        )))

        # Apply filters before pagination
        filtered_items = all_items

        # Apply search filter
        if search:
            filtered_items = [
                item for item in filtered_items
                if search in item.stock_code.lower() or
                   search in item.get_stock_name().lower() or
                   search in getattr(item, 'brand', '').lower() or
                   search in item.get_stock_description().lower()
            ]

        # Apply brand filter
        if brand_filter:
            filtered_items = [
                item for item in filtered_items
                if hasattr(item, 'brand') and brand_filter in item.brand.lower()
            ]

        # Calculate statistics
        stats = {
            'total_items': len(filtered_items),
            'total_value': sum(item.price * item.quantity for item in filtered_items),
            'total_value_vat': sum(item.get_price_with_VAT() * item.quantity for item in filtered_items),
            'low_stock_items': sum(1 for item in filtered_items if item.quantity < 10)
        }

        # Sort items
        filtered_items.sort(
            key=lambda x: getattr(x, sort_by, x.stock_code),
            reverse=sort_order == 'desc'
        )

        # Paginate after filtering
        total_items = len(filtered_items)
        total_pages = (total_items + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, total_items)
        paginated_items = filtered_items[start_idx:end_idx]

        return jsonify({
            'items': [item.to_dict() for item in paginated_items],
            'pagination': {
                'current_page': page,
                'total_pages': total_pages,
                'total_items': total_items,
                'per_page': per_page
            },
            'statistics': stats,
            'available_brands': all_brands
        })

    except Exception as e:
        logger.error(f"Error getting items: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/items', methods=['POST'])
def add_item():
    """Add a new stock item or update if it exists"""
    try:
        data = request.json

        # Load existing items to check for duplicates
        existing_items = file_handler.load_items()
        existing_item = next((item for item in existing_items
                            if item.stock_code == data['stock_code']), None)

        if existing_item:
            # If item exists, validate the total quantity before updating
            try:
                new_quantity = int(data['quantity'])
                total_quantity = existing_item.quantity + new_quantity

                # Check if total quantity would exceed limit
                if total_quantity > 100:
                    return jsonify({
                        'error': f'Cannot add {new_quantity} items. Total quantity ({total_quantity}) would exceed 100 items limit'
                    }), 400

                # Add the new quantity to existing quantity
                existing_item.increase_stock(new_quantity)

                # Update price if different
                if float(data['price']) != existing_item.price:
                    existing_item.price = float(data['price'])
                # Update brand if different
                if hasattr(existing_item, 'brand') and data['brand'] != existing_item.brand:
                    existing_item._brand = data['brand']

                file_handler.save_item(existing_item)
                logger.info(f"Updated existing item: {existing_item.stock_code}")
                return jsonify({
                    'message': 'Item updated successfully',
                    'item': existing_item.to_dict()
                }), 200
            except Exception as e:
                logger.error(f"Error updating existing item: {str(e)}")
                return jsonify({'error': str(e)}), 400
        else:
            # Create new item if it doesn't exist
            # Validate initial quantity
            if int(data['quantity']) > 100:
                return jsonify({
                    'error': 'Initial quantity cannot exceed 100 items'
                }), 400

            nav_sys = NavSys(
                data['stock_code'],
                int(data['quantity']),
                float(data['price']),
                data['brand']
            )
            file_handler.save_item(nav_sys)
            logger.info(f"Added new item: {nav_sys.stock_code}")
            return jsonify({
                'message': 'Item added successfully',
                'item': nav_sys.to_dict()
            }), 201

    except Exception as e:
        logger.error(f"Error in add_item: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/items/<stock_code>', methods=['PUT'])
def update_item(stock_code):
    """Update an existing stock item"""
    try:
        data = request.json
        items = file_handler.load_items()
        item = next((item for item in items if item.stock_code == stock_code), None)

        if not item:
            return jsonify({'error': 'Item not found'}), 404

        if 'price' in data:
            # Validate price
            try:
                new_price = float(data['price'])
                if new_price <= 0:
                    return jsonify({'error': 'Price must be greater than 0'}), 400
                item.price = new_price
                logger.info(f"Updated price for {stock_code} to {new_price}")
            except ValueError:
                return jsonify({'error': 'Invalid price format'}), 400

        if 'quantity' in data:
            try:
                new_quantity = int(data['quantity'])
                if new_quantity <= 0:
                    return jsonify({'error': 'Quantity must be greater than 0'}), 400

                # Check if adding this quantity would exceed 100
                total_quantity = item.quantity + new_quantity
                if total_quantity > 100:
                    return jsonify({
                        'error': f'Cannot add {new_quantity} items. Total quantity ({total_quantity}) would exceed 100 items limit'
                    }), 400

                item.increase_stock(new_quantity)
                logger.info(f"Updated quantity for {stock_code} by adding {new_quantity}")
            except ValueError:
                return jsonify({'error': 'Invalid quantity format'}), 400
            except StockError as e:
                return jsonify({'error': str(e)}), 400

        if 'brand' in data:
            if not data['brand'].strip():
                return jsonify({'error': 'Brand cannot be empty'}), 400
            item._brand = data['brand']
            logger.info(f"Updated brand for {stock_code} to {data['brand']}")

        file_handler.save_item(item)
        return jsonify({
            'message': 'Item updated successfully',
            'item': item.to_dict()
        })
    except Exception as e:
        logger.error(f"Error updating item: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/items/<stock_code>/sell', methods=['POST'])
def sell_item(stock_code):
    """Sell quantity of an item"""
    try:
        data = request.json
        quantity = int(data['quantity'])

        if quantity <= 0:
            return jsonify({'error': 'Quantity must be greater than 0'}), 400

        items = file_handler.load_items()
        item = next((item for item in items if item.stock_code == stock_code), None)

        if not item:
            return jsonify({'error': 'Item not found'}), 404

        if quantity > item.quantity:
            return jsonify({
                'error': f'Cannot sell {quantity} items. Only {item.quantity} items available in stock'
            }), 400

        if item.sell_stock(quantity):
            # Save updated inventory
            file_handler.save_item(item)

            # Record the sale
            sales_handler.record_sale(
                stock_code=stock_code,
                quantity=quantity,
                price=item.price,
                brand=getattr(item, 'brand', 'N/A')
            )

            logger.info(f"Sold {quantity} units of {stock_code}")
            return jsonify({
                'message': f'Successfully sold {quantity} units',
                'item': item.to_dict()
            })

        return jsonify({'error': 'Failed to sell items'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid quantity format'}), 400
    except Exception as e:
        logger.error(f"Error selling item: {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.route('/api/sales/history', methods=['GET'])
def get_sales_history():
    """Get sales history data"""
    try:
        sales_data = sales_handler.get_sales_history()
        return jsonify(sales_data)
    except Exception as e:
        logger.error(f"Error getting sales history: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/sales/export', methods=['GET'])
def export_sales():
    """Export sales history to CSV"""
    try:
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            'Date', 'Stock Code', 'Quantity', 'Price', 'Brand', 'Revenue'
        ])

        sales_rows = sales_handler.get_all_sales()
        writer.writerows(sales_rows)

        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition':
                f'attachment; filename=sales_history_{datetime.now().strftime("%Y%m%d")}.csv'
            }
        )
    except Exception as e:
        logger.error(f"Error exporting sales: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/sales/summary', methods=['GET'])
def get_sales_summary():
    """Get sales summary statistics"""
    try:
        summary = sales_handler.get_sales_summary()
        return jsonify(summary)
    except Exception as e:
        logger.error(f"Error getting sales summary: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/items/<stock_code>', methods=['DELETE'])
def delete_item(stock_code):
    """Delete a stock item"""
    try:
        if file_handler.delete_item(stock_code):
            logger.info(f"Deleted item: {stock_code}")
            return jsonify({'message': 'Item deleted successfully'}), 200
        return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        logger.error(f"Error deleting item: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/items/export', methods=['GET'])
def export_items():
    """Export items to CSV"""
    try:
        items = file_handler.load_items()
        output = io.StringIO()
        writer = csv.writer(output)

        # Write headers
        writer.writerow([
            'Stock Code', 'Name', 'Description', 'Quantity',
            'Price', 'Price with VAT', 'Brand'
        ])

        # Write data
        for item in items:
            writer.writerow([
                item.stock_code,
                item.get_stock_name(),
                item.get_stock_description(),
                item.quantity,
                item.price,
                item.get_price_with_VAT(),
                getattr(item, 'brand', 'N/A')
            ])

        # Prepare response
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition':
                f'attachment; filename=stock_items_{datetime.now().strftime("%Y%m%d")}.csv'
            }
        )
    except Exception as e:
        logger.error(f"Error exporting items: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
