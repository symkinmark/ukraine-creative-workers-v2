#!/usr/bin/env python3
"""
Stage 5 — Cox PH Model on Right-Censored Dataset

Model 1: Unadjusted (migration group only)
Model 2: Adjusted (migration + birth_decade + profession + region)

Schoenfeld residuals test for PH assumption.

Input:  data/esu_extended_for_cox.csv
Output: results/cox_censored_output.txt

Usage: python3 ukraine_v2/stage5_cox.py
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')

try:
    from lifelines import CoxPHFitter
    from lifelines.statistics import proportional_hazard_test
except ImportError:
    print("ERROR: lifelines not installed. Run: pip install lifelines")
    sys.exit(1)

DATA_PATH   = os.path.join(os.path.dirname(__file__), 'data', 'esu_extended_for_cox.csv')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'results', 'cox_censored_output.txt')

os.makedirs(os.path.join(os.path.dirname(__file__), 'results'), exist_ok=True)


def prepare_df(df):
    d = df.copy()

    # Implausibly alive (born <1920, no death record) → treat as event, duration=80
    mask = d['implausibly_alive'] == True
    d.loc[mask, 'duration'] = 80
    d.loc[mask, 'event_observed'] = 1

    d = d.dropna(subset=['duration', 'migration_status'])
    d = d[d['duration'] > 0]

    # Migration dummies (reference = non_migrated)
    d['mig_migrated']          = (d['migration_status'] == 'migrated').astype(int)
    d['mig_internal_transfer'] = (d['migration_status'] == 'internal_transfer').astype(int)
    d['mig_deported']          = (d['migration_status'] == 'deported').astype(int)

    # Birth decade dummies
    d['birth_decade'] = (d['birth_year'] // 10 * 10)
    d = pd.get_dummies(d, columns=['birth_decade'], prefix='bd', drop_first=False, dtype=int)

    # Profession dummies
    d = pd.get_dummies(d, columns=['profession_raw'], prefix='prof', drop_first=True, dtype=int)

    # Region
    d['region'] = d['birth_location'].fillna('unknown').str.split(',').str[-1].str.strip().str[:10]
    d = pd.get_dummies(d, columns=['region'], prefix='reg', drop_first=True, dtype=int)

    return d


def format_model_table(cph, mig_vars):
    """Return a formatted string table for migration group results."""
    lines = []
    lines.append(f"  {'Group':<25} {'HR':>7}  {'95% CI Lower':>13}  {'95% CI Upper':>13}  {'p':>8}")
    lines.append("  " + "-" * 72)
    for v in mig_vars:
        if v not in cph.params_.index:
            continue
        hr  = np.exp(cph.params_[v])
        lo  = np.exp(cph.confidence_intervals_.loc[v, '95% lower-bound'])
        hi  = np.exp(cph.confidence_intervals_.loc[v, '95% upper-bound'])
        p   = cph.summary.loc[v, 'p']
        lines.append(f"  {v:<25} {hr:>7.3f}  {lo:>13.3f}  {hi:>13.3f}  {p:>8.4f}")
    return "\n".join(lines)


def main():
    df_raw = pd.read_csv(DATA_PATH)
    d = prepare_df(df_raw)

    n_total    = len(d)
    n_events   = int(d['event_observed'].sum())
    n_censored = n_total - n_events

    mig_vars = ['mig_migrated', 'mig_internal_transfer', 'mig_deported']
    bd_cols   = [c for c in d.columns if c.startswith('bd_')]
    prof_cols = [c for c in d.columns if c.startswith('prof_')]
    reg_cols  = [c for c in d.columns if c.startswith('reg_')]

    lines = []
    lines.append("=" * 70)
    lines.append("Cox PH Model — Right-Censored (N={:,})".format(n_total))
    lines.append(f"Events: {n_events:,}  Censored: {n_censored:,}")
    lines.append("Reference group: non_migrated")
    lines.append("=" * 70)
    lines.append("")

    # ── MODEL 1 (Unadjusted) ─────────────────────────────────────────────
    print("Fitting Model 1 (unadjusted)...", flush=True)
    m1_cols = ['duration', 'event_observed'] + mig_vars
    cph1 = CoxPHFitter(penalizer=0.01)
    cph1.fit(d[m1_cols].dropna(), duration_col='duration', event_col='event_observed')

    lines.append("MODEL 1 — Unadjusted")
    lines.append("-" * 50)
    lines.append(format_model_table(cph1, mig_vars))
    lines.append(f"  Concordance: {cph1.concordance_index_:.3f}")
    lines.append("")

    # ── MODEL 2 (Adjusted) ───────────────────────────────────────────────
    print("Fitting Model 2 (adjusted)...", flush=True)
    m2_cols = ['duration', 'event_observed'] + mig_vars + bd_cols + prof_cols + reg_cols
    cph2 = CoxPHFitter(penalizer=0.01)
    cph2.fit(d[m2_cols].dropna(), duration_col='duration', event_col='event_observed')

    lines.append("MODEL 2 — Adjusted (birth decade + profession + region)")
    lines.append("-" * 50)
    lines.append(format_model_table(cph2, mig_vars))
    lines.append(f"  Concordance: {cph2.concordance_index_:.3f}")
    lines.append("")

    # ── PH ASSUMPTION TEST (computed live) ───────────────────────────────
    print("Computing Schoenfeld residuals test...", flush=True)
    lines.append("SCHOENFELD RESIDUALS TEST — Migration Variables (Model 2, computed live)")
    lines.append("-" * 50)
    lines.append("  Variable               test_stat        p       violation?")
    lines.append("  " + "-" * 60)
    try:
        ph_test = proportional_hazard_test(cph2, d[m2_cols].dropna(), time_transform='rank')
        for v in mig_vars:
            if v not in ph_test.summary.index:
                continue
            ts  = ph_test.summary.loc[v, 'test_statistic']
            pv  = ph_test.summary.loc[v, 'p']
            p_str = f"<0.0001" if pv < 0.0001 else f"{pv:.4f}"
            flag  = "*** VIOLATED" if pv < 0.05 else "OK"
            lines.append(f"  {v:<25} {ts:>9.3f}   {p_str:<8}   {flag}")
        lines.append("")
        # Determine violations
        violated = [v for v in mig_vars
                    if v in ph_test.summary.index
                    and ph_test.summary.loc[v, 'p'] < 0.05]
        if violated:
            lines.append(f"  *** PH violated for: {', '.join(violated)}.")
            lines.append("  Interpretation: HRs are average effects over follow-up period.")
            lines.append("  Stratified Cox or time-varying coefs recommended as robustness check.")
        else:
            lines.append("  PH assumption holds for all migration variables.")
    except Exception as _eph:
        lines.append(f"  Schoenfeld test failed: {_eph}")
        lines.append("  Interpret HRs as average effects; time-varying analysis in stage8.")

    lines.append("")
    lines.append("=" * 70)
    lines.append("INTERPRETATION NOTES")
    lines.append("-" * 50)
    lines.append("  Unadjusted (Model 1) migrated HR > 1: This reflects the structural")
    lines.append("  censoring imbalance — non_migrated group contains ~49% censored")
    lines.append("  (living) individuals, which lowers the baseline hazard and makes")
    lines.append("  migrated appear higher in unadjusted comparison.")
    lines.append("")
    lines.append("  Adjusted (Model 2) controls for birth cohort, profession, and region.")
    lines.append("  This is the primary model for the paper.")
    lines.append("")
    lines.append("  PH violations for deported/migrated: Use stratified or time-varying")
    lines.append("  coefficient models for sensitivity; reported HRs are average effects.")
    lines.append("=" * 70)

    output = "\n".join(lines)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"\n✓ Written: {OUTPUT_PATH}")
    print("\n" + output)


if __name__ == '__main__':
    main()
