"""
exceptions.py
-------------
Custom exception classes used across the Inventory Management System.
Using specific exception types (instead of generic ones) makes error
handling clearer and messages more meaningful.
"""


class InventoryError(Exception):
    """Base class for all inventory-related errors."""
    pass


class DuplicateProductError(InventoryError):
    """Raised when trying to add a product with an ID that already exists."""
    pass


class ProductNotFoundError(InventoryError):
    """Raised when a requested product ID/name cannot be found."""
    pass


class InvalidQuantityError(InventoryError):
    """Raised when a quantity is negative, zero (where invalid), or non-numeric."""
    pass


class InsufficientStockError(InventoryError):
    """Raised when trying to sell/reduce more stock than is available."""
    pass


class InvalidInputError(InventoryError):
    """Raised for generic invalid/malformed user input."""
    pass
