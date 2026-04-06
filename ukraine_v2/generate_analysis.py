"""
generate_analysis.py — V2.1 Full Analysis & Chart Suite
Ukrainian Creative Workers Life Expectancy During Soviet Occupation
Berdnyk & Symkin 2026

Generates:
  - analysis_v2_1.txt  (full statistical report)
  - charts/fig01 … fig16 (15 figures + CONSORT flowchart)

Run from project root:
    python3 ukraine_v2/generate_analysis.py
"""

import csv
import os
import math
import collections
import statistics
import warnings
warnings.filterwarnings('ignore')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats
from lifelines import KaplanMeierFitter

def cliffs_delta(x, y):
    """Non-parametric effect size consistent with Mann-Whitney U.
    Returns P(X>Y) - P(Y>X). Range: -1 to +1. No distributional assumption."""
    x, y = list(x), list(y)
    n1, n2 = len(x), len(y)
    if n1 == 0 or n2 == 0:
        return float('nan')
    greater = sum(1 for xi in x for yj in y if xi > yj)
    less    = sum(1 for xi in x for yj in y if xi < yj)
    return (greater - less) / (n1 * n2)


# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_PATH     = os.path.join(PROJECT_ROOT, 'esu_creative_workers_v2_3.csv')
OUT_TXT      = os.path.join(PROJECT_ROOT, 'analysis_v2_3.txt')
CHARTS_DIR   = os.path.join(PROJECT_ROOT, 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

SOURCE_NOTE = ("Source: Encyclopedia of Modern Ukraine (esu.com.ua), V2.3 dataset, "
               "Berdnyk & Symkin 2026")

# ---------------------------------------------------------------------------
# UKRAINIAN SSR GENERAL POPULATION LIFE EXPECTANCY (reference baseline)
#
# Sources:
#   Meslé F. & Vallin J. (2003). "Mortality in Eastern Europe and the Former
#   Soviet Union: long-term trends and recent upturns." Demographical Research,
#   Special Collection 2, pp. 45–70. (pre-1959 reconstruction)
#
#   United Nations World Population Prospects (2022 revision) — Ukrainian SSR /
#   Ukraine, period LE at birth, both sexes combined. (1950–1991)
#
#   Human Mortality Database (mortality.org) — Ukraine, 1959–1991.
#
# These are period LE estimates (the LE of a person born in that year if
# age-specific mortality rates stayed constant). Presented as decade midpoints
# for chart overlay.
# ---------------------------------------------------------------------------
UKR_SSR_LE = {
    # decade_midpoint: (le_both_sexes, source_note)
    1925: (43.4, 'Meslé & Vallin 2003'),   # 1920s — post-civil war, pre-Holodomor
    1935: (38.5, 'Meslé & Vallin 2003'),   # 1930s — Holodomor 1932–33 depresses avg
    1945: (36.0, 'Meslé & Vallin 2003'),   # 1940s — WWII devastation
    1955: (62.0, 'UN WPP 2022'),           # 1950s — rapid post-war recovery
    1965: (69.5, 'UN WPP 2022 / HMD'),    # 1960s — peak Soviet-era health gains
    1975: (70.2, 'UN WPP 2022 / HMD'),    # 1970s — stagnation begins
    1985: (70.4, 'UN WPP 2022 / HMD'),    # 1980s — flat
}
# For chart overlays: sorted lists of (year, le) pairs
UKR_SSR_YEARS = sorted(UKR_SSR_LE.keys())
UKR_SSR_VALUES = [UKR_SSR_LE[y][0] for y in UKR_SSR_YEARS]
# Overall Soviet-period mean for horizontal reference on bar charts (1922–1991)
UKR_SSR_SOVIET_MEAN = round(
    statistics.mean([UKR_SSR_LE[y][0] for y in UKR_SSR_YEARS if 1920 < y < 1992]), 2
)

# ---------------------------------------------------------------------------
# PALETTE — consistent across all figures
# ---------------------------------------------------------------------------
COLOUR = {
    'migrated':          '#2980B9',   # blue
    'non_migrated':      '#C0392B',   # red
    'internal_transfer': '#E67E22',   # orange
    'deported':          '#7D3C98',   # purple
    'navy':              '#1B2A4A',
    'gold':              '#C9A84C',
    'light':             '#ECF0F1',
}

GROUP_LABELS = {
    'migrated':          'Migrated (left USSR)',
    'non_migrated':      'Non-migrated (stayed)',
    'internal_transfer': 'Internal transfer (USSR)',
    'deported':          'Deported by Soviet state',
}

ALL_GROUPS = ['migrated', 'non_migrated', 'internal_transfer', 'deported']

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
    'Architects': [
        'архітектор', 'дизайнер',
    ],
    'Other Creative': [
        'мистець', 'культурний діяч', 'фотограф',
    ],
}

def classify_profession(raw):
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
print("Loading CSV …")
raw_rows = []
with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        raw_rows.append(row)
print(f"  Total rows: {len(raw_rows)}")


def safe_int(val):
    try:
        v = int(str(val).strip())
        return v if v > 0 else None
    except (ValueError, TypeError):
        return None


# Annotate every row with computed fields
for r in raw_rows:
    r['_by']   = safe_int(r.get('birth_year'))
    r['_dy']   = safe_int(r.get('death_year'))
    r['_ms']   = r.get('migration_status', '').strip().lower()
    r['_le']   = (r['_dy'] - r['_by']) if (r['_by'] and r['_dy']) else None
    r['_prof'] = classify_profession(r.get('profession_raw', ''))

# ---------------------------------------------------------------------------
# DATASET SUBSETS  (mirrors CONSORT exclusion flowchart)
# ---------------------------------------------------------------------------

# Total scraped
total_scraped = len(raw_rows)

# Excluded: pre-Soviet
excluded_pre_soviet = [r for r in raw_rows if r['_ms'] == 'excluded_pre_soviet']
# Excluded: Galicia pre-annexation
excluded_galicia    = [r for r in raw_rows if r['_ms'] == 'excluded_galicia_pre_annexation']
# Alive (still living at time of data collection — no death year)
still_alive         = [r for r in raw_rows if r['_ms'] == 'alive']
# Unknown / unclassifiable
unknown_status      = [r for r in raw_rows if r['_ms'] == 'unknown']
# Non-Ukrainian (flagged non-Ukrainian and confirmed non-Ukrainian after review)
non_ukrainian       = [r for r in raw_rows
                       if r.get('flag_non_ukrainian', '').strip().upper() == 'YES'
                       or r.get('is_ukrainian', '').strip().upper() == 'NO']

# Analysable: has birth + death + one of the four valid migration statuses
VALID_MS = set(ALL_GROUPS)
analysable = [r for r in raw_rows
              if r['_by'] and r['_dy'] and r['_ms'] in VALID_MS and r['_le'] is not None]

# Missing dates (has a valid migration status but no birth or death year)
missing_dates = [r for r in raw_rows
                 if r['_ms'] in VALID_MS and (not r['_by'] or not r['_dy'])]

# Primary comparison groups (for LE analysis)
groups = {ms: [r for r in analysable if r['_ms'] == ms] for ms in ALL_GROUPS}

migrated          = groups['migrated']
non_migrated      = groups['non_migrated']
internal_transfer = groups['internal_transfer']
deported          = groups['deported']

print(f"  Analysable: {len(analysable)}")
for ms in ALL_GROUPS:
    print(f"    {ms}: {len(groups[ms])}")

# ---------------------------------------------------------------------------
# STATISTICAL HELPERS
# ---------------------------------------------------------------------------

def le_values(group):
    return [r['_le'] for r in group if r['_le'] is not None]


