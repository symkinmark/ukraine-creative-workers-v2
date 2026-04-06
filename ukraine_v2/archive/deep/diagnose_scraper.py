#!/usr/bin/env python3
"""
V2.3 Diagnostic Script — ESU Scraper Pagination Audit
READ-ONLY — makes HTTP GET requests only, no writes.

Checks:
1. What does get_total_pages() return for each suspicious letter?
2. What is the actual pagination HTML for those letters?
3. Do the missing famous figures appear in any page HTML?

Usage: python3 diagnose_scraper.py
"""

import requests
import re
import time
import sys

BASE_URL = "https://esu.com.ua"

# Letters with suspiciously low counts from V2.2 scrape
SUSPECT_LETTERS = ['р', 'с', 'т', 'х', 'ч']

# Letters we know worked well (control group)
CONTROL_LETTERS = ['к', 'м', 'б']

# Famous figures we know are absent from raw CSV — search for them in page HTML
MISSING_FIGURES = [
    'Тичина',    # letter т
    'Рильськ',   # letter р
    'Семенко',   # letter с
    'Хвильов',   # letter х
    'Стус',      # letter с
    'Чорновіл',  # letter ч
    'Симоненко', # letter с
    'Світличн',  # letter с
]


def make_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ),
        'Accept-Language': 'uk,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    })
    return session


def get_total_pages_original(html):
    """Original buggy implementation from esu_scraper.py."""
    m = re.search(r'із\s+(\d+)', html)
    return int(m.group(1)) if m else 1


def get_total_pages_fixed(html):
    """Fixed implementation — tries multiple patterns, falls back to scanning."""
    # Pattern 1: original "із N"
    m = re.search(r'із\s+(\d+)', html)
    if m:
        return int(m.group(1)), 'pattern: із N'

    # Pattern 2: "з N" without "із"
    m = re.search(r'\bз\s+(\d+)', html)
    if m:
        return int(m.group(1)), 'pattern: з N'

    # Pattern 3: generic "of N" (English)
    m = re.search(r'\bof\s+(\d+)', html)
    if m:
        return int(m.group(1)), 'pattern: of N'

    # Pattern 4: look for any "page X of N" style
    m = re.search(r'(\d+)\s*[/з]\s*(\d+)', html)
    if m:
        return int(m.group(2)), 'pattern: N/M'

    return 1, 'fallback: no pattern found'


def extract_pagination_context(html, window=200):
    """Find the pagination HTML section and return surrounding text."""
    # Common pagination markers
    markers = ['Стор', 'page', 'Page', 'із', 'пагін', 'pagination', 'pages']
    for marker in markers:
        idx = html.lower().find(marker.lower())
        if idx >= 0:
            start = max(0, idx - 50)
            end = min(len(html), idx + window)
            return html[start:end].strip()
    return "(no pagination marker found)"


def check_for_missing_figures(html, letter):
    """Search page HTML for any of the missing famous figures."""
    found = []
    for name in MISSING_FIGURES:
        if name.lower() in html.lower():
            found.append(name)
    return found


def diagnose_letter(letter, session):
    """Full diagnosis for a single letter."""
    print(f"\n{'='*60}")
    print(f"LETTER: {letter.upper()}")
    print(f"{'='*60}")

    # Fetch page 1
    url = f"{BASE_URL}/letter.php?s={letter}&page=1"
    print(f"Fetching: {url}")
    try:
        r = session.get(url, timeout=20)
        html = r.text
        print(f"  HTTP {r.status_code}, {len(html):,} chars")
    except Exception as e:
        print(f"  FAILED: {e}")
        return

    # Original get_total_pages
    original_result = get_total_pages_original(html)
    print(f"\n  get_total_pages() [ORIGINAL]: {original_result}")

    # Fixed get_total_pages
    fixed_result, method = get_total_pages_fixed(html)
    print(f"  get_total_pages() [FIXED]:    {fixed_result} (via {method})")

    # Show pagination context
    context = extract_pagination_context(html)
    print(f"\n  Pagination HTML context:")
    print(f"  {repr(context[:300])}")

    # Count h2 tags (approximate entries on this page)
    h2_count = html.lower().count('<h2')
    print(f"\n  <h2> tags on page 1: {h2_count}")

    # Check for missing famous figures on page 1
    found = check_for_missing_figures(html, letter)
    if found:
        print(f"\n  Famous figures found on PAGE 1: {found}")
    else:
        print(f"\n  Famous figures on page 1: NONE")

    # If original says 1 but fixed says more → CONFIRMED PAGINATION BUG
    if original_result == 1 and fixed_result > 1:
        print(f"\n  *** PAGINATION BUG CONFIRMED for '{letter}' ***")
        print(f"  Original returns 1, but there are actually {fixed_result} pages")

        # Check page 2 for famous figures
        time.sleep(0.8)
        url2 = f"{BASE_URL}/letter.php?s={letter}&page=2"
        print(f"\n  Checking page 2: {url2}")
        try:
            r2 = session.get(url2, timeout=20)
            html2 = r2.text
            h2_count2 = html2.lower().count('<h2')
            print(f"  Page 2: HTTP {r2.status_code}, {h2_count2} <h2> tags")
            found2 = check_for_missing_figures(html2, letter)
            if found2:
                print(f"  Famous figures found on PAGE 2: {found2} ← THEY'RE HERE!")
        except Exception as e:
            print(f"  Page 2 fetch failed: {e}")

    elif original_result == fixed_result == 1:
        print(f"\n  Original and fixed both return 1 — may be a 1-page letter OR both broken")

    return original_result, fixed_result


def main():
    print("ESU Scraper Pagination Diagnostic — V2.3")
    print("Read-only. No writes. HTTP GET only.")
    print()

    session = make_session()

    results = {}

    # Check control letters first
    print("\n--- CONTROL LETTERS (should be working) ---")
    for letter in CONTROL_LETTERS:
        orig, fixed = diagnose_letter(letter, session) or (1, 1)
        results[letter] = (orig, fixed)
        time.sleep(1.0)

    # Check suspect letters
    print("\n\n--- SUSPECT LETTERS (likely broken) ---")
    for letter in SUSPECT_LETTERS:
        orig, fixed = diagnose_letter(letter, session) or (1, 1)
        results[letter] = (orig, fixed)
        time.sleep(1.0)

    # Summary
    print(f"\n\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"{'Letter':<10} {'Original':<12} {'Fixed':<10} {'Status'}")
    print("-" * 50)
    for letter, (orig, fixed) in results.items():
        if orig == 1 and fixed > 1:
            status = f"*** BUG — missing {fixed-1} pages"
        elif orig == fixed:
            status = "OK"
        else:
            status = "?"
        print(f"  {letter.upper():<8} {orig:<12} {fixed:<10} {status}")

    print("\nDone.")


if __name__ == '__main__':
    main()
