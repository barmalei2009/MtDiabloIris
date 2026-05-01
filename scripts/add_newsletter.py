#!/usr/bin/env python3
"""
add_newsletter.py - Add a monthly newsletter PDF to the MDIS website.

Usage:
    python add_newsletter.py <pdf_file> [<month>] [<year>]

Arguments:
    pdf_file   Path to the newsletter PDF file
    month      Month name or number (e.g. "April", "Apr", "4"). Optional if
               the filename contains the month (e.g. Apr2026.pdf).
    year       4-digit year (e.g. 2026). Optional if inferable from filename
               or defaults to the current year.

Examples:
    python add_newsletter.py ~/Downloads/Apr2026.pdf
    python add_newsletter.py ~/Downloads/newsletter.pdf April 2026
    python add_newsletter.py ~/Downloads/newsletter.pdf 4 2026
"""

import sys
import os
import re
import shutil
from datetime import datetime

MONTH_FULL = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December",
}

MONTH_SHORT = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
}

MONTH_DESC = {
    1: "Start the year with club news and winter iris care tips.",
    2: "Club news, planting guidance, and event recaps.",
    3: "Spring planting tips and society updates.",
    4: "Show season news and spring highlights.",
    5: "Late spring iris care and member spotlights.",
    6: "Summer iris care and club announcements.",
    7: "Mid-summer updates and member stories.",
    8: "Late summer news and garden tips.",
    9: "Fall preview and club happenings.",
    10: "Autumn events and iris care reminders.",
    11: "Year-end wrap-up and winter prep.",
    12: "Holiday greetings and end-of-year club news.",
}

# Build lookup: full/short name and number string -> month number
_NAME_TO_NUM = {}
for _n, _full in MONTH_FULL.items():
    _NAME_TO_NUM[_full.lower()] = _n
    _NAME_TO_NUM[_full[:3].lower()] = _n
    _NAME_TO_NUM[str(_n)] = _n
    _NAME_TO_NUM[f"{_n:02d}"] = _n


def parse_month(value: str) -> int | None:
    return _NAME_TO_NUM.get(value.strip().lower())


def infer_from_filename(filename: str):
    """Return (month_num, year) parsed from filename, or (None, None)."""
    name = os.path.splitext(filename)[0]

    # Pattern: MonYYYY or Month_YYYY etc. e.g. Apr2026, April-2026
    m = re.search(r'([A-Za-z]+)[_\-]?(\d{4})', name)
    if m:
        month = parse_month(m.group(1))
        if month:
            return month, int(m.group(2))

    # Pattern: MM_YYYY or MM-YYYY e.g. 04_2026
    m = re.search(r'(\d{1,2})[_\-](\d{4})', name)
    if m:
        month = parse_month(m.group(1))
        if month:
            return month, int(m.group(2))

    # Pattern: YYYYMM
    m = re.search(r'(\d{4})(\d{2})', name)
    if m:
        month = parse_month(m.group(2))
        if month:
            return month, int(m.group(1))

    return None, None


def create_year_page(path: str, year: int):
    content = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{year} Newsletters - Mt. Diablo Iris Society</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
  <nav>
    <a href="../index.html" class="nav-logo">
      <img src="../images/logo-flower.jpg" alt="Iris Flower" class="logo-mark">
      <div class="logo-text">
        Mt. Diablo
        <span>Iris Society</span>
      </div>
    </a>
    <ul class="nav-links">
      <li><a href="about-us.html">About Us</a></li>
      <li><a href="events.html">Events</a></li>
      <li><a href="gallery.html">Gallery</a></li>
      <li><a href="about-iris.html">About Iris</a></li>
      <li><a href="resources.html">Resources</a></li>
      <li><a href="about-us.html#membership" class="nav-cta">Join Us</a></li>
    </ul>
  </nav>
  <main>
    <section class="interior-header reveal">
      <div class="interior-header-inner">
        <div class="section-eyebrow">Club Publications</div>
        <h2 class="section-title">{year} Newsletters</h2>
        <p class="section-body">Browse our {year} club newsletters below.</p>
      </div>
    </section>
    <section class="about-section reveal">
      <div class="about-card-grid">
      </div>
    </section>
  </main>
  <footer>
    <p>&copy; {year} Mt. Diablo Iris Society</p>
  </footer>
  <script src="../js/scripts.js"></script>
</body>
</html>
"""
    with open(path, "w") as f:
        f.write(content)
    print(f"  Created new page: pages/newsletters-{year}.html")


def add_card(html_path: str, month_num: int, year: int, pdf_filename: str):
    month_label = f"{MONTH_FULL[month_num]} {year}"
    card = (
        f'        <a class="about-card" href="../files/newsletters/{pdf_filename}" target="_blank">\n'
        f'          <h3>{month_label}</h3>\n'
        f'          <p>{MONTH_DESC[month_num]}</p>\n'
        f'        </a>'
    )

    with open(html_path, "r") as f:
        content = f.read()

    if month_label in content:
        print(f"  Warning: '{month_label}' already exists in the page — skipping HTML update.")
        return

    # Insert before the closing </div> of about-card-grid (6-space indent)
    grid_start = content.find('<div class="about-card-grid">')
    if grid_start == -1:
        print("  Error: could not find <div class=\"about-card-grid\"> in the page.")
        sys.exit(1)

    grid_close = content.find('\n      </div>', grid_start)
    if grid_close == -1:
        print("  Error: could not find closing </div> for about-card-grid.")
        sys.exit(1)

    new_content = content[:grid_close] + "\n" + card + content[grid_close:]

    with open(html_path, "w") as f:
        f.write(new_content)

    print(f"  Added '{month_label}' card to pages/newsletters-{year}.html")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if sys.argv[1:] else 1)

    pdf_src = sys.argv[1]
    month_arg = sys.argv[2] if len(sys.argv) > 2 else None
    year_arg = sys.argv[3] if len(sys.argv) > 3 else None

    if not os.path.isfile(pdf_src):
        print(f"Error: file not found: {pdf_src}")
        sys.exit(1)

    # Resolve month/year
    month_num, year = infer_from_filename(os.path.basename(pdf_src))

    if month_arg:
        parsed = parse_month(month_arg)
        if not parsed:
            print(f"Error: unrecognized month '{month_arg}'")
            sys.exit(1)
        month_num = parsed

    if year_arg:
        year = int(year_arg)

    if not month_num:
        month_num = datetime.now().month
        print(f"  Month not detected — using current month ({MONTH_FULL[month_num]}).")

    if not year:
        year = datetime.now().year
        print(f"  Year not detected — using current year ({year}).")

    pdf_filename = f"{MONTH_SHORT[month_num]}{year}.pdf"

    # Resolve repo root relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)

    # Copy PDF
    newsletters_dir = os.path.join(repo_root, "files", "newsletters")
    os.makedirs(newsletters_dir, exist_ok=True)
    pdf_dest = os.path.join(newsletters_dir, pdf_filename)

    if os.path.exists(pdf_dest):
        print(f"  Warning: files/newsletters/{pdf_filename} already exists — overwriting.")

    shutil.copy2(pdf_src, pdf_dest)
    print(f"  Copied PDF  →  files/newsletters/{pdf_filename}")

    # Update / create HTML page
    html_path = os.path.join(repo_root, "pages", f"newsletters-{year}.html")
    if not os.path.exists(html_path):
        create_year_page(html_path, year)

    add_card(html_path, month_num, year, pdf_filename)

    print(f"\nDone. {MONTH_FULL[month_num]} {year} newsletter is live.")


if __name__ == "__main__":
    main()
