"""
Ukrainian Creative Workers V2 - Extended Statistical Analysis & Chart Generation
Run from project root: cd "/Users/symkinmark_/projects/Ai agent basic"
"""

import csv
import os
import math
import collections
import statistics

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_PATH     = os.path.join(PROJECT_ROOT, 'esu_creative_workers_reviewed.csv')
OUT_TXT      = os.path.join(PROJECT_ROOT, 'analysis_extended.txt')
CHARTS_DIR   = os.path.join(PROJECT_ROOT, 'charts')

os.makedirs(CHARTS_DIR, exist_ok=True)

SOURCE_NOTE = "Source: Encyclopedia of Modern Ukraine (esu.com.ua), V2 dataset, Berdnyk & Symkin 2026"

# ---------------------------------------------------------------------------
# PALETTE
# ---------------------------------------------------------------------------
NAVY   = '#1B2A4A'
GOLD   = '#C9A84C'
RED    = '#C0392B'
BLUE   = '#2980B9'
TEAL   = '#1A6B72'
LIGHT  = '#ECF0F1'

# ---------------------------------------------------------------------------
# PROFESSION KEYWORD MAP
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
    'Architects/Designers': [
        'архітектор', 'дизайнер',
    ],
    'Other Creative': [
        'мистець', 'культурний діяч', 'фотограф', 'kilimarnytsia', 'писанкарка',
    ],
}


def classify_profession(raw: str) -> str:
    if not raw:
        return 'Other Creative'
    lower = raw.lower()
    for category, keywords in PROFESSION_KEYWORDS.items():
        for kw in keywords:
            if kw in lower:
                return category
    return 'Other Creative'


# ---------------------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------------------
print("Loading CSV...")

rows = []
with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print(f"  Loaded {len(rows)} total rows.")

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def safe_int(val):
    try:
        v = int(str(val).strip())
        return v if v > 0 else None
    except (ValueError, TypeError):
        return None


def is_confirmed_ukrainian(row):
    if str(row.get('flag_non_ukrainian', '')).strip().upper() == 'YES':
        return False
    if str(row.get('flag_needs_claude_review', '')).strip().upper() == 'YES':
        return str(row.get('is_ukrainian', '')).strip().upper() == 'YES'
    return True


def is_usable_le(row):
    """Confirmed Ukrainian + birth + death + migration in migrated/non_migrated."""
    if not is_confirmed_ukrainian(row):
        return False
    by = safe_int(row.get('birth_year'))
    dy = safe_int(row.get('death_year'))
    if by is None or dy is None:
        return False
    ms = str(row.get('migration_status', '')).strip().lower()
    return ms in ('migrated', 'non_migrated')


# Classify professions on all rows
for row in rows:
    row['profession_category'] = classify_profession(row.get('profession_raw', ''))

# Subsets
confirmed_ua = [r for r in rows if is_confirmed_ukrainian(r)]
usable        = [r for r in rows if is_usable_le(r)]

for row in usable:
    row['_by'] = safe_int(row['birth_year'])
    row['_dy'] = safe_int(row['death_year'])
    row['_le'] = row['_dy'] - row['_by']
    row['_ms'] = row['migration_status'].strip().lower()

migrated     = [r for r in usable if r['_ms'] == 'migrated']
non_migrated = [r for r in usable if r['_ms'] == 'non_migrated']

print(f"  Confirmed Ukrainian: {len(confirmed_ua)}")
print(f"  Usable for LE analysis: {len(usable)} ({len(migrated)} migrated, {len(non_migrated)} non-migrated)")

# ---------------------------------------------------------------------------
# STATISTICAL HELPERS
# ---------------------------------------------------------------------------

