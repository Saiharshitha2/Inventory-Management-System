"""
display.py
----------
Small helper functions for printing nicely formatted output to the
console (tables, headers, messages). Kept separate from business
logic so the menu code and manager classes stay clean.

Uses only the standard library (no external dependency required),
but the table layout is similar to what `tabulate` would produce.
"""

HEADERS = ["Product ID", "Name", "Category", "Price", "Quantity", "Supplier"]
COL_WIDTHS = [12, 20, 15, 10, 10, 15]


def print_header(title):
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)


def print_success(message):
    print(f"[OK] {message}")


def print_error(message):
    print(f"[ERROR] {message}")


def print_info(message):
    print(f"[INFO] {message}")


def print_product_table(products):
    """Print a list of Product objects as a formatted table."""
    if not products:
        print_info("No products to display.")
        return

    row_format = "".join(f"{{:<{w}}}" for w in COL_WIDTHS)
    print(row_format.format(*HEADERS))
    print("-" * sum(COL_WIDTHS))
    for p in products:
        print(row_format.format(*[str(v) for v in p.as_row()]))


def print_sales_table(sales):
    """Print a list of sale dict records as a formatted table."""
    if not sales:
        print_info("No sales recorded yet.")
        return

    headers = ["Date/Time", "Product ID", "Product Name", "Qty", "Unit Price", "Total"]
    widths = [20, 12, 20, 6, 12, 10]
    row_format = "".join(f"{{:<{w}}}" for w in widths)
    print(row_format.format(*headers))
    print("-" * sum(widths))
    for s in sales:
        print(row_format.format(
            s["timestamp"], s["product_id"], s["product_name"],
            s["quantity_sold"], f"{s['unit_price']:.2f}", f"{s['total_amount']:.2f}"
        ))


def print_menu():
    print_header("INVENTORY MANAGEMENT SYSTEM")
    menu_items = [
        "1. Add Product",
        "2. View Products",
        "3. Search Product",
        "4. Update Product",
        "5. Delete Product",
        "6. Add Stock",
        "7. Reduce Stock",
        "8. Record Sale",
        "9. Low Stock Alert",
        "10. Inventory Report",
        "11. Sales Report",
        "12. Exit",
    ]
    for item in menu_items:
        print(item)
    print("-" * 60)
