#!/usr/bin/env python3
"""
V2.3 Phase 5 — Re-classify 196 unknown-status entries that have death years.

These were left as 'unknown' in V2.2 due to:
  - API errors (JSON parse failures, timeouts)
  - Genuinely ambiguous bios

Strategy:
  1. Filter rows: migration_status == 'unknown' AND death_year is set
  2. Fetch full ESU article bio (same as claude_review.py does)
  3. Try Haiku first, then Sonnet deep retry if still unknown
  4. Update migration_status and migration_reasoning in place
  5. Saves after every 10 entries (incremental — safe to re-run)

Reads/writes: esu_creative_workers_v2_2.csv (in-place)
Cost estimate: 196 entries × ~$0.001 = ~$0.20 total

Usage: python3 reclassify_unknowns.py
"""

import csv
import os
import sys
import time
import json
import re
import requests
from bs4 import BeautifulSoup
import anthropic

CSV_PATH = os.path.join(os.path.dirname(__file__), 'esu_creative_workers_v2_3.csv')
DELAY_FETCH = 0.6
DELAY_CLAUDE = 0.3
MODEL_HAIKU = 'claude-haiku-4-5-20251001'
MODEL_SONNET = 'claude-sonnet-4-6'

FIELDNAMES = [
    'name', 'birth_year', 'death_year',
    'birth_location', 'death_location',
    'profession_raw', 'flag_non_ukrainian', 'flag_needs_claude_review',
    'article_url', 'notes',
    'is_ukrainian', 'ukrainian_reasoning',
    'migration_status', 'migration_reasoning',
    'gender', 'death_cause', 'death_cause_reasoning',
    'dates_fixed', 'needs_migration_reclassify',
]

MIGRATION_SYSTEM = """\
You are a research assistant classifying migration status of Ukrainian creative workers for an academic life expectancy study.

You must classify each person into exactly one of four categories. Read the biography carefully.

STEP 1 — CHECK FOR FORCED DISPLACEMENT FIRST (before anything else):
If there is ANY evidence that Soviet authorities forcibly relocated this person — arrest, Gulag, labour camp, deportation order, special settler status (спецпоселенець), exile (заслання) imposed by NKVD/KGB/MGB — classify as DEPORTED, regardless of destination.
Key Ukrainian signals: табір, ГУЛАГ, ув'язнення, заслання, спецпоселення, репресований, НКВС, МДБ, КДБ, розстріляний (executed).

STEP 2 — CLASSIFY:

- migrated: Left the Soviet sphere entirely. Settled in a non-Soviet country (Western Europe, North America, South America, non-Soviet Asia) for a substantial part of adult life. Diaspora institution membership (УВАН, НТШ, УВАН у США) or diaspora press publication confirms this. Moving to Soviet Russia does NOT qualify.

- non_migrated: Remained in the Ukrainian SSR throughout working life. No evidence of emigration or forced displacement.

- internal_transfer: Voluntarily moved from Ukrainian SSR to another Soviet republic (Russia, Belarus, Central Asia, etc.) and based career there. No evidence of coercion. Career-motivated or personal choice.

- deported: Soviet state forcibly relocated this person. See Step 1. Destination does not matter — Siberia, Kazakhstan, or a Donbas labour camp all qualify.

- unknown: Genuinely insufficient information even after careful reading.

Reply ONLY in this exact JSON format, no extra text:
{"migration_status": "migrated" or "non_migrated" or "internal_transfer" or "deported" or "unknown", "reasoning": "one sentence max"}"""

MIGRATION_DEEP_SYSTEM = """\
You are a research assistant. A previous analysis returned 'unknown' for this Ukrainian creative worker's migration status. Look harder.

STEP 1 — FORCED DISPLACEMENT CHECK (mandatory, do this first):
Any of these signals = DEPORTED: arrest, Gulag, labour camp, exile order, special settler, NKVD/KGB action resulting in relocation.
Ukrainian: табір, ГУЛАГ, ув'язнення, заслання, спецпоселення, репресований, розстріляний.

STEP 2 — GEOGRAPHY CLUES:
- Died in Paris, New York, Munich, London, Buenos Aires, Toronto, Rome, Prague (post-1948), Vienna → likely MIGRATED
- Died in Ukraine, Russia, or any Soviet republic → NON_MIGRATED (unless Step 1 applies)
- Born in Galicia/western Ukraine + died abroad → very likely MIGRATED (post-WWII emigration wave)
- Lived career in Moscow/Leningrad/other Soviet city, no coercion signals → INTERNAL_TRANSFER

STEP 3 — DIASPORA SIGNALS:
Membership in УВАН, НТШ, УВАН у США, Пролог, diaspora press publication → MIGRATED

Use 'unknown' only as a last resort if truly no clues exist after all of the above.

Reply ONLY in this exact JSON format:
{"migration_status": "migrated" or "non_migrated" or "internal_transfer" or "deported" or "unknown", "reasoning": "one sentence max"}"""


