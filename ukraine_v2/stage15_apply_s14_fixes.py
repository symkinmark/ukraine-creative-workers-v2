"""
stage15_apply_s14_fixes.py
Applies corrections from the Stage 14 manual validation review.
6 corrections identified by human reviewer.
"""

import csv, os
from collections import Counter

PROJECT = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(PROJECT, 'esu_creative_workers_v2_6.csv')

FIXES = {
    # Глушаниця Павло — bad data, unknown death date
    'https://esu.com.ua/article-30518': {
        'migration_status': 'excluded_bad_dates',
        'fix_applied': 'S15: S14 review — migrated→excluded_bad_dates (bad data, unknown death date)',
    },
    # Збіржховська Антоніна — Galicia pre-annexation
    'https://esu.com.ua/article-16491': {
        'migration_status': 'excluded_galicia_pre_annexation',
        'fix_applied': 'S15: S14 review — migrated→excluded_galicia_pre_annexation (Galicia, died pre-Soviet annexation)',
    },
    # Злоцький Феодосій Антонович — Galicia pre-annexation
    'https://esu.com.ua/article-16344': {
        'migration_status': 'excluded_galicia_pre_annexation',
        'fix_applied': 'S15: S14 review — non_migrated→excluded_galicia_pre_annexation (Galicia, died pre-Soviet annexation)',
    },
    # Камінський Віктор — Galicia pre-annexation
    'https://esu.com.ua/article-10895': {
        'migration_status': 'excluded_galicia_pre_annexation',
        'fix_applied': 'S15: S14 review — non_migrated→excluded_galicia_pre_annexation (Galicia, died pre-Soviet annexation)',
    },
    # Конрад Джозеф (Joseph Conrad) — pre-Soviet emigrant, died 1924
    'https://esu.com.ua/article-4547': {
        'migration_status': 'excluded_pre_soviet',
        'fix_applied': 'S15: S14 review — migrated→excluded_pre_soviet (emigrated pre-Soviet era, died 1924)',
    },
    # Лефлер Чарльз-Мартін (Charles Martin Loeffler) — not Ukrainian
    'https://esu.com.ua/article-54491': {
        'migration_status': 'excluded_non_ukrainian',
        'fix_applied': 'S15: S14 review — migrated→excluded_non_ukrainian (not Ukrainian)',
    },
}

with open(CSV_PATH, encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

applied = 0
for row in rows:
    url = row.get('article_url', '').strip()
    if url in FIXES:
        fix = FIXES[url]
        old = row.get('migration_status', '')
        for field, val in fix.items():
            row[field] = val
        applied += 1
        print(f"  FIXED: {row.get('name','?')[:40]} | {old} → {row['migration_status']}")

print(f"\nApplied {applied}/{len(FIXES)} fixes")

with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved → {CSV_PATH}")

# Summary
ANALYSIS = {'migrated', 'non_migrated', 'internal_transfer', 'deported'}
analysable = [r for r in rows if r.get('migration_status','') in ANALYSIS]
counts = Counter(r['migration_status'] for r in analysable)
print(f"\nAnalysable cohort after S15: {len(analysable)}")
for k, v in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {k:25s} {v}")
