#!/usr/bin/env python3
"""
Phase 4: Claude-powered review of Ukrainian Creative Workers dataset.
V2.1 — revised following Phase 5 human accuracy check (2026-04-03)

Phases:
  --phase nationality   Review flagged entries — Claude decides if person is Ukrainian.
  --phase migration     Four-way migration classification: migrated / non_migrated /
                        internal_transfer / deported. Applies pre-1921 and Galicia
                        exclusions as pure Python filters before any Claude call.
  --phase analysis      Calculate life expectancy stats across all four groups.

Flags:
  --rerun               (migration phase only) Re-classify all entries from scratch,
                        ignoring any existing migration_status. Required for V2.1 rerun.

Output:
  nationality phase → esu_creative_workers_reviewed.csv  (in-place, incremental)
  migration phase   → esu_creative_workers_v2_1.csv      (new file, full rerun)
  analysis phase    → esu_analysis_results.txt

Model strategy:
  Haiku  — first-pass classification (~6,300 entries, ~$1.50 total)
  Sonnet — deep retry for entries that return 'unknown' after Haiku

Authors: Elza Berdnyk, Mark Symkin
AI: Claude Haiku-4.5 (first pass) + Claude Sonnet-4.6 (deep retry)
"""

import csv
import os
import sys
import time
import re
import json
import argparse
import requests
from bs4 import BeautifulSoup
import anthropic


# ─── Config ───────────────────────────────────────────────────────────────────

INPUT_FILE       = os.path.join(os.path.dirname(__file__), 'esu_creative_workers_raw.csv')
REVIEWED_FILE    = os.path.join(os.path.dirname(__file__), 'esu_creative_workers_reviewed.csv')
OUTPUT_FILE      = os.path.join(os.path.dirname(__file__), 'esu_creative_workers_v2_1.csv')
ANALYSIS_FILE    = os.path.join(os.path.dirname(__file__), 'esu_analysis_results.txt')

DELAY_FETCH   = 0.6   # seconds between ESU article fetches
DELAY_CLAUDE  = 0.3   # seconds between Claude API calls

MODEL_HAIKU   = 'claude-haiku-4-5-20251001'
MODEL_SONNET  = 'claude-sonnet-4-6'

FIELDNAMES = [
    'name', 'birth_year', 'death_year',
    'birth_location', 'death_location',
    'profession_raw', 'flag_non_ukrainian', 'flag_needs_claude_review',
    'article_url', 'notes',
    'is_ukrainian',           # YES / NO / UNCERTAIN  (blank = clean entry, assumed YES)
    'ukrainian_reasoning',
    'migration_status',       # migrated / non_migrated / internal_transfer / deported
                              # / unknown / alive
                              # / excluded_pre_soviet / excluded_galicia_pre_annexation
    'migration_reasoning',
]

# migration_status values that count as "done" in a normal (non-rerun) pass
RESOLVED_STATUSES = {
    'migrated', 'non_migrated', 'internal_transfer', 'deported',
    'alive', 'excluded_pre_soviet', 'excluded_galicia_pre_annexation',
}


# ─── Galicia detection ────────────────────────────────────────────────────────
# Galicia = modern Lviv, Ternopil, Ivano-Frankivsk oblasts + historical Galician territory.
# Was part of Austro-Hungarian Empire until 1918, then Poland until 1939.
# Workers born here and dead before 1939 never experienced Soviet rule.

GALICIAN_MARKERS = [
    # Region names
    'галичин', 'галиці', 'галич',
    # Lviv oblast cities
    'львів', 'дрогобич', 'самбір', 'стрий', 'яворів', 'золочів', 'жовква',
    'рава-руськ', 'городок', 'перемишль', 'белз', 'сокаль', 'броди',
    # Ternopil oblast
    'тернопіл', 'чортків', 'збараж', 'бережан', 'борщів', 'бучач',
    'копичинц', 'кременец', 'підгайц', 'теребовл', 'заліщик', 'зборів',
    'монастириськ', 'скалат', 'товст', 'козів', 'лановц',
    # Ivano-Frankivsk oblast
    'івано-франківськ', 'станіслав', 'коломи', 'снятин', 'городенк',
    'калуш', 'косів', 'надвірн', 'рогатин', 'тлумач', 'болехів',
    'долин', 'богородчан', 'галич',
    # Austro-Hungarian / Polish birth location indicators
    'австро-угорщин', 'австрійськ',
]


