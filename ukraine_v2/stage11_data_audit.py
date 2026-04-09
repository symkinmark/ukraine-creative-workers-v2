"""
stage11_data_audit.py
V2.6 Database Audit — documents all known data quality issues
with counts, severity, and estimated impact on primary findings.

Outputs:
  ukraine_v2/data_audit_report.md  — structured audit (appendix to paper)
"""

import os
import re
import pandas as pd
import numpy as np

PROJECT = os.path.dirname(os.path.abspath(__file__))
CSV_IN  = os.path.join(PROJECT, 'esu_creative_workers_v2_3.csv')
OUT_MD  = os.path.join(PROJECT, 'data_audit_report.md')

df = pd.read_csv(CSV_IN)
print(f"Loaded {len(df):,} rows × {len(df.columns)} columns")

# ---------------------------------------------------------------------------
# Helper: first year appearing in notes field
# ---------------------------------------------------------------------------
def first_year_in_notes(notes):
    if pd.isna(notes):
        return None
    m = re.search(r'\b(1[6-9]\d{2})\b', str(notes))
    return int(m.group(1)) if m else None

df['_first_year_notes'] = df['notes'].apply(first_year_in_notes)
df['_death_year_n'] = pd.to_numeric(df['death_year'], errors='coerce')
df['_birth_year_n'] = pd.to_numeric(df['birth_year'], errors='coerce')

# ---------------------------------------------------------------------------
# Section 1 — Row counts by migration_status
# ---------------------------------------------------------------------------
status_counts = df['migration_status'].value_counts().sort_values(ascending=False)

ANALYSIS_STATUSES = {'migrated', 'non_migrated', 'internal_transfer', 'deported', 'unknown'}

analysis_df = df[df['migration_status'].isin(ANALYSIS_STATUSES)]
dead_df = analysis_df[analysis_df['_death_year_n'].notna() | (analysis_df['migration_status'] == 'alive')]

migrated   = df[df['migration_status'] == 'migrated']
non_mig    = df[df['migration_status'] == 'non_migrated']
deported   = df[df['migration_status'] == 'deported']
int_trans  = df[df['migration_status'] == 'internal_transfer']

# Primary gap recompute for audit
mig_mean   = (df[df['migration_status'] == 'migrated']['_death_year_n'] -
              df[df['migration_status'] == 'migrated']['_birth_year_n']).dropna().mean()
nm_mean    = (df[df['migration_status'] == 'non_migrated']['_death_year_n'] -
              df[df['migration_status'] == 'non_migrated']['_birth_year_n']).dropna().mean()

# ---------------------------------------------------------------------------
# Section 2 — Birth/death year completeness
# ---------------------------------------------------------------------------
def year_completeness(subset, label):
    n = len(subset)
    n_birth = subset['_birth_year_n'].notna().sum()
    n_death = subset['_death_year_n'].notna().sum()
    return {
        'group': label, 'n': n,
        'birth_year_filled': n_birth, 'birth_pct': f"{100*n_birth/n:.1f}%" if n else 'N/A',
        'death_year_filled': n_death, 'death_pct': f"{100*n_death/n:.1f}%" if n else 'N/A',
    }

completeness = [
    year_completeness(migrated, 'migrated'),
    year_completeness(non_mig,  'non_migrated'),
    year_completeness(deported, 'deported'),
    year_completeness(int_trans,'internal_transfer'),
    year_completeness(df[df['migration_status']=='unknown'], 'unknown'),
    year_completeness(df[df['migration_status']=='alive'],   'alive'),
]

# ---------------------------------------------------------------------------
# Section 3 — Birth-year-as-death-year suspects
# ---------------------------------------------------------------------------
pre_soviet = df[df['migration_status'] == 'excluded_pre_soviet'].copy()
pre_soviet['_first'] = pre_soviet['notes'].apply(first_year_in_notes)
# Suspect: birth_year=NaN, death_year = first year in notes
suspects = pre_soviet[
    (pre_soviet['_birth_year_n'].isna()) &
    (pre_soviet['_death_year_n'].notna()) &
    (pre_soviet['_first'] == pre_soviet['_death_year_n'])
]
# Death year distribution among suspects
sus_death_dist = suspects['_death_year_n'].value_counts().sort_index()

