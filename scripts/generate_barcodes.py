import csv
import os
import barcode
from barcode.writer import ImageWriter

# Paths
csv_path = '../files/iris-barcodes.csv'
output_dir = 'barcodes'
os.makedirs(output_dir, exist_ok=True)

with open(csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        code = row['code']
        name = row['name']
        barcode_obj = barcode.get('code128', code, writer=ImageWriter())
        filename = os.path.join(output_dir, f'{code}_{name.replace(" ", "_")}')
        barcode_obj.save(filename)
        print(f"Saved: {filename}.png")