def is_galician_birth(birth_location):
    """Return True if birth_location matches a known Galician city or region."""
    if not birth_location:
        return False
    loc = birth_location.lower()
    return any(marker in loc for marker in GALICIAN_MARKERS)


def should_exclude_galicia(row):
    """
    Exclude if: born in Galicia AND died before 1939.
    Galicia was only under Soviet rule from September 1939 onwards.
    Workers alive in 1939 experienced Soviet conditions; those who died before did not.
    """
    death_year = safe_int(row.get('death_year'))
    if death_year is None:
        return False
    if death_year >= 1939:
        return False
    return is_galician_birth(row.get('birth_location', ''))


def should_exclude_pre_soviet(row):
    """
    Exclude if died before 1921 — the Ukrainian SSR was not consolidated
    until 1920-1922. These individuals were never subject to Soviet conditions.
    """
    death_year = safe_int(row.get('death_year'))
    return death_year is not None and death_year < 1921


# ─── Helpers ──────────────────────────────────────────────────────────────────

def safe_int(val):
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, val = line.split('=', 1)
                    os.environ.setdefault(key.strip(), val.strip())


def parse_json_response(text):
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return json.loads(text.strip())


# ─── CSV I/O ──────────────────────────────────────────────────────────────────

def load_csv(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def save_csv(rows, path):
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def append_csv(row, path):
    file_exists = os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction='ignore')
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


# ─── ESU article fetcher ──────────────────────────────────────────────────────

def make_session():
    s = requests.Session()
    s.headers.update({
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ),
        'Accept-Language': 'uk,en;q=0.9',
    })
    return s


def fetch_article_text(url, session):
    """Fetch full ESU article text. Returns up to 1500 chars or empty string."""
    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            return ''
        soup = BeautifulSoup(r.text, 'html.parser')
        article_div = (
            soup.find('div', class_=re.compile(r'article[-_]?(text|body|content)', re.I))
            or soup.find('div', class_=re.compile(r'content', re.I))
        )
        if article_div:
            return article_div.get_text(' ', strip=True)[:1500]
        return ' '.join(
            p.get_text(' ', strip=True) for p in soup.find_all('p')[:12]
        )[:1500]
    except Exception:
        return ''


# ─── Claude prompts ────────────────────────────────────────────────────────────

NATIONALITY_SYSTEM = """\
You are a research assistant for an academic paper on Soviet-era persecution of Ukrainian creative workers.

Decide whether a person listed in the Encyclopedia of Modern Ukraine qualifies as "Ukrainian" for this research.

A person QUALIFIES (answer YES) if ANY apply:
- Born, grew up, or lived a significant part of their life in territory that is now Ukraine
  (includes historical Ukrainian lands: Galicia, Bukovyna, Zakarpattia, Volhynia, Crimea, etc.)
- Contributed meaningfully to Ukrainian culture, literature, art — regardless of ethnicity
- Was subject to Soviet persecution in the context of suppressing Ukrainian culture
- Self-identified as Ukrainian or was a member of the Ukrainian creative community

A person does NOT qualify (answer NO) if:
- They lived entirely outside Ukraine with no meaningful Ukrainian connection
- Their only tie is being mentioned in the ESU as a foreign reference figure

Answer UNCERTAIN only if truly ambiguous even after reading the bio.

Reply ONLY in this exact JSON format, no extra text:
{"is_ukrainian": "YES" or "NO" or "UNCERTAIN", "reasoning": "one sentence max"}"""


# ── Four-way migration prompt (Haiku first pass) ──────────────────────────────

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


# ── Four-way deep retry prompt (Sonnet — for unknowns only) ──────────────────

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


# ─── Claude API calls ─────────────────────────────────────────────────────────

