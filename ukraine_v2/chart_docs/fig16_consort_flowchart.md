# Fig 16 — CONSORT-Style Dataset Exclusion Flowchart

**File:** `charts/fig16_consort_flowchart.png`

> **UPDATED FOR V2.3** — Numbers below reflect the corrected V2.3 dataset. V2.2 had 8,830 analysable (migrated:1,305 / non_migrated:6,157 / internal:1,179 / deported:189). Old V2.1 numbers were: 6,106 analysable (migrated:927 / non_migrated:4,625 / internal:479 / deported:75).

## What this chart shows
A flowchart showing how the dataset was built — how many entries were in the raw ESU scrape, how many were excluded at each step, and why. This is a standard requirement in medical/social science research (based on the CONSORT reporting standard for clinical trials).

The steps (V2.3):
1. ESU.com.ua scraped: **16,215** entries
2. Excluded pre-Soviet deaths (died <1921): −371; Galicia pre-1939: −89
3. Excluded confirmed non-Ukrainian: −5
4. Excluded still-alive or unknown status: −6,680 alive, −119 unknown (was −197 in V2.2; 77 reclassified via reclassify_unknowns.py + 1 manual)
5. Excluded bad/impossible dates: −62 (was −43; 19 impossible-age entries added in V2.3)
6. Excluded migration status corrections: −46 (entries moved from analysable groups to excluded_bad_dates or other)
7. **Final analysable dataset: 8,643** (−187 vs V2.2 due to V2.3 corrections)
   - Migrated: 1,280 | Non-migrated: 6,030 | Internal transfer: 1,150 | Deported: 183

## Key finding
Of 16,215 scraped entries, **8,643 (53.3%)** are analytically usable — down slightly from V2.2 (54.5%) because V2.3 applied corrections that excluded 187 entries with impossible ages or classification errors. The main exclusion reason is "still alive or unknown status".

## Why the dataset grew then shrank slightly
V2.1 had a regex bug in the ESU scraper that caused 8,971 entries with Inner parens (`14(26). 04. 1890`) or pseudonym prefixes (`справж. – Name; 1887 – 1937`) to silently fail date extraction. fix_dates_v2.py recovered dates via bio-header analysis (V2.2), recovering famous Executed Renaissance victims (Курбас, Зеров, Підмогильний, Бабель, Вороний) among many others.

V2.3 applied targeted corrections: 19 impossible-age entries (age_at_death < 10, dates clearly wrong) excluded; 77 unknown-status entries reclassified; 3 individual historical corrections (Куліш, Квітко, Маркіш). Net effect: 8,643 analysable — a small decrease from V2.2's 8,830.

## What to look for
- Each exclusion step is justified with a specific criterion
- The n numbers at each step should add up correctly
- The final box shows the four-group split — check these match fig01

## Why this chart matters
Transparency. Any reviewer will ask: "How did you go from 16,000 entries to 6,000?" This chart answers that before they have to ask. It's a sign of methodological rigour.

## Known issues / improvements
- Clean chart, no bugs.
- The Galicia pre-1939 exclusion could have a tooltip/footnote explaining why (Galicia was under Polish/Austrian rule pre-1939, not Soviet; different political context).
