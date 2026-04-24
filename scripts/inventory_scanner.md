# MDIS Iris Inventory Scanner

A command-line tool for managing iris inventory using a barcode scanner or manual input.

---

## Files Overview

| File | Purpose |
|------|---------|
| `inventory_scanner.py` | Main scanner — add/sell stock by scanning barcodes |
| `generate_barcodes.py` | Generates individual barcode PNG images |
| `generate_labels.py` | Generates Avery 5160 print-ready label sheets |
| `iris-barcodes.csv` | Code-to-name mapping for barcode generation |
| `iris-inventory.json` | Master inventory with counts, prices, and details |

---

## Full Workflow

### Step 1 — Set up inventory codes
Ensure `/Users/sergey/Downloads/MtDiabloIris_website/files/iris-inventory.json` has a `code` field for each item (e.g. `IRIS001`) and a `count` field starting at `0`.

Barcode codes are also listed in:
```
/Users/sergey/Downloads/MtDiabloIris_website/files/iris-barcodes.csv
```

### Step 2 — Generate barcodes
```bash
cd /Users/sergey/Downloads/MyPy
python3 generate_barcodes.py
```
Outputs individual barcode PNG images to `barcodes/`.

### Step 3 — Scan inventory (restock)
```bash
python3 inventory_scanner.py
```
Default mode is **ADD**. Scan each iris bag/tag barcode to increment counts.
When done, type `quit` to save.

### Step 4 — Print labels
```bash
python3 generate_labels.py
```
Reads current counts from `iris-inventory.json`.
Generates one label per unit in stock, arranged on **Avery 5160** sheets (3×10, 30 per page).
Outputs to `labels/labels_A4_page1.png`, `page2.png`, etc.
Print at **300 DPI**, actual size, on Avery 5160 label paper.

### Step 5 — Sell mode (at point of sale)
```bash
python3 inventory_scanner.py
```
Type `mode sell`, then scan barcodes as items are sold to decrement counts automatically.

---

## Commands

| Input | Action |
|-------|--------|
| `IRIS001` (scan or type) | Add or sell 1 depending on current mode |
| `-IRIS001` | Always subtract 1 regardless of mode |
| `mode add` | Switch to **ADD** mode — scans increase count |
| `mode sell` | Switch to **SELL** mode — scans decrease count |
| `list` | Display all items and their current counts |
| `quit` | Save inventory and exit |
| **Ctrl+C** | Force quit (last scan is already auto-saved) |

---

## Modes

The scanner supports two modes shown in the prompt (`[ADD]` or `[SELL]`):

- **ADD mode** (default) — each scan increases the item count by 1. Use when restocking.
- **SELL mode** — each scan decreases the item count by 1. Use at point of sale.

Switch modes at any time by typing `mode add` or `mode sell`.

---

## Barcode Scanner Setup

1. Plug in any USB barcode scanner that supports **Code128**.
2. Click into the terminal window running the script.
3. Scan a barcode — the scanner types the code and presses Enter automatically.

---

## Adding New Items

If a scanned code is not found in the inventory, the script will prompt:
1. Enter the iris name
2. Enter the price (default: $8.00)

The new item is added with a count of 1 and saved automatically.

---

## Inventory File Format

Each item in `iris-inventory.json`:

| Field | Description |
|-------|-------------|
| `code` | Unique barcode ID (e.g. `IRIS001`) |
| `name` | Iris variety name |
| `price` | Price per plant |
| `count` | Current quantity in stock |
| `description` | Short description |
| `image` | Image filename |
| `aisWiki` | Link to AIS Wiki entry |

---

## Label Format (Avery 5160)

- **Label size:** 2-5/8" × 1"
- **Layout:** 3 columns × 10 rows = 30 labels per sheet
- **Resolution:** 300 DPI
- **Content:** Barcode + iris name
- **Quantity:** One label generated per unit in stock

