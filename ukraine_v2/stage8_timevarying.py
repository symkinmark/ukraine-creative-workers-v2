#!/usr/bin/env python3
"""
Stage 8 — Time-Varying Hazard Ratio Analysis (age-band landmark Cox)

Problem: The Cox PH assumption is violated for the deported group (Schoenfeld p<0.0001)
because deportees did not face a constant steady-state risk — they faced concentrated
mass killing between roughly ages 30–55 (the Great Terror / Gulag years, 1937–1945),
followed by much lower mortality among survivors.

Solution: Fit a separate Cox model within each age band using only individuals alive
at the start of that band (landmark analysis). This shows how the deported HR changes
across the life course — expected to show a massive spike in age 30–60, collapsing
toward 1.0 afterward.

Also: Schoenfeld residuals smoothed log-HR plot (direct visualisation of PH violation).

Output:
  charts/fig28_deported_hr_by_age.png + interactive
  charts/fig28b_schoenfeld_smooth.png
  results/timevarying_output.txt

Usage: python3 ukraine_v2/stage8_timevarying.py
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')

try:
    from lifelines import CoxPHFitter
except ImportError:
    print("ERROR: lifelines not installed."); sys.exit(1)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    print("ERROR: matplotlib not installed."); sys.exit(1)

try:
    import plotly.graph_objects as go
    import plotly.io as pio
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

DATA_PATH   = os.path.join(os.path.dirname(__file__), 'data', 'esu_extended_for_cox.csv')
OUTPUT_TXT  = os.path.join(os.path.dirname(__file__), 'results', 'timevarying_output.txt')
CHARTS_DIR  = os.path.join(os.path.dirname(__file__), 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(OUTPUT_TXT), exist_ok=True)


def load_and_prep(df_raw):
    d = df_raw.copy()
    mask = d['implausibly_alive'] == True
    d.loc[mask, 'duration'] = 80
    d.loc[mask, 'event_observed'] = 1
    d = d.dropna(subset=['duration', 'migration_status'])
    d = d[d['duration'] > 0]
    d['mig_deported']          = (d['migration_status'] == 'deported').astype(int)
    d['mig_migrated']          = (d['migration_status'] == 'migrated').astype(int)
    d['mig_internal_transfer'] = (d['migration_status'] == 'internal_transfer').astype(int)
    return d


def landmark_cox_by_band(d, age_bands):
    """
    For each age band [lo, hi), take all individuals still alive at age=lo
    (i.e., duration >= lo) and fit a Cox model on the residual time within
    the band. Returns list of dicts with band info + deported HR.
    """
    results = []
    # Only use confirmed dead + deported/non_migrated groups for deported HR stability
    groups_of_interest = ['deported', 'non_migrated', 'migrated', 'internal_transfer']
    d_sub = d[d['migration_status'].isin(groups_of_interest)].copy()

    for lo, hi in age_bands:
        # Individuals alive at age lo: duration >= lo
        at_risk = d_sub[d_sub['duration'] >= lo].copy()

        # Truncate duration to the band
        # Time in band = min(duration, hi) - lo
        at_risk['band_duration'] = np.minimum(at_risk['duration'], hi) - lo
        # Event observed = 1 only if they died within this band
        at_risk['band_event'] = (
            (at_risk['event_observed'] == 1) &
            (at_risk['duration'] < hi)
        ).astype(int)

        at_risk = at_risk[at_risk['band_duration'] > 0]

        if len(at_risk) < 20:
            print(f"  Band {lo}-{hi}: too few ({len(at_risk)}) — skipping")
            continue

        n_dep = (at_risk['mig_deported'] == 1).sum()
        n_dep_events = at_risk.loc[at_risk['mig_deported'] == 1, 'band_event'].sum()

        if n_dep < 3 or n_dep_events < 2:
            print(f"  Band {lo}-{hi}: too few deported events ({n_dep_events}) — skipping")
            continue

        try:
            cph = CoxPHFitter(penalizer=0.5)
            fit_cols = ['band_duration', 'band_event', 'mig_deported',
                        'mig_migrated', 'mig_internal_transfer']
            cph.fit(at_risk[fit_cols].dropna(),
                    duration_col='band_duration', event_col='band_event')

            v = 'mig_deported'
            hr  = float(np.exp(cph.params_[v]))
            lo2 = float(np.exp(cph.confidence_intervals_.loc[v, '95% lower-bound']))
            hi2 = float(np.exp(cph.confidence_intervals_.loc[v, '95% upper-bound']))
            p   = float(cph.summary.loc[v, 'p'])

            n_total_events = int(at_risk['band_event'].sum())

            results.append({
                'band_lo': lo, 'band_hi': hi,
                'label': f'{lo}–{hi}',
                'n_at_risk': len(at_risk),
                'n_deported': int(n_dep),
                'n_deported_events': int(n_dep_events),
                'n_total_events': n_total_events,
                'hr': hr, 'lo': lo2, 'hi': hi2, 'p': p,
            })
            print(f"  Band {lo}–{hi}: n={len(at_risk):,}  dep_events={n_dep_events}  "
                  f"HR={hr:.2f} ({lo2:.2f}–{hi2:.2f})  p={p:.4f}", flush=True)
        except Exception as e:
            print(f"  Band {lo}–{hi}: fit failed — {e}")

    return results


def make_fig28(band_results):
    """Main figure: deported HR by age band."""
    print("\n  Generating fig28...", flush=True)

    labels = [r['label'] for r in band_results]
    hrs    = [r['hr']   for r in band_results]
    los    = [r['lo']   for r in band_results]
    his    = [r['hi']   for r in band_results]
    ns     = [r['n_deported_events'] for r in band_results]
    ps     = [r['p']    for r in band_results]
    x      = np.arange(len(band_results))

    # Colour by significance
    colors = ['#D32F2F' if p < 0.05 else '#FF8A65' for p in ps]

    fig, ax = plt.subplots(figsize=(14, 7))

    for i in range(len(band_results)):
        ax.errorbar(x[i], hrs[i],
                    yerr=[[hrs[i] - los[i]], [his[i] - hrs[i]]],
                    fmt='o', color=colors[i], capsize=5,
                    markersize=9, linewidth=2,
                    zorder=3)
        # Annotate with n events
        ax.annotate(f'n={ns[i]}', xy=(x[i], his[i]),
                    xytext=(0, 6), textcoords='offset points',
                    ha='center', fontsize=8, color='#555')

    ax.axhline(1.0, color='black', linewidth=0.9, linestyle='--', alpha=0.6,
               label='HR = 1.0 (no difference from non-migrants)')

    ax.set_yscale('log')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_xlabel('Age band (years)', fontsize=11)
    ax.set_ylabel('Hazard ratio for deported workers vs. non-migrants\n(log scale)', fontsize=10)
    ax.set_title(
        'Figure 28 — Deported Workers: Mortality Hazard by Age Band\n'
        'Landmark Cox model fitted within each decade of age (reference = non-migrated)\n'
        'Red = p < 0.05  Orange = p ≥ 0.05  n = number of deported deaths in band',
        fontsize=10
    )

    # Shading for Terror years context
    # Most deportees born ~1880–1920 → aged 30–55 during 1935–1945
    ax.axvspan(-0.5, 2.5, alpha=0.06, color='#B71C1C',
               label='Primary Terror / Gulag period exposure (ages 30–55, c.1935–1945)')

    ax.legend(fontsize=8, loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
        lambda y, _: f'{y:.0f}' if y >= 1 else f'{y:.1f}'
    ))

    plt.tight_layout()
    out = os.path.join(CHARTS_DIR, 'fig28_deported_hr_by_age.png')
    fig.savefig(out, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"    ✓ {out}")

    if HAS_PLOTLY:
        _fig28_plotly(band_results, labels, hrs, los, his, ns, ps)


def _fig28_plotly(band_results, labels, hrs, los, his, ns, ps):
    fig = go.Figure()

    colors = ['#D32F2F' if p < 0.05 else '#FF8A65' for p in ps]

    fig.add_trace(go.Scatter(
        x=labels,
        y=hrs,
        error_y=dict(
            type='data', symmetric=False,
            array=[h - hr for h, hr in zip(his, hrs)],
            arrayminus=[hr - l for hr, l in zip(hrs, los)],
        ),
        mode='markers',
        marker=dict(size=12, color=colors),
        hovertemplate=[
            f'Age {r["label"]}<br>'
            f'HR = {r["hr"]:.2f} (95% CI {r["lo"]:.2f}–{r["hi"]:.2f})<br>'
            f'p = {r["p"]:.4f}<br>'
            f'Deported deaths in band: {r["n_deported_events"]}<br>'
            f'Total at risk: {r["n_at_risk"]:,}<extra></extra>'
            for r in band_results
        ],
        name='Deported HR vs non-migrated',
    ))

    fig.add_hline(y=1.0, line_dash='dash', line_color='black',
                  annotation_text='HR = 1.0 (no difference)', opacity=0.6)

    fig.add_vrect(x0=labels[0], x1=labels[2],
                  fillcolor='#B71C1C', opacity=0.06,
                  annotation_text='Terror/Gulag exposure age range',
                  annotation_position='top left')

    fig.update_yaxes(type='log', title='Hazard ratio (log scale)')
    fig.update_xaxes(title='Age band (years)')
    fig.update_layout(
        title='Figure 28 — Deported Workers: Mortality Hazard by Age Band<br>'
              '<sup>Landmark Cox model within each decade. Reference = non-migrated. '
              'Red = p < 0.05</sup>',
        template='plotly_white',
        height=500,
    )

    out = os.path.join(CHARTS_DIR, 'fig28_interactive.html')
    pio.write_html(fig, out, include_plotlyjs='cdn', full_html=True)
    print(f"    ✓ {out}")


def make_fig28b_narrative(band_results):
    """
    Figure 28b — "When were deported workers most at risk?"
    A plain-language area chart for historian readers, not a statistics diagnostic.
    Uses the landmark band HRs already computed — no Schoenfeld residuals.

    Design:
    - X axis: age in years (readable, no transformations)
    - Y axis: hazard ratio (1.0 = same risk as non-migrants)
    - Filled area between CI lower and upper bound
    - Terror/Gulag years shaded with label
    - Annotated peak band
    - Every axis label in plain English
    """
    print("\n  Generating fig28b (narrative HR arc)...", flush=True)
    try:
        labels   = [r['label']    for r in band_results]
        midpoints = [(r['band_lo'] + r['band_hi']) / 2 for r in band_results]
        hrs      = [r['hr']  for r in band_results]
        los      = [r['lo']  for r in band_results]
        his      = [r['hi']  for r in band_results]
        ns       = [r['n_deported_events'] for r in band_results]
        ps       = [r['p']   for r in band_results]

        fig, ax = plt.subplots(figsize=(14, 7))

        # Filled CI band
        ax.fill_between(midpoints, los, his,
                        alpha=0.18, color='#B71C1C', label='95% confidence interval')

        # HR line
        ax.plot(midpoints, hrs, color='#B71C1C', linewidth=3,
                marker='o', markersize=10, zorder=4,
                label='Relative mortality risk vs. non-migrated workers')

        # Null line
        ax.axhline(1.0, color='#333', linestyle='--', linewidth=1.2, alpha=0.7,
                   label='1.0 = same mortality rate as non-migrated workers')

        # Terror / Gulag shading — ages 30–55 are the prime exposure window
        ax.axvspan(30, 55, alpha=0.09, color='#B71C1C', zorder=1)
        ax.text(42.5, ax.get_ylim()[0] if ax.get_ylim()[0] > 0 else 0.85,
                'Great Terror &\nGulag years\n(ages 30–55)',
                ha='center', va='bottom', fontsize=9, color='#7f0000',
                style='italic')

        # Annotate each band with n deported deaths
        for i, (x, hr, n, p) in enumerate(zip(midpoints, hrs, ns, ps)):
            sig = '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else ''))
            ax.annotate(
                f'n={n}{sig}',
                xy=(x, hr), xytext=(0, 14),
                textcoords='offset points',
                ha='center', fontsize=9, color='#555',
            )

        # Annotate peak
        peak_idx = hrs.index(max(hrs))
        ax.annotate(
            f'Peak risk: {hrs[peak_idx]:.2f}×\n(ages {labels[peak_idx]})',
            xy=(midpoints[peak_idx], hrs[peak_idx]),
            xytext=(12, 12), textcoords='offset points',
            fontsize=10, color='#B71C1C', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#B71C1C', lw=1.5),
        )

        ax.set_xlim(15, 95)
        ax.set_xticks(midpoints)
        ax.set_xticklabels(labels, fontsize=11)
        ax.set_xlabel('Age range (years)', fontsize=12)
        ax.set_ylabel('Mortality risk relative to non-migrated workers\n'
                      '(e.g. 1.89 = dying at 1.89× the rate at that age)',
                      fontsize=11)
        ax.set_title(
            'Figure 28b — When Were Deported Ukrainian Creative Workers Most at Risk?\n'
            'Mortality hazard by decade of life (reference = workers who stayed in Soviet Ukraine)\n'
            '* p<0.05  ** p<0.01  *** p<0.001  |  n = deported deaths in each age window',
            fontsize=10, pad=14
        )
        ax.legend(fontsize=9, loc='upper right')
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(bottom=0.5)

        plt.tight_layout()
        out = os.path.join(CHARTS_DIR, 'fig28b_schoenfeld_smooth.png')
        fig.savefig(out, dpi=200, bbox_inches='tight')
        plt.close()
        print(f"    ✓ {out}")

        # Interactive Plotly version
        if HAS_PLOTLY:
            _fig28b_plotly(band_results, midpoints, labels, hrs, los, his, ns, ps)

    except Exception as e:
        print(f"    fig28b: skipped — {e}")


def _fig28b_plotly(band_results, midpoints, labels, hrs, los, his, ns, ps):
    fig = go.Figure()

    # CI fill
    fig.add_trace(go.Scatter(
        x=midpoints + midpoints[::-1],
        y=his + los[::-1],
        fill='toself',
        fillcolor='rgba(179,0,0,0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo='skip',
        name='95% CI',
    ))

    # HR line
    fig.add_trace(go.Scatter(
        x=midpoints, y=hrs,
        mode='lines+markers',
        line=dict(color='#B71C1C', width=3),
        marker=dict(size=12, color=[
            '#D32F2F' if p < 0.05 else '#FF8A65' for p in ps
        ]),
        hovertemplate=[
            f'Ages {r["label"]}<br>'
            f'Hazard ratio: {r["hr"]:.2f}<br>'
            f'95% CI: {r["lo"]:.2f}–{r["hi"]:.2f}<br>'
            f'p = {r["p"]:.4f}<br>'
            f'Deported deaths in window: {r["n_deported_events"]}<extra></extra>'
            for r in band_results
        ],
        name='Mortality risk (deported vs. non-migrated)',
    ))

    fig.add_hline(y=1.0, line_dash='dash', line_color='#333',
                  annotation_text='HR = 1.0 (same rate as non-migrants)',
                  annotation_position='bottom right', opacity=0.7)

    fig.add_vrect(x0=30, x1=55, fillcolor='#B71C1C', opacity=0.08,
                  annotation_text='Great Terror & Gulag years',
                  annotation_position='top left')

    fig.update_xaxes(title='Age range (years)', tickvals=midpoints, ticktext=labels)
    fig.update_yaxes(title='Mortality risk relative to non-migrated workers<br>(1.0 = same rate)',
                     rangemode='tozero')
    fig.update_layout(
        title='Figure 28b — When Were Deported Ukrainian Creative Workers Most at Risk?<br>'
              '<sup>Mortality hazard by decade of life. Reference = workers who stayed in Soviet Ukraine.</sup>',
        template='plotly_white',
        height=520,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    )

    out = os.path.join(CHARTS_DIR, 'fig28b_interactive.html')
    pio.write_html(fig, out, include_plotlyjs='cdn', full_html=True)
    print(f"    ✓ {out}")



def main():
    df_raw = pd.read_csv(DATA_PATH)
    d = load_and_prep(df_raw)
    print(f"Loaded {len(d):,} rows\n")

    # Age bands: every 10 years from 20 to 90
    age_bands = [(lo, lo + 10) for lo in range(20, 90, 10)]

    lines = ["=" * 60, "STAGE 8 — TIME-VARYING HAZARD RATIO ANALYSIS", "=" * 60, ""]
    lines.append("Landmark Cox: Deported HR by age band (reference = non-migrated)")
    lines.append("-" * 60)
    lines.append(f"  {'Band':<10} {'n_at_risk':>10} {'dep_events':>12} {'HR':>8}  "
                 f"{'95% CI lo':>10}  {'95% CI hi':>10}  {'p':>8}")
    lines.append("  " + "-" * 72)

    print("Fitting landmark Cox models by age band...", flush=True)
    band_results = landmark_cox_by_band(d, age_bands)

    for r in band_results:
        sig = "***" if r['p'] < 0.001 else ("**" if r['p'] < 0.01 else ("*" if r['p'] < 0.05 else ""))
        lines.append(f"  {r['label']:<10} {r['n_at_risk']:>10,} {r['n_deported_events']:>12}  "
                     f"{r['hr']:>7.3f}  {r['lo']:>10.3f}  {r['hi']:>10.3f}  "
                     f"{r['p']:>8.4f} {sig}")

    lines += ["", "KEY PATTERN:"]
    if band_results:
        peak = max(band_results, key=lambda r: r['hr'])
        late = [r for r in band_results if r['band_lo'] >= 65]
        lines.append(f"  Peak HR: {peak['hr']:.2f} at age band {peak['label']} "
                     f"({peak['n_deported_events']} deported deaths)")
        if late:
            avg_late = np.mean([r['hr'] for r in late])
            lines.append(f"  Mean HR age 65+: {avg_late:.2f} "
                         f"({sum(r['n_deported_events'] for r in late)} deported deaths)")
            lines.append(f"  HR collapse from peak to age 65+: "
                         f"{peak['hr']:.2f} → {avg_late:.2f} ({(1-avg_late/peak['hr'])*100:.0f}% reduction)")

    output = "\n".join(lines)
    with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"\n✓ Written: {OUTPUT_TXT}")

    make_fig28(band_results)
    make_fig28b_narrative(band_results)

    print("\n" + output)
    return band_results


if __name__ == '__main__':
    main()
