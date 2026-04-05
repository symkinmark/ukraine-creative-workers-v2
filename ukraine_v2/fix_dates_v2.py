#!/usr/bin/env python3
"""
fix_dates_v2.py — V2.2 Date Recovery & Migration Re-classification
Ukrainian Creative Workers Dataset
Berdnyk & Symkin 2026

WHY THIS EXISTS
───────────────
The V2.1 scraper used a regex `\(([^)]{5,200})\)` that fails in two ways:
  1. Inner parentheses — Old/New Style dual dates like `14(26). 04. 1890` contain a `)`
     that terminates the outer regex match prematurely → birth_year and death_year both empty.
  2. Pseudonym prefixes — `(справж. – Real Name; 1887 – 1937)` the FIRST em-dash is after
     "справж.", so birth_part = "(справж." and birth_year = None.

Result: 8,971 entries were misclassified as "alive" (no death_year) even though the date is
right there in the notes field. Famous Executed Renaissance figures — Курбас, Зеров,
Підмогильний, Бабель, Вороний — were silently dropped from the analysis.

WHAT THIS SCRIPT DOES
──────────────────────
Phase A (zero tokens): Re-parses notes with a robust regex approach that bypasses both failures.
  - Extracts bio header by finding `) –` (profession separator), not by bracket-matching
  - Strips pseudonym/alias prefixes before splitting birth from death
  - Handles swapped dates (birth > death) using alternate year candidates
  - Flags fixed entries with dates_fixed=True
  - Writes esu_creative_workers_v2_2.csv (new file, v2_1 unchanged)

Phase B (zero tokens): Re-evaluates migration_status for affected rows.
  - excluded_pre_soviet with corrected death_year >= 1921 → reclassify candidate
  - alive with newly recovered death_year → reclassify candidate
  - Obvious repression signals (Сандормох, розстріляний) → direct classification
  - Marks needs_migration_reclassify=True for the rest

Phase C (Haiku, ~$0.50): Re-classifies the needs_migration_reclassify=True rows.
  Run with: --reclassify

USAGE
─────
  python3 ukraine_v2/fix_dates_v2.py              # Phase A + B only, dry stats
  python3 ukraine_v2/fix_dates_v2.py --write      # Phase A + B, write v2_2 CSV
  python3 ukraine_v2/fix_dates_v2.py --write --reclassify  # + Phase C (needs API key)
  python3 ukraine_v2/fix_dates_v2.py --check Курбас        # check one name
"""

import csv
import os
import re
import sys
import json
import time
import argparse
from collections import Counter
from dotenv import load_dotenv

_env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(_env_path)

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
IN_CSV  = os.path.join(os.path.dirname(__file__), 'esu_creative_workers_v2_1.csv')
OUT_CSV = os.path.join(os.path.dirname(__file__), 'esu_creative_workers_v2_2.csv')

YEAR_RE = re.compile(r'\b(1[5-9]\d{2}|20[0-2]\d)\b')

# ---------------------------------------------------------------------------
# PHASE A — DATE EXTRACTION
# ---------------------------------------------------------------------------

def extract_bio_header(notes: str) -> str:
    """
    Return the opening biographical parenthetical, e.g.:
      '(14(26). 04. 1890, Зіньків – 03. 11. 1937, Сандормох)'

    Strategy: find the FIRST `) –` or `) —` which marks where the bio section
    ends and the profession description begins. Everything up to and including
    that `)` is the bio header. This is robust to nested inner parens.
    """
    m = re.search(r'\)\s*[–—]\s', notes)
    if m:
        return notes[:m.start() + 1]
    # Fallback: take first 500 chars (handles very short entries)
    return notes[:500]


