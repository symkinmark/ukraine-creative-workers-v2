#!/usr/bin/env python3
"""
Phase 4: Claude-powered review of Ukrainian Creative Workers dataset.

Phases:
  --phase nationality   Review 1,356 flagged entries — Claude reads each bio
                        and decides if the person qualifies as Ukrainian.
  --phase migration     For all confirmed-Ukrainian entries, determine whether
                        they migrated out of the USSR or stayed.
  --phase analysis      Calculate life expectancy stats and print results.

Usage:
  python claude_review.py --phase nationality
  python claude_review.py --phase migration
  python claude_review.py --phase analysis

Output: esu_creative_workers_reviewed.csv
        esu_analysis_results.txt  (analysis phase only)

Authors: Elza Berdnyk, Mark Symkin
AI: Claude Haiku-4.5 (Anthropic)
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

INPUT_FILE  = os.path.join(os.path.dirname(__file__), 'esu_creative_workers_raw.csv')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'esu_creative_workers_reviewed.csv')
ANALYSIS_FILE = os.path.join(os.path.dirname(__file__), 'esu_analysis_results.txt')

DELAY_BETWEEN_REQUESTS = 0.6   # seconds between ESU article fetches
DELAY_BETWEEN_CLAUDE   = 0.3   # seconds between Claude API calls

# Output columns — original + new Phase 4 columns
FIELDNAMES = [
    'name', 'birth_year', 'death_year',
    'birth_location', 'death_location',
    'profession_raw', 'flag_non_ukrainian', 'flag_needs_claude_review',
    'article_url', 'notes',
    # Phase 4a
    'is_ukrainian',          # YES / NO / UNCERTAIN  (blank = clean entry, assumed YES)
    'ukrainian_reasoning',   # Claude's one-sentence explanation
    # Phase 4b
    'migration_status',      # migrated / non_migrated / unknown
    'migration_reasoning',   # Claude's one-sentence explanation
]


# ─── Load API key from .env ────────────────────────────────────────────────────

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, val = line.split('=', 1)
                    os.environ.setdefault(key.strip(), val.strip())


# ─── Load / save CSV ──────────────────────────────────────────────────────────

def load_input():
    """Load the raw scraper output. Returns list of dicts."""
    with open(INPUT_FILE, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def load_reviewed():
    """
    Load existing reviewed output (if it exists).
    Returns a dict keyed by article_url so we can pick up where we left off.
    """
    if not os.path.exists(OUTPUT_FILE):
        return {}
    with open(OUTPUT_FILE, newline='', encoding='utf-8-sig') as f:
        return {row['article_url']: row for row in csv.DictReader(f)}


def save_reviewed(rows):
    """Overwrite the output file with the full reviewed dataset."""
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def append_reviewed(row):
    """Append a single row to the output file (fast incremental save)."""
    file_exists = os.path.exists(OUTPUT_FILE)
    with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction='ignore')
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


# ─── Fetch article bio from ESU ───────────────────────────────────────────────

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
    """
    Fetch the full text of an ESU article.
    Returns up to 1500 chars of plain text, or empty string on failure.
    """
    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            return ''
        soup = BeautifulSoup(r.text, 'html.parser')
        # ESU article content lives in a <div> with class containing 'article' or 'content'
        article_div = (
            soup.find('div', class_=re.compile(r'article[-_]?(text|body|content)', re.I))
            or soup.find('div', class_=re.compile(r'content', re.I))
        )
        if article_div:
            return article_div.get_text(' ', strip=True)[:1500]
        # Fallback: collect all <p> tags
        return ' '.join(p.get_text(' ', strip=True) for p in soup.find_all('p')[:12])[:1500]
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


MIGRATION_SYSTEM = """\
You are a research assistant for an academic paper on life expectancy of Ukrainian creative workers during Soviet occupation.

Determine whether a Ukrainian creative worker migrated OUT of Soviet-controlled territory, or stayed.

