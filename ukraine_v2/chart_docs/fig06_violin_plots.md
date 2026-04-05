# Fig 06 — Violin Plots: Distribution Shape by Group

**File:** `charts/fig06_violin_plots.png`

## What this chart shows
Violin plots — like box plots but the width of the shape shows where the data is concentrated. Fat in the middle = lots of people died at that age. The inner box shows the IQR, the dot shows the median.

This gives a richer view of distribution shape than box plots — you can see whether data is symmetrical, skewed, or bimodal.

## Key finding
- **Migrated violin:** Wide at the top (many people dying in their 70s-80s), narrow at the bottom
- **Deported violin:** Wide in the middle (many dying in their 40s-50s), fat at the bottom relative to others
- **Non-migrated & Internal transfer:** Similar bell-shaped distributions, slightly lower than migrated

## What to look for
- The widest part of each violin = where most deaths are concentrated
- Deported violin is much fatter lower down than the others
- Migrated violin is the tallest and fattest at high ages

## ⚠️ Y-axis bug — FIXED in V2.2
`ax.set_ylim(0, 110)` added to `generate_analysis.py`. Y-axis no longer extends below 0. Regenerated chart is clean.