def describe_le(group, label=''):
    les = [r['_le'] for r in group]
    if not les:
        return {'label': label, 'n': 0, 'mean_by': None, 'mean_dy': None,
                'mean_le': None, 'median_le': None, 'std_le': None}
    return {
        'label':    label,
        'n':        len(les),
        'mean_by':  round(statistics.mean([r['_by'] for r in group]), 1),
        'mean_dy':  round(statistics.mean([r['_dy'] for r in group]), 1),
        'mean_le':  round(statistics.mean(les), 2),
        'median_le':round(statistics.median(les), 2),
        'std_le':   round(statistics.stdev(les) if len(les) > 1 else 0, 2),
    }


def cohens_d(a, b):
    """Cohen's d between two lists."""
    if len(a) < 2 or len(b) < 2:
        return None
    pooled_std = math.sqrt(
        ((len(a) - 1) * statistics.variance(a) + (len(b) - 1) * statistics.variance(b))
        / (len(a) + len(b) - 2)
    )
    if pooled_std == 0:
        return 0.0
    return round((statistics.mean(a) - statistics.mean(b)) / pooled_std, 4)


def mannwhitney(a, b):
    if len(a) < 3 or len(b) < 3:
        return None, None
    res = stats.mannwhitneyu(a, b, alternative='two-sided')
    return round(res.statistic, 2), round(res.pvalue, 6)


# ---------------------------------------------------------------------------
# REPRESSION PERIODS
# ---------------------------------------------------------------------------
PERIODS = [
    ('Pre-1917 (Tsarist era)',          lambda y: y < 1917),
    ('1917-1921 (Revolution/Civil War)', lambda y: 1917 <= y <= 1921),
    ('1922-1929 (Early Soviet/NEP)',     lambda y: 1922 <= y <= 1929),
    ('1930-1933 (Holodomor/Early Purges)',lambda y: 1930 <= y <= 1933),
    ('1934-1938 (Great Terror peak)',    lambda y: 1934 <= y <= 1938),
    ('1937 ONLY (single-year spotlight)',lambda y: y == 1937),
    ('1939-1945 (WWII)',                 lambda y: 1939 <= y <= 1945),
    ('1946-1953 (Late Stalin)',          lambda y: 1946 <= y <= 1953),
    ('1954-1964 (Khrushchev Thaw)',      lambda y: 1954 <= y <= 1964),
    ('1965-1991 (Stagnation/Late Soviet)',lambda y: 1965 <= y <= 1991),
    ('Post-1991',                        lambda y: y > 1991),
]

# ---------------------------------------------------------------------------
# BUILD ANALYSIS TEXT
# ---------------------------------------------------------------------------
print("Running statistical analysis...")

lines = []
def h(text=''):
    lines.append(text)
def hr(char='=', width=80):
    lines.append(char * width)

hr()
h("UKRAINIAN CREATIVE WORKERS V2 — EXTENDED STATISTICAL ANALYSIS")
h("Berdnyk & Symkin 2026 | Source: Encyclopedia of Modern Ukraine (esu.com.ua)")
hr()
h()

# -------------------------------------------------------------------
# 1. OVERALL SUMMARY
# -------------------------------------------------------------------
h("1. OVERALL SUMMARY")
hr('-')
h(f"  Total records in dataset           : {len(rows)}")
h(f"  Confirmed Ukrainian                : {len(confirmed_ua)}")
h(f"    - Clean Ukrainian (no flags)     : {sum(1 for r in rows if not r.get('flag_non_ukrainian','').strip() and not r.get('flag_needs_claude_review','').strip())}")
h(f"    - Reviewed & confirmed Ukrainian : {sum(1 for r in rows if r.get('flag_needs_claude_review','').strip().upper()=='YES' and r.get('is_ukrainian','').strip().upper()=='YES')}")
h(f"  Non-Ukrainian (excluded)           : {sum(1 for r in rows if r.get('flag_non_ukrainian','').strip().upper()=='YES')}")
h(f"  Usable for life expectancy analysis: {len(usable)}")
h(f"    - Migrated                       : {len(migrated)}")
h(f"    - Non-migrated                   : {len(non_migrated)}")

