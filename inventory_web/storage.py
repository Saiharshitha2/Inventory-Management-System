"""
storage.py
----------
Handles all file I/O for the Inventory Management System.

Data is persisted locally using JSON files:
    data/products.json
    data/sales.json

Keeping file-handling logic in one place makes it easy to swap the
storage backend later (e.g. to CSV or a database) without touching
the business logic in the manager classes.
"""

import json
import os


class JSONStorage:
    """A small helper class for reading/writing JSON data files safely."""

    def __init__(self, filepath):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        """Create the data directory/file with an empty list if missing."""
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.filepath):
            self.write([])

    def read(self):
        """Read and return the JSON data (a list of dicts). Handles errors."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except FileNotFoundError:
            # File missing -> treat as empty dataset instead of crashing
            return []
        except json.JSONDecodeError:
            print(f"[Warning] '{self.filepath}' contains invalid JSON. "
                  f"Starting with an empty dataset instead.")
            return []
        except OSError as e:
            print(f"[Error] Could not read file '{self.filepath}': {e}")
            return []

    def write(self, data):
        """Write the given data (list of dicts) to the JSON file."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True
        except OSError as e:
            print(f"[Error] Could not write to file '{self.filepath}': {e}")
            return False
