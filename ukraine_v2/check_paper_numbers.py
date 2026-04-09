"""
check_paper_numbers.py
======================
Loads esu_creative_workers_v2_6.csv using identical logic to generate_analysis.py,
recomputes every statistic from scratch, then checks each numeric claim in
PAPER_DRAFT.md against computed values.

Usage:
    python3 ukraine_v2/check_paper_numbers.py

Exit code 0 = all checks pass. Exit code 1 = at least one FAIL.
"""

import csv
import math
import os
import statistics
import sys
from scipy import stats as scipy_stats

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
HERE     = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, 'esu_creative_workers_v2_6.csv')

# ---------------------------------------------------------------------------
# ANSI colour helpers (no external dep)
# ---------------------------------------------------------------------------
GREEN  = '\033[92m'
RED    = '\033[91m'
YELLOW = '\033[93m'
RESET  = '\033[0m'
BOLD   = '\033[1m'

_results = []   # list of (label, passed, computed, claimed, tol)


def check(label, computed, claimed, tol=0.015):
    """Record a PASS/FAIL comparison.

    tol: absolute tolerance for floats; for ints tol=0 means exact.
    """
    if claimed is None:
        return  # skip
    try:
        diff = abs(float(computed) - float(claimed))
        passed = diff <= tol
    except (TypeError, ValueError):
        passed = (computed == claimed)
        diff = 0
    _results.append((label, passed, computed, claimed, tol))


def checkn(label, computed, claimed):
    """Exact-match integer count check."""
    passed = (int(computed) == int(claimed))
    _results.append((label, passed, int(computed), int(claimed), 0))

# ---------------------------------------------------------------------------
# IDENTICAL DATA-LOADING CODE (copied from generate_analysis.py)
# ---------------------------------------------------------------------------

PROFESSION_KEYWORDS = {
    'Writers/Poets': [
        'письменник', 'поет', 'прозаїк', 'драматург', 'літературознавець',
        'байкар', 'публіцист', 'романіст', 'есеїст', 'новеліст', 'перекладач',
    ],
    'Visual Artists': [
        'художник', 'живописець', 'скульптор', 'графік', 'ілюстратор',
        'мистецтвознавець', 'декоратор', 'гравер', 'акварел', 'мозаїст', 'іконописець',
    ],
    'Musicians/Composers': [
        'композитор', 'диригент', 'піаніст', 'скрипаль', 'співак', 'музикант',
        'музикознавець', 'хормейстер', 'хореограф', 'балетмейстер',
        'тенор', 'баритон', 'сопрано',
    ],
    'Theatre/Film': [
        'актор', 'режисер', 'кінорежисер', 'сценарист', 'кінооператор',
        'театрознавець', 'сценограф', 'аніматор',
    ],
    'Architects': [
        'архітектор', 'дизайнер',
    ],
    'Other Creative': [
        'мистець', 'культурний діяч', 'фотограф',
    ],
}

ALL_GROUPS = ['migrated', 'non_migrated', 'internal_transfer', 'deported']


def classify_profession(raw):
    if not raw:
        return 'Other Creative'
    lower = raw.lower()
    for category, keywords in PROFESSION_KEYWORDS.items():
        for kw in keywords:
            if kw in lower:
                return category
    return 'Other Creative'


def safe_int(val):
    try:
        v = int(float(str(val).strip()))
        return v if v > 0 else None
    except (ValueError, TypeError):
        return None


def le_values(group):
    return [r['_le'] for r in group if r['_le'] is not None]


def describe(group):
    les = le_values(group)
    if not les:
        return {'n': 0, 'mean': None, 'median': None, 'std': None,
                'ci95_lo': None, 'ci95_hi': None}
    n  = len(les)
    mn = statistics.mean(les)
    sd = statistics.stdev(les) if n > 1 else 0
    se = sd / math.sqrt(n)
    t  = scipy_stats.t.ppf(0.975, df=n - 1) if n > 1 else 0
    return {
        'n':       n,
        'mean':    round(mn, 2),
        'median':  round(statistics.median(les), 2),
        'std':     round(sd, 2),
        'se':      round(se, 4),
        'ci95_lo': round(mn - t * se, 2),
        'ci95_hi': round(mn + t * se, 2),
    }


