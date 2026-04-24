import json
import os
import math
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter

INVENTORY_FILE = '../files/iris-inventory.json'
output_dir = 'labels'
os.makedirs(output_dir, exist_ok=True)

# Font
font_path = "/Library/Fonts/Arial.ttf"

# Avery 5160: 2-5/8" x 1", 3 cols x 10 rows, on 8.5" x 11" sheet at 300 DPI
DPI = 300
PAGE_W = int(8.5 * DPI)       # 2550 px
PAGE_H = int(11.0 * DPI)      # 3300 px
LABEL_W = int(2.625 * DPI)    # 787 px
LABEL_H = int(1.0 * DPI)      # 300 px
TOP_MARGIN = int(0.5 * DPI)   # 150 px
LEFT_MARGIN = int(0.1875 * DPI)  # 56 px
COL_PITCH = int(2.75 * DPI)   # 825 px (left edge to left edge)
ROW_PITCH = int(1.0 * DPI)    # 300 px
COLS = 3
ROWS = 10
LABELS_PER_PAGE = COLS * ROWS
LABEL_PADDING = 10

def make_label(code, name, count):
    """Generate a single label image with barcode and iris name (no code text)."""
    barcode_filename = f'/tmp/{code}.png'
    barcode_obj = barcode.get('code128', code, writer=ImageWriter())
    # Save without the text below the barcode
    barcode_path = barcode_obj.save(barcode_filename, options={"write_text": False})
    barcode_img = Image.open(barcode_path).convert('RGB')

    # Resize barcode — reserve 60px at bottom for the iris name
    NAME_AREA = 60
    bc_w = LABEL_W - LABEL_PADDING * 2
    max_bc_h = LABEL_H - NAME_AREA
    ratio = bc_w / barcode_img.width
    bc_h = int(barcode_img.height * ratio)
    if bc_h > max_bc_h:
        bc_h = max_bc_h
        bc_w = int(barcode_img.width * (bc_h / barcode_img.height))
    barcode_img = barcode_img.resize((bc_w, bc_h), Image.LANCZOS)

    label = Image.new('RGB', (LABEL_W, LABEL_H), 'white')
    # Center barcode horizontally
    label.paste(barcode_img, ((LABEL_W - bc_w) // 2, 0))

    draw = ImageDraw.Draw(label)
    try:
        font_name = ImageFont.truetype(font_path, 34)
    except:
        font_name = ImageFont.load_default()

    # Name — placed in the reserved area below barcode
    bbox = draw.textbbox((0, 0), name, font=font_name)
    tw = bbox[2] - bbox[0]
    text_y = bc_h + (NAME_AREA - (bbox[3] - bbox[1])) // 2
    draw.text(((LABEL_W - tw) // 2, text_y), name, fill='black', font=font_name)

    # Border
    draw.rectangle([(0, 0), (LABEL_W - 1, LABEL_H - 1)], outline='#cccccc', width=1)

    return label

# Load inventory
with open(INVENTORY_FILE, 'r') as f:
    inventory = json.load(f)

# Only include items with count > 0
items = [item for item in inventory if item.get('count', 0) > 0]

if not items:
    print("No items with count > 0 found in inventory.")
    exit()

# Build all labels
labels = []
for item in items:
    code = item.get('code', '')
    name = item.get('name', '')
    count = item.get('count', 0)
    # Repeat label for each unit in stock
    for _ in range(count):
        labels.append(make_label(code, name, count))
    print(f"  Generated label for: {name} (x{count})")

# Calculate label size from first label
lw, lh = labels[0].size
gap = 0
total_pages = math.ceil(len(labels) / LABELS_PER_PAGE)

print(f"\n  {len(labels)} labels across {total_pages} Avery 5160 sheet(s)...")

for page_num in range(total_pages):
    page = Image.new('RGB', (PAGE_W, PAGE_H), 'white')
    page_labels = labels[page_num * LABELS_PER_PAGE:(page_num + 1) * LABELS_PER_PAGE]

    for i, label in enumerate(page_labels):
        col = i % COLS
        row = i // COLS
        x = LEFT_MARGIN + col * COL_PITCH
        y = TOP_MARGIN + row * ROW_PITCH
        page.paste(label, (x, y))

    page_path = os.path.join(output_dir, f'labels_A4_page{page_num + 1}.png')
    page.save(page_path)
    print(f"  Saved: {page_path}")

print("\nDone!")
