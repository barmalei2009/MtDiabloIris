# GitHub Copilot Instructions for Mt. Diablo Iris Society Website

This repository is a small static website with a separate Python utility folder for inventory/barcode workflows.

## Project structure
- `index.html` is the site entry point.
- `pages/` contains standalone HTML pages like `events.html`, `gallery.html`, `about-us.html`, and newsletter pages.
- `css/styles.css` is the single stylesheet.
- `js/scripts.js` contains all client-side interactivity and dynamic rendering logic.
- `files/` holds data and content sources used by the site and scripts, e.g. `events.json`, submission templates, inventory data, and CSVs.
- `scripts/` contains Python utilities, not site runtime code.

## Architecture and data flow
- The website is static. There is no build tool, bundler, or server-side rendering step.
- Pages reference assets with relative paths, so preserve directory relationships when editing or moving files.
- `js/scripts.js` loads JSON data for dynamic pages:
  - `pages/events.html` renders event cards from `../files/events.json`.
  - `pages/gallery.html` is expected to render gallery data from `../files/images.json` if added.
- The site uses repeated static markup for navigation and footer in each page, rather than a templating system.

## Key workflows
- Local preview: run a simple HTTP server from repository root.
  - `python -m http.server 8000`
  - or `npm install -g http-server` then `http-server`
- No test suite or package manifest is present; changes are validated by opening the site in a browser and checking the rendered pages.
- Use browser dev tools to inspect fetch failures (`functions.js` loading `files/events.json`) and verify relative asset paths.

## Python utilities
- `scripts/README.md` documents script dependencies: `pip install python-barcode Pillow`.
- `scripts/generate_barcodes.py` reads `files/iris-barcodes.csv`.
- `scripts/generate_labels.py` reads `files/iris-inventory.json`.
- `scripts/inventory_scanner.py` and `scripts/import_iris.py` are maintenance tools separate from the website.

## Project-specific conventions
- Keep static pages minimal and self-contained.
- Prefer direct HTML edits for content updates rather than adding a build or templating step.
- When adding dynamic content, ensure the JSON file path and page `id` match the renderer in `js/scripts.js`.
- `files/event-submission-template.md` is the source template for new event submissions, not a runtime file.

## Notes for agents
- Do not introduce a Node.js build system unless the task explicitly requires it.
- Preserve the existing static layout and relative linking conventions.
- When updating events, edit `files/events.json` and/or `pages/events.html` content, not the JavaScript rendering helper.
- Treat `scripts/` as a separate maintenance area: changes there should not affect the main static website unless the task is specifically about inventory/barcode workflows.

> If you are unsure whether a change belongs in `pages/` or `scripts/`, choose `pages/` for website content and `scripts/` for inventory or label generation utilities.