"""
stage9c_wave_lifespan_chart.py
Figure 29c — Age at death by emigration wave (box plot + mean markers)
Shows the distribution of actual lifespans per wave vs the non-migrant reference.
Outputs:
  charts/fig29c_wave_lifespan.png
  charts/fig29c_interactive.html
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.graph_objects as go

PROJECT = os.path.dirname(os.path.abspath(__file__))
CHARTS  = os.path.join(PROJECT, 'charts')
os.makedirs(CHARTS, exist_ok=True)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

main_df = pd.read_csv(os.path.join(PROJECT, 'esu_creative_workers_v2_3.csv'))
wave_df = pd.read_csv(os.path.join(PROJECT, 'wave_assignments.csv'))

# Compute age at death
main_df['age_at_death'] = pd.to_numeric(main_df['death_year'], errors='coerce') - \
                          pd.to_numeric(main_df['birth_year'], errors='coerce')

# Non-migrant reference
nm = main_df[main_df['migration_status'] == 'non_migrated']['age_at_death'].dropna()
nm_mean = nm.mean()  # 71.22

# Merge wave assignments onto migrant rows with age_at_death
migrants = main_df[main_df['migration_status'] == 'migrated'].copy()
merged = migrants.merge(wave_df[['name', 'wave']], on='name', how='left')
merged['wave'] = merged['wave'].fillna('UNKNOWN')

# Only plot WAVE1, WAVE2, WAVE3 (exclude WAVE4 — post-Soviet, different epoch;
# exclude UNKNOWN — insufficient data)
wave_order  = ['Non-migrated', 'WAVE1\n(pre-1922)', 'WAVE2\n(1939–45)', 'WAVE3\n(1946–91)']
wave_labels = ['Non-migrated', 'WAVE1\n(pre-1922)', 'WAVE2\n(1939–45)', 'WAVE3\n(1946–91)']
wave_keys   = ['NON_MIG', 'WAVE1', 'WAVE2', 'WAVE3']

groups = {
    'NON_MIG': nm.values,
    'WAVE1':   merged[merged['wave'] == 'WAVE1']['age_at_death'].dropna().values,
    'WAVE2':   merged[merged['wave'] == 'WAVE2']['age_at_death'].dropna().values,
    'WAVE3':   merged[merged['wave'] == 'WAVE3']['age_at_death'].dropna().values,
}

colours = {
    'NON_MIG': '#888888',
    'WAVE1':   '#2196F3',   # blue
    'WAVE2':   '#FF9800',   # orange
    'WAVE3':   '#4CAF50',   # green
}

ns = {k: len(v) for k, v in groups.items()}
means = {k: np.mean(v) for k, v in groups.items()}

# ---------------------------------------------------------------------------
# Static PNG (matplotlib)
# ---------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#fafafa')
ax.set_facecolor('#f7f7f7')

positions = [1, 2, 3, 4]
data_list = [groups[k] for k in wave_keys]

bp = ax.boxplot(
    data_list,
    positions=positions,
    widths=0.5,
    patch_artist=True,
    medianprops=dict(color='black', linewidth=2),
    whiskerprops=dict(linewidth=1.3),
    capprops=dict(linewidth=1.3),
    flierprops=dict(marker='o', markersize=3, alpha=0.3, linestyle='none'),
    showfliers=True,
)

for patch, key in zip(bp['boxes'], wave_keys):
    patch.set_facecolor(colours[key])
    patch.set_alpha(0.75)
for flier, key in zip(bp['fliers'], wave_keys):
    flier.set_markerfacecolor(colours[key])
    flier.set_markeredgecolor(colours[key])

# Mean diamond markers
for pos, key in zip(positions, wave_keys):
    ax.plot(pos, means[key], marker='D', color='white',
            markeredgecolor='black', markeredgewidth=1.5,
            markersize=9, zorder=5, label='_nolegend_')

# Non-migrant reference line
ax.axhline(nm_mean, color='#888888', linewidth=1.5, linestyle='--',
           alpha=0.8, zorder=2)
ax.text(4.55, nm_mean + 0.6, f'Non-mig\nmean\n{nm_mean:.1f}y',
        fontsize=8, color='#555', va='bottom', ha='center')

# Gap annotations above each migrant box
for pos, key, lbl in zip(positions[1:], wave_keys[1:], wave_labels[1:]):
    gap = means[key] - nm_mean
    sign = '+' if gap >= 0 else ''
    colour = '#2e7d32' if gap > 0 else ('#c62828' if gap < 0 else '#555')
    ax.annotate(
        f'{sign}{gap:.1f}y vs ref',
        xy=(pos, np.percentile(groups[key], 75)),
        xytext=(pos, np.percentile(groups[key], 75) + 5),
        fontsize=8.5, color=colour, ha='center', fontweight='bold',
        arrowprops=dict(arrowstyle='->', color=colour, lw=1.2),
    )

# x-axis labels with n
xlabels = [f'{lbl}\n(n={ns[k]:,})' for lbl, k in zip(wave_labels, wave_keys)]
ax.set_xticks(positions)
ax.set_xticklabels(xlabels, fontsize=10)
ax.set_ylabel('Age at Death (years)', fontsize=11)
ax.set_xlabel('Emigration Wave', fontsize=11)
ax.set_title(
    'Age at Death by Emigration Wave\n'
    'Box = IQR; line = median; ◆ = mean; dashed = non-migrant reference',
    fontsize=12, fontweight='bold', pad=12
)
ax.set_ylim(0, 110)
ax.yaxis.grid(True, linestyle='--', alpha=0.5)
ax.set_axisbelow(True)

# Legend patches
legend_handles = [
    mpatches.Patch(facecolor=colours[k], alpha=0.75, label=lbl.replace('\n', ' '))
    for k, lbl in zip(wave_keys, wave_labels)
]
ax.legend(handles=legend_handles, loc='lower right', fontsize=9,
          framealpha=0.9, edgecolor='#ccc')

plt.tight_layout()
out_png = os.path.join(CHARTS, 'fig29c_wave_lifespan.png')
plt.savefig(out_png, dpi=150, bbox_inches='tight')
plt.close()
print(f'Saved {out_png}')

# ---------------------------------------------------------------------------
# Interactive Plotly version
# ---------------------------------------------------------------------------

fig_plotly = go.Figure()

plotly_labels = ['Non-migrated', 'WAVE1 (pre-1922)', 'WAVE2 (1939–45)', 'WAVE3 (1946–91)']
plotly_colours = ['#888888', '#2196F3', '#FF9800', '#4CAF50']

for key, label, colour in zip(wave_keys, plotly_labels, plotly_colours):
    data = groups[key]
    fig_plotly.add_trace(go.Box(
        y=data,
        name=f'{label}<br>(n={ns[key]:,})',
        boxmean='sd',
        marker_color=colour,
        marker_opacity=0.75,
        line_color=colour,
        fillcolor=colour,
        opacity=0.75,
        hovertemplate=(
            f'<b>{label}</b><br>'
            'Age: %{y:.0f}y<br>'
            '<extra></extra>'
        )
    ))

# Reference line
fig_plotly.add_hline(
    y=nm_mean,
    line_dash='dash',
    line_color='#888',
    line_width=1.5,
    annotation_text=f'Non-mig mean: {nm_mean:.1f}y',
    annotation_position='right',
)

fig_plotly.update_layout(
    title=dict(
        text='Age at Death by Emigration Wave<br>'
             '<sup>Box = IQR; line = median; dot = mean ± SD; dashed = non-migrant reference</sup>',
        font_size=15,
    ),
    yaxis_title='Age at Death (years)',
    xaxis_title='Emigration Wave',
    yaxis=dict(range=[0, 110]),
    plot_bgcolor='#f7f7f7',
    paper_bgcolor='#fafafa',
    showlegend=True,
    legend=dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5),
    height=520,
    margin=dict(l=60, r=60, t=100, b=80),
)

html_div = fig_plotly.to_html(full_html=False, include_plotlyjs=False)
out_html = os.path.join(CHARTS, 'fig29c_interactive.html')
with open(out_html, 'w', encoding='utf-8') as f:
    f.write(html_div)
print(f'Saved {out_html}')

# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------

print('\n--- AGE AT DEATH SUMMARY BY WAVE ---')
print(f'{"Wave":<20} {"n":>6}  {"Mean":>7}  {"Median":>7}  {"SD":>6}  {"Gap":>8}')
print('-' * 65)
for key, label in zip(wave_keys, ['Non-migrated', 'WAVE1', 'WAVE2', 'WAVE3']):
    data = groups[key]
    gap = means[key] - nm_mean if key != 'NON_MIG' else 0.0
    sign = '+' if gap > 0 else ''
    print(f'{label:<20} {ns[key]:>6}  {means[key]:>7.2f}  {np.median(data):>7.1f}  '
          f'{np.std(data):>6.1f}  {sign}{gap:>7.2f}y')
