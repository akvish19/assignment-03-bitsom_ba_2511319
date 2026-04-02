# part3_api_files.py
# Product Explorer & Error-Resilient Logger
# Uses: File I/O, requests, exception handling, datetime logging

import requests
from datetime import datetime

LOG_FILE   = "error_log.txt"
NOTES_FILE = "python_notes.txt"

# ─────────────────────────────────────────────
# HELPER — Error Logger
# ─────────────────────────────────────────────

def log_error(context, error_type, message):
    """Append a timestamped error entry to error_log.txt."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ERROR in {context}: {error_type} — {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"  [Logged] {entry.strip()}")

# ─────────────────────────────────────────────
# TASK 1 — File Read & Write Basics
# ─────────────────────────────────────────────

print("=" * 50)
print("TASK 1 — File Read & Write")
print("=" * 50)

# Part A — Write
lines = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes.",
]

with open(NOTES_FILE, "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")
print("File written successfully.")

# Append two extra lines
extra_lines = [
    "Topic 6: Functions promote code reuse and readability.",
    "Topic 7: Modules and packages help organise larger projects.",
]
with open(NOTES_FILE, "a", encoding="utf-8") as f:
    for line in extra_lines:
        f.write(line + "\n")
print("Lines appended.")

# Part B — Read
print("\nReading file:")
all_lines = []
with open(NOTES_FILE, "r", encoding="utf-8") as f:
    all_lines = f.readlines()

for i, line in enumerate(all_lines, start=1):
    print(f"  {i}. {line.rstrip()}")

print(f"\nTotal lines: {len(all_lines)}")

# Keyword search
keyword = input("\nEnter a keyword to search: ").strip().lower()
matches = [line.rstrip() for line in all_lines if keyword in line.lower()]
if matches:
    print(f"Lines containing '{keyword}':")
    for m in matches:
        print(f"  → {m}")
else:
    print(f"No lines found containing '{keyword}'.")

# ─────────────────────────────────────────────
# TASK 2 — API Integration
# ─────────────────────────────────────────────

print("\n" + "=" * 50)
print("TASK 2 — API Integration")
print("=" * 50)

BASE_URL = "https://dummyjson.com/products"

# Step 1 — Fetch 20 products
def fetch_products():
    try:
        response = requests.get(f"{BASE_URL}?limit=20", timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("products", [])
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("fetch_products", "ConnectionError", "Could not connect to dummyjson.com")
        return []
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("fetch_products", "Timeout", "Request timed out after 5s")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("fetch_products", "Exception", str(e))
        return []

products = fetch_products()

if products:
    print(f"\n{'ID':<4} | {'Title':<30} | {'Category':<14} | {'Price':>8} | {'Rating':>6}")
    print("-" * 70)
    for p in products:
        print(f"{p['id']:<4} | {p['title'][:29]:<30} | {p['category'][:13]:<14} | ${p['price']:>7.2f} | {p['rating']:>6.2f}")

    # Step 2 — Filter rating >= 4.5, sort by price descending
    filtered = sorted([p for p in products if p["rating"] >= 4.5],
                      key=lambda x: x["price"], reverse=True)
    print(f"\nFiltered (rating ≥ 4.5), sorted by price desc:")
    for p in filtered:
        print(f"  {p['title']} — ${p['price']:.2f} (rating: {p['rating']})")

# Step 3 — Search by category: laptops
def fetch_category(category):
    try:
        response = requests.get(f"{BASE_URL}/category/{category}", timeout=5)
        response.raise_for_status()
        return response.json().get("products", [])
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("fetch_category", "ConnectionError", f"Could not fetch category '{category}'")
        return []
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("fetch_category", "Timeout", "Timeout fetching category")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("fetch_category", "Exception", str(e))
        return []

laptops = fetch_category("laptops")
print("\nLaptops:")
for p in laptops:
    print(f"  {p['title']} — ${p['price']:.2f}")

# Step 4 — POST request (simulated)
def post_product():
    payload = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API",
    }
    try:
        response = requests.post(f"{BASE_URL}/add", json=payload, timeout=5)
        print("\nPOST response:")
        print(response.json())
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("post_product", "ConnectionError", "Could not POST to dummyjson.com")
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("post_product", "Timeout", "POST request timed out")
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("post_product", "Exception", str(e))

post_product()

# ─────────────────────────────────────────────
# TASK 3 — Exception Handling
# ─────────────────────────────────────────────

print("\n" + "=" * 50)
print("TASK 3 — Exception Handling")
print("=" * 50)

# Part A — Guarded Calculator
def safe_divide(a, b):
    """Divide a by b with exception handling."""
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print("\nsafe_divide(10, 2)    →", safe_divide(10, 2))
print("safe_divide(10, 0)    →", safe_divide(10, 0))
print("safe_divide('ten', 2) →", safe_divide("ten", 2))

# Part B — Guarded File Reader
def read_file_safe(filename):
    """Try to read a file; handle missing file gracefully."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    finally:
        print("File operation attempt complete.")