Classification rules:
- migrated:      Left Soviet-controlled territory and lived abroad for a significant period
- non_migrated:  Stayed in the USSR/Ukraine their whole life
- non_migrated:  Was killed by Soviets while in former Polish territories (western Ukraine)
- non_migrated:  Migrated but returned to the USSR and died there
- non_migrated:  Released from prison/camp due to poor health and died within 1 year
- non_migrated:  Was killed by Soviet agents outside USSR territory
- unknown:       Insufficient information to make a determination

Reply ONLY in this exact JSON format, no extra text:
{"migration_status": "migrated" or "non_migrated" or "unknown", "reasoning": "one sentence max"}"""


def parse_json_response(text):
    """Parse JSON from Claude response, stripping markdown code blocks if present."""
    text = text.strip()
    # Remove ```json ... ``` or ``` ... ``` wrappers
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return json.loads(text.strip())


def ask_claude_nationality(client, name, profession, birth_loc, death_loc, bio):
    """Ask Claude Haiku if this person qualifies as Ukrainian."""
    user_msg = (
        f"Name: {name}\n"
        f"Profession: {profession}\n"
        f"Born: {birth_loc or 'unknown'}\n"
        f"Died: {death_loc or 'unknown'}\n"
        f"Biography excerpt:\n{bio[:900] if bio else 'Not available'}"
    )
    try:
        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=120,
            system=NATIONALITY_SYSTEM,
            messages=[{'role': 'user', 'content': user_msg}],
        )
        data = parse_json_response(response.content[0].text)
        return data.get('is_ukrainian', 'UNCERTAIN'), data.get('reasoning', '')
    except Exception as e:
        return 'UNCERTAIN', f'error: {e}'


def ask_claude_migration(client, name, profession, birth_loc, death_loc,
                         birth_year, death_year, bio):
    """Ask Claude Haiku for migration status."""
    user_msg = (
        f"Name: {name}\n"
        f"Profession: {profession}\n"
        f"Born: {birth_year or '?'} — {birth_loc or 'unknown'}\n"
        f"Died: {death_year or '?'} — {death_loc or 'unknown'}\n"
        f"Biography excerpt:\n{bio[:900] if bio else 'Not available'}"
    )
    try:
        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=120,
            system=MIGRATION_SYSTEM,
            messages=[{'role': 'user', 'content': user_msg}],
        )
        data = parse_json_response(response.content[0].text)
        return data.get('migration_status', 'unknown'), data.get('reasoning', '')
    except Exception as e:
        return 'unknown', f'error: {e}'


MIGRATION_DEEP_SYSTEM = """\
You are a research assistant. A previous analysis could not determine whether this Ukrainian creative worker migrated out of the USSR.

Look harder. Consider:
- Death location: if they died outside Soviet territory (e.g. Paris, New York, Munich, London, Buenos Aires, Toronto, Rome) → migrated
- If they died in Ukraine, Russia, or any Soviet republic → non_migrated
- If born in western Ukraine (Galicia, Bukovyna, Zakarpattia, Volhynia) and died abroad → likely migrated post-WWII
- If they were repressed, imprisoned, or executed by Soviets → non_migrated
- If the biography mentions emigration, exile, displaced persons camps, or living abroad → migrated
- If truly no information exists → unknown is acceptable as last resort

