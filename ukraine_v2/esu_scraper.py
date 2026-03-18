#!/usr/bin/env python3
"""
ESU Creative Workers Scraper — Ukrainian Creative Workers Life Expectancy V2 Paper
Scrapes Encyclopedia of Modern Ukraine (esu.com.ua) for Ukrainian creative workers.

Authors: Elza Berdnyk, Mark Symkin
Source: https://esu.com.ua

Output: esu_creative_workers_raw.csv
Columns: name, birth_year, death_year, birth_location, death_location,
         profession_raw, article_url, notes
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import os
import sys

# ─── Config ───────────────────────────────────────────────────────────────────

BASE_URL = "https://esu.com.ua"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "esu_creative_workers_raw.csv")
SAMPLE_HTML_FILE = os.path.join(os.path.dirname(__file__), "sample_page.html")

# Delay between requests in seconds — be polite to the server
DELAY_BETWEEN_PAGES = 0.8
DELAY_BETWEEN_LETTERS = 2.0

# Ukrainian alphabet (33 letters)
UKRAINIAN_LETTERS = [
    'а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з',
    'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
    'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ',
    'ь', 'ю', 'я'
]

# Creative profession keywords (Ukrainian). Case-insensitive matching.
# These appear in the first sentence of ESU articles after the em-dash.
CREATIVE_KEYWORDS = [
    # Visual arts
    'живописець', 'живописниця', 'художник', 'художниця', 'графік',
    'скульптор', 'скульпторка', 'ілюстратор', 'ілюстраторка',
    'карикатурист', 'карикатуристка', 'гравер', 'акварелістка',
    'акварелі', 'мозаїст', 'іконописець', 'мистецтвознавець',
    'килимарниця', 'писанкарка', 'декоратор',
    # Literature & writing
    'письменник', 'письменниця', 'поет', 'поетеса', 'прозаїк',
    'прозаїкиня', 'драматург', 'романіст', 'романістка', 'новеліст',
    'байкар', 'публіцист', 'публіцистка', 'літературознавець',
    'літературна критик', 'перекладач', 'перекладачка',
    'есеїст', 'мемуарист', 'критик літератур',
    # Music
    'композитор', 'композиторка', 'диригент', 'диригентка',
    'піаніст', 'піаністка', 'скрипаль', 'скрипалька', 'віолончеліст',
    'співак', 'співачка', 'тенор', 'баритон', 'бас', 'сопрано',
    'музикант', 'музикантка', 'музикознавець', 'хормейстер',
    'балетмейстер', 'хореограф', 'хореографка',
    # Theatre
    'актор', 'акторка', 'режисер', 'режисерка', 'театральний режисер',
    'театрознавець', 'сценограф', 'театральний художник',
    # Film
    'кінорежисер', 'кінорежисерка', 'кіноактор', 'кіноакторка',
    'сценарист', 'сценаристка', 'кінематографіст', 'кінооператор',
    'кінодраматург', 'аніматор',
    # Dance
    'танцівник', 'танцівниця', 'балерина', 'балетний',
    # Architecture & design
    'архітектор', 'архітекторка', 'дизайнер', 'дизайнерка',
    # Photography
    'фотограф', 'фотографка',
    # Broad creative / cultural
    'мистець', 'мисткиня', 'культурний діяч', 'культурна діячка',
]

# Nationality adjectives that indicate a NON-Ukrainian creative worker.
# If the profession description starts with one of these, the entry is flagged.
# NOTE: кримськотатарський (Crimean Tatar) is NOT in this list — they lived on
# Ukrainian territory and were targeted by Soviet repressions. Inclusion is
# intentional and can be reviewed in the analysis phase.
NON_UKRAINIAN_NATIONALITY_MARKERS = [
    'грузинськ', 'японськ', 'норвезьк', 'узбецьк', 'башкирськ',
    'казахськ', 'азербайджанськ', 'чеськ', 'данськ', 'болгарськ',
    'молдавськ', 'румунськ', 'білорусьськ', 'литовськ', 'французьк',
    'американськ', 'британськ', 'німецьк', 'австрійськ', 'угорськ',
    'польськ', 'словацьк', 'сербськ', 'хорватськ', 'фінськ', 'шведськ',
    'латиськ', 'естонськ', 'вірменськ', 'туркменськ', 'таджицьк',
    'киргизьк', 'монгольськ', 'китайськ', 'корейськ', 'іранськ',
    'турецьк', 'арабськ', 'ізраїльськ', 'іспанськ', 'португальськ',
    'голландськ', 'бельгійськ', 'швейцарськ', 'австралійськ',
]


# ─── Parsing helpers ──────────────────────────────────────────────────────────

def extract_year(text):
    """Extract a 4-digit year from a text fragment."""
    m = re.search(r'\b(1[5-9]\d{2}|20[0-2]\d)\b', text)
    return int(m.group(1)) if m else None


def parse_dates_and_locations(desc_text):
    """
    Parse birth/death year and location from the parenthetical at the start
    of an ESU article description.

    Formats seen:
      (DD. MM. YYYY, City, Region – DD. MM. YYYY, City)
      (YYYY, City – YYYY, City)
      (DD. MM. YYYY, City)          ← alive or death unknown
      (справж. – Real Name; YYYY, City – YYYY)  ← pseudonym entry
    """
    # Extract the leading parenthetical block
    m = re.match(r'^\s*\(([^)]{5,200})\)', desc_text.strip())
    if not m:
        return None, None, None, None

    inner = m.group(1)

    # Split on em-dash or regular hyphen-dash used as range separator
    # Use a dash that is surrounded by spaces or followed by a location
    parts = re.split(r'\s[–—]\s', inner, maxsplit=1)

    birth_part = parts[0].strip()
    death_part = parts[1].strip() if len(parts) > 1 else ''

    # Handle pseudonym prefix like "справж. – Real Name; YYYY, ..."
    if ';' in birth_part:
        birth_part = birth_part.split(';', 1)[1].strip()

    birth_year = extract_year(birth_part)
    death_year = extract_year(death_part) if death_part else None

    # Extract location: text after the year
    def extract_location(part):
        year_match = re.search(r'\b1[5-9]\d{2}\b|\b20[0-2]\d\b', part)
        if year_match:
            loc = part[year_match.end():].strip().lstrip(',').strip()
            return loc[:80] if loc else ''
        return ''

    birth_loc = extract_location(birth_part)
    death_loc = extract_location(death_part) if death_part else ''

    return birth_year, death_year, birth_loc, death_loc


def extract_profession(desc_text):
    """
    Extract the profession phrase from the article description.
    ESU format: (dates) – profession description...
    """
    # Find the em-dash after the closing parenthesis
    m = re.search(r'\)\s*[–—]\s*(.+?)(?:\.|,|$)', desc_text, re.DOTALL)
    if m:
        profession = m.group(1).strip()
        # Truncate at next sentence or 120 chars
        profession = re.split(r'[.;]', profession)[0].strip()
        return profession[:120]
    return ''


def is_creative_worker(profession_text):
    """Return True if the profession text matches any creative keyword."""
    text_lower = profession_text.lower()
    return any(kw in text_lower for kw in CREATIVE_KEYWORDS)


def is_likely_non_ukrainian(profession_text):
    """
    Return True if the profession description starts with a non-Ukrainian
    nationality marker (e.g. 'грузинський поет', 'японський письменник').
    """
    text_lower = profession_text.lower().strip()
    return any(text_lower.startswith(marker) for marker in NON_UKRAINIAN_NATIONALITY_MARKERS)


# ─── Scraping ─────────────────────────────────────────────────────────────────

def make_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ),
        'Accept-Language': 'uk,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    })
    return session


def fetch_letter_page(letter, page_num, session, retries=2):
    """Fetch one page of a letter listing. Returns HTML string or None."""
    # ESU uses letter.php?s=LETTER&page=N  (page 1 = no page param needed but works with it)
    url = f"{BASE_URL}/letter.php?s={letter}&page={page_num}"
    for attempt in range(retries + 1):
        try:
            r = session.get(url, timeout=20)
            if r.status_code == 200:
                return r.text
            print(f"    HTTP {r.status_code} for {url}")
            return None
        except requests.RequestException as e:
            if attempt < retries:
                time.sleep(3)
            else:
                print(f"    Request failed: {e}")
    return None


def get_total_pages(html):
    """Extract total number of pages from 'Стор. 1 із N' pagination text."""
    m = re.search(r'із\s+(\d+)', html)
    return int(m.group(1)) if m else 1


def parse_entries(html):
    """
    Parse article entries from a letter listing page.
    Returns list of dicts: {name, birth_year, death_year, birth_loc,
                             death_loc, profession_raw, article_url}
    """
    soup = BeautifulSoup(html, 'html.parser')
    entries = []

    # Structure: <h2><a href="article-NNNNN">Name</a></h2>
    #            <p>  (date info) – profession...</p>
    for h2 in soup.find_all('h2'):
        link = h2.find('a', href=re.compile(r'^article-\d+'))
        if not link:
            continue

        name = link.get_text(strip=True)
        article_url = f"{BASE_URL}/{link['href']}"

        # Get the next sibling <p> for the description
        desc_tag = h2.find_next_sibling('p')
        if not desc_tag:
            continue
        desc_text = desc_tag.get_text(' ', strip=True)

        profession_raw = extract_profession(desc_text)

        if not is_creative_worker(profession_raw):
            continue

        birth_year, death_year, birth_loc, death_loc = parse_dates_and_locations(desc_text)

        entries.append({
            'name': name,
            'birth_year': birth_year or '',
            'death_year': death_year or '',
            'birth_location': birth_loc or '',
            'death_location': death_loc or '',
            'profession_raw': profession_raw,
            'flag_non_ukrainian': 'YES' if is_likely_non_ukrainian(profession_raw) else '',
            'article_url': article_url,
            'notes': desc_text[:300],
        })

    return entries


# ─── Progress tracking ────────────────────────────────────────────────────────

def load_progress():
    """Return set of already-scraped article URLs (for resume support)."""
    if not os.path.exists(OUTPUT_FILE):
        return set(), []
    seen_urls = set()
    rows = []
    with open(OUTPUT_FILE, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            seen_urls.add(row['article_url'])
            rows.append(row)
    return seen_urls, rows


def save_to_csv(rows, mode='w'):
    fieldnames = [
        'name', 'birth_year', 'death_year',
        'birth_location', 'death_location',
        'profession_raw', 'flag_non_ukrainian', 'article_url', 'notes'
    ]
    with open(OUTPUT_FILE, mode, newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if mode == 'w':
            writer.writeheader()
        writer.writerows(rows)


# ─── Main ─────────────────────────────────────────────────────────────────────

def scrape(start_letter=None, max_pages_per_letter=None):
    """
    Main scraping loop.
    - start_letter: resume from this letter (e.g. 'к') if a previous run was interrupted
    - max_pages_per_letter: limit pages per letter (useful for testing)
    """
    session = make_session()
    seen_urls, existing_rows = load_progress()

    if existing_rows:
        print(f"Resuming: {len(existing_rows)} entries already collected.")
        append_mode = True
    else:
        append_mode = False
        save_to_csv([], mode='w')  # write header

    total_found = len(existing_rows)
    new_rows_buffer = []

    # Save a sample HTML file from the first letter for debugging
    save_sample = not os.path.exists(SAMPLE_HTML_FILE)

    letters_to_process = UKRAINIAN_LETTERS
    if start_letter:
        try:
            idx = UKRAINIAN_LETTERS.index(start_letter.lower())
            letters_to_process = UKRAINIAN_LETTERS[idx:]
        except ValueError:
            print(f"Warning: '{start_letter}' not found in alphabet, starting from beginning.")

    for letter in letters_to_process:
        print(f"\n{'='*55}")
        print(f"  Letter: {letter.upper()}")
        print(f"{'='*55}")

        # Fetch page 1 to get total pages
        html = fetch_letter_page(letter, 1, session)
        if not html:
            print(f"  Could not fetch letter {letter}, skipping.")
            time.sleep(DELAY_BETWEEN_LETTERS)
            continue

        if save_sample:
            with open(SAMPLE_HTML_FILE, 'w', encoding='utf-8') as sf:
                sf.write(html)
            print(f"  Saved sample HTML to {SAMPLE_HTML_FILE}")
            save_sample = False

        total_pages = get_total_pages(html)
        if max_pages_per_letter:
            total_pages = min(total_pages, max_pages_per_letter)

        print(f"  Total pages: {total_pages}")

        letter_found = 0

        for page_num in range(1, total_pages + 1):
            if page_num > 1:
                html = fetch_letter_page(letter, page_num, session)
                if not html:
                    print(f"  Page {page_num}: failed, skipping.")
                    time.sleep(2)
                    continue

            entries = parse_entries(html)
            new_entries = [e for e in entries if e['article_url'] not in seen_urls]

            for entry in new_entries:
                seen_urls.add(entry['article_url'])
                new_rows_buffer.append(entry)
                total_found += 1
                letter_found += 1
                print(f"  ✓ {entry['name']} ({entry['birth_year']}–{entry['death_year']}) | {entry['profession_raw'][:50]}")

            # Flush to disk every 50 new entries
            if len(new_rows_buffer) >= 50:
                save_to_csv(new_rows_buffer, mode='a')
                new_rows_buffer = []
                print(f"  [saved — {total_found} total so far]")

            if page_num % 20 == 0:
                print(f"  Page {page_num}/{total_pages} — {letter_found} found this letter, {total_found} total")

            time.sleep(DELAY_BETWEEN_PAGES)

        # Flush any remaining rows for this letter
        if new_rows_buffer:
            save_to_csv(new_rows_buffer, mode='a')
            new_rows_buffer = []

        print(f"  Letter {letter.upper()} done: {letter_found} creative workers found")
        time.sleep(DELAY_BETWEEN_LETTERS)

    print(f"\n{'='*55}")
    print(f"COMPLETE — {total_found} creative workers saved to:")
    print(f"  {OUTPUT_FILE}")


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Scrape Encyclopedia of Modern Ukraine for creative workers.'
    )
    parser.add_argument(
        '--start', metavar='LETTER',
        help='Resume from this Ukrainian letter (e.g. к). Default: start from а.'
    )
    parser.add_argument(
        '--test', action='store_true',
        help='Test mode: only process first 3 pages per letter.'
    )
    args = parser.parse_args()

    max_pages = 3 if args.test else None

    print("ESU Creative Workers Scraper")
    print("Encyclopedia of Modern Ukraine — esu.com.ua")
    print(f"Output: {OUTPUT_FILE}")
    if args.test:
        print("MODE: TEST (3 pages per letter)")
    print()

    scrape(start_letter=args.start, max_pages_per_letter=max_pages)