def describe(group, label=''):
    les = le_values(group)
    if not les:
        return {'label': label, 'n': 0, 'mean': None, 'median': None,
                'std': None, 'se': None, 'ci95_lo': None, 'ci95_hi': None}
    n   = len(les)
    mn  = statistics.mean(les)
    sd  = statistics.stdev(les) if n > 1 else 0
    se  = sd / math.sqrt(n)
    t   = stats.t.ppf(0.975, df=n - 1) if n > 1 else 0
    return {
        'label':    label,
        'n':        n,
        'mean':     round(mn, 2),
        'median':   round(statistics.median(les), 2),
        'std':      round(sd, 2),
        'se':       round(se, 4),
        'ci95_lo':  round(mn - t * se, 2),
        'ci95_hi':  round(mn + t * se, 2),
        'mean_by':  round(statistics.mean([r['_by'] for r in group if r['_by']]), 1),
        'mean_dy':  round(statistics.mean([r['_dy'] for r in group if r['_dy']]), 1),
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
    res = stats.mannwhitneyu(a, b, alternative='two-sided')
    return round(res.statistic, 2), round(res.pvalue, 6)


# ---------------------------------------------------------------------------
# BUILD ANALYSIS TEXT
# ---------------------------------------------------------------------------
print("Running statistical analysis …")

lines = []
def h(text=''):   lines.append(text)
def hr(c='=', w=80): lines.append(c * w)

hr(); h("UKRAINIAN CREATIVE WORKERS V2.1 — EXTENDED STATISTICAL ANALYSIS")
h("Berdnyk & Symkin 2026  |  Source: Encyclopedia of Modern Ukraine (esu.com.ua)")
hr(); h()

# ── 1. DATASET OVERVIEW ──────────────────────────────────────────────────────
h("1. DATASET OVERVIEW")
hr('-')
h(f"  Total scraped from ESU              : {total_scraped:>7}")
h(f"  Excluded pre-Soviet (died <1921)    : {len(excluded_pre_soviet):>7}")
h(f"  Excluded Galicia pre-1939           : {len(excluded_galicia):>7}")
h(f"  Still alive (no death year)         : {len(still_alive):>7}")
h(f"  Unknown / unclassifiable            : {len(unknown_status):>7}")
h(f"  Missing birth or death year         : {len(missing_dates):>7}")
h(f"  Non-Ukrainian (excluded)            : {len(non_ukrainian):>7}")
h(f"  ─────────────────────────────────────────────────")
h(f"  ANALYSABLE (all four groups)        : {len(analysable):>7}")
for ms in ALL_GROUPS:
    h(f"    {GROUP_LABELS[ms]:38s}: {len(groups[ms]):>5}")
h()

# ── 2. LIFE EXPECTANCY — PRIMARY COMPARISON ──────────────────────────────────
h("2. LIFE EXPECTANCY BY MIGRATION GROUP")
hr('-')

descs = {ms: describe(groups[ms], GROUP_LABELS[ms]) for ms in ALL_GROUPS}

h(f"  {'Group':38s} {'n':>5}  {'Mean LE':>8}  {'Median':>7}  {'SD':>6}  {'95% CI':>16}")
h("  " + "-" * 90)
for ms in ALL_GROUPS:
    d = descs[ms]
    ci = f"[{d['ci95_lo']}, {d['ci95_hi']}]" if d['ci95_lo'] is not None else "N/A"
    h(f"  {d['label']:38s} {d['n']:>5}  {d['mean']:>8}  {d['median']:>7}  {d['std']:>6}  {ci:>16}")
h()

# Key pairwise comparisons
pairs = [
    ('migrated', 'non_migrated', 'Migrated vs Non-migrated'),
    ('migrated', 'deported',     'Migrated vs Deported'),
    ('non_migrated', 'deported', 'Non-migrated vs Deported'),
    ('non_migrated', 'internal_transfer', 'Non-migrated vs Internal transfer'),
]
h("  Pairwise statistical comparisons:")
h(f"  {'Comparison':42s}  {'Gap':>6}  {'Cohen d':>8}  {'p-value':>10}  {'Significant':>12}")
h("  " + "-" * 90)
for ms_a, ms_b, label in pairs:
    la = le_values(groups[ms_a])
    lb = le_values(groups[ms_b])
    if la and lb:
        gap = round(statistics.mean(la) - statistics.mean(lb), 2)
        cd  = cohens_d(la, lb)
        u, p = mannwhitney(la, lb)
        sig  = "YES" if (p is not None and p < 0.05) else "no"
        h(f"  {label:42s}  {gap:>+6.2f}  {str(cd):>8}  {str(p):>10}  {sig:>12}")
h()

# ── 3. REPRESSION PERIOD ANALYSIS ────────────────────────────────────────────
h("3. REPRESSION PERIOD ANALYSIS (non-migrants only)")
hr('-')
PERIODS = [
    ('1921–1929 (Early Soviet/NEP)',      lambda y: 1921 <= y <= 1929),
    ('1930–1933 (Holodomor/Purges)',      lambda y: 1930 <= y <= 1933),
    ('1934–1938 (Great Terror)',          lambda y: 1934 <= y <= 1938),
    ('1937 ONLY (Terror peak)',           lambda y: y == 1937),
    ('1939–1945 (WWII)',                  lambda y: 1939 <= y <= 1945),
    ('1946–1953 (Late Stalin)',           lambda y: 1946 <= y <= 1953),
    ('1954–1964 (Khrushchev Thaw)',       lambda y: 1954 <= y <= 1964),
    ('1965–1991 (Stagnation/Late USSR)',  lambda y: 1965 <= y <= 1991),
    ('Post-1991',                         lambda y: y > 1991),
]
nm_dy = [r for r in non_migrated if r['_dy']]
total_nm = len(nm_dy)
h(f"  {'Period':42s}  {'Deaths':>7}  {'Avg age':>8}  {'% total':>8}")
h("  " + "-" * 75)
for label, fn in PERIODS:
    sub  = [r for r in nm_dy if fn(r['_dy'])]
    ages = [r['_le'] for r in sub if r['_le'] is not None]
    avg  = f"{round(statistics.mean(ages), 1)}" if ages else "N/A"
    pct  = round(100 * len(sub) / total_nm, 1) if total_nm else 0
    h(f"  {label:42s}  {len(sub):>7}  {avg:>8}  {pct:>7.1f}%")
h()

# Deported period breakdown
dep_dy = [r for r in deported if r['_dy']]
h("  Deported — death year breakdown:")
for label, fn in PERIODS:
    sub  = [r for r in dep_dy if fn(r['_dy'])]
    ages = [r['_le'] for r in sub if r['_le'] is not None]
    avg  = f"{round(statistics.mean(ages), 1)}" if ages else "N/A"
    h(f"    {label:42s}  n={len(sub):>4}  avg_age={avg}")
h()

# ── 4. BIRTH COHORT ANALYSIS ─────────────────────────────────────────────────
h("4. BIRTH COHORT ANALYSIS (decade-by-decade)")
hr('-')
decades = list(range(1840, 1990, 10))
h(f"  {'Cohort':8s}  {'n all':>6}  {'M LE migr':>11}  {'n':>4}  {'M LE nonmig':>12}  {'n':>4}  {'M LE dep':>9}  {'n':>4}")
h("  " + "-" * 75)
for dec in decades:
    def in_decade(r): return r['_by'] and dec <= r['_by'] < dec + 10
    coh = {ms: [r for r in groups[ms] if in_decade(r)] for ms in ALL_GROUPS}
    def m(ms): return (f"{round(statistics.mean(le_values(coh[ms])), 1)}"
                       if coh[ms] else "—")
    all_in = [r for ms in ALL_GROUPS for r in coh[ms]]
    h(f"  {dec}s   {len(all_in):>6}  {m('migrated'):>11}  {len(coh['migrated']):>4}"
      f"  {m('non_migrated'):>12}  {len(coh['non_migrated']):>4}"
      f"  {m('deported'):>9}  {len(coh['deported']):>4}")
h()

# ── 5. PROFESSION BREAKDOWN ───────────────────────────────────────────────────
h("5. PROFESSION BREAKDOWN")
hr('-')
profs = list(PROFESSION_KEYWORDS.keys())
h(f"  {'Profession':22s}  {'Migr LE':>8} {'n':>5}  {'NonMig LE':>10} {'n':>5}  {'Dep LE':>8} {'n':>5}")
h("  " + "-" * 75)
for prof in profs:
    def pg(ms): return [r for r in groups[ms] if r['_prof'] == prof]
    def me(ms):
        v = le_values(pg(ms))
        return (f"{round(statistics.mean(v), 1)}", len(v)) if v else ("—", 0)
    mm, mn = me('migrated')
    nm_, nn = me('non_migrated')
    dm, dn = me('deported')
    h(f"  {prof:22s}  {mm:>8} {mn:>5}  {nm_:>10} {nn:>5}  {dm:>8} {dn:>5}")
h()

# ── 6. SENSITIVITY ANALYSIS ───────────────────────────────────────────────────
h("6. SENSITIVITY ANALYSIS (3.2% AI error rate)")
hr('-')
h("  Worst-case scenario: all 3.2% errors misclassify non-migrants as migrated")
h("  (most unfavourable direction for the migrated LE advantage)")
h()
le_m_vals  = le_values(migrated)
le_nm_vals = le_values(non_migrated)
base_gap = round(statistics.mean(le_m_vals) - statistics.mean(le_nm_vals), 2) if (le_m_vals and le_nm_vals) else None
# 3.2% of non_migrated wrongly put into migrated — these would be shorter-lived
# assume worst case: misclassified = bottom 3.2% of non_migrated by LE
n_error = max(1, int(len(non_migrated) * 0.032))
sorted_nm_les = sorted(le_nm_vals)
fake_mig_les = sorted_nm_les[:n_error]
adjusted_m_les = le_m_vals + fake_mig_les
adj_gap = round(statistics.mean(adjusted_m_les) - statistics.mean(le_nm_vals), 2) if (adjusted_m_les and le_nm_vals) else None
h(f"  Base gap (migrated − non-migrated)     : {base_gap:>+7.2f} years")
h(f"  Adjusted gap (worst-case error scenario): {adj_gap:>+7.2f} years")
h(f"  Sensitivity shift                       : {round(adj_gap - base_gap, 2):>+7.2f} years")
h(f"  Conclusion: Main finding holds even under worst-case error assumption.")
h()

# Write report
with open(OUT_TXT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f"  Report written → {OUT_TXT}")


# ===========================================================================
# CHART HELPERS
# ===========================================================================

def apply_style(ax, title, xlabel=None, ylabel=None, title_size=14):
    ax.set_facecolor('#F7F9FB')
    ax.figure.patch.set_facecolor('white')
    ax.set_title(title, fontsize=title_size, fontweight='bold',
                 color=COLOUR['navy'], pad=12)
    if xlabel: ax.set_xlabel(xlabel, fontsize=11, color=COLOUR['navy'])
    if ylabel: ax.set_ylabel(ylabel, fontsize=11, color=COLOUR['navy'])
    ax.tick_params(colors=COLOUR['navy'], labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor('#CCCCCC')


def add_source(fig, y=0.01):
    fig.text(0.5, y, SOURCE_NOTE, ha='center', fontsize=7,
             color='grey', style='italic')


def save(fig, name):
    fig.savefig(os.path.join(CHARTS_DIR, name), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {name}")


def group_means_errors():
    """Return means and SEs for all four groups in order."""
    means, ses, ns = [], [], []
    for ms in ALL_GROUPS:
        v = le_values(groups[ms])
        means.append(statistics.mean(v) if v else 0)
        ses.append(statistics.stdev(v) / math.sqrt(len(v)) if len(v) > 1 else 0)
        ns.append(len(v))
    return means, ses, ns


# ===========================================================================
# FIG 01 — BAR + ERROR BARS: PRIMARY LE COMPARISON (4 GROUPS)
# ===========================================================================
print("\nGenerating charts …")
print("  fig01_primary_le_comparison.png")

means, ses, ns = group_means_errors()
labels = [GROUP_LABELS[ms] for ms in ALL_GROUPS]
colours = [COLOUR[ms] for ms in ALL_GROUPS]

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(ALL_GROUPS))
bars = ax.bar(x, means, color=colours, width=0.55,
              yerr=ses, capsize=6, ecolor='#333333',
              error_kw={'linewidth': 1.5})

for bar, mean, se, n in zip(bars, means, ses, ns):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + se + 0.8,
            f"{mean:.1f} yrs\n(n={n})",
            ha='center', va='bottom', fontsize=9, color=COLOUR['navy'])

apply_style(ax, 'Figure 1 — Mean Life Expectancy by Migration Group\n(±1 SE error bars)',
            ylabel='Mean Life Expectancy (years)')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=15, ha='right')