def cohens_d(a, b):
    if len(a) < 2 or len(b) < 2:
        return None
    pooled = math.sqrt(
        ((len(a) - 1) * statistics.variance(a) + (len(b) - 1) * statistics.variance(b))
        / (len(a) + len(b) - 2)
    )
    return round((statistics.mean(a) - statistics.mean(b)) / pooled, 4) if pooled else 0.0


def mannwhitney(a, b):
    if len(a) < 3 or len(b) < 3:
        return None, None
    res = scipy_stats.mannwhitneyu(a, b, alternative='two-sided')
    return round(res.statistic, 2), round(res.pvalue, 6)


def cliffs_delta(x, y):
    x, y = list(x), list(y)
    n1, n2 = len(x), len(y)
    if n1 == 0 or n2 == 0:
        return float('nan')
    greater = sum(1 for xi in x for yj in y if xi > yj)
    less    = sum(1 for xi in x for yj in y if xi < yj)
    return (greater - less) / (n1 * n2)


# ---------------------------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------------------------
print(f"Loading {CSV_PATH} …")
raw_rows = []
with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        raw_rows.append(row)

for r in raw_rows:
    r['_by']   = safe_int(r.get('birth_year'))
    r['_dy']   = safe_int(r.get('death_year'))
    r['_ms']   = r.get('migration_status', '').strip().lower()
    r['_le']   = (r['_dy'] - r['_by']) if (r['_by'] and r['_dy']) else None
    r['_prof'] = classify_profession(r.get('profession_raw', ''))

total_scraped       = len(raw_rows)
excluded_pre_soviet = [r for r in raw_rows if r['_ms'] == 'excluded_pre_soviet']
excluded_galicia    = [r for r in raw_rows if r['_ms'] == 'excluded_galicia_pre_annexation']
still_alive         = [r for r in raw_rows if r['_ms'] == 'alive']
unknown_status      = [r for r in raw_rows if r['_ms'] == 'unknown']
non_ukrainian       = [r for r in raw_rows
                       if r.get('flag_non_ukrainian', '').strip().upper() == 'YES'
                       or r.get('is_ukrainian', '').strip().upper() == 'NO']
VALID_MS = set(ALL_GROUPS)
analysable  = [r for r in raw_rows
               if r['_by'] and r['_dy'] and r['_ms'] in VALID_MS and r['_le'] is not None]
missing_dates = [r for r in raw_rows
                 if r['_ms'] in VALID_MS and (not r['_by'] or not r['_dy'])]
groups = {ms: [r for r in analysable if r['_ms'] == ms] for ms in ALL_GROUPS}
migrated          = groups['migrated']
non_migrated      = groups['non_migrated']
internal_transfer = groups['internal_transfer']
deported          = groups['deported']

print(f"  Scraped: {total_scraped:,}  |  Analysable: {len(analysable):,}")
print(f"  mig={len(migrated)}  nm={len(non_migrated)}  it={len(internal_transfer)}  dep={len(deported)}")

# ---------------------------------------------------------------------------
# COMPUTE KEY STATISTICS
# ---------------------------------------------------------------------------
descs = {ms: describe(groups[ms]) for ms in ALL_GROUPS}

le_m  = le_values(migrated)
le_nm = le_values(non_migrated)
le_it = le_values(internal_transfer)
le_d  = le_values(deported)

gap_mn  = round(statistics.mean(le_m)  - statistics.mean(le_nm), 2)
gap_md  = round(statistics.mean(le_m)  - statistics.mean(le_d),  2)
gap_nmd = round(statistics.mean(le_nm) - statistics.mean(le_d),  2)
gap_nmit= round(statistics.mean(le_nm) - statistics.mean(le_it), 2)

