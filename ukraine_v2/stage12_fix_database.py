"""
stage12_fix_database.py
V2.6 Database Fixes — produces esu_creative_workers_v2_6.csv

Steps:
  B1 — Hardcoded patch: 8 specific validation errors
  B2 — Birth-year-as-death-year: re-fetch 102 ESU articles, correct dates
  B3 — API-error unknowns: re-classify 57 entries via Claude Haiku
  B4 — Audit is_ukrainian for analysis groups
  B5 — Attempt to resolve genuine unknowns via full bio re-fetch

Each step is idempotent — re-run safely; adds fix_applied column for audit trail.
"""

import os
import re
import sys
import time
import json
import requests
import pandas as pd
import anthropic

PROJECT   = os.path.dirname(os.path.abspath(__file__))
CSV_IN    = os.path.join(PROJECT, 'esu_creative_workers_v2_3.csv')
CSV_OUT   = os.path.join(PROJECT, 'esu_creative_workers_v2_6.csv')
LOG_FILE  = os.path.join(PROJECT, 'stage12_fix_log.txt')

DELAY     = 0.5   # seconds between ESU HTTP requests
MODEL     = 'claude-haiku-4-5-20251001'

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
df = pd.read_csv(CSV_IN)
print(f"Loaded {len(df):,} rows")

if 'fix_applied' not in df.columns:
    df['fix_applied'] = ''

log_lines = []
def log(msg):
    print(msg)
    log_lines.append(msg)

# ---------------------------------------------------------------------------
# HTTP session for ESU fetches
# ---------------------------------------------------------------------------
session = requests.Session()
session.headers.update({
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'uk,en;q=0.9',
})

def fetch_article(url, retries=3):
    """Fetch ESU article HTML. Returns text or None."""
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=20)
            if r.status_code == 200:
                return r.text
            return None
        except requests.RequestException:
            if attempt < retries - 1:
                time.sleep(3)
    return None

# Ukrainian month abbreviations → month number (for year extraction context)
UK_MONTHS = {
    'січ': 1, 'лют': 2, 'берез': 3, 'квіт': 4, 'трав': 5, 'черв': 6,
    'лип': 7, 'серп': 8, 'верес': 9, 'жовт': 10, 'листоп': 11, 'груд': 12,
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12,
}

def parse_year_from_date_field(text):
    """Extract 4-digit year from a date string like '13 берез. 1991' or '1975'."""
    m = re.search(r'\b(1[6-9]\d{2}|20[0-2]\d)\b', str(text))
    return int(m.group(1)) if m else None