# Migration status breakdown for confirmed UA
ms_counts = collections.Counter(r.get('migration_status','').strip().lower() for r in confirmed_ua)
h()
h("  Migration status breakdown (confirmed Ukrainian):")
for k, v in sorted(ms_counts.items(), key=lambda x: -x[1]):
    h(f"    {k or '(blank)':30s}: {v}")
h()

# -------------------------------------------------------------------
# 2. LIFE EXPECTANCY BY MIGRATION STATUS
# -------------------------------------------------------------------
h("2. LIFE EXPECTANCY BY MIGRATION STATUS")
hr('-')

desc_m  = describe_le(migrated, 'Migrated')
desc_nm = describe_le(non_migrated, 'Non-migrated')

le_m  = [r['_le'] for r in migrated]
le_nm = [r['_le'] for r in non_migrated]

cd    = cohens_d(le_m, le_nm)
u_stat, p_val = mannwhitney(le_m, le_nm)

for d in [desc_m, desc_nm]:
    h(f"  {d['label']:20s}  n={d['n']:4d}  mean_birth={d['mean_by']}  mean_death={d['mean_dy']}")
    h(f"  {'':20s}  mean_LE={d['mean_le']}  median_LE={d['median_le']}  std={d['std_le']}")
    h()

if desc_m['mean_le'] and desc_nm['mean_le']:
    gap = round(desc_m['mean_le'] - desc_nm['mean_le'], 2)
    h(f"  LE Gap (migrated minus non-migrated): {gap:+.2f} years")
h(f"  Cohen's d effect size              : {cd}")
h(f"  Mann-Whitney U statistic           : {u_stat}")
h(f"  Mann-Whitney p-value               : {p_val}")
if p_val is not None:
    sig = "SIGNIFICANT (p < 0.05)" if p_val < 0.05 else "not significant at p=0.05"
    h(f"  Result                             : {sig}")
h()

# -------------------------------------------------------------------
# 3. LIFE EXPECTANCY BY PROFESSION x MIGRATION STATUS
# -------------------------------------------------------------------
h("3. LIFE EXPECTANCY BY PROFESSION × MIGRATION STATUS")
hr('-')

professions = list(PROFESSION_KEYWORDS.keys())
header = f"  {'Profession':25s} | {'Migrated LE':>12s} {'(n)':>5s} | {'Non-migr LE':>12s} {'(n)':>5s} | {'Gap':>8s}"
h(header)
h("  " + "-" * (len(header) - 2))

for prof in professions:
    pg_m  = [r for r in migrated     if r['profession_category'] == prof]
    pg_nm = [r for r in non_migrated if r['profession_category'] == prof]
    le_pm  = [r['_le'] for r in pg_m]
    le_pnm = [r['_le'] for r in pg_nm]
    mean_m  = round(statistics.mean(le_pm),  1) if le_pm  else None
    mean_nm = round(statistics.mean(le_pnm), 1) if le_pnm else None
    gap_str = f"{mean_m - mean_nm:+.1f}" if (mean_m and mean_nm) else "N/A"
    m_str   = f"{mean_m}"  if mean_m  else "N/A"
    nm_str  = f"{mean_nm}" if mean_nm else "N/A"
    h(f"  {prof:25s} | {m_str:>12s} {len(le_pm):>5d} | {nm_str:>12s} {len(le_pnm):>5d} | {gap_str:>8s}")
h()

# -------------------------------------------------------------------
# 4. REPRESSION PERIOD DEEP-DIVE (NON-MIGRANTS ONLY)
# -------------------------------------------------------------------
h("4. REPRESSION PERIOD DEEP-DIVE (non-migrants only)")
hr('-')

nm_with_dy = [r for r in non_migrated if r.get('_dy')]
total_nm_deaths = len(nm_with_dy)

h(f"  Total non-migrant deaths with death year: {total_nm_deaths}")
h()
header4 = f"  {'Period':42s} | {'Deaths':>7s} | {'Avg Age':>8s} | {'% of total':>10s}"
h(header4)
h("  " + "-" * (len(header4) - 2))