def ask_claude_nationality(client, name, profession, birth_loc, death_loc, bio):
    user_msg = (
        f"Name: {name}\n"
        f"Profession: {profession}\n"
        f"Born: {birth_loc or 'unknown'}\n"
        f"Died: {death_loc or 'unknown'}\n"
        f"Biography excerpt:\n{bio[:900] if bio else 'Not available'}"
    )
    try:
        response = client.messages.create(
            model=MODEL_HAIKU,
            max_tokens=120,
            system=NATIONALITY_SYSTEM,
            messages=[{'role': 'user', 'content': user_msg}],
        )
        data = parse_json_response(response.content[0].text)
        return data.get('is_ukrainian', 'UNCERTAIN'), data.get('reasoning', '')
    except Exception as e:
        return 'UNCERTAIN', f'error: {e}'


def ask_claude_migration_haiku(client, name, profession, birth_loc, death_loc,
                                birth_year, death_year, bio):
    user_msg = (
        f"Name: {name}\n"
        f"Profession: {profession}\n"
        f"Born: {birth_year or '?'} — {birth_loc or 'unknown'}\n"
        f"Died: {death_year or '?'} — {death_loc or 'unknown'}\n"
        f"Biography:\n{bio[:900] if bio else 'Not available'}"
    )
    try:
        response = client.messages.create(
            model=MODEL_HAIKU,
            max_tokens=150,
            system=MIGRATION_SYSTEM,
            messages=[{'role': 'user', 'content': user_msg}],
        )
        data = parse_json_response(response.content[0].text)
        return data.get('migration_status', 'unknown'), data.get('reasoning', '')
    except Exception as e:
        return 'unknown', f'haiku_error: {e}'


def ask_claude_migration_sonnet(client, name, profession, birth_loc, death_loc,
                                 birth_year, death_year, bio):
    """Sonnet deep retry — used only when Haiku returns 'unknown'."""
    user_msg = (
        f"Name: {name}\n"
        f"Profession: {profession}\n"
        f"Born: {birth_year or '?'} — {birth_loc or 'unknown'}\n"
        f"Died: {death_year or '?'} — {death_loc or 'unknown'}\n"
        f"Full biography:\n{bio[:1400] if bio else 'Not available'}\n\n"
        f"Previous Haiku pass returned 'unknown'. Look harder at all clues."
    )
    try:
        response = client.messages.create(
            model=MODEL_SONNET,
            max_tokens=200,
            system=MIGRATION_DEEP_SYSTEM,
            messages=[{'role': 'user', 'content': user_msg}],
        )
        data = parse_json_response(response.content[0].text)
        return data.get('migration_status', 'unknown'), data.get('reasoning', '')
    except Exception as e:
        return 'unknown', f'sonnet_error: {e}'


# ─── Phase 4a: Nationality review ─────────────────────────────────────────────

def run_nationality_phase():
    load_env()
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        sys.exit('Error: ANTHROPIC_API_KEY not found in .env')

    client = anthropic.Anthropic(api_key=api_key)
    session = make_session()

    raw_rows = load_csv(INPUT_FILE)
    reviewed = {}
    if os.path.exists(REVIEWED_FILE):
        reviewed = {row['article_url']: row for row in load_csv(REVIEWED_FILE)}

    working = []
    for row in raw_rows:
        url = row['article_url']
        if url in reviewed:
            working.append(reviewed[url])
        else:
            working.append({
                **row,
                'is_ukrainian': '',
                'ukrainian_reasoning': '',
                'migration_status': '',
                'migration_reasoning': '',
            })

    to_review = [
        r for r in working
        if r.get('flag_needs_claude_review') == 'YES'
        and not r.get('is_ukrainian')
    ]

    total = len(to_review)
    already = sum(1 for r in working
                  if r.get('flag_needs_claude_review') == 'YES' and r.get('is_ukrainian'))
    print(f"\nPhase 4a — Nationality review")
    print(f"Entries to review: {total}")
    print(f"Already reviewed:  {already}")
    print()

    if total == 0:
        print("Nothing left to review. Run --phase migration --rerun next.")
        return

    if not os.path.exists(REVIEWED_FILE):
        seed = [r for r in working if r.get('flag_needs_claude_review') != 'YES']
        save_csv(seed, REVIEWED_FILE)
        print(f"  Seeded output with {len(seed)} non-flagged entries.")

    done = 0
    for row in to_review:
        url   = row['article_url']
        notes = row.get('notes', '')
        bio   = notes if len(notes.strip()) >= 150 else fetch_article_text(url, session)
        if bio != notes:
            time.sleep(DELAY_FETCH)

        is_ua, reasoning = ask_claude_nationality(
            client, row['name'], row['profession_raw'],
            row['birth_location'], row['death_location'], bio
        )
        time.sleep(DELAY_CLAUDE)

        row['is_ukrainian']        = is_ua
        row['ukrainian_reasoning'] = reasoning
        append_csv(row, REVIEWED_FILE)
        done += 1

        icon = {'YES': '✓ Ukrainian', 'NO': '✗ Not Ukrainian', 'UNCERTAIN': '? Uncertain'}.get(is_ua, is_ua)
        print(f"  [{done}/{total}] {row['name'][:45]:45s} → {icon}")
        if done % 50 == 0:
            print(f"  [checkpoint {done}/{total}]")

    print(f"\nDone. {done} entries reviewed.")
    print(f"Next: python claude_review.py --phase migration --rerun")