def fetch_article_bio(url, session):
    try:
        time.sleep(DELAY_FETCH)
        r = session.get(url, timeout=20)
        if r.status_code != 200:
            return ''
        soup = BeautifulSoup(r.text, 'html.parser')
        article_div = (
            soup.find('div', class_=re.compile(r'article[-_]?(text|body|content)', re.I))
            or soup.find('div', class_=re.compile(r'content', re.I))
        )
        if article_div:
            return article_div.get_text(' ', strip=True)[:1500]
        return ' '.join(p.get_text(' ', strip=True) for p in soup.find_all('p')[:12])[:1500]
    except Exception:
        return ''


def parse_json_response(text):
    text = text.strip()
    m = re.search(r'\{.*\}', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    return {}


def classify_migration(client, row, bio):
    user_msg = (
        f"Name: {row['name']}\n"
        f"Profession: {row['profession_raw']}\n"
        f"Born: {row['birth_year'] or '?'} — {row['birth_location'] or 'unknown'}\n"
        f"Died: {row['death_year'] or '?'} — {row['death_location'] or 'unknown'}\n"
        f"Biography:\n{bio[:900] if bio else row.get('notes','')[:400] or 'Not available'}"
    )
    # Haiku first pass
    try:
        time.sleep(DELAY_CLAUDE)
        resp = client.messages.create(
            model=MODEL_HAIKU,
            max_tokens=120,
            system=MIGRATION_SYSTEM,
            messages=[{'role': 'user', 'content': user_msg}],
        )
        data = parse_json_response(resp.content[0].text)
        status = data.get('migration_status', 'unknown')
        reason = data.get('reasoning', '')
        if status != 'unknown':
            return status, f'[haiku] {reason}'
    except Exception as e:
        reason = f'haiku_error: {e}'

    # Sonnet deep retry
    try:
        time.sleep(DELAY_CLAUDE)
        resp = client.messages.create(
            model=MODEL_SONNET,
            max_tokens=150,
            system=MIGRATION_DEEP_SYSTEM,
            messages=[{'role': 'user', 'content': user_msg}],
        )
        data = parse_json_response(resp.content[0].text)
        status = data.get('migration_status', 'unknown')
        reason = data.get('reasoning', '')
        return status, f'[sonnet-retry] {reason}'
    except Exception as e:
        return 'unknown', f'sonnet_error: {e}'


def load_rows():
    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_rows(rows):
    with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = load_rows()
    targets = [
        (i, r) for i, r in enumerate(rows)
        if r.get('migration_status', '') == 'unknown' and r.get('death_year', '').strip()
    ]
    print(f'Targets: {len(targets)} unknown-status entries with death years')

    client = anthropic.Anthropic()
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept-Language': 'uk,en;q=0.9',
    })

    reclassified = 0
    still_unknown = 0

    for batch_start in range(0, len(targets), 10):
        batch = targets[batch_start:batch_start + 10]
        for i, (row_idx, row) in enumerate(batch):
            n = batch_start + i + 1
            print(f'[{n}/{len(targets)}] {row["name"]} ({row["birth_year"]}-{row["death_year"]})', end=' ... ')
            sys.stdout.flush()

            # Fetch full article bio
            bio = fetch_article_bio(row.get('article_url', ''), session)

            # Classify
            status, reason = classify_migration(client, row, bio)

            rows[row_idx]['migration_status'] = status
            rows[row_idx]['migration_reasoning'] = reason

            if status != 'unknown':
                reclassified += 1
                print(f'→ {status}')
            else:
                still_unknown += 1
                print(f'→ still unknown ({reason[:60]})')

        # Save after every batch of 10
        save_rows(rows)
        print(f'  [saved batch {batch_start // 10 + 1}]')

    print(f'\nDone. Reclassified: {reclassified}, Still unknown: {still_unknown}')


if __name__ == '__main__':
    main()