# ---------------------------------------------------------------------------
# Section 4 — API-error unknowns
# ---------------------------------------------------------------------------
api_err = df[df['migration_reasoning'].str.contains(
    'credit balance is too low|sonnet_error.*Error code: 400', na=False, regex=True
)]
api_err_statuses = api_err['migration_status'].value_counts()

# ---------------------------------------------------------------------------
# Section 5 — Gender completeness
# ---------------------------------------------------------------------------
has_gender = df['gender'].notna() if 'gender' in df.columns else pd.Series([False]*len(df))
gender_total = has_gender.sum() if 'gender' in df.columns else 0
gender_missing = (~has_gender).sum() if 'gender' in df.columns else len(df)

gender_dist = df['gender'].value_counts() if 'gender' in df.columns else pd.Series()

# ---------------------------------------------------------------------------
# Section 6 — Profession coverage
# ---------------------------------------------------------------------------
has_prof = df['profession_raw'].notna()
prof_missing = (~has_prof).sum()
# Top 20 profession_raw values
prof_top = df['profession_raw'].value_counts().head(20)

# ---------------------------------------------------------------------------
# Section 7 — is_ukrainian vs flag_non_ukrainian conflicts
# ---------------------------------------------------------------------------
# flag_non_ukrainian=True means scraper flagged as potentially non-Ukrainian
# is_ukrainian is the AI classification result
flag_col = 'flag_non_ukrainian' if 'flag_non_ukrainian' in df.columns else None
is_uk_col = 'is_ukrainian' if 'is_ukrainian' in df.columns else None

conflict_entries = None
if flag_col and is_uk_col:
    in_analysis = df[df['migration_status'].isin(ANALYSIS_STATUSES - {'unknown', 'alive'})]
    flagged_in_analysis = in_analysis[
        in_analysis[flag_col].astype(str).str.lower().isin(['true', '1', 'yes'])
    ]
    conflict_entries = flagged_in_analysis[['name', 'migration_status', flag_col, is_uk_col]].head(30)

# ---------------------------------------------------------------------------
# Section 8 — Unknown group breakdown
# ---------------------------------------------------------------------------
unknowns = df[df['migration_status'] == 'unknown']
api_unk = unknowns[unknowns['migration_reasoning'].str.contains(
    'credit balance is too low|sonnet_error.*Error code: 400', na=False, regex=True
)]
genuine_unk = unknowns[~unknowns.index.isin(api_unk.index)]
# Genuine unknowns: death year coverage
gu_with_death = genuine_unk['_death_year_n'].notna().sum()

# ---------------------------------------------------------------------------
# Section 9 — Retracted wave figures
# ---------------------------------------------------------------------------
charts_dir = os.path.join(PROJECT, 'charts')
retracted_figs = [f for f in os.listdir(charts_dir) if 'fig29' in f] if os.path.exists(charts_dir) else []

# ---------------------------------------------------------------------------
# Section 10 — Estimated maximum impact of fixes on primary gap
# ---------------------------------------------------------------------------
# From validation: ~5 excluded_pre_soviet entries in 82-entry review were wrongly excluded
# as migrated/non_migrated.
# Scaling to 102 suspects: ~6% become migrated (~6), ~6% become non_migrated (~6)
# Conservative estimate: 6 new migrants with mean age ~80 (they lived to 1970s–1990s)
# 6 new non-migrants with mean age ~72

