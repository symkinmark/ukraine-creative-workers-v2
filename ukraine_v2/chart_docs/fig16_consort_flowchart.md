# Fig 16 — CONSORT-Style Dataset Exclusion Flowchart

**File:** `charts/fig16_consort_flowchart.png`

> ⚠️ **UPDATED FOR V2.2** — Numbers below reflect the corrected V2.2 dataset after fix_dates_v2.py recovered 8,971 previously-missing death years. Old V2.1 numbers were: 6,106 analysable (migrated:927 / non_migrated:4,625 / internal:479 / deported:75).

## What this chart shows
A flowchart showing how the dataset was built — how many entries were in the raw ESU scrape, how many were excluded at each step, and why. This is a standard requirement in medical/social science research (based on the CONSORT reporting standard for clinical trials).

The steps (V2.2):
1. ESU.com.ua scraped: **16,215** entries
2. Excluded pre-Soviet deaths (died <1921): −371; Galicia pre-1939: −89
3. Excluded confirmed non-Ukrainian: −5
4. Excluded still-alive or unknown status: −6,680 alive, −197 unknown
5. Excluded bad/impossible dates: −43
6. **Final analysable dataset: 8,830** (+45% vs V2.1)
   - Migrated: 1,305 | Non-migrated: 6,157 | Internal transfer: 1,179 | Deported: 189

## Key finding
Of 16,215 scraped entries, **8,830 (54.5%)** are analytically usable — up from 37.7% in V2.1 due to date recovery from corrupted ESU bio-header parsing. The main exclusion reason is "still alive or unknown status".

## Why the dataset grew
V2.1 had a regex bug in the ESU scraper that caused 8,971 entries with Inner parens (`14(26). 04. 1890`) or pseudonym prefixes (`справж. – Name; 1887 – 1937`) to silently fail date extraction. fix_dates_v2.py recovered dates via bio-header analysis, recovering famous Executed Renaissance victims (Курбас, Зеров, Підмогильний, Бабель, Вороний) among many others.

## What to look for
- Each exclusion step is justified with a specific criterion
- The n numbers at each step should add up correctly
- The final box shows the four-group split — check these match fig01

## Why this chart matters
Transparency. Any reviewer will ask: "How did you go from 16,000 entries to 6,000?" This chart answers that before they have to ask. It's a sign of methodological rigour.

## Known issues / improvements
- Clean chart, no bugs.
- The Galicia pre-1939 exclusion could have a tooltip/footnote explaining why (Galicia was under Polish/Austrian rule pre-1939, not Soviet; different political context).
