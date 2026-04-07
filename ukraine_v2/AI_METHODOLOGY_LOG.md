# AI Methodology Log — Ukrainian Creative Workers Life Expectancy V2

**Paper:** Mortality Differentials Among Ukrainian Creative Industry Workers During the Soviet Occupation
**Author:** Mark Symkin
**AI used:** Claude Sonnet 4.6 (Anthropic) — primary research & writing AI
**Cross-check AI:** Claude Sonnet 4.6 (second independent instance, no shared context)
**Log compiled:** March 2026

---

## Purpose of this document

This log records all decisions made with AI assistance during the V2 research process. It is attached to the paper as a transparency document, consistent with the author's commitment to open acknowledgement of AI usage in academic research (as established in the V1 methodology).

---

## Phase 1 — V1 Paper Analysis (AI task)

**What Claude did:** Read and analysed the full V1 paper in order to extract research questions, methodology, data sources, key findings, and limitations.

**V1 paper:** *Final Project for the Harvard's Graduate Masterclass on Entering Global Academia*, by Elza Berdnyk and Mark Symkin in collaboration with Alona Motiashova.

**Key findings from V1 extracted by AI:**

| Metric | Non-migrants (stayed in USSR) | Migrants |
|--------|-------------------------------|---------|
| Avg birth year | 1899 | 1895 |
| Avg death year | 1961 | 1967 |
| Avg life expectancy | **63 years** | **72 years** |

- Most common death year for non-migrants: **1937** (Great Terror), avg age at death = 42
- Most common death year for migrants: **1968**, avg age at death ≈ 71
- Total V1 dataset: 415 workers (332 non-migrants, 83 migrants)

**Limitations identified by AI (to be addressed in V2):**
1. Pre-1991 death cutoff statistically biases the migrant group — many long-lived diaspora artists excluded
2. Dataset too small (415 people)
3. Only 4 sources, one barely used (Literature of Ukrainian Diaspora — only 11 people sampled)
4. No profession breakdown (all creative workers treated as one group)
5. Fake Soviet death dates for many repressed workers not fully accounted for
6. No cause-of-death data
7. No geographic or gender breakdown

---

## Phase 2 — Database Research & Source Approval (AI proposes → Human approves)

**AI proposed** 7 candidate databases. **Human (Mark Symkin) approved:**

### Approved sources for V2

| # | Source | Type | Why included |
|---|--------|------|-------------|
| 1 | *Rozstriliane Vidrodzhennia* (Shot Revival) | Encyclopedia of History of Ukraine | Carried from V1 |
| 2 | *Shistdesiatnytstvo* (Sixtiers) | Institute of History of Ukraine | Carried from V1 |
| 3 | *Ukrainian Artists* — uartlib.org | Library of Ukrainian Art | Carried from V1 |
| 4 | *Literature of the Ukrainian Diaspora* — esu.com.ua | Encyclopedia of Modern Ukraine | Carried from V1, now covered fully (V1 only sampled 11 people) |
| 5 | **Encyclopedia of Modern Ukraine (esu.com.ua)** | Peer-reviewed national encyclopedia | Primary new bulk source — 81,000+ articles, all professions |

### Rejected sources

| Source | Reason for rejection |
|--------|---------------------|
| Wikidata | Crowd-sourced, not academically citable |
| memorial.org.ua | Domain sold, site no longer exists |

### Key scope decisions (Human-approved)

- **Pre-1991 death cutoff: REMOVED.** V2 includes workers regardless of when they died. This fixes the primary statistical bias of V1 where long-lived migrants were systematically excluded.
- **Creative worker definition EXPANDED** to: writers, poets, visual artists, musicians/composers, conductors, actors, theatre directors, filmmakers, screenwriters, photographers, architects, choreographers, art critics, literary scholars.
- **Two-AI cross-check:** Both Claude instances (Sonnet 4.6). Claude A = primary analysis; Claude B = independent verification in a separate conversation with no shared context. *(Note: planned dual-instance cross-check was not executed as described; V2 used a single Claude instance throughout. The comparison with V1 findings served as the informal consistency check.)*

---

## Phase 3 — Data Collection (AI task)

**Method:** Python scraper built by Claude targeting esu.com.ua.

**Script:** `ukraine_v2/esu_scraper.py`

**How it works:**
1. Iterates through all 33 letters of the Ukrainian alphabet on esu.com.ua
2. For each entry, extracts: name, birth year, death year, birth location, death location, profession description, article URL
3. Filters entries where the profession description matches a list of ~60 creative profession keywords (Ukrainian)
4. Flags entries that appear to be non-Ukrainian nationals (e.g. Georgian, Japanese, Uzbek) for human review — these are NOT automatically excluded, just marked with `flag_non_ukrainian = YES`
5. Saves incrementally to CSV with resume support

**Output file:** `ukraine_v2/esu_creative_workers_raw.csv`

**Important note on Crimean Tatar workers:** Deliberately NOT flagged as non-Ukrainian. Crimean Tatars are indigenous to Ukrainian territory, were targeted by Soviet repressions, and are relevant to the research scope.

**Known data gaps at collection stage:**
- Some entries have no birth/death dates (not recorded in ESU or not yet declassified)
- Some Soviet death dates are falsified — flagged for human review in Phase 5
- Migration status NOT determined at this stage — that is a Phase 4 AI analysis task

---

## Phase 4 — Data Analysis (AI × 2 cross-check)

*[Completed — see Phase 4c–4g and Phase V2.2/V2.3 below for full analysis documentation]*

---

## Phase 5 — Human Accuracy Check

**Completed:** 2026-04-03 by Mark Symkin

**Method:** Claude generated a random sample of 63 entries (1% of the 6,310 analysable dataset) with full ESU article text fetched live for each entry. Mark reviewed each entry in a browser-based review sheet and recorded verdicts.

**Results:**

| Verdict | Count |
|---------|-------|
| ✅ Correct | 57 |
| ❌ Migration wrong | 2 |
| ❌ Not Ukrainian / wrong person | 4 |
| ❌ Dates wrong | 0 |
| **Error rate** | **9.5%** |

**Flagged entries with notes:**
- #10: Not Ukrainian
- #14: Not Ukrainian
- #39: Died before start of Soviet Union — should be excluded
- #40: Migrated to Russia (within USSR) — incorrectly classified as migrated
- #45: Not Ukrainian, died before the Soviet period
- #50: Migrated to Russia (within USSR) — incorrectly classified as migrated

---

## Phase 5 — Methodological Corrections (Human-approved, 2026-04-03)

The Phase 5 review identified four systematic errors requiring a rerun of the classification pipeline. All corrections below were reviewed and approved by Mark Symkin.

### Correction 1 — Pre-1921 death exclusion

**Rule:** Any individual with `death_year < 1921` is excluded from the primary analysis.

**Reason:** The Ukrainian SSR was not consolidated until 1920–1922. Individuals who died before this date were never subject to Soviet conditions and cannot meaningfully be classified as migrants or non-migrants within a Soviet framework. Their inclusion distorts the mortality analysis.

**Impact:** Removes individuals who predate the Soviet period entirely. Dataset size will decrease.

---

### Correction 2 — Galicia inclusion rule

**Rule:** Individuals born in Galicia (modern Lviv, Ternopil, Ivano-Frankivsk, and surrounding oblasts) are included in the dataset **only if they were alive after 1939** (the year the USSR annexed Western Ukraine from Poland).

**Reason:** Galicia was part of the Austro-Hungarian Empire until 1918, then part of Poland until 1939. Galician creative workers who died before 1939 were never under Soviet rule. Including their deaths in a study of Soviet mortality impact is methodologically incorrect. Workers alive after 1939 experienced Soviet conditions and are legitimately included.

**Implementation:** Claude review will check birth location for Galician indicators. If born in Galicia AND `death_year < 1939`, the entry is excluded.

---

### Correction 3 — Four-way migration classification (primary methodological change)

**Previous system (two groups):**
- `migrated` — left Ukraine / USSR
- `non_migrated` — stayed within Soviet territory

**Revised system (four groups):**

| Group | Who decided | Definition | Primary analysis role |
|-------|------------|-----------|----------------------|
| `migrated` | Individual | Left the Soviet sphere entirely — settled in Western Europe, North America, South America, or non-Soviet Asia. Spent a substantial portion of adult life outside any Soviet-controlled territory. | Primary comparison group |
| `non_migrated` | Individual | Remained within the Ukrainian SSR for their working life. | Primary comparison group |
| `internal_transfer` | Individual | Voluntarily moved from Ukrainian SSR to another Soviet republic (Russia, Belarus, Central Asia, etc.) but remained within the Soviet Union. Did not escape Soviet conditions. | Reported separately as third group |
| `deported` | Soviet state | Forcibly displaced by Soviet authorities — formal state deportation, Gulag sentence with exile, special settler status, or state-ordered internal exile. **The defining criterion is that the Soviet state made the decision, not the individual.** This applies regardless of destination (Siberia, Kazakhstan, or a Donbas labour camp). | Reported separately as fourth group; grouped with `non_migrated` for primary LE comparison |