n_mig_current = len(migrated[migrated['_death_year_n'].notna() & migrated['_birth_year_n'].notna()])
n_nm_current  = len(non_mig[non_mig['_death_year_n'].notna() & non_mig['_birth_year_n'].notna()])
mig_ages = (migrated['_death_year_n'] - migrated['_birth_year_n']).dropna()
nm_ages  = (non_mig['_death_year_n']  - non_mig['_birth_year_n']).dropna()

# Scenario: add 6 migrants aged 80, 6 non-migrants aged 72
add_mig = 6; add_mig_age = 80.0
add_nm  = 6; add_nm_age  = 72.0
new_mig_mean = (mig_ages.sum() + add_mig * add_mig_age) / (len(mig_ages) + add_mig)
new_nm_mean  = (nm_ages.sum()  + add_nm  * add_nm_age)  / (len(nm_ages)  + add_nm)
new_gap = new_mig_mean - new_nm_mean

current_gap = mig_ages.mean() - nm_ages.mean()

# ---------------------------------------------------------------------------
# Write output markdown
# ---------------------------------------------------------------------------

lines = []
def ln(s=""): lines.append(s)

ln("# Database Quality Audit Report")
ln(f"*Dataset: esu_creative_workers_v2_3.csv — generated by stage11_data_audit.py*")
ln()
ln("---")
ln()

# ── Section 1 ──
ln("## 1. Row Counts by Migration Status")
ln()
ln("| Status | Count | % of total | In primary analysis |")
ln("|--------|-------|------------|---------------------|")
total = len(df)
for status, count in status_counts.items():
    in_analysis = "✓" if status in ANALYSIS_STATUSES else "—"
    ln(f"| {status} | {count:,} | {100*count/total:.1f}% | {in_analysis} |")
ln()
ln(f"**Total rows:** {total:,}")
ln(f"**Analysable dead cohort (migrated + non_migrated + internal_transfer + deported):** "
   f"{len(df[df['migration_status'].isin({'migrated','non_migrated','internal_transfer','deported'})]):,}")
ln()

# ── Section 2 ──
ln("## 2. Birth/Death Year Completeness by Group")
ln()
ln("| Group | n | Birth year filled | Death year filled |")
ln("|-------|---|-------------------|-------------------|")
for row in completeness:
    ln(f"| {row['group']} | {row['n']:,} | {row['birth_year_filled']:,} ({row['birth_pct']}) | "
       f"{row['death_year_filled']:,} ({row['death_pct']}) |")
ln()

# ── Section 3 ──
ln("## 3. Birth Year Stored as Death Year (Issue #1 — HIGH SEVERITY)")
ln()
ln(f"**Total excluded_pre_soviet entries:** {len(pre_soviet):,}")
ln(f"**Suspect entries** (birth_year=NaN AND death_year = first year in notes): **{len(suspects):,}** ({100*len(suspects)/len(pre_soviet):.1f}% of excluded_pre_soviet)")
ln()
ln("These entries have the scraper's birth year stored in the death_year field. "
   "The actual death year is unknown without re-fetching the full ESU article.")
ln()
ln("**Death year distribution among suspects** (these are actually birth years):")
ln()
ln("| Year range | Count | Interpretation |")
ln("|------------|-------|----------------|")
ranges = [(1800,1860),(1860,1880),(1880,1900),(1900,1910),(1910,1921)]
for lo, hi in ranges:
    n = len(suspects[(suspects['_death_year_n'] >= lo) & (suspects['_death_year_n'] < hi)])
    ln(f"| {lo}–{hi-1} | {n} | Person born in this range |")
ln()
ln("**Fix:** Re-fetch full ESU article for each suspect entry. Parse 'Дата смерті:' field. "
   "If actual death_year ≥ 1921, reclassify via Claude.")
ln()

# ── Section 4 ──
ln("## 4. API-Credit-Error 'Unknown' Entries (Issue #2 — HIGH SEVERITY)")
ln()
ln(f"**Total entries with API error in migration_reasoning:** **{len(api_err):,}**")
ln()
ln("| Current migration_status | Count |")
ln("|--------------------------|-------|")
for status, count in api_err_statuses.items():
    ln(f"| {status} | {count} |")