for period_label, period_fn in PERIODS:
    subset = [r for r in nm_with_dy if period_fn(r['_dy'])]
    ages   = [r['_le'] for r in subset if r.get('_le') is not None]
    avg_age_str = f"{round(statistics.mean(ages), 1)}" if ages else "N/A"
    pct    = round(100 * len(subset) / total_nm_deaths, 1) if total_nm_deaths else 0
    h(f"  {period_label:42s} | {len(subset):>7d} | {avg_age_str:>8s} | {pct:>9.1f}%")
h()

# -------------------------------------------------------------------
# 5. BIRTH COHORT ANALYSIS
# -------------------------------------------------------------------
h("5. BIRTH COHORT ANALYSIS")
hr('-')

decades = list(range(1840, 1990, 10))

h(f"  {'Cohort':10s} | {'n (all)':>8s} | {'% surv >1991':>13s} | {'m LE migr':>12s} (n) | {'m LE non-m':>12s} (n)")
h("  " + "-" * 80)

for dec in decades:
    cohort_all  = [r for r in confirmed_ua if safe_int(r.get('birth_year')) is not None
                   and dec <= safe_int(r['birth_year']) < dec + 10]
    surv = [r for r in cohort_all if safe_int(r.get('death_year')) is not None
            and safe_int(r['death_year']) > 1991]
    pct_surv = round(100 * len(surv) / len(cohort_all), 1) if cohort_all else 0

    coh_m  = [r for r in migrated     if dec <= r['_by'] < dec + 10]
    coh_nm = [r for r in non_migrated if dec <= r['_by'] < dec + 10]
    le_cm  = [r['_le'] for r in coh_m]
    le_cnm = [r['_le'] for r in coh_nm]
    m_str  = f"{round(statistics.mean(le_cm),1)}"  if le_cm  else "N/A"
    nm_str = f"{round(statistics.mean(le_cnm),1)}" if le_cnm else "N/A"
    h(f"  {dec}s      | {len(cohort_all):>8d} | {pct_surv:>12.1f}% | {m_str:>12s} {len(le_cm):>3d} | {nm_str:>12s} {len(le_cnm):>3d}")
h()

# -------------------------------------------------------------------
# 6. DEATH AGE DISTRIBUTION
# -------------------------------------------------------------------
h("6. DEATH AGE DISTRIBUTION")
hr('-')

AGE_BUCKETS = [
    ('<30',   lambda a: a < 30),
    ('30-39', lambda a: 30 <= a <= 39),
    ('40-49', lambda a: 40 <= a <= 49),
    ('50-59', lambda a: 50 <= a <= 59),
    ('60-69', lambda a: 60 <= a <= 69),
    ('70-79', lambda a: 70 <= a <= 79),
    ('80-89', lambda a: 80 <= a <= 89),
    ('90+',   lambda a: a >= 90),
]

h(f"  {'Age bucket':10s} | {'Migrated':>10s} | {'Non-migrated':>13s}")
h("  " + "-" * 40)
for bucket_label, bucket_fn in AGE_BUCKETS:
    bm  = sum(1 for r in migrated     if r.get('_le') is not None and bucket_fn(r['_le']))
    bnm = sum(1 for r in non_migrated if r.get('_le') is not None and bucket_fn(r['_le']))
    h(f"  {bucket_label:10s} | {bm:>10d} | {bnm:>13d}")

h()
prem_m  = sum(1 for r in migrated     if r.get('_le') is not None and r['_le'] < 50)
prem_nm = sum(1 for r in non_migrated if r.get('_le') is not None and r['_le'] < 50)
prem_m_pct  = round(100 * prem_m  / len(migrated),     1) if migrated     else 0
prem_nm_pct = round(100 * prem_nm / len(non_migrated), 1) if non_migrated else 0
h(f"  Premature death rate (died before 50):")
h(f"    Migrated     : {prem_m}  / {len(migrated)}  = {prem_m_pct}%")
h(f"    Non-migrated : {prem_nm} / {len(non_migrated)} = {prem_nm_pct}%")
h()