def extract_dates_from_html(html, name):
    """
    Parse birth_year and death_year from full ESU article HTML.
    Looks for:
      1. Structured <td>Дата народження:</td><td>...</td> fields
      2. Structured fields in text: "Дата народження: DD MMMM YYYY"
      3. Parenthetical at start of article body: (DD.MM.YYYY, loc — DD.MM.YYYY, loc)
    Returns (birth_year, death_year, bio_text) where years may be None.
    """
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Extract full text
    bio_text = soup.get_text(' ', strip=True)

    birth_year = None
    death_year  = None

    # Strategy 1: Look for "Дата народження:" and "Дата смерті:" patterns
    birth_m = re.search(r'Дата\s+народження\s*:?\s*([^\n]{1,50})', bio_text)
    death_m  = re.search(r'Дата\s+смерті\s*:?\s*([^\n]{1,50})', bio_text)

    if birth_m:
        birth_year = parse_year_from_date_field(birth_m.group(1))
    if death_m:
        death_year = parse_year_from_date_field(death_m.group(1))

    # Strategy 2: Main article content parenthetical
    # ESU format: (DD. MM. YYYY, location — DD. MM. YYYY, location)
    # The article title/name is in caps, then the parenthetical follows
    if not (birth_year and death_year):
        # Look for pattern: (MM. DD. YYYY ... – ... YYYY)
        paren_m = re.search(
            r'\(\s*(?:[^()]{0,80}?;?\s*)?'
            r'(\d{1,2}\.\s*\d{1,2}\.\s*(1[6-9]\d{2}|20[0-2]\d)'
            r'|(?:(?:берез|лют|квіт|трав|черв|лип|серп|верес|жовт|листоп|груд|січ)\.\s*)?(1[6-9]\d{2}|20[0-2]\d))'
            r'[^—–]*[—–][^)]*?(1[6-9]\d{2}|20[0-2]\d)',
            bio_text
        )
        if paren_m:
            years = re.findall(r'\b(1[6-9]\d{2}|20[0-2]\d)\b', paren_m.group(0))
            if len(years) >= 2:
                if not birth_year:
                    birth_year = int(years[0])
                if not death_year:
                    death_year = int(years[-1])
            elif len(years) == 1 and not birth_year:
                birth_year = int(years[0])

    # Strategy 3: Fallback — find all years in the first 500 chars of bio
    if not (birth_year and death_year):
        # Look for the article header with the parenthetical right after the caps name
        # Slice to first 600 chars after finding the name
        name_upper = name.upper()
        idx = bio_text.find(name_upper)
        if idx >= 0:
            snippet = bio_text[idx:idx+600]
            all_years = [int(y) for y in re.findall(r'\b(1[6-9]\d{2}|20[0-2]\d)\b', snippet)]
            # Filter: years in plausible birth range (1700–1950) and death range (1700–2026)
            plausible = [y for y in all_years if 1700 <= y <= 2026]
            if len(plausible) >= 2 and not birth_year:
                birth_year = plausible[0]
            if len(plausible) >= 2 and not death_year:
                death_year = plausible[-1] if plausible[-1] != birth_year else None

    return birth_year, death_year, bio_text[:3000]

# ---------------------------------------------------------------------------
# Claude client
# ---------------------------------------------------------------------------
try:
    client = anthropic.Anthropic()
    _claude_available = True
except Exception:
    _claude_available = False
    log("WARNING: Claude API not available — B3 step will be skipped")

MIGRATION_SYSTEM = """\
You are a research assistant classifying migration status of Ukrainian creative workers for an academic life expectancy study.

You must classify each person into exactly one of these categories. Read the biography carefully.

STEP 1 — CHECK FOR FORCED DISPLACEMENT FIRST:
If there is ANY evidence that Soviet authorities forcibly relocated this person — arrest, Gulag, labour camp, deportation order, special settler, exile imposed by NKVD/KGB/MGB — classify as DEPORTED.
Ukrainian signals: табір, ГУЛАГ, ув'язнення, заслання, спецпоселення, репресований, розстріляний.

STEP 2 — CLASSIFY:
- migrated: Left Soviet sphere entirely; settled in non-Soviet country for substantial adult life.
- non_migrated: Remained in Ukrainian SSR throughout working life; no emigration or forced displacement.
- internal_transfer: Voluntarily moved from Ukrainian SSR to another Soviet republic (Russia, Central Asia, etc.). No coercion.
- deported: Soviet state forcibly relocated this person (see Step 1).
- unknown: Genuinely insufficient information even after careful reading.
- excluded_non_ukrainian: Person has no genuine connection to Ukraine — foreign national who happened to be included in ESU but lived entire career outside Soviet Ukraine.

Reply ONLY in this exact JSON format:
{"migration_status": "migrated|non_migrated|internal_transfer|deported|unknown|excluded_non_ukrainian", "reasoning": "one sentence max"}"""