d_mn   = cohens_d(le_m, le_nm)
d_md   = cohens_d(le_m, le_d)
d_nmd  = cohens_d(le_nm, le_d)
d_nmit = cohens_d(le_nm, le_it)

_, p_mn   = mannwhitney(le_m, le_nm)
_, p_md   = mannwhitney(le_m, le_d)
_, p_nmd  = mannwhitney(le_nm, le_d)
_, p_nmit = mannwhitney(le_nm, le_it)

cd_mn = round(cliffs_delta(le_m, le_nm), 2)

# Sensitivity: remove top n_err longest-lived migrants, same as FIG 14 chart
error_rates = [0, 1, 2, 3.2, 5, 7.5, 10]
base_nm_mean = statistics.mean(le_nm)
sens_gaps = []
for er in error_rates:
    n_err   = int(len(migrated) * er / 100)
    sorted_m = sorted(le_m, reverse=True)
    adj_m    = sorted_m[n_err:]
    if adj_m:
        sens_gaps.append(round(statistics.mean(adj_m) - base_nm_mean, 2))
    else:
        sens_gaps.append(round(gap_mn, 2))

sens_at_3_2  = sens_gaps[error_rates.index(3.2)]
sens_at_10   = sens_gaps[error_rates.index(10)]

# ---------------------------------------------------------------------------
# PERIOD ANALYSIS (non-migrants only)
# ---------------------------------------------------------------------------
PERIODS = [
    ('1921–1929', lambda y: 1921 <= y <= 1929),
    ('1930–1933', lambda y: 1930 <= y <= 1933),
    ('1934–1938', lambda y: 1934 <= y <= 1938),
    ('1939–1945', lambda y: 1939 <= y <= 1945),
    ('1946–1953', lambda y: 1946 <= y <= 1953),
    ('1954–1964', lambda y: 1954 <= y <= 1964),
    ('1965–1991', lambda y: 1965 <= y <= 1991),
    ('Post-1991', lambda y: y > 1991),
]
nm_dy    = [r for r in non_migrated if r['_dy']]
total_nm = len(nm_dy)
periods_nm = {}
for label, fn in PERIODS:
    sub  = [r for r in nm_dy if fn(r['_dy'])]
    ages = [r['_le'] for r in sub if r['_le'] is not None]
    periods_nm[label] = {
        'deaths': len(sub),
        'avg_age': round(statistics.mean(ages), 1) if ages else None,
        'pct': round(100 * len(sub) / total_nm, 1) if total_nm else 0,
    }

# 1937 spotlight
def year1937(group):
    sub  = [r for r in group if r['_dy'] == 1937]
    ages = [r['_le'] for r in sub if r['_le'] is not None]
    return len(sub), (round(statistics.mean(ages), 1) if ages else None)

nm1937_n,  nm1937_avg  = year1937(non_migrated)
dep1937_n, dep1937_avg = year1937(deported)
it1937_n,  it1937_avg  = year1937(internal_transfer)
mig1937_n, mig1937_avg = year1937(migrated)
total1937 = nm1937_n + dep1937_n + it1937_n + mig1937_n

# ---------------------------------------------------------------------------
# PROFESSION BREAKDOWN
# ---------------------------------------------------------------------------
profs = list(PROFESSION_KEYWORDS.keys())
prof_data = {}
for prof in profs:
    def pg(ms, p=prof): return [r for r in groups[ms] if r['_prof'] == p]
    def me(ms, p=prof):
        v = le_values(pg(ms))
        return (round(statistics.mean(v), 1) if v else None, len(v))
    prof_data[prof] = {
        'mig_le':  me('migrated')[0],   'mig_n':  me('migrated')[1],
        'nm_le':   me('non_migrated')[0],'nm_n':   me('non_migrated')[1],
        'dep_le':  me('deported')[0],    'dep_n':  me('deported')[1],
    }