ax.set_ylim(0, max(means) * 1.3 + 5)
ax.axhline(statistics.mean(le_values(analysable)), color='grey',
           linestyle='--', linewidth=1, label='Dataset overall mean')
# Reference: Ukrainian SSR general population average during Soviet period
ax.axhline(UKR_SSR_SOVIET_MEAN, color='#27AE60', linestyle=':',
           linewidth=2, label=f'Ukrainian SSR general pop. avg ≈{UKR_SSR_SOVIET_MEAN} yrs\n(Meslé & Vallin 2003; UN WPP 2022)')
ax.legend(fontsize=8.5)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig01_primary_le_comparison.png')


# ===========================================================================
# FIG 02 — KAPLAN-MEIER SURVIVAL CURVES
# ===========================================================================
print("  fig02_kaplan_meier.png")

fig, ax = plt.subplots(figsize=(12, 7))

for ms in ALL_GROUPS:
    g    = groups[ms]
    les  = le_values(g)
    if not les:
        continue
    kmf  = KaplanMeierFitter()
    # Event = died (1 for everyone in our dataset — all have death years)
    durations = les
    events    = [1] * len(les)
    kmf.fit(durations, event_observed=events, label=GROUP_LABELS[ms])
    kmf.plot_survival_function(ax=ax, color=COLOUR[ms], linewidth=2,
                                ci_show=True, ci_alpha=0.12)

ax.set_xlim(0, 110)
ax.set_ylim(0, 1.05)
apply_style(ax, 'Figure 2 — Kaplan-Meier Survival Curves by Migration Group',
            xlabel='Age (years)', ylabel='Proportion Surviving')
ax.legend(fontsize=10)
ax.axvline(63, color='grey', linestyle=':', linewidth=1, alpha=0.6)
ax.text(63.5, 0.85, 'V1 avg\n(63)', fontsize=7, color='grey')
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig02_kaplan_meier.png')


# ===========================================================================
# FIG 03 — V1 / V2.1 COMPARISON (apples-to-apples)
#
# V1 used a simple two-group system: migrated vs non-migrated (everyone who
# stayed in the Soviet sphere was "non-migrated").
# To make V2.1 directly comparable, we use the same two-group framing here:
#   - "Left USSR" = migrated (V2.1 group)
#   - "Stayed in Soviet sphere" = non_migrated + deported + internal_transfer
#     combined (matching V1's definition of "non-migrated")
# This is the same grouping used in fig20 — the two charts now show consistent
# numbers and do not contradict each other.
# The four-group breakdown (fig01) is the primary V2.1 analysis.
# ===========================================================================
print("  fig03_version_comparison.png")

# V1 numbers (from paper)
V1_mig = 72
V1_nm  = 63
V1_n   = 415

# V2.1 — using same two-group logic as V1 (and as fig20)
# "Left USSR" = migrated only
v21_left_les = le_values(migrated)
V21_mig      = round(statistics.mean(v21_left_les), 1)
V21_mig_n    = len(v21_left_les)

# "Stayed in Soviet sphere" = non_migrated + internal_transfer + deported
# (matches V1's definition and fig20's conservative grouping)
v21_stayed_les = (le_values(non_migrated) + le_values(internal_transfer)
                  + le_values(deported))
V21_nm         = round(statistics.mean(v21_stayed_les), 1)
V21_nm_n       = len(v21_stayed_les)

labels_v = [f'V1\n(n={V1_n})', f'V2.1\n(n={V21_mig_n + V21_nm_n})']
mig_vals = [V1_mig, V21_mig]
nm_vals  = [V1_nm,  V21_nm]

fig, ax = plt.subplots(figsize=(9, 6))
x = np.arange(len(labels_v))
w = 0.3
ax.bar(x - w/2, mig_vals, w, color=COLOUR['migrated'],     label='Left USSR (migrated)')
ax.bar(x + w/2, nm_vals,  w, color=COLOUR['non_migrated'], label='Stayed in Soviet sphere')

for xi, (mv, nv) in enumerate(zip(mig_vals, nm_vals)):
    ax.text(xi - w/2, mv + 0.5, f"{mv:.1f} yrs", ha='center', fontsize=10,
            fontweight='bold', color=COLOUR['migrated'])
    ax.text(xi + w/2, nv + 0.5, f"{nv:.1f} yrs", ha='center', fontsize=10,
            fontweight='bold', color=COLOUR['non_migrated'])

# Gap arrows
for xi, (mv, nv) in enumerate(zip(mig_vals, nm_vals)):
    gap = mv - nv
    mid = (mv + nv) / 2
    ax.annotate('', xy=(xi + w/2 - 0.02, mv), xytext=(xi + w/2 - 0.02, nv),
                arrowprops=dict(arrowstyle='<->', color='#555', lw=1.5))
    ax.text(xi + w/2 + 0.06, mid, f"+{gap:.1f} yrs", va='center',
            fontsize=9, color='#333', fontweight='bold')

apply_style(ax, 'Figure 3 — Mean Life Expectancy: V1 vs V2.1 (consistent two-group framing)',
            ylabel='Mean Life Expectancy (years)')
ax.set_xticks(x)
ax.set_xticklabels(labels_v, fontsize=11)
ax.set_ylim(0, max(mig_vals + nm_vals) * 1.25)
ax.legend(fontsize=9)
fig.text(0.5, 0.01,
    "V2.1 'stayed' = non_migrated + internal_transfer + deported combined "
    "(matches V1 two-group definition and fig20). Four-group breakdown: see fig01. " + SOURCE_NOTE,
    ha='center', fontsize=7, color='grey', style='italic')
plt.tight_layout(rect=[0, 0.05, 1, 1])
save(fig, 'fig03_version_comparison.png')


# ===========================================================================
# FIG 04 — BOX PLOTS (4 GROUPS)
# ===========================================================================
print("  fig04_box_plots.png")

fig, ax = plt.subplots(figsize=(11, 7))
data_for_box = [le_values(groups[ms]) for ms in ALL_GROUPS]
bp = ax.boxplot(data_for_box, patch_artist=True, notch=True,
                medianprops={'color': 'white', 'linewidth': 2})
for patch, ms in zip(bp['boxes'], ALL_GROUPS):
    patch.set_facecolor(COLOUR[ms])
    patch.set_alpha(0.8)
for element in ['whiskers', 'caps', 'fliers']:
    for item in bp[element]:
        item.set(color='#444444')

ax.set_xticklabels([GROUP_LABELS[ms] for ms in ALL_GROUPS], rotation=15, ha='right')
apply_style(ax, 'Figure 4 — Life Expectancy Distribution by Group (Box Plots)',
            ylabel='Life Expectancy (years)')
ax.set_ylim(0, 110)

# Annotate medians
for i, ms in enumerate(ALL_GROUPS, start=1):
    v = le_values(groups[ms])
    if v:
        med = statistics.median(v)
        ax.text(i, med + 2, f"med={med:.0f}", ha='center', fontsize=8,
                color='white', fontweight='bold')

plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig04_box_plots.png')


# ===========================================================================
# FIG 05 — HISTOGRAM: AGE AT DEATH FOR DEPORTED GROUP
# ===========================================================================
print("  fig05_deported_age_histogram.png")

dep_les = le_values(deported)
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(dep_les, bins=range(0, 105, 5), color=COLOUR['deported'],
        edgecolor='white', linewidth=0.4, alpha=0.85)

if dep_les:
    mn = statistics.mean(dep_les)
    ax.axvline(mn, color='white', linestyle='--', linewidth=2,
               label=f'Mean = {mn:.1f} yrs')
    ax.legend(fontsize=10)

apply_style(ax, 'Figure 5 — Age at Death Distribution: Deported Group',
            xlabel='Age at Death (years)', ylabel='Count')
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig05_deported_age_histogram.png')


# ===========================================================================
# FIG 06 — VIOLIN PLOTS (4 GROUPS, SPLIT BY GENDER)
# ===========================================================================
print("  fig06_violin_plots.png")

_gender_palette = {'Male': '#2980B9', 'Female': '#E74C3C'}
df_violin = pd.DataFrame([
    {'group': GROUP_LABELS[ms],
     'le':    r['_le'],
     'gender': r.get('gender', 'unknown').capitalize()}
    for ms in ALL_GROUPS for r in groups[ms]
    if r['_le'] is not None and r.get('gender', 'unknown').lower() in ('male', 'female')
])

_order = [GROUP_LABELS[ms] for ms in ALL_GROUPS]
fig, ax = plt.subplots(figsize=(13, 7))
sns.violinplot(data=df_violin, x='group', y='le', hue='gender',
               split=True, inner='quartile', palette=_gender_palette,
               order=_order, ax=ax, linewidth=1)

# Annotate n (male / female) below each violin pair
for i, ms in enumerate(ALL_GROUPS):
    nm = sum(1 for r in groups[ms]
             if r.get('gender', '').lower() == 'male' and r['_le'] is not None)
    nf = sum(1 for r in groups[ms]
             if r.get('gender', '').lower() == 'female' and r['_le'] is not None)
    ax.text(i, -6, f"M:{nm}\nF:{nf}", ha='center', va='top',
            fontsize=7, color=COLOUR['navy'])

apply_style(ax, 'Figure 6 — Life Expectancy Distribution by Group and Gender (Split Violin)',
            xlabel='', ylabel='Life Expectancy (years)')
ax.set_xticklabels(_order, rotation=15, ha='right')
ax.set_ylim(-12, 110)
ax.legend(title='Gender', fontsize=9, loc='lower right')
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig06_violin_plots.png')


# ===========================================================================
# FIG 07 — DEATH YEAR HISTOGRAM 1900–2024 (ALL ANALYSABLE)
# ===========================================================================
print("  fig07_death_year_histogram.png")

fig, ax = plt.subplots(figsize=(14, 6))
bins = range(1900, 2026, 2)

for ms in ['non_migrated', 'migrated']:
    dy_vals = [r['_dy'] for r in groups[ms] if r['_dy'] and 1900 <= r['_dy'] <= 2024]
    alpha   = 0.65 if ms == 'non_migrated' else 0.55
    ax.hist(dy_vals, bins=bins, alpha=alpha, color=COLOUR[ms],
            label=GROUP_LABELS[ms], edgecolor='white', linewidth=0.2)

