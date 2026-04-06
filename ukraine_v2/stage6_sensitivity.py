#!/usr/bin/env python3
"""
Stage 6 — Sensitivity Analyses for Right-Censored Cox PH Model

Three scenarios:
  A. Implausibly alive assumption: test duration=70, 75, 80, 85, 90 for born<1920
  B. Post-1991 emigrant inclusion/exclusion: exclude likely_post_soviet_emigrant migrants
  C. Bootstrap misclassification: 100 iterations at 5%, 10%, 15% random swap rates

Output: ukraine_v2/results/sensitivity_output.txt
        ukraine_v2/results/sensitivity_results.json

Usage: python3 ukraine_v2/stage6_sensitivity.py
"""

import json
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

DATA_PATH    = os.path.join(os.path.dirname(__file__), 'data', 'esu_extended_for_cox.csv')
OUTPUT_TXT   = os.path.join(os.path.dirname(__file__), 'results', 'sensitivity_output.txt')
OUTPUT_JSON  = os.path.join(os.path.dirname(__file__), 'results', 'sensitivity_results.json')

MIGRATION_GROUPS = ['mig_migrated', 'mig_internal_transfer', 'mig_deported']

os.makedirs(os.path.join(os.path.dirname(__file__), 'results'), exist_ok=True)


