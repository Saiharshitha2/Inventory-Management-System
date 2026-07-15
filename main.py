"""
main.py
-------
Entry point for the Inventory Management System.

This file wires together the InventoryManager, SalesManager and
ReportGenerator classes, and presents a menu-driven console
interface to the user. Run this file to start the application:

    python main.py
"""

from inventory_manager import InventoryManager, LOW_STOCK_THRESHOLD
from sales_manager import SalesManager
from reports import ReportGenerator
from display import (
    print_header, print_success, print_error, print_info,
    print_product_table, print_sales_table, print_menu,
)
from input_helpers import (
    read_non_empty_string, read_optional_string,
    read_float, read_int, read_menu_choice,
)
from exceptions import InventoryError

PRODUCTS_FILE = "data/products.json"
SALES_FILE = "data/sales.json"


# --------------------------------------------------------------------
# Menu action handlers
# --------------------------------------------------------------------
def handle_add_product(inventory):
    print_header("ADD NEW PRODUCT")
    try:
        product_id = read_non_empty_string("Product ID: ")
        name = read_non_empty_string("Product Name: ")
        category = read_non_empty_string("Category: ")
        price = read_float("Price: ")
        quantity = read_int("Quantity Available: ")
        supplier = read_non_empty_string("Supplier Name: ")

        product = inventory.add_product(
            product_id, name, category, price, quantity, supplier)
        print_success(f"Product '{product.name}' added successfully.")
    except InventoryError as e:
        print_error(str(e))


def handle_view_products(inventory):
    print_header("ALL PRODUCTS")
    print_product_table(inventory.view_products())


def handle_search_product(inventory):
    print_header("SEARCH PRODUCT")
    keyword = read_non_empty_string("Enter Product ID or Product Name: ")
    try:
        results = inventory.search_product(keyword)
        print_product_table(results)
    except InventoryError as e:
        print_error(str(e))


def handle_update_product(inventory):
    print_header("UPDATE PRODUCT")
    product_id = read_non_empty_string("Enter Product ID to update: ")
    try:
        product = inventory.get_product_or_raise(product_id)
        print_info(f"Current details: {product.as_row()}")
        print_info("Leave a field blank to keep its current value.")

        name = read_optional_string("New Name: ")
        category = read_optional_string("New Category: ")
        price = read_float("New Price: ", allow_blank=True)
        quantity = read_int("New Quantity: ", allow_blank=True)

        updated = inventory.update_product(
            product_id,
            name=name if name else None,
            category=category if category else None,
            price=price,
            quantity=quantity,
        )
        print_success(f"Product '{updated.product_id}' updated successfully.")
    except InventoryError as e:
        print_error(str(e))


def handle_delete_product(inventory):
    print_header("DELETE PRODUCT")
    product_id = read_non_empty_string("Enter Product ID to delete: ")
    try:
        product = inventory.delete_product(product_id)
        print_success(f"Product '{product.name}' (ID: {product.product_id}) deleted.")
    except InventoryError as e:
        print_error(str(e))


def handle_add_stock(inventory):
    print_header("ADD STOCK")
    product_id = read_non_empty_string("Enter Product ID: ")
    amount = read_int("Quantity to add: ")
    try:
        product = inventory.add_stock(product_id, amount)
        print_success(f"Stock updated. '{product.name}' now has {product.quantity} units.")
    except InventoryError as e:
        print_error(str(e))


def handle_reduce_stock(inventory):
    print_header("REDUCE STOCK")
    product_id = read_non_empty_string("Enter Product ID: ")
    amount = read_int("Quantity to reduce: ")
    try:
        product = inventory.reduce_stock(product_id, amount)
        print_success(f"Stock updated. '{product.name}' now has {product.quantity} units.")
    except InventoryError as e:
        print_error(str(e))


def handle_record_sale(inventory, sales):
    print_header("RECORD SALE")
    product_id = read_non_empty_string("Enter Product ID: ")
    quantity = read_int("Quantity Sold: ")
    try:
        sale = sales.record_sale(product_id, quantity)
        print_success(
            f"Sale recorded: {sale['quantity_sold']} x {sale['product_name']} "
            f"= ${sale['total_amount']:.2f}"
        )
    except InventoryError as e:
        print_error(str(e))


def handle_low_stock_alert(inventory):
    print_header(f"LOW STOCK ALERT (threshold: {LOW_STOCK_THRESHOLD} units)")
    low_stock = inventory.low_stock_products()
    if not low_stock:
        print_info("All products are sufficiently stocked.")
    else:
        print_product_table(low_stock)


def handle_inventory_report(reports):
    print_header("INVENTORY REPORT")
    data = reports.inventory_report()
    print(f"Total Products      : {data['total_products']}")
    print(f"Total Categories    : {data['total_categories']}")
    print(f"Total Available Stock: {data['total_available_stock']}")
    print(f"Total Stock Value   : ${data['total_stock_value']:.2f}")


def handle_sales_report(reports, sales):
    print_header("SALES REPORT")
    data = reports.sales_report()
    print(f"Total Products Sold : {data['total_products_sold']}")
    print(f"Total Revenue       : ${data['total_revenue']:.2f}")
    if data["most_sold_product"]:
        name, qty = data["most_sold_product"]
        print(f"Most Sold Product   : {name} ({qty} units)")
    else:
        print("Most Sold Product   : N/A (no sales yet)")

    print()
    print_info("Sales history:")
    print_sales_table(sales.all_sales())


# --------------------------------------------------------------------
# Main loop
# --------------------------------------------------------------------
def main():
    inventory = InventoryManager(PRODUCTS_FILE)
    sales = SalesManager(inventory, SALES_FILE)
    reports = ReportGenerator(inventory, sales)

    valid_choices = [str(i) for i in range(1, 13)]

    print_info("Welcome to the Inventory Management System!")

    while True:
        print_menu()
        choice = read_menu_choice("Enter your choice (1-12): ", valid_choices)

        if choice == "1":
            handle_add_product(inventory)
        elif choice == "2":
            handle_view_products(inventory)
        elif choice == "3":
            handle_search_product(inventory)
        elif choice == "4":
            handle_update_product(inventory)
        elif choice == "5":
            handle_delete_product(inventory)
        elif choice == "6":
            handle_add_stock(inventory)
        elif choice == "7":
            handle_reduce_stock(inventory)
        elif choice == "8":
            handle_record_sale(inventory, sales)
        elif choice == "9":
            handle_low_stock_alert(inventory)
        elif choice == "10":
            handle_inventory_report(reports)
        elif choice == "11":
            handle_sales_report(reports, sales)
        elif choice == "12":
            print_info("Thank you for using the Inventory Management System. Goodbye!")
            break

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Program interrupted by user. Exiting safely.")
    except Exception as e:
        # Catch-all safety net so unexpected errors don't crash with a
        # raw traceback in front of the end user.
        print_error(f"An unexpected error occurred: {e}")