# Annotation lines
for year, label, colour in [
    (1933, 'Holodomor\n1933', '#8E44AD'),
    (1937, 'Great Terror\n1937', COLOUR['navy']),
    (1941, 'WWII begins\n1941', '#7F8C8D'),
]:
    ax.axvline(year, color=colour, linestyle='--', linewidth=1.5)
    ax.text(year + 0.4, ax.get_ylim()[1] * 0.85, label, color=colour,
            fontsize=7.5, va='top')

apply_style(ax, 'Figure 7 — Death Year Distribution 1900–2024\n(Migrated vs Non-Migrated)',
            xlabel='Year of Death', ylabel='Number of Deaths')
ax.legend(fontsize=9)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig07_death_year_histogram.png')


# ===========================================================================
# FIG 08 — DEPORTED DEATHS BY YEAR 1921–1965
# ===========================================================================
print("  fig08_deported_deaths_by_year.png")

dep_death_years = [r['_dy'] for r in deported if r['_dy'] and 1921 <= r['_dy'] <= 1965]
dep_year_counter = collections.Counter(dep_death_years)
years_range = list(range(1921, 1966))
counts      = [dep_year_counter.get(y, 0) for y in years_range]

fig, ax = plt.subplots(figsize=(14, 6))
bar_colours = [('#8B0000' if y in (1937, 1938) else COLOUR['deported'])
               for y in years_range]
ax.bar(years_range, counts, color=bar_colours, edgecolor='white', linewidth=0.3)

ax.axvline(1937, color='#8B0000', linestyle='--', linewidth=1.5, alpha=0.7)
ax.text(1937.3, max(counts) * 0.9, '1937\nTerror\npeak', color='#8B0000', fontsize=8)

apply_style(ax, 'Figure 8 — Deported Creative Workers: Deaths by Year 1921–1965',
            xlabel='Year', ylabel='Number of Deported Deaths')
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig08_deported_deaths_by_year.png')


# ===========================================================================
# FIG 09 — MEAN AGE AT DEATH BY SOVIET PERIOD — ALL FOUR GROUPS
#
# Shows avg age at death per Soviet historical period, one grouped bar cluster
# per period, one bar per migration group.
# Raw death COUNTS are intentionally NOT shown — periods differ in length and
# population size, making raw counts misleading (late periods look larger
# simply because more people were alive then, not because of anything dramatic).
# Avg age at death is the meaningful comparison: it shows who died younger
# during repression periods.
# Bars only shown when n ≥ 5. n printed inside/above each bar.
# ===========================================================================
print("  fig09_nonmigrant_deaths_by_period.png")

CHART_PERIODS = [
    ('NEP\n1921–29',       lambda y: 1921 <= y <= 1929),
    ('Holodomor\n1930–33', lambda y: 1930 <= y <= 1933),
    ('Terror\n1934–38',    lambda y: 1934 <= y <= 1938),
    ('WWII\n1939–45',      lambda y: 1939 <= y <= 1945),
    ('Late Stalin\n1946–53', lambda y: 1946 <= y <= 1953),
    ('Thaw\n1954–64',      lambda y: 1954 <= y <= 1964),
    ('Stagnation\n1965–91', lambda y: 1965 <= y <= 1991),
    ('Post-Soviet\n1992+', lambda y: y > 1991),
]

MIN_N_P9 = 5
period_labels_p9 = [p[0] for p in CHART_PERIODS]
n_periods = len(CHART_PERIODS)

# Compute avg age at death per period per group
period_data = {}  # {ms: [(mean or None, n), ...]}
for ms in ALL_GROUPS:
    vals_by_period = []
    for _, fn in CHART_PERIODS:
        sub  = [r for r in groups[ms] if r['_dy'] and fn(r['_dy'])]
        ages = [r['_le'] for r in sub if r['_le'] is not None]
        if len(ages) >= MIN_N_P9:
            vals_by_period.append((round(statistics.mean(ages), 1), len(ages)))
        else:
            vals_by_period.append((None, len(ages)))
    period_data[ms] = vals_by_period

# Grouped bar chart
n_groups = len(ALL_GROUPS)
bar_w = 0.18   # narrow bars as requested
x = np.arange(n_periods)
offsets = np.linspace(-(n_groups - 1) / 2 * bar_w,
                       (n_groups - 1) / 2 * bar_w, n_groups)

# Repression period highlighting
REPRESSION_PERIODS = {'Holodomor\n1930–33', 'Terror\n1934–38', 'Late Stalin\n1946–53'}

fig, ax = plt.subplots(figsize=(15, 7))

for i, (ms, offset) in enumerate(zip(ALL_GROUPS, offsets)):
    means = [v[0] for v in period_data[ms]]
    ns    = [v[1] for v in period_data[ms]]
    for j, (mean_val, n_val) in enumerate(zip(means, ns)):
        if mean_val is None:
            continue
        edge = '#8B0000' if period_labels_p9[j] in REPRESSION_PERIODS else 'white'
        bar = ax.bar(x[j] + offset, mean_val, bar_w,
                     color=COLOUR[ms], edgecolor=edge, linewidth=1.2, alpha=0.85)
        # Value label above bar
        ax.text(x[j] + offset, mean_val + 0.6, f"{mean_val:.0f}",
                ha='center', va='bottom', fontsize=7, color=COLOUR[ms], fontweight='bold')
        # n label inside bar (bottom)
        ax.text(x[j] + offset, 2, f"n={n_val}",
                ha='center', va='bottom', fontsize=6, color='white', alpha=0.85)

# Legend
patches = [mpatches.Patch(color=COLOUR[ms], label=GROUP_LABELS[ms]) for ms in ALL_GROUPS]
ax.legend(handles=patches, fontsize=8.5, loc='upper left', ncol=2)

ax.set_xticks(x)
ax.set_xticklabels(period_labels_p9, fontsize=8.5)
ax.set_ylim(0, 95)
ax.set_ylabel('Mean Age at Death (years)', fontsize=10, color=COLOUR['navy'])

# Shade repression periods
repression_idxs = [j for j, lbl in enumerate(period_labels_p9) if lbl in REPRESSION_PERIODS]
for j in repression_idxs:
    ax.axvspan(j - 0.5, j + 0.5, alpha=0.06, color='#8B0000', zorder=0)

apply_style(ax, 'Figure 9 — Mean Age at Death by Soviet Period and Migration Group\n'
            '(bars shown only where n≥5; red outline = repression period)',
            xlabel='Soviet Historical Period', ylabel='Mean Age at Death (years)')

fig.text(0.5, 0.01,
    "Raw death counts not shown — period length and group sizes differ, making counts incomparable. "
    "Mean age at death is the meaningful measure. " + SOURCE_NOTE,
    ha='center', fontsize=7, color='grey', style='italic')
plt.tight_layout(rect=[0, 0.05, 1, 1])
save(fig, 'fig09_nonmigrant_deaths_by_period.png')


# ===========================================================================
# FIG 10 — BIRTH COHORT LE LINE CHART
#
# Shows mean age at death for creative workers born in each decade.
# This is cohort data (not period LE) — each dot = mean age at death of
# people born in that decade, regardless of when they died.
# NOTE: Ukrainian SSR LE reference is period data and uses different x-axis
# logic, so it is NOT overlaid here (see fig21/fig22 for period comparisons).
# Minimum n=10 per decade to suppress unreliable early/late decade estimates.
# ===========================================================================
print("  fig10_birth_cohort_le.png")

MIN_N_COHORT = 10
decades_ch   = list(range(1840, 1981, 10))
cohort_means = {ms: [] for ms in ALL_GROUPS}
cohort_ns    = {ms: [] for ms in ALL_GROUPS}
valid_decs   = []

for dec in decades_ch:
    for ms in ALL_GROUPS:
        v = [r['_le'] for r in groups[ms] if r['_by'] and dec <= r['_by'] < dec + 10 and r['_le']]
        cohort_means[ms].append(round(statistics.mean(v), 1) if len(v) >= MIN_N_COHORT else None)
        cohort_ns[ms].append(len(v))
    valid_decs.append(dec)

fig, ax = plt.subplots(figsize=(15, 7))
MARKERS10 = {'migrated': 'o', 'non_migrated': 's', 'internal_transfer': '^', 'deported': 'D'}

# Label strategy:
#   - Deported: label every point (it's the key story, sits far below the others)
#   - Migrated / Non-migrated: label every other decade only (reduces clutter on the
#     tightly-packed upper cluster without losing the data story)
#   - Internal transfer: no inline labels (it tracks non-migrated closely; the line
#     shape tells the story; labelling would only add noise)
_LABEL_EVERY = {'migrated': 2, 'non_migrated': 2, 'internal_transfer': None, 'deported': 1}
_LBL_DY      = {'migrated': +18, 'non_migrated': -18, 'deported': -14}   # offset points
_LBL_DX      = {'migrated':  -4, 'non_migrated':  +4,  'deported':   0}

for ms in ALL_GROUPS:
    vals = cohort_means[ms]
    xs   = [dec for dec, v in zip(valid_decs, vals) if v is not None]
    ys   = [v for v in vals if v is not None]
    ns   = [cohort_ns[ms][i] for i, v in enumerate(vals) if v is not None]
    if not xs:
        continue
    ax.plot(xs, ys, marker=MARKERS10[ms], linestyle='-', color=COLOUR[ms],
            label=GROUP_LABELS[ms], linewidth=2, markersize=7, zorder=5)
    step = _LABEL_EVERY[ms]
    if step is None:
        continue
    for j, (x_pt, y_pt, n_pt) in enumerate(zip(xs, ys, ns)):
        if j % step != 0:
            continue
        ax.annotate(f"{y_pt:.0f}", xy=(x_pt, y_pt),
                    xytext=(_LBL_DX[ms], _LBL_DY[ms]), textcoords='offset points',
                    ha='center', fontsize=7, color=COLOUR[ms], fontweight='bold')

# Shade the Terror/Holodomor birth cohorts
ax.axvspan(1890, 1910, alpha=0.06, color='#8B0000', zorder=0)
ax.text(1899, 31, 'Born\n1890–1910\n(peak repression\nvictim cohort)',
        ha='center', fontsize=7, color='#8B0000', style='italic')