print("\nReading python_notes.txt:")
content = read_file_safe(NOTES_FILE)
if content:
    print(content[:100], "...")

print("\nReading ghost_file.txt:")
read_file_safe("ghost_file.txt")

# Part C — Robust API calls already wrapped in Tasks 2 (see fetch_products, fetch_category, post_product)
print("\n(Part C) Robust API calls are implemented in the fetch_products,"
      "\nfetch_category, and post_product functions above.")

# Part D — Input Validation Loop
print("\nPart D — Product ID Lookup")
while True:
    user_input = input("Enter a product ID to look up (1–100), or 'quit' to exit: ").strip()
    if user_input.lower() == "quit":
        print("Exiting lookup.")
        break
    try:
        product_id = int(user_input)
        if not (1 <= product_id <= 100):
            print("  ⚠ Warning: Please enter a number between 1 and 100.")
            continue
    except ValueError:
        print("  ⚠ Warning: That is not a valid integer. Try again.")
        continue

    # Valid ID — make API call
    try:
        resp = requests.get(f"{BASE_URL}/{product_id}", timeout=5)
        if resp.status_code == 404:
            print("  Product not found.")
            log_error("lookup_product", "HTTPError", f"404 Not Found for product ID {product_id}")
        elif resp.status_code == 200:
            p = resp.json()
            print(f"  Title: {p['title']}  |  Price: ${p['price']:.2f}")
        else:
            print(f"  Unexpected status code: {resp.status_code}")
    except requests.exceptions.ConnectionError:
        print("  Connection failed. Please check your internet.")
        log_error("lookup_product", "ConnectionError", f"Could not reach server for ID {product_id}")
    except requests.exceptions.Timeout:
        print("  Request timed out. Try again later.")
        log_error("lookup_product", "Timeout", f"Timeout for product ID {product_id}")
    except Exception as e:
        print(f"  Unexpected error: {e}")
        log_error("lookup_product", "Exception", str(e))

# ─────────────────────────────────────────────
# TASK 4 — Logging to File
# ─────────────────────────────────────────────

print("\n" + "=" * 50)
print("TASK 4 — Logging to File (intentional triggers)")
print("=" * 50)

# Trigger 1 — ConnectionError via unreachable URL
print("\nTrigger 1: ConnectionError from unreachable URL")
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except requests.exceptions.ConnectionError as e:
    print("  Connection failed. Please check your internet.")
    log_error("fetch_products", "ConnectionError", "No connection could be made")
except requests.exceptions.Timeout:
    print("  Request timed out.")
    log_error("fetch_products", "Timeout", "Request timed out")
except Exception as e:
    log_error("fetch_products", "Exception", str(e))

# Trigger 2 — HTTP 404 for product ID 999
print("\nTrigger 2: HTTP 404 for product ID 999")
try:
    resp = requests.get(f"{BASE_URL}/999", timeout=5)
    if resp.status_code != 200:
        log_error("lookup_product", "HTTPError", f"404 Not Found for product ID 999")
        print("  Product not found (logged).")
    else:
        p = resp.json()
        print(f"  Found: {p['title']}")
except requests.exceptions.ConnectionError:
    print("  Connection failed.")
    log_error("lookup_product", "ConnectionError", "Could not reach server for ID 999")
except Exception as e:
    log_error("lookup_product", "Exception", str(e))

# Print full error_log.txt
print("\n--- Contents of error_log.txt ---")
try:
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("  error_log.txt not found (no errors were logged this run).")
