#!/usr/bin/env python3
"""
pdf_search.py — Token-efficient PDF source checker
Berdnyk & Symkin research tools

Usage:
    python3 ukraine_v2/pdf_search.py path/to/book.pdf "keyword or claim phrase"
    python3 ukraine_v2/pdf_search.py path/to/book.pdf "death rate" "1942" "annual"

What it does:
    - Extracts text page by page
    - Finds pages containing ALL search terms (AND logic)
    - Returns only the relevant passage (±4 lines around each hit)
    - Shows page numbers so you can open the PDF to verify
    - Prints nothing for pages with no hits — keeps output minimal

Output is intentionally short — meant to be pasted into Claude context
without wasting tokens on irrelevant pages.
"""

import sys
import re
import textwrap
import pdfplumber

CONTEXT_LINES = 4      # lines before/after each match to show
MAX_HITS_PER_PAGE = 3  # stop after this many hit-passages per page


def extract_passages(pdf_path, terms):
    terms_lower = [t.lower() for t in terms]
    results = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"PDF: {pdf_path}")
        print(f"Pages: {total_pages}  |  Searching for: {terms}\n")
        print("=" * 70)

        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue

            text_lower = text.lower()

            # Page must contain ALL search terms (AND logic)
            if not all(t in text_lower for t in terms_lower):
                continue

            # Split into lines and find hit lines
            lines = text.split('\n')
            hit_count = 0

            for i, line in enumerate(lines):
                if any(t in line.lower() for t in terms_lower):
                    if hit_count >= MAX_HITS_PER_PAGE:
                        break

                    # Extract surrounding context
                    start = max(0, i - CONTEXT_LINES)
                    end   = min(len(lines), i + CONTEXT_LINES + 1)
                    passage = '\n'.join(lines[start:end])

                    # Highlight matched terms
                    for term in terms:
                        passage = re.sub(
                            re.escape(term),
                            f'>>>{term}<<<',
                            passage,
                            flags=re.IGNORECASE
                        )

                    results.append((page_num, passage))
                    hit_count += 1

    return results


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 pdf_search.py <file.pdf> <term1> [term2] [term3]")
        print('Example: python3 pdf_search.py applebaum.pdf "death rate" "1942"')
        sys.exit(1)

    pdf_path = sys.argv[1]
    terms    = sys.argv[2:]

    hits = extract_passages(pdf_path, terms)

    if not hits:
        print(f"NO MATCHES found for: {terms}")
        print("Try fewer or broader terms.")
        return

    print(f"Found {len(hits)} passage(s):\n")
    for page_num, passage in hits:
        print(f"── PAGE {page_num} " + "─" * 50)
        print(textwrap.indent(passage.strip(), "  "))
        print()

    print("=" * 70)
    print(f"Total hits: {len(hits)}  |  Terms: {terms}")


if __name__ == '__main__':
    main()
