import sys
import os
import csv

# Add the parent directory to the path so we can import core and config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.db import get_supabase_client

def load_csv(filepath):
    """Helper to read CSV into a list of dictionaries."""
    data = []
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found.")
        return data
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def seed_database():
    client = get_supabase_client()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")

    print("Seeding Inventory...")
    inventory_data = load_csv(os.path.join(data_dir, "inventory.csv"))
    for item in inventory_data:
        # Convert numeric fields
        item['quantity'] = int(item['quantity'])
        try:
            client.post("inventory", item)
        except Exception as e:
            print(f"Failed to insert {item}: {e}")

    print("Seeding Sales...")
    sales_data = load_csv(os.path.join(data_dir, "sales.csv"))
    for item in sales_data:
        # Convert numeric fields
        item['volume'] = float(item['volume'])
        try:
            client.post("sales", item)
        except Exception as e:
            print(f"Failed to insert {item}: {e}")

    print("Seeding Orders...")
    orders_data = load_csv(os.path.join(data_dir, "orders.csv"))
    for item in orders_data:
        # Convert numeric fields
        item['days_delayed'] = int(item['days_delayed'])
        try:
            client.post("orders", item)
        except Exception as e:
            print(f"Failed to insert {item}: {e}")

    print("Seeding Products...")
    products_data = load_csv(os.path.join(data_dir, "products.csv"))
    for item in products_data:
        # Convert numeric fields
        item['margin_percentage'] = float(item['margin_percentage'])
        try:
            client.post("products", item)
        except Exception as e:
            print(f"Failed to insert {item}: {e}")
            
    print("Seeding Complete!")

if __name__ == "__main__":
    seed_database()
