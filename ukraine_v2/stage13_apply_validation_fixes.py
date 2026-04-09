"""
stage13_apply_validation_fixes.py
Applies corrections from the 200-entry validation review to esu_creative_workers_v2_6.csv.

Two categories of fixes:
  A) 8 specific individual corrections from reviewer (by article_url)
  B) Systematic fix: any entry in analysis groups with death_year < 1921 → excluded_pre_soviet
     (classifier was incorrectly including pre-Soviet era people in the analysis cohort)
"""

import csv, os

PROJECT = os.path.dirname(os.path.abspath(__file__))
CSV_IN  = os.path.join(PROJECT, 'esu_creative_workers_v2_6.csv')
CSV_OUT = os.path.join(PROJECT, 'esu_creative_workers_v2_6.csv')   # overwrite in-place

ANALYSIS_STATUSES = {'migrated', 'non_migrated', 'internal_transfer', 'deported'}

# ---------------------------------------------------------------------------
# A) Specific individual corrections from validation review
# ---------------------------------------------------------------------------
# Each entry: url → dict of fields to set (and optional expected old values for safety)
SPECIFIC_FIXES = {
    # idx 9: Гринюк Юрій — persecuted/deported by USSR 1937, not Galicia pre-annexation
    'https://esu.com.ua/article-31695': {
        'migration_status': 'deported',
        'fix_applied': 'B5: validation review — reclassified excluded_galicia_pre_annexation→deported (died 1937, persecution confirmed)',
    },
    # idx 120: Збіглей Йосиф — born in diaspora, should count as migrated
    'https://esu.com.ua/article-16490': {
        'migration_status': 'migrated',
        'fix_applied': 'B5: validation review — reclassified non_migrated→migrated (born in migration)',
    },
    # idx 190: Прибік Йосиф — death year stored as 1855 (birth-as-death bug), actually died 1937 Odessa
    'https://esu.com.ua/article-879497': {
        'death_year': '1937',
        'migration_status': 'non_migrated',
        'fix_applied': 'B5: validation review — death_year corrected 1855→1937 (died Odessa), status excluded_pre_soviet→non_migrated',
    },
    # idx 192: Кендзерський Ігнатій — died in Lublin Poland, should be migrated
    'https://esu.com.ua/article-11745': {
        'migration_status': 'migrated',
        'fix_applied': 'B5: validation review — reclassified non_migrated→migrated (died in Lublin, Poland)',
    },
    # idx 82: Кошиць Ніна — death year 1892 wrong (birth-as-death bug), actually died 1965 California
    'https://esu.com.ua/article-1727': {
        'death_year': '1965',
        'migration_status': 'migrated',
        'fix_applied': 'B5: validation review — death_year corrected 1892→1965 (died California 1965), status excluded_bad_dates→migrated',
    },
    # idx 124: Лещук Осип — born in migration, should be migrated (currently unknown)
    'https://esu.com.ua/article-54553': {
        'migration_status': 'migrated',
        'fix_applied': 'B5: validation review — reclassified unknown→migrated (born in migration)',
    },
}
# Note: idx 112 (Аббакумов, died 1919) and idx 180 (Морськой, died 1914) are handled
# by the systematic pre-Soviet fix below.

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
with open(CSV_IN, encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

print(f"Loaded {len(rows)} rows.")

# ---------------------------------------------------------------------------
# Apply specific fixes
# ---------------------------------------------------------------------------
specific_applied = 0
for row in rows:
    url = row.get('article_url', '').strip()
    if url in SPECIFIC_FIXES:
        fix = SPECIFIC_FIXES[url]
        old_status = row.get('migration_status', '')
        for field, val in fix.items():
            row[field] = val
        specific_applied += 1
        print(f"  [SPECIFIC] {row.get('name','?')} — {old_status} → {row.get('migration_status','?')}")

print(f"\nSpecific fixes applied: {specific_applied}/{len(SPECIFIC_FIXES)}")

# ---------------------------------------------------------------------------
# Systematic fix: analysis group with death_year < 1921 → excluded_pre_soviet
# Skip entries already handled by specific fixes above
# ---------------------------------------------------------------------------
SPECIFIC_URLS = set(SPECIFIC_FIXES.keys())
pre_soviet_fixed = 0
pre_soviet_list  = []

def safe_int(val):
    try:
        return int(float(str(val).strip()))
    except:
        return None

for row in rows:
    url    = row.get('article_url', '').strip()
    status = row.get('migration_status', '').strip().lower()
    dy     = safe_int(row.get('death_year', ''))

    if url in SPECIFIC_URLS:
        continue  # already handled
    if status not in ANALYSIS_STATUSES:
        continue
    if dy is None or dy >= 1921:
        continue

    # Pre-Soviet death in analysis group — move to excluded_pre_soviet
    pre_soviet_list.append({
        'name': row.get('name', ''),
        'url':  url,
        'old_status': status,
        'death_year': dy,
    })
    row['migration_status'] = 'excluded_pre_soviet'
    row['fix_applied'] = f'B5: systematic — death_year {dy} < 1921, moved from {status} to excluded_pre_soviet'
    pre_soviet_fixed += 1

print(f"\nSystematic pre-Soviet fix: {pre_soviet_fixed} entries moved to excluded_pre_soviet")
print("Sample of moved entries:")
for e in pre_soviet_list[:20]:
    print(f"  {e['name']} | died {e['death_year']} | was {e['old_status']}")
if len(pre_soviet_list) > 20:
    print(f"  ... and {len(pre_soviet_list) - 20} more")

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
with open(CSV_OUT, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"\nSaved → {CSV_OUT}")

# ---------------------------------------------------------------------------
# Summary stats after fixes
# ---------------------------------------------------------------------------
from collections import Counter
status_counts = Counter(r.get('migration_status','') for r in rows)
print("\nStatus counts after fixes:")
for k, v in sorted(status_counts.items(), key=lambda x: -x[1]):
    print(f"  {k:40s} {v:6d}")

analysable = [r for r in rows if r.get('migration_status','') in ANALYSIS_STATUSES
              and safe_int(r.get('birth_year')) and safe_int(r.get('death_year'))]
print(f"\nAnalysable dead cohort: {len(analysable)}")

by_group = Counter(r['migration_status'] for r in analysable)
for k, v in sorted(by_group.items(), key=lambda x: -x[1]):
    ages = [safe_int(r['death_year']) - safe_int(r['birth_year']) for r in analysable
            if r['migration_status'] == k]
    mean_age = sum(ages)/len(ages) if ages else 0
    print(f"  {k:25s} n={v:5d}  mean_age={mean_age:.2f}")

# Primary gap
mig = [safe_int(r['death_year']) - safe_int(r['birth_year'])
       for r in analysable if r['migration_status'] == 'migrated']
nm  = [safe_int(r['death_year']) - safe_int(r['birth_year'])
       for r in analysable if r['migration_status'] == 'non_migrated']
gap = sum(mig)/len(mig) - sum(nm)/len(nm)
print(f"\nPrimary gap: {sum(mig)/len(mig):.2f} (mig) - {sum(nm)/len(nm):.2f} (nm) = {gap:.2f} yrs")
print(f"Total fixes applied: {specific_applied + pre_soviet_fixed}")