def classify_via_claude(name, bio_text, birth_year, death_year):
    """Run Claude Haiku migration classification. Returns (status, reasoning)."""
    if not _claude_available:
        return 'unknown', 'Claude API not available'
    prompt = (
        f"Name: {name}\n"
        f"Birth year: {birth_year or 'unknown'}\n"
        f"Death year: {death_year or 'unknown'}\n"
        f"Biography:\n{bio_text[:2000]}"
    )
    try:
        msg = client.messages.create(
            model=MODEL,
            max_tokens=200,
            system=MIGRATION_SYSTEM,
            messages=[{'role': 'user', 'content': prompt}]
        )
        text = msg.content[0].text.strip()
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            result = json.loads(m.group(0))
            return result.get('migration_status', 'unknown'), result.get('reasoning', '')
        return 'unknown', f'parse_fail: {text[:100]}'
    except Exception as e:
        return 'unknown', f'api_error: {str(e)[:100]}'

# ---------------------------------------------------------------------------
# B1 — Hardcoded patch: specific validation errors
# ---------------------------------------------------------------------------
log("\n" + "="*60)
log("STEP B1: Applying hardcoded patches (8 specific entries)")
log("="*60)

PATCHES = [
    # (name_partial, field: value, ...)
    {
        'name_contains': 'Керч Оксана',
        'death_year': 1991,
        'birth_year': 1911,
        'migration_status': 'migrated',
        'migration_reasoning': 'B1-patch: Born 1911 Przemysl; left Ukraine 1944 to Austria then France, Argentina, USA; died Philadelphia 1991. Birth year was incorrectly stored as death year.',
    },
    {
        'name_contains': 'Антонович Катерина',
        'death_year': 1975,
        'birth_year': 1884,
        'migration_status': 'migrated',
        'migration_reasoning': 'B1-patch: Born 1884 Kharkiv; emigrated; died Winnipeg, Canada 22 Feb 1975. Birth year was incorrectly stored as death year.',
    },
    {
        'name_contains': 'Містраль Ґабрієла',
        'migration_status': 'excluded_non_ukrainian',
        'migration_reasoning': 'B1-patch: Gabriela Mistral (1889–1957) is the Chilean Nobel laureate; no Ukrainian residence or connection. Wrongly included in ESU dataset.',
    },
    {
        'name_contains': 'Петровичева Людмила',
        'death_year': 1971,
        'migration_status': 'non_migrated',
        'migration_reasoning': 'B1-patch: Died 1971 (not 1882 as stored). Birth year was stored as death year. No emigration evidence; classified non_migrated.',
    },
    {
        'name_contains': 'Черняхівська Вероніка',
        'death_year': 1938,
        'migration_status': 'non_migrated',
        'migration_reasoning': 'B1-patch: Veronika Cherniakhivska died 1938 (within Soviet period, not pre-Soviet). Birth year was stored as death year. No emigration evidence; non_migrated.',
    },
    {
        'name_contains': 'Бойченко Микола Романович',
        'migration_status': 'excluded_bad_dates',
        'migration_reasoning': 'B1-patch: Conflicting death records (Kyiv 1946 vs Budapest 1947); dates unreliable. Birth year (1896) was stored as death year.',
    },
    {
        'name_contains': 'Кудравець Анатоль',
        'migration_status': 'excluded_non_ukrainian',
        'migration_reasoning': 'B1-patch: Anatol Kudravets born Mogilev region, Belarus; entire career in Belarus (Minsk). No Ukrainian connection. Should be excluded_non_ukrainian.',
    },
    {
        'name_contains': 'Кейс Віталій',
        'migration_status': 'migrated',
        'migration_reasoning': 'B1-patch: Bio confirms "1951 родина емігрувала до США". Taught at Long Island University and Rutgers (NJ) 1970–2005. Correct status is migrated, not unknown.',
    },
]

b1_count = 0
for patch in PATCHES:
    mask = df['name'].str.contains(patch['name_contains'], na=False)
    matches = df[mask]
    if len(matches) == 0:
        log(f"  WARNING: No match for '{patch['name_contains']}'")
        continue
    idx = matches.index[0]
    changes = []
    for field, value in patch.items():
        if field == 'name_contains':
            continue
        old_val = df.at[idx, field] if field in df.columns else 'N/A'
        df.at[idx, field] = value
        changes.append(f"{field}: {old_val!r} → {value!r}")
    tag = df.at[idx, 'fix_applied']
    df.at[idx, 'fix_applied'] = (tag + '; ' if tag else '') + 'B1'
    log(f"  Patched [{idx}] {df.at[idx, 'name']}: {'; '.join(changes)}")
    b1_count += 1

