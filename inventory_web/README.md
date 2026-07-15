# Inventory Management System — Web Edition

A browser-based version of the console Inventory Management System,
built with **Flask**. All the original business logic
(`InventoryManager`, `SalesManager`, `ReportGenerator`, `Product`) is
reused unchanged — only the interface layer is new, so this is
deployable as a real web service (e.g. on Render).

## Features
- **Dashboard** — inventory totals, sales totals, revenue, best seller, low-stock banner
- **Products** — add, search, edit, delete, and add/reduce stock inline, from a table view
- **Sales** — record a sale (auto-updates stock + calculates total) and view full sales history
- **Reports** — inventory report (products, categories, stock, value) and sales report (units sold, revenue, best seller)
- Same JSON-based persistence (`data/products.json`, `data/sales.json`) and the same error handling (duplicate IDs, not-found, negative/insufficient stock) as the console version — surfaced as on-page flash messages instead of console text

## Project Structure
```
inventory_web/
├── app.py                 # Flask routes (the only new "interface" code)
├── models.py               # Product class (unchanged from console version)
├── inventory_manager.py    # Product CRUD + stock logic (unchanged)
├── sales_manager.py        # Sales recording + summaries (unchanged)
├── reports.py               # Report generation (unchanged)
├── storage.py                # JSON persistence layer (unchanged)
├── exceptions.py             # Custom exceptions (unchanged)
├── templates/                # Jinja2 HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── products.html
│   ├── product_form.html
│   ├── sales.html
│   ├── record_sale.html
│   └── reports.html
├── static/
│   └── style.css            # Design system (stockroom ledger theme)
├── data/
│   ├── products.json
│   └── sales.json
├── requirements.txt
└── README.md
```

## Running Locally

```bash
pip install -r requirements.txt
python3 app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## Deploying on Render

Create a new **Web Service** on Render, point it at this repo, and use:

**Build Command**
```
pip install -r requirements.txt
```

**Start Command**
```
gunicorn app:app
```

Render will detect the port automatically via the `PORT` environment
variable (already handled in `app.py`).

### ⚠️ Important: Render's free-tier filesystem is ephemeral
Render's free web services use an **ephemeral filesystem** — any files
written while the app is running (like updates to `products.json` /
`sales.json`) are **wiped on every deploy and on every restart/spin-down**.
That means:
- The app will run and work correctly in the browser.
- But changes you make (adding products, recording sales) won't
  survive a redeploy or a free-tier restart after inactivity.

This is fine for a demo/internship submission, but for real
persistent data on Render you'd want one of:
1. A **Render Persistent Disk** (paid tier) mounted at the `data/`
   folder, or
2. Swapping `storage.py` for a real database (Render offers free
   PostgreSQL) — the `JSONStorage` class is isolated specifically so
   this kind of swap doesn't require touching the manager classes.

## Environment Variables
- `SECRET_KEY` — used to sign Flask's session/flash cookies. Render
  will let you set this under your service's Environment tab; if
  unset, a development default is used (fine for a demo, not for
  production).

## Notes
This web edition and the original console edition (`main.py`) share
the exact same underlying modules — you can run either interface
against the same `data/` folder.