Reply ONLY in this exact JSON format:
{"migration_status": "migrated" or "non_migrated" or "unknown", "reasoning": "one sentence max"}"""


def ask_claude_migration_deep(client, name, profession, birth_loc, death_loc,
                               birth_year, death_year, bio):
    """Second-pass migration check with a more aggressive prompt for stubborn unknowns."""
    user_msg = (
        f"Name: {name}\n"
        f"Profession: {profession}\n"
        f"Born: {birth_year or '?'} — {birth_loc or 'unknown'}\n"
        f"Died: {death_year or '?'} — {death_loc or 'unknown'}\n"
        f"Full biography:\n{bio[:1400] if bio else 'Not available'}\n\n"
        f"Previous attempt returned 'unknown'. Please look harder at all available clues."
    )
    try:
        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=150,
            system=MIGRATION_DEEP_SYSTEM,
            messages=[{'role': 'user', 'content': user_msg}],
        )
        data = parse_json_response(response.content[0].text)
        return data.get('migration_status', 'unknown'), data.get('reasoning', '')
    except Exception as e:
        return 'unknown', f'error: {e}'


# ─── Phase 4a: Nationality review ─────────────────────────────────────────────

def run_nationality_phase():
    """
    For each entry with flag_needs_claude_review=YES, ask Claude whether
    the person qualifies as Ukrainian. Uses notes field first; fetches the
    full article only if the notes are too sparse (< 150 chars).
    """
    load_env()
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        sys.exit('Error: ANTHROPIC_API_KEY not found in .env')

    client = anthropic.Anthropic(api_key=api_key)
    session = make_session()

    raw_rows = load_input()
    reviewed = load_reviewed()

    # Build working list: start from reviewed data if it exists, else from raw
    working = []
    for row in raw_rows:
        url = row['article_url']
        if url in reviewed:
            working.append(reviewed[url])  # already has Phase 4 columns
        else:
            # Add blank Phase 4 columns
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
        and not r.get('is_ukrainian')   # skip already done
    ]

    total = len(to_review)
    print(f"\nPhase 4a — Nationality review")
    print(f"Entries to review: {total}")
    print(f"Already reviewed:  {sum(1 for r in working if r.get('flag_needs_claude_review') == 'YES' and r.get('is_ukrainian'))}")
    print()

    if total == 0:
        print("Nothing left to review. Run --phase migration next.")
        return

    # Write header if file doesn't exist yet
    if not os.path.exists(OUTPUT_FILE):
        # Seed output file with all rows that don't need review
        seed = [r for r in working if r.get('flag_needs_claude_review') != 'YES']
        save_reviewed(seed)
        print(f"  Seeded output file with {len(seed)} non-review entries.")

    done = 0
    for row in to_review:
        name       = row['name']
        profession = row['profession_raw']
        birth_loc  = row['birth_location']
        death_loc  = row['death_location']
        notes      = row.get('notes', '')
        url        = row['article_url']

        # Use notes if long enough; otherwise fetch the full article
        bio = notes
        if len(notes.strip()) < 150:
            bio = fetch_article_text(url, session)
            time.sleep(DELAY_BETWEEN_REQUESTS)

        is_ua, reasoning = ask_claude_nationality(
            client, name, profession, birth_loc, death_loc, bio
        )
        time.sleep(DELAY_BETWEEN_CLAUDE)

        row['is_ukrainian']        = is_ua
        row['ukrainian_reasoning'] = reasoning

        # Update working list in place
        for i, r in enumerate(working):
            if r['article_url'] == url:
                working[i] = row
                break

        append_reviewed(row)
        done += 1

        flag = {'YES': '✓ Ukrainian', 'NO': '✗ Not Ukrainian', 'UNCERTAIN': '? Uncertain'}.get(is_ua, is_ua)
        print(f"  [{done}/{total}] {name[:40]:40s} → {flag}")
        if done % 50 == 0:
            print(f"  [checkpoint: {done}/{total} done]")

    print(f"\nDone. {done} entries reviewed.")
    print(f"Output: {OUTPUT_FILE}")
    print(f"\nNext step: python claude_review.py --phase migration")


# ─── Phase 4b: Migration status ───────────────────────────────────────────────

def run_migration_phase():
    """
    For all confirmed-Ukrainian entries (clean + reviewed-as-YES),
    determine migration status using birth/death location + Claude Haiku.
    """
    load_env()
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        sys.exit('Error: ANTHROPIC_API_KEY not found in .env')

    client = anthropic.Anthropic(api_key=api_key)
    session = make_session()

    if not os.path.exists(OUTPUT_FILE):
        sys.exit(f'Error: {OUTPUT_FILE} not found. Run --phase nationality first.')

    reviewed = load_reviewed()
    working  = list(reviewed.values())

    # Which entries are confirmed Ukrainian?
    def is_confirmed_ukrainian(row):
        if row.get('flag_non_ukrainian') == 'YES':
            return False
        if row.get('flag_needs_claude_review') == 'YES':
            return row.get('is_ukrainian') == 'YES'
        return True  # clean entry = Ukrainian

    to_process = [
        r for r in working
        if is_confirmed_ukrainian(r)
        and r.get('migration_status') not in ('migrated', 'non_migrated', 'alive')
        # re-process old unknowns with full bio + deep retry
    ]

    total = len(to_process)
    confirmed = sum(1 for r in working if is_confirmed_ukrainian(r))
    already_resolved = sum(1 for r in working if is_confirmed_ukrainian(r) and r.get('migration_status') in ('migrated', 'non_migrated'))
    unknowns = sum(1 for r in working if is_confirmed_ukrainian(r) and r.get('migration_status') == 'unknown')
    print(f"\nPhase 4b — Migration status (full biography fetch)")
    print(f"Confirmed Ukrainian entries:  {confirmed}")
    print(f"Already resolved (m/nm):      {already_resolved}")
    print(f"Unknowns being re-processed:  {unknowns}")
    print(f"To process now:               {total}")
    print()

    if total == 0:
        print("All migration statuses already determined.")
        print("Run --phase analysis to see results.")
        return

    done = 0
    for row in to_process:
        name       = row['name']
        profession = row['profession_raw']
        birth_loc  = row['birth_location']
        death_loc  = row['death_location']
        birth_year = row['birth_year']
        death_year = row['death_year']
        notes      = row.get('notes', '')
        url        = row['article_url']

        # If no death year — person is likely still alive, mark and skip Claude
        if not death_year:
            row['migration_status']    = 'alive'
            row['migration_reasoning'] = 'No death year recorded — presumed alive or death date unknown.'
            for i, r in enumerate(working):
                if r['article_url'] == url:
                    working[i] = row
                    break
            append_reviewed(row)
            done += 1
            print(f"  [{done}/{total}] {name[:40]:40s} → ○ Alive/no date")
            continue

        # Always fetch the full article — migration info is rarely in the first 300 chars
        bio = fetch_article_text(url, session)
        if not bio:
            bio = notes  # fallback to notes if fetch fails
        time.sleep(DELAY_BETWEEN_REQUESTS)

        status, reasoning = ask_claude_migration(
            client, name, profession, birth_loc, death_loc,
            birth_year, death_year, bio
        )
        time.sleep(DELAY_BETWEEN_CLAUDE)

        # If still unknown — retry with a deeper, more explicit prompt
        if status == 'unknown':
            status, reasoning = ask_claude_migration_deep(
                client, name, profession, birth_loc, death_loc,
                birth_year, death_year, bio
            )
            time.sleep(DELAY_BETWEEN_CLAUDE)

        row['migration_status']    = status
        row['migration_reasoning'] = reasoning

        for i, r in enumerate(working):
            if r['article_url'] == url:
                working[i] = row
                break

        append_reviewed(row)
        done += 1

        icon = {'migrated': '→ Migrated', 'non_migrated': '• Stayed', 'unknown': '? Unknown', 'alive': '○ Alive'}.get(status, status)
        print(f"  [{done}/{total}] {name[:40]:40s} → {icon}")

        if done % 100 == 0:
            print(f"  [checkpoint: {done}/{total} done — saving full file]")
            save_reviewed(working)

    save_reviewed(working)
    print(f"\nDone. {done} entries processed.")
    print(f"Output: {OUTPUT_FILE}")
    print(f"\nNext step: python claude_review.py --phase analysis")


# ─── Phase 4c: Analysis ───────────────────────────────────────────────────────

def run_analysis_phase():
    """
    Calculate life expectancy statistics by migration status, profession,
    time period, and other breakdowns. Print results and save to text file.
    """
    if not os.path.exists(OUTPUT_FILE):
        sys.exit(f'Error: {OUTPUT_FILE} not found. Run nationality + migration phases first.')

    reviewed = load_reviewed()
    rows = list(reviewed.values())

    def is_confirmed_ukrainian(row):
        if row.get('flag_non_ukrainian') == 'YES':
            return False
        if row.get('flag_needs_claude_review') == 'YES':
            return row.get('is_ukrainian') == 'YES'
        return True

    def safe_int(val):
        try:
            return int(val)
        except (TypeError, ValueError):
            return None

    # Filter to Ukrainian entries with both dates and migration status
    usable = [
        r for r in rows
        if is_confirmed_ukrainian(r)
        and safe_int(r.get('birth_year'))
        and safe_int(r.get('death_year'))
        and r.get('migration_status') in ('migrated', 'non_migrated')
    ]

    results = []
    def log(line=''):
        print(line)
        results.append(line)

    log("=" * 60)
    log("UKRAINIAN CREATIVE WORKERS — LIFE EXPECTANCY ANALYSIS")
    log("V2 Paper — Berdnyk & Symkin")
    log("=" * 60)
    log()

    # ── Overall counts ─────────────────────────────────────────
    total_ua = sum(1 for r in rows if is_confirmed_ukrainian(r))
    with_dates = sum(
        1 for r in rows
        if is_confirmed_ukrainian(r)
        and safe_int(r.get('birth_year'))
        and safe_int(r.get('death_year'))
    )
    log(f"Total confirmed Ukrainian entries: {total_ua:,}")
    log(f"With both birth + death dates:     {with_dates:,}")
    log(f"Used in life expectancy analysis:  {len(usable):,}")
    log()

    # ── Life expectancy by migration status ────────────────────
    migrated     = [r for r in usable if r['migration_status'] == 'migrated']
    non_migrated = [r for r in usable if r['migration_status'] == 'non_migrated']

    def avg_life(group):
        ages = [safe_int(r['death_year']) - safe_int(r['birth_year']) for r in group]
        ages = [a for a in ages if 10 <= a <= 110]  # filter outliers
        return sum(ages) / len(ages) if ages else 0

    def avg_birth(group):
        years = [safe_int(r['birth_year']) for r in group if safe_int(r['birth_year'])]
        return sum(years) / len(years) if years else 0

    def avg_death(group):
        years = [safe_int(r['death_year']) for r in group if safe_int(r['death_year'])]
        return sum(years) / len(years) if years else 0

    log("── Life Expectancy by Migration Status ──────────────────")
    log(f"{'Group':<20} {'Count':>6}  {'Avg Birth':>10}  {'Avg Death':>10}  {'Avg Life Exp':>13}")
    log("-" * 65)
    for label, group in [("Non-migrants", non_migrated), ("Migrants", migrated)]:
        log(f"{label:<20} {len(group):>6}  {avg_birth(group):>10.1f}  {avg_death(group):>10.1f}  {avg_life(group):>12.1f}y")

    gap = avg_life(migrated) - avg_life(non_migrated)
    log()
    log(f"Life expectancy gap (migrants vs non-migrants): {gap:+.1f} years")
    log()

    # ── Death year clustering ──────────────────────────────────
    from collections import Counter

    log("── Most Common Death Years ──────────────────────────────")
    for label, group in [("Non-migrants", non_migrated), ("Migrants", migrated)]:
        death_years = [safe_int(r['death_year']) for r in group if safe_int(r['death_year'])]
        top5 = Counter(death_years).most_common(5)
        log(f"\n{label}:")
        for year, count in top5:
            avg_age = avg_life([r for r in group if safe_int(r['death_year']) == year])
            log(f"  {year}: {count} deaths  (avg age at death: {avg_age:.0f})")
    log()

    # ── Profession breakdown ───────────────────────────────────
    log("── Life Expectancy by Profession ────────────────────────")

    profession_keywords = {
        'Writers/Poets':     ['письменник', 'поет', 'прозаїк', 'драматург', 'літературознавець'],
        'Visual Artists':    ['художник', 'живописець', 'скульптор', 'графік', 'ілюстратор'],
        'Musicians':         ['композитор', 'диригент', 'піаніст', 'скрипаль', 'співак'],
        'Theatre/Film':      ['актор', 'режисер', 'кінорежисер', 'сценарист'],
        'Architects':        ['архітектор'],
    }

    log(f"{'Profession':<20} {'Count':>6}  {'Migrated':>9}  {'Non-mig':>8}  {'Gap':>6}")
    log("-" * 56)
    for prof_label, keywords in profession_keywords.items():
        prof_rows = [
            r for r in usable
            if any(kw in r.get('profession_raw', '').lower() for kw in keywords)
        ]
        if not prof_rows:
            continue
        pm  = [r for r in prof_rows if r['migration_status'] == 'migrated']
        pnm = [r for r in prof_rows if r['migration_status'] == 'non_migrated']
        g   = avg_life(pm) - avg_life(pnm) if pm and pnm else 0
        log(f"{prof_label:<20} {len(prof_rows):>6}  {avg_life(pm):>8.1f}y  {avg_life(pnm):>7.1f}y  {g:>+5.1f}y")
    log()

    # ── Time period breakdown ──────────────────────────────────
    log("── Non-migrant Deaths by Time Period ────────────────────")
    periods = [
        ('Pre-1917 (Tsarist)',   1800, 1917),
        ('1917–1929 (early Soviet)', 1917, 1930),
        ('1930–1939 (Great Terror)', 1930, 1940),
        ('1940–1945 (WWII)',     1940, 1946),
        ('1946–1953 (Late Stalin)', 1946, 1954),
        ('1954–1991 (post-Stalin)', 1954, 1992),
        ('Post-1991',            1992, 2100),
    ]
    log(f"{'Period':<30} {'Deaths':>7}  {'Avg Age':>8}")
    log("-" * 50)
    for label, start, end in periods:
        group = [
            r for r in non_migrated
            if start <= (safe_int(r['death_year']) or 0) < end
        ]
        log(f"{label:<30} {len(group):>7}  {avg_life(group):>7.1f}y")
    log()

    # ── Summary note for paper ─────────────────────────────────
    log("── Notes for paper ──────────────────────────────────────")
    log(f"V1 dataset: 415 workers (332 non-migrant / 83 migrant)")
    log(f"V2 dataset: {len(usable):,} workers with dates ({len(non_migrated):,} non-migrant / {len(migrated):,} migrant)")
    log(f"V1 life expectancy gap: 9 years (63 vs 72)")
    log(f"V2 life expectancy gap: {gap:+.1f} years")
    log()
    log("Pre-1991 death cutoff: REMOVED in V2 (fixes V1 statistical bias)")
    log("Sources: Encyclopedia of Modern Ukraine (esu.com.ua)")
    log("=" * 60)

    # Save to file
    with open(ANALYSIS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
    print(f"\nResults saved to: {ANALYSIS_FILE}")


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Phase 4: Claude-powered review of Ukrainian creative workers dataset.'
    )
    parser.add_argument(
        '--phase',
        choices=['nationality', 'migration', 'analysis'],
        required=True,
        help='Which phase to run.'
    )
    args = parser.parse_args()

    if args.phase == 'nationality':
        run_nationality_phase()
    elif args.phase == 'migration':
        run_migration_phase()
    elif args.phase == 'analysis':
        run_analysis_phase()
