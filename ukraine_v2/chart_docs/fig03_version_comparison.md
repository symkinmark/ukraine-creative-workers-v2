# Fig 03 — Version Comparison: V1 vs V2.1 vs V2.2

**File:** `charts/fig03_version_comparison.png`

## What this chart shows
How our main finding changed between study versions, using the same two-group framing (Migrated vs Stayed in Soviet Sphere) to keep comparisons fair.

## Key finding (updated for V2.2)
| | V1 (n=415) | V2.1 (n=6,106) | V2.2 (n=8,606) |
|---|---|---|---|
| Migrated LE | 72.0 yrs | 75.9 yrs | 75.26 yrs |
| Stayed LE | 63.0 yrs | 70.5 yrs | 70.61 yrs |
| Gap | +9.0 yrs | +5.4 yrs | **+4.66 yrs** |
| Cohen's d | — | ~0.374 | 0.332 |

The gap narrowed progressively as the dataset grew 15x (V1→V2.1) and then 40% more (V2.1→V2.2). V2.2 brought in 2,500 previously-missing entries whose death years were recovered from ESU biographical text — including most of the Executed Renaissance victims. The finding is more conservative and more representative with each version, but **has not disappeared at any sample size.**

## What to look for
- The gap narrowed but did **not** disappear — the finding is robust across all dataset sizes
- The V2.2 narrowing relative to V2.1 reflects adding long-lived non-migrants who were missed due to the ESU date parsing bug (their dates were in the text but not parsed)
- The "Stayed" group definition: non_migrated + internal_transfer + deported combined — collapses four-group model to two groups for V1 comparability

## Group definition note
"Stayed in Soviet Sphere" = non_migrated + internal_transfer + deported combined. This collapses the four-group model back to two groups for comparison with V1, which didn't have the four-way split. The four-group version is in fig01 and is the preferred framing for V2.2.

## Known issues / improvements
The chart was generated with V2.1 data only (two bars). It should be regenerated as three grouped bars (V1 / V2.1 / V2.2) to show the full progression.
