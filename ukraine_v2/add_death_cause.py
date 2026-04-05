#!/usr/bin/env python3
"""
add_death_cause.py — Death Cause Classification Pipeline
Ukrainian Creative Workers V2.1
Berdnyk & Symkin 2026

Adds a `death_cause` column to esu_creative_workers_v2_2.csv by asking
Claude Haiku to classify the cause of death for each entry from the
biography text available in the `notes` field. If notes are too short
(< 150 chars), the full ESU article is fetched live.

DEATH CAUSE CATEGORIES
──────────────────────
  executed          — Shot or executed by Soviet/Nazi authorities
  gulag             — Died in a labour camp (Gulag, concentration camp)
  exile             — Died in exile/deportation (survived camp, died far from home)
  suicide           — Self-inflicted death (including under pressure of arrest)
  wwii_combat       — Died fighting in WWII
  wwii_occupation   — Killed during WWII occupation (not combat)
  repression_other  — Clearly a victim of Soviet repression, exact cause unclear
  natural           — Died of illness or old age (no evidence of repression)
  accident          — Accident, unrelated to repression
  unknown           — Insufficient information to classify

COST ESTIMATE (Haiku, April 2026 pricing $0.25/M input, $1.25/M output)
────────────────────────────────────────────────────────────────────────
  Analysable entries (birth+death+migration):         ~6,106
  Avg input tokens per entry (notes + prompt):          ~380
  Avg output tokens per entry (cause + 1-line reason):   ~30
  ─────────────────────────────────────────────────────────
  Total input tokens:  6,106 × 380 = ~2.32M → $0.58
  Total output tokens: 6,106 × 30  = ~0.18M → $0.23
  Total Claude cost:                           ~$0.81

  Entries needing live ESU fetch (notes < 150 chars): ~20% = ~1,200
  Fetch overhead: 1,200 × 0.5s = ~10 min extra

RUNTIME ESTIMATE
────────────────
  Claude calls (0.3s delay):  6,106 × 0.3s  = ~30 min
  ESU fetches when needed:   ~1,200 × 0.5s  = ~10 min
  Total expected runtime:                    ~40–50 min

Run:
    python3 ukraine_v2/add_death_cause.py             # analysable only (default)
    python3 ukraine_v2/add_death_cause.py --all       # all rows with death year
    python3 ukraine_v2/add_death_cause.py --rerun     # reclassify everything
    python3 ukraine_v2/add_death_cause.py --dry-run   # show 10 samples, no writes
"""

import csv
import os
import sys
import re
import time
import argparse
import requests
from bs4 import BeautifulSoup
import anthropic
from dotenv import load_dotenv

# Load API key from .env in project root
_env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(_env_path)

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
CSV_PATH = os.path.join(os.path.dirname(__file__), 'esu_creative_workers_v2_2.csv')
MODEL    = 'claude-haiku-4-5-20251001'
DELAY    = 0.30   # seconds between Claude calls
FETCH_DELAY = 0.50  # seconds between ESU fetches
MIN_NOTES_LEN = 150  # below this, fetch full article text

VALID_CAUSES = {
    'executed', 'gulag', 'exile', 'suicide',
    'wwii_combat', 'wwii_occupation', 'repression_other',
    'natural', 'accident', 'unknown',
}

VALID_MS = {'migrated', 'non_migrated', 'internal_transfer', 'deported'}

_api_key = os.environ.get('ANTHROPIC_API_KEY', '')
if not _api_key:
    sys.exit('Error: ANTHROPIC_API_KEY not found in .env')
client = anthropic.Anthropic(api_key=_api_key)


# ---------------------------------------------------------------------------
# SYSTEM PROMPT
# ---------------------------------------------------------------------------
SYSTEM = """\
You are a historian classifying causes of death for Ukrainian creative workers
from their biographical encyclopedia entries.

Classify the cause of death into EXACTLY ONE of these categories:
  executed          — Shot or executed by Soviet or Nazi authorities
  gulag             — Died inside a labour camp (Gulag, concentration camp, prison camp)
  exile             — Died in exile or deportation (survived the camp/sentence but died
                      while still in exile, far from home, or shortly after return)
  suicide           — Suicide (including when driven to it by imminent arrest)
  wwii_combat       — Killed in combat during WWII (fighting at the front)
  wwii_occupation   — Killed during WWII occupation by occupying forces (not combat)
  repression_other  — Clearly a victim of Soviet repression but exact cause is unclear
  natural           — Died of illness, disease, or old age, no evidence of repression
  accident          — Accident, unrelated to any repression
  unknown           — Not enough information to classify

KEY SIGNALS:
  Ukrainian: розстріляний/розстріл = executed | табір/ГУЛАГу/концтабір = gulag
  засланні/заслання = exile | самогубство = suicide | фронт/бій/загинув на війні = wwii_combat
  помер від хвороби/природна смерть = natural

Respond in this exact format — two lines, nothing else:
CAUSE: <one of the ten categories above>
REASON: <one sentence in English explaining why>
"""


