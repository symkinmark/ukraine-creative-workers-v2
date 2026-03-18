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

*[To be completed — details to be added after human review]*

**Planned process:**
- Mark Symkin manually verifies a 1–2% random sample of entries
- Checks: correct identification, correct dates, correct profession categorisation
- Systemic errors trigger re-run of affected batch

---

## Phase 6 — Paper Writing

*[To be completed — details to be added]*

---

## AI error rate reference

V1 established a baseline AI error rate of ~20% for biography analysis tasks (using ChatGPT for migration status determination). Half were casual mistakes; half required deep human review.

V2 uses Claude Sonnet 4.6. Error rate will be tracked during the Phase 5 accuracy check and reported in the methodology section of the paper.

---

*This document is updated throughout the research process. Final version to be attached as Appendix to V2 paper.*