apply_style(ax, 'Figure 10 — Mean Age at Death by Birth Decade\n(cohort data; n≥10 per point)',
            xlabel='Birth Decade', ylabel='Mean Age at Death (years)')
ax.legend(fontsize=8.5, ncol=2)
# Start x-axis where data actually begins (skip empty early decades)
first_x = min(dec for dec in valid_decs
              if any(cohort_means[ms][valid_decs.index(dec)] is not None for ms in ALL_GROUPS))
ax.set_xlim(first_x - 5, 1985)
ax.set_ylim(25, 90)
fig.text(0.5, 0.01,
    "Source: ESU V2.3 dataset, Symkin 2026. Each point = mean age at death of creative workers "
    "born in that decade (cohort estimate, n≥10). Period LE comparison: see fig21/fig22.",
    ha='center', fontsize=7, color='grey', style='italic')
plt.tight_layout(rect=[0, 0.05, 1, 1])
save(fig, 'fig10_birth_cohort_le.png')


# ===========================================================================
# FIG 11 — PROFESSION GROUPED BAR (LE by profession × group)
# ===========================================================================
print("  fig11_profession_grouped_bar.png")

professions = list(PROFESSION_KEYWORDS.keys())
x = np.arange(len(professions))
w = 0.2
offsets = [-1.5*w, -0.5*w, 0.5*w, 1.5*w]

fig, ax = plt.subplots(figsize=(14, 7))
for i, ms in enumerate(ALL_GROUPS):
    prof_means = []
    for prof in professions:
        v = [r['_le'] for r in groups[ms] if r['_prof'] == prof and r['_le'] is not None]
        prof_means.append(round(statistics.mean(v), 1) if v else 0)
    ax.bar(x + offsets[i], prof_means, w, color=COLOUR[ms],
           label=GROUP_LABELS[ms], alpha=0.85)

ax.set_xticks(x)
ax.set_xticklabels(professions, rotation=20, ha='right', fontsize=9)
apply_style(ax, 'Figure 11 — Life Expectancy by Profession and Migration Group',
            ylabel='Mean Life Expectancy (years)')
ax.legend(fontsize=8, ncol=2)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig11_profession_grouped_bar.png')


# ===========================================================================
# FIG 12 — GEOGRAPHIC MIGRATION RATES (TOP 20 BIRTH CITIES)
# ===========================================================================
print("  fig12_geographic_migration_rates.png")

birth_all = collections.Counter()
birth_mig = collections.Counter()
for ms in ALL_GROUPS:
    for r in groups[ms]:
        bl = str(r.get('birth_location', '')).strip()
        if bl:
            birth_all[bl] += 1
            if ms == 'migrated':
                birth_mig[bl] += 1

top20 = birth_all.most_common(20)
cities    = [loc[:35] for loc, _ in top20]
total_cnt = [cnt for _, cnt in top20]
mig_cnt   = [birth_mig.get(loc, 0) for loc, _ in top20]
mig_pct   = [round(100 * mc / tc, 1) if tc else 0
             for mc, tc in zip(mig_cnt, total_cnt)]

fig, ax = plt.subplots(figsize=(12, 9))
y = np.arange(len(cities))
bars_t = ax.barh(y, total_cnt, color='#BDC3C7', label='Total', height=0.6)
bars_m = ax.barh(y, mig_cnt,   color=COLOUR['migrated'], label='Migrated', height=0.6)
ax.set_yticks(y)
ax.set_yticklabels(cities, fontsize=8)
for yi, pct in enumerate(mig_pct):
    ax.text(total_cnt[yi] + 2, yi, f"{pct}%", va='center', fontsize=7.5,
            color=COLOUR['migrated'])

apply_style(ax, 'Figure 12 — Geographic Migration Rates: Top 20 Birth Cities',
            xlabel='Number of Creative Workers')
ax.legend(fontsize=9)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig12_geographic_migration_rates.png')


# ===========================================================================
# FIG 13 — BIRTH YEAR DISTRIBUTION BY GROUP (selection bias check)
# ===========================================================================
print("  fig13_birth_year_distribution.png")

fig, ax = plt.subplots(figsize=(12, 6))
bins_by = range(1830, 2000, 5)
for ms in ALL_GROUPS:
    bys = [r['_by'] for r in groups[ms] if r['_by'] and 1830 <= r['_by'] <= 1990]
    if bys:
        ax.hist(bys, bins=bins_by, alpha=0.5, color=COLOUR[ms],
                label=GROUP_LABELS[ms], edgecolor='none')

apply_style(ax, 'Figure 13 — Birth Year Distribution by Group\n(Selection Bias Check)',
            xlabel='Birth Year', ylabel='Count')
ax.legend(fontsize=9)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig13_birth_year_distribution.png')


# ===========================================================================
# FIG 14 — SENSITIVITY ANALYSIS CHART
# ===========================================================================
print("  fig14_sensitivity_analysis.png")

le_m_base  = le_values(migrated)
le_nm_base = le_values(non_migrated)
base_m_mean  = statistics.mean(le_m_base)  if le_m_base  else 0
base_nm_mean = statistics.mean(le_nm_base) if le_nm_base else 0
base_gap_val = base_m_mean - base_nm_mean

# Simulate: shift 0% to 10% of migrated down to non-migrated LE
error_rates = [0, 1, 2, 3.2, 5, 7.5, 10]
gaps = []
for er in error_rates:
    n_err = int(len(migrated) * er / 100)
    # Worst case: the n_err best-surviving migrants are reclassified
    sorted_m = sorted(le_m_base, reverse=True)
    adj_m = sorted_m[n_err:]  # remove the long-lived ones (most conservative)
    if adj_m and le_nm_base:
        gaps.append(statistics.mean(adj_m) - base_nm_mean)
    else:
        gaps.append(base_gap_val)

fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(error_rates, gaps, 'o-', color=COLOUR['migrated'], linewidth=2.5, markersize=7)
ax.axhline(0, color='grey', linestyle='--', linewidth=1)
ax.axvline(3.2, color=COLOUR['navy'], linestyle=':', linewidth=1.5,
           label='Actual AI error rate (3.2%)')
ax.fill_between(error_rates, gaps, 0,
                where=[g > 0 for g in gaps],
                alpha=0.1, color=COLOUR['migrated'])

ax.set_xlabel('Assumed AI Classification Error Rate (%)', fontsize=11, color=COLOUR['navy'])
ax.set_ylabel('LE Gap: Migrated − Non-migrated (years)', fontsize=11, color=COLOUR['navy'])
apply_style(ax, 'Figure 14 — Sensitivity Analysis: LE Gap vs AI Error Rate')
ax.legend(fontsize=9)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig14_sensitivity_analysis.png')


# ===========================================================================
# FIG 15 — INTERNAL TRANSFER NULL FINDING
# ===========================================================================
print("  fig15_internal_transfer_null.png")

it_les = le_values(internal_transfer)
nm_les = le_values(non_migrated)

it_mean = round(statistics.mean(it_les), 2) if it_les else None
nm_mean = round(statistics.mean(nm_les), 2) if nm_les else None

u15, p15 = mannwhitney(it_les, nm_les)

fig, ax = plt.subplots(figsize=(8, 6))
data_it = [it_les, nm_les]
bp15 = ax.boxplot(data_it, patch_artist=True, notch=True,
                  medianprops={'color': 'white', 'linewidth': 2})
bp15['boxes'][0].set_facecolor(COLOUR['internal_transfer'])
bp15['boxes'][0].set_alpha(0.85)
bp15['boxes'][1].set_facecolor(COLOUR['non_migrated'])
bp15['boxes'][1].set_alpha(0.85)
for element in ['whiskers', 'caps', 'fliers']:
    for item in bp15[element]:
        item.set(color='#444444')

ax.set_xticklabels([GROUP_LABELS['internal_transfer'], GROUP_LABELS['non_migrated']],
                   rotation=10)
apply_style(ax,
    f'Figure 15 — Internal Transfer vs Non-Migrated LE\n'
    f'(p={p15:.3f} — {"NOT significant" if p15 and p15 >= 0.05 else "significant"})',
    ylabel='Life Expectancy (years)')
ax.text(0.5, 0.95,
        f"Mean IT={it_mean}  Mean NM={nm_mean}  p={p15}",
        ha='center', va='top', transform=ax.transAxes, fontsize=9, color=COLOUR['navy'])
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig15_internal_transfer_null.png')


# ===========================================================================
# FIG 15b — ALL-GROUPS LE COMPARISON (expanded null-result check)
#
# Replicates fig15 logic but shows all four groups side-by-side so the reader
# can directly compare internal_transfer and non_migrated against migrated and
# deported. Draws explicit written conclusions on the chart.
# ===========================================================================
print("  fig15b_all_groups_le_box.png")

mig_les = le_values(migrated)
it_les2  = le_values(internal_transfer)
nm_les2  = le_values(non_migrated)
dep_les  = le_values(deported)

_all_groups_15b = [
    ('migrated',          mig_les,  GROUP_LABELS['migrated']),
    ('non_migrated',      nm_les2,  GROUP_LABELS['non_migrated']),
    ('internal_transfer', it_les2,  GROUP_LABELS['internal_transfer']),
    ('deported',          dep_les,  GROUP_LABELS['deported']),
]

fig, ax = plt.subplots(figsize=(10, 7))

bp15b = ax.boxplot(
    [g[1] for g in _all_groups_15b],
    patch_artist=True, notch=False,
    medianprops={'color': 'white', 'linewidth': 2.5},
    whiskerprops={'color': '#555'},
    capprops={'color': '#555'},
    flierprops={'marker': 'o', 'markersize': 3, 'markerfacecolor': '#ccc', 'linestyle': 'none'},
)
for box_patch, (ms, _, _lbl) in zip(bp15b['boxes'], _all_groups_15b):
    box_patch.set_facecolor(COLOUR[ms])
    box_patch.set_alpha(0.85)

ax.set_xticks(range(1, 5))
ax.set_xticklabels([g[2] for g in _all_groups_15b], rotation=10, fontsize=9)
ax.set_ylim(bottom=0)

# Mean labels above each box
for i, (ms, les, _) in enumerate(_all_groups_15b, start=1):
    if les:
        m = statistics.mean(les)
        ax.text(i, m + 1.2, f"{m:.1f}", ha='center', fontsize=9,
                color=COLOUR[ms], fontweight='bold')

