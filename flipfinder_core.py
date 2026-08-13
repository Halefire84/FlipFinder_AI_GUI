import json
import os

DATA_FILE = "inventory.json"

def load_inventory():
    """Loads saved inventory items from disk."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_inventory(items):
    """Saves the inventory list to disk."""
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=4)