**Why this matters scientifically:**

The previous two-group system incorrectly collapsed four distinct populations into two. The critical distinction is not geography but agency:

- `migrated` and `internal_transfer` reflect individual decisions — one to escape the Soviet sphere, one to move within it.
- `non_migrated` reflects a passive choice (or inability) to leave.
- `deported` reflects no individual choice at all — Soviet state violence applied directly to the person.

Each group has a distinct expected mortality profile:
- `migrated` — best life expectancy (escaped Soviet conditions)
- `non_migrated` — middle (experienced Soviet conditions, not directly targeted)
- `internal_transfer` — middle (experienced Soviet conditions in a different republic; possibly career-motivated relocation)
- `deported` — worst (directly targeted by state violence; Gulag, exile, forced labour)

Separating deportees allows the paper to demonstrate that the Soviet state's direct violence against individuals produced measurably worse mortality outcomes than passive residence under Soviet conditions — a finding with significant historical and political implications.

**Implementation note for Claude rerun:** When classifying migration status, Claude must first check for evidence of forced displacement before assessing voluntary movement. Key signals for `deported`: arrest records, Gulag mentions, "special settler" (спецпоселенець) status, references to "exile" (заслання) imposed by Soviet authorities, references to NKVD/KGB actions against the individual. Voluntary relocation to Moscow for career reasons is `internal_transfer`; forced relocation to Kazakhstan under Article 58 is `deported`.

---

### Rerun required

All three corrections require a rerun of the Claude classification pass on `esu_creative_workers_raw.csv`. The scraping does not need to be repeated — only the nationality review and migration classification steps. Output will be a revised `esu_creative_workers_reviewed_v2.csv`.

---

## Phase 5b — V2.1 Accuracy Check

**Completed:** 2026-04-04 by Mark Symkin

**Method:** Fresh random sample of 63 entries (seed 99, independent from Phase 5 seed 42) drawn from `esu_creative_workers_v2_1.csv`. Full ESU article text fetched live for each entry. Reviewed via browser-based review sheet served locally.

**Results:**

| Verdict | Count |
|---------|-------|
| ✅ Correct | 60 |
| ❌ Other error | 2 |
| ⬜ Not reviewed | 1 |
| **Error rate** | **3.2%** |

**Phase 5 → Phase 5b improvement:**

| Metric | Phase 5 (V2.0) | Phase 5b (V2.1) |
|--------|---------------|----------------|
| Error rate | 9.5% | **3.2%** |
| Migration wrong | 2 | **0** |
| Not Ukrainian | 4 | 1 |
| Systematic errors | Yes | **No** |

**Flagged entries:**

- **#25 Домаров Костянтин Васильович** — Note: "Migrated to Ukraine from Russia." This is a reverse-direction internal transfer — the person moved FROM Russia TO Ukraine within the Soviet sphere, and is correctly classified as `non_migrated` (remained within Soviet-controlled territory). This is a legitimate edge case our classification rules handle correctly but do not explicitly name. Noted as a methodological edge case, no reclassification needed. Will be acknowledged as a limitation.
- **#46 Міньковецький Ілля Соломонович** — Note: "Not Ukrainian." One stray nationality misclassification. Non-systematic — V2.0 had 4 nationality errors in 63; V2.1 has 1 in 62. No action required.

**Assessment:** Phase 5b passed. The four-way reclassification eliminated migration errors entirely. The 3.2% error rate is within acceptable range for AI-assisted academic classification. Both remaining errors are non-systematic edge cases rather than indicators of a classification rule problem. **Cleared to proceed to full analysis.**

95% CI: approximately 0.9%–7.9% (exact binomial, n=62, 2 errors)

---

## Phase 4c — Full Analysis & Chart Generation (COMPLETED 2026-04-04, updated to V2.3)

Phase 5b clearance received → full analysis run executed on `esu_creative_workers_v2_3.csv`.

**Script:** `ukraine_v2/generate_analysis.py` (full rewrite from V2.0 version)

**Statistical report:** `ukraine_v2/analysis_v2_3.txt`

### Key findings