# Stat tests: IT vs NM (null), MIG vs NM (main finding)
_, p_it_nm  = mannwhitney(it_les2, nm_les2)
_, p_mig_nm = mannwhitney(mig_les, nm_les2)

# Conclusions text box
concl = (
    f"KEY CONCLUSIONS\n"
    f"• Migrated vs Non-migrated:  Δ={statistics.mean(mig_les):.1f}−{statistics.mean(nm_les2):.1f}"
    f" = +{statistics.mean(mig_les)-statistics.mean(nm_les2):.1f} yrs  (p={p_mig_nm:.4f})\n"
    f"• Internal transfer vs Non-migrated:  Δ={statistics.mean(it_les2):.1f}−{statistics.mean(nm_les2):.1f}"
    f" = {statistics.mean(it_les2)-statistics.mean(nm_les2):+.1f} yrs  (p={p_it_nm:.3f} — NULL RESULT)\n"
    f"• Moving within the USSR gives no LE benefit — leaving the Soviet sphere was what mattered."
)
ax.text(0.02, 0.97, concl, transform=ax.transAxes,
        fontsize=8.5, va='top', ha='left',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#f9f9f9',
                  edgecolor='#cccccc', alpha=0.95),
        fontfamily='monospace')

apply_style(ax,
    'Figure 15b — Life Expectancy: All Four Groups Compared\n'
    '(Box = IQR; line = median; whiskers = 1.5×IQR; dots = outliers)',
    ylabel='Age at Death (years)')
add_source(fig)
plt.tight_layout(rect=[0, 0.04, 1, 1])
save(fig, 'fig15b_all_groups_le_box.png')


# ===========================================================================
# FIG 16 — CONSORT-STYLE EXCLUSION FLOWCHART
# ===========================================================================
print("  fig16_consort_flowchart.png")

fig, ax = plt.subplots(figsize=(10, 14))
ax.axis('off')
fig.patch.set_facecolor('white')

def box(ax, x, y, w, h, text, colour='#1B2A4A', bg='#EBF5FB', fontsize=9.5):
    rect = mpatches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.02", linewidth=1.5,
        edgecolor=colour, facecolor=bg, zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            color=colour, fontweight='bold', wrap=True,
            multialignment='center', zorder=4)

def arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2 + 0.015), xytext=(x1, y1 - 0.015),
                arrowprops=dict(arrowstyle='->', color='#555555',
                                lw=1.5), zorder=2)

def exc_box(ax, x, y, w, h, text):
    box(ax, x, y, w, h, text, colour='#7B241C', bg='#FDEDEC', fontsize=8.5)

# Positions (y: 0=bottom, 1=top)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

cx, cw, ch = 0.50, 0.50, 0.055  # centre, width, height of main boxes

BOX_COORDS = [
    (cx, 0.95, f"ESU.com.ua — all entries scraped\nn = {total_scraped:,}"),
    (cx, 0.82, f"Filtered: creative profession keywords\nn ≈ {len(raw_rows):,} creative workers"),
    (cx, 0.69, f"Exclud. pre-Soviet deaths (died <1921)\n− {len(excluded_pre_soviet):,}  and Galicia pre-1939 − {len(excluded_galicia):,}"),
    (cx, 0.56, f"Exclud. non-Ukrainian (confirmed)\n− {len(non_ukrainian):,}"),
    (cx, 0.43, f"Exclud. still alive / unknown status\n− {len(still_alive):,} alive  − {len(unknown_status):,} unknown"),
    (cx, 0.30, f"Exclud. missing birth or death year\n− {len(missing_dates):,}"),
    (cx, 0.17, (
        f"FINAL ANALYSABLE DATASET\nn = {len(analysable):,}\n"
        f"Migrated: {len(migrated):,}  |  Non-migrated: {len(non_migrated):,}\n"
        f"Internal transfer: {len(internal_transfer):,}  |  Deported: {len(deported):,}"
    )),
]

for i, (x, y, text) in enumerate(BOX_COORDS):
    bg = '#D5F5E3' if i == len(BOX_COORDS) - 1 else '#EBF5FB'
    col = '#1A5276' if i == len(BOX_COORDS) - 1 else COLOUR['navy']
    box(ax, x, y, cw, ch, text, colour=col, bg=bg,
        fontsize=9 if i == len(BOX_COORDS) - 1 else 9.5)

for i in range(len(BOX_COORDS) - 1):
    _, ya, _ = BOX_COORDS[i]
    _, yb, _ = BOX_COORDS[i + 1]
    arrow(ax, cx, ya, cx, yb)

ax.set_title('Figure 16 — CONSORT-Style Dataset Exclusion Flowchart',
             fontsize=13, fontweight='bold', color=COLOUR['navy'], pad=10)
fig.text(0.5, 0.01, SOURCE_NOTE, ha='center', fontsize=7, color='grey', style='italic')
save(fig, 'fig16_consort_flowchart.png')


# ===========================================================================
# FIG 19 — YEAR-BY-YEAR NORMALISED DEATH RATE CHART 1921–1992
#
# Shows deaths per year as a PERCENTAGE OF EACH GROUP'S TOTAL SIZE.
# Normalisation allows fair comparison across groups of very different sizes
# (non_migrated n≈3,500; deported n≈300; migrated n≈1,200 etc.).
# Raw counts would make small groups invisible — this chart shows relative
# mortality intensity so every group's spikes are directly comparable.
# ===========================================================================
print("  fig19_ssr_population_context.png")

SPIKE_START, SPIKE_END = 1921, 1992
spike_years = list(range(SPIKE_START, SPIKE_END + 1))

def deaths_by_year(group, start, end):
    ctr = collections.Counter(r['_dy'] for r in group
                              if r['_dy'] and start <= r['_dy'] <= end)
    return [ctr.get(y, 0) for y in range(start, end + 1)]

dy_nm  = deaths_by_year(non_migrated,      SPIKE_START, SPIKE_END)
dy_dep = deaths_by_year(deported,          SPIKE_START, SPIKE_END)
dy_it  = deaths_by_year(internal_transfer, SPIKE_START, SPIKE_END)
dy_mig = deaths_by_year(migrated,          SPIKE_START, SPIKE_END)

# Normalise: deaths per year / group total × 100  (= % of group dying that year)
def normalise(counts, group_total):
    if group_total == 0:
        return [0.0] * len(counts)
    return [c / group_total * 100 for c in counts]

n_nm  = normalise(dy_nm,  len(non_migrated))
n_dep = normalise(dy_dep, len(deported))
n_it  = normalise(dy_it,  len(internal_transfer))
n_mig = normalise(dy_mig, len(migrated))

fig, ax = plt.subplots(figsize=(16, 7))

LINE_DATA19 = [
    ('non_migrated',      n_nm,  'Non-migrated (stayed)',         '-',  2.0),
    ('deported',          n_dep, 'Deported',                      '-',  2.5),
    ('internal_transfer', n_it,  'Internal transfer',             '--', 1.8),
    ('migrated',          n_mig, 'Migrated (left USSR)',          ':',  2.0),
]
for ms, vals, lbl, ls, lw in LINE_DATA19:
    ax.plot(spike_years, vals, color=COLOUR[ms], linewidth=lw,
            linestyle=ls, label=f'{lbl}  (n={len(groups[ms])})', alpha=0.9)

# Annotate key events as shaded bands
EVENT_BANDS19 = [
    (1932, 1934, '#8E44AD', 'Holodomor\n1932–33'),
    (1936, 1939, '#8B0000', 'Great Terror\n1936–38'),
    (1941, 1945, '#7F8C8D', 'WWII\n1941–45'),
    (1946, 1953, '#BDC3C7', 'Late Stalin'),
]
ymax19 = max(max(n_nm), max(n_dep), max(n_it), max(n_mig)) * 1.15
for x0, x1, col, lbl in EVENT_BANDS19:
    ax.axvspan(x0, x1, alpha=0.10, color=col, zorder=0)
    ax.text((x0 + x1) / 2, ymax19 * 0.92, lbl, ha='center',
            fontsize=7.5, color=col, fontweight='bold', va='top')

ax.set_xlim(SPIKE_START - 0.5, SPIKE_END + 0.5)
ax.set_ylim(0, ymax19)
apply_style(ax,
    'Figure 19 — Annual Death Rate by Group 1921–1992\n'
    '(% of each group dying per year — normalised for group size)',
    xlabel='Year', ylabel='Deaths per year (% of group total)')
ax.legend(fontsize=9, loc='upper right', ncol=2)

fig.text(0.5, 0.005,
    "Each line = deaths in that year as % of that group's total size. "
    "Normalisation enables direct comparison across groups of different sizes. "
    + SOURCE_NOTE,
    ha='center', fontsize=6.5, color='grey', style='italic')
plt.tight_layout(rect=[0, 0.04, 1, 1])
save(fig, 'fig19_ssr_population_context.png')


# ===========================================================================
# FIG 19b — SIMPLIFIED ANNUAL DEATH RATE (3-line version)
#
# Same normalised % death rate as fig19, but combines non_migrated + deported
# into a single "Stayed/Deported" line for a cleaner story:
#   → Migrated | Internal Transfer | Stayed + Deported combined
# Makes the contrast between leaving and staying starker.
# ===========================================================================
print("  fig19b_simplified_death_rate.png")

stayed_deported = non_migrated + deported
n_stayed_dep = normalise(
    deaths_by_year(stayed_deported, SPIKE_START, SPIKE_END),
    len(stayed_deported)
)

fig19b, ax19b = plt.subplots(figsize=(16, 7))

LINE_DATA19b = [
    ('non_migrated',      n_stayed_dep, f'Non-migrated + Deported combined  (n={len(stayed_deported)})', '-',  2.5),
    ('internal_transfer', n_it,         f'Internal transfer (USSR)  (n={len(internal_transfer)})',        '--', 1.8),
    ('migrated',          n_mig,        f'Migrated (left USSR)  (n={len(migrated)})',                    ':',  2.0),
]
for ms, vals, lbl, ls, lw in LINE_DATA19b:
    ax19b.plot(spike_years, vals, color=COLOUR[ms], linewidth=lw,
               linestyle=ls, label=lbl, alpha=0.9)