def clean_pseudonym_prefix(text: str) -> str:
    """
    Remove pseudonym/alias prefixes that appear before the actual dates:
      (справж. – Real Name; 1887, City – 1937, City)
      (справжнє – Full Real Name; DD.MM.YYYY, City – DD.MM.YYYY, City)
      (псевд.: Alias1, Alias2; DD.MM.YYYY, ...)
      (від YYYY — New Name; DD.MM.YYYY, ...)
    After stripping, the string starts directly at the birth date.
    """
    # Pattern: opening paren + prefix ending in semicolon
    text = re.sub(
        r'\((?:справж(?:нє)?\.?|псевд\.?:?)[^;]{0,120};\s*',
        '(', text
    )
    # "від YYYY" name change prefix
    text = re.sub(
        r'\(від \d{4}[^;]{0,60};\s*',
        '(', text
    )
    return text


def extract_years(notes: str):
    """
    Return (birth_year: int|None, death_year: int|None) from the notes field.

    Works on entries that failed the original scraper:
      - Dual dates: 14(26). 04. 1890  ← inner paren no longer breaks us
      - Pseudonym prefixes: stripped before em-dash split
      - Swapped dates: detected and corrected using alternate year candidates
    """
    if not notes:
        return None, None

    bio = clean_pseudonym_prefix(extract_bio_header(notes))

    # Find the birth–death separator (em-dash or en-dash with surrounding spaces)
    em = re.search(r'\s[–—]\s', bio)
    if not em:
        return None, None

    birth_part = bio[:em.start()]
    death_part = bio[em.start():]

    birth_yrs = [int(y) for y in YEAR_RE.findall(birth_part)]
    death_yrs = [int(y) for y in YEAR_RE.findall(death_part)]

    by = birth_yrs[0] if birth_yrs else None
    dy = death_yrs[0] if death_yrs else None

    # Swap detection: if birth > death, try alternate birth years
    # (happens with "за паспортом" or "за ін. даними" double-date entries)
    if by and dy and by > dy:
        for alt in birth_yrs[1:]:
            if alt < dy:
                by = alt
                break
        else:
            # Can't fix it — return as-is (will be flagged)
            pass

    return by, dy


# ---------------------------------------------------------------------------
# PHASE B — RE-EXCLUSION & SHORTCUT CLASSIFICATION
# ---------------------------------------------------------------------------

# Repression keywords that allow direct classification without Claude
EXECUTED_SIGNALS = re.compile(
    r'Сандормох|Сандармох|розстріляний|розстріляно|розстріл(?!ьн)|'
    r'вирок\s+розстрілу|страчений',
    re.IGNORECASE
)
GULAG_SIGNALS = re.compile(
    r'ГУЛАГу?|концтабір|конц\.\s*табір|виправно-трудовий\s+табір|'
    r'ВТТ\b|Карлаг|Соловки',
    re.IGNORECASE
)
DEPORTATION_SIGNALS = re.compile(
    r'заслання|засланн[іі]|спецпоселен|НКВС|МДБ|КДБ|арештований|'
    r'депортован|примусово\s+переселен',
    re.IGNORECASE
)
MIGRATION_SIGNALS = re.compile(
    r'\bУВАН\b|НТШ|Пролог|діаспор|емігрував|еміграці[іі]|'
    r'\bDPs?\b|displaced\s+person',
    re.IGNORECASE
)

def shortcut_classify(notes: str, death_location: str = ''):
    """
    Return (migration_status, death_cause, reasoning) for obvious cases.
    Returns (None, None, None) if no shortcut applies — Claude needed.
    """
    text = (notes or '') + ' ' + (death_location or '')

    if EXECUTED_SIGNALS.search(text):
        if DEPORTATION_SIGNALS.search(text):
            return 'deported', 'executed', 'Notes contain both deportation and execution signals.'
        return 'non_migrated', 'executed', 'Notes explicitly mention execution (розстріляний/Сандормох).'

    if GULAG_SIGNALS.search(text):
        return 'deported', 'gulag', 'Notes contain Gulag/labour camp signals.'

    if DEPORTATION_SIGNALS.search(text):
        return 'deported', 'repression_other', 'Notes contain Soviet deportation/repression signals.'

    if MIGRATION_SIGNALS.search(text):
        return 'migrated', None, 'Notes contain diaspora institution or emigration signals.'

    return None, None, None


