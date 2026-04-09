"""
rebuild_extended_cox_dataset.py
Rebuilds data/esu_extended_for_cox.csv from the current V2.6 dead cohort
+ the existing living_individuals_cleaned.csv.

This is needed whenever the main dataset (esu_creative_workers_v2_6.csv) changes,
to keep the Cox PH models in sync.

Usage: python3 ukraine_v2/rebuild_extended_cox_dataset.py
"""

import csv
import os

HERE    = os.path.dirname(os.path.abspath(__file__))
MAIN    = os.path.join(HERE, 'esu_creative_workers_v2_6.csv')
LIVING  = os.path.join(HERE, 'data', 'living_individuals_cleaned.csv')
OUT     = os.path.join(HERE, 'data', 'esu_extended_for_cox.csv')

ANALYSIS_STATUSES = {'migrated', 'non_migrated', 'internal_transfer', 'deported'}

# ---------------------------------------------------------------------------
# Load main V2.6 dead cohort
# ---------------------------------------------------------------------------
with open(MAIN, encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

dead_rows = []
skipped = 0
for r in rows:
    ms = r.get('migration_status', '').strip()
    if ms not in ANALYSIS_STATUSES:
        skipped += 1
        continue
    try:
        by = int(float(r['birth_year']))
        dy = int(float(r['death_year']))
    except (ValueError, KeyError):
        skipped += 1
        continue
    duration = dy - by
    if duration < 0:
        skipped += 1
        continue

    gender = r.get('gender', '').strip() or 'unknown'
    dead_rows.append({
        'name':                      r.get('name', ''),
        'birth_year':                by,
        'death_year':                dy,
        'migration_status':          ms,
        'profession_raw':            r.get('profession_raw', ''),
        'birth_location':            r.get('birth_location', ''),
        'gender':                    gender,
        'duration':                  duration,
        'event_observed':            1,
        'cohort':                    'dead',
        'implausibly_alive':         False,
        'likely_post_soviet_emigrant': False,
    })

print(f"Dead cohort: {len(dead_rows)} rows loaded ({skipped} skipped)")

# ---------------------------------------------------------------------------
# Load living individuals
# ---------------------------------------------------------------------------
with open(LIVING, encoding='utf-8-sig') as f:
    living_raw = list(csv.DictReader(f))

ANALYSIS_STATUSES_LIVING = {'migrated', 'non_migrated', 'internal_transfer', 'deported'}
CENSOR_YEAR = 2026

living_rows = []
liv_skipped = 0
for r in living_raw:
    ms = r.get('migration_status', '').strip()
    if ms not in ANALYSIS_STATUSES_LIVING:
        liv_skipped += 1
        continue
    try:
        by = int(float(r['birth_year']))
    except (ValueError, KeyError):
        liv_skipped += 1
        continue

    implausibly_alive = str(r.get('implausibly_alive', 'False')).strip().lower() in ('true', '1', 'yes')
    likely_pse        = str(r.get('likely_post_soviet_emigrant', 'False')).strip().lower() in ('true', '1', 'yes')

    # Implausibly alive: treat as event (dead) at duration=80
    if implausibly_alive:
        duration       = 80
        event_observed = 1
    else:
        duration       = CENSOR_YEAR - by
        event_observed = 0

    profession = r.get('profession', '') or r.get('profession_raw', '')
    birth_loc  = r.get('birth_city', '') or r.get('birth_location', '')

    living_rows.append({
        'name':                      r.get('name', ''),
        'birth_year':                by,
        'death_year':                '',
        'migration_status':          ms,
        'profession_raw':            profession,
        'birth_location':            birth_loc,
        'gender':                    r.get('gender', 'unknown'),
        'duration':                  duration,
        'event_observed':            event_observed,
        'cohort':                    'censored',
        'implausibly_alive':         implausibly_alive,
        'likely_post_soviet_emigrant': likely_pse,
    })

print(f"Living cohort: {len(living_rows)} rows loaded ({liv_skipped} skipped)")

# ---------------------------------------------------------------------------
# Combine and write
# ---------------------------------------------------------------------------
all_rows = dead_rows + living_rows

FIELDNAMES = [
    'name', 'birth_year', 'death_year', 'migration_status',
    'profession_raw', 'birth_location', 'gender',
    'duration', 'event_observed', 'cohort',
    'implausibly_alive', 'likely_post_soviet_emigrant',
]

with open(OUT, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"\nExtended dataset written → {OUT}")
print(f"Total rows: {len(all_rows)} (dead={len(dead_rows)}, censored={len(living_rows)})")

# Group summary
from collections import Counter
ms_counts = Counter(r['migration_status'] for r in all_rows)
for ms, n in sorted(ms_counts.items(), key=lambda x: -x[1]):
    print(f"  {ms:25s} {n}")
