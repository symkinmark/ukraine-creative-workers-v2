#!/usr/bin/env python3
"""
add_gender.py — Gender Classification Pass
Ukrainian Creative Workers V2.1
Berdnyk & Symkin 2026

Adds a `gender` column to esu_creative_workers_v2_1.csv.

Strategy (fastest + cheapest):
  1. Rule-based: Ukrainian/Slavic first-name endings are strongly gendered.
     - First name ends in -а, -я, -ія, -іна, -іла, -іда → female
     - First name ends in consonant, -о, -ій, -ій, -ій    → male
     - First name not parseable                            → unknown → Claude Haiku
  2. Claude Haiku for anything the rule engine marks unknown (~5-10% of entries).
     Context: full name + notes field fed to Haiku with a tight prompt.

Output: rewrites esu_creative_workers_v2_1.csv in-place,
        adds column `gender` (male / female / unknown) after `migration_reasoning`.

Cost estimate: ~5,000–7,000 Haiku calls at most → < $0.30

Run:
    python3 ukraine_v2/add_gender.py
    python3 ukraine_v2/add_gender.py --rerun    # re-classify everything from scratch
"""

import csv
import os
import re
import sys
import time
import argparse
import anthropic

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
CSV_PATH = os.path.join(os.path.dirname(__file__), 'esu_creative_workers_v2_1.csv')
MODEL    = 'claude-haiku-4-5-20251001'
DELAY    = 0.25   # seconds between Claude calls

client = anthropic.Anthropic()

# ---------------------------------------------------------------------------
# RULE-BASED ENGINE
# Ukrainian naming conventions:
#   - Full name format: SURNAME Firstname Patronymic  (Patronymic optional)
#   - First name is the second token (index 1 after splitting on space)
#   - Female first names almost always end: -а, -я, -ія, and also -іна, -ла, -да
#   - Male first names almost always end: consonant, -о, -ій, -ій, -ін, -ил
#
# Additionally: patronymics are strongly gendered:
#   female patronymic ends in -івна, -ївна, -овна
#   male   patronymic ends in -ович, -йович, -євич
# We use patronymic as a high-confidence tiebreaker.
# ---------------------------------------------------------------------------

FEMALE_ENDINGS = ('а', 'я', 'ія', 'іна', 'іла', 'іда', 'іра', 'ора', 'еа')
MALE_ENDINGS   = ('ій', 'ій', 'ій', 'ін', 'ил', 'ел', 'ер', 'ан', 'он',
                  'ко', 'о')  # -о is tricky (Іванко → male), handled below
FEMALE_PATRONYMIC_ENDINGS = ('івна', 'ївна', 'овна', 'евна')
MALE_PATRONYMIC_ENDINGS   = ('ович', 'йович', 'євич', 'евич')


def parse_first_name(full_name: str):
    """Return first_name, patronymic (may be empty) from 'SURNAME Firstname [Patronymic]'."""
    parts = full_name.strip().split()
    if len(parts) < 2:
        return '', ''
    first = parts[1]
    patronymic = parts[2] if len(parts) >= 3 else ''
    return first, patronymic


def rule_gender(full_name: str) -> str:
    """
    Return 'male', 'female', or 'unknown'.
    Priority: patronymic (very reliable) → first name ending → unknown.
    """
    first, patronymic = parse_first_name(full_name)
    if not first:
        return 'unknown'

    first_lower = first.lower()
    pat_lower   = patronymic.lower()

    # 1. Patronymic — highest confidence
    if pat_lower:
        if any(pat_lower.endswith(e) for e in FEMALE_PATRONYMIC_ENDINGS):
            return 'female'
        if any(pat_lower.endswith(e) for e in MALE_PATRONYMIC_ENDINGS):
            return 'male'

    # 2. First-name ending — female check (most unambiguous)
    if any(first_lower.endswith(e) for e in FEMALE_ENDINGS):
        # Special case: -ко, -но, -ло endings (Іванко, Тарасенко) are male
        if first_lower.endswith('ко') or first_lower.endswith('но') or first_lower.endswith('ло'):
            return 'male'
        return 'female'

    # 3. First-name ending — male check
    # ends in consonant (not -а/-я) → male
    vowels = 'аеєиіїоуюя'
    if first_lower and first_lower[-1] not in vowels:
        return 'male'

    # 4. Ends in -о → male (e.g., Тарасенко, Павло, Михайло)
    if first_lower.endswith('о'):
        return 'male'

    return 'unknown'


