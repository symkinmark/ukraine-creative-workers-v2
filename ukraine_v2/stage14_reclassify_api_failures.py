"""
stage14_reclassify_api_failures.py
Reclassifies the 135 entries that failed during Stage 12 B3 due to API auth errors.
Loads ANTHROPIC_API_KEY from .env before calling Claude.
"""

import csv, os, re, time, requests
import anthropic

PROJECT = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(PROJECT, 'esu_creative_workers_v2_6.csv')

# Load .env from project root
env_path = os.path.join(os.path.dirname(PROJECT), '.env')
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())
    print(f"Loaded .env from {env_path}")
else:
    print(f"WARNING: .env not found at {env_path}")

client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

# ---------------------------------------------------------------------------
# Fetch bio from ESU
# ---------------------------------------------------------------------------
SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'Mozilla/5.0 (research)'})

def fetch_bio(url, timeout=12):
    if not url or not url.startswith('http'):
        return ''
    try:
        resp = SESSION.get(url, timeout=timeout)
        resp.encoding = 'utf-8'
        html = resp.text
        clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.IGNORECASE)
        clean = re.sub(r'<style[^>]*>.*?</style>',  '', clean, flags=re.DOTALL|re.IGNORECASE)
        m = re.search(r'<div\b[^>]*\bitemprop=["\']articleBody["\'][^>]*>', clean, re.IGNORECASE)
        if m:
            start = m.end()
            end = clean.find('</article>', start)
            raw = clean[start:end] if end > start else clean[start:start+10000]
            text = re.sub(r'<[^>]+>', ' ', raw)
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text) > 80:
                return text[:3000]
        m2 = re.search(r'<meta[^>]+name=["\']citation_abstract["\'][^>]+content="([^"]+)"', html)
        if not m2:
            m2 = re.search(r'<meta[^>]+content="([^"]+)"[^>]+name=["\']citation_abstract["\']', html)
        if m2:
            return m2.group(1).strip()[:2000]
    except Exception as e:
        return f'[fetch error: {e}]'
    return ''

# ---------------------------------------------------------------------------
# Classification prompt (same as Stage 12)
# ---------------------------------------------------------------------------
MIGRATION_SYSTEM = """\
You are a research assistant classifying migration status of Ukrainian creative workers for an academic life expectancy study.

Classify each person into exactly one of these categories:

STEP 1 — CHECK FOR FORCED DISPLACEMENT FIRST:
If there is ANY evidence that Soviet authorities forcibly relocated this person — arrest, Gulag, labour camp, deportation order, special settler, exile imposed by NKVD/KGB/MGB — classify as DEPORTED.

STEP 2 — CHECK FOR VOLUNTARY EMIGRATION:
If the person voluntarily left and settled permanently outside Soviet/post-Soviet borders — classify as MIGRATED.

STEP 3 — CHECK FOR INTERNAL MOVEMENT:
If the person moved within the Soviet Union but never left its borders, AND there is no forced displacement — classify as INTERNAL_TRANSFER.

STEP 4 — DEFAULT:
If the person lived and died within Ukraine (or its pre-independence territory) with no significant migration — classify as NON_MIGRATED.

EXCLUSIONS (respond EXCLUDE_* if applies):
- EXCLUDE_PRE_SOVIET: died before 1921 and no significant Soviet-era activity
- EXCLUDE_NON_UKRAINIAN: not Ukrainian (different nationality entirely)
- EXCLUDE_BAD_DATES: birth/death dates clearly wrong or impossible

Respond with ONLY:
STATUS: [one of: MIGRATED, NON_MIGRATED, INTERNAL_TRANSFER, DEPORTED, EXCLUDE_PRE_SOVIET, EXCLUDE_NON_UKRAINIAN, EXCLUDE_BAD_DATES]
REASONING: [1-2 sentences explaining the key evidence]
"""

STATUS_MAP = {
    'MIGRATED': 'migrated',
    'NON_MIGRATED': 'non_migrated',
    'INTERNAL_TRANSFER': 'internal_transfer',
    'DEPORTED': 'deported',
    'EXCLUDE_PRE_SOVIET': 'excluded_pre_soviet',
    'EXCLUDE_NON_UKRAINIAN': 'excluded_non_ukrainian',
    'EXCLUDE_BAD_DATES': 'excluded_bad_dates',
}

def classify(name, bio, birth_year, death_year):
    if not bio or len(bio) < 30:
        return None, 'bio_too_short'
    prompt = f"""Name: {name}
Birth year: {birth_year}
Death year: {death_year}

Biography:
{bio}"""
    try:
        msg = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=200,
            system=MIGRATION_SYSTEM,
            messages=[{'role': 'user', 'content': prompt}],
        )
        text = msg.content[0].text.strip()
        m = re.search(r'STATUS:\s*(\w+)', text)
        r = re.search(r'REASONING:\s*(.+)', text, re.DOTALL)
        if m:
            raw_status = m.group(1).upper()
            status = STATUS_MAP.get(raw_status)
            reasoning = r.group(1).strip()[:400] if r else text[:200]
            return status, reasoning
        return None, f'parse_fail: {text[:100]}'
    except Exception as e:
        return None, f'api_error: {e}'

# ---------------------------------------------------------------------------
# Load CSV, find API-fail unknowns
# ---------------------------------------------------------------------------
with open(CSV_PATH, encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

targets = [
    r for r in rows
    if r.get('migration_status','') == 'unknown'
    and ('Could not resolve authentication' in r.get('migration_reasoning','')
         or 'credit balance is too low' in r.get('migration_reasoning',''))
]

print(f"Found {len(targets)} API-fail unknowns to reclassify.")
print("Starting classification (claude-haiku @ 0.3s/entry)...\n")

resolved = 0
still_failed = 0

for i, row in enumerate(targets):
    url = row.get('article_url','')
    name = row.get('name','')

    bio = fetch_bio(url)
    time.sleep(0.1)  # brief pause after fetch

    status, reasoning = classify(name, bio, row.get('birth_year',''), row.get('death_year',''))
    time.sleep(0.3)  # rate limit

    if status:
        row['migration_status'] = status
        row['migration_reasoning'] = f'S14-reclassified: {reasoning}'
        row['fix_applied'] = f'S14: API-fail reclassified → {status}'
        resolved += 1
        if (i + 1) % 10 == 0 or i < 3:
            print(f"  [{i+1}/{len(targets)}] {name[:40]} → {status}")
    else:
        row['migration_reasoning'] = f'S14-still-failed: {reasoning}'
        still_failed += 1
        if i < 3 or (i+1) % 20 == 0:
            print(f"  [{i+1}/{len(targets)}] {name[:40]} — FAILED: {reasoning[:60]}")

print(f"\nResolved: {resolved}/{len(targets)}  |  Still failed: {still_failed}")

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved → {CSV_PATH}")

# Quick status summary
from collections import Counter
newly_resolved = Counter()
for r in targets:
    if r['migration_status'] != 'unknown':
        newly_resolved[r['migration_status']] += 1
print("\nNewly classified breakdown:")
for k, v in sorted(newly_resolved.items(), key=lambda x: -x[1]):
    print(f"  {k:30s} {v}")
