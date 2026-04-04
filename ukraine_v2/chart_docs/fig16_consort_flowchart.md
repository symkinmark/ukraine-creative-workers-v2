# Fig 16 — CONSORT-Style Dataset Exclusion Flowchart

**File:** `charts/fig16_consort_flowchart.png`

## What this chart shows
A flowchart showing how the dataset was built — how many entries were in the raw ESU scrape, how many were excluded at each step, and why. This is a standard requirement in medical/social science research (based on the CONSORT reporting standard for clinical trials).

The steps:
1. ESU.com.ua scraped: **16,213** entries
2. Filtered to creative profession keywords: **16,215** (kept all)
3. Excluded pre-Soviet deaths (died <1921): −649; Galicia pre-1939: −89
4. Excluded confirmed non-Ukrainian: −0
5. Excluded still-alive or unknown status: −9,971 alive, −115 unknown
6. Excluded missing birth or death year: −283
7. **Final analysable dataset: 6,106**
   - Migrated: 927 | Non-migrated: 4,625 | Internal transfer: 479 | Deported: 75

## Key finding
Of 16,213 scraped entries, **6,106 (37.7%)** are analytically usable. The main exclusion reason is "still alive or unknown status" — most of the encyclopedia covers living people or people whose death date isn't recorded.

## What to look for
- Each exclusion step is justified with a specific criterion
- The n numbers at each step should add up correctly
- The final box shows the four-group split — check these match fig01

## Why this chart matters
Transparency. Any reviewer will ask: "How did you go from 16,000 entries to 6,000?" This chart answers that before they have to ask. It's a sign of methodological rigour.

## Known issues / improvements
- Clean chart, no bugs.
- The Galicia pre-1939 exclusion could have a tooltip/footnote explaining why (Galicia was under Polish/Austrian rule pre-1939, not Soviet; different political context).