# -------------------------------------------------------------------
# 7. GEOGRAPHIC ANALYSIS
# -------------------------------------------------------------------
h("7. GEOGRAPHIC ANALYSIS (birth location)")
hr('-')

birth_loc_all    = collections.Counter()
birth_loc_mig    = collections.Counter()
birth_loc_nonmig = collections.Counter()

for r in confirmed_ua:
    bl = str(r.get('birth_location', '')).strip()
    if bl:
        birth_loc_all[bl] += 1
for r in migrated:
    bl = str(r.get('birth_location', '')).strip()
    if bl:
        birth_loc_mig[bl] += 1
for r in non_migrated:
    bl = str(r.get('birth_location', '')).strip()
    if bl:
        birth_loc_nonmig[bl] += 1

h("  Top 20 birth cities/regions (all confirmed Ukrainian):")
h(f"  {'Location':50s} | {'Count':>6s} | {'Migrated':>9s} | {'% Migrated':>11s}")
h("  " + "-" * 85)
for loc, cnt in birth_loc_all.most_common(20):
    mig_cnt = birth_loc_mig.get(loc, 0)
    pct_mig = round(100 * mig_cnt / cnt, 1) if cnt else 0
    h(f"  {loc[:50]:50s} | {cnt:>6d} | {mig_cnt:>9d} | {pct_mig:>10.1f}%")
h()

# -------------------------------------------------------------------
# 8. 1937 SPOTLIGHT
# -------------------------------------------------------------------
h("8. 1937 SPOTLIGHT")
hr('-')

died_1937_nm = [r for r in non_migrated if r['_dy'] == 1937]
died_1937_m  = [r for r in migrated     if r['_dy'] == 1937]

h(f"  Non-migrants who died in 1937   : {len(died_1937_nm)}")
h(f"  Migrants who died in 1937       : {len(died_1937_m)}")
h()

ages_1937 = [r['_le'] for r in died_1937_nm if r.get('_le') is not None]
if ages_1937:
    h(f"  Avg age at death (non-migrants) : {round(statistics.mean(ages_1937), 1)}")
    h(f"  Min age                         : {min(ages_1937)}")
    h(f"  Max age                         : {max(ages_1937)}")
h()

prof_1937 = collections.Counter(r['profession_category'] for r in died_1937_nm)
h("  Profession breakdown of non-migrants who died in 1937:")
for prof, cnt in prof_1937.most_common():
    h(f"    {prof:30s}: {cnt}")
h()

hr()
h("END OF ANALYSIS")
hr()

# Write to file
with open(OUT_TXT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"  Analysis written to: {OUT_TXT}")

# ---------------------------------------------------------------------------
# CHART HELPERS
# ---------------------------------------------------------------------------

def apply_style(ax, title, xlabel=None, ylabel=None):
    ax.set_facecolor('#F7F9FB')
    ax.figure.patch.set_facecolor('white')
    ax.set_title(title, fontsize=14, fontweight='bold', color=NAVY, pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11, color=NAVY)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11, color=NAVY)
    ax.tick_params(colors=NAVY)
    for spine in ax.spines.values():
        spine.set_edgecolor('#CCCCCC')


def add_source(fig):
    fig.text(0.5, 0.01, SOURCE_NOTE, ha='center', fontsize=7, color='grey', style='italic')


# ---------------------------------------------------------------------------
# FIG 1 — GROUPED BAR: LE COMPARISON MIGRATED VS NON-MIGRATED (OVERALL + PROFESSION)
# ---------------------------------------------------------------------------
print("Generating fig1_life_expectancy_comparison.png ...")

categories   = ['Overall'] + professions
means_m, means_nm = [], []
se_m,    se_nm    = [], []