# ---------------------------------------------------------------------------
# BIRTH COHORT ANALYSIS
# ---------------------------------------------------------------------------
cohorts = {}
for dec in range(1840, 1990, 10):
    def in_dec(r, d=dec): return r['_by'] and d <= r['_by'] < d + 10
    coh = {ms: [r for r in groups[ms] if in_dec(r)] for ms in ALL_GROUPS}
    def cm(ms, c=coh):
        v = le_values(c[ms])
        return (round(statistics.mean(v), 1) if v else None, len(c[ms]))
    cohorts[dec] = {
        'mig':  cm('migrated'),
        'nm':   cm('non_migrated'),
        'dep':  cm('deported'),
        'it':   cm('internal_transfer'),
    }

# ---------------------------------------------------------------------------
# DEATH AGE DISTRIBUTION (§4.8)
# ---------------------------------------------------------------------------
def count_les(group, lo, hi):
    return sum(1 for r in group if r['_le'] is not None and lo <= r['_le'] < hi)

def count_le_lt(group, age):
    return sum(1 for r in group if r['_le'] is not None and r['_le'] < age)

def count_le_ge(group, age):
    return sum(1 for r in group if r['_le'] is not None and r['_le'] >= age)

nm_lt50  = count_les(non_migrated, 0, 50)
mig_lt50 = count_les(migrated, 0, 50)
nm_lt30  = count_le_lt(non_migrated, 30)
mig_lt30 = count_le_lt(migrated, 30)
nm_30_39 = count_les(non_migrated, 30, 40)
mig_30_39= count_les(migrated, 30, 40)
nm_40_49 = count_les(non_migrated, 40, 50)
mig_40_49= count_les(migrated, 40, 50)
nm_90p   = count_le_ge(non_migrated, 90)
mig_90p  = count_le_ge(migrated, 90)

nm_lt50_pct  = round(100 * nm_lt50  / len(non_migrated), 1)
mig_lt50_pct = round(100 * mig_lt50 / len(migrated), 1)
nm_lt30_pct  = round(100 * nm_lt30  / len(non_migrated), 3)
mig_lt30_pct = round(100 * mig_lt30 / len(migrated), 3)
nm_90p_pct   = round(100 * nm_90p   / len(non_migrated), 1)
mig_90p_pct  = round(100 * mig_90p  / len(migrated), 1)

# ---------------------------------------------------------------------------
# GEOGRAPHIC (Table 6) — requires birth_city field
# ---------------------------------------------------------------------------
# Geographic: use same exact-match logic as fig12 (Counter on raw birth_location)
import collections as _collections

_birth_all_p = _collections.Counter()
_birth_mig_p = _collections.Counter()
for r in analysable:
    bl = str(r.get('birth_location', '')).strip()
    if bl:
        _birth_all_p[bl] += 1
        if r['_ms'] == 'migrated':
            _birth_mig_p[bl] += 1

# Fuzzy match for each paper-reported city (Ukrainian keyword in birth_location)
# Table 6 methodology: exact birth_location string match on analysable rows only
# (same population as fig12 — consistent with the rest of the analysis)
CITY_EXACT_LOCS = {
    'Lviv':              'Львів',
    'Ternopil':          'Тернопіль',
    'Chernivtsi':        'Чернівці',
    'Kyiv':              'Київ',
    'Donetsk (Stalino)': 'м. Сталіно, нині Донецьк',
}

def city_stats(loc_str):
    hits  = [r for r in analysable if (r.get('birth_location', '') or '').strip() == loc_str]
    n_mig = sum(1 for r in hits if r['_ms'] == 'migrated')
    pct   = round(100 * n_mig / len(hits), 1) if hits else 0.0
    return len(hits), pct

city_computed = {k: city_stats(v) for k, v in CITY_EXACT_LOCS.items()}

# ---------------------------------------------------------------------------
# RUN ALL CHECKS
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print(f"{BOLD}PAPER NUMBER CHECKS — V2.6 DATASET{RESET}")
print("=" * 70)

