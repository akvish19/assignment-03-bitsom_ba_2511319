# part2_order_system.py
# Restaurant Menu & Order Management System — lists, dicts, nested structures

import copy

# ── PROVIDED DATA ─────────────────────────────────────────────────────────

menu = {
    "Paneer Tikka":   {"category": "Starters",  "price": 180.0, "available": True},
    "Chicken Wings":  {"category": "Starters",  "price": 220.0, "available": False},
    "Veg Soup":       {"category": "Starters",  "price": 120.0, "available": True},
    "Butter Chicken": {"category": "Mains",     "price": 320.0, "available": True},
    "Dal Tadka":      {"category": "Mains",     "price": 180.0, "available": True},
    "Veg Biryani":    {"category": "Mains",     "price": 250.0, "available": True},
    "Garlic Naan":    {"category": "Mains",     "price":  40.0, "available": True},
    "Gulab Jamun":    {"category": "Desserts",  "price":  90.0, "available": True},
    "Rasgulla":       {"category": "Desserts",  "price":  80.0, "available": True},
    "Ice Cream":      {"category": "Desserts",  "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka":   {"stock": 10, "reorder_level": 3},
    "Chicken Wings":  {"stock":  8, "reorder_level": 2},
    "Veg Soup":       {"stock": 15, "reorder_level": 5},
    "Butter Chicken": {"stock": 12, "reorder_level": 4},
    "Dal Tadka":      {"stock": 20, "reorder_level": 5},
    "Veg Biryani":    {"stock":  6, "reorder_level": 3},
    "Garlic Naan":    {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":    {"stock":  5, "reorder_level": 2},
    "Rasgulla":       {"stock":  4, "reorder_level": 3},
    "Ice Cream":      {"stock":  7, "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1,  "items": ["Paneer Tikka", "Garlic Naan"],          "total": 220.0},
        {"order_id": 2,  "items": ["Gulab Jamun", "Veg Soup"],              "total": 210.0},
        {"order_id": 3,  "items": ["Butter Chicken", "Garlic Naan"],        "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4,  "items": ["Dal Tadka", "Garlic Naan"],             "total": 220.0},
        {"order_id": 5,  "items": ["Veg Biryani", "Gulab Jamun"],           "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6,  "items": ["Paneer Tikka", "Rasgulla"],             "total": 260.0},
        {"order_id": 7,  "items": ["Butter Chicken", "Veg Biryani"],        "total": 570.0},
        {"order_id": 8,  "items": ["Garlic Naan", "Gulab Jamun"],           "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9,  "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"],          "total": 270.0},
    ],
}

# ─────────────────────────────────────────────
# TASK 1 — Explore the Menu
# ─────────────────────────────────────────────

print("=" * 45)
print("TASK 1 — Full Menu by Category")
print("=" * 45)

# Collect unique categories preserving insertion order
categories = []
for item_data in menu.values():
    if item_data["category"] not in categories:
        categories.append(item_data["category"])

for cat in categories:
    print(f"\n===== {cat} =====")
    for item_name, item_data in menu.items():
        if item_data["category"] == cat:
            availability = "[Available]" if item_data["available"] else "[Unavailable]"
            print(f"  {item_name:<18} ₹{item_data['price']:.2f}   {availability}")

# Stats using dictionary methods
total_items     = len(menu)
available_items = sum(1 for v in menu.values() if v["available"])
most_expensive  = max(menu, key=lambda k: menu[k]["price"])
cheap_items     = {k: v for k, v in menu.items() if v["price"] < 150}

print(f"\nTotal items    : {total_items}")
print(f"Available items: {available_items}")
print(f"Most expensive : {most_expensive} (₹{menu[most_expensive]['price']:.2f})")
print("Items under ₹150:")
for k, v in cheap_items.items():
    print(f"  {k} — ₹{v['price']:.2f}")

# ─────────────────────────────────────────────
# TASK 2 — Cart Operations
# ─────────────────────────────────────────────

print("\n" + "=" * 45)
print("TASK 2 — Cart Operations")
print("=" * 45)

cart = []   # Each entry: {"item": str, "quantity": int, "price": float}

def add_to_cart(item_name, qty):
    """Add item to cart; increase quantity if already present."""
    if item_name not in menu:
        print(f"  ✗ '{item_name}' does not exist in the menu.")
        return
    if not menu[item_name]["available"]:
        print(f"  ✗ '{item_name}' is currently unavailable.")
        return
    # Check if item already in cart
    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] += qty
            print(f"  ↑ Updated quantity: '{item_name}' is now x{entry['quantity']}.")
            return
    # New entry
    cart.append({"item": item_name, "quantity": qty, "price": menu[item_name]["price"]})
    print(f"  ✓ Added '{item_name}' x{qty} to cart.")

def remove_from_cart(item_name):
    """Remove item from cart by name."""
    for i, entry in enumerate(cart):
        if entry["item"] == item_name:
            del cart[i]
            print(f"  ✓ Removed '{item_name}' from cart.")
            return
    print(f"  ✗ '{item_name}' is not in the cart.")

def update_quantity(item_name, new_qty):
    """Update the quantity of an item already in the cart."""
    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] = new_qty
            print(f"  ✓ Quantity of '{item_name}' updated to x{new_qty}.")
            return
    print(f"  ✗ '{item_name}' not found in cart to update.")

def print_cart():
    print(f"  Cart: {cart}")

# Simulate the sequence
print("\nStep 1 — Add Paneer Tikka x2")
add_to_cart("Paneer Tikka", 2); print_cart()

print("\nStep 2 — Add Gulab Jamun x1")
add_to_cart("Gulab Jamun", 1); print_cart()

print("\nStep 3 — Add Paneer Tikka x1 (should update qty to 3)")
add_to_cart("Paneer Tikka", 1); print_cart()

print("\nStep 4 — Try adding Mystery Burger")
add_to_cart("Mystery Burger", 1); print_cart()

print("\nStep 5 — Try adding Chicken Wings (unavailable)")
add_to_cart("Chicken Wings", 1); print_cart()

print("\nStep 6 — Remove Gulab Jamun")
remove_from_cart("Gulab Jamun"); print_cart()

# Final Order Summary
subtotal = sum(e["quantity"] * e["price"] for e in cart)
gst      = round(subtotal * 0.05, 2)
total    = round(subtotal + gst, 2)

print("\n========== Order Summary ==========")
for e in cart:
    line_total = e["quantity"] * e["price"]
    print(f"  {e['item']:<20} x{e['quantity']}    ₹{line_total:.2f}")
print("  " + "-" * 34)
print(f"  Subtotal:               ₹{subtotal:.2f}")
print(f"  GST (5%):               ₹{gst:.2f}")
print(f"  Total Payable:          ₹{total:.2f}")
print("====================================")

# ─────────────────────────────────────────────
# TASK 3 — Inventory Tracker with Deep Copy
# ─────────────────────────────────────────────

print("\n" + "=" * 45)
print("TASK 3 — Inventory Tracker with Deep Copy")
print("=" * 45)

# Deep copy before any changes
inventory_backup = copy.deepcopy(inventory)

# Demonstrate deep copy works: change a value, show backup unaffected
inventory["Garlic Naan"]["stock"] = 999
print("\n[Demo] inventory['Garlic Naan']['stock'] changed to 999")
print(f"  inventory['Garlic Naan']['stock']        = {inventory['Garlic Naan']['stock']}")
print(f"  inventory_backup['Garlic Naan']['stock'] = {inventory_backup['Garlic Naan']['stock']}  ← backup unaffected ✓")

# Restore original before continuing
inventory["Garlic Naan"]["stock"] = 30

# Deduct quantities from final cart (Paneer Tikka x3)
print("\nDeducting cart items from inventory:")
for entry in cart:
    item    = entry["item"]
    qty_req = entry["quantity"]
    current = inventory[item]["stock"]
    if current < qty_req:
        print(f"  ⚠ Insufficient stock for {item}: need {qty_req}, have {current}. Deducting {current}.")
        inventory[item]["stock"] = 0
    else:
        inventory[item]["stock"] -= qty_req
        print(f"  ✓ Deducted {qty_req} from {item}. Remaining: {inventory[item]['stock']}")

# Reorder alerts
print("\nReorder Alerts:")
for item, data in inventory.items():
    if data["stock"] <= data["reorder_level"]:
        print(f"  ⚠ Reorder Alert: {item} — Only {data['stock']} unit(s) left (reorder level: {data['reorder_level']})")

# Confirm inventory vs backup differ
print(f"\ninventory['Paneer Tikka']['stock']        = {inventory['Paneer Tikka']['stock']}")
print(f"inventory_backup['Paneer Tikka']['stock'] = {inventory_backup['Paneer Tikka']['stock']}  ← deep copy confirmed ✓")

# ─────────────────────────────────────────────
# TASK 4 — Daily Sales Log Analysis
# ─────────────────────────────────────────────

print("\n" + "=" * 45)
print("TASK 4 — Sales Log Analysis (original data)")
print("=" * 45)

def revenue_per_day(log):
    return {date: round(sum(o["total"] for o in orders), 2) for date, orders in log.items()}

def best_selling_day(rev_dict):
    return max(rev_dict, key=rev_dict.get)

def most_ordered_item(log):
    item_count = {}
    for orders in log.values():
        for order in orders:
            for item in order["items"]:
                item_count[item] = item_count.get(item, 0) + 1
    return max(item_count, key=item_count.get), max(item_count.values())

rev = revenue_per_day(sales_log)
print("\nRevenue per day:")
for date, amount in rev.items():
    print(f"  {date} : ₹{amount:.2f}")

best_day = best_selling_day(rev)
print(f"\nBest-selling day : {best_day} (₹{rev[best_day]:.2f})")

top_item, top_count = most_ordered_item(sales_log)
print(f"Most ordered item: {top_item} (appeared in {top_count} orders)")

# Add new day
sales_log["2025-01-05"] = [
    {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
    {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"],                     "total": 260.0},
]

print("\n--- Updated stats after adding 2025-01-05 ---")
rev = revenue_per_day(sales_log)
print("Revenue per day:")
for date, amount in rev.items():
    print(f"  {date} : ₹{amount:.2f}")
best_day = best_selling_day(rev)
print(f"Best-selling day : {best_day} (₹{rev[best_day]:.2f})")

# Numbered list of all orders across all dates using enumerate
print("\nAll orders (numbered):")
counter = 1
for date, orders in sales_log.items():
    for order in orders:
        items_str = ", ".join(order["items"])
        print(f"  {counter}. [{date}] Order #{order['order_id']}  — ₹{order['total']:.2f} — Items: {items_str}")
        counter += 1