# ---------------------------------------------------------------------------
# ESU ARTICLE FETCHER
# ---------------------------------------------------------------------------
def fetch_article_text(url: str) -> str:
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (research; Ukrainian Creative Workers V2)'}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        for sel in ['.article-body', '.entry-content', 'article', '.content', 'main']:
            el = soup.select_one(sel)
            if el:
                text = el.get_text(separator=' ', strip=True)
                if len(text) > 100:
                    return text[:4000]
        paras = soup.find_all('p')
        text = ' '.join(p.get_text(strip=True) for p in paras if len(p.get_text(strip=True)) > 30)
        return text[:4000] if text else ''
    except Exception as e:
        return ''


# ---------------------------------------------------------------------------
# CLAUDE CLASSIFICATION
# ---------------------------------------------------------------------------
def classify_death_cause(name: str, notes: str, death_year: str,
                          migration_status: str) -> tuple[str, str]:
    """Return (cause, reason). Falls back to ('unknown', 'API error') on failure."""
    user_msg = (
        f"Name: {name}\n"
        f"Death year: {death_year or 'unknown'}\n"
        f"Migration status: {migration_status}\n"
        f"Biography text:\n{notes[:3500] if notes else '(no text available)'}"
    )
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=80,
            system=SYSTEM,
            messages=[{'role': 'user', 'content': user_msg}],
        )
        raw = resp.content[0].text.strip()
        cause  = 'unknown'
        reason = raw

        for line in raw.splitlines():
            if line.upper().startswith('CAUSE:'):
                c = line.split(':', 1)[1].strip().lower()
                if c in VALID_CAUSES:
                    cause = c
            elif line.upper().startswith('REASON:'):
                reason = line.split(':', 1)[1].strip()
        return cause, reason

    except Exception as e:
        return 'unknown', f'API error: {e}'


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Death cause classification pipeline')
    parser.add_argument('--all',     action='store_true',
                        help='Classify all rows with a death year (not just analysable)')
    parser.add_argument('--rerun',   action='store_true',
                        help='Reclassify entries already done')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print 10 sample classifications, do not write CSV')
    args = parser.parse_args()

    # Load CSV
    print(f"Loading {CSV_PATH} …")
    with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    print(f"  {len(rows):,} rows loaded.")

    # Add new columns if missing
    for col in ('death_cause', 'death_cause_reasoning'):
        if col not in fieldnames:
            fieldnames.append(col)
            for r in rows:
                r[col] = ''

    # Decide which rows to process
    def should_process(r):
        dy = r.get('death_year', '').strip()
        if not dy or not dy.isdigit():
            return False
        ms = r.get('migration_status', '').strip().lower()
        if not args.all and ms not in VALID_MS:
            return False
        existing = r.get('death_cause', '').strip().lower()
        if not args.rerun and existing in VALID_CAUSES:
            return False
        return True

    to_process = [r for r in rows if should_process(r)]
    total = len(to_process)
    print(f"  To classify: {total:,} entries")

    if args.dry_run:
        print("\n--- DRY RUN: 10 samples ---")
        sample = to_process[:10]
    else:
        sample = to_process

    # Counters
    n_notes_only = 0
    n_fetched    = 0
    n_done       = 0
    n_skipped    = 0
    from collections import Counter
    cause_counter = Counter()

    for i, row in enumerate(sample, start=1):
        name  = row.get('name', '').strip()
        notes = row.get('notes', '').strip()
        url   = row.get('article_url', '').strip()
        dy    = row.get('death_year', '').strip()
        ms    = row.get('migration_status', '').strip().lower()

        # Decide whether to fetch full article text
        bio_text = notes
        if len(notes) < MIN_NOTES_LEN and url:
            bio_text = fetch_article_text(url)
            n_fetched += 1
            time.sleep(FETCH_DELAY)
            if not bio_text:
                bio_text = notes  # fall back to notes if fetch fails
        else:
            n_notes_only += 1

        cause, reason = classify_death_cause(name, bio_text, dy, ms)
        cause_counter[cause] += 1

        row['death_cause']           = cause
        row['death_cause_reasoning'] = reason
        n_done += 1

        if args.dry_run:
            print(f"\n#{i} {name} (died {dy}, {ms})")
            print(f"   Notes preview: {notes[:120]}…")
            print(f"   → CAUSE: {cause}")
            print(f"   → REASON: {reason}")
        elif i % 200 == 0 or i == total:
            print(f"  [{i:>5}/{total}] notes_only={n_notes_only} "
                  f"fetched={n_fetched}  dist={dict(cause_counter.most_common(5))}")

        time.sleep(DELAY)

    if args.dry_run:
        print("\n--- DRY RUN complete — no CSV written ---")
        return

    # Write back
    print(f"\nWriting updated CSV …")
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDone. {n_done:,} entries classified.")
    print("\nDeath cause distribution:")
    for cause, cnt in cause_counter.most_common():
        pct = round(100 * cnt / n_done, 1) if n_done else 0
        print(f"  {cause:<22}: {cnt:>5,}  ({pct}%)")


if __name__ == '__main__':
    main()
