# Fig 04 — Box Plots: Age at Death Distribution

**File:** `charts/fig04_box_plots.png`

## What this chart shows
Box-and-whisker plots showing the full statistical distribution of ages at death for each group. The box covers the middle 50% of the data (IQR); the line in the middle is the median; whiskers extend to the min/max non-outlier values; dots are outliers.

## Key finding (V2.3)
- **Migrated:** Median = 77, box sits highest — most deaths in the 70s-80s (n=1,324)
- **Non-migrated:** Median = 73, close to internal transfer (n=5,960)
- **Internal transfer:** Median = 72, nearly identical to non-migrated (null result confirmed) (n=1,111)
- **Deported:** Median = **45 years**, box dramatically lower, wide spread (IQR spans ~35-60) (n=195)

## What to look for
- The deported box sits far below the others — visually shows the severity
- Outlier dots above the migrated box = long-lived diaspora members (some reached 90s+)
- Overlap between non-migrated and internal transfer groups confirms they're similar populations

## ⚠️ Y-axis bug — FIXED in V2.2 (still clean in V2.3)
`ax.set_ylim(0, 110)` is in `generate_analysis.py`. Y-axis no longer goes negative. Charts regenerated from V2.6 data are clean.