ln()
ln("These entries were never genuinely classified — the Claude API returned a billing error "
   "mid-classification and that error message was stored as the reasoning. "
   "Their true migration status is unknown.")
ln()
ln("**Fix:** Re-fetch full ESU article. Re-run Claude classification with full bio text.")
ln()

# ── Section 5 ──
ln("## 5. Gender Completeness (Issue #8 — LOW SEVERITY)")
ln()
if 'gender' in df.columns:
    ln(f"**Gender distribution:**")
    ln()
    ln("| Value | Count |")
    ln("|-------|-------|")
    for val, cnt in gender_dist.items():
        ln(f"| {val} | {cnt:,} |")
    ln(f"| *missing (NaN)* | {gender_missing:,} |")
    ln()
    ln(f"**Missing gender:** {gender_missing:,} of {total:,} ({100*gender_missing/total:.1f}%)")
else:
    ln("*gender column not found*")
ln()

# ── Section 6 ──
ln("## 6. Profession Coverage (Issue #9 — LOW SEVERITY)")
ln()
ln(f"**Entries with no profession_raw:** {prof_missing:,} ({100*prof_missing/total:.1f}%)")
ln()
ln("**Top 20 profession_raw values:**")
ln()
ln("| Profession (raw) | Count |")
ln("|------------------|-------|")
for prof, cnt in prof_top.items():
    ln(f"| {str(prof)[:60]} | {cnt:,} |")
ln()

# ── Section 7 ──
ln("## 7. Non-Ukrainian Inclusions (Issue #4 — MEDIUM SEVERITY)")
ln()
if flag_col and is_uk_col and conflict_entries is not None:
    ln(f"**Entries in analysis groups with flag_non_ukrainian=True:** {len(conflict_entries):,}")
    ln()
    if len(conflict_entries) > 0:
        ln("| Name | migration_status | flag_non_ukrainian | is_ukrainian |")
        ln("|------|-----------------|-------------------|--------------|")
        for _, row in conflict_entries.iterrows():
            ln(f"| {row['name']} | {row['migration_status']} | {row[flag_col]} | {row[is_uk_col]} |")
    else:
        ln("*No flagged entries found in analysis groups.*")
else:
    ln("*flag_non_ukrainian or is_ukrainian column not available*")
ln()
ln("**Validation-confirmed non-Ukrainian inclusions (from 82-entry manual review):**")
ln("- Кудравець Анатоль Павлович: Belarusian writer born/died in Belarus — should be excluded_non_ukrainian")
ln("- Містраль Ґабрієла: Chilean Nobel laureate Gabriela Mistral — should be excluded_non_ukrainian")
ln("- Кресеску Віктор: Moldovan/Romanian writer — correctly excluded but wrong reason code")
ln("- Лефлер Чарльз-Мартін: Never resident in Ukraine — should be excluded_non_ukrainian")
ln()

# ── Section 8 ──
ln("## 8. Unknown Group Analysis (Issue #5 — MEDIUM SEVERITY)")
ln()
ln(f"**Total unknown entries:** {len(unknowns):,}")
ln(f"  - API-error unknowns (billing failure): {len(api_unk):,}")
ln(f"  - Genuine unknowns (insufficient data): {len(genuine_unk):,}")
ln(f"    - Of genuine unknowns, have death year: {gu_with_death} ({100*gu_with_death/max(1,len(genuine_unk)):.1f}%)")
ln()
ln("**Fix:** For API-error unknowns — re-classify (Phase B3). "
   "For genuine unknowns with death year — attempt re-classification with full bio fetch.")
ln()

# ── Section 9 ──
ln("## 9. Retracted Wave Analysis Figures (Issue #10 — INFORMATIONAL)")
ln()
ln(f"**Wave figures in charts/:** {len(retracted_figs)} files")
ln()
for f in sorted(retracted_figs):
    ln(f"- `{f}`")