# ─── Phase 4b: Migration classification ───────────────────────────────────────

def is_confirmed_ukrainian(row):
    if row.get('flag_non_ukrainian') == 'YES':
        return False
    if row.get('flag_needs_claude_review') == 'YES':
        return row.get('is_ukrainian') == 'YES'
    return True


def run_migration_phase(rerun=False):
    load_env()
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        sys.exit('Error: ANTHROPIC_API_KEY not found in .env')

    client  = anthropic.Anthropic(api_key=api_key)
    session = make_session()

    source_file = REVIEWED_FILE if os.path.exists(REVIEWED_FILE) else INPUT_FILE
    rows = load_csv(source_file)

    # Build working dict keyed by URL
    working = {row['article_url']: row for row in rows}

    # If rerun — load OUTPUT_FILE progress so we can resume mid-rerun
    already_done = {}
    if os.path.exists(OUTPUT_FILE) and rerun:
        already_done = {row['article_url']: row for row in load_csv(OUTPUT_FILE)}
        print(f"  Resuming rerun — {len(already_done)} entries already written to output.")

    # Build list of confirmed Ukrainian entries to process
    candidates = [
        row for row in working.values()
        if is_confirmed_ukrainian(row)
    ]

    # Apply date-based exclusions (pure Python — no Claude needed)
    pre_soviet_excluded = 0
    galicia_excluded     = 0
    to_process           = []

    for row in candidates:
        if should_exclude_pre_soviet(row):
            row['migration_status']    = 'excluded_pre_soviet'
            row['migration_reasoning'] = (
                f"Died before 1921 (death_year={row.get('death_year')}) — "
                f"pre-Soviet, outside study scope."
            )
            working[row['article_url']] = row
            pre_soviet_excluded += 1
        elif should_exclude_galicia(row):
            row['migration_status']    = 'excluded_galicia_pre_annexation'
            row['migration_reasoning'] = (
                f"Born in Galicia, died {row.get('death_year')} — before 1939 "
                f"USSR annexation of western Ukraine. Never under Soviet rule."
            )
            working[row['article_url']] = row
            galicia_excluded += 1
        else:
            to_process.append(row)

    # Filter to_process based on rerun mode
    if rerun:
        # Skip entries already written in this rerun's output file
        to_process = [r for r in to_process if r['article_url'] not in already_done]
    else:
        # Normal mode — skip already resolved entries
        to_process = [
            r for r in to_process
            if r.get('migration_status') not in RESOLVED_STATUSES
        ]

    total     = len(to_process)
    confirmed = len(candidates)
    print(f"\nPhase 4b — Migration classification (V2.1 four-way)")
    print(f"Confirmed Ukrainian entries:       {confirmed:,}")
    print(f"Excluded pre-1921:                 {pre_soviet_excluded:,}")
    print(f"Excluded Galicia pre-1939:         {galicia_excluded:,}")
    print(f"To classify now:                   {total:,}")
    print(f"Rerun mode:                        {'YES — re-classifying all' if rerun else 'NO — skipping resolved'}")
    print()

    if total == 0:
        print("Nothing to classify. Run --phase analysis to see results.")
        return

    # Write excluded entries to output first
    if rerun and not already_done:
        excluded_rows = [
            r for r in working.values()
            if r.get('migration_status') in ('excluded_pre_soviet', 'excluded_galicia_pre_annexation')
        ]
        # Also write already-resolved from prior rerun
        if already_done:
            excluded_rows += list(already_done.values())
        if excluded_rows:
            save_csv(excluded_rows, OUTPUT_FILE)

    done         = 0
    sonnet_count = 0

    for row in to_process:
        url        = row['article_url']
        name       = row['name']
        birth_year = row.get('birth_year', '')
        death_year = row.get('death_year', '')

        # No death year → alive, skip Claude
        if not death_year:
            row['migration_status']    = 'alive'
            row['migration_reasoning'] = 'No death year — presumed alive or date unknown.'
            append_csv(row, OUTPUT_FILE)
            working[url] = row
            done += 1
            print(f"  [{done}/{total}] {name[:45]:45s} → ○ Alive")
            continue

        # Fetch full article
        bio = fetch_article_text(url, session)
        if not bio:
            bio = row.get('notes', '')
        time.sleep(DELAY_FETCH)

        # Haiku first pass
        status, reasoning = ask_claude_migration_haiku(
            client, name, row['profession_raw'],
            row['birth_location'], row['death_location'],
            birth_year, death_year, bio
        )
        time.sleep(DELAY_CLAUDE)

        # Sonnet deep retry for unknowns
        if status == 'unknown':
            status, reasoning = ask_claude_migration_sonnet(
                client, name, row['profession_raw'],
                row['birth_location'], row['death_location'],
                birth_year, death_year, bio
            )
            time.sleep(DELAY_CLAUDE)
            sonnet_count += 1

        row['migration_status']    = status
        row['migration_reasoning'] = reasoning
        working[url]               = row
        append_csv(row, OUTPUT_FILE)
        done += 1

        icons = {
            'migrated':          '→ Migrated',
            'non_migrated':      '• Stayed',
            'internal_transfer': '~ Internal transfer',
            'deported':          '⚑ Deported',
            'unknown':           '? Unknown',
        }
        icon = icons.get(status, status)
        sonnet_flag = ' [Sonnet]' if 'sonnet' in reasoning.lower() or status == 'unknown' else ''
        print(f"  [{done}/{total}] {name[:45]:45s} → {icon}{sonnet_flag}")

        if done % 200 == 0:
            print(f"\n  [checkpoint {done}/{total} — Sonnet escalations so far: {sonnet_count}]\n")

    print(f"\nDone. {done} entries classified.")
    print(f"Sonnet escalations: {sonnet_count}")
    print(f"Output: {OUTPUT_FILE}")
    print(f"\nNext: python claude_review.py --phase analysis")


