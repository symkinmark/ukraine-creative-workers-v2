#!/usr/bin/env python3
"""
romanize_paper.py — Apply ALA-LC romanization to PAPER_DRAFT.md
Berdnyk & Symkin research tools

Usage:
    python3 ukraine_v2/romanize_paper.py --preview    # show changes, don't touch file
    python3 ukraine_v2/romanize_paper.py --apply      # write changes to file

Format applied:
    First occurrence of each unique Cyrillic string:  Romanized [Cyrillic]
    Subsequent occurrences:                           Romanized

Lines that are deliberately left as Cyrillic:
    - Profession keyword lists (lines containing поет, письменник etc. in list context)
    - Lines that are already inside a [...] bracket pair (already annotated)
    - Lines in the bibliography that show Cyrillic as the original title in brackets
    - The ЕСУ institutional name when it appears inside a bracket already
"""

import os
import re
import sys
import subprocess

PROJECT  = os.path.dirname(os.path.abspath(__file__))
PAPER    = os.path.join(PROJECT, 'PAPER_DRAFT.md')
SCRIPT   = os.path.join(PROJECT, 'romanize.py')

# Lines containing these strings are profession/methodology keyword lists — skip entirely
SKIP_LINE_MARKERS = [
    'поет',            # profession list line
    'письменник',
    'журналіст',
    'Українець/Українка',
    'спецпоселенець',
]

# Cyrillic strings to leave untouched (they're inside brackets already or
# are the canonical Cyrillic form in the bibliography)
SKIP_STRINGS = {
    # Already presented as [Cyrillic] in bibliography/footnotes — don't double-wrap
}

from romanize import romanize, find_cyrillic_spans


def should_skip_line(line: str) -> bool:
    for marker in SKIP_LINE_MARKERS:
        if marker in line:
            return True
    return False


def process(text: str, apply: bool):
    lines = text.split('\n')
    seen = {}          # cyrillic_string -> romanized (track first occurrences)
    new_lines = []
    changes = []

    for lineno, line in enumerate(lines, start=1):
        if should_skip_line(line):
            new_lines.append(line)
            continue

        spans = find_cyrillic_spans(line)
        if not spans:
            new_lines.append(line)
            continue

        # Work right-to-left so character positions stay valid
        new_line = line
        for start, end, cyrillic in reversed(spans):
            # Skip if already inside [...] square brackets
            before = new_line[:start]
            if before.rfind('[') > before.rfind(']'):
                continue

            # Skip if the Cyrillic span is INSIDE a parenthetical that already
            # contains a romanization: pattern ( Cyrillic, Latin romanization )
            # Only triggers if paren_open is AFTER the last closing paren before start,
            # meaning the Cyrillic is actually inside the paren — not before it.
            last_close_before = before.rfind(')')
            paren_open = before.rfind('(')
            if paren_open > last_close_before and paren_open >= 0:
                # Cyrillic is inside an open paren — check if paren also has Latin after comma
                paren_close = new_line.find(')', end)
                if paren_close >= 0:
                    inside_paren = new_line[paren_open:paren_close + 1]
                    comma_pos = inside_paren.find(',')
                    if comma_pos >= 0:
                        after_comma = inside_paren[comma_pos:]
                        if re.search(r'[A-Za-z]', after_comma):
                            continue

            rom = romanize(cyrillic)
            if not rom.strip():
                continue

            if cyrillic not in seen:
                seen[cyrillic] = rom
                replacement = f'{rom} [{cyrillic}]'
                is_first = True
            else:
                replacement = rom
                is_first = False

            changes.append({
                'line': lineno,
                'original': cyrillic,
                'romanized': rom,
                'first': is_first,
            })

            if apply:
                new_line = new_line[:start] + replacement + new_line[end:]

        new_lines.append(new_line)

    return '\n'.join(new_lines), changes


def main():
    mode = '--preview'
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    if mode not in ('--preview', '--apply'):
        print("Usage: python3 romanize_paper.py [--preview|--apply]")
        sys.exit(1)

    with open(PAPER, encoding='utf-8') as f:
        text = f.read()

    applying = (mode == '--apply')
    new_text, changes = process(text, apply=applying)

    if not changes:
        print("No Cyrillic found that needs romanization.")
        return

    print(f"\n{'='*70}")
    print(f"ALA-LC ROMANIZATION — {'APPLYING' if applying else 'PREVIEW'}")
    print(f"{'='*70}")
    for c in changes:
        tag = '[FIRST — with Cyrillic in brackets]' if c['first'] else '[subsequent]'
        print(f"  Line {c['line']:4d}: {c['original']}  →  {c['romanized']}  {tag}")
    print(f"{'='*70}")
    print(f"Total changes: {len(changes)}")

    if applying:
        with open(PAPER, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"\nFile updated: {PAPER}")

        # Rebuild HTML and highlight the first change
        if changes:
            first_rom = changes[0]['romanized']
            subprocess.run(
                ['python3', os.path.join(PROJECT, 'highlight_fix.py'), first_rom],
                cwd=PROJECT
            )
    else:
        print("\nRun with --apply to write changes.")


if __name__ == '__main__':
    main()
