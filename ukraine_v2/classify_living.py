#!/usr/bin/env python3
"""
cox-rc Stage 2: Classify migration status for 6,563 living individuals.

Uses ThreadPoolExecutor for parallel API calls (30 workers).
Haiku first pass, Sonnet retry for unknowns.
Saves progress every 100 entries — safe to re-run if interrupted.

Input:  data/living_individuals_for_classification.csv
Output: data/living_individuals_classified.csv

Usage: python3 ukraine_v2/classify_living.py
"""

import csv
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import anthropic

INPUT_CSV  = os.path.join(os.path.dirname(__file__), 'data', 'living_individuals_for_classification.csv')
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), 'data', 'living_individuals_classified.csv')

WORKERS    = 30
MODEL_HAIKU  = 'claude-haiku-4-5-20251001'
MODEL_SONNET = 'claude-sonnet-4-6'

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

NOTE: This person is still alive as of 2026. Classify based on their life trajectory as described in the biography.

Reply ONLY in this exact JSON format, no extra text:
{"migration_status": "migrated" or "non_migrated" or "internal_transfer" or "deported" or "unknown", "reasoning": "one sentence max"}"""

MIGRATION_DEEP_SYSTEM = """\
You are a research assistant. A previous analysis returned 'unknown' for this Ukrainian creative worker's migration status. Look harder.

STEP 1 — FORCED DISPLACEMENT CHECK (mandatory, do this first):
Any of these signals = DEPORTED: arrest, Gulag, labour camp, exile order, special settler, NKVD/KGB action resulting in relocation.
Ukrainian: табір, ГУЛАГ, ув'язнення, заслання, спецпоселення, репресований, розстріляний.

STEP 2 — GEOGRAPHY CLUES:
- Currently lives or works in Paris, New York, Munich, London, Buenos Aires, Toronto, Rome, Vienna → likely MIGRATED
- Works in Ukraine, Russia, or any former Soviet republic → NON_MIGRATED (unless Step 1 applies)
- Born in Galicia/western Ukraine + currently abroad → very likely MIGRATED
- Career based in Moscow/other former Soviet city, no coercion signals → INTERNAL_TRANSFER

STEP 3 — DIASPORA SIGNALS:
Membership in УВАН, НТШ, УВАН у США, Пролог, diaspora press publication → MIGRATED

Use 'unknown' only as a last resort if truly no clues exist after all of the above.