# ---------------------------------------------------------------------------
# PHASE C — CLAUDE MIGRATION RE-CLASSIFICATION
# ---------------------------------------------------------------------------

MIGRATION_SYSTEM = """\
You are a research assistant classifying migration status of Ukrainian creative workers for an academic life expectancy study.

You must classify each person into exactly one of four categories. Read the biography carefully.

STEP 1 — CHECK FOR FORCED DISPLACEMENT FIRST (before anything else):
If there is ANY evidence that Soviet authorities forcibly relocated this person — arrest, Gulag, labour camp, deportation order, special settler status (спецпоселенець), exile (заслання) imposed by NKVD/KGB/MGB — classify as DEPORTED, regardless of destination.
Key Ukrainian signals: табір, ГУЛАГ, ув'язнення, заслання, спецпоселення, репресований, НКВС, МДБ, КДБ, розстріляний (executed).

STEP 2 — CLASSIFY:
- migrated: Left the Soviet sphere entirely. Settled in a non-Soviet country for substantial adult life.
- non_migrated: Remained in the Ukrainian SSR throughout working life. No emigration or forced displacement.
- internal_transfer: Voluntarily moved to another Soviet republic; career-motivated, no coercion.
- deported: Soviet state forcibly relocated. See Step 1.
- unknown: Genuinely insufficient information.

Reply ONLY in this exact JSON format, no extra text:
{"migration_status": "migrated" or "non_migrated" or "internal_transfer" or "deported" or "unknown", "reasoning": "one sentence max"}"""