# ── §3.4 / Abstract dataset size ─────────────────────────────────────────────
print(f"\n{BOLD}── DATASET OVERVIEW ──{RESET}")
checkn("Total scraped (§3.3, Abstract)",         total_scraped,       16215)
checkn("Analysable total (§3.4, Abstract)",      len(analysable),     8590)
checkn("n — Migrated",                           len(migrated),       1324)
checkn("n — Non-migrated",                       len(non_migrated),   5960)
checkn("n — Internal transfer",                  len(internal_transfer), 1111)
checkn("n — Deported",                           len(deported),       195)

# ── Table 1 — Life expectancy ─────────────────────────────────────────────────
print(f"\n{BOLD}── TABLE 1: LIFE EXPECTANCY BY GROUP ──{RESET}")
for ms, label, paper in [
    ('migrated',          'Migrated',          {'mean':75.42, 'median':77, 'std':13.84, 'ci95_lo':74.68, 'ci95_hi':76.17}),
    ('non_migrated',      'Non-migrated',      {'mean':71.44, 'median':73, 'std':13.61, 'ci95_lo':71.10, 'ci95_hi':71.79}),
    ('internal_transfer', 'Internal transfer', {'mean':71.09, 'median':73, 'std':13.61, 'ci95_lo':70.29, 'ci95_hi':71.89}),
    ('deported',          'Deported',          {'mean':49.39, 'median':46, 'std':15.38, 'ci95_lo':47.22, 'ci95_hi':51.57}),
]:
    d = descs[ms]
    check(f"  {label} — mean",    d['mean'],    paper['mean'],    0.015)
    check(f"  {label} — median",  d['median'],  paper['median'],  0.5)
    check(f"  {label} — SD",      d['std'],     paper['std'],     0.015)
    check(f"  {label} — CI lo",   d['ci95_lo'], paper['ci95_lo'], 0.015)
    check(f"  {label} — CI hi",   d['ci95_hi'], paper['ci95_hi'], 0.015)

# ── §4.2 Gaps and effect sizes ────────────────────────────────────────────────
print(f"\n{BOLD}── §4.2: GAPS, EFFECT SIZES, P-VALUES ──{RESET}")
check("Gap mig vs nm (Abstract, §4.1, §4.2, §6)", gap_mn, 3.98, 0.015)
check("Cohen's d mig vs nm (Abstract, §4.2)",       round(d_mn, 3), 0.292, 0.002)
check("Cliff's delta mig vs nm (Abstract, §3.8)",   cd_mn, 0.18, 0.01)
check("Gap mig vs dep (Abstract, §4.1, §4.2)",     gap_md, 26.03, 0.015)
check("Cohen's d mig vs dep (§4.2)",                round(d_md, 3), 1.853, 0.002)
check("Gap nm vs dep (Abstract, §4.1, §4.2, §5.1)",gap_nmd, 22.05, 0.015)
check("Cohen's d nm vs dep (§4.2)",                 round(d_nmd, 3), 1.613, 0.002)
check("Gap nm vs IT (§4.1, §4.2, Abstract)",        gap_nmit, 0.35, 0.015)
check("Cohen's d nm vs IT (§4.2)",                  round(d_nmit, 3), 0.026, 0.002)
check("p-value nm vs IT (§4.1, §4.2)",              round(p_nmit, 3), 0.271, 0.002)

# ── §4.2 Sensitivity ─────────────────────────────────────────────────────────
print(f"\n{BOLD}── §4.2: SENSITIVITY ANALYSIS ──{RESET}")
check("Sensitivity gap at 3.2% (§4.2)",  sens_at_3_2, 3.24, 0.015)
check("Sensitivity gap at 10% (§4.2)",   sens_at_10,  1.84, 0.015)

