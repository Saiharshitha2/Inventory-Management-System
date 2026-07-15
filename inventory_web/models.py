"""
models.py
---------
Defines the Product data structure used throughout the Inventory
Management System.

A Product is a simple data class (OOP) that represents one row of
inventory. It knows how to convert itself to/from a dictionary so it
can be easily serialized to JSON.
"""


class Product:
    """Represents a single product in the inventory."""

    def __init__(self, product_id, name, category, price, quantity, supplier):
        self.product_id = str(product_id).strip()
        self.name = str(name).strip()
        self.category = str(category).strip()
        self.price = float(price)
        self.quantity = int(quantity)
        self.supplier = str(supplier).strip()

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self):
        """Convert the Product object into a plain dictionary (for JSON)."""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "supplier": self.supplier,
        }

    @staticmethod
    def from_dict(data):
        """Create a Product object from a dictionary (loaded from JSON)."""
        return Product(
            product_id=data["product_id"],
            name=data["name"],
            category=data["category"],
            price=data["price"],
            quantity=data["quantity"],
            supplier=data["supplier"],
        )

    def total_value(self):
        """Return the total stock value (price * quantity) for this product."""
        return round(self.price * self.quantity, 2)

    def as_row(self):
        """Return a list of values suitable for printing in a table row."""
        return [
            self.product_id,
            self.name,
            self.category,
            f"{self.price:.2f}",
            self.quantity,
            self.supplier,
        ]

    def __repr__(self):
        return f"Product({self.product_id}, {self.name}, qty={self.quantity})"