log(f"B1 complete: {b1_count} entries patched")

# ---------------------------------------------------------------------------
# B2 — Fix birth-year-as-death-year (102 excluded_pre_soviet suspects)
# ---------------------------------------------------------------------------
log("\n" + "="*60)
log("STEP B2: Re-fetching ESU articles for birth-year-as-death-year suspects")
log("="*60)

def first_year_in_notes(notes):
    if pd.isna(notes):
        return None
    m = re.search(r'\b(1[6-9]\d{2})\b', str(notes))
    return int(m.group(1)) if m else None

df['_first_notes'] = df['notes'].apply(first_year_in_notes)
df['_death_n'] = pd.to_numeric(df['death_year'], errors='coerce')
df['_birth_n'] = pd.to_numeric(df['birth_year'], errors='coerce')

suspects_mask = (
    (df['migration_status'] == 'excluded_pre_soviet') &
    (df['_birth_n'].isna()) &
    (df['_death_n'].notna()) &
    (df['_first_notes'] == df['_death_n']) &
    (~df['fix_applied'].str.contains('B1', na=False))  # skip already B1-patched
)
suspects = df[suspects_mask].copy()
log(f"Found {len(suspects)} suspects to re-fetch")

b2_corrected = 0
b2_reclassified = 0
b2_failed = 0

for i, (idx, row) in enumerate(suspects.iterrows()):
    url = row.get('article_url', '')
    if pd.isna(url) or not str(url).startswith('http'):
        log(f"  [{i+1}/{len(suspects)}] {row['name']}: no URL, skipping")
        b2_failed += 1
        continue

    html = fetch_article(str(url))
    time.sleep(DELAY)

    if not html:
        log(f"  [{i+1}/{len(suspects)}] {row['name']}: fetch failed")
        b2_failed += 1
        continue

    birth_yr, death_yr, bio_text = extract_dates_from_html(html, str(row['name']))

    if not death_yr:
        log(f"  [{i+1}/{len(suspects)}] {row['name']}: could not extract death year from HTML")
        b2_failed += 1
        continue

    # Correct the birth year regardless
    if birth_yr and pd.isna(row['_birth_n']):
        df.at[idx, 'birth_year'] = birth_yr

    old_death = row['death_year']

    if death_yr < 1921:
        # Genuinely pre-Soviet — keep excluded_pre_soviet but correct the year
        df.at[idx, 'death_year'] = death_yr
        tag = df.at[idx, 'fix_applied']
        df.at[idx, 'fix_applied'] = (tag + '; ' if tag else '') + 'B2-date-corrected'
        b2_corrected += 1
        log(f"  [{i+1}/{len(suspects)}] {row['name']}: death_year {old_death}→{death_yr} (still pre-Soviet)")
    else:
        # Post-1921 — correct year AND reclassify via Claude
        df.at[idx, 'death_year'] = death_yr
        if birth_yr:
            df.at[idx, 'birth_year'] = birth_yr

        status, reasoning = classify_via_claude(
            str(row['name']), bio_text, birth_yr, death_yr
        )
        df.at[idx, 'migration_status']    = status
        df.at[idx, 'migration_reasoning'] = f'B2-reclassified (death_year corrected {old_death}→{death_yr}): {reasoning}'
        tag = df.at[idx, 'fix_applied']
        df.at[idx, 'fix_applied'] = (tag + '; ' if tag else '') + f'B2-reclassified-to-{status}'
        b2_reclassified += 1
        log(f"  [{i+1}/{len(suspects)}] {row['name']}: death_year {old_death}→{death_yr}, reclassified to {status}")

    # Save progress every 10 entries
    if (i + 1) % 10 == 0:
        df.to_csv(CSV_OUT, index=False)
        log(f"  Progress saved ({i+1}/{len(suspects)})")