Reply ONLY in this exact JSON format:
{"migration_status": "migrated" or "non_migrated" or "internal_transfer" or "deported" or "unknown", "reasoning": "one sentence max"}"""

# Thread-safe counter
_lock = threading.Lock()
_counter = {'done': 0, 'total': 0, 'errors': 0}


def parse_json_response(text):
    text = text.strip()
    m = re.search(r'\{.*\}', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    return {}


def classify_one(client, row):
    """Classify a single row. Returns (row_id, migration_status, reasoning)."""
    bio = (row.get('bio_text') or '')[:1200]
    user_msg = (
        f"Name: {row['name']}\n"
        f"Profession: {row.get('profession', '')}\n"
        f"Born: {row.get('birth_year', '?')} — {row.get('birth_city', 'unknown')}\n"
        f"Biography:\n{bio or 'Not available'}"
    )

    # Haiku first pass — with rate-limit retry
    for attempt in range(4):
        try:
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
                return row['id'], status, f'[haiku] {reason}'
            break  # got a definitive 'unknown' — move to sonnet
        except anthropic.RateLimitError:
            wait = 2 ** attempt
            time.sleep(wait)
        except Exception as e:
            reason = f'haiku_error: {e}'
            break

    # Sonnet deep retry
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=MODEL_SONNET,
                max_tokens=150,
                system=MIGRATION_DEEP_SYSTEM,
                messages=[{'role': 'user', 'content': user_msg}],
            )
            data = parse_json_response(resp.content[0].text)
            status = data.get('migration_status', 'unknown')
            reason = data.get('reasoning', '')
            return row['id'], status, f'[sonnet-retry] {reason}'
        except anthropic.RateLimitError:
            wait = 2 ** attempt
            time.sleep(wait)
        except Exception as e:
            return row['id'], 'unknown', f'sonnet_error: {e}'

    return row['id'], 'unknown', 'all_models_failed'


def load_already_done():
    """Load any previously saved results (for resumability)."""
    done = {}
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                if row.get('migration_status') and row['migration_status'] != '':
                    done[row['id']] = row
    return done


def save_results(rows_by_id, input_rows):
    """Write full output CSV (all input rows + results so far)."""
    fieldnames = list(input_rows[0].keys()) + ['migration_status', 'migration_reasoning']
    tmp_path = OUTPUT_CSV + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in input_rows:
            out = dict(row)
            if row['id'] in rows_by_id:
                out['migration_status'] = rows_by_id[row['id']]['migration_status']
                out['migration_reasoning'] = rows_by_id[row['id']]['migration_reasoning']
            else:
                out['migration_status'] = ''
                out['migration_reasoning'] = ''
            writer.writerow(out)
    os.replace(tmp_path, OUTPUT_CSV)


def main():
    # Load input
    with open(INPUT_CSV, 'r', encoding='utf-8-sig') as f:
        input_rows = list(csv.DictReader(f))
    total = len(input_rows)
    print(f'Loaded {total} living individuals for classification')

    # Check for prior progress
    done = load_already_done()
    remaining = [r for r in input_rows if r['id'] not in done]
    print(f'Already classified: {len(done)}')
    print(f'Remaining: {len(remaining)}')

    if not remaining:
        print('All done! Nothing to classify.')
    else:
        _counter['total'] = len(remaining)
        _counter['done'] = 0

        client = anthropic.Anthropic()
        results = dict(done)  # start with already-done
        last_save = 0

        print(f'\nStarting classification with {WORKERS} parallel workers...')
        print('Progress: ', end='', flush=True)

        with ThreadPoolExecutor(max_workers=WORKERS) as executor:
            futures = {executor.submit(classify_one, client, row): row for row in remaining}

            for future in as_completed(futures):
                row_id, status, reasoning = future.result()
                results[row_id] = {'migration_status': status, 'migration_reasoning': reasoning}

                with _lock:
                    _counter['done'] += 1
                    n = _counter['done']
                    if n % 100 == 0 or n == _counter['total']:
                        # Save checkpoint
                        save_results(results, input_rows)
                        last_save = n
                        pct = n / _counter['total'] * 100
                        print(f'{n}/{_counter["total"]} ({pct:.0f}%)... ', end='', flush=True)

        # Final save
        if last_save < len(remaining):
            save_results(results, input_rows)

        print('\nDone!')

    # Final stats
    with open(OUTPUT_CSV, 'r', encoding='utf-8-sig') as f:
        classified = list(csv.DictReader(f))

    from collections import Counter
    dist = Counter(r['migration_status'] for r in classified if r['migration_status'])
    print(f'\n=== STAGE 2 RESULTS ===')
    print(f'Total classified: {len([r for r in classified if r["migration_status"]])}')
    print(f'\nDistribution:')
    for k, v in sorted(dist.items(), key=lambda x: -x[1]):
        pct = v / len(classified) * 100
        print(f'  {k:<20} {v:>5}  ({pct:.1f}%)')

    # Comparison with dead cohort
    print(f'\n=== COMPARISON: LIVING vs DEAD COHORT ===')
    dead_dist = {
        'non_migrated': 6205,
        'migrated': 1313,
        'internal_transfer': 1174,
        'deported': 197,
    }
    dead_total = sum(dead_dist.values())
    living_total = len([r for r in classified if r['migration_status'] in dead_dist])
    print(f'{"Group":<22} {"Dead %":>8} {"Living %":>10}')
    print('-' * 44)
    for g in ['non_migrated', 'migrated', 'internal_transfer', 'deported']:
        dead_pct = dead_dist.get(g, 0) / dead_total * 100
        living_pct = dist.get(g, 0) / living_total * 100 if living_total else 0
        print(f'  {g:<20} {dead_pct:>7.1f}%  {living_pct:>8.1f}%')

    # Red flag checks
    print(f'\n=== RED FLAG CHECKS ===')
    deported_pct = dist.get('deported', 0) / len(classified) * 100
    unknown_pct = (dist.get('unknown', 0) + dist.get('', 0)) / len(classified) * 100
    print(f'Deported %: {deported_pct:.1f}% (flag if >5%)')
    print(f'Unknown/error %: {unknown_pct:.1f}% (flag if >20%)')
    if deported_pct > 5:
        print('  *** RED FLAG: >5% deported — living deportees from 1930s-40s implausible ***')
    if unknown_pct > 20:
        print('  *** RED FLAG: >20% unknown ***')
    if deported_pct <= 5 and unknown_pct <= 20:
        print('  All clear — no red flags.')


if __name__ == '__main__':
    main()
