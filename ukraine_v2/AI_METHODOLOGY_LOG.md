# AI Methodology Log — Ukrainian Creative Workers Life Expectancy V2

**Paper:** Life Expectancy of Ukrainian Creative Industry Workers During the Soviet Occupation
**Authors:** Elza Berdnyk, Mark Symkin
**AI used:** Claude Sonnet 4.6 (Anthropic) — primary research & writing AI
**Cross-check AI:** Claude Sonnet 4.6 (second independent instance, no shared context)
**Log compiled:** March 2026

---

## Purpose of this document

This log records all decisions made with AI assistance during the V2 research process. It is attached to the paper as a transparency document, consistent with the authors' commitment to open acknowledgement of AI usage in academic research (as established in the V1 methodology).

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
- **Two-AI cross-check:** Both Claude instances (Sonnet 4.6). Claude A = primary analysis; Claude B = independent verification in a separate conversation with no shared context.

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

*[To be completed — details to be added after analysis]*

**Planned process:**
- Claude A analyses full dataset: life expectancy by migration status, profession, gender, time period
- Claude B independently analyses the same dataset in a fresh conversation
- Discrepancies between the two analyses flagged for human review (Mark Symkin)

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

## Phase 5b — V2.1 Accuracy Check (pending)

Before running analysis on the V2.1 classified dataset, a second human accuracy check will be performed on a fresh random sample of ~63 entries from `esu_creative_workers_v2_1.csv`. This verifies that the four-way classification (migrated / non_migrated / internal_transfer / deported) is performing correctly, and specifically that:
- Deportees are not being misclassified as internal transfers or non-migrants
- Internal transfers are not being conflated with migrants
- Pre-1921 and Galicia exclusions are applied correctly

Error rate target: below 5% (improvement from V2.0's 9.5%).

---

## Phase 4c — Extended Analysis Plan (pending Phase 5b clearance)

Once V2.1 accuracy is confirmed, the following analysis and charts will be generated:

### Charts — 10 figures + 1 flowchart

| Fig | Type | Scientific purpose |
|-----|------|--------------------|
| 1 | Bar + error bars (±1 SD) | Primary LE comparison across four groups |
| 2 | Box plots (4 groups) | Show distribution shape — means alone mislead on skewed data |
| 3 | Kaplan-Meier survival curves | Standard mortality research chart — proportion surviving past each age |
| 4 | Histogram: death year clustering | Great Terror spike visible in raw death year data |
| 5 | Bar: deaths + avg age by Soviet period | How mortality changed across political history of USSR |
| 6 | Line: LE by birth cohort (decade) | Which generations were most affected |
| 7 | Grouped bar: LE by profession + group | Secondary finding — profession-level risk |
| 8 | Bar: deported deaths by year 1921–1960 | New V2.1 finding — repression concentration in 1937–1942 |
| 9 | Bar: birth year distribution by group | Selection bias check — are groups comparable at baseline? |
| 10 | Significance brackets + CI overlay | Connect statistical tests (Mann-Whitney U, Cohen's d) to visuals |
| Flow | CONSORT-style exclusion flowchart | Standard for filtered datasets — 70,000 → 6,420 entries, step by step |

### Additional analysis (not in V2.0)

- **Confidence intervals on deported group** — n=75 is small; CI must be shown to validate the 22-year penalty finding
- **Comparison to general Soviet/Ukrainian population LE** — contextual reference line on charts
- **Gender acknowledgment** — check whether gender distribution differs across groups; report as limitation if data is insufficient
- **Sensitivity analysis for 9.5% AI error rate** — show conclusions hold if 9.5% of classifications are flipped in the least favourable direction

---

## Phase 6 — Paper Writing

*[To be completed after Phase 5b accuracy check and full analysis run]*

---

## AI error rate reference

V1 established a baseline AI error rate of ~20% for biography analysis tasks (using ChatGPT for migration status determination). Half were casual mistakes; half required deep human review.

V2 Phase 5 accuracy check found a **9.5% error rate** (6 errors in 63 entries reviewed). Error types: nationality misclassification (4 cases), migration misclassification (2 cases). No date errors found. All errors were systematic in nature — addressable by rule corrections rather than individual manual fixes — which is why a full rerun with corrected classification rules is the appropriate response rather than patching individual entries.

---

*This document is updated throughout the research process. Final version to be attached as Appendix to V2 paper.*