log(f"B2 complete: {b2_corrected} date-corrected (still pre-Soviet), "
    f"{b2_reclassified} reclassified, {b2_failed} failed/skipped")

# ---------------------------------------------------------------------------
# B3 — Reclassify API-error unknowns (57 entries)
# ---------------------------------------------------------------------------
log("\n" + "="*60)
log("STEP B3: Reclassifying API-error unknowns via Claude")
log("="*60)

api_err_mask = df['migration_reasoning'].str.contains(
    'credit balance is too low|sonnet_error.*Error code: 400', na=False, regex=True
)
api_err_entries = df[api_err_mask].copy()
log(f"Found {len(api_err_entries)} API-error entries to reclassify")

b3_done = 0
b3_failed = 0

for i, (idx, row) in enumerate(api_err_entries.iterrows()):
    url = row.get('article_url', '')
    if pd.isna(url) or not str(url).startswith('http'):
        b3_failed += 1
        continue

    html = fetch_article(str(url))
    time.sleep(DELAY)

    if not html:
        log(f"  [{i+1}/{len(api_err_entries)}] {row['name']}: fetch failed")
        b3_failed += 1
        continue

    birth_yr, death_yr, bio_text = extract_dates_from_html(html, str(row['name']))

    # Update dates if we got better info
    if birth_yr and pd.isna(row.get('_birth_n')):
        df.at[idx, 'birth_year'] = birth_yr
    if death_yr and pd.isna(row.get('_death_n')):
        df.at[idx, 'death_year'] = death_yr

    status, reasoning = classify_via_claude(
        str(row['name']), bio_text,
        birth_yr or row.get('birth_year'),
        death_yr or row.get('death_year')
    )

    df.at[idx, 'migration_status']    = status
    df.at[idx, 'migration_reasoning'] = f'B3-reclassified: {reasoning}'
    tag = df.at[idx, 'fix_applied']
    df.at[idx, 'fix_applied'] = (tag + '; ' if tag else '') + f'B3-to-{status}'
    b3_done += 1
    log(f"  [{i+1}/{len(api_err_entries)}] {row['name']}: → {status}")

    if (i + 1) % 10 == 0:
        df.to_csv(CSV_OUT, index=False)
        log(f"  Progress saved ({i+1}/{len(api_err_entries)})")

log(f"B3 complete: {b3_done} reclassified, {b3_failed} failed")

# ---------------------------------------------------------------------------
# B4 — Audit is_ukrainian vs flag_non_ukrainian
# ---------------------------------------------------------------------------
log("\n" + "="*60)
log("STEP B4: Auditing is_ukrainian / flag_non_ukrainian conflicts")
log("="*60)

ANALYSIS_STATUSES = {'migrated', 'non_migrated', 'internal_transfer', 'deported', 'unknown'}
analysis_df = df[df['migration_status'].isin(ANALYSIS_STATUSES)]

if 'flag_non_ukrainian' in df.columns:
    flagged = analysis_df[
        analysis_df['flag_non_ukrainian'].astype(str).str.lower().isin(['true', '1', 'yes'])
    ]
    log(f"  Entries in analysis groups with flag_non_ukrainian=True: {len(flagged)}")
    for _, row in flagged.iterrows():
        log(f"    {row['name']} | status={row['migration_status']} | is_ukrainian={row.get('is_ukrainian','N/A')}")
else:
    log("  flag_non_ukrainian column not found")

# ---------------------------------------------------------------------------
# B5 — Attempt to resolve genuine unknowns via full bio re-fetch
# ---------------------------------------------------------------------------
log("\n" + "="*60)
log("STEP B5: Attempting to resolve genuine unknowns")
log("="*60)