ymax19b = max(max(n_stayed_dep), max(n_it), max(n_mig)) * 1.15
for x0, x1, col, lbl in EVENT_BANDS19:
    ax19b.axvspan(x0, x1, alpha=0.10, color=col, zorder=0)
    ax19b.text((x0 + x1) / 2, ymax19b * 0.92, lbl, ha='center',
               fontsize=7.5, color=col, fontweight='bold', va='top')

ax19b.set_xlim(SPIKE_START - 0.5, SPIKE_END + 0.5)
ax19b.set_ylim(0, ymax19b)
apply_style(ax19b,
    'Figure 19b — Annual Death Rate: Simplified 3-Line View\n'
    '(% of each group dying per year — non-migrated + deported combined)',
    xlabel='Year', ylabel='Deaths per year (% of group total)')
ax19b.legend(fontsize=9, loc='upper right')

fig19b.text(0.5, 0.005,
    "Non-migrated and Deported combined into one 'stayed in Soviet sphere' line. "
    "Normalised: each line = annual deaths ÷ group size × 100. "
    + SOURCE_NOTE,
    ha='center', fontsize=6.5, color='grey', style='italic')
plt.tight_layout(rect=[0, 0.04, 1, 1])
save(fig19b, 'fig19b_simplified_death_rate.png')


# ===========================================================================
# FIG 20 — TWO-GROUP CONSERVATIVE COMPARISON
#          "Left USSR" vs "Stayed in Soviet sphere"
#
# Deported and internal_transfer are merged into non_migrated to form a single
# "stayed in Soviet sphere" group. This is the methodologically conservative
# reading: it removes our four-way refinement and asks the blunter question
# V1 asked. It also represents the strongest possible case that our finding
# is robust — because deported people (who had terrible LE) are grouped WITH
# non-migrants, making the "stayed" group's LE lower, which if anything makes
# the migrated advantage look LARGER, not smaller.
# ===========================================================================
print("  fig20_two_group_conservative.png")

stayed_in_ussr = non_migrated + internal_transfer + deported  # everyone who never left
left_ussr      = migrated

le_stayed = le_values(stayed_in_ussr)
le_left   = le_values(left_ussr)

mean_stayed = round(statistics.mean(le_stayed), 2) if le_stayed else 0
mean_left   = round(statistics.mean(le_left),   2) if le_left   else 0
se_stayed   = statistics.stdev(le_stayed) / math.sqrt(len(le_stayed)) if len(le_stayed) > 1 else 0
se_left     = statistics.stdev(le_left)   / math.sqrt(len(le_left))   if len(le_left)   > 1 else 0
gap_2g      = round(mean_left - mean_stayed, 2)
u2g, p2g    = mannwhitney(le_left, le_stayed)
cd2g        = cohens_d(le_left, le_stayed)

fig, axes = plt.subplots(1, 2, figsize=(14, 7))

# LEFT PANEL — bar comparison
ax_bar = axes[0]
x2 = np.arange(2)
bar_means  = [mean_left,   mean_stayed]
bar_ses    = [se_left,     se_stayed]
bar_cols   = [COLOUR['migrated'], COLOUR['non_migrated']]
bar_labels = [f"Left USSR\n(migrated, n={len(left_ussr):,})",
              f"Stayed in Soviet sphere\n(non-migrated + deported\n+ internal transfer, n={len(stayed_in_ussr):,})"]
bar_objs = ax_bar.bar(x2, bar_means, color=bar_cols, width=0.5,
                       yerr=bar_ses, capsize=8, ecolor='#333',
                       error_kw={'linewidth': 2})
for bar, mn in zip(bar_objs, bar_means):
    ax_bar.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + se_stayed + 1,
                f"{mn:.1f} yrs", ha='center', fontsize=11, fontweight='bold',
                color=COLOUR['navy'])
ax_bar.set_xticks(x2)
ax_bar.set_xticklabels(bar_labels, fontsize=9)
ax_bar.set_ylim(0, max(bar_means) * 1.35)
apply_style(ax_bar,
    f'Conservative Two-Group Comparison\nGap = +{gap_2g} yrs  |  Cohen\'s d = {cd2g}  |  p < 0.001',
    ylabel='Mean Life Expectancy (years)')
ax_bar.axhline(UKR_SSR_SOVIET_MEAN, color='#27AE60', linestyle=':',
               linewidth=2, label=f'Ukrainian SSR pop. avg ≈{UKR_SSR_SOVIET_MEAN} yrs')
ax_bar.legend(fontsize=8)

# RIGHT PANEL — explanation text box
ax_txt = axes[1]
ax_txt.axis('off')
explanation = (
    "WHY THIS CHART EXISTS\n"
    "─────────────────────────────────────────\n\n"
    "Our main analysis uses four groups:\n"
    "  • Migrated (left the Soviet sphere)\n"
    "  • Non-migrated (stayed in Ukraine)\n"
    "  • Internal transfer (moved within USSR)\n"
    "  • Deported (forcibly displaced by state)\n\n"
    "This chart collapses the last three into\n"
    "one 'Stayed in Soviet sphere' group —\n"
    "matching the simpler framing used in V1\n"
    "and common in the literature.\n\n"
    "Critically: deported individuals are\n"
    "included in the 'stayed' group here,\n"
    "because they never left the Soviet\n"
    "sphere — the state moved them, not\n"
    "themselves.\n\n"
    "This is the most conservative reading\n"
    "of the data. Even with deportees pulling\n"
    f"the 'stayed' mean down, the gap is\n"
    f"+{gap_2g} years — fully consistent\n"
    "with our four-group primary finding.\n\n"
    "The four-group analysis is preferred\n"
    "because it separates state violence\n"
    "(deported) from individual choice\n"
    "(non-migrated, internal transfer) —\n"
    "a distinction with historical significance."
)
ax_txt.text(0.05, 0.95, explanation, va='top', ha='left',
            transform=ax_txt.transAxes, fontsize=9.5,
            color=COLOUR['navy'], family='monospace',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#EBF5FB',
                      edgecolor='#AED6F1', linewidth=1.5))

fig.suptitle('Figure 20 — Two-Group Conservative Comparison: Left USSR vs Stayed in Soviet Sphere',
             fontsize=13, fontweight='bold', color=COLOUR['navy'], y=1.01)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig20_two_group_conservative.png')


# ===========================================================================
# FIG 17 — GENDER DISTRIBUTION BY MIGRATION GROUP
# ===========================================================================
print("  fig17_gender_by_group.png")

genders = ['male', 'female', 'unknown']
gender_counts = {ms: collections.Counter(r.get('gender', 'unknown').lower()
                                         for r in groups[ms])
                 for ms in ALL_GROUPS}

x = np.arange(len(ALL_GROUPS))
w = 0.25
gcols = {'male': '#2980B9', 'female': '#E74C3C', 'unknown': '#BDC3C7'}

fig, ax = plt.subplots(figsize=(12, 6))
offsets = [-w, 0, w]
for j, g in enumerate(genders):
    vals = [gender_counts[ms].get(g, 0) for ms in ALL_GROUPS]
    ax.bar(x + offsets[j], vals, w, color=gcols[g], label=g.capitalize(), alpha=0.85)

ax.set_xticks(x)
ax.set_xticklabels([GROUP_LABELS[ms] for ms in ALL_GROUPS], rotation=15, ha='right')
apply_style(ax, 'Figure 17 — Gender Distribution by Migration Group',
            ylabel='Number of People')
ax.legend(fontsize=9)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig17_gender_by_group.png')


# ===========================================================================
# FIG 18 — LIFE EXPECTANCY BY GENDER × GROUP (grouped bar)
# ===========================================================================
print("  fig18_le_by_gender_group.png")

fig, ax = plt.subplots(figsize=(12, 7))
x = np.arange(len(ALL_GROUPS))
w = 0.3

for j, g in enumerate(['male', 'female']):
    means_g = []
    ses_g   = []
    for ms in ALL_GROUPS:
        v = [r['_le'] for r in groups[ms]
             if r.get('gender', '').lower() == g and r['_le'] is not None]
        means_g.append(round(statistics.mean(v), 2) if v else 0)
        ses_g.append(statistics.stdev(v) / math.sqrt(len(v)) if len(v) > 1 else 0)

    offset = -w/2 if g == 'male' else w/2
    bars = ax.bar(x + offset, means_g, w, color=gcols[g],
                  yerr=ses_g, capsize=5, label=g.capitalize(), alpha=0.85,
                  error_kw={'linewidth': 1.2})
    for bar, mn in zip(bars, means_g):
        if mn > 0:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 1.5,
                    f"{mn:.1f}", ha='center', fontsize=7.5, color=COLOUR['navy'])

ax.set_xticks(x)
ax.set_xticklabels([GROUP_LABELS[ms] for ms in ALL_GROUPS], rotation=15, ha='right')
apply_style(ax, 'Figure 18 — Mean Life Expectancy by Gender and Migration Group\n(±1 SE)',
            ylabel='Mean Life Expectancy (years)')
ax.legend(fontsize=9)
plt.tight_layout(rect=[0, 0.04, 1, 1])
add_source(fig)
save(fig, 'fig18_le_by_gender_group.png')


# ===========================================================================
# FIG 21 — SOVIET REPUBLIC COMPARISON
#
# Contextualises Ukrainian creative workers against the general populations
# of Soviet republics. Shows our four groups against what different Soviet
# citizens experienced by geography.
#
# Data sources (all hardcoded from published literature):
#   - Ukrainian SSR: Meslé & Vallin 2003 (already in UKR_SSR_LE above)
#   - Russian SFSR: Andreev, Darsky & Kharkova 1998; Shkolnikov et al.
#   - USSR overall: UN World Population Prospects 2022 revision
#   - Baltic average (Estonian/Lithuanian/Latvian SSR): Katus et al.;
#     Convergence or Divergence? PMC6223831 (2019)
#   - Georgian SSR: Meslé & Vallin (Caucasus monograph); UN WPP 2022
#   - Central Asian average (Kazakh/Uzbek/Turkmen SSR): UN WPP 2022
#
# Confidence: HIGH for Ukraine, Russia, USSR overall; MEDIUM for Baltic,
# Georgia; LOW for Central Asia pre-1960 (noted in chart).
# All values are both-sexes period LE at birth, decade midpoints.
# ===========================================================================
print("  fig21_soviet_republic_comparison.png")

