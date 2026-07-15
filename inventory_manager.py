"""
inventory_manager.py
---------------------
Contains the InventoryManager class, which is responsible for the
Product Management Module and the Stock Management Module:

    - Add / View / Search / Update / Delete products
    - Add stock / Reduce stock
    - Low stock alerts

All product data is persisted to data/products.json via JSONStorage.
"""

from models import Product
from storage import JSONStorage
from exceptions import (
    DuplicateProductError,
    ProductNotFoundError,
    InvalidQuantityError,
    InsufficientStockError,
)

LOW_STOCK_THRESHOLD = 10


class InventoryManager:
    def __init__(self, filepath="data/products.json"):
        self.storage = JSONStorage(filepath)
        self.products = self._load_products()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _load_products(self):
        raw = self.storage.read()
        return [Product.from_dict(item) for item in raw]

    def _save_products(self):
        data = [p.to_dict() for p in self.products]
        self.storage.write(data)

    def _find_by_id(self, product_id):
        product_id = str(product_id).strip()
        for p in self.products:
            if p.product_id == product_id:
                return p
        return None

    # ------------------------------------------------------------------
    # Product Management
    # ------------------------------------------------------------------
    def add_product(self, product_id, name, category, price, quantity, supplier):
        """Add a new product. Raises DuplicateProductError if ID exists."""
        if self._find_by_id(product_id):
            raise DuplicateProductError(
                f"Product ID '{product_id}' already exists.")

        if price < 0:
            raise InvalidQuantityError("Price cannot be negative.")
        if quantity < 0:
            raise InvalidQuantityError("Quantity cannot be negative.")

        product = Product(product_id, name, category, price, quantity, supplier)
        self.products.append(product)
        self._save_products()
        return product

    def view_products(self):
        """Return the full list of products."""
        return self.products

    def search_product(self, keyword):
        """Search by Product ID (exact) or Product Name (partial, case-insensitive)."""
        keyword = str(keyword).strip().lower()
        results = [
            p for p in self.products
            if p.product_id.lower() == keyword or keyword in p.name.lower()
        ]
        if not results:
            raise ProductNotFoundError(
                f"No product found matching '{keyword}'.")
        return results

    def update_product(self, product_id, name=None, category=None,
                        price=None, quantity=None):
        """Update one or more fields of an existing product."""
        product = self._find_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product ID '{product_id}' not found.")

        if name is not None and name != "":
            product.name = name
        if category is not None and category != "":
            product.category = category
        if price is not None:
            if price < 0:
                raise InvalidQuantityError("Price cannot be negative.")
            product.price = price
        if quantity is not None:
            if quantity < 0:
                raise InvalidQuantityError("Quantity cannot be negative.")
            product.quantity = quantity

        self._save_products()
        return product

    def delete_product(self, product_id):
        """Remove a product from inventory by Product ID."""
        product = self._find_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product ID '{product_id}' not found.")
        self.products.remove(product)
        self._save_products()
        return product

    # ------------------------------------------------------------------
    # Stock Management
    # ------------------------------------------------------------------
    def add_stock(self, product_id, amount):
        """Increase inventory quantity for a product."""
        if amount <= 0:
            raise InvalidQuantityError("Stock to add must be a positive number.")
        product = self._find_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product ID '{product_id}' not found.")
        product.quantity += amount
        self._save_products()
        return product

    def reduce_stock(self, product_id, amount):
        """Reduce inventory quantity for a product (e.g. after a sale)."""
        if amount <= 0:
            raise InvalidQuantityError("Stock to reduce must be a positive number.")
        product = self._find_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product ID '{product_id}' not found.")
        if amount > product.quantity:
            raise InsufficientStockError(
                f"Cannot reduce {amount} units — only {product.quantity} "
                f"in stock for '{product.name}'."
            )
        product.quantity -= amount
        self._save_products()
        return product

    def low_stock_products(self, threshold=LOW_STOCK_THRESHOLD):
        """Return products whose quantity is below the given threshold."""
        return [p for p in self.products if p.quantity < threshold]

    def get_product_or_raise(self, product_id):
        product = self._find_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product ID '{product_id}' not found.")
        return product