# ── Table 2 — Profession ─────────────────────────────────────────────────────
print(f"\n{BOLD}── TABLE 2: PROFESSION BREAKDOWN ──{RESET}")
PAPER_PROF = {
    'Writers/Poets':      {'mig_le':74.5,'mig_n':389, 'nm_le':70.5,'nm_n':1754,'dep_le':46.0,'dep_n':123},
    'Visual Artists':     {'mig_le':74.8,'mig_n':385, 'nm_le':71.6,'nm_n':1954,'dep_le':56.9,'dep_n':39},
    'Musicians/Composers':{'mig_le':75.8,'mig_n':308, 'nm_le':71.4,'nm_n':916, 'dep_le':44.9,'dep_n':14},
    'Theatre/Film':       {'mig_le':75.5,'mig_n':64,  'nm_le':71.8,'nm_n':731, 'dep_le':55.2,'dep_n':9},
    'Architects':         {'mig_le':79.0,'mig_n':61,  'nm_le':73.2,'nm_n':384, 'dep_le':61.0,'dep_n':4},
    'Other Creative':     {'mig_le':77.7,'mig_n':117, 'nm_le':73.3,'nm_n':221, 'dep_le':63.5,'dep_n':6},
}
for prof, paper in PAPER_PROF.items():
    d = prof_data[prof]
    short = prof[:16]
    check(f"  {short} — mig LE",  d['mig_le'], paper['mig_le'], 0.05)
    checkn(f"  {short} — mig n",  d['mig_n'],  paper['mig_n'])
    check(f"  {short} — nm LE",   d['nm_le'],  paper['nm_le'],  0.05)
    checkn(f"  {short} — nm n",   d['nm_n'],   paper['nm_n'])
    if paper['dep_n'] >= 3:
        check(f"  {short} — dep LE", d['dep_le'], paper['dep_le'], 0.05)
    checkn(f"  {short} — dep n",  d['dep_n'],  paper['dep_n'])

# ── Table 3 — Period analysis ─────────────────────────────────────────────────
print(f"\n{BOLD}── TABLE 3: NON-MIGRANT DEATHS BY PERIOD ──{RESET}")
PAPER_PERIODS = {
    '1921–1929': {'deaths': 95,   'avg_age': 58.4, 'pct': 1.6},
    '1930–1933': {'deaths': 54,   'avg_age': 59.5, 'pct': 0.9},
    '1934–1938': {'deaths': 96,   'avg_age': 55.8, 'pct': 1.6},
    '1939–1945': {'deaths': 207,  'avg_age': 55.1, 'pct': 3.5},
    '1946–1953': {'deaths': 124,  'avg_age': 62.6, 'pct': 2.1},
    '1954–1964': {'deaths': 236,  'avg_age': 66.6, 'pct': 4.0},
    '1965–1991': {'deaths': 1432, 'avg_age': 69.2, 'pct': 24.0},
    'Post-1991': {'deaths': 3716, 'avg_age': 74.7, 'pct': 62.3},
}
for p_label, paper in PAPER_PERIODS.items():
    d = periods_nm.get(p_label)
    if d is None:
        continue
    checkn(f"  {p_label} — deaths",    d['deaths'],   paper['deaths'])
    check(f"  {p_label} — avg age",    d['avg_age'],  paper['avg_age'], 0.1)
    check(f"  {p_label} — % total",    d['pct'],      paper['pct'],     0.1)

# ── Table 4 — 1937 spotlight ─────────────────────────────────────────────────
print(f"\n{BOLD}── TABLE 4: 1937 DEATHS ──{RESET}")
checkn("1937 — Non-migrated deaths",  nm1937_n,  25)
check( "1937 — Non-migrated avg age", nm1937_avg, 49.4, 0.1)
checkn("1937 — Deported deaths",      dep1937_n, 67)
check( "1937 — Deported avg age",     dep1937_avg, 42.7, 0.1)
checkn("1937 — Internal transfer deaths", it1937_n, 1)
# it avg age = 25.0 (only 1 person, exact)
check( "1937 — IT avg age",           it1937_avg, 25.0, 0.5)
checkn("1937 — Migrated deaths",      mig1937_n, 11)
check( "1937 — Migrated avg age",     mig1937_avg, 64.3, 0.15)
checkn("1937 — Total deaths",         total1937, 104)

