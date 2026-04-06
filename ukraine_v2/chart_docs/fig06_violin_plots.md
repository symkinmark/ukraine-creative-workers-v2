# Fig 06 — Split Violin Plots: Distribution Shape by Group × Gender

**File:** `charts/fig06_violin_plots.png`

## What this chart shows
Split violin plots — each violin is divided down the middle by gender. **Blue (left half) = Male, Red (right half) = Female.** The width of each half shows where that gender's deaths are concentrated. Inner quartile lines mark the median and IQR within each half.

This gives a richer view of distribution shape than box plots, and now shows whether the group-level mortality patterns hold for both sexes independently.

Sample counts (M: / F:) are annotated below each violin pair.

## Key finding
- **Migrated:** Both male and female halves are wide at the top (70s–80s) — the long upper tail is present in both sexes
- **Deported:** Both halves are fat in the 40s–50s and truncated above — state violence hit male and female creative workers alike
- **Non-migrated & Internal transfer:** Similar symmetrical distributions in both sexes, slightly lower than migrated

## What to look for
- Whether the male and female halves are similarly shaped (they broadly are — the group-level pattern is not gender-specific)
- The female deported half is based on a small n (~30 women) — it will be wider and less smooth than the male half
- The migrated female violin extends into the 90s — consistent with the general female longevity advantage in the diaspora

## Update history
- **V2.3 (2026-04-06):** Chart redesigned as a **split violin by gender** (was previously a single undivided violin per group). `hue='gender'`, `split=True` in seaborn. Y-axis extended to −12 to accommodate M:/F: annotations below the x-axis.
- **V2.2:** Y-axis bug fixed (`ax.set_ylim(0, 110)`). Now `(-12, 110)` to allow annotation space.