# ---------------------------------------------------------------------------
# CLAUDE FALLBACK (Haiku)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """\
You are a Ukrainian name gender classifier. Given a full Ukrainian name,
determine the gender of the person.

Rules:
- Ukrainian female first names almost always end in -а or -я.
- Ukrainian male first names almost always end in a consonant or -о.
- Female patronymics end in -івна / -ївна / -овна.
- Male patronymics end in -ович / -йович / -євич.

Respond with exactly ONE word: male, female, or unknown.
No explanation. No punctuation. Just the single word.
"""


def claude_gender(name: str, notes: str) -> str:
    """Ask Claude Haiku for gender when the rule engine returns unknown."""
    user_msg = f"Name: {name}\nContext: {notes[:300] if notes else '(none)'}"
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=5,
            system=SYSTEM_PROMPT,
            messages=[{'role': 'user', 'content': user_msg}],
        )
        answer = resp.content[0].text.strip().lower()
        if answer in ('male', 'female', 'unknown'):
            return answer
        # Try to extract from longer reply
        for word in ('female', 'male'):
            if word in answer:
                return word
        return 'unknown'
    except Exception as e:
        print(f"    [Claude error] {e}", file=sys.stderr)
        return 'unknown'


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rerun', action='store_true',
                        help='Re-classify all entries, even those already done')
    args = parser.parse_args()

    # Load CSV
    print(f"Loading {CSV_PATH} …")
    with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    print(f"  {len(rows):,} rows loaded.")

    # Add gender column to fieldnames if not already present
    if 'gender' not in fieldnames:
        fieldnames.append('gender')
        for r in rows:
            r['gender'] = ''

    # Counters
    n_rule_male   = 0
    n_rule_female = 0
    n_rule_unk    = 0
    n_claude      = 0
    n_skipped     = 0

    for i, row in enumerate(rows, start=1):
        existing = row.get('gender', '').strip().lower()

        # Skip if already done (unless --rerun)
        if not args.rerun and existing in ('male', 'female', 'unknown'):
            n_skipped += 1
            continue

        name  = row.get('name', '').strip()
        notes = row.get('notes', '').strip()

        # Rule-based first
        gender = rule_gender(name)

        if gender == 'male':
            n_rule_male += 1
        elif gender == 'female':
            n_rule_female += 1
        else:
            n_rule_unk += 1
            # Claude fallback
            print(f"  [{i}/{len(rows)}] Claude: {name}")
            gender = claude_gender(name, notes)
            n_claude += 1
            time.sleep(DELAY)

        row['gender'] = gender

        # Progress every 500 rows
        if i % 500 == 0:
            print(f"  … {i:,}/{len(rows):,} processed "
                  f"(rule M={n_rule_male} F={n_rule_female} unk={n_rule_unk} "
                  f"Claude={n_claude} skip={n_skipped})")

    # Write back
    print(f"\nWriting updated CSV …")
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    total_done = n_rule_male + n_rule_female + n_claude
    print(f"\nDone.")
    print(f"  Rule-based male   : {n_rule_male:>6,}")
    print(f"  Rule-based female : {n_rule_female:>6,}")
    print(f"  Claude calls      : {n_claude:>6,}  (unknowns after rule engine)")
    print(f"  Previously done   : {n_skipped:>6,}  (skipped)")
    print(f"  Total classified  : {total_done:>6,}")

    # Gender distribution in analysable subset
    from collections import Counter
    VALID_MS = {'migrated', 'non_migrated', 'internal_transfer', 'deported'}
    analysable = [r for r in rows if r.get('migration_status', '').strip().lower() in VALID_MS]
    gc = Counter(r.get('gender', 'unknown').strip().lower() for r in analysable)
    print(f"\nGender distribution (analysable {len(analysable):,} entries):")
    for g, cnt in sorted(gc.items(), key=lambda x: -x[1]):
        pct = round(100 * cnt / len(analysable), 1) if analysable else 0
        print(f"  {g:<10}: {cnt:>5,}  ({pct}%)")


if __name__ == '__main__':
    main()
