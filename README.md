# Inventory Management System

A console-based **Inventory Management System** built in Python as part of the
Python Development Internship Program. It demonstrates object-oriented
programming, file handling, data persistence, and menu-driven user
interaction through a real-world business application.

## Project Overview

### Objective
Help a small business manage products, track stock levels, record sales,
and generate simple reports — all from a console interface, with data
saved locally so it persists between runs.

### Features
- **Product Management** — add, view, search, update, and delete products
- **Stock Management** — add/reduce stock, and get low-stock alerts (< 10 units)
- **Sales Management** — record sales (auto-updates stock and calculates
  totals), view sales history and summaries
- **Reporting** — inventory report (totals, categories, stock value) and
  sales report (revenue, most sold product)
- **Data Persistence** — all data is stored locally in JSON files and
  survives application restarts
- **Robust Error Handling** — invalid input, duplicate IDs, missing
  products, negative/insufficient stock, and file errors are all handled
  with clear, meaningful messages instead of crashes

## Technologies Used

- **Python 3.x** (standard library only — no installation required)
- `json` — reading/writing persisted data
- `datetime` — timestamping sales transactions
- `os` — file/directory handling

No third-party packages (e.g. `pandas`, `tabulate`) are required to run
the project; all tables are formatted using plain Python for maximum
portability. The code is structured so those libraries could be swapped
in easily if desired.

## Project Structure

```
inventory_system/
├── main.py              # Entry point — menu-driven console interface
├── models.py             # Product class (data structure + serialization)
├── inventory_manager.py  # Product CRUD + stock management (add/reduce/low-stock)
├── sales_manager.py      # Sales recording, revenue & "most sold" calculations
├── reports.py             # Inventory & sales report generation
├── storage.py             # JSON file read/write helper (persistence layer)
├── input_helpers.py       # Safe, validated console input functions
├── display.py              # Console table/menu formatting helpers
├── exceptions.py           # Custom exception classes for clear error handling
├── data/
│   ├── products.json      # Sample product inventory data
│   └── sales.json         # Sample sales transaction history
└── README.md
```

Each module has a single, focused responsibility (separation of concerns),
so the codebase stays easy to navigate and extend — e.g. you could add a
`csv`-based `Storage` class alongside `JSONStorage` without touching any
of the manager or CLI code.

## How to Run

1. **Requirements**: Python 3.7 or later (no external packages needed).

2. **Clone or download** this project folder, then open a terminal inside it:
   ```bash
   cd inventory_system
   ```

3. **Run the application**:
   ```bash
   python3 main.py
   ```
   (On Windows, use `python main.py`.)

4. **Use the menu** — enter the number of the action you want:
   ```
   1. Add Product
   2. View Products
   3. Search Product
   4. Update Product
   5. Delete Product
   6. Add Stock
   7. Reduce Stock
   8. Record Sale
   9. Low Stock Alert
   10. Inventory Report
   11. Sales Report
   12. Exit
   ```

5. **Data persistence** — every change is saved immediately to
   `data/products.json` and `data/sales.json`, so your inventory and
   sales history will still be there the next time you run the program.
   Sample data is already included so you can explore the system
   right away.

## Sample Output

**Main Menu**
```
============================================================
                INVENTORY MANAGEMENT SYSTEM
============================================================
1. Add Product
2. View Products
3. Search Product
4. Update Product
5. Delete Product
6. Add Stock
7. Reduce Stock
8. Record Sale
9. Low Stock Alert
10. Inventory Report
11. Sales Report
12. Exit
------------------------------------------------------------
Enter your choice (1-12):
```

**Viewing Products**
```
============================================================
                        ALL PRODUCTS
============================================================
Product ID  Name                Category       Price     Quantity  Supplier
------------------------------------------------------------------------------
P001        Wireless Mouse      Electronics    19.99     50        TechSource Ltd
P002        Mechanical Keyboard Electronics    49.99     8         TechSource Ltd
P003        Notebook A5         Stationery     2.50      200       PaperWorks Inc
P004        Ballpoint Pen (P... Stationery     3.75      5         PaperWorks Inc
P005        Office Chair        Furniture      89.99     15        ComfortSeating Co
```

**Recording a Sale**
```
============================================================
                        RECORD SALE
============================================================
Enter Product ID: P001
Quantity Sold: 4
[OK] Sale recorded: 4 x Wireless Mouse = $87.96
```

**Sales Report**
```
============================================================
                        SALES REPORT
============================================================
Total Products Sold : 32
Total Revenue        : $297.88
Most Sold Product    : Notebook A5 (20 units)
```

**Error Handling Example**
```
============================================================
                       REDUCE STOCK
============================================================
Enter Product ID: P004
Quantity to reduce: 1000
[ERROR] Cannot reduce 1000 units — only 5 in stock for 'Ballpoint Pen (Pack of 10)'.
```

> Note: Actual screenshots of a terminal session can be added here once
> the project is run locally — capture your terminal window while
> exercising each menu option and save the images under an `assets/`
> folder, then reference them in this README (e.g.
> `![Main Menu](assets/main_menu.png)`).

## Error Handling Summary

| Scenario                  | How it's handled                                      |
|----------------------------|--------------------------------------------------------|
| Invalid menu input         | Re-prompts until a valid option is entered             |
| Non-numeric price/quantity | Re-prompts with a clear message                        |
| Duplicate Product ID       | `DuplicateProductError` raised, add rejected            |
| Product not found          | `ProductNotFoundError` raised, action cancelled         |
| Negative price/quantity    | `InvalidQuantityError` raised, value rejected           |
| Selling/removing more stock than available | `InsufficientStockError` raised, stock unchanged |
| Corrupt or missing data file | Falls back to an empty dataset with a warning, instead of crashing |

## Possible Future Enhancements
- Export reports to CSV/PDF
- Add a `pandas`-powered analytics dashboard
- Multi-user login and role-based permissions
- Switch to a proper database (SQLite) for larger inventories
