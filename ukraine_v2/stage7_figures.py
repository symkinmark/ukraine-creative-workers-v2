#!/usr/bin/env python3
"""
Stage 7 — Regenerate figures for right-censored analysis (V2.4)

Generates:
  fig24 — Cox forest plot (Model 1 + Model 2 HRs) — UPDATED
  fig25 — Censoring pattern by group — UPDATED (proper distribution)
  fig26 — Kaplan-Meier curves with right-censoring — UPDATED
  fig27 — Sensitivity analysis summary plot (NEW)

Input:  data/esu_extended_for_cox.csv
        results/cox_censored_output.txt  (for HR values)
        results/sensitivity_results.json

Output: charts/fig24_cox_forest_plot.png + interactive
        charts/fig25_censoring_pattern.png + interactive
        charts/fig26_km_censored.png + interactive
        charts/fig27_sensitivity_summary.png + interactive

Usage: python3 ukraine_v2/stage7_figures.py
"""

import json
import os
import sys
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    print("ERROR: matplotlib not installed"); sys.exit(1)

try:
    import plotly.graph_objects as go
    import plotly.io as pio
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
    print("WARNING: plotly not installed — skipping interactive charts")

try:
    from lifelines import KaplanMeierFitter
    HAS_LIFELINES = True
except ImportError:
    HAS_LIFELINES = False
    print("WARNING: lifelines not installed — skipping KM curves")

CHARTS_DIR = os.path.join(os.path.dirname(__file__), 'charts')
DATA_PATH  = os.path.join(os.path.dirname(__file__), 'data', 'esu_extended_for_cox.csv')
SENS_PATH  = os.path.join(os.path.dirname(__file__), 'results', 'sensitivity_results.json')
os.makedirs(CHARTS_DIR, exist_ok=True)

GROUP_COLORS = {
    'migrated':          '#2196F3',
    'non_migrated':      '#4CAF50',
    'internal_transfer': '#FF9800',
    'deported':          '#F44336',
}
GROUP_LABELS = {
    'migrated':          'Migrated',
    'non_migrated':      'Non-migrated',
    'internal_transfer': 'Internal transfer',
    'deported':          'Deported',
}


# ──────────────────────────────────────────────────────────────────────────────
# FIG 24 — Cox Forest Plot
# ──────────────────────────────────────────────────────────────────────────────

