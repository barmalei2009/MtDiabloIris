import json
import csv
import re

INPUT_FILE = 'alden_lane.txt'
INVENTORY_FILE = '../files/iris-inventory.json'
CSV_FILE = '../files/iris-barcodes.csv'

# Load existing inventory and CSV to find the highest existing code
with open(INVENTORY_FILE, 'r') as f:
    inventory = json.load(f)

existing_codes = [item.get('code', '') for item in inventory]
existing_names = {item['name'].strip().lower() for item in inventory}

# Find the next available code number
max_num = 0
for code in existing_codes:
    m = re.match(r'IRIS(\d+)', code)
    if m:
        max_num = max(max_num, int(m.group(1)))

next_num = max_num + 1

# Parse alden_lane.txt
new_items = []
with open(INPUT_FILE, 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        # Each line: "Name   TYPE" — split on last whitespace cluster
        parts = re.split(r'\s{2,}|\t', line)
        if len(parts) >= 2:
            name = parts[0].strip()
            iris_type = parts[-1].strip()
        else:
            # fallback: last word is type
            tokens = line.rsplit(None, 1)
            if len(tokens) == 2:
                name, iris_type = tokens[0].strip(), tokens[1].strip()
            else:
                continue

        # Skip if already in inventory
        if name.lower() in existing_names:
            print(f"  Skipping duplicate: {name}")
            continue

        code = f'IRIS{next_num:04d}'
        next_num += 1

        new_items.append({
            "code": code,
            "name": name,
            "type": iris_type,
            "price": 8.00,
            "count": 0,
            "description": f"{iris_type} iris.",
            "image": "",
            "aisWiki": ""
        })

# Append to inventory
inventory.extend(new_items)
with open(INVENTORY_FILE, 'w') as f:
    json.dump(inventory, f, indent=2)

# Append to CSV
with open(CSV_FILE, 'r') as f:
    existing_csv = f.read()

with open(CSV_FILE, 'a', newline='') as f:
    writer = csv.writer(f)
    for item in new_items:
        writer.writerow([item['code'], item['name']])

print(f"\n✅ Added {len(new_items)} irises.")
print(f"   Codes range: IRIS{max_num + 1:04d} – IRIS{next_num - 1:04d}")