for cat in categories:
    if cat == 'Overall':
        g_m  = le_m
        g_nm = le_nm
    else:
        g_m  = [r['_le'] for r in migrated     if r['profession_category'] == cat]
        g_nm = [r['_le'] for r in non_migrated if r['profession_category'] == cat]

    means_m.append(statistics.mean(g_m)  if g_m  else 0)
    means_nm.append(statistics.mean(g_nm) if g_nm else 0)
    se_m.append(statistics.stdev(g_m)  / math.sqrt(len(g_m))  if len(g_m)  > 1 else 0)
    se_nm.append(statistics.stdev(g_nm) / math.sqrt(len(g_nm)) if len(g_nm) > 1 else 0)

x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 7))
bars_m  = ax.bar(x - width/2, means_m,  width, label='Migrated',     color=BLUE, yerr=se_m,  capsize=4, ecolor='#1A5276')
bars_nm = ax.bar(x + width/2, means_nm, width, label='Non-migrated', color=RED,  yerr=se_nm, capsize=4, ecolor='#7B241C')

ax.set_xticks(x)
ax.set_xticklabels(categories, rotation=20, ha='right', fontsize=9)
apply_style(ax, 'Life Expectancy: Migrated vs Non-Migrated\n(Overall and by Profession Category)',
            ylabel='Average Life Expectancy (years)')