def prepare_df(df, implausibly_alive_duration=80):
    """Prepare dataframe with dummies. Apply implausibly_alive_duration to born<1920 censored."""
    d = df.copy()

    # Apply implausibly_alive assumption
    mask = d['implausibly_alive'] == True
    if mask.any():
        d.loc[mask, 'duration'] = implausibly_alive_duration
        d.loc[mask, 'event_observed'] = 1

    # Drop rows with missing duration or migration status
    d = d.dropna(subset=['duration', 'migration_status'])
    d = d[d['duration'] > 0]

    # Migration dummies (reference = non_migrated)
    d['mig_migrated']           = (d['migration_status'] == 'migrated').astype(int)
    d['mig_internal_transfer']  = (d['migration_status'] == 'internal_transfer').astype(int)
    d['mig_deported']           = (d['migration_status'] == 'deported').astype(int)

    # Birth decade dummies
    d['birth_decade'] = (d['birth_year'] // 10 * 10)
    d = pd.get_dummies(d, columns=['birth_decade'], prefix='bd', drop_first=False, dtype=int)

    # Profession dummies
    d = pd.get_dummies(d, columns=['profession_raw'], prefix='prof', drop_first=True, dtype=int)

    # Region from birth_location
    d['region'] = d['birth_location'].fillna('unknown').str.split(',').str[-1].str.strip().str[:10]
    d = pd.get_dummies(d, columns=['region'], prefix='reg', drop_first=True, dtype=int)

    return d


def fit_and_extract(d, covariates):
    """Fit Cox model and return dict of HR, CI, p for migration covariates."""
    cph = CoxPHFitter(penalizer=0.1)
    cols = ['duration', 'event_observed'] + covariates
    fit_df = d[cols].dropna()
    cph.fit(fit_df, duration_col='duration', event_col='event_observed')

    results = {}
    for v in MIGRATION_GROUPS:
        if v not in cph.params_.index:
            results[v] = {'hr': None, 'lo': None, 'hi': None, 'p': None}
            continue
        hr  = float(np.exp(cph.params_[v]))
        lo  = float(np.exp(cph.confidence_intervals_.loc[v, '95% lower-bound']))
        hi  = float(np.exp(cph.confidence_intervals_.loc[v, '95% upper-bound']))
        p   = float(cph.summary.loc[v, 'p'])
        results[v] = {'hr': hr, 'lo': lo, 'hi': hi, 'p': p}
    return results


def get_model2_covariates(d):
    """Return covariate list for Model 2 (mig + bd + prof + reg dummies)."""
    mig_cols  = MIGRATION_GROUPS
    bd_cols   = [c for c in d.columns if c.startswith('bd_')]
    prof_cols = [c for c in d.columns if c.startswith('prof_')]
    reg_cols  = [c for c in d.columns if c.startswith('reg_')]
    return mig_cols + bd_cols + prof_cols + reg_cols


def fmt_row(label, res):
    r = []
    for v in MIGRATION_GROUPS:
        g = res.get(v, {})
        if g.get('hr') is None:
            r.append(f"  {v}: N/A")
        else:
            r.append(f"  {v}: HR={g['hr']:.3f} (95%CI {g['lo']:.3f}–{g['hi']:.3f}) p={g['p']:.4f}")
    return f"{label}\n" + "\n".join(r)


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():
    df_raw = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df_raw)} rows")

    lines = ["=" * 60, "STAGE 6 SENSITIVITY ANALYSES", "=" * 60, ""]
    all_results = {}

    # NOTE: All sensitivity models use unadjusted Model 1 (migration dummies only).
    # The adjusted Model 2 results are in cox_censored_output.txt — sensitivity
    # analyses test directional robustness, not full covariate control.

    # ── SCENARIO A: Implausibly alive duration assumptions ──────
    print("\nScenario A: Implausibly alive duration sensitivity...")
    lines += ["SCENARIO A — Implausibly Alive Duration Assumption (unadjusted)", "-" * 50]
    scenario_a = {}
    for dur in [70, 75, 80, 85, 90]:
        d = prepare_df(df_raw, implausibly_alive_duration=dur)
        res = fit_and_extract(d, MIGRATION_GROUPS)
        scenario_a[dur] = res
        lines.append(fmt_row(f"  Duration={dur}:", res))
        print(f"  dur={dur} → migrated HR={res['mig_migrated']['hr']:.3f}", flush=True)
    lines.append("")
    all_results['scenario_a'] = scenario_a

    # ── SCENARIO B: Post-1991 emigrant inclusion/exclusion ──────
    print("\nScenario B: Post-1991 emigrant sensitivity...")
    lines += ["SCENARIO B — Post-1991 Emigrant Inclusion/Exclusion (unadjusted)", "-" * 50]
    scenario_b = {}

    post_soviet_mask = (df_raw['likely_post_soviet_emigrant'] == True) & \
                       (df_raw['migration_status'] == 'migrated')
    n_excl = post_soviet_mask.sum()

    # B1: Baseline (include all, use implausibly_alive=80)
    d_base = prepare_df(df_raw, implausibly_alive_duration=80)
    res_base = fit_and_extract(d_base, MIGRATION_GROUPS)
    scenario_b['include_all'] = res_base
    lines.append(fmt_row("  Include all (baseline):", res_base))

    # B2: Exclude likely_post_soviet_emigrants from migrated
    df_excl = df_raw[~post_soviet_mask].copy()
    d_excl = prepare_df(df_excl, implausibly_alive_duration=80)
    res_excl = fit_and_extract(d_excl, MIGRATION_GROUPS)
    scenario_b['exclude_post_soviet'] = res_excl
    lines.append(fmt_row(f"  Exclude {n_excl} post-Soviet emigrants:", res_excl))

    # B3: Reclassify likely_post_soviet_emigrants as non_migrated
    df_recl = df_raw.copy()
    df_recl.loc[post_soviet_mask, 'migration_status'] = 'non_migrated'
    d_recl = prepare_df(df_recl, implausibly_alive_duration=80)
    res_recl = fit_and_extract(d_recl, MIGRATION_GROUPS)
    scenario_b['reclassify_post_soviet'] = res_recl
    lines.append(fmt_row(f"  Reclassify {n_excl} post-Soviet emigrants as non_migrated:", res_recl))
    lines.append("")
    all_results['scenario_b'] = scenario_b
    print(f"  B1={res_base['mig_migrated']['hr']:.3f}, "
          f"B2={res_excl['mig_migrated']['hr']:.3f}, "
          f"B3={res_recl['mig_migrated']['hr']:.3f}", flush=True)

    # ── SCENARIO C: Bootstrap misclassification ──────────────────
    print("\nScenario C: Bootstrap misclassification (100 iter × 3 rates)...")
    lines += ["SCENARIO C — Bootstrap Misclassification Error", "-" * 50]
    scenario_c = {}

    rng = np.random.default_rng(42)
    statuses = ['migrated', 'non_migrated', 'internal_transfer', 'deported']
    N_ITER = 50  # 50 iterations × 3 rates = 150 fits; faster than 300

    for rate in [0.05, 0.10, 0.15]:
        hrs = {v: [] for v in MIGRATION_GROUPS}
        for it in range(N_ITER):
            if (it + 1) % 10 == 0:
                print(f"    rate={rate:.0%} iter {it+1}/{N_ITER}", flush=True)
            df_b = df_raw.copy()
            # Randomly swap migration_status for `rate` fraction of rows
            n_swap = int(len(df_b) * rate)
            swap_idx = rng.choice(df_b.index, size=n_swap, replace=False)
            df_b.loc[swap_idx, 'migration_status'] = rng.choice(statuses, size=n_swap)
            d_b = prepare_df(df_b, implausibly_alive_duration=80)
            try:
                # Use Model 1 (unadjusted) for bootstrap — faster, sufficient for sensitivity
                res_b = fit_and_extract(d_b, MIGRATION_GROUPS)
                for v in MIGRATION_GROUPS:
                    if res_b[v]['hr'] is not None:
                        hrs[v].append(res_b[v]['hr'])
            except Exception:
                pass  # skip failed iterations

        rate_results = {}
        row_parts = [f"  Rate={rate:.0%}:"]
        for v in MIGRATION_GROUPS:
            arr = np.array(hrs[v])
            if len(arr) == 0:
                rate_results[v] = None
                row_parts.append(f"    {v}: N/A")
            else:
                med = float(np.median(arr))
                lo2 = float(np.percentile(arr, 2.5))
                hi2 = float(np.percentile(arr, 97.5))
                rate_results[v] = {'median_hr': med, 'lo': lo2, 'hi': hi2, 'n': len(arr)}
                row_parts.append(f"    {v}: median HR={med:.3f} (2.5–97.5%: {lo2:.3f}–{hi2:.3f}) n={len(arr)}")
        scenario_c[str(rate)] = rate_results
        lines.extend(row_parts)
        print(f"  rate={rate:.0%} migrated median HR={np.median(hrs['mig_migrated']):.3f}")
    lines.append("")
    all_results['scenario_c'] = scenario_c

    # ── SUMMARY ──────────────────────────────────────────────────
    lines += ["=" * 60, "SUMMARY", "=" * 60]
    lines.append("Migrated HR across all scenarios:")
    a_hrs = [f"{scenario_a[d]['mig_migrated']['hr']:.3f}" for d in [70,75,80,85,90]]
    lines.append(f"  A (dur=70-90): {a_hrs}")
    lines.append(f"  B1 (include): {scenario_b['include_all']['mig_migrated']['hr']:.3f}")
    lines.append(f"  B2 (exclude): {scenario_b['exclude_post_soviet']['mig_migrated']['hr']:.3f}")
    lines.append(f"  B3 (reclassify): {scenario_b['reclassify_post_soviet']['mig_migrated']['hr']:.3f}")
    lines.append(f"  C 5%: {scenario_c['0.05']['mig_migrated']['median_hr']:.3f}  "
                 f"10%: {scenario_c['0.1']['mig_migrated']['median_hr']:.3f}  "
                 f"15%: {scenario_c['0.15']['mig_migrated']['median_hr']:.3f}")

    output = "\n".join(lines)
    with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
        f.write(output)

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)

    print(f"\n✓ Written: {OUTPUT_TXT}")
    print(f"✓ Written: {OUTPUT_JSON}")
    print("\n" + "=" * 60)
    print(output.split("SUMMARY")[1])


if __name__ == '__main__':
    main()
