import json
import os
from datetime import datetime

INVENTORY_FILE = '../files/iris-inventory.json'

def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_inventory(inventory):
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(inventory, f, indent=2)

def find_item(inventory, code):
    for item in inventory:
        if item.get('code') == code:
            return item
    return None

def print_inventory(inventory):
    print("\n--- Current Inventory ---")
    if not inventory:
        print("  (empty)")
    for item in inventory:
        print(f"  [{item.get('code', 'N/A')}] {item['name']} — count: {item.get('count', 0)}")
    print("-------------------------\n")

def main():
    inventory = load_inventory()
    mode = 'add'  # Default mode: 'add' or 'sell'

    print("=== MDIS Iris Inventory Scanner ===")
    print("Commands:")
    print("  Scan or type a barcode code (e.g. IRIS001) to add/sell 1")
    print("  Type '-CODE' (e.g. -IRIS001) to always subtract 1 regardless of mode")
    print("  Type 'mode add'  — switch to ADD mode (scans increase count)")
    print("  Type 'mode sell' — switch to SELL mode (scans decrease count)")
    print("  Type 'list' to show inventory")
    print("  Type 'quit' to exit and save\n")
    print(f"  Current mode: {mode.upper()}\n")

    while True:
        user_input = input(f"[{mode.upper()}] Scan barcode or enter command: ").strip()

        if not user_input:
            continue

        if user_input.lower() == 'quit':
            save_inventory(inventory)
            print("Inventory saved. Goodbye!")
            break

        if user_input.lower() == 'list':
            print_inventory(inventory)
            continue

        if user_input.lower().startswith('mode '):
            new_mode = user_input.lower().split(' ', 1)[1].strip()
            if new_mode in ('add', 'sell'):
                mode = new_mode
                print(f"  ✅ Switched to {mode.upper()} mode.\n")
            else:
                print("  ⚠️  Unknown mode. Use 'mode add' or 'mode sell'.")
            continue

        # Determine add or subtract
        # '-CODE' always subtracts regardless of mode
        if user_input.startswith('-'):
            subtract = True
            code = user_input.lstrip('-').upper()
        else:
            subtract = (mode == 'sell')
            code = user_input.upper()

        item = find_item(inventory, code)

        if item:
            if subtract:
                if item.get('count', 0) > 0:
                    item['count'] -= 1
                    print(f"  ➖ {item['name']} → count: {item['count']}")
                else:
                    print(f"  ⚠️  {item['name']} is already at 0.")
            else:
                item['count'] = item.get('count', 0) + 1
                print(f"  ➕ {item['name']} → count: {item['count']}")
        else:
            if subtract:
                print(f"  ⚠️  Code '{code}' not found. Cannot subtract.")
            else:
                # Add new item
                name = input(f"  New code '{code}' not found. Enter iris name: ").strip()
                price_str = input(f"  Enter price (default 8.00): ").strip()
                try:
                    price = float(price_str) if price_str else 8.00
                except ValueError:
                    price = 8.00
                new_item = {
                    "code": code,
                    "name": name,
                    "price": price,
                    "count": 1,
                    "description": "",
                    "image": "",
                    "aisWiki": ""
                }
                inventory.append(new_item)
                print(f"  ✅ Added new item: {name} (code: {code}) → count: 1")

        # Auto-save after each scan
        save_inventory(inventory)

if __name__ == '__main__':
    main()