ax.legend(framealpha=0.8)
ax.set_ylim(0, max(means_m + means_nm) * 1.2 + 5)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
fig.savefig(os.path.join(CHARTS_DIR, 'fig1_life_expectancy_comparison.png'), dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 2 — OVERLAID HISTOGRAM: DEATH YEARS
# ---------------------------------------------------------------------------
print("Generating fig2_death_year_histogram.png ...")

dy_m  = [r['_dy'] for r in migrated     if 1900 <= r['_dy'] <= 2024]
dy_nm = [r['_dy'] for r in non_migrated if 1900 <= r['_dy'] <= 2024]

fig, ax = plt.subplots(figsize=(12, 6))
bins = range(1900, 2025, 2)
ax.hist(dy_nm, bins=bins, alpha=0.6, color=RED,  label='Non-migrated', edgecolor='white', linewidth=0.3)
ax.hist(dy_m,  bins=bins, alpha=0.6, color=BLUE, label='Migrated',     edgecolor='white', linewidth=0.3)

ax.axvline(1937, color=NAVY, linestyle='--', linewidth=1.5, label='1937 (Great Terror)')
ax.text(1937.5, ax.get_ylim()[1] * 0.95, 'Great Terror\n1937', color=NAVY, fontsize=8, va='top')

ax.axvline(1933, color='#8E44AD', linestyle='--', linewidth=1.5, label='1933 (Holodomor)')
ax.text(1933.5, ax.get_ylim()[1] * 0.80, 'Holodomor\n1933', color='#8E44AD', fontsize=8, va='top')

apply_style(ax, 'Death Year Distribution: Migrated vs Non-Migrated (1900–2024)',
            xlabel='Death Year', ylabel='Number of Deaths')
ax.legend(framealpha=0.8)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
fig.savefig(os.path.join(CHARTS_DIR, 'fig2_death_year_histogram.png'), dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 3 — BAR: REPRESSION PERIODS (NON-MIGRANTS ONLY, AVG AGE AT DEATH)
# ---------------------------------------------------------------------------
print("Generating fig3_repression_periods_nonmigrants.png ...")

# Use main periods only (excluding the single-year 1937 spotlight to avoid double-counting on chart)
CHART_PERIODS = [p for p in PERIODS if p[0] != '1937 ONLY (single-year spotlight)']

period_labels = []
period_avg_ages = []
period_counts  = []

for period_label, period_fn in CHART_PERIODS:
    subset = [r for r in nm_with_dy if period_fn(r['_dy'])]
    ages   = [r['_le'] for r in subset if r.get('_le') is not None]
    period_labels.append(period_label.split(' (')[0])   # short label
    period_avg_ages.append(round(statistics.mean(ages), 1) if ages else 0)
    period_counts.append(len(subset))

# Color gradient: darker = more repressive (manually coded)
PERIOD_COLORS = [
    '#5D8AA8', '#7B6D8D', '#B07D62', '#C0392B', '#8B0000',
    '#3498DB', '#7F8C8D', '#1A5276', '#2874A6', '#85C1E9',
]

fig, ax = plt.subplots(figsize=(14, 7))
bars = ax.barh(period_labels, period_avg_ages, color=PERIOD_COLORS[:len(period_labels)], edgecolor='white')

for i, (bar, cnt, avg) in enumerate(zip(bars, period_counts, period_avg_ages)):
    if avg > 0:
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"n={cnt}, avg={avg}", va='center', fontsize=8, color=NAVY)

apply_style(ax, 'Average Age at Death by Historical Period\n(Non-Migrants Only)',
            xlabel='Average Age at Death', ylabel='')
ax.set_xlim(0, max(period_avg_ages) * 1.25 + 5 if period_avg_ages else 80)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
fig.savefig(os.path.join(CHARTS_DIR, 'fig3_repression_periods_nonmigrants.png'), dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 4 — HEATMAP: PROFESSION × DEATH DECADE (NON-MIGRANTS)
# ---------------------------------------------------------------------------
print("Generating fig4_profession_heatmap.png ...")

death_decades = list(range(1900, 2020, 10))
heatmap_data  = {}

for prof in professions:
    row_vals = []
    for dec in death_decades:
        cnt = sum(1 for r in non_migrated
                  if r['profession_category'] == prof and dec <= r['_dy'] < dec + 10)
        row_vals.append(cnt)
    heatmap_data[prof] = row_vals

hm_df = pd.DataFrame(heatmap_data, index=[f"{d}s" for d in death_decades]).T

fig, ax = plt.subplots(figsize=(14, 6))
sns.heatmap(hm_df, annot=True, fmt='d', cmap='YlOrRd', linewidths=0.5,
            linecolor='white', ax=ax, cbar_kws={'label': 'Deaths'})
ax.set_title('Non-Migrant Deaths by Profession and Death Decade',
             fontsize=14, fontweight='bold', color=NAVY, pad=12)
ax.set_xlabel('Death Decade', fontsize=11, color=NAVY)
ax.set_ylabel('Profession Category', fontsize=11, color=NAVY)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
fig.savefig(os.path.join(CHARTS_DIR, 'fig4_profession_heatmap.png'), dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 5 — LINE CHART: AVG LE BY BIRTH DECADE (MIGRATED VS NON-MIGRATED)
# ---------------------------------------------------------------------------
print("Generating fig5_birth_cohort_survival.png ...")

plot_decades = list(range(1850, 1970, 10))

avg_le_m_by_dec  = []
avg_le_nm_by_dec = []

for dec in plot_decades:
    g_m  = [r['_le'] for r in migrated     if dec <= r['_by'] < dec + 10]
    g_nm = [r['_le'] for r in non_migrated if dec <= r['_by'] < dec + 10]
    avg_le_m_by_dec.append( statistics.mean(g_m)  if g_m  else None)
    avg_le_nm_by_dec.append(statistics.mean(g_nm) if g_nm else None)

fig, ax = plt.subplots(figsize=(12, 6))

# Filter out None values for plotting
x_m  = [d for d, v in zip(plot_decades, avg_le_m_by_dec)  if v is not None]
y_m  = [v for v in avg_le_m_by_dec  if v is not None]
x_nm = [d for d, v in zip(plot_decades, avg_le_nm_by_dec) if v is not None]
y_nm = [v for v in avg_le_nm_by_dec if v is not None]

ax.plot(x_m,  y_m,  'o-', color=BLUE, linewidth=2.5, markersize=6, label='Migrated')
ax.plot(x_nm, y_nm, 's-', color=RED,  linewidth=2.5, markersize=6, label='Non-migrated')

ax.fill_between(x_m,  y_m,  alpha=0.12, color=BLUE)
ax.fill_between(x_nm, y_nm, alpha=0.12, color=RED)

ax.set_xticks(plot_decades)
ax.set_xticklabels([f"{d}s" for d in plot_decades], rotation=0)
apply_style(ax, 'Average Life Expectancy by Birth Decade\n(Migrated vs Non-Migrated)',
            xlabel='Birth Decade', ylabel='Average Life Expectancy (years)')
ax.legend(framealpha=0.8)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
fig.savefig(os.path.join(CHARTS_DIR, 'fig5_birth_cohort_survival.png'), dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 6 — SIDE-BY-SIDE BAR: AGE AT DEATH DISTRIBUTION
# ---------------------------------------------------------------------------
print("Generating fig6_age_at_death_distribution.png ...")

bucket_labels = [b[0] for b in AGE_BUCKETS]
counts_m  = []
counts_nm = []

for bucket_label, bucket_fn in AGE_BUCKETS:
    counts_m.append( sum(1 for r in migrated     if r.get('_le') is not None and bucket_fn(r['_le'])))
    counts_nm.append(sum(1 for r in non_migrated if r.get('_le') is not None and bucket_fn(r['_le'])))

x = np.arange(len(bucket_labels))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(x - width/2, counts_m,  width, label='Migrated',     color=BLUE, edgecolor='white')
ax.bar(x + width/2, counts_nm, width, label='Non-migrated', color=RED,  edgecolor='white')

ax.set_xticks(x)
ax.set_xticklabels(bucket_labels)
apply_style(ax, 'Age at Death Distribution: Migrated vs Non-Migrated',
            xlabel='Age at Death (years)', ylabel='Number of People')
ax.legend(framealpha=0.8)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
fig.savefig(os.path.join(CHARTS_DIR, 'fig6_age_at_death_distribution.png'), dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 7 — PIE/HORIZONTAL BAR: 1937 PROFESSION BREAKDOWN
# ---------------------------------------------------------------------------
print("Generating fig7_1937_profession_breakdown.png ...")

prof_1937_counts = collections.Counter(r['profession_category'] for r in died_1937_nm)

if prof_1937_counts:
    labels_1937 = list(prof_1937_counts.keys())
    values_1937 = [prof_1937_counts[l] for l in labels_1937]

    # sort by count descending
    sorted_pairs = sorted(zip(values_1937, labels_1937), reverse=True)
    values_1937 = [p[0] for p in sorted_pairs]
    labels_1937 = [p[1] for p in sorted_pairs]

    palette_1937 = [NAVY, RED, GOLD, TEAL, BLUE, '#E67E22'][:len(labels_1937)]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(labels_1937[::-1], values_1937[::-1], color=palette_1937[::-1], edgecolor='white')
    for bar, val in zip(bars, values_1937[::-1]):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                str(val), va='center', fontsize=10, color=NAVY, fontweight='bold')
    apply_style(ax, f'Profession Breakdown of Non-Migrants Who Died in 1937\n(Total: {len(died_1937_nm)})',
                xlabel='Number of Deaths', ylabel='')
    ax.set_xlim(0, max(values_1937) * 1.25 + 1)
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    add_source(fig)
    fig.savefig(os.path.join(CHARTS_DIR, 'fig7_1937_profession_breakdown.png'), dpi=150)
    plt.close(fig)
else:
    print("  WARNING: No non-migrant deaths found for 1937 with current data — fig7 skipped.")

# ---------------------------------------------------------------------------
# FINAL SUMMARY
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("GENERATION COMPLETE")
print("=" * 60)
print(f"  Analysis text : {OUT_TXT}")
print(f"  Charts dir    : {CHARTS_DIR}")
charts_generated = [f for f in os.listdir(CHARTS_DIR) if f.endswith('.png')]
for c in sorted(charts_generated):
    print(f"    - {c}")
print(f"  Total charts  : {len(charts_generated)}")
print(f"  Analysis lines: {len(lines)}")
print("=" * 60)