# ── Table 5 — Birth cohort ───────────────────────────────────────────────────
print(f"\n{BOLD}── TABLE 5: BIRTH COHORT ANALYSIS ──{RESET}")
PAPER_COHORTS = {
    1880: {'mig_le':74.3,'mig_n':176,'nm_le':69.3,'nm_n':260,'dep_le':57.3,'dep_n':32,'gap':5.0},
    1890: {'mig_le':75.4,'mig_n':232,'nm_le':70.8,'nm_n':325,'dep_le':44.7,'dep_n':62,'gap':4.6},
    1900: {'mig_le':75.2,'mig_n':218,'nm_le':72.4,'nm_n':650,'dep_le':44.2,'dep_n':59,'gap':2.8},
    1910: {'mig_le':77.6,'mig_n':219,'nm_le':74.9,'nm_n':809,'dep_le':46.9,'dep_n':14,'gap':2.7},
    1920: {'mig_le':78.9,'mig_n':167,'nm_le':75.4,'nm_n':1260,'dep_le':53.2,'dep_n':6,'gap':3.5},
    1930: {'mig_le':74.9,'mig_n':92, 'nm_le':73.2,'nm_n':1136,'dep_le':78.3,'dep_n':4,'gap':1.7},
}
for dec, paper in PAPER_COHORTS.items():
    c = cohorts[dec]
    mig_le, mig_n = c['mig']
    nm_le,  nm_n  = c['nm']
    dep_le, dep_n = c['dep']
    check(f"  {dec}s — mig LE",  mig_le, paper['mig_le'], 0.1)
    checkn(f"  {dec}s — mig n",  mig_n,  paper['mig_n'])
    check(f"  {dec}s — nm LE",   nm_le,  paper['nm_le'],  0.1)
    checkn(f"  {dec}s — nm n",   nm_n,   paper['nm_n'])
    if paper['dep_n'] >= 5:
        check(f"  {dec}s — dep LE",  dep_le, paper['dep_le'], 0.1)
    checkn(f"  {dec}s — dep n",  dep_n,  paper['dep_n'])
    # gap = mig_le - nm_le
    if mig_le is not None and nm_le is not None:
        comp_gap = round(mig_le - nm_le, 1)
        check(f"  {dec}s — gap (M-NM)", comp_gap, paper['gap'], 0.15)

# ── §4.8 Death age distribution ──────────────────────────────────────────────
print(f"\n{BOLD}── §4.8: DEATH AGE DISTRIBUTION ──{RESET}")
check("nm % died <50 (§4.8)",          nm_lt50_pct,  6.6, 0.15)
check("mig % died <50 (§4.8)",         mig_lt50_pct, 5.2, 0.15)
checkn("nm died <30 (§4.8)",           nm_lt30,  41)
checkn("mig died <30 (§4.8)",          mig_lt30, 4)
check("nm % died <30 (§4.8)",          round(nm_lt30_pct, 2),  0.69, 0.02)
check("mig % died <30 (§4.8)",         round(mig_lt30_pct, 2), 0.30, 0.02)
checkn("nm age 30-39 (§4.8)",          nm_30_39,  117)
checkn("mig age 30-39 (§4.8)",         mig_30_39, 26)
checkn("nm age 40-49 (§4.8)",          nm_40_49,  238)
checkn("mig age 40-49 (§4.8)",         mig_40_49, 38)
checkn("nm age 90+ (§4.8)",            nm_90p,   373)
checkn("mig age 90+ (§4.8)",           mig_90p,  199)
check("nm % age 90+ (§4.8)",           nm_90p_pct,  6.3, 0.15)
check("mig % age 90+ (§4.8)",          mig_90p_pct, 15.0, 0.15)

