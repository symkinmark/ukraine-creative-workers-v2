# Fig 08 — Deported Group: Deaths by Year (Line Chart)

**File:** `charts/fig08_deported_deaths_by_year.png`

## What this chart shows
A year-by-year count of deaths in the deported group only (V2.3: n=183). Shows the precise timing of when deportees died, which maps directly onto Soviet historical events.

## Key finding
**1937 is the single worst year by an enormous margin.** 65 of 183 deportees (35.5%) died in 1937 alone — the Stalinist Great Terror's peak. This is not a gradual rise; it's a cliff. The year 1938 saw the second worst death toll: 28 deaths (15.3%). Together, 1937-1938 account for ~51% of all deported deaths.

**Year-by-year top deaths (V2.3):**
| Year | Deaths | % of deported group |
|------|--------|---------------------|
| 1937 | 65 | 35.5% |
| 1938 | 28 | 15.3% |
| 1942 | 12 | 6.6% |
| 1941 | 9 | 4.9% |
| 1944 | 7 | 3.8% |

A secondary cluster appears during WWII (1941-45). After 1950, deaths drop to near-zero — the cohort is effectively gone.

## What to look for
- The 1937 spike — 36.5% of the entire group in a single year
- The 1938 spike — still 15.7%; this was not a one-day event but a sustained campaign
- Secondary peaks in 1941-1944 — WWII occupation and ongoing repression
- The flat zone before 1936 — historically accurate: large-scale deportations of Ukrainian cultural workers began in mid-1930s
- The flat zone after 1950 — the cohort is gone

## V2.3 note
The deported group grew from n=75 (V2.1) to n=183 (V2.3) after V2.2 date recovery + V2.3 corrections (Куліш death_cause fix + 5 newly reclassified unknown entries). The 1937 spike is now far more visible and historically accurate — most of the newly recovered entries are Sandarmokh massacre victims whose ESU dates had the nested-paren parsing bug.

The 1937 spike decreased slightly from 36.5% (V2.2, n=178) to 35.5% (V2.3, n=183) because the 5 new deported entries added in V2.3 died in years other than 1937.

## Known issues / improvements
- The wide blank region 1921-1935 could look like missing data. Consider adding a note: "No deportation deaths recorded pre-1936 — consistent with historical record."
- Add numeric labels to the 1937 and 1938 bars (65 deaths, 28 deaths).
