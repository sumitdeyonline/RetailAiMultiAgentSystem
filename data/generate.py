import csv
import random

# 1. Products (50 records)
categories = ['Footwear', 'Apparel', 'Accessories', 'Electronics', 'Home']
products = []
for i in range(1, 51):
    products.append({
        'sku': f"SKU-{1000+i}",
        'category': random.choice(categories),
        'margin_percentage': round(random.uniform(10.0, 65.0), 2)
    })

with open('data/products.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['sku', 'category', 'margin_percentage'])
    writer.writeheader()
    writer.writerows(products)

# 2. Inventory (50 records)
locations = ['CA-STORE-1', 'NY-STORE-1', 'TX-STORE-1', 'FL-STORE-1', 'WA-STORE-1']
inventory = []
seen = set()
while len(inventory) < 50:
    sku = random.choice(products)['sku']
    loc = random.choice(locations)
    key = (sku, loc)
    if key not in seen:
        seen.add(key)
        inventory.append({
            'sku': sku,
            'location_id': loc,
            'quantity': random.randint(0, 500)
        })

with open('data/inventory.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['sku', 'location_id', 'quantity'])
    writer.writeheader()
    writer.writerows(inventory)

# 3. Sales (50 records)
regions = ['California', 'New York', 'Texas', 'Florida', 'Washington', 'Illinois', 'Nevada', 'Ohio', 'Georgia', 'Arizona']
timeframes = ['Q1', 'Q2', 'Q3', 'Q4', 'last week', 'yesterday', 'last month', 'this month', 'YTD']
sales = []
seen_sales = set()
while len(sales) < 50:
    reg = random.choice(regions)
    tf = random.choice(timeframes)
    key = (reg, tf)
    if key not in seen_sales:
        seen_sales.add(key)
        sales.append({
            'region': reg,
            'timeframe': tf,
            'volume': round(random.uniform(1000.0, 5000000.0), 2)
        })
        
with open('data/sales.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['region', 'timeframe', 'volume'])
    writer.writeheader()
    writer.writerows(sales)

# 4. Orders (50 records)
statuses = ['IN_TRANSIT', 'DELAYED', 'DELIVERED', 'PROCESSING', 'CANCELLED']
orders = []
for i in range(1, 51):
    status = random.choice(statuses)
    days_delayed = random.randint(1, 14) if status == 'DELAYED' else 0
    orders.append({
        'order_id': f"ORD-{2000+i}",
        'status': status,
        'days_delayed': days_delayed
    })

with open('data/orders.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['order_id', 'status', 'days_delayed'])
    writer.writeheader()
    writer.writerows(orders)
    
print("Successfully generated 50 records for products, inventory, sales, and orders!")