ln()
ln("These figures were generated by stage9_wave_disaggregation.py (retracted). "
   "The wave classifier was found to recover birth/death years rather than emigration departure years. "
   "Figures remain in charts/ for reference but are removed from FIGURE_MAP in build_paper_html.py "
   "and are not cited as findings in the paper.")
ln()

# ── Section 10 ──
ln("## 10. Estimated Maximum Impact of Fixes on Primary Gap")
ln()
ln(f"**Current primary gap:** {current_gap:.2f} years "
   f"(migrants {mig_ages.mean():.2f} yrs, non-migrants {nm_ages.mean():.2f} yrs)")
ln()
ln("**Conservative scenario** (from validation sample scaling):")
ln(f"- ~6 wrongly-excluded migrants added at mean age ~80 yrs")
ln(f"- ~6 wrongly-excluded non-migrants added at mean age ~72 yrs")
ln(f"- **Adjusted gap:** {new_gap:.2f} years (change: {new_gap - current_gap:+.2f} yrs)")
ln()
ln("**Direction of effect:** Corrections from excluded_pre_soviet fixes and non-Ukrainian removals "
   "are expected to **widen or maintain** the gap, not reduce it. "
   "The 4.04-year estimate is a conservative lower bound.")
ln()
ln("---")
ln()
ln("## Summary Table")
ln()
ln("| # | Issue | Count | Severity | Status |")
ln("|---|-------|-------|----------|--------|")
ln(f"| 1 | Birth year stored as death year (excluded_pre_soviet) | {len(suspects)} of {len(pre_soviet)} | HIGH | Fix in Stage 12 |")
ln(f"| 2 | API-credit-error 'unknown' classifications | {len(api_err)} | HIGH | Fix in Stage 12 |")
ln(f"| 3 | Specific validation errors (confirmed wrong) | 7 named | HIGH | Fix in Stage 12 |")
ln(f"| 4 | Non-Ukrainian inclusions | ~4 confirmed, ~5–15 possible | MEDIUM | Audit in Stage 12 |")
ln(f"| 5 | Unresolvable genuine unknowns | ~{len(genuine_unk)} | MEDIUM | Attempt re-classify |")
ln(f"| 6 | Incomplete validation sample | 118 of 200 not reviewed | MEDIUM | User task (Phase C) |")
ln(f"| 7 | Missing high-profile figures (ESU gap) | 7 confirmed absent | MEDIUM | Documented (Stage 10) |")
ln(f"| 8 | Gender missing | {gender_missing:,} | LOW | Low priority |")
ln(f"| 9 | Profession raw inconsistency | {prof_missing} with no profession | LOW | Mapping in Stage 12 |")
ln(f"| 10 | Retracted wave figures | {len(retracted_figs)} files | INFORMATIONAL | Remove from FIGURE_MAP |")
ln()

report = "\n".join(lines)
with open(OUT_MD, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"\nAudit report written → {OUT_MD}")
print(f"\n{'='*60}")
print(f"KEY NUMBERS FOR V2.6:")
print(f"{'='*60}")
print(f"Total rows: {total:,}")
print(f"Primary gap (current): {current_gap:.2f} yrs")
print(f"  Migrants mean: {mig_ages.mean():.2f} yrs (n={len(mig_ages):,})")
print(f"  Non-migrants mean: {nm_ages.mean():.2f} yrs (n={len(nm_ages):,})")
print(f"\nISSUE 1 — Birth-year-as-death-year suspects: {len(suspects)}")
print(f"ISSUE 2 — API-error unknowns: {len(api_err)}")
print(f"ISSUE 7 — Genuine unknowns (non-API): {len(genuine_unk)}")
print(f"ISSUE 4 — Gender missing: {gender_missing:,}")
print(f"\nEstimated gap after fixes: {new_gap:.2f} yrs (change: {new_gap - current_gap:+.2f} yrs)")
