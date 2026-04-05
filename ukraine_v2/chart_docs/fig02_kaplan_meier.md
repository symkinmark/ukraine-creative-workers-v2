# Fig 02 — Kaplan-Meier Survival Curves

**File:** `charts/fig02_kaplan_meier.png`

## What this chart shows
A survival curve for each of the four groups. The Y-axis is the probability of still being alive at a given age; the X-axis is age. Each curve starts at 1.0 (100% alive at birth) and drops as people die.

This is a standard tool from medical research — same method used to compare cancer treatment outcomes. Here we're using it on historical mortality data.

## Key finding
The migrated group's curve stays higher for longer — they have a higher probability of surviving to any given age compared to the other groups. The deported group's curve drops earliest and steepest. The non-migrated and internal transfer curves sit in between, close to each other.

**V2.2 median survival ages:**
- Migrated: 77 yrs
- Non-migrated: 73 yrs
- Internal transfer: 72 yrs
- Deported: 45 yrs

## What to look for
- **Where curves diverge:** They start to separate around age 40-50. Below that, all groups had similar survival — the difference is in middle and old age.
- **Deported curve:** Drops steeply and early. Large portions of the deported group never reached their 60s. Median survival is 45 — half the group was dead before age 45.
- **Shaded bands:** The shaded region around each curve is the confidence interval. Wide band = less certainty (smaller group).
- **Median survival:** The age where each curve crosses 0.5 (50% probability) gives the median life expectancy.

## Known issues / improvements
- ~~"V1 avg (63)" annotation is outdated.~~ Update to V2.2 overall non-migrated median = 73 yrs, migrated median = 77 yrs.
- Consider adding a table of median survival ages per group below the chart.

## Technical note
Computed using the `lifelines` library (v0.30.3). Log-rank test was used to confirm statistical significance of differences between curves.