# ─── Phase 4c: Analysis ───────────────────────────────────────────────────────

def run_analysis_phase():
    # Use V2.1 output if it exists, otherwise fall back to reviewed
    source = OUTPUT_FILE if os.path.exists(OUTPUT_FILE) else REVIEWED_FILE
    if not os.path.exists(source):
        sys.exit(f'Error: no output file found. Run nationality + migration phases first.')

    rows = load_csv(source)

    def ages(group):
        result = []
        for r in group:
            b = safe_int(r.get('birth_year'))
            d = safe_int(r.get('death_year'))
            if b and d and 5 <= d - b <= 110:
                result.append(d - b)
        return result

    def avg(lst):
        return sum(lst) / len(lst) if lst else 0

    def median(lst):
        if not lst:
            return 0
        s = sorted(lst)
        n = len(s)
        return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

    results = []
    def log(line=''):
        print(line)
        results.append(line)

    # ── Filter confirmed Ukrainian with dates ──────────────────
    confirmed_ua = [r for r in rows if is_confirmed_ukrainian(r)]
    total_ua = len(confirmed_ua)

    migrated    = [r for r in confirmed_ua if r.get('migration_status') == 'migrated']
    non_mig     = [r for r in confirmed_ua if r.get('migration_status') == 'non_migrated']
    internal    = [r for r in confirmed_ua if r.get('migration_status') == 'internal_transfer']
    deported    = [r for r in confirmed_ua if r.get('migration_status') == 'deported']
    alive       = [r for r in confirmed_ua if r.get('migration_status') == 'alive']
    unknown     = [r for r in confirmed_ua if r.get('migration_status') == 'unknown']
    ex_pre      = [r for r in confirmed_ua if r.get('migration_status') == 'excluded_pre_soviet']
    ex_gal      = [r for r in confirmed_ua if r.get('migration_status') == 'excluded_galicia_pre_annexation']

    # Primary analysis groups: migrated vs (non_migrated + deported)
    primary_nm = non_mig + deported

    log("=" * 65)
    log("UKRAINIAN CREATIVE WORKERS — LIFE EXPECTANCY ANALYSIS V2.1")
    log("Berdnyk & Symkin")
    log("=" * 65)
    log()
    log(f"Total confirmed Ukrainian entries:           {total_ua:,}")
    log(f"  Excluded (pre-1921 deaths):                {len(ex_pre):,}")
    log(f"  Excluded (Galicia, died before 1939):      {len(ex_gal):,}")
    log(f"  Alive / no death date:                     {len(alive):,}")
    log(f"  Unknown migration (after Sonnet retry):    {len(unknown):,}")
    log()
    log(f"Primary analysis dataset:")
    log(f"  Migrated (left USSR):                      {len(migrated):,}")
    log(f"  Non-migrated (stayed in Ukrainian SSR):    {len(non_mig):,}")
    log(f"  Deported (forced by Soviet state):         {len(deported):,}")
    log(f"  Internal transfer (voluntary, within USSR):{len(internal):,}")
    log()

    # ── Primary LE comparison ──────────────────────────────────
    log("── Primary Life Expectancy Comparison ───────────────────────")
    log(f"{'Group':<35} {'N':>6}  {'Mean LE':>8}  {'Median':>7}")
    log("-" * 62)

    for label, group in [
        ('Migrated (left USSR)',           migrated),
        ('Non-migrated (stayed in USSR)',  non_mig),
        ('Deported (forced by state)',     deported),
        ('Internal transfer (voluntary)',  internal),
        ('Non-mig + Deported (combined)', primary_nm),
    ]:
        a = ages(group)
        log(f"{label:<35} {len(a):>6}  {avg(a):>7.2f}y  {median(a):>6.0f}y")

    if ages(migrated) and ages(primary_nm):
        gap_mean   = avg(ages(migrated))   - avg(ages(primary_nm))
        gap_median = median(ages(migrated)) - median(ages(primary_nm))
        log()
        log(f"Primary gap (migrated vs non-mig+deported): mean {gap_mean:+.2f}y / median {gap_median:+.0f}y")
        gap_nm_only = avg(ages(migrated)) - avg(ages(non_mig))
        log(f"Gap (migrated vs non-mig only):             mean {gap_nm_only:+.2f}y")
        gap_dep = avg(ages(deported)) - avg(ages(non_mig)) if ages(deported) else 0
        log(f"Deported vs non-mig penalty:                mean {gap_dep:+.2f}y")
    log()

    # ── Most common death years ────────────────────────────────
    from collections import Counter
    log("── Most Common Death Years ───────────────────────────────────")
    for label, group in [
        ('Non-migrated', non_mig),
        ('Migrated',     migrated),
        ('Deported',     deported),
    ]:
        death_years = [safe_int(r['death_year']) for r in group if safe_int(r.get('death_year'))]
        top5 = Counter(death_years).most_common(5)
        log(f"\n{label}:")
        for year, count in top5:
            yr_group = [r for r in group if safe_int(r.get('death_year')) == year]
            log(f"  {year}: {count} deaths  (avg age: {avg(ages(yr_group)):.0f})")
    log()

    # ── Profession breakdown ───────────────────────────────────
    log("── Life Expectancy by Profession ─────────────────────────────")
    profession_keywords = {
        'Writers/Poets':  ['письменник', 'поет', 'прозаїк', 'драматург'],
        'Visual Artists': ['художник', 'живописець', 'скульптор', 'графік', 'ілюстратор'],
        'Musicians':      ['композитор', 'диригент', 'піаніст', 'скрипаль', 'співак'],
        'Theatre/Film':   ['актор', 'режисер', 'кінорежисер', 'сценарист'],
        'Architects':     ['архітектор'],
    }
    log(f"{'Profession':<20} {'N':>5}  {'Migr':>7}  {'Non-mig':>8}  {'Deported':>9}  {'Gap':>6}")
    log("-" * 62)
    for prof_label, keywords in profession_keywords.items():
        prof = [r for r in confirmed_ua
                if any(kw in r.get('profession_raw', '').lower() for kw in keywords)
                and r.get('migration_status') in ('migrated', 'non_migrated', 'deported')]
        pm  = [r for r in prof if r['migration_status'] == 'migrated']
        pnm = [r for r in prof if r['migration_status'] == 'non_migrated']
        pd  = [r for r in prof if r['migration_status'] == 'deported']
        g   = avg(ages(pm)) - avg(ages(pnm)) if ages(pm) and ages(pnm) else 0
        log(f"{prof_label:<20} {len(prof):>5}  {avg(ages(pm)):>6.1f}y  {avg(ages(pnm)):>7.1f}y  {avg(ages(pd)):>8.1f}y  {g:>+5.1f}y")
    log()

    # ── Period breakdown ───────────────────────────────────────
    log("── Non-migrant Deaths by Soviet Period ───────────────────────")
    periods = [
        ('1921–1929 (early Soviet)',    1921, 1930),
        ('1930–1939 (Great Terror)',    1930, 1940),
        ('1940–1945 (WWII)',            1940, 1946),
        ('1946–1953 (Late Stalin)',     1946, 1954),
        ('1954–1991 (post-Stalin)',     1954, 1992),
        ('Post-1991',                  1992, 2100),
    ]
    log(f"{'Period':<30} {'Deaths':>7}  {'Avg Age':>8}")
    log("-" * 50)
    for label, start, end in periods:
        grp = [r for r in non_mig
               if start <= (safe_int(r.get('death_year')) or 0) < end]
        log(f"{label:<30} {len(grp):>7}  {avg(ages(grp)):>7.1f}y")
    log()

    # ── Deported period breakdown ──────────────────────────────
    log("── Deported Deaths by Period ─────────────────────────────────")
    log(f"{'Period':<30} {'Deaths':>7}  {'Avg Age':>8}")
    log("-" * 50)
    for label, start, end in periods:
        grp = [r for r in deported
               if start <= (safe_int(r.get('death_year')) or 0) < end]
        log(f"{label:<30} {len(grp):>7}  {avg(ages(grp)):>7.1f}y")
    log()

    # ── Summary ───────────────────────────────────────────────
    log("── Paper Summary ─────────────────────────────────────────────")
    log(f"V1: 415 workers / 9-year gap (63y vs 72y) — pre-1991 cutoff bias")
    log(f"V2.0: 6,310 workers / 4.77-year gap — cutoff bias removed")
    log(f"V2.1: rerun with four-way classification + date exclusions")
    log(f"  Migrated:          {len(migrated):,} workers")
    log(f"  Non-migrated:      {len(non_mig):,} workers")
    log(f"  Deported:          {len(deported):,} workers")
    log(f"  Internal transfer: {len(internal):,} workers")
    log("=" * 65)

    with open(ANALYSIS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
    print(f"\nSaved to: {ANALYSIS_FILE}")


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Phase 4: Claude-powered review — V2.1 four-way migration classification.'
    )
    parser.add_argument(
        '--phase',
        choices=['nationality', 'migration', 'analysis'],
        required=True,
    )
    parser.add_argument(
        '--rerun',
        action='store_true',
        help='(migration only) Re-classify all entries from scratch, ignoring existing statuses.'
    )
    args = parser.parse_args()

    if args.phase == 'nationality':
        run_nationality_phase()
    elif args.phase == 'migration':
        run_migration_phase(rerun=args.rerun)
    elif args.phase == 'analysis':
        run_analysis_phase()
