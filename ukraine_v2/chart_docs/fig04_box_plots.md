# Fig 04 — Box Plots: Age at Death Distribution

**File:** `charts/fig04_box_plots.png`

## What this chart shows
Box-and-whisker plots showing the full statistical distribution of ages at death for each group. The box covers the middle 50% of the data (IQR); the line in the middle is the median; whiskers extend to the min/max non-outlier values; dots are outliers.

## Key finding
- **Migrated:** Median and box are the highest — most deaths in the 70s-80s
- **Non-migrated & Internal transfer:** Similar boxes, slightly lower than migrated
- **Deported:** Box is dramatically lower, median is ~47 years, wide spread

## What to look for
- The deported box sits far below the others — visually shows the severity
- Outlier dots above the migrated box = long-lived diaspora members (some reached 90s+)
- Overlap between non-migrated and internal transfer groups confirms they're similar populations

## ⚠️ Known bug — Y-axis goes negative
**The Y-axis currently extends below 0**, which is physically impossible (age at death cannot be negative). This is a matplotlib autoscaling issue — the whiskers on the deported box or outliers are pulling the axis down.

**Fix needed:** Add `ax.set_ylim(bottom=0)` in `generate_analysis.py` for this chart.

This is a cosmetic bug but looks unprofessional in a paper and could confuse readers. Must fix before publication.
