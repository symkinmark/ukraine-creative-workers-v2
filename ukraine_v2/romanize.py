#!/usr/bin/env python3
"""
romanize.py — ALA-LC Ukrainian romanization (Library of Congress standard)
Berdnyk & Symkin research tools

Usage:
    python3 ukraine_v2/romanize.py "Василь Стус"
    python3 ukraine_v2/romanize.py "Розстріляне Відродження"

ALA-LC source: Library of Congress Romanization Tables — Ukrainian
https://www.loc.gov/catdir/cpso/romanization/ukrainia.pdf
"""

import sys
import re
import unicodedata

# ---------------------------------------------------------------------------
# ALA-LC Ukrainian character map (lowercase; capitalisation handled separately)
# Multi-character outputs listed for digraph pairs first (Щ before Ш, etc.)
# ---------------------------------------------------------------------------

CHAR_MAP = {
    # Standard single-char mappings
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'h',      # Ukrainian Г = H, not G
    'ґ': 'g',      # Ukrainian Ґ = G
    'д': 'd',
    'е': 'e',
    'є': 'ie',
    'ж': 'zh',
    'з': 'z',
    'и': 'y',
    'і': 'i',
    'ї': 'ï',      # i with dieresis (U+00EF)
    'й': 'ĭ',      # i with breve (U+012D)
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ь': 'ʹ',      # modifier letter prime U+02B9 (soft sign)
    'ю': 'iu',
    'я': 'ia',
    # Hard sign — rare in Ukrainian, omit silently
    'ъ': '',
    # Ukrainian apostrophe (hard sign separator) — omit silently
    '\u2019': '',  # RIGHT SINGLE QUOTATION MARK (used as Ukrainian apostrophe)
    "'": '',       # ASCII apostrophe fallback
}

VOWELS = set('аеєиіїоуюя')


def _apply_case(source_char: str, output: str) -> str:
    """
    If source_char is uppercase, capitalise the first letter of output only.
    ALA-LC rule: Ш → Sh (not SH), Щ → Shch (not SHCH).
    """
    if source_char.isupper() and output:
        return output[0].upper() + output[1:]
    return output


def romanize(text: str) -> str:
    """
    Romanize Ukrainian Cyrillic text to ALA-LC.
    Non-Cyrillic characters are passed through unchanged.
    """
    result = []
    i = 0
    chars = list(text)

    while i < len(chars):
        ch = chars[i]
        ch_lower = ch.lower()

        if ch_lower in CHAR_MAP:
            mapped = CHAR_MAP[ch_lower]
            result.append(_apply_case(ch, mapped))
        else:
            # Not in map — pass through (Latin, digits, punctuation, spaces)
            result.append(ch)

        i += 1

    return ''.join(result)


def find_cyrillic_spans(text: str):
    """
    Return list of (start, end, substring) for each run of Cyrillic characters
    (including Ukrainian apostrophe within a word).
    """
    # Match Cyrillic Unicode block + Ukrainian apostrophe/quote mid-word
    pattern = re.compile(r"[\u0400-\u04FF\u2019']+(?:\s+[\u0400-\u04FF\u2019']+)*")
    spans = []
    for m in pattern.finditer(text):
        # Only include if it actually contains Cyrillic (not just apostrophes)
        if re.search(r'[\u0400-\u04FF]', m.group()):
            spans.append((m.start(), m.end(), m.group()))
    return spans


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 romanize.py \"Ukrainian text\"")
        sys.exit(1)
    text = ' '.join(sys.argv[1:])
    print(romanize(text))