genuine_unk_mask = (
    (df['migration_status'] == 'unknown') &
    (~df['migration_reasoning'].str.contains('credit balance is too low|B3-reclassified', na=False))
)
genuine_unk = df[genuine_unk_mask].copy()
log(f"Found {len(genuine_unk)} genuine unknowns (non-API-error)")

b5_done = 0
b5_still_unknown = 0

for i, (idx, row) in enumerate(genuine_unk.iterrows()):
    url = row.get('article_url', '')
    if pd.isna(url) or not str(url).startswith('http'):
        b5_still_unknown += 1
        continue

    html = fetch_article(str(url))
    time.sleep(DELAY)

    if not html:
        b5_still_unknown += 1
        continue

    birth_yr, death_yr, bio_text = extract_dates_from_html(html, str(row['name']))

    # Update dates if missing
    if birth_yr and pd.isna(row.get('_birth_n')):
        df.at[idx, 'birth_year'] = birth_yr
    if death_yr and pd.isna(row.get('_death_n')):
        df.at[idx, 'death_year'] = death_yr

    status, reasoning = classify_via_claude(
        str(row['name']), bio_text,
        birth_yr or row.get('birth_year'),
        death_yr or row.get('death_year')
    )

    if status != 'unknown':
        df.at[idx, 'migration_status']    = status
        df.at[idx, 'migration_reasoning'] = f'B5-resolved: {reasoning}'
        tag = df.at[idx, 'fix_applied']
        df.at[idx, 'fix_applied'] = (tag + '; ' if tag else '') + f'B5-to-{status}'
        b5_done += 1
        log(f"  [{i+1}/{len(genuine_unk)}] {row['name']}: resolved → {status}")
    else:
        b5_still_unknown += 1

    if (i + 1) % 10 == 0:
        df.to_csv(CSV_OUT, index=False)

log(f"B5 complete: {b5_done} resolved, {b5_still_unknown} remain unknown")

# ---------------------------------------------------------------------------
# Clean up temp columns & save
# ---------------------------------------------------------------------------
for col in ['_first_notes', '_death_n', '_birth_n']:
    if col in df.columns:
        df.drop(columns=[col], inplace=True)

df.to_csv(CSV_OUT, index=False)

# Write log
with open(LOG_FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(log_lines))

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
log("\n" + "="*60)
log("STAGE 12 COMPLETE")
log("="*60)

df2 = pd.read_csv(CSV_OUT)
status_counts = df2['migration_status'].value_counts()
print("\nFinal migration_status distribution:")
for status, n in status_counts.items():
    delta = n - pd.read_csv(CSV_IN)['migration_status'].value_counts().get(status, 0)
    delta_str = f" ({delta:+d})" if delta != 0 else ""
    print(f"  {status}: {n:,}{delta_str}")

mig   = df2[df2['migration_status'] == 'migrated']
nm    = df2[df2['migration_status'] == 'non_migrated']
mig_age = (pd.to_numeric(mig['death_year'], errors='coerce') -
           pd.to_numeric(mig['birth_year'], errors='coerce')).dropna()
nm_age  = (pd.to_numeric(nm['death_year'],  errors='coerce') -
           pd.to_numeric(nm['birth_year'],  errors='coerce')).dropna()

print(f"\nUpdated primary gap: {mig_age.mean():.2f} - {nm_age.mean():.2f} = {mig_age.mean()-nm_age.mean():.2f} yrs")
print(f"  Migrants: n={len(mig_age):,}, mean={mig_age.mean():.2f}")
print(f"  Non-migrants: n={len(nm_age):,}, mean={nm_age.mean():.2f}")
print(f"\nOutput → {CSV_OUT}")
print(f"Log    → {LOG_FILE}")

fixes = df2[df2['fix_applied'] != '']['fix_applied'].value_counts()
print(f"\nFix summary:")
for fix_type in ['B1', 'B2-date-corrected', 'B2-reclassified', 'B3', 'B5']:
    count = df2['fix_applied'].str.contains(fix_type, na=False).sum()
    if count:
        print(f"  {fix_type}: {count} entries")