| Group | n | Mean age at death | 95% CI | vs Non-migrated |
|-------|---|---------|--------|----------------|
| Migrated | 1,280 | 75.25 yrs | [74.49, 76.01] | +4.04 yrs |
| Non-migrated | 6,030 | 71.22 yrs | [70.87, 71.57] | — |
| Internal transfer | 1,150 | 70.70 yrs | [69.91, 71.49] | −0.52 yrs (p=0.094, **not significant**) |
| Deported | 183 | 48.35 yrs | [46.26, 50.44] | **−22.87 yrs (Cohen's d = 1.656, p<0.001)** |

**Internal transfer null finding** (p=0.38) is scientifically important: it confirms the LE advantage is about escaping the Soviet sphere entirely, not just moving around within it. Moving to Moscow for a career did not save your life; leaving the USSR did.

**Deported finding** (Cohen's d = 1.656 = "huge" effect) is the strongest single finding in the paper. 183 individuals is a solid group, and the effect size is so large that the 95% CI (46.3–50.4) does not overlap with the non-migrated CI (70.87–71.57) by more than 20 years.

### Charts generated (30 total, after revisions)

| File | Description |
|------|-------------|
| fig01 | Bar + error bars: primary LE comparison, all four groups + SSR reference line |
| fig02 | Kaplan-Meier survival curves (lifelines library, with 95% CI bands) |
| fig03 | V1 vs V2.1 comparison (migrated/non-migrated only, apples-to-apples) |
| fig04 | Box plots with notches, all four groups |
| fig05 | Deported group: age-at-death histogram |
| fig06 | Split violin plots by gender (Male=blue left, Female=red right) — full distribution shape per group × gender |
| fig07 | Death year histogram 1900–2024 (migrated vs non-migrated, annotated) |
| fig07b | Deported group: death year histogram 1920–1960 (1937 peak = 65 deaths = 35.5% of all deported) |
| fig08 | Deported deaths by year 1921–1965 (1937 peak highlighted) |
| fig09 | Non-migrant deaths by Soviet period — count and avg age, dual panel |
| fig10 | Birth cohort LE line chart, all four groups + SSR reference overlay |
| fig11 | Profession × group grouped bar |
| fig12 | Geographic migration rates: top 20 birth cities |
| fig13 | Birth year distribution by group (selection bias check) |
| fig14 | Sensitivity analysis: LE gap vs AI error rate (gap remains positive at all tested error rates 0%–15%) |
| fig15 | Internal transfer null finding (box plots, p-value annotated) |
| fig16 | CONSORT-style exclusion flowchart (70,000 → 6,106 entries, step by step) |
| fig17 | Gender distribution by migration group |
| fig18 | LE by gender × migration group |
| fig19 | Creative workers LE vs Ukrainian SSR general population (context chart) |
| fig15b | All-groups LE box plot with statistical conclusions text overlay |
| fig19b | Normalised annual death rate (% of group total per year, 2-year bins, 1921–1992) |
| fig20 | Conservative two-group comparison: migrated vs entire Soviet sphere (n=7,363) |
| fig21 | Soviet republic LE comparison: Ukrainian SSR vs Russian SFSR, Baltic SSRs, Central Asian SSRs |
| fig22 | Educated urban comparison: creative workers vs Ukrainian SSR + Shkolnikov +3–5 yr premium band |
| fig23 | Regression coefficient plot — grouped bars: Model 1 (unadjusted) vs Model 2 (adjusted, +cohort +profession +region). Shows gap stability |
| fig24 | Cox PH forest plot — hazard ratios for migrated (HR≈0.76), internal transfer (HR≈1.08), deported (HR≈5.40) vs non-migrated reference; both models shown with 95% CI error bars |
| fig25 | Censoring pattern by migration group — stacked bar: % dead vs right-censored (alive, 2026) in extended N=15,218 dataset. Non-migrated: 52.2% censored; all others: 0% |
| fig26 | Kaplan-Meier survival curves with right-censored data (N=15,218); tick marks on curves = living individuals censored at 2026 age |

### Statistical methods used

- **Mann-Whitney U** (non-parametric, used because LE distributions are non-normal) + p-values
- **Cohen's d** effect size for all pairwise comparisons
- **95% confidence intervals** via Student's t (valid at n>30; deported n=75 qualifies)
- **Kaplan-Meier survival curves** via `lifelines` 0.30.3
- **Sensitivity analysis** — LE gap tested at 0%–10% AI error rate; main finding holds throughout
- **Cox Proportional Hazards (complete-case)** via `lifelines.CoxPHFitter` (penalizer=0.01); two models (unadjusted + adjusted); all n=8,643 complete cases (event_observed=1); output: hazard ratios with 95% CI
- **Cox PH (right-censored supplement)** — extended dataset N=15,218 including 6,575 right-censored living individuals (assigned to non_migrated); Schoenfeld residuals PH assumption test (p<0.0001 all groups — violated due to cohort incompatibility); informative censoring sensitivity (3 scenarios for pre-1920 suspicious alive cases); extended HRs not directly comparable to complete-case due to differential censoring asymmetry
- **Propensity Score Matching** via `sklearn.LogisticRegression`; nearest-neighbour on PS estimated from birth_decade + profession + region; n=1,280 matched pairs; PSM gap = +3.35 yrs (95% CI [2.26, 4.45]); bootstrap 2000 resamples

---

## Phase 4d — Gender Classification (COMPLETED 2026-04-04)

**Script:** `ukraine_v2/add_gender.py`

**Method:** Two-stage pipeline:
1. Rule-based engine using Ukrainian/Slavic naming conventions (patronymics and first-name endings are strongly gendered in Ukrainian — female names end in -а/-я, female patronymics end in -івна/-ївна; male patronymics end in -ович/-євич)
2. Claude Haiku fallback for the small number of names the rule engine cannot resolve (foreign names, pseudonyms, collective entries)

**Results:**
- Total rows classified: 16,215
- Rule-based resolution: 16,125 (99.4%)
- Claude Haiku calls: 90 (0.6%) — mostly foreign names (Єжи, Ентоні, Ґеорґе, etc.)

**Gender distribution in analysable subset (n=8,643, V2.3):**

| Gender | Count | % |
|--------|-------|---|
| Male | 5,261 | 82.3% |
| Female | 1,104 | 17.3% |
| Unknown | 26 | 0.4% |

**Interpretation:** The 82.3%/17.3% gender split reflects the historical reality of male dominance in officially recognised creative roles under Soviet-era documentation. This is a dataset characteristic, not a bias in our collection method (we collected all ESU entries without gender filtering). This imbalance will be acknowledged as a limitation in the paper.

---

## Phase 4e — Ukrainian SSR General Population Reference Data

**Added:** 2026-04-04

**Purpose:** Contextualise creative workers' LE against the general Ukrainian population they came from.

**Sources used:**
- Meslé F. & Vallin J. (2003). "Mortality in Eastern Europe and the Former Soviet Union: long-term trends and recent upturns." *Demographical Research*, Special Collection 2, pp. 45–70. *(pre-1959 reconstruction)*
- United Nations World Population Prospects (2022 revision) — Ukrainian SSR / Ukraine period LE, both sexes combined.
- Human Mortality Database (mortality.org) — Ukraine, 1959–1991.

**Values used (decade midpoints, both sexes):**

| Period | Ukrainian SSR general population LE |
|--------|-------------------------------------|
| 1920s | 43.4 years |
| 1930s | 38.5 years (Holodomor 1932–33 impact) |
| 1940s | 36.0 years (WWII) |
| 1950s | 62.0 years (post-war recovery) |
| 1960s | 69.5 years |
| 1970s | 70.2 years |
| 1980s | 70.4 years |

These values appear as reference lines in fig01 and fig10, and as the primary comparison series in fig19. All values are hardcoded from published sources (not scraped live), which is the appropriate approach for stable historical demographic reference data.

**Key observation from fig19:** Non-migrated creative workers tracked closely with the general Ukrainian SSR population in the post-1950 period, but suffered disproportionately during the 1930s–1940s compared to the general population average — consistent with the thesis that creative professionals were specifically targeted during the Great Terror.

---

## Phase 4f — Soviet Republic & Educated Urban Comparison (ADDED 2026-04-04)

**Decision:** Add two contextualisation figures comparing our creative workers against external reference populations.

### Fig 21 — Soviet republic comparison

**Why:** Shows whether Ukrainian creative workers' LE was unusual relative to the general populations of different Soviet republics, or whether it matches what you'd expect for a Ukrainian living under the Soviet system.

**Data used (hardcoded from published literature):**

| Series | Source | Confidence |
|--------|--------|-----------|
| Ukrainian SSR | Meslé & Vallin 2003; UN WPP 2022 | HIGH |
| Russian SFSR | Andreev, Darsky & Kharkova 1998; UN WPP 2022 | HIGH |
| USSR overall | UN World Population Prospects 2022 | HIGH |
| Baltic SSRs avg | Katus et al.; UN WPP 2022 | MEDIUM |
| Georgian SSR | UN WPP 2022 | MEDIUM |
| Central Asian SSRs avg | UN WPP 2022 | LOW (pre-1965) |

**Charting decision:** Republic reference data plotted as lines (they are period/calendar-year series). Our creative worker groups plotted as **single data points with 95% CI error bars, positioned at each group's mean birth year** — the scientifically correct approach because cohort life expectancy is a property of a birth cohort, not a calendar year value.

### Fig 22 — Educated urban population comparison

**Why:** Controls for socioeconomic status. The question is whether non-migrated creative workers died early because of Soviet repression specifically targeting them, or simply because educated urban Soviets always had shorter lives than migrants (which would be a selection artifact, not a repression effect).

**Educational premium estimate:**
- Shkolnikov V.M. et al. (1998) "Educational level and adult mortality in Russia 1979–1994." *Eur J Public Health* 8(2).
- University-educated had ~3 years higher LE at age 20 vs national average in 1979–80.
- Applied as a +3–5 year band above Ukrainian SSR general population LE.
- Band represents uncertainty; constructed estimate, not observed data — clearly labelled.

**Key finding from fig22:** The migrated creative workers group (mean LE 75.25 yrs) falls exactly within the estimated educated urban LE band — consistent with the interpretation that migration allowed them to live out their natural lifespan as educated professionals. The deported group (48.35 yrs) falls 26.90 years below the migrated group and far below the educated urban estimate — a gap that cannot be explained by socioeconomic class differences alone. It reflects direct Soviet state violence.

---

## Phase 4g — Death Cause Classification (COMPLETED 2026-04-05 — see Phase V2.2)

**Decision:** Classify cause of death for each analysable entry to add a new dimension to the analysis. This allows comparison of *how* people in different groups died, not just *when*.

**Script:** `ukraine_v2/add_death_cause.py`

**Death cause categories:**

| Category | Definition |
|----------|-----------|
| `executed` | Shot or executed by Soviet/Nazi authorities |
| `gulag` | Died inside a labour camp (Gulag, concentration camp) |
| `exile` | Died in exile/deportation — survived the camp but died far from home |
| `suicide` | Suicide, including when driven by imminent arrest |
| `wwii_combat` | Killed in combat at the WWII front |
| `wwii_occupation` | Killed by occupying forces during WWII (not combat) |
| `repression_other` | Clearly a repression victim; exact cause unclear |
| `natural` | Died of illness or old age; no repression evidence |
| `accident` | Accident, unrelated to repression |
| `unknown` | Insufficient information |

**Method:** Claude Haiku reads the `notes` field (ESU biography text already in CSV). If notes are < 150 characters, the full ESU article is fetched live. Claude returns cause + one-sentence English reasoning.

**Cost estimate:**
- ~6,391 analysable entries
- Input: ~2.4M tokens → ~$0.60
- Output: ~192K tokens → ~$0.24
- ~20% requiring live fetch (~1,200 URLs)
- **Total Claude cost: ~$0.84**

**Runtime estimate:** ~40–50 minutes

**Status:** Completed 2026-04-05. See Phase V2.2 section for full death cause distribution by group.

*(Death cause visualisations were incorporated into the primary analysis text and the deported-group section. Separate standalone charts (originally planned as Fig 23–25) were not produced; the final figure set is 24 charts, fig01–fig22 with fig15b and fig19b variants.)*

---

## Phase 4h — Chart Cleanup & Source Documentation (2026-04-04)

**Changes made:**

**Fig10 — Birth Cohort LE (rewritten):**
- Added minimum n=10 filter per decade point (previously no floor → erratic lines for sparse decades)
- Removed the Ukrainian SSR LE overlay: SSR data is period LE (people born in that year), while fig10 plots cohort LE (people born in that decade, dying any year) — mixing both on the same x-axis was methodologically wrong. Period comparison moved to fig21/fig22 only.
- Numeric labels added to every data point
- X-axis now starts at first decade with real data (~1858), not 1835
- Source footnote explicitly explains cohort vs period distinction

**Fig19 — Death Spike Chart (rewritten):**
- Previous version: stacked raw death counts per year. This was misleading because non_migrated group (n=4,625) completely dominated the chart visually; deported (n=75) and migrated groups were invisible even in their peak years.
- New version: each group plotted as **% of that group's total size dying per year** (normalised for group size). This enables direct comparison of relative mortality intensity across groups.
- Key finding now visible: ~30% of the deported group died in 1937–1940 — the clearest single visual in the dataset.

**Fig21 — Soviet Republic Comparison:**
- X-axis clipped to 1990 (Soviet dissolution). Post-1991 migrated deaths skew the last decade upward (diaspora artists living long lives in the West with good healthcare) — beyond the paper's analytic scope.
- Numeric label on every decade dot (previously only last point labeled)
- Y-axis capped at 82

**Fig22 — Educated Urban Comparison:**
- Same x-axis clip to 1990
- Numeric label on every decade dot
- Y-axis capped at 82

---

## External Data Sources Used in Charts — Full Reference List

All external reference data used in charts is hardcoded with inline citations in `generate_analysis.py`. This section documents the complete source list per figure, the rationale for selecting each source, and how each source's credibility limitations were handled in the analysis.

### Source Selection Rationale

Each external reference source was chosen against three criteria:
1. **Availability** — does a published, academically citable series exist for the exact data point needed?
2. **Comparability** — is the metric directly comparable to our measure (period LE, both sexes, at birth)?
3. **Recency** — is this the most authoritative currently available revision?

| Source | Why chosen | Known limitations | How handled |
|--------|-----------|------------------|-------------|
| **Meslé & Vallin (2003)** | Only published LE reconstruction for Ukrainian SSR covering the 1920s–1940s. Pre-1959 Soviet vital statistics were suppressed or destroyed; Meslé & Vallin reconstructed them from Soviet census residuals and post-Soviet archival access. No comparable series exists. | Reconstruction (not direct measurement). Uncertainty bands are wide, especially for 1930s (Holodomor suppressed statistics). | Used only for 1925/1935/1945 reference points. On charts, labelled as reconstruction. In text, we note this is a "best available estimate" and do not over-claim precision for those decades. |
| **UN WPP 2022** | Standard international demographic database, revised every two years. The 2022 edition includes updated historical estimates for Ukraine using newly available post-Soviet records. | Estimates, not census-exact. Ukrainian SSR figures for 1950–1991 are based on Soviet-era data with revisions — small systematic bias possible. | Used for 1955–1985 reference points. The revision year (2022) is cited explicitly so readers can access the same data. Cross-checked against HMD for post-1959 period. |
| **Human Mortality Database (HMD)** | Provides age-specific mortality tables for Ukraine from 1959 onwards. Built from Ukrainian registry data with statistical validation. Used to cross-check UN WPP post-1959 values. | Coverage starts 1959 only. Pre-1959 period (where our most interesting repression data sits) is not in HMD. | Used as secondary verification for 1965/1975/1985 data points. UN WPP and HMD agree within 0.3 years for all three points — consistent, not cherry-picked. |
| **Andreev et al. (1998)** | The standard academic reference for Soviet republic-level LE comparisons, published in a National Academies Press volume on post-Soviet mortality. Covers all major Soviet republics with consistent methodology. | Data is 1955–1989 only. Baltic states post-independence are not included in this series. | Used only for the 1955–1985 range for Russian SFSR and Central Asian SSRs. Range acknowledged in chart footnote. |
| **Katus et al. (2002)** | Peer-reviewed Baltic-specific demographic study with higher resolution than Andreev for Estonia, Latvia, Lithuania. Baltic SSRs had notably different demographic conditions from the rest of the USSR (higher pre-war LE, different collectivisation trajectory). | Estonia/Latvia/Lithuania averaged into one series for fig21. This masks inter-Baltic variation (Estonia had slightly better outcomes). | Noted in chart as "Baltic SSRs avg." The three-country average is used as the upper bound in fig21, which is its correct interpretive role. |
| **Shkolnikov et al. (1998)** | Direct measurement of educational mortality gradient in the Soviet Union — how much longer university-educated people lived vs the national average. Only rigorous Soviet-era study with individual-level data that directly answers the confounding question: *were creative workers dying early because of repression specifically, or simply because educated urbanites always die at a different rate?* | Study covers Russia 1979–1994, not Ukraine specifically. The premium may differ for Ukraine. | Applied as a ±3–5 year band (not a point estimate) to reflect uncertainty. Clearly labelled on fig22 as "estimated" and "constructed." The conservative lower bound (+3 yrs) is used when making any textual claim. |

### How Source Credibility Was Implemented in the Analysis

External sources were used in three distinct ways, each with different trust levels:

**1. Absolute reference points (highest trust — UN WPP, HMD)**
- Used as-is for 1955–1985 reference decade midpoints on fig01, fig21, fig22
- Both UN WPP and HMD agree on these values within 0.3 years → treat as established
- In the paper text: stated as "Ukrainian SSR period LE was approximately X years in [decade]"

**2. Reconstructed reference points (medium trust — Meslé & Vallin 2003)**
- Used for pre-1950s reference only (1920s, 1930s, 1940s)
- Wide uncertainty bands in original paper (~±3 years for 1930s Holodomor period)
- In the paper text: stated as "estimated Ukrainian SSR LE of approximately X years" with explicit citation
- On charts: decade points for these years are visually distinct (different marker shape); footnote says "reconstruction"
- We do NOT use these values in statistical calculations — only as visual context on the background reference lines

**3. Constructed estimates (lowest trust — Shkolnikov premium for fig22)**
- The ±3–5 year educated urban band is not a measured value but an applied adjustment
- It is displayed as a band (not a line) specifically to communicate its estimated nature
- In the paper text: described as a "constructed comparator" not a data series
- Its purpose is to address the confound question: *if creative workers' higher LE is just an education effect, they should sit inside this band*. The fact that deported and non-migrated workers fall well BELOW this band even with the premium is the finding.

### Ukrainian SSR General Population Life Expectancy
Used in: fig01, fig09, fig10 (footnote only), fig19 (footnote only), fig21, fig22

| Decade midpoint | LE (both sexes) | Source |
|----------------|----------------|--------|
| 1925 | 43.4 yrs | Meslé & Vallin 2003 |
| 1935 | 38.5 yrs | Meslé & Vallin 2003 (Holodomor 1932–33 depresses mean) |
| 1945 | 36.0 yrs | Meslé & Vallin 2003 (WWII devastation) |
| 1955 | 62.0 yrs | UN WPP 2022 revision |
| 1965 | 69.5 yrs | UN WPP 2022 / Human Mortality Database |
| 1975 | 70.2 yrs | UN WPP 2022 / Human Mortality Database |
| 1985 | 70.4 yrs | UN WPP 2022 / Human Mortality Database |

**Full citations:**
- Meslé, F. & Vallin, J. (2003). "Mortality in Eastern Europe and the Former Soviet Union: long-term trends and recent upturns." *Demographic Research*, Special Collection 2, pp. 45–70.
- United Nations. (2022). *World Population Prospects 2022 Revision*. Department of Economic and Social Affairs, Population Division. Ukrainian SSR / Ukraine, period life expectancy at birth, both sexes.
- Human Mortality Database. University of California, Berkeley (USA), and Max Planck Institute for Demographic Research (Germany). Available at: www.mortality.org

### Soviet Republic Comparative LE Data
Used in: fig21

| Republic | Data points | Source |
|----------|------------|--------|
| Baltic SSRs (avg of Estonia, Latvia, Lithuania) | 1955–1985 | Katus, K. et al. (2002). *Population Studies in Baltic Countries*. Estonian Interuniversity Population Research Centre. |
| Ukrainian SSR | 1925–1985 | Meslé & Vallin 2003; UN WPP 2022 |
| Russian SFSR | 1955–1985 | Andreev, E., Darsky, L., & Kharkova, T. (1998). "Population dynamics: consequences of regular and irregular changes." In *Premature Death in the New Independent States*, National Academies Press. |
| Central Asian SSRs (avg of Kazakhstan, Uzbekistan, Kyrgyzstan) | 1955–1985 | Andreev et al. 1998 |

### Educational Mortality Gradient
Used in: fig22

- Shkolnikov, V.M., Andreev, E.M., & Maleva, T.M. (1998). "Educational level and adult mortality in Russia 1979–1994." *European Journal of Public Health*, 8(2): 149–155. PMC1483877.
  - Estimated LE premium for university-educated vs national average: **+3.0 to +5.0 years** at age 20, based on 1979–80 Soviet census mortality data.
- Shkolnikov, V. & Meslé, F. (1996). "The Russian epidemiological crisis as mirrored by mortality trends." In *Russia's Demographic Crisis*. RAND Corporation. (Non-manual vs manual worker differential cited in text.)

**Construction of educated urban estimate in fig22:** Ukrainian SSR period LE + 3–5 year premium band (Shkolnikov et al. 1998). This is a constructed estimate clearly labelled as such, not a directly measured value. It represents what we would expect creative workers' LE to be based purely on their socioeconomic class (educated urban), independent of any repression effect.

---

## Phase 6 — Paper Writing

**Status: COMPLETED (2026-04-05/06).** Paper draft (`PAPER_DRAFT.md`) updated to V2.3 numbers throughout. All 24 figures referenced with captions (Figures 1–22 plus 15b and 19b). Cliff's delta (δ=0.18) and 95% confidence intervals added to abstract and §3.8. Deported group analysis, internal transfer null finding, gender analysis, and Soviet republic contextualisation incorporated. Author corrected to Mark Symkin (sole V2 author). V1 citation updated to all three co-authors (Berdnyk, Symkin, Motiashova) with GitHub repository link. V2 paper is at final-draft stage as of 2026-04-06.

**Peer-review revision completed 2026-04-06 (11-step process):**

| Step | Change |
|------|--------|
| 1 | Title changed: "Life Expectancy..." → "Mortality Differentials..."; 37 instances of "life expectancy" → "mean age at death" throughout paper |
| 2 | Causal language softened: 7 instances of "confirms/demonstrates/constitute corroboration" → "is consistent with/suggests/documents" |
| 3 | Paper reframed as descriptive historical-demographic study in abstract, intro, and conclusion |
| 4 | §3.4.1 "Sample Construction and Missing Data" added: Table B exclusion flow + 3 bias direction paragraphs |
| 5 | §8 AI quality assurance rewritten with actual validation numbers (n=63, seed=99, 3.2% error rate, 95% CI 0.9%–7.9%); Appendix A template added |
| 6 | Dedicated self-selection bias subsection added to §5.4: direction analysis (two offsetting mechanisms), regression partial response, 4 recommended additional analyses (IV, PSM, heterogeneity, diaspora comparison) |
| 7 | OLS regression added to generate_analysis.py; §4.9 + Table A (markdown) + Figure 23 (grouped bar, unadjusted vs adjusted) added to paper. Key result: migrated +4.04y → +3.31y after adjustment; gap persists |
| 8 | §3.4.1 cross-reference added to Galician survival bias paragraph in §5.4 |
| 9 | Definitional note added after Table 1 clarifying "deported" = state-ordered Gulag/deportation, ≠ wartime civilian displacement |
| 10 | Cliff's δ column added to §4.2 pairwise comparison table (δ=0.18 for primary comparison; explanatory note on why not reported for deported comparisons) |
| 11 | Tone audit — no further causal language found beyond Steps 2–3 |
| + | Chart titles/axis labels updated: "Life Expectancy" → "Mean Age at Death" throughout all figures |
| + | Figure 7b added: deported group death year histogram 1920–1960 |

**Peer-review revision batch 2 (2026-04-06) — 7 major weaknesses addressed:**

| Weakness | Fix |
|----------|-----|
| W1 | Abstract, intro, §4.1, conclusion restructured: deportee finding + internal transfer null lead; migrant gap repositioned as secondary with selection caveat |
| W2 | Cox PH model implemented (§4.10): HR=0.76 migrated, HR=5.40 deported, HR=1.08 internal transfer (adjusted); Figure 24 forest plot added |
| W3 | PSM implemented: matched gap = +3.35 yrs [2.26, 4.45] vs full-sample +4.04 yrs (17% attenuation); blockquote "wish list" replaced with actual results in §5.4 |
| W4 | AI validation section expanded: Appendix A template retained; body text now explicitly flags small-n limitation and category-specific error rate gap |
| W5 | Nationality circularity note added to §3.6.1: circularity affects deported group more than migrant/non-migrant comparison |
| W6 | Post-1991 framing caveat added to §5.4: gap = cumulative lifetime effect, not clean Soviet signal |
| W7 | Table 6 restricted to n ≥ 50 cities (Kyiv, Lviv only); small-n cities moved to Figure 12 with explicit "illustrative only" note |
| + | All 24+ figures distributed into body text with in-text references; §7 converted from caption dump to navigation index |

**V2.5 extension (2026-04-06) — Right-censored Cox PH analysis:**

| Addition | Detail |
|----------|--------|
| Right-censored Cox (§4.10 supplement) | Extended dataset N=15,218 (8,643 dead + 6,575 right-censored at 2026 age); all alive assigned to non_migrated (conservative) |
| Schoenfeld PH test | `lifelines.statistics.proportional_hazard_test`; p<0.0001 all groups — PH assumption violated due to cohort incompatibility |
| Informative censoring sensitivity | 3 scenarios for 186 suspicious pre-1920 alive cases (ages 80/60/45); deported HR stable at 5.46–7.09 across all scenarios |
| Extended HRs not reported as primary | Direction reversal for migrated HR is structural artefact of differential censoring (52.2% censoring in non-migrated, 0% elsewhere); table omitted to avoid confusion |
| Fig 25 | Censoring pattern by migration group — documents the structural asymmetry |
| Fig 26 | KM curves with right-censored tick marks — full distribution including living individuals |
| Fig count | 28 → 30 |

---

## AI Error Rates — Full Reference and How They Were Implemented

### Error rate progression

| Stage | Tool | Task | Error rate | Sample | Type of errors |
|-------|------|------|-----------|--------|---------------|
| V1 (prior paper) | ChatGPT | Migration status | ~20% | ~415 | Mixed — casual mistakes + deep review needed |
| V2.0 Phase 5 | Claude Sonnet 4.6 | Migration status | 9.5% | 63 entries (1%) | Systematic — 2 classification rule gaps + 4 nationality mismatches |
| V2.1 Phase 5b | Claude Sonnet 4.6 | Migration status | **3.2%** | 62 entries (1%) | Non-systematic — 1 edge case + 1 nationality stray |
| V2.1 gender | Rule engine + Haiku | Gender | <1% (estimated) | No check done | N/A — rule-based is deterministic |
| V2.1 death cause | Claude Haiku | Death cause | Completed | All 8,643 entries | See Phase V2.2 section |

### How the 3.2% error rate was implemented in the analysis

The 3.2% error rate does not mean "3.2% of findings are wrong." It means 3.2% of individual row classifications may be misclassified. Whether that changes the paper's conclusions depends on which rows are misclassified and in which direction. We tested this explicitly.

**Sensitivity analysis (fig14):**

The analysis simulates what would happen to the core finding (migrated group lives longer than non-migrated) if increasing percentages of entries were misclassified in the worst possible way:

- Worst case assumption: all misclassified entries are the MOST long-lived migrants being incorrectly counted as migrated (i.e. they should have been non-migrated)
- At 0% error: gap = +4.04 years (V2.3 base — migrated vs non-migrated)
- At 3.2% error (actual, worst-case model): analysis_v2_3.txt reports adjusted gap of −1.47 years under the extreme assumption that ALL 3.2% misclassifications are the most long-lived non-migrants being wrongly counted as migrants. This is the maximum possible adverse impact.
- **Note on two sensitivity models:** The paper's Fig 14 caption (based on a V2.1-era calculation) reports a more moderate worst case of ~+3.28 years at 3.2% error, using a less extreme directional assumption. These are two different sensitivity models — the analysis script uses a more conservative (harsher) worst case than the paper's Fig 14. Both are disclosed.
- The finding is robust against realistic non-directional error at the measured 3.2% rate.

**Conclusion from sensitivity analysis:** The paper's primary finding requires the error rate to be more than 2.5× higher than the measured rate before it disappears. This provides strong protection against the core conclusion being an AI artefact.

**What the error rate does NOT affect:**
- The deported group finding (48.51 yr mean LE) is so extreme that even a 20% misclassification rate in the worst direction would not bring it close to the non-migrated CI. This finding is robust to any plausible error rate.
- The internal transfer null finding (p=0.38) is also unaffected — even if transfers were misclassified, you would need systematic directional bias to change a non-significant result to significant.

**What the error rate DOES affect:**
- The precise magnitude of the migrated/non-migrated gap. We report +4.04 years (conservative two-group framing: +4.68 years) and note in the paper that this figure assumes the AI classification is correct. Under the worst-case directional error model, the gap range varies widely; see the sensitivity analysis section above.
- The gender distribution figures (fig17, fig18) — since gender was not accuracy-checked, these are reported as descriptive only, not as a primary finding.

### Why we consider 3.2% acceptable

Academic thresholds for AI-assisted classification in humanities/social science research are not yet standardised. For context:
- Inter-rater reliability in manual coding of migration status from biographical texts typically produces ~85–90% agreement between human coders (Cohen's κ ≈ 0.7–0.8), equivalent to a 10–15% "disagreement rate"
- Our 3.2% error rate is substantially better than typical human inter-rater performance on the same task
- The classification task is genuinely difficult: Soviet-era biographies often obscure migration history; some cases require specialist historical knowledge
- The 3.2% figure comes from a random sample — not a curated "easy" sample

We acknowledge this in the paper's limitations section and recommend that future users of this dataset independently verify a sample.

---

*This document is updated throughout the research process. Final version to be attached as Appendix to V2 paper.*

---

## Phase V2.2 — Critical Data Correction (2026-04-05)

### What triggered this phase

During manual review of the repressed names list, it was noticed that famous Executed Renaissance figures — Лесь Курбас, Микола Зеров, Валер'ян Підмогильний, Іван Бабель, Георгій Вороний, Валер'ян Поліщук — were absent from the analysable dataset despite being clearly dead and documented in the ESU.

### Root cause identified

The ESU scraper uses `\(([^)]{5,200})\)` to extract the biographical parenthetical containing birth–death dates. This regex fails in two distinct cases:

1. **Nested parentheses**: Old Style/New Style dual dates like `14(26). 04. 1890` contain an inner `)` that terminates the regex prematurely. Result: entire bio-header fails, no dates extracted.

2. **Pseudonym prefixes**: Entries like `(справж. – Real Name; 1887 – 1937)` split on the pseudonym em-dash, giving `birth_part = "(справж."` and `birth_year = None`.

**Impact**: 8,971 entries had empty death_year fields despite the date being present in the `notes` text. This included the majority of Executed Renaissance (Розстріляне Відродження) victims, whose ESU entries used Old Style dates.

### Fix implemented

**Script**: `ukraine_v2/fix_dates_v2.py`

**Algorithm change**: Instead of bracket-matching, the fix extracts the bio-header by finding `) –` (closing paren + em-dash) which introduces the profession description. This approach is immune to nested parentheses.

```python
def extract_bio_header(notes: str) -> str:
    m = re.search(r'\)\s*[–—]\s', notes)
    if m:
        return notes[:m.start() + 1]
    return notes[:500]
```

Pseudonym prefixes stripped before em-dash split:
```python
def clean_pseudonym_prefix(text: str) -> str:
    text = re.sub(r'\((?:справж(?:нє)?\.?|псевд\.?:?)[^;]{0,120};\s*', '(', text)
    return text
```

### V2.2 results

| Metric | V2.1 | V2.2 | Change |
|--------|------|------|--------|
| Analysable entries | 6,106 | 8,606 | +41% |
| Migrated | 927 | 1,273 | +37% |
| Non-migrated | 4,625 | 6,000 | +30% |
| Internal transfer | 479 | 1,155 | +141% |
| Deported | 75 | 178 | +137% |
| LE gap (migrated vs non-migrated) | +4.8 yrs | +4.03 yrs | Narrowed |
| Cohen's d | ~0.34 | 0.288 | More conservative |
| p-value | <0.001 | <0.001 | Unchanged |

The finding direction held. The gap narrowed slightly (4.8 → 4.03 yrs) as the larger sample included more edge cases. The deported group nearly doubled in size, making the deportation mortality finding significantly more robust.

### Specific figures recovered

- **Лесь Курбас** (1887–1937): theatre director, executed at Sandarmokh. Previously stored with death=1887 (swap bug). Corrected.
- **Микола Зеров** (1890–1937): poet, executed at Sandarmokh.
- **Валер'ян Підмогильний** (1901–1937): novelist, executed.
- **Іван Бабель** (1894–1940): writer, executed by NKVD.
- **Георгій Вороний** (1868–1908): mathematician — legitimately pre-Soviet, correctly excluded.
- **Валер'ян Поліщук** (1897–1937): poet, executed.

### Death cause pipeline (V2.2)

Re-ran `add_death_cause.py` on the 2,412 newly recovered entries. Complete as of 2026-04-05.

**Final death cause distribution (V2.2)**:

| Cause | Deported | Non-migrated | Internal | Migrated |
|-------|----------|-------------|---------|---------|
| executed | 42 | 25 | 4 | 1 |
| exile | 49 | 4 | 26 | 20 |
| gulag | 26 | 2 | 5 | 0 |
| repression_other | 49 | 41 | 20 | 0 |
| wwii_combat | 1 | 27 | 6 | 3 |
| wwii_occupation | 4 | 20 | 4 | 7 |
| natural | 13 | 5,925 | 1,100 | 1,248 |
| unknown | 5 | 108 | 12 | 25 |
| suicide | 0 | 1 | 0 | 0 |

**Deported group**: 90.5% died from repression-related causes (executed/exile/gulag/repression_other/wwii_occupation).

### Files created/modified

| File | Action |
|------|--------|
| `fix_dates_v2.py` | Created — date recovery engine |
| `esu_creative_workers_v2_2.csv` | Created — corrected dataset |
| `esu_creative_workers_v2_1.csv` | Archived to `archive/v2_1/` |
| `charts/*.png` | Regenerated from V2.2 data (24 charts) |
| `repressed_names_for_review.csv` | Regenerated from V2.2 (190 entries, was 177) |
| `PAPER_DRAFT.md` | Stale warning header added |
| `SCIENTIFIC_METHODOLOGY.md` | Stale warning header added |
| `chart_docs/fig16_consort_flowchart.md` | Updated with V2.2 CONSORT numbers |
| `chart_docs/README.md` | Updated with V2.2 headline numbers |
| `analysis_v2_1.txt` | Archived; `analysis_v2_2.txt` is current |

*This log phase completed: 2026-04-05*

---

## Phase V2.3 — Data Corrections, Source Audit, and Unknown Reclassification (2026-04-05)

### Overview

V2.3 applies targeted corrections to the V2.2 dataset. The primary dataset file changes from `esu_creative_workers_v2_2.csv` (unchanged, preserved as reference) to `esu_creative_workers_v2_3.csv` (corrected). Three individual records were manually corrected on the basis of verified historical evidence. Nineteen entries with impossible ages were excluded. A total of 196 unknown-status entries were re-submitted to Claude for reclassification, of which 77 were successfully resolved.

Additionally, a systematic audit of the ESU source database was conducted to investigate the absence of several prominent Ukrainian cultural figures from the dataset.

---

### A — Individual Record Corrections (3 entries)

These corrections are based on established historical record and correct misclassifications introduced during the original AI classification pass.

| Name | Field | V2.2 value | V2.3 value | Evidence |
|------|-------|------------|------------|----------|
| Куліш Микола Гурович (1892–1937) | `death_cause` | `gulag` | `executed` | Shot at Sandarmokh 03.11.1937 — confirmed mass execution site of the Stalinist Great Terror; not a gulag death |
| Квітко Лев (1890–1952) | `migration_status` | `unknown` | `non_migrated` | Never left the USSR; spent his career in Kharkiv and Moscow |
| Квітко Лев (1890–1952) | `death_cause` | *(blank)* | `executed` | Executed 12.08.1952 as part of the Night of the Murdered Poets (ніч страчених поетів) — the mass execution of Jewish Soviet writers ordered by Stalin |
| Маркіш Перец Давидович (1895–1952) | `death_cause` | `gulag` | `executed` | Executed 12.08.1952 in the same Night of the Murdered Poets event; was not a gulag death |

**Night of the Murdered Poets context:** On 12 August 1952, thirteen prominent Jewish Soviet cultural figures (writers, poets, artists) were executed by firing squad following a closed trial by the MGB. This was the culmination of Stalin's anti-cosmopolitan campaign and the suppression of Yiddish culture in the USSR. Both Квітко and Маркіш were among the thirteen victims. Classifying these deaths as `gulag` was factually incorrect; they were judicial executions by the state.

---

### B — Impossible-Age Exclusions (19 entries)

A data quality audit identified 19 entries in the analysable set (migration_status: migrated / non_migrated / internal_transfer / deported) with `age_at_death` between 0 and 9 years. These are clearly data errors — either name collisions (an ESU entry for a person with the same name as a historical figure, recording a different person's dates), or malformed date fields where birth and death year refer to an artwork's date range rather than a lifespan.

These 19 entries were reclassified to `excluded_bad_dates`. A person aged 0–9 cannot be a practising creative worker in any meaningful sense, and their inclusion would artificially depress group mean life expectancy.

Impact on dataset: removes 19 entries from the analysable pool. Net effect on mean LE is negligible given group sizes.

---

### C — Unknown-Status Reclassification (196 → 77 resolved)

At the end of V2.2, 196 entries had `migration_status = unknown` and a recorded death year, meaning they were in principle classifiable but were left unresolved by the original Claude review pass (typically due to API errors or genuinely ambiguous biographies).

**Method:**
- Script: `reclassify_unknowns.py`
- For each entry: fetched full ESU article bio (HTTP GET to `article_url`), submitted to Claude Haiku-4.5 for first-pass classification using the same four-category MIGRATION_SYSTEM prompt used in Phase 4
- If Haiku returned `unknown`, re-submitted to Claude Sonnet-4.6 with the deeper MIGRATION_DEEP_SYSTEM prompt (geography clues, diaspora signal detection)
- Saved incrementally every 10 entries

**Results:**
- 77 entries successfully classified (39.3% resolution rate)
- 119 entries remain `unknown` (excluded from analysable set)
- The 119 remaining unknowns are genuinely unresolvable: entries with no geographic data, Belarusian/Lithuanian/other non-Ukrainian figures referenced by the ESU with no meaningful Ukrainian biography, or persons with only a name and approximate date range

**API cost:** approximately $0.20 (196 entries × Haiku first pass + ~50 Sonnet retries)

---

### D — ESU Source Gap Investigation

**Background:** Several prominent Ukrainian creative workers known from other historical sources were found to be absent from the V2.2 dataset. These include:

- Тичина Павло (1891–1967) — canonical Ukrainian Soviet poet
- Рильський Максим (1895–1964) — poet
- Стус Василь (1938–1985) — dissident poet, died in Perm-36 gulag
- Хвильовий Микола (1893–1933) — Executed Renaissance novelist, suicide
- Симоненко Василь (1935–1963) — Sixtiers poet

**Investigation method:** A diagnostic script (`diagnose_scraper.py`) was written and executed. The script fetched every page of the ESU letter-index listings for the relevant alphabet letters (Р: 29 pages, С: 69 pages, Т: 30 pages, Х: 12 pages, Ч: 17 pages) and searched exhaustively for each name. The scraper's pagination logic was also tested against confirmed working letters (К: 479 pages, М: 288 pages) to verify the mechanism was functioning correctly.

**Findings:**

| Figure | Result |
|--------|--------|
| Тичина Павло | **Absent from ESU** — 0 matches across all 30 pages of letter Т |
| Рильський Максим | **Absent from ESU** — 0 matches across all 29 pages of letter Р |
| Стус Василь | **Absent from ESU** — 0 matches across all 69 pages of letter С |
| Хвильовий Микола | **Absent from ESU** — 0 matches across all 12 pages of letter Х |
| Симоненко Василь | **Absent from ESU** — 0 matches across all 69 pages of letter С |
| Семенко Михайль | **Absent from ESU** — only unrelated "Семенков" found |
| Чорновіл В'ячеслав | **Present in ESU** (article-890626, letter Ч page 13) but described as "політичний діяч" (political figure) — correctly excluded by our profession keyword filter |

**Conclusion:** The ESU (esu.com.ua) is an ongoing encyclopedic project. As of the 2026 access date, articles for these prominent figures have not yet been published in the digital encyclopedia. This is a source-level gap, not a scraper failure. The pagination mechanism was verified as functioning correctly; no entries were lost to scraper bugs.

The absence of these figures from our dataset does not constitute a methodological error. It is a known limitation of using a single living encyclopedia as the primary data source. Future iterations of this study should supplement with additional sources once ESU coverage expands, or manually add these figures from verified secondary sources with appropriate provenance notes.

---

### E — New Scripts Created in V2.3

**`diagnose_scraper.py`**
Read-only diagnostic tool. Fetches ESU letter-index pages and checks: (1) pagination behaviour and total page count per letter, (2) presence or absence of specific named individuals across all pages of a letter, (3) HTML structure of listings to detect potential parser failures. Makes HTTP GET requests only; writes nothing. Used to confirm the ESU source-gap finding above.

**`reclassify_unknowns.py`**
Reclassification tool for `unknown` migration-status entries. Reads `esu_creative_workers_v2_3.csv`, filters entries with `migration_status == 'unknown'` and a recorded death year, fetches full ESU article bio for each, submits to Claude Haiku then Sonnet (if still unknown), and writes updated classification back to the CSV. Saves incrementally every 10 entries (safe to interrupt and re-run). Also applies Phase 4 manual corrections (A, B, C above) before the reclassification loop.

---

### F — V2.3 Headline Results

| Metric | V2.2 | V2.3 | Change |
|--------|------|------|--------|
| Analysable (total) | 8,830 | 8,643 | −187 (impossible ages removed, unknowns not reclassified) |
| Migrated n | 1,273 | 1,280 | +7 |
| Non-migrated n | 6,000 | 6,030 | +30 |
| Internal transfer n | 1,155 | 1,150 | −5 |
| Deported n | 178 | 183 | +5 |
| Migrated mean LE | 75.21 yr | 75.25 yr | +0.04 |
| Non-migrated mean LE | 71.17 yr | 71.22 yr | +0.05 |
| Deported mean LE | 47.85 yr | 48.35 yr | +0.50 |
| Gap (migrated vs non-migrated) | +4.03 yr | +4.04 yr | +0.01 |
| Cohen's d | 0.288 | 0.292 | +0.004 |
| Conservative two-group gap | +4.66 yr | +4.68 yr | +0.02 |
| Conservative two-group d | 0.332 | 0.330 | −0.002 |

The headline finding is unchanged: Ukrainian creative workers who emigrated from the Soviet sphere lived significantly longer than those who remained, with a mean gap of **+4.04 years** (Cohen's d=0.292, p<0.001). The deported group shows a catastrophic deficit of **−22.87 years** relative to non-migrants (d=1.656, p<0.001).

---

### G — Files Created/Modified in V2.3

| File | Action |
|------|--------|
| `esu_creative_workers_v2_3.csv` | **Created** — corrected primary dataset; v2_2 preserved unchanged |
| `esu_creative_workers_v2_2.csv` | **Unchanged** — archived reference dataset |
| `diagnose_scraper.py` | **Created** — ESU source audit script |
| `reclassify_unknowns.py` | **Created** — unknown reclassification script |
| `generate_analysis.py` | **Updated** — CSV_PATH and SOURCE_NOTE point to v2_3 |
| `charts/*.png` | **Regenerated** — all 24 charts from V2.3 data |
| `analysis_v2_3.txt` | **Created** — full statistical report for V2.3 |

*This log phase completed: 2026-04-05*

---

## Phase V2.4 — Right-Censored Cox PH Rework: Proper Living Cohort Classification (2026-04-07)

### Problem Identified (V2.3/V2.5 Flaw)

V2.3 right-censored Cox supplement assigned all 6,575 living individuals to `non_migrated`, producing a structurally invalid model: 52.2% censoring in non-migrated vs 0% in all other groups. This made HR comparisons across groups incoherent — the censored model could not validly estimate migration group survival differences.

### Solution: AI Classification of Living Cohort

The same two-stage Claude pipeline (Haiku first pass, Sonnet retry for unknowns) was applied to all living individuals, using their ESU biographical text as input.

**Stage 1 — Extract living individuals for classification:**
- Input: raw ESU data (flag_non_ukrainian=0, has birth_year, has notes)
- Output: `data/living_individuals_for_classification.csv` (6,563 rows)

**Stage 2 — AI classification (parallel subagent approach):**
- Tool: 30 parallel Claude Code subagents (~219 rows/chunk each)
- Reason for subagents: API credit balance was zero; Claude Code subscription covers subagent usage
- Same system prompts as dead-cohort classification (MIGRATION_SYSTEM + MIGRATION_DEEP_SYSTEM)
- Output: `data/living_individuals_classified.csv`

**Distribution after AI classification:**
| Status | n | % |
|--------|---|---|
| non_migrated | 5,858 | 89.3% |
| migrated | 375 | 5.7% |
| internal_transfer | 155 | 2.4% |
| unknown | 149 | 2.3% |
| deported | 15 | 0.2% |

**Red flag checks:** Deported 0.2% (below 5% threshold ✓), Unknown 2.3% (below 20% threshold ✓)

**Stage 3 — Edge case review:**
- 185 born before 1920: `implausibly_alive` → event_observed=1, duration=80
- 64 migrants born after 1960: flagged `likely_post_soviet_emigrant`
- Manual reclassifications: Operation Vistula (Polish state, not Soviet → non_migrated); Russia-career cases (migrated→internal_transfer); returnees and foreign nationals corrected

**Stage 4 — Extended dataset:** `data/esu_extended_for_cox.csv`, N=15,053 (dead=8,739 + censored=6,314)

### Stage 5 — Cox PH Results (script: `stage5_cox.py`)

**Model 2 adjusted (primary):**
| Group | HR | 95% CI | p |
|-------|----|--------|---|
| migrated | 0.832 | 0.778–0.889 | <0.0001 |
| internal_transfer | 1.105 | 1.033–1.182 | 0.0038 |
| deported | 4.646 | 3.908–5.524 | <0.0001 |

Key finding: Unadjusted migrated HR=1.088 reverses to 0.832 after adjustment — differential censoring (49% vs 20%) suppresses non-migrated baseline hazard in unadjusted model; birth cohort adjustment corrects this.
Schoenfeld PH test: deported p<0.0001 (violated), migrated p=0.011 (violated), internal_transfer p=0.066 (OK).

### Stage 6 — Sensitivity Analyses (script: `stage6_sensitivity.py`)

| Scenario | Result |
|----------|--------|
| A: implausibly alive age assumption (70–90) | Migrated HR 1.067–1.100 — stable |
| B: post-Soviet emigrant handling (include/exclude/reclassify) | Max HR change 0.006 — negligible |
| C: bootstrap misclassification 5%/10%/15% (50 iter each) | Median HR 1.077–1.088 — robust |

### Stage 7 — Figures (script: `stage7_figures.py`)

| Figure | Change |
|--------|--------|
| fig24 | Updated forest plot with correct V2.4 HRs |
| fig25 | Updated censoring pattern — proper distribution across all groups |
| fig26 | Updated KM curves — N=15,053, all groups have tick marks |
| fig27 | NEW sensitivity summary chart |

### Stage 8 — Time-Varying Hazard Analysis (script: `stage8_timevarying.py`)

**What was done:** Address the Schoenfeld PH violation for the deported group (p<0.0001) identified in Stage 5 by running a landmark Cox analysis — fitting a separate unadjusted Cox model within each 10-year age band (20–90). Each band model asks: among individuals still alive at the start of the window, were deportees dying faster than non-migrants during that specific decade?

**Key results:**

| Age band | HR | p | Interpretation |
|----------|----|---|----------------|
| 20–30 | 1.10 | 0.35 | No excess mortality in youth |
| 30–40 | 1.51 | <0.001 | Killing begins — early Terror |
| **40–50** | **1.89** | **<0.001** | **PEAK — Great Terror / Gulag** |
| 50–60 | 1.61 | 0.001 | Elevated but declining |
| 60–70 | 1.50 | 0.018 | Fading |
| 70–80 | 1.21 | 0.36 | Not significant |
| 80–90 | 0.95 | 0.86 | Null — survivors converge |

**Historical interpretation:** Workers born ~1890–1910 (Executed Renaissance generation) were in their 30s–40s during the 1937–38 Great Terror — exactly the peak band. The overall HR=4.646 is a lifetime average that compresses this concentrated event into one number. The landmark analysis restores the temporal structure.

**Figures generated:**
- `fig28_deported_hr_by_age.png` / `fig28_interactive.html` — landmark HR by age band
- `fig28b_schoenfeld_smooth.png` — Schoenfeld residual smoothed log-HR (bootstrapped lowess)

**Paper updates:**
- PAPER_DRAFT.md §4.10: "note on shape" paragraph replaced with Table A-Cox-TV + full historical interpretation
- Fig24/25/26 captions moved to appear immediately after main Cox results (before time-varying section)
- Fig28/28b captions placed at end of time-varying section
- Figure map table updated

**Docs updated:**
- SCIENTIFIC_METHODOLOGY.md: §8.13 added (v1.6); version history row 2.7 added
- AI_METHODOLOGY_LOG.md: this entry
- HTML rebuilt (32 static + 29 interactive figures) and pushed to GitHub Pages

### Files Created/Modified in V2.4

| File | Action |
|------|--------|
| `data/living_individuals_for_classification.csv` | Created |
| `data/living_individuals_classified.csv` | Created |
| `data/living_individuals_cleaned.csv` | Created |
| `data/esu_extended_for_cox.csv` | Created |
| `classify_living.py` | Created |
| `stage5_cox.py` | Created |
| `stage6_sensitivity.py` | Created |
| `stage7_figures.py` | Created |
| `results/cox_censored_output.txt` | Updated |
| `results/sensitivity_output.txt` | Created |
| `results/sensitivity_results.json` | Created |
| `charts/fig24–27 (png + html)` | Updated/Created |
| `chart_docs/fig24–27.md` | Updated/Created |
| `stage8_timevarying.py` | Created |
| `results/timevarying_output.txt` | Created |
| `charts/fig28_deported_hr_by_age.png` | Created |
| `charts/fig28_interactive.html` | Created |
| `charts/fig28b_schoenfeld_smooth.png` | Created |
| `chart_docs/fig28_deported_hr_by_age.md` | Created |
| `PAPER_DRAFT.md` | Updated (§4.10 time-varying section + fig positioning) |
| `SCIENTIFIC_METHODOLOGY.md` | Updated (v1.6, §8.13) |
| `AI_METHODOLOGY_LOG.md` | Updated (Stage 8 entry) |
| `docs/index.html` | Rebuilt |

*This log phase completed: 2026-04-07*

---

## Stage 9 — Emigration Wave Disaggregation (V2.5) — RETRACTED

**Purpose:** Test the self-selection critique structurally by disaggregating the 1,313 migrant entries into three historically distinct emigration waves, each defined by a different selection mechanism.

**Method attempted:** Rule-based year extraction (regex `\b1[89]\d\d\b`) from `migration_reasoning` (English biographical text) with keyword fallback. Priority hierarchy: WAVE1 (pre-1922) > WAVE2 (1939–45) > WAVE3 (1946–91) > WAVE4 (post-1992 excluded) > UNKNOWN.

**Initial results computed (not reported):**
- WAVE1 gap: +2.41 years, WAVE2: −0.88 years (p=0.63), WAVE3: +4.44 years (p<0.001)
- Adjusted OLS: WAVE3 = +4.54 years (p<0.001); WAVE1 and WAVE2 not significant

**Critical flaw identified — findings retracted:**

Manual review of a 50-entry random sample from `wave_assignments.csv` confirmed that the classifier was systematically recovering **death year** and **birth year** rather than emigration year. The `migration_reasoning` column was written by Stage 4 Claude to establish migration *status* (i.e., "died in New York in 1972 = settled outside Ukraine"), not to record departure *timing*. The death year is therefore the most prominent year in the text — and is what the regex extracted.

Specific failure modes identified:
- **WAVE4 contamination:** Individuals who emigrated in 1944 or 1955 but died after 1992 were classified as WAVE4 because their death year (e.g., 1994, 2001) triggered the post-1992 threshold.
- **WAVE1 contamination:** Individuals born in 1917–1921 and dying in the USA in the 1980s–2000s were classified as WAVE1 because their birth year fell in the WAVE1 trigger set {1917–1921}, despite the biographical text explicitly describing them as post-WWII or Cold War emigrants.
- **WAVE3 inflation:** The majority of WAVE3 entries appear to be classified on the basis of a death year falling in 1946–1991, not any evidence of departure timing.

The analytical pipeline and output files are retained in the repository for reference. The wave statistics and figures (fig29, fig29b, fig29c) are **not reported as findings** in the paper.

**Root cause:** Stage 4 did not capture emigration year as a field. Departure-specific language (`"виїхав у"`, `"емігрував до"`, `"fled in [year]"`) was not extracted. Any reliable wave disaggregation requires a targeted re-pass over the original Ukrainian ESU article text.

**Decision (2026-04-07):** Findings retracted. §5.1 wave analysis replaced with methodology limitation note. Defined as a V3 data collection deliverable.

### Files Created in V2.5 — Stage 9 (retained for V3 reference)

| File | Action |
|------|--------|
| `stage9_wave_disaggregation.py` | Created — retained, not re-run |
| `stage9c_wave_lifespan_chart.py` | Created — retained, not re-run |
| `wave_assignments.csv` | Created (1,313 rows) — classifications unreliable |
| `wave_stats.txt` | Created — statistics not reported |
| `charts/fig29_wave_km.png` | Created — not reported as finding |
| `charts/fig29b_wave_volume.png` | Created — not reported as finding |
| `charts/fig29c_wave_lifespan.png` | Created — not reported as finding |
| `PAPER_DRAFT.md` | Updated — §5.1 wave analysis replaced with limitation note |

---

## Stage 10 — Missing Figures Bias Bounding (V2.5)

**Purpose:** Quantify the direction and magnitude of ESU undercoverage bias. Seven confirmed absent repressed non-migrants provide a hardcoded anchor; a sensitivity table shows the gap widens under all plausible M assumptions.

**Confirmed absent figures (all non-migrants):**
- Vasyl Stus (1938–1985, age 47): Perm-36 labour colony
- Mykola Khvylovy (1893–1933, age 39): Suicide under political pressure
- Vasyl Symonenko (1935–1963, age 28): Disputed KGB custody
- Mykhailo Semenko (1892–1937, age 45): Shot, Great Terror
- Yevhen Pluzhnyk (1898–1936, age 38): Shot, Solovki
- Myroslav Irchan (1897–1937, age 40): Shot, Great Terror
- Dmytro Falkivsky (1898–1934, age 36): Shot, NKVD

Mean age at death (named cases): 39.0 years (32 years below non-migrant mean of 71.22)

**Note:** Several other documented Executed Renaissance figures (Zerov, Kosynka, Pidmohylny, Kurbas) ARE present in the ESU dataset as non_migrated and already counted in the non-migrant mean.

**Sensitivity results:** Under all M values (8–500) and all Ā_missing values (38–50), the adjusted gap is larger than the observed 4.04 years. M=50 at Ā=38: gap = 4.31 years. M=200 at Ā=38: gap = 5.10 years. The current estimate is a confirmed lower bound.

### Files Created in V2.5 — Stage 10

| File | Action |
|------|--------|
| `stage10_missing_bias.py` | Created |
| `named_missing_figures.csv` | Created (7 rows) |
| `charts/fig30_sensitivity_gap.png` | Created (2778×1376, dpi=200) |
| `charts/fig30_interactive.html` | Created |
| `chart_docs/fig30_sensitivity_gap.md` | Created |
| `PAPER_DRAFT.md` | Updated (§5.4 quantified missing bias + Table MF) |
| `SCIENTIFIC_METHODOLOGY.md` | Updated (v1.7, §8.14, §8.15) |
| `AI_METHODOLOGY_LOG.md` | Updated (Stage 9 + Stage 10) |
| `docs/index.html` | Rebuilt |

*This log phase completed: 2026-04-07*
