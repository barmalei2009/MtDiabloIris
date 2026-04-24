# Iris Scripts

This folder contains scripts for managing iris inventory, generating barcodes, labels, and scanning.

## Dependencies

Install required Python packages:

```bash
pip install python-barcode Pillow
```

## Scripts

- `generate_barcodes.py`: Generates barcode images from `iris-barcodes.csv`
- `generate_labels.py`: Generates printable labels from `iris-inventory.json`
- `inventory_scanner.py`: Command-line tool for scanning barcodes to update inventory
- `import_iris.py`: Imports iris data from `alden_lane.txt` into inventory

## Usage

Run from the `scripts/` directory:

```bash
cd scripts
python generate_labels.py
python inventory_scanner.py
# etc.
```

## Files

- `iris-barcodes.csv`: CSV with iris codes and names for barcodes
- `alden_lane.txt`: Text file with iris data for import
- `barcodes/`: Directory for generated barcode images
- `labels/`: Directory for generated label sheets