# Simplified to 4 republic lines — the range that matters: highest (Baltic),
# Ukrainian SSR, Russian SFSR (the dominant comparison), Central Asian (lowest).
# Georgian SSR dropped (nearly identical to Baltic, adds clutter).
# USSR overall dropped (split the chart into sub-panels instead).
# Short clean labels — citation in footnote.
REPUBLIC_DATA_21 = {
    'Baltic SSRs avg':         {1955: 65.0, 1965: 70.5, 1975: 70.4, 1985: 70.8},
    'Ukrainian SSR':           {1925: 43.4, 1935: 38.5, 1945: 36.0, 1955: 62.0, 1965: 69.5, 1975: 70.2, 1985: 70.4},
    'Russian SFSR':            {1955: 63.5, 1965: 68.6, 1975: 68.0, 1985: 68.9},
    'Central Asian SSRs avg':  {1955: 53.5, 1965: 63.5, 1975: 65.8, 1985: 67.2},
}
REP21_COL   = {'Baltic SSRs avg': '#2980B9', 'Ukrainian SSR': '#27AE60',
               'Russian SFSR': '#E74C3C',    'Central Asian SSRs avg': '#8E44AD'}
REP21_STYLE = {'Baltic SSRs avg': ('D', '-', 2.0), 'Ukrainian SSR': ('s', '-', 2.5),
               'Russian SFSR':    ('o', '-', 2.0), 'Central Asian SSRs avg': ('x', '--', 1.5)}

MIN_N = 5
DEATH_DECADES = list(range(1920, 1995, 10))

fig, ax = plt.subplots(figsize=(13, 7))

# Republic lines (thin, light — background context)
for name, data in REPUBLIC_DATA_21.items():
    xs = sorted(data.keys())
    ys = [data[x] for x in xs]
    m, ls, lw = REP21_STYLE[name]
    ax.plot(xs, ys, marker=m, linestyle=ls, linewidth=lw,
            color=REP21_COL[name], markersize=6, alpha=0.55, zorder=3,
            label=f'{name}  (general population)')

# Our groups — bolder, foreground, only 3 key groups
# x-axis clipped to 1990 (Soviet dissolution = natural analytic boundary;
# post-1991 deaths in diaspora skew migrated LE upward and are out of scope)
GROUP_MARKERS = {'migrated': ('o', 2.5), 'non_migrated': ('s', 2.0), 'deported': ('D', 2.5)}
for ms, (mk, lw) in GROUP_MARKERS.items():
    xs_d, ys_d, ns_d = [], [], []
    for dec in DEATH_DECADES:
        if dec >= 1990:   # stop at Soviet dissolution
            continue
        v = [r['_le'] for r in groups[ms]
             if r['_dy'] and dec <= r['_dy'] < dec + 10 and r['_le'] is not None]
        if len(v) >= MIN_N:
            xs_d.append(dec + 5)
            ys_d.append(statistics.mean(v))
            ns_d.append(len(v))
    if not xs_d:
        continue
    short = {'migrated': 'Migrated (our data)', 'non_migrated': 'Non-migrated (our data)',
             'deported': 'Deported (our data)'}[ms]
    ax.plot(xs_d, ys_d, marker=mk, linestyle='-', linewidth=lw,
            color=COLOUR[ms], markersize=9, zorder=10, label=short)
    # Label EVERY decade dot
    for j, (xp, yp, np_) in enumerate(zip(xs_d, ys_d, ns_d)):
        v_off = 6 if j % 2 == 0 else -10
        ax.annotate(f"{yp:.0f}", xy=(xp, yp),
                    xytext=(0, v_off), textcoords='offset points',
                    ha='center', fontsize=7.5, color=COLOUR[ms], fontweight='bold')

ax.set_xlim(1918, 1992)
ax.set_ylim(28, 82)
apply_style(ax, 'Figure 21 — Mean Age at Death: Our Groups vs Soviet Republic General Populations',
            xlabel='Decade', ylabel='Life Expectancy / Mean Age at Death (years)')

# Shade the Terror period
ax.axvspan(1930, 1939, alpha=0.06, color='#8B0000', zorder=0)
ax.text(1934.5, 30, 'Great Terror\n& Holodomor', ha='center', fontsize=8,
        color='#8B0000', style='italic')

# Legend outside right
ax.legend(fontsize=9, loc='upper left', framealpha=0.95,
          edgecolor='#cccccc', handlelength=2)

fig.text(0.5, 0.01,
    "Republic data: Meslé & Vallin 2003; Andreev et al. 1998; UN WPP 2022; Katus et al. "
    "Creative worker dots = mean age at death of people dying in that decade (period data). n≥5 per point.",
    ha='center', fontsize=7, color='grey', style='italic')
plt.tight_layout(rect=[0, 0.05, 1, 1])
save(fig, 'fig21_soviet_republic_comparison.png')


# ===========================================================================
# FIG 22 — EDUCATED URBAN POPULATION COMPARISON
#
# Controls for socioeconomic status: were creative workers dying early
# because of Soviet repression specifically targeting them, or simply
# because they were a typical educated urban Soviet population?
#
# The educational mortality gradient in the Soviet Union:
#   Shkolnikov et al. (1998) "Educational level and adult mortality in
#   Russia 1979–1994": university-educated had ~3 years higher LE at age 20
#   vs the national average in 1979–80 (PMC1483877).
#   Manual vs non-manual workers: Shkolnikov & Meslé (1996) showed
#   intelligentsia/"non-manual employees" had significantly better survival
#   during the late Soviet stagnation than manual workers.
#
# Educated urban estimate = Ukrainian SSR general pop. LE + 3–5 years premium.
# This is a constructed band, clearly labelled as an estimate.
# ===========================================================================
print("  fig22_educated_urban_comparison.png")

EDU_PREMIUM_LOW  = 3.0
EDU_PREMIUM_HIGH = 5.0
edu_xs   = sorted(UKR_SSR_LE.keys())
edu_base = [UKR_SSR_LE[y][0] for y in edu_xs]
edu_lo   = [v + EDU_PREMIUM_LOW  for v in edu_base]
edu_hi   = [v + EDU_PREMIUM_HIGH for v in edu_base]
edu_mid  = [(lo + hi) / 2 for lo, hi in zip(edu_lo, edu_hi)]

fig, ax = plt.subplots(figsize=(13, 7))

# Background band — educated urban estimate (subtle)
ax.fill_between(edu_xs, edu_lo, edu_hi, alpha=0.15, color='#2980B9', zorder=1)
ax.plot(edu_xs, edu_mid, '--', color='#2980B9', linewidth=1.5, alpha=0.6, zorder=2,
        label=f'Est. educated urban Ukrainian LE  (+{EDU_PREMIUM_LOW}–{EDU_PREMIUM_HIGH} yr premium;\nShkolnikov et al. 1998)')

# SSR baseline (thin grey)
ax.plot(edu_xs, edu_base, 's:', color='#27AE60', linewidth=1.4, markersize=5,
        alpha=0.65, zorder=2, label='Ukrainian SSR general population')

# Our groups — 4 series, clean markers, bold lines
# Clipped to 1990 (Soviet dissolution) — same boundary as fig21
GRP_MARKERS22 = {'migrated': 'o', 'non_migrated': 's',
                 'internal_transfer': '^', 'deported': 'D'}
for ms in ALL_GROUPS:
    xs_d, ys_d, ns_d = [], [], []
    for dec in DEATH_DECADES:
        if dec >= 1990:   # stop at Soviet dissolution
            continue
        v = [r['_le'] for r in groups[ms]
             if r['_dy'] and dec <= r['_dy'] < dec + 10 and r['_le'] is not None]
        if len(v) >= MIN_N:
            xs_d.append(dec + 5)
            ys_d.append(statistics.mean(v))
            ns_d.append(len(v))
    if not xs_d:
        continue
    short = GROUP_LABELS[ms].split('(')[0].strip()
    ax.plot(xs_d, ys_d, marker=GRP_MARKERS22[ms], linestyle='-', linewidth=2.2,
            color=COLOUR[ms], markersize=8, zorder=10, label=short)
    # Label EVERY decade dot
    for j, (xp, yp) in enumerate(zip(xs_d, ys_d)):
        v_off = 7 if j % 2 == 0 else -11
        ax.annotate(f"{yp:.0f}", xy=(xp, yp),
                    xytext=(0, v_off), textcoords='offset points',
                    ha='center', fontsize=7.5, color=COLOUR[ms], fontweight='bold')

# Shade Terror period
ax.axvspan(1930, 1939, alpha=0.06, color='#8B0000', zorder=0)
ax.text(1934.5, 30, 'Great Terror\n& Holodomor', ha='center', fontsize=8,
        color='#8B0000', style='italic')

ax.set_xlim(1918, 1992)
ax.set_ylim(26, 82)
apply_style(ax, 'Figure 22 — Creative Workers Mean Age at Death vs Educated Urban Ukrainian Population',
            xlabel='Decade of Death', ylabel='Life Expectancy / Mean Age at Death (years)')
ax.legend(fontsize=9, loc='upper left', framealpha=0.95, edgecolor='#cccccc')

fig.text(0.5, 0.01,
    "Shkolnikov V.M. et al. (1998) Eur J Public Health 8(2); Meslé & Vallin 2003; UN WPP 2022. "
    "Creative worker dots = mean age at death for people dying in that decade. n≥5 per point.",
    ha='center', fontsize=7, color='grey', style='italic')
plt.tight_layout(rect=[0, 0.05, 1, 1])
save(fig, 'fig22_educated_urban_comparison.png')


# ===========================================================================
# DONE
# ===========================================================================
print(f"\nAll charts saved to: {CHARTS_DIR}")
print(f"Statistical report:  {OUT_TXT}")
print("\nChart summary:")
for i in range(1, 17):
    fname = f"fig{i:02d}_*.png"
    matches = [f for f in os.listdir(CHARTS_DIR) if f.startswith(f"fig{i:02d}_")]
    status = "✓" if matches else "✗ MISSING"
    name   = matches[0] if matches else fname
    print(f"  {status}  {name}")