# ── Table 6 — Geography ──────────────────────────────────────────────────────
print(f"\n{BOLD}── TABLE 6: GEOGRAPHIC MIGRATION RATES ──{RESET}")
print(f"  (methodology: exact birth_location match on all 16,215 rows)")
PAPER_CITIES = {
    'Lviv':              {'n': 165,  'pct_mig': 44.8},
    'Ternopil':          {'n': 17,   'pct_mig': 52.9},
    'Chernivtsi':        {'n': 23,   'pct_mig': 34.8},
    'Kyiv':              {'n': 454,  'pct_mig': 13.9},
    'Donetsk (Stalino)': {'n': 14,   'pct_mig': 0.0},
}
for city_key, paper in PAPER_CITIES.items():
    n_comp, pct_comp = city_computed.get(city_key, (0, 0.0))
    checkn(f"  {city_key} — n",         n_comp,   paper['n'])
    check(f"  {city_key} — % migrated", pct_comp, paper['pct_mig'], 0.15)

# ── §5.1 discussion cross-refs ────────────────────────────────────────────────
print(f"\n{BOLD}── §5.1 DISCUSSION CROSS-REFS ──{RESET}")
# "89 non-migrated and deported deaths concentrated in 1937"
combined_1937 = nm1937_n + dep1937_n
checkn("1937 nm+dep deaths = 92 (§5.1)", combined_1937, 92)
# "average age ~44 for those two groups" — we compute blended avg
all_1937_staying = [r for r in non_migrated + deported if r['_dy'] == 1937]
ages_1937_staying = [r['_le'] for r in all_1937_staying if r['_le'] is not None]
if ages_1937_staying:
    blended_1937_avg = round(statistics.mean(ages_1937_staying), 1)
    check("1937 nm+dep blended avg age ~44 (§5.1, §6)", blended_1937_avg, 44.0, 1.5)

# "the 11 migrants who died in 1937 did so at a mean age of 64.3"
check("1937 migrated avg age 64.3 (§5.1, §6)", mig1937_avg, 64.3, 0.2)

# §5.5 "average age of 43.4 years during 1934–1938" — deported group period
dep_dy = [r for r in deported if r['_dy']]
dep_terror = [r for r in dep_dy if 1934 <= r['_dy'] <= 1938]
dep_terror_ages = [r['_le'] for r in dep_terror if r['_le'] is not None]
dep_terror_avg = round(statistics.mean(dep_terror_ages), 1) if dep_terror_ages else None
check("Deported 1934–38 avg age 43.4 (§5.5, §6)", dep_terror_avg, 43.4, 0.15)

dep_wwii = [r for r in dep_dy if 1939 <= r['_dy'] <= 1945]
dep_wwii_ages = [r['_le'] for r in dep_wwii if r['_le'] is not None]
dep_wwii_avg = round(statistics.mean(dep_wwii_ages), 1) if dep_wwii_ages else None
check("Deported 1939–45 avg age 45.0 (§5.5)", dep_wwii_avg, 45.0, 0.15)

# ---------------------------------------------------------------------------
# PRINT RESULTS
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print(f"{BOLD}RESULTS{RESET}")
print("=" * 70)

passes = 0
fails  = 0
skips  = 0

for label, passed, computed, claimed, tol in _results:
    if passed is None:
        # skipped / missing field
        print(f"  {YELLOW}SKIP{RESET}  {label}")
        skips += 1
    elif passed:
        print(f"  {GREEN}PASS{RESET}  {label}  (computed={computed}, claimed={claimed})")
        passes += 1
    else:
        print(f"  {RED}FAIL{RESET}  {label}")
        print(f"        computed={computed}  claimed={claimed}  tol=±{tol}")
        fails += 1

print()
print("=" * 70)
colour = GREEN if fails == 0 else RED
print(f"{BOLD}{colour}{passes} PASS  |  {fails} FAIL  |  {skips} SKIP{RESET}")
print("=" * 70)

if fails > 0:
    print(f"\n{RED}{BOLD}ACTION REQUIRED: {fails} paper claim(s) do not match computed values.{RESET}")
    sys.exit(1)
else:
    print(f"\n{GREEN}{BOLD}All numeric claims verified against the V2.3 dataset.{RESET}")
    sys.exit(0)