def claude_classify_migration(client, row: dict) -> tuple[str, str]:
    """Call Claude Haiku for migration classification. Returns (status, reasoning)."""
    import anthropic as _anthro
    user_msg = (
        f"Name: {row.get('name','')}\n"
        f"Profession: {row.get('profession_raw','')}\n"
        f"Born: {row.get('birth_year','?')} — {row.get('birth_location','unknown')}\n"
        f"Died: {row.get('death_year','?')} — {row.get('death_location','unknown')}\n"
        f"Biography:\n{(row.get('notes','') or '')[:900]}"
    )
    try:
        resp = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=120,
            system=MIGRATION_SYSTEM,
            messages=[{'role': 'user', 'content': user_msg}],
        )
        text = resp.content[0].text.strip()
        # Strip markdown code fences if present
        text = re.sub(r'^```(?:json)?\s*|\s*```$', '', text, flags=re.MULTILINE).strip()
        data = json.loads(text)
        return data.get('migration_status', 'unknown'), data.get('reasoning', '')
    except Exception as e:
        return 'unknown', f'API error: {e}'


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='V2.2 date recovery and migration re-classification')
    parser.add_argument('--write',       action='store_true', help='Write output CSV (default: stats only)')
    parser.add_argument('--reclassify',  action='store_true', help='Phase C: run Claude re-classification')
    parser.add_argument('--check',       metavar='NAME',      help='Check a specific name and print result')
    args = parser.parse_args()

    # --check mode: quick diagnostic for a single name
    if args.check:
        print(f"Loading {IN_CSV} ...")
        with open(IN_CSV, encoding='utf-8-sig', newline='') as f:
            rows = list(csv.DictReader(f))
        target = args.check.lower()
        matches = [r for r in rows if target in r.get('name','').lower()]
        if not matches:
            print(f"No match for '{args.check}'")
            return
        for r in matches:
            by, dy = extract_years(r.get('notes',''))
            print(f"\nName:              {r['name']}")
            print(f"CSV birth_year:    {r.get('birth_year','')!r}")
            print(f"CSV death_year:    {r.get('death_year','')!r}")
            print(f"Parsed birth_year: {by}")
            print(f"Parsed death_year: {dy}")
            print(f"migration_status:  {r.get('migration_status','')}")
            bio = r.get('notes','')
            print(f"Notes (first 200): {bio[:200]}")
            ms, dc, rsn = shortcut_classify(r.get('notes',''), r.get('death_location',''))
            print(f"Shortcut classif.: {ms} / {dc} → {rsn}")
        return

    # Load CSV
    print(f"Loading {IN_CSV} ...")
    with open(IN_CSV, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    print(f"  {len(rows):,} rows loaded.")

    # Add new columns if missing
    for col in ('dates_fixed', 'needs_migration_reclassify'):
        if col not in fieldnames:
            fieldnames.append(col)
            for r in rows:
                r[col] = ''

    # ── Phase A: Date recovery ───────────────────────────────────────────────
    print("\nPhase A — Date recovery ...")

    stats = Counter()
    reclassify_rows = []

    for row in rows:
        notes = row.get('notes', '') or ''
        cur_by = row.get('birth_year', '').strip()
        cur_dy = row.get('death_year', '').strip()

        new_by, new_dy = extract_years(notes)

        changed = False

        # Fill empty birth_year
        if not cur_by and new_by:
            row['birth_year'] = str(new_by)
            changed = True
            stats['birth_filled'] += 1

        # Fill empty death_year
        if not cur_dy and new_dy:
            row['death_year'] = str(new_dy)
            changed = True
            stats['death_filled'] += 1

        # Fix swapped dates: if current death_year looks like a birth year
        # and the notes give us a plausible death year that's later
        if cur_by and cur_dy:
            try:
                cb, cd = int(cur_by), int(cur_dy)
                if cb > cd and new_by and new_dy and new_by < new_dy:
                    row['birth_year'] = str(new_by)
                    row['death_year'] = str(new_dy)
                    changed = True
                    stats['swap_fixed'] += 1
            except ValueError:
                pass

        # Handle the Курбас case: birth_year is empty, death_year contains birth year
        # Detected when: birth empty, death filled, but notes show a later death year
        if not cur_by and cur_dy and new_by and new_dy:
            try:
                cd = int(cur_dy)
                if cd == new_by and new_dy > new_by:
                    # death_year field contains the birth year → fix both
                    row['birth_year'] = str(new_by)
                    row['death_year'] = str(new_dy)
                    changed = True
                    stats['scraper_swap_fixed'] += 1
            except ValueError:
                pass

        row['dates_fixed'] = 'True' if changed else ''

    # ── Phase B: Re-exclusion logic ──────────────────────────────────────────
    print("Phase B — Re-exclusion and shortcut classification ...")

    for row in rows:
        ms = row.get('migration_status', '').strip().lower()
        dy_str = row.get('death_year', '').strip()
        by_str = row.get('birth_year', '').strip()
        dates_fixed = row.get('dates_fixed', '') == 'True'

        if not dates_fixed:
            continue

        try:
            dy = int(dy_str) if dy_str else None
            by = int(by_str) if by_str else None
        except ValueError:
            dy = by = None

        # Was "excluded_pre_soviet" but death year was wrong (scraper put birth year in death field)
        if ms == 'excluded_pre_soviet' and dy and dy >= 1921:
            stats['pre_soviet_corrected'] += 1
            # Try shortcut first
            sc_status, sc_cause, sc_reason = shortcut_classify(
                row.get('notes', ''), row.get('death_location', '')
            )
            if sc_status:
                row['migration_status']    = sc_status
                row['migration_reasoning'] = sc_reason
                if sc_cause and not row.get('death_cause'):
                    row['death_cause']           = sc_cause
                    row['death_cause_reasoning'] = sc_reason
                row['needs_migration_reclassify'] = 'shortcut'
                stats['shortcut_classified'] += 1
            else:
                row['migration_status']           = 'unknown'
                row['migration_reasoning']        = 'Date corrected — was excluded_pre_soviet due to scraper error.'
                row['needs_migration_reclassify'] = 'True'
                reclassify_rows.append(row)

        # Was "alive" (no death year) and now has a death year
        elif ms == 'alive' and dy:
            stats['alive_recovered'] += 1
            if by and dy and (dy - by) > 110:
                # Age > 110 is implausible — likely still a parse error
                row['needs_migration_reclassify'] = 'implausible_age'
                stats['implausible_age'] += 1
                continue

            sc_status, sc_cause, sc_reason = shortcut_classify(
                row.get('notes', ''), row.get('death_location', '')
            )
            if sc_status:
                row['migration_status']    = sc_status
                row['migration_reasoning'] = sc_reason
                if sc_cause and not row.get('death_cause'):
                    row['death_cause']           = sc_cause
                    row['death_cause_reasoning'] = sc_reason
                row['needs_migration_reclassify'] = 'shortcut'
                stats['shortcut_classified'] += 1
            else:
                row['migration_status']           = 'unknown'
                row['migration_reasoning']        = 'Date recovered — was alive due to scraper error.'
                row['needs_migration_reclassify'] = 'True'
                reclassify_rows.append(row)

    print(f"\nPhase A+B statistics:")
    print(f"  Birth year filled in:       {stats['birth_filled']:>6,}")
    print(f"  Death year filled in:       {stats['death_filled']:>6,}")
    print(f"  Swap fixed (birth>death):   {stats['swap_fixed']:>6,}")
    print(f"  Scraper swap fixed (Курбас-style): {stats['scraper_swap_fixed']:>3,}")
    print(f"  pre-Soviet exclusion corrected: {stats['pre_soviet_corrected']:>3,}")
    print(f"  Alive → recovered:          {stats['alive_recovered']:>6,}")
    print(f"  Shortcut classified:        {stats['shortcut_classified']:>6,}")
    print(f"  Need Claude re-classification: {len(reclassify_rows):>4,}")
    print(f"  Implausible age (skipped):  {stats['implausible_age']:>6,}")

    # Quick sanity checks on named figures
    print("\nSanity check — named Executed Renaissance figures:")
    targets = ['Курбас', 'Зеров', 'Підмогильний', 'Бабель', 'Вороний', 'Поліщук', 'Косинка']
    for t in targets:
        matches = [r for r in rows if t in r.get('name', '')]
        for r in matches:
            print(f"  {r['name']:<50} birth={r['birth_year']:<6} death={r['death_year']:<6} "
                  f"status={r['migration_status']}")

    # ── Phase C: Claude re-classification ────────────────────────────────────
    if args.reclassify and reclassify_rows:
        api_key = os.environ.get('ANTHROPIC_API_KEY', '')
        if not api_key:
            print("\n[Phase C] ANTHROPIC_API_KEY not found — skipping.")
        else:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            total_c = len(reclassify_rows)
            print(f"\nPhase C — Claude re-classification ({total_c:,} entries, ~${total_c*0.0003:.2f}) ...")

            for i, row in enumerate(reclassify_rows, start=1):
                status, reasoning = claude_classify_migration(client, row)
                row['migration_status']           = status
                row['migration_reasoning']        = reasoning
                row['needs_migration_reclassify'] = 'done'

                if i % 100 == 0 or i == total_c:
                    dist = Counter(r['migration_status'] for r in reclassify_rows[:i])
                    print(f"  [{i:>5}/{total_c}] {dict(dist.most_common(4))}")

                time.sleep(0.30)

            print(f"  Claude re-classification complete.")

    # ── Write output ──────────────────────────────────────────────────────────
    if not args.write:
        print("\n(Dry run — pass --write to save the corrected CSV)")
        return

    print(f"\nWriting {OUT_CSV} ...")
    with open(OUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Final analysable count
    VALID_MS = {'migrated', 'non_migrated', 'internal_transfer', 'deported'}
    analysable = [
        r for r in rows
        if r.get('migration_status','').strip().lower() in VALID_MS
        and r.get('birth_year','').strip().isdigit()
        and r.get('death_year','').strip().isdigit()
    ]
    print(f"\nDone.")
    print(f"  Total rows:        {len(rows):>7,}")
    print(f"  Analysable (V2.2): {len(analysable):>7,}  (was 6,106 in V2.1)")
    ms_dist = Counter(r['migration_status'] for r in analysable)
    for ms, n in ms_dist.most_common():
        print(f"    {ms:<25}: {n:>5,}")


if __name__ == '__main__':
    main()