def make_fig24():
    """Cox forest plot with Model 1 (unadjusted) and Model 2 (adjusted) HRs."""
    print("  fig24: Cox forest plot...", flush=True)

    # Hard-coded from stage5_cox output
    models = {
        'Model 1 (unadjusted)': {
            'migrated':          (1.088, 1.028, 1.151),
            'internal_transfer': (1.541, 1.451, 1.637),
            'deported':          (4.964, 4.267, 5.773),
        },
        'Model 2 (adjusted)': {
            'migrated':          (0.832, 0.778, 0.889),
            'internal_transfer': (1.105, 1.033, 1.182),
            'deported':          (4.646, 3.908, 5.524),
        },
    }

    groups = ['migrated', 'internal_transfer', 'deported']
    group_labels = [GROUP_LABELS[g] for g in groups]
    n_groups = len(groups)
    y_pos_m1 = np.arange(n_groups) * 3 + 1.3
    y_pos_m2 = np.arange(n_groups) * 3 + 0.7

    fig, ax = plt.subplots(figsize=(9, 5))

    for i, g in enumerate(groups):
        # Model 1
        hr1, lo1, hi1 = models['Model 1 (unadjusted)'][g]
        ax.errorbar(hr1, y_pos_m1[i], xerr=[[hr1-lo1], [hi1-hr1]],
                    fmt='s', color=GROUP_COLORS[g], alpha=0.5, capsize=4,
                    markersize=7, label='Model 1' if i == 0 else '')
        ax.annotate(f'{hr1:.2f} ({lo1:.2f}–{hi1:.2f})',
                    xy=(hi1, y_pos_m1[i]), xytext=(5, 0),
                    textcoords='offset points', va='center', fontsize=7.5, color='#555')

        # Model 2
        hr2, lo2, hi2 = models['Model 2 (adjusted)'][g]
        ax.errorbar(hr2, y_pos_m2[i], xerr=[[hr2-lo2], [hi2-hr2]],
                    fmt='D', color=GROUP_COLORS[g], alpha=1.0, capsize=4,
                    markersize=7, label='Model 2' if i == 0 else '')
        ax.annotate(f'{hr2:.2f} ({lo2:.2f}–{hi2:.2f})',
                    xy=(hi2, y_pos_m2[i]), xytext=(5, 0),
                    textcoords='offset points', va='center', fontsize=7.5, color='#222')

    ax.axvline(1.0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.set_xscale('log')
    ax.set_xlabel('Hazard Ratio (log scale)', fontsize=10)
    ax.set_title('Figure 11 — Cox PH Hazard Ratios by Migration Group\n'
                 '(Right-censored N=15,053; reference = non-migrated)', fontsize=10)
    ax.set_yticks([(y_pos_m1[i] + y_pos_m2[i]) / 2 for i in range(n_groups)])
    ax.set_yticklabels(group_labels, fontsize=10)
    ax.set_ylim(0, n_groups * 3 + 0.5)

    m1_patch = mpatches.Patch(facecolor='grey', alpha=0.5, label='Model 1 (unadjusted) — square')
    m2_patch = mpatches.Patch(facecolor='grey', alpha=1.0, label='Model 2 (adjusted) — diamond')
    ax.legend(handles=[m1_patch, m2_patch], fontsize=8, loc='lower right')

    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()

    out_path = os.path.join(CHARTS_DIR, 'fig24_cox_forest_plot.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    ✓ {out_path}")

    # Interactive
    if HAS_PLOTLY:
        _fig24_plotly(models, groups, group_labels)


def _fig24_plotly(models, groups, group_labels):
    fig = go.Figure()
    for i, (g, gl) in enumerate(zip(groups, group_labels)):
        color = GROUP_COLORS[g]
        for j, (mname, symbol, opacity) in enumerate([
            ('Model 1 (unadjusted)', 'square', 0.5),
            ('Model 2 (adjusted)',   'diamond', 1.0),
        ]):
            hr, lo, hi = models[mname][g]
            fig.add_trace(go.Scatter(
                x=[hr], y=[f"{gl} — {mname.split()[0]} {mname.split()[1]}"],
                error_x=dict(type='data', symmetric=False,
                             array=[hi-hr], arrayminus=[hr-lo]),
                mode='markers',
                marker=dict(symbol=symbol, size=10, color=color, opacity=opacity),
                name=mname,
                showlegend=(i == 0),
                hovertemplate=f"{gl}<br>{mname}<br>HR={hr:.3f} (95%CI {lo:.3f}–{hi:.3f})<extra></extra>",
            ))
    fig.add_vline(x=1.0, line_dash='dash', line_color='black', opacity=0.5)
    fig.update_xaxes(type='log', title='Hazard Ratio (log scale)')
    fig.update_layout(
        title='Figure 11 — Cox PH Hazard Ratios (Right-Censored N=15,053)',
        height=400, template='plotly_white',
    )
    out = os.path.join(CHARTS_DIR, 'fig24_interactive.html')
    pio.write_html(fig, out, include_plotlyjs='cdn', full_html=True)
    print(f"    ✓ {out}")


# ──────────────────────────────────────────────────────────────────────────────
# FIG 25 — Censoring Pattern
# ──────────────────────────────────────────────────────────────────────────────

def make_fig25(df):
    print("  fig25: Censoring pattern...", flush=True)

    groups = ['migrated', 'non_migrated', 'internal_transfer', 'deported']
    stats = []
    for g in groups:
        sub = df[df['migration_status'] == g]
        n = len(sub)
        n_dead = int(sub['event_observed'].sum())
        n_alive = n - n_dead
        stats.append({'group': g, 'label': GROUP_LABELS[g], 'n': n,
                      'pct_dead': n_dead/n*100, 'pct_alive': n_alive/n*100,
                      'n_dead': n_dead, 'n_alive': n_alive})

    x = np.arange(len(stats))
    width = 0.6

    fig, ax = plt.subplots(figsize=(8, 5))
    bars_dead  = ax.bar(x, [s['pct_dead']  for s in stats], width, label='Dead (event observed)',  color='#F44336', alpha=0.8)
    bars_alive = ax.bar(x, [s['pct_alive'] for s in stats], width, bottom=[s['pct_dead'] for s in stats],
                        label='Alive in 2026 (right-censored)', color='#2196F3', alpha=0.6)

    for i, s in enumerate(stats):
        ax.text(i, s['pct_dead']/2, f"{s['pct_dead']:.1f}%\n(n={s['n_dead']:,})",
                ha='center', va='center', fontsize=8, color='white', fontweight='bold')
        if s['pct_alive'] > 2:
            ax.text(i, s['pct_dead'] + s['pct_alive']/2,
                    f"{s['pct_alive']:.1f}%\n(n={s['n_alive']:,})",
                    ha='center', va='center', fontsize=8, color='white', fontweight='bold')
        ax.text(i, 102, f"N={s['n']:,}", ha='center', va='bottom', fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels([s['label'] for s in stats], fontsize=9)
    ax.set_ylabel('Percentage (%)', fontsize=10)
    ax.set_ylim(0, 115)
    ax.set_title('Figure A11 — Censoring Pattern by Migration Group\n'
                 f'Extended dataset N={len(df):,} (dead + right-censored living individuals)', fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    out_path = os.path.join(CHARTS_DIR, 'fig25_censoring_pattern.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    ✓ {out_path}")

    if HAS_PLOTLY:
        _fig25_plotly(stats, len(df))


def _fig25_plotly(stats, n_total):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[s['label'] for s in stats],
        y=[s['pct_dead'] for s in stats],
        name='Dead (event observed)',
        marker_color='#F44336',
        text=[f"{s['pct_dead']:.1f}%<br>(n={s['n_dead']:,})" for s in stats],
        textposition='inside',
    ))
    fig.add_trace(go.Bar(
        x=[s['label'] for s in stats],
        y=[s['pct_alive'] for s in stats],
        name='Alive in 2026 (right-censored)',
        marker_color='#2196F3',
        text=[f"{s['pct_alive']:.1f}%<br>(n={s['n_alive']:,})" for s in stats],
        textposition='inside',
    ))
    fig.update_layout(
        barmode='stack',
        title=f'Figure A11 — Censoring Pattern by Migration Group (N={n_total:,})',
        yaxis_title='Percentage (%)',
        template='plotly_white',
        height=450,
    )
    out = os.path.join(CHARTS_DIR, 'fig25_interactive.html')
    pio.write_html(fig, out, include_plotlyjs='cdn', full_html=True)
    print(f"    ✓ {out}")


# ──────────────────────────────────────────────────────────────────────────────
# FIG 26 — Kaplan-Meier Curves
# ──────────────────────────────────────────────────────────────────────────────

def make_fig26(df):
    if not HAS_LIFELINES:
        print("  fig26: skipping (no lifelines)")
        return
    print("  fig26: KM curves with right-censoring...", flush=True)

    groups = ['migrated', 'non_migrated', 'internal_transfer', 'deported']
    fig, ax = plt.subplots(figsize=(10, 6))

    for g in groups:
        sub = df[df['migration_status'] == g].copy()
        kmf = KaplanMeierFitter()
        kmf.fit(sub['duration'], event_observed=sub['event_observed'],
                label=f"{GROUP_LABELS[g]} (n={len(sub):,})")
        kmf.plot_survival_function(ax=ax, color=GROUP_COLORS[g],
                                   show_censors=True, censor_styles={'ms': 3, 'marker': '|'})

    ax.set_xlabel('Age (years)', fontsize=11)
    ax.set_ylabel('Survival probability', fontsize=11)
    ax.set_title('Figure A12 — Kaplan-Meier Survival Curves with Right-Censored Data\n'
                 f'N={len(df):,} (tick marks = censoring events)', fontsize=10)
    ax.set_xlim(0, 110)
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(alpha=0.3)
    plt.tight_layout()

    out_path = os.path.join(CHARTS_DIR, 'fig26_km_censored.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    ✓ {out_path}")

    if HAS_PLOTLY:
        _fig26_plotly(df, groups)


def _fig26_plotly(df, groups):
    from lifelines import KaplanMeierFitter
    fig = go.Figure()
    for g in groups:
        sub = df[df['migration_status'] == g].copy()
        kmf = KaplanMeierFitter()
        kmf.fit(sub['duration'], event_observed=sub['event_observed'])
        t = kmf.survival_function_.index
        s = kmf.survival_function_['KM_estimate']
        fig.add_trace(go.Scatter(
            x=t, y=s,
            mode='lines',
            name=f"{GROUP_LABELS[g]} (n={len(sub):,})",
            line=dict(color=GROUP_COLORS[g]),
        ))
    fig.update_layout(
        title=f'Figure A12 — KM Survival Curves with Right-Censoring (N={len(df):,})',
        xaxis_title='Age (years)',
        yaxis_title='Survival probability',
        xaxis=dict(range=[0, 110]),
        template='plotly_white',
        height=500,
    )
    out = os.path.join(CHARTS_DIR, 'fig26_interactive.html')
    pio.write_html(fig, out, include_plotlyjs='cdn', full_html=True)
    print(f"    ✓ {out}")


# ──────────────────────────────────────────────────────────────────────────────
# FIG 27 — Sensitivity Summary
# ──────────────────────────────────────────────────────────────────────────────

def make_fig27():
    print("  fig27: Sensitivity summary...", flush=True)

    with open(SENS_PATH) as f:
        sens = json.load(f)

    # Collect migrated HR across all scenarios
    points = []

    # Baseline (Model 2 adjusted)
    points.append(('Baseline\n(Model 2)', 0.832, 0.778, 0.889, 'primary'))

    # Scenario A
    for dur in [70, 75, 80, 85, 90]:
        hr = sens['scenario_a'][str(dur)]['mig_migrated']['hr']
        lo = sens['scenario_a'][str(dur)]['mig_migrated']['lo']
        hi = sens['scenario_a'][str(dur)]['mig_migrated']['hi']
        points.append((f'Age={dur}\n(unadj)', hr, lo, hi, 'scenA'))

    # Scenario B
    for key, label in [('include_all', 'Incl. all\n(unadj)'),
                        ('exclude_post_soviet', 'Excl. post-\nSoviet em.'),
                        ('reclassify_post_soviet', 'Recl. post-\nSoviet em.')]:
        hr = sens['scenario_b'][key]['mig_migrated']['hr']
        lo = sens['scenario_b'][key]['mig_migrated']['lo']
        hi = sens['scenario_b'][key]['mig_migrated']['hi']
        points.append((label, hr, lo, hi, 'scenB'))

    # Scenario C (bootstrap medians)
    for rate_str, label in [('0.05', 'Misclass\n5%'), ('0.1', 'Misclass\n10%'), ('0.15', 'Misclass\n15%')]:
        d = sens['scenario_c'][rate_str]['mig_migrated']
        points.append((label, d['median_hr'], d['lo'], d['hi'], 'scenC'))

    labels   = [p[0] for p in points]
    hrs      = [p[1] for p in points]
    los      = [p[2] for p in points]
    his      = [p[3] for p in points]
    types    = [p[4] for p in points]

    color_map = {'primary': '#1a237e', 'scenA': '#0288d1', 'scenB': '#388e3c', 'scenC': '#e64a19'}
    colors = [color_map[t] for t in types]

    x = np.arange(len(points))
    fig, ax = plt.subplots(figsize=(14, 5))

    for i in range(len(points)):
        ax.errorbar(i, hrs[i], yerr=[[hrs[i]-los[i]], [his[i]-hrs[i]]],
                    fmt='o', color=colors[i], capsize=4, markersize=7,
                    linewidth=1.5 if types[i] == 'primary' else 1.0)

    ax.axhline(1.0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.axhline(0.832, color='#1a237e', linewidth=0.8, linestyle=':', alpha=0.4)

    # Shade scenarios
    ax.axvspan(-0.5, 0.5, alpha=0.04, color='#1a237e')
    ax.axvspan(0.5, 5.5, alpha=0.04, color='#0288d1')
    ax.axvspan(5.5, 8.5, alpha=0.04, color='#388e3c')
    ax.axvspan(8.5, 11.5, alpha=0.04, color='#e64a19')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=7.5)
    ax.set_ylabel('Migrated HR vs non-migrated', fontsize=10)
    ax.set_title('Figure A17 — Sensitivity Analysis: Migrated Hazard Ratio Across Scenarios\n'
                 'Dashed = HR=1.0  Dotted = Baseline HR=0.832', fontsize=10)
    ax.grid(axis='y', alpha=0.3)

    patches = [
        mpatches.Patch(color='#1a237e', label='Baseline (Model 2 adjusted)'),
        mpatches.Patch(color='#0288d1', label='Scenario A: age assumption'),
        mpatches.Patch(color='#388e3c', label='Scenario B: post-Soviet migrants'),
        mpatches.Patch(color='#e64a19', label='Scenario C: misclassification bootstrap'),
    ]
    ax.legend(handles=patches, fontsize=8, loc='upper right')
    plt.tight_layout()

    out_path = os.path.join(CHARTS_DIR, 'fig27_sensitivity_summary.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    ✓ {out_path}")

    if HAS_PLOTLY:
        _fig27_plotly(points, labels, hrs, los, his, types, color_map)


def _fig27_plotly(points, labels, hrs, los, his, types, color_map):
    fig = go.Figure()
    for i, (label, hr, lo, hi, t) in enumerate(points):
        fig.add_trace(go.Scatter(
            x=[label.replace('\n', ' ')], y=[hr],
            error_y=dict(type='data', symmetric=False,
                         array=[hi-hr], arrayminus=[hr-lo]),
            mode='markers',
            marker=dict(size=9, color=color_map[t]),
            name=label.replace('\n', ' '),
            showlegend=False,
            hovertemplate=f"{label.replace(chr(10),' ')}<br>HR={hr:.3f} (95%CI {lo:.3f}–{hi:.3f})<extra></extra>",
        ))
    fig.add_hline(y=1.0, line_dash='dash', line_color='black', opacity=0.5)
    fig.add_hline(y=0.832, line_dash='dot', line_color='navy', opacity=0.4)
    fig.update_layout(
        title='Figure A17 — Sensitivity: Migrated HR Across Scenarios',
        yaxis_title='Hazard Ratio',
        template='plotly_white',
        height=450,
    )
    out = os.path.join(CHARTS_DIR, 'fig27_interactive.html')
    pio.write_html(fig, out, include_plotlyjs='cdn', full_html=True)
    print(f"    ✓ {out}")


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    df = pd.read_csv(DATA_PATH)
    # Apply implausibly_alive fix for KM/censoring charts
    mask = df['implausibly_alive'] == True
    df.loc[mask, 'duration'] = 80
    df.loc[mask, 'event_observed'] = 1
    df = df.dropna(subset=['duration', 'migration_status'])
    df = df[df['duration'] > 0]

    print(f"Loaded {len(df):,} rows for figures")
    print()

    make_fig24()
    make_fig25(df)
    make_fig26(df)
    make_fig27()

    print("\nAll Stage 7 figures complete.")


if __name__ == '__main__':
    main()
