"""
sales_manager.py
-----------------
Contains the SalesManager class, responsible for the Sales Management
Module:

    - Record a sale (reduces stock automatically, calculates total)
    - Sales summary (total items sold, total revenue)
    - Sales report (most sold product, etc.)

Sales are persisted to data/sales.json via JSONStorage.
"""

from datetime import datetime
from storage import JSONStorage
from exceptions import InvalidQuantityError


class SalesManager:
    def __init__(self, inventory_manager, filepath="data/sales.json"):
        self.inventory_manager = inventory_manager
        self.storage = JSONStorage(filepath)
        self.sales = self.storage.read()  # list of plain dicts

    def _save_sales(self):
        self.storage.write(self.sales)

    # ------------------------------------------------------------------
    # Recording sales
    # ------------------------------------------------------------------
    def record_sale(self, product_id, quantity_sold):
        """
        Record a sale of `quantity_sold` units of `product_id`.
        Automatically reduces stock and calculates the total sale amount.
        Raises exceptions (propagated from InventoryManager) if the
        product doesn't exist or stock is insufficient.
        """
        if quantity_sold <= 0:
            raise InvalidQuantityError("Quantity sold must be a positive number.")

        product = self.inventory_manager.get_product_or_raise(product_id)

        # This will raise InsufficientStockError if not enough stock
        self.inventory_manager.reduce_stock(product_id, quantity_sold)

        total_amount = round(product.price * quantity_sold, 2)
        sale_record = {
            "product_id": product.product_id,
            "product_name": product.name,
            "quantity_sold": quantity_sold,
            "unit_price": product.price,
            "total_amount": total_amount,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.sales.append(sale_record)
        self._save_sales()
        return sale_record

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------
    def total_products_sold(self):
        return sum(sale["quantity_sold"] for sale in self.sales)

    def total_revenue(self):
        return round(sum(sale["total_amount"] for sale in self.sales), 2)

    def most_sold_product(self):
        """Return (product_name, total_quantity_sold) for the top seller, or None."""
        if not self.sales:
            return None

        totals = {}
        for sale in self.sales:
            key = (sale["product_id"], sale["product_name"])
            totals[key] = totals.get(key, 0) + sale["quantity_sold"]

        best_key = max(totals, key=totals.get)
        return best_key[1], totals[best_key]

    def all_sales(self):
        return self.sales
