"""
reports.py
----------
Contains the ReportGenerator class, responsible for the Reporting
Module:

    - Inventory Report: total products, total categories, available stock
    - Sales Report: total sales, revenue generated, most sold product
"""


class ReportGenerator:
    def __init__(self, inventory_manager, sales_manager):
        self.inventory_manager = inventory_manager
        self.sales_manager = sales_manager

    def inventory_report(self):
        products = self.inventory_manager.view_products()
        total_products = len(products)
        total_categories = len({p.category.lower() for p in products})
        total_available_stock = sum(p.quantity for p in products)
        total_stock_value = round(sum(p.total_value() for p in products), 2)

        return {
            "total_products": total_products,
            "total_categories": total_categories,
            "total_available_stock": total_available_stock,
            "total_stock_value": total_stock_value,
        }

    def sales_report(self):
        total_sold = self.sales_manager.total_products_sold()
        revenue = self.sales_manager.total_revenue()
        top_seller = self.sales_manager.most_sold_product()

        return {
            "total_products_sold": total_sold,
            "total_revenue": revenue,
            "most_sold_product": top_seller,  # (name, qty) or None
        }
