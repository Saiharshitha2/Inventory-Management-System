"""
app.py
------
Flask web interface for the Inventory Management System.

This reuses the exact same business-logic classes as the console
version (InventoryManager, SalesManager, ReportGenerator) — only the
interface layer changes, from console menus to HTTP routes + HTML
pages. Data is still persisted locally as JSON (data/products.json,
data/sales.json), so it works the same on Render's free tier as it
did locally (note: Render's free filesystem is ephemeral across
deploys/restarts — see README for details).
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash

from inventory_manager import InventoryManager, LOW_STOCK_THRESHOLD
from sales_manager import SalesManager
from reports import ReportGenerator
from exceptions import InventoryError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, "data", "products.json")
SALES_FILE = os.path.join(BASE_DIR, "data", "sales.json")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-change-in-production")

inventory = InventoryManager(PRODUCTS_FILE)
sales = SalesManager(inventory, SALES_FILE)
reports = ReportGenerator(inventory, sales)


# ----------------------------------------------------------------------
# Dashboard
# ----------------------------------------------------------------------
@app.route("/")
def dashboard():
    inv_report = reports.inventory_report()
    sales_report = reports.sales_report()
    low_stock = inventory.low_stock_products()
    return render_template(
        "dashboard.html",
        inv_report=inv_report,
        sales_report=sales_report,
        low_stock=low_stock,
        threshold=LOW_STOCK_THRESHOLD,
    )


# ----------------------------------------------------------------------
# Products
# ----------------------------------------------------------------------
@app.route("/products")
def products_list():
    query = request.args.get("q", "").strip()
    if query:
        try:
            products = inventory.search_product(query)
        except InventoryError as e:
            flash(str(e), "error")
            products = []
    else:
        products = inventory.view_products()
    return render_template("products.html", products=products, query=query,
                            threshold=LOW_STOCK_THRESHOLD)


@app.route("/products/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        try:
            product_id = request.form["product_id"].strip()
            name = request.form["name"].strip()
            category = request.form["category"].strip()
            price = float(request.form["price"])
            quantity = int(request.form["quantity"])
            supplier = request.form["supplier"].strip()

            if not product_id or not name or not category or not supplier:
                raise InventoryError("All fields are required.")

            inventory.add_product(product_id, name, category, price, quantity, supplier)
            flash(f"Product '{name}' added successfully.", "success")
            return redirect(url_for("products_list"))
        except (ValueError, KeyError):
            flash("Please enter a valid price and quantity.", "error")
        except InventoryError as e:
            flash(str(e), "error")
    return render_template("product_form.html", mode="add", product=None)


@app.route("/products/<product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    try:
        product = inventory.get_product_or_raise(product_id)
    except InventoryError as e:
        flash(str(e), "error")
        return redirect(url_for("products_list"))

    if request.method == "POST":
        try:
            name = request.form["name"].strip()
            category = request.form["category"].strip()
            price = float(request.form["price"])
            quantity = int(request.form["quantity"])

            inventory.update_product(
                product_id, name=name, category=category,
                price=price, quantity=quantity,
            )
            flash(f"Product '{product_id}' updated successfully.", "success")
            return redirect(url_for("products_list"))
        except (ValueError, KeyError):
            flash("Please enter a valid price and quantity.", "error")
        except InventoryError as e:
            flash(str(e), "error")

    return render_template("product_form.html", mode="edit", product=product)


@app.route("/products/<product_id>/delete", methods=["POST"])
def delete_product(product_id):
    try:
        product = inventory.delete_product(product_id)
        flash(f"Product '{product.name}' (ID: {product_id}) deleted.", "success")
    except InventoryError as e:
        flash(str(e), "error")
    return redirect(url_for("products_list"))


@app.route("/products/<product_id>/stock", methods=["POST"])
def adjust_stock(product_id):
    action = request.form.get("action")
    try:
        amount = int(request.form["amount"])
        if action == "add":
            product = inventory.add_stock(product_id, amount)
            flash(f"Added {amount} units to '{product.name}'. New quantity: {product.quantity}.", "success")
        elif action == "reduce":
            product = inventory.reduce_stock(product_id, amount)
            flash(f"Reduced {amount} units from '{product.name}'. New quantity: {product.quantity}.", "success")
        else:
            flash("Unknown stock action.", "error")
    except (ValueError, KeyError):
        flash("Please enter a valid whole number for quantity.", "error")
    except InventoryError as e:
        flash(str(e), "error")
    return redirect(url_for("products_list"))


# ----------------------------------------------------------------------
# Sales
# ----------------------------------------------------------------------
@app.route("/sales")
def sales_list():
    return render_template("sales.html", sales=list(reversed(sales.all_sales())))


@app.route("/sales/record", methods=["GET", "POST"])
def record_sale():
    if request.method == "POST":
        try:
            product_id = request.form["product_id"].strip()
            quantity = int(request.form["quantity"])
            sale = sales.record_sale(product_id, quantity)
            flash(
                f"Sale recorded: {sale['quantity_sold']} x {sale['product_name']} "
                f"= ${sale['total_amount']:.2f}",
                "success",
            )
            return redirect(url_for("sales_list"))
        except (ValueError, KeyError):
            flash("Please enter a valid Product ID and quantity.", "error")
        except InventoryError as e:
            flash(str(e), "error")
    return render_template("record_sale.html", products=inventory.view_products())


# ----------------------------------------------------------------------
# Reports
# ----------------------------------------------------------------------
@app.route("/reports")
def reports_page():
    inv_report = reports.inventory_report()
    sale_report = reports.sales_report()
    return render_template("reports.html", inv_report=inv_report, sale_report=sale_report)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
