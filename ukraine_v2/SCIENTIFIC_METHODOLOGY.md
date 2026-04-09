# Scientific Methodology and Replication Guide

## Mortality Differentials Among Ukrainian Creative Industry Workers During the Soviet Occupation: An Expanded Study (V2)

**Author:** Mark Symkin
**Study completed:** 2026
**Data source:** Encyclopedia of Modern Ukraine (esu.com.ua)
**This document version:** 1.9 — revised 2026-04-09 following Stages 11–15 database quality pipeline: 97 birth-year-as-death-year corrections, 57 API-error retries (Stage 12), 8 manual validation patches (Stage 13), 135 authentication-error reclassifications (Stage 14), 6 Stage-14-review corrections (Stage 15); all 200 validation entries reviewed (3.2% error rate confirmed); dataset finalised at N=8,590; paper rewritten as V3.0 with all statistics verified (177/177 checks pass)


## Version History

| Version | Date | Key change |
|---|---|---|
| 1.0 | 2025 | Initial V1 methodology (2-group, n=415, Harvard Masterclass) |
| 2.0 | 2026 | V2 expanded dataset (4-group, n=8,643), full AI disclosure |
| 2.1 | 2026-04-03 | Phase 5 human check; pre-1921 and Galicia filters added |
| 2.2 | 2026-04 | Author corrected to Mark Symkin; sample sizes updated to V2.3; Cliff's delta and CI added |
| 2.3 | 2026-04-06 | Peer-review batch 1 (11 steps): terminology, §3.4.1, §4.9 OLS regression, Fig 23, selection bias §, Fig 7b |
| 2.4 | 2026-04-06 | Peer-review batch 2 (7 major weaknesses): Cox PH (§4.10, Fig 24), PSM (+3.35 yrs matched), argument restructure (deportee leads), figures distributed into narrative, nationality circularity note, post-1991 caveat, Table 6 small-n fix |
| 2.5 | 2026-04-06 | Right-censored Cox PH extension (§4.10 supplement): N=15,218 extended dataset, Schoenfeld PH test, informative censoring sensitivity analysis, Fig 25 (censoring pattern), Fig 26 (KM with censored data) |
| 2.6 | 2026-04-07 | V2.4 right-censored rework: living cohort classified via AI pipeline (6,314 properly distributed); Cox N=15,053; migrated HR=0.832 adjusted; §8.11–8.12 sensitivity analyses; fig24–27 regenerated |
| 2.7 | 2026-04-07 | Stage 8: time-varying landmark Cox by age band (§8.13); peak HR=1.86 at age 40–50; fig28/28b; §4.10 updated with Table A-Cox-TV |
| 2.8 | 2026-04-07 | Stage 9: emigration wave disaggregation attempted (§8.14); classifier built and run; manual review of 50-entry sample confirmed death year / birth year recovery rather than departure year; findings retracted; §5.1 replaced with methodology limitation; defined as V3 deliverable |
| 2.9 | 2026-04-07 | Stage 10: missing figures bias bounding (§8.15); 7 confirmed absent repressed non-migrants documented; sensitivity table shows 4.04y gap is conservative lower bound; fig30 |
| 2.10 | 2026-04-07 | Doc version 1.8: §8.14 rewritten to document Stage 9 failure mode and retraction; SCIENTIFIC_METHODOLOGY and AI_METHODOLOGY_LOG updated to reflect that wave figures are not reported findings |
| 2.11 | 2026-04-08 | Stage 11: data audit report (§8.16); Stage 12: full database quality pipeline B1–B5 → esu_creative_workers_v2_6.csv (§8.17); Stage 13: validation review corrections applied (§8.18) |
| 2.12 | 2026-04-09 | Stage 14: 135 API-fail entries reclassified via Haiku (§8.19); Stage 15: 6 Stage-14-review corrections (§8.20); 200/200 validation complete; paper rewritten as V3.0; 177/177 checks pass; N=8,590 final |

---
> **V3.0 CURRENT.** Primary dataset: `esu_creative_workers_v2_6.csv`. Analysable dead cohort: **N=8,590** (migrated=1,324 | non_migrated=5,960 | internal_transfer=1,111 | deported=195). Primary gap: **3.98 years** (Cohen's d=0.292). All 177 numeric claims verified. See AI_METHODOLOGY_LOG.md Stages 11–15 for full log.

---

## Purpose of This Document

This document is written for a researcher with no prior knowledge of this project who wishes to fully replicate the study from scratch. It provides the exact research question, data sources, inclusion and exclusion criteria, classification protocols (including verbatim AI prompts), statistical methods, known limitations, and file descriptions. Nothing is assumed; everything is specified.

If you are replicating this study, you should read this document in its entirety before touching any data or code. The decisions made at each stage — particularly nationality determination and migration classification — are interdependent, and misapplying them out of sequence will produce incorrect results.

---

## 1. Research Question

### 1.1 Primary Research Question

**Did Ukrainian creative industry workers who emigrated from the Soviet Union show a statistically significant mean age at death advantage compared to those who remained within Soviet-controlled territory, and if so, by how much?**

### 1.2 Secondary Research Questions

1. Does the mean age at death gap vary by creative profession?
2. Does the gap vary by birth cohort, and if so, in which cohorts is it largest?
3. Are there identifiable historical periods of anomalously elevated premature mortality among non-migrant creative workers, consistent with documented Soviet repression campaigns?
4. Are there geographic patterns in migration rates among Ukrainian creative workers, and what is the likely explanation?
5. How do the V2 findings compare to the V1 findings, and what methodological factors account for the differences?

### 1.3 What This Study Does Not Claim to Answer

This study does not establish clean causal identification of the mortality effect of Soviet conditions. It establishes an observational association between migration status and observed age at death in a specific professional population. Selection effects — the possibility that migrants and non-migrants differed before emigration in ways correlated with longevity — cannot be fully controlled for in this observational design. Readers should not interpret the mean age at death gap as a precise estimate of "how many additional years you would have lived if you had emigrated" at the individual level.

---

## 2. Dataset

### 2.1 Primary Data Source

**Source:** Encyclopedia of Modern Ukraine (Енциклопедія сучасної України, ESU)
**Maintained by:** Institute of Encyclopedic Research of the National Academy of Sciences of Ukraine (Інститут енциклопедичних досліджень НАН України)
**URL:** https://esu.com.ua
**Access date:** 2026
**Language:** Ukrainian

### 2.2 Description of the Data Source

The ESU is the authoritative scholarly encyclopedia of Ukrainian cultural and intellectual life. It is not a database with a structured API; it is a web-based encyclopedia with individual HTML pages for each entry. As of the access date, it contained approximately 70,000 individual entries covering Ukrainian cultural, scientific, political, and religious figures from antiquity to the present.

Each ESU entry typically contains:
- Full name in Ukrainian
- Birth year and place (sometimes with month and day)
- Death year and place (sometimes with month and day; absent for living individuals)
- One or more profession/field labels
- A biographical narrative in Ukrainian (typically 200–2,000 words)
- References to primary and secondary sources
- External links (sometimes including archival sources or other encyclopedias)

The quality and length of entries varies considerably. Short entries for minor figures may contain only 100–200 words, which can make nationality and migration determination difficult. Long entries for major figures may run several thousand words and contain extensive biographical detail.

### 2.3 Programmatic Access

The ESU does not provide an official API or bulk data download. Data were collected via web scraping. The scraper is documented in Section 12 (Scripts).

**To access the ESU programmatically:**

1. The site uses a URL structure of the form: `https://esu.com.ua/article-XXXXX` where XXXXX is a numeric article ID.
2. Article IDs are not sequential without gaps; the scraper must either iterate through a range of IDs (with error handling for 404 responses) or build an index from the sitemap (https://esu.com.ua/sitemap.xml).
3. The HTML structure uses standard Ukrainian-language encoding (UTF-8). Parser libraries should be configured for UTF-8.
4. The site's robots.txt should be consulted before scraping; scraping should be performed at a polite rate (minimum 1–2 second delay between requests) to avoid overloading the server.
5. The site may implement rate limiting; the scraper should implement exponential backoff on HTTP 429 (Too Many Requests) responses.

**Required Python libraries:**
- `requests` (HTTP requests)
- `beautifulsoup4` (HTML parsing)
- `lxml` (HTML parser backend)
- `pandas` (data management)
- `time` (for delays between requests)
- `re` (regular expressions for date extraction)
- `anthropic` (for Claude API calls in the nationality/migration review phases)

### 2.4 Dataset Scale

- **Total ESU entries scraped:** approximately 70,000
- **Entries matching creative worker profession keywords:** 16,215
- **Entries usable for primary age-at-death analysis (birth date + death date + determinable migration status + confirmed Ukrainian nationality):** 8,643 (V2.3)
- **Of which non-migrants:** 6,030
- **Of which migrants:** 1,280
- **Of which internal transfers:** 1,150
- **Of which deported:** 183
- **Entries excluded due to living status (no death date):** the majority of the excluded entries
- **Entries excluded due to non-Ukrainian nationality:** 1,218 (after Claude review)
- **Entries excluded due to indeterminate migration status:** several hundred

---

## 3. Inclusion Criteria

An entry was included in the primary age-at-death analysis if and only if ALL of the following conditions were met:

**Condition 1: Confirmed Ukrainian nationality.**
The individual was determined to be Ukrainian according to the three-tier nationality determination protocol described in Section 6. This does not require ethnic Ukrainian heritage; it requires that the individual participated in Ukrainian cultural life and identified with Ukrainian cultural or national identity. Criteria are detailed in Section 6.

**Condition 2: Creative worker profession.**
The individual's primary listed profession in the ESU matched at least one of the Ukrainian-language profession keywords in the inclusion list in Section 5. Profession determination used the ESU's own profession labels, not inference from the biographical text.

**Condition 3: Confirmed birth year.**
The entry contained a specific birth year (not an approximate date, date range, or "circa" date). Entries with birth year listed as "?", "circa," "c.", "бл." (Ukrainian abbreviation for "approximately"), or a range (e.g., "1880s") were excluded.

**Condition 4: Confirmed death year.**
The entry contained a specific death year. Entries for living individuals (no death year) and entries with approximate or uncertain death years were excluded. Entries where the death year was the same as the birth year (possible data entry error) were flagged for manual review before inclusion.

**Condition 5: Determinable migration status.**
The individual's migration status (migrated from Soviet territory or remained in Soviet territory) could be determined with reasonable confidence from the ESU biographical text. The exact classification rules are specified in Section 7.

---

## 4. Exclusion Criteria

An entry was excluded from the primary analysis if ANY of the following applied. Excluded entries were retained in the raw dataset with a flag indicating the reason for exclusion.

### 4.1 Living Individuals

Entries with no death year recorded were classified as potentially living and excluded from age-at-death analysis. Some of these individuals may in fact be deceased but lack a recorded death date in the ESU; this is a data availability issue, not a classification error.

### 4.2 Uncertain or Approximate Dates

Birth or death years recorded with any of the following markers were excluded:
- "?" in the date field
- "бл." (abbreviation for "близько," meaning approximately)
- "c." or "circa" in transliterated entries
- A range of years (e.g., "1880–1885")
- A decade without a specific year (e.g., "1880s")
- Explicit scholarly notation of uncertainty (e.g., "можливо 1923" — "possibly 1923")

**Rationale:** Including approximate dates would introduce measurement error of potentially ±5–10 years per individual into life expectancy calculations. Given that the overall gap we are measuring is approximately 5 years, this level of measurement error would be unacceptable.

### 4.3 Non-Ukrainian Nationality

Individuals determined to be non-Ukrainian through the nationality determination protocol (Section 6) were excluded. This included:
- Foreign artists referenced in the ESU for their influence on Ukrainian culture
- Soviet-era figures of non-Ukrainian nationality who worked in Soviet Ukraine
- Individuals of ambiguous nationality who could not be confirmed as Ukrainian after Claude review

### 4.4 Non-Creative Professions

Individuals whose ESU-listed professions did not match any keyword on the creative worker inclusion list (Section 5) were excluded. This primarily affected:
- Scientists, academics, and philosophers without creative practice
- Journalists without dual creative profession listings
- Religious figures
- Politicians and military figures

### 4.5 Indeterminate Migration Status

Individuals whose migration status could not be determined from the biographical text, even after Claude review, were excluded rather than assigned to either group based on guesswork. This exclusion was applied conservatively: if the biographical text made migration status ambiguous, the individual was excluded.

### 4.6 Late-Life Emigration

Individuals who emigrated after age 70 were excluded from the migration analysis (though retained in descriptive counts). The rationale is that emigration after age 70 is too late to have substantially affected working-life mortality exposure; the primary period of differential mortality risk from Soviet conditions is the working years (approximately ages 20–65).

### 4.7 Pre-Soviet Deaths — Added in V2.1 (2026-04-03)

**Rule:** Individuals with `death_year < 1921` are excluded from the primary analysis.

**Rationale:** The Ukrainian Soviet Socialist Republic was not consolidated until 1920–1922. Individuals who died before 1921 were never subject to Soviet governance, Soviet cultural repression, or Soviet mortality conditions. Including them in a study of Soviet-era mortality impact is anachronistic and methodologically indefensible. They are retained in the raw dataset with an `excluded_pre_soviet` flag.

**Historical note:** The date 1921 was selected because it marks the approximate end of the Ukrainian-Soviet War and the consolidation of Soviet control over most of Ukrainian territory. Some historians use 1922 (formal formation of the USSR). We use 1921 as the more conservative cutoff.

### 4.8 Galicia Temporal Filter — Added in V2.1 (2026-04-03)

**Rule:** Individuals born in Galicia (modern Lviv, Ternopil, Ivano-Frankivsk oblasts and surrounding historically Galician territory) are included **only if they were alive after 1939**.

**Rationale:** Galicia was part of the Austro-Hungarian Empire until 1918, then part of the Polish Second Republic until September 1939, when the USSR annexed Western Ukraine under the Molotov-Ribbentrop Pact. Galician creative workers who died before 1939 were never under Soviet rule. Including their mortality data in a study of Soviet conditions would be an error of historical fact, not merely a methodological choice. Workers who were alive in 1939 and later experienced Soviet conditions after annexation are legitimately included.

**Implementation:** Birth location field is checked for Galician city/region names. If a Galician birthplace is identified AND `death_year < 1939`, the entry is excluded with flag `excluded_galicia_pre_annexation`.

### 4.7 Complete Nationality Exclusion Markers

The following nationality and geographic markers, when appearing as the primary nationality description in an ESU entry **without** any accompanying statement of Ukrainian connection, activity in Ukrainian cultural life, or self-identification as Ukrainian, were used to auto-exclude entries from the Ukrainian nationality pool (Tier 3 of the nationality determination protocol):

**Language/origin auto-exclusion markers:**
- Russian (Росіянин/Росіянка) — without explicit Ukrainian connection
- Belarusian (Білорус/Білоруска) — without explicit Ukrainian connection
- Polish (Поляк/Полька) — without explicit Ukrainian connection (note: Galician Poles with Ukrainian activity require Claude review)
- German (Німець/Німкеня) — without explicit Ukrainian connection
- French (Француз/Француженка) — without explicit Ukrainian connection
- British/English (Британець/Британка, Англієць/Англійка) — without explicit Ukrainian connection
- American (Американець/Американка) — without explicit Ukrainian connection
- Romanian (Румун/Румунка) — without explicit Ukrainian connection
- Czech (Чех/Чешка) — without explicit Ukrainian connection
- Slovak (Словак/Словачка) — without explicit Ukrainian connection
- Hungarian (Угорець/Угорка) — without explicit Ukrainian connection
- Austro-Hungarian (Австрієць/Австрійка) — without explicit Ukrainian connection
- Italian (Італієць/Італійка) — without explicit Ukrainian connection

**Markers triggering Claude review (Tier 2) rather than auto-exclusion:**
- Jewish (Єврей/Єврейка, also "Жид/Жидівка" in historical texts) — because many Ukrainian Jews participated fully in Ukrainian cultural life and self-identified as Ukrainian
- "Soviet" (Радянський) as primary nationality label — requires review to determine underlying national identity
- Polish-Ukrainian mixed identification — requires review
- "Galician" (Галичанин) — may indicate Polish or Ukrainian identity; requires review
- Armenian (Вірменин/Вірменка) — a small community with significant Ukrainian connections; requires review
- Greek (Грек/Грекиня) — Pontic Greek communities in Ukraine; requires review

---

## 5. Creative Worker Definition

The following Ukrainian-language profession keywords were used to identify creative workers. An entry was classified as a creative worker if its ESU profession field contained at least one of these terms (case-insensitive matching).

### 5.1 Literary Arts

| Ukrainian term | English translation |
|----------------|---------------------|
| поет | poet |
| поетеса | female poet |
| письменник | writer (general) |
| письменниця | female writer |
| прозаїк | prose writer |
| прозаїчка | female prose writer |
| романіст | novelist |
| романістка | female novelist |
| новеліст | short story writer |
| драматург | playwright |
| літератор | literary figure (general) |
| байкар | fabulist (fable writer) |
| перекладач | translator (literary) |
| перекладачка | female translator |
| есеїст | essayist |
| мемуарист | memoirist |
| гуморист | humorist |
| сатирик | satirist |
| фантаст | science fiction / fantasy writer |

### 5.2 Visual Arts

| Ukrainian term | English translation |
|----------------|---------------------|
| художник | artist (general) |
| художниця | female artist |
| живописець | painter |
| живописиця | female painter |
| скульптор | sculptor |
| скульпторка | female sculptor |
| графік | graphic artist |
| графічка | female graphic artist |
| ілюстратор | illustrator |
| ілюстраторка | female illustrator |
| гравер | engraver |
| граверка | female engraver |
| карикатурист | caricaturist |
| мозаїчист | mosaicist |
| кераміст | ceramicist |
| керамістка | female ceramicist |
| ткач | weaver (artistic textile) |
| ткачка | female weaver |
| вишивальниця | embroiderer |
| декоратор | decorator (artistic) |
| монументаліст | monumental artist |
| фрескіст | fresco artist |

### 5.3 Music

| Ukrainian term | English translation |
|----------------|---------------------|
| композитор | composer |
| композиторка | female composer |
| музикант | musician |
| музикантка | female musician |
| піаніст | pianist |
| піаністка | female pianist |
| скрипаль | violinist |
| скрипалька | female violinist |
| диригент | conductor |
| диригентка | female conductor |
| хоровий диригент | choral conductor |
| органіст | organist |
| органістка | female organist |
| бандурист | bandura player |
| бандуристка | female bandura player |
| кобзар | kobzar (Ukrainian travelling bard) |
| вокаліст | vocalist |
| вокалістка | female vocalist |
| баритон | baritone |
| тенор | tenor |
| сопрано | soprano |
| фольклорист | folklorist (musical) |

### 5.4 Performing Arts

| Ukrainian term | English translation |
|----------------|---------------------|
| актор | actor |
| акторка | actress |
| режисер | director (general) |
| режисерка | female director |
| театральний режисер | theatre director |
| кінорежисер | film director |
| кінорежисерка | female film director |
| хореограф | choreographer |
| хореографка | female choreographer |
| танцівник | dancer |
| танцівниця | female dancer |
| балетмейстер | ballet master |
| артист | performing artist (general) |
| артистка | female performing artist |
| циркач | circus performer |
| циркачка | female circus performer |

### 5.5 Architecture and Design

| Ukrainian term | English translation |
|----------------|---------------------|
| архітектор | architect |
| архітекторка | female architect |
| дизайнер | designer |
| дизайнерка | female designer |
| урбаніст | urban designer / urbanist |
| ландшафтний архітектор | landscape architect |
| інтер'єрний дизайнер | interior designer |

### 5.6 Film and Photography

| Ukrainian term | English translation |
|----------------|---------------------|
| кінооператор | cinematographer |
| кінооператорка | female cinematographer |
| сценарист | screenwriter |
| сценаристка | female screenwriter |
| фотограф | photographer (artistic; not press/documentary) |
| фотографка | female photographer |
| аніматор | animator |
| аніматорка | female animator |

### 5.7 Exclusion Notes for Adjacent Professions

The following professions were explicitly excluded even when they appeared alongside creative professions:

- **Журналіст/Журналістка (journalist):** Excluded as a standalone profession. Included only if dual-listed with a creative profession from the above lists. Journalism was treated as a distinct professional category because journalistic work under the Soviet system often served functions very different from independent creative practice.

- **Науковець/Вчений (scientist/scholar):** Excluded. Art historians, musicologists, and literary critics who were themselves also practising artists were included based on their practising profession, not their scholarly role.

- **Педагог/Вчитель (educator/teacher):** Excluded as a standalone profession. Many creative workers also taught; they were included based on their creative profession, not their teaching role.

- **Релігійний діяч (religious figure):** Excluded.

- **Політик/Громадський діяч (politician/civic activist):** Excluded.

---

## 6. Nationality Determination Protocol

### 6.0 Definition: Who Counts as Ukrainian

This study uses a **cultural participation definition of Ukrainian identity**, not an ethnic or linguistic one. This is a deliberate methodological choice with a principled scholarly basis, and it is stated here explicitly so that it can be critiqued, replicated, and compared against alternative definitions.

**A person is counted as Ukrainian in this study if they meet ANY of the following criteria:**

1. **Born or raised on territory that is now Ukraine** (including all historical Ukrainian lands: Left-Bank and Right-Bank Ukraine, Galicia, Bukovyna, Zakarpattia, Volhynia, Sloboda Ukraine, Novorossiya, and Crimea), AND made a creative contribution that forms part of the Ukrainian cultural record.

2. **Contributed substantially to Ukrainian cultural life**, regardless of ethnic or linguistic background — for example, a composer who wrote in the Ukrainian folk tradition, a theatre director who led Ukrainian-language productions, or an architect who shaped Ukrainian urban identity.

3. **Self-identified as Ukrainian** or was recognised as part of the Ukrainian creative community by their contemporaries, regardless of the ethnic category imposed by Soviet administrative records.

4. **Was subject to Soviet persecution specifically in the context of suppressing Ukrainian culture** — for example, was targeted during the Executed Renaissance purges, or lost their position during Soviet Ukrainisation rollbacks.

**A person is NOT counted as Ukrainian if:**

- They lived entirely outside Ukrainian territory with no substantial Ukrainian cultural connection.
- Their only connection to the ESU is being referenced as a foreign influence on Ukrainian culture (e.g., a famous French novelist whose work was translated into Ukrainian).
- They worked in Ukraine solely in a Soviet administrative capacity, with no creative output connected to Ukrainian cultural identity.
- They are an ethnic Russian whose entire career and creative output was oriented toward Russian rather than Ukrainian culture, even if they were born or worked in Ukraine.

**Why this definition:**

The Soviet Union systematically attacked Ukrainian cultural identity precisely because identity is expressed through cultural participation, not biological descent. Writers who chose to write in Ukrainian, composers who chose Ukrainian folk forms, theatre directors who chose Ukrainian-language staging — these were the people whose work was suppressed, whose manuscripts were burned, and who were disproportionately shot during the Great Terror. Defining "Ukrainian" by ethnicity or language alone would exclude significant portions of this persecuted community — including Ukrainian Jews whose entire cultural world was Ukrainian even when they wrote in Yiddish, and including Galician Poles who participated fully in Ukrainian cultural institutions. Defining it by cultural participation captures the population that was actually at risk.

**Notable inclusions justified by this definition:**

- **Crimean Tatars**: Indigenous to Ukrainian territory, targeted by the 1944 mass deportation. Included without review.
- **Ukrainian Jews**: Many participated fully in Ukrainian cultural life — writing about Ukraine, working in Ukrainian institutions, being targeted as part of the Ukrainian intelligentsia. Reviewed individually; those with substantial Ukrainian cultural connection included.
- **Galician Poles**: Those who self-identified with Ukrainian rather than Polish national identity and participated in Ukrainian cultural institutions included after review.
- **Non-Ukrainian-ethnicity figures with substantial Ukrainian careers**: Reviewed individually; included where Ukrainian cultural contribution is substantive and sustained.

**Stress-test questions applied during classification:**

| Scenario | Decision | Reasoning |
|----------|----------|-----------|
| Jewish, born Odesa, wrote in Yiddish, whole life in Ukraine | ✅ Include | Ukrainian territory, Ukrainian cultural world |
| Ethnic Russian, born Kharkiv, wrote in Russian, moved to Moscow at 25 | ❌ Exclude | No meaningful Ukrainian cultural contribution |
| Pole from Galicia, self-identified Ukrainian, wrote in Ukrainian | ✅ Include | Cultural participation + self-identification |
| Crimean Tatar, born Crimea, wrote in Crimean Tatar | ✅ Include | Indigenous to Ukrainian territory |
| Georgian composer, 30 years in Kyiv conducting Ukrainian orchestras | ✅ Include | Substantial Ukrainian cultural contribution |
| French writer referenced in ESU for influence on Ukrainian literature | ❌ Exclude | Referenced figure only, no Ukrainian presence |
| Ethnic Ukrainian born in Russia, no Ukraine connection | ❌ Exclude | No Ukrainian cultural or territorial connection |

### 6.1 Overview

The ESU contains entries for individuals of varied national backgrounds. Because we are studying Ukrainian creative workers specifically, we must determine whether each individual in our dataset should be classified as Ukrainian under the definition in Section 6.0. This is not always straightforward in practice, even with a clear definition: Soviet records often obscured or imposed national identities, and biographical texts reflect the political constraints of the periods in which they were written.

We developed a three-tier system:

**Tier 1 (Clean inclusion):** Unambiguously Ukrainian under Section 6.0 — include directly.
**Tier 2 (Claude review):** Biographical markers suggest possible ambiguity — send to Claude for review against Section 6.0 criteria.
**Tier 3 (Auto-exclusion):** Unambiguously non-Ukrainian under Section 6.0 — exclude directly.

### 6.2 Tier 1: Clean Inclusion Criteria

An entry was classified as Tier 1 (clean Ukrainian, no review needed) if the biographical text explicitly described the individual as Ukrainian (Українець/Українка) AND none of the Tier 2 ambiguity markers were present.

### 6.3 Tier 2: Ambiguity Markers Requiring Claude Review

An entry was flagged for Tier 2 Claude review if the biographical text contained any of the following markers, regardless of whether the entry also contained Ukrainian nationality descriptors:

- Any mention of Jewish heritage or Jewish identity (Єврей, Єврейка, єврейського походження, "of Jewish origin," Jewish surname patterns without explicit nationality statement)
- Explicit Polish nationality with any possible Ukrainian connection (born in Ukrainian territory, worked in Ukrainian cultural institutions, wrote in Ukrainian)
- Explicit German, Austrian, or Austro-Hungarian origin with any Ukrainian connection
- Armenian, Greek, or other minority nationality with Ukrainian regional connection
- "Soviet" as the primary nationality label without an underlying national identity specified
- Born outside Ukraine entirely but with significant creative career in Ukraine
- Dual or multiple nationality descriptors in the same entry
- Any phrasing suggesting disputed or complex national identity in the text

**Volume:** 1,356 entries were flagged for Tier 2 Claude review.

### 6.4 Claude Nationality Review Protocol

Each Tier 2 entry was reviewed by Claude (claude-sonnet-4-6) using the following protocol:

**Model:** claude-sonnet-4-6
**Temperature:** Default (1.0)
**Max tokens:** 500 (sufficient for a classification with brief reasoning)
**Language of input:** Ukrainian (the full ESU biographical text was passed in Ukrainian)
**Language of output:** English (for ease of logging and review)

**Verbatim prompt used:**

```
You are helping classify whether a person should be counted as a Ukrainian creative worker for an academic study about Soviet-era mortality.

Here is the full biographical text from the Encyclopedia of Modern Ukraine for this person:

---
[FULL_ESU_TEXT_IN_UKRAINIAN]
---

Please classify this person as one of:
- INCLUDE: This person should be counted as a Ukrainian creative worker. They participated substantially in Ukrainian cultural life, worked in Ukrainian language or with Ukrainian themes, or identified as Ukrainian, regardless of ethnic heritage.
- EXCLUDE: This person should NOT be counted as a Ukrainian creative worker. They were a foreign artist referenced for their influence on Ukrainian culture, or a Soviet-era figure with no authentic Ukrainian cultural connection.
- UNCERTAIN: The text does not contain enough information to make a confident determination.

Reply with ONLY the classification word (INCLUDE, EXCLUDE, or UNCERTAIN) followed by a colon and a single sentence of reasoning. Example: "INCLUDE: Born in Lviv, wrote exclusively in Ukrainian, and was a member of the Ukrainian Writers' Union."

Do not add any other text.
```

**Handling of UNCERTAIN responses:** Entries classified as UNCERTAIN by Claude were excluded from the dataset rather than manually reviewed, to avoid the introduction of researcher bias in ambiguous cases.

**Results of Claude review:**
- INCLUDE: 137 entries
- EXCLUDE: 1,218 entries
- UNCERTAIN: 1 entry (excluded)

### 6.5 Tier 3: Auto-Exclusion

Entries with explicit non-Ukrainian nationality markers and no Ukrainian connection markers were excluded without Claude review. The full list of auto-exclusion nationality markers is provided in Section 4.7.

### 6.6 Error Rate Estimation for Nationality Review

**Recommended Phase 5 human sample check procedure:**

To estimate the error rate in Claude's nationality classifications, a researcher should perform the following:

1. Randomly sample 100 entries from the INCLUDE classifications and 100 entries from the EXCLUDE classifications (200 total).
2. For each sampled entry, read the full ESU biographical text (in Ukrainian) and independently classify it as INCLUDE or EXCLUDE according to the criteria in Section 6.4.
3. Record any disagreements between the human classification and Claude's classification.
4. Calculate: error rate = (number of disagreements / 200) × 100%.
5. If the error rate exceeds 5%, the Claude classifications should be reviewed more carefully and potentially re-run with a refined prompt.
6. If the error rate is below 5%, report it in the published paper as the estimated Claude classification error rate.

**Important:** The human reviewer should not know Claude's classification before making their own determination. Review Claude's classification only after recording your own.

**Actual error rate (Phase 5b validation, completed 2026-04-03):** 3.2% (2 errors in 62 reviewable entries; 1 entry excluded from denominator as indeterminate). Seed=99, n=63 drawn randomly from the classified dataset.

**Deviation from recommended procedure:** The procedure above specifies 100 INCLUDE + 100 EXCLUDE = 200 entries stratified by classification outcome. The validation as conducted drew a single unstratified random sample of 63 entries, of which the INCLUDE/EXCLUDE split was not recorded separately. This means category-specific error rates (false positive rate for INCLUDEs vs false negative rate for EXCLUDEs) cannot be computed from the existing validation. The 3.2% overall rate carries a wide 95% CI (approximately 0.9%–7.9% by exact binomial) given n=62. A stratified 200-entry validation remains recommended for V3 prior to journal submission.

---

## 7. Migration Classification Rules

> **⚠ REVISED V2.1 — 2026-04-03:** Phase 5 human accuracy check found that the original two-group classification system collapsed four meaningfully distinct populations into two, introducing systematic error. The system below replaces the original two-group system with a four-group classification. See AI_METHODOLOGY_LOG.md (Phase 5 — Methodological Corrections) for full rationale.

### 7.1 Classification Categories

Each confirmed Ukrainian creative worker with complete date data was classified into one of four migration categories:

**MIGRATED:** The individual left the Soviet sphere entirely and settled in a non-Soviet country for a substantial portion of their adult life. The critical criterion is exit from the Soviet sphere — not merely from Ukraine. Only emigration to non-Soviet territory (Western Europe, North America, South America, non-Soviet Asia) qualifies.

**NON-MIGRATED:** The individual remained within the Ukrainian SSR for their working life, with no significant period of residence outside Soviet-controlled territory.

**INTERNAL_TRANSFER:** The individual voluntarily relocated from the Ukrainian SSR to another Soviet republic (Russia, Belarus, Central Asia, etc.) and spent a substantial portion of their adult life there. They remained within the Soviet sphere and experienced Soviet conditions, but in a different republic. This is a voluntary choice distinct from deportation.

**DEPORTED:** The individual was forcibly displaced by Soviet authorities — through formal state deportation orders, Gulag imprisonment followed by exile in another region, assignment as a "special settler" (спецпоселенець) in a designated zone, or any other state-ordered relocation that removed individual choice. **The defining criterion is that the Soviet state made the movement decision, not the individual.** Destination is irrelevant — deportation to Kazakhstan, Siberia, or a Donbas labour camp all qualify. Deported individuals experienced Soviet conditions as direct victims of state violence, not as passive residents.

**EXCLUDED (indeterminate):** Migration status could not be determined, emigration was temporary (individual returned to Soviet Ukraine), or emigration occurred after age 70.

---

**Role in primary analysis:**

| Group | Role |
|-------|------|
| `migrated` | Primary comparison group (escaped Soviet sphere) |
| `non_migrated` | Primary comparison group (remained in Ukrainian SSR) |
| `internal_transfer` | Reported separately as third comparison group |
| `deported` | Reported separately as fourth group; grouped with `non_migrated` in primary LE comparison |

---

### 7.2 Detailed Classification Rules

**Classified as MIGRATED if:**
- The ESU biographical text states explicitly that the person emigrated, fled, or left for a named non-Soviet country (e.g., Germany, France, USA, Canada, Czechoslovakia, Poland post-WWII, etc.)
- The text mentions membership in a diaspora institution (e.g., Ukrainian Free Academy of Sciences / УВАН, Ukrainian Academy of Arts and Sciences in the US, Shevchenko Scientific Society in Sarcelles, Ukrainian Institute in London, Prosvita in the diaspora, etc.)
- The text mentions publication in diaspora press (e.g., Svoboda, Ukrainske Slovo (Paris), Novy Shliakh, etc.)
- The text describes permanent settlement abroad with specific non-Soviet country or city mentioned
- The person is described as a representative of the Ukrainian diaspora (діаспора, еміграція)
- The person emigrated during the first wave (1917–1921) or second wave (1941–1945) and there is no mention of return

**Classified as NON-MIGRATED if:**
- The text contains no mention of emigration or life abroad
- The text explicitly states the person lived and worked in Soviet Ukraine throughout their career
- The text mentions wartime evacuation within Soviet territory (e.g., to Central Asia, Siberia, Urals) with return to Soviet Ukraine after the war

**Classified as INTERNAL_TRANSFER if:**
- The person voluntarily relocated to Soviet Russia, Soviet Belarus, or another Soviet republic
- Their ESU entry describes a career based primarily in another Soviet city (Moscow, Leningrad, Minsk, Tashkent, etc.) without any indication of forced displacement
- There is no mention of arrest, Gulag, exile orders, or state-mandated relocation
- The move was career-motivated or voluntary in character

**Classified as DEPORTED if:**
- The text mentions arrest by Soviet authorities followed by Gulag imprisonment (ув'язнення, табір, ГУЛАГ)
- The text uses "заслання" (exile), "спецпоселення" (special settlement), or describes assignment to a restricted zone
- The text references NKVD, MGB, KGB action against the individual resulting in relocation
- The individual was described as "репресований" (repressed) with geographic displacement as a result
- The text describes deportation of an ethnic community to which the individual belonged (e.g., Crimean Tatar mass deportations of 1944)
- **Priority rule:** If there is any evidence of forced displacement, classify as DEPORTED before considering INTERNAL_TRANSFER. Voluntary and forced displacement must not be conflated.

**Classified as EXCLUDED (indeterminate) if:**
- Emigration is mentioned but the destination is unclear
- The person's postwar fate is unknown or described as unknown in the text
- The person emigrated but returned to Soviet Ukraine
- The person emigrated after age 70
- The biographical text is too short or vague to determine migration status

### 7.3 Claude Migration Classification Protocol

For entries where migration status was ambiguous after applying the rules above, Claude was used as a secondary reviewer.

**Model:** claude-sonnet-4-6
**Temperature:** Default (1.0)
**Max tokens:** 500

**Verbatim migration classification prompt (revised V2.1):**

```
You are helping classify the migration status of a Ukrainian creative worker for an academic study about Soviet-era life expectancy.

Here is the full biographical text from the Encyclopedia of Modern Ukraine for this person:

---
[FULL_ESU_TEXT_IN_UKRAINIAN]
---

Please classify this person's migration status as exactly one of these four categories:

- MIGRATED: This person left the Soviet sphere entirely and settled in a non-Soviet country (Western Europe, North America, South America, non-Soviet Asia) for a substantial portion of their adult life. Moving to Soviet Russia or another Soviet republic does NOT qualify as migrated.

- NON_MIGRATED: This person remained within the Ukrainian SSR for their working life with no significant period outside Soviet-controlled territory.

- INTERNAL_TRANSFER: This person voluntarily relocated to another Soviet republic (Russia, Belarus, Central Asia, etc.) and based their career there. There is no evidence of forced displacement — the move appears career-motivated or voluntary.

- DEPORTED: This person was forcibly displaced by Soviet authorities — through Gulag imprisonment, state deportation orders, special settler assignment, or any other state-mandated relocation. The defining criterion is that the Soviet state decided the movement, not the individual. Classify as DEPORTED even if the destination was within Ukraine (e.g., a labour camp in Donbas).

- INDETERMINATE: The text does not contain enough information to classify with confidence.

IMPORTANT: If there is any evidence of forced displacement by Soviet authorities, classify as DEPORTED rather than INTERNAL_TRANSFER. Do not conflate voluntary relocation with state-imposed exile.

Reply with ONLY the classification word (MIGRANT, NON-MIGRANT, or INDETERMINATE) followed by a colon and a single sentence of reasoning. Example: "MIGRANT: Fled to Germany in 1943 and later settled in New York, where they published with Ukrainian diaspora press."

Do not add any other text.
```

**Handling of INDETERMINATE:** Entries classified as INDETERMINATE were excluded from the primary analysis dataset.

### 7.4 Key Disambiguation Cases

**Soviet internal exile vs. emigration:** An individual who was arrested and sent to a labour camp in Kazakhstan, Siberia, or another Soviet republic but was later released and returned to Soviet Ukraine is classified as NON-MIGRANT. Internal displacement within the Soviet Union does not constitute emigration for our purposes.

**Wartime occupation territory:** Individuals who remained in German-occupied Ukraine during WWII but were not under Soviet authority are still classified as NON-MIGRANT (they did not emigrate; they were occupied). Occupation is distinct from emigration.

**Ostarbeiters and forced labourers:** Individuals taken to Germany as forced labourers during WWII are classified case by case:
- If they returned to Soviet Ukraine after the war: NON-MIGRANT
- If they remained in West Germany or emigrated elsewhere after the war: MIGRANT
- If their postwar fate is unknown: INDETERMINATE / EXCLUDED

**Born outside Soviet territory, worked in Ukraine:** Artists born in Galicia before its Soviet annexation (1939) or in other non-Soviet Ukrainian territories who later came under Soviet control are classified based on their status after Soviet annexation: if they subsequently emigrated, MIGRANT; if they remained under Soviet rule, NON-MIGRANT.

---

## 8. Statistical Methods

### 8.1 Life Expectancy Calculation

Life expectancy (age at death) was calculated for each individual as:

```
age_at_death = death_year - birth_year
```

This calculation is performed in integer years (year-level precision), as the ESU does not consistently record month and day of birth and death for all individuals. The result is an integer between 0 and approximately 110.

No actuarial adjustments were applied. We do not use period life tables, cohort life tables, or demographic survival curve methods. We report raw age at death as the simplest, most transparent, and most reproducible measure of longevity for this dataset.

**Note on age 0 deaths:** Cases where death_year = birth_year yield an age at death of 0, which is possible (infant mortality) but likely also includes some data entry errors. Such cases were flagged and reviewed before inclusion.

### 8.2 Central Tendency Measures

We report both arithmetic mean and median for each group.

**Mean:** The arithmetic average of all ages at death in the group. Sensitive to outliers. Reported because it is the most widely understood summary statistic and is necessary for Cohen's d calculation.

**Median:** The middle value when all ages at death are sorted in ascending order. Robust to outliers. Reported because the non-migrant distribution is substantially left-skewed (heavy tail of young deaths from political violence), which causes the mean to understate the typical longevity experience of the majority.

### 8.3 Standard Deviation

Standard deviation (SD) was calculated as the population standard deviation of ages at death within each group:

```
SD = sqrt( sum((x_i - mean)^2) / n )
```

The SD is reported as a descriptor of the spread of the distribution within each group, not as an inferential statistic.

### 8.4 Mann-Whitney U Test

The Mann-Whitney U test (also called the Wilcoxon rank-sum test) was used as the primary statistical significance test for the difference in life expectancy between migrants and non-migrants.

**Rationale for choice over t-test:** The t-test assumes that both samples are drawn from normally distributed populations. The non-migrant life expectancy distribution is substantially non-normal: it has a pronounced left skew due to the excess of premature deaths from political violence (the mass executions of the 1930s produce a cluster of deaths in the 25–55 age range that creates a left tail absent from a normal distribution). The Mann-Whitney U test makes no parametric distributional assumption; it tests whether values from one population tend to be larger or smaller than values from another, using ranks rather than raw values. It is therefore the appropriate test for this data structure.

**Implementation:** Implemented using `scipy.stats.mannwhitneyu` in Python, with `alternative='two-sided'` for the hypothesis test (testing whether the two distributions differ in either direction, not just whether migrants live longer).

**Interpretation of p-value:** The p-value from the Mann-Whitney U test represents the probability of observing a rank difference at least as extreme as the one we observed, under the null hypothesis that the two groups were drawn from the same distribution. A p-value of approximately 0.0 (smaller than any representable floating-point value in standard scientific notation) means this probability is vanishingly small; we reject the null hypothesis with overwhelming confidence.

### 8.5 Cohen's d

Cohen's d is a standardised effect size measure that expresses the difference in group means in units of standard deviations. It is calculated as:

```
d = (mean_migrants - mean_non-migrants) / pooled_SD
```

where pooled SD is calculated as:

```
pooled_SD = sqrt( ((n1 - 1) * SD1^2 + (n2 - 1) * SD2^2) / (n1 + n2 - 2) )
```

with n1 = 1,038 (migrants), n2 = 5,272 (non-migrants), SD1 = 14.47, SD2 = 15.04.

**Interpretation benchmarks (Cohen, 1988):**
- d = 0.2: Small effect
- d = 0.5: Medium effect
- d = 0.8: Large effect

Our value of d = 0.319 falls in the medium range, indicating that the life expectancy difference, while not large enough to be obvious in individual comparisons, is large enough to be practically and clinically meaningful at the population level.

**Implementation:** Calculated using `numpy` operations in Python; verified against `pingouin.compute_effsize` for consistency.

**Note on distributional assumptions:** Cohen's d benchmarks (0.2 small / 0.5 medium / 0.8 large) assume normality and are applied here for comparability with prior literature. For this demonstrably non-normal distribution (see §8.4), the appropriate non-parametric effect size is Cliff's delta (δ), which is calculated in the companion analysis script and reported alongside Cohen's d in the paper. Cliff's delta measures P(migrant > non-migrant) − P(non-migrant > migrant) and requires no distributional assumptions.

### 8.6 Period Analysis

Deaths among non-migrants were grouped by the year of death into the following historical periods, chosen to align with established historiographic periodisation of Soviet Ukrainian history:

| Period label | Year range | Historical rationale |
|---|---|---|
| Pre-1917 | Before 1917 | Pre-Soviet baseline; Imperial Russian period |
| Revolution/Civil War | 1917–1921 | Bolshevik consolidation, Ukrainian People's Republic, civil war |
| Early Soviet/NEP | 1922–1929 | New Economic Policy; relative liberalisation before Stalinism |
| Holodomor/First Five-Year Plan | 1930–1933 | Collectivisation, Holodomor, acceleration of Soviet nationalisation |
| Great Terror | 1934–1938 | Stalinist mass repression; Executed Renaissance |
| World War II | 1939–1945 | Soviet-German pact, German invasion, occupation, liberation |
| Late Stalinist | 1946–1953 | Post-war Stalinism; Zhdanovshchina; late repressions |
| Khrushchev Thaw | 1954–1964 | De-Stalinisation; relative cultural liberalisation |
| Late Soviet | 1965–1991 | Brezhnev stagnation through Gorbachev reforms and independence |
| Post-1991 | 1992 onwards | Independent Ukraine |

For each period, two statistics were calculated:
- Count of non-migrant deaths occurring within the period
- Average age at death of non-migrants who died within the period

**Note — important caveat on death-year assignment:** Period assignment uses year of *death*, not year of *repression event*. An individual executed in 1937 is assigned to the Great Terror period (1934–1938). An individual arrested in 1937, who survived Gulag imprisonment and died in 1961, is assigned to the Khrushchev Thaw period — even though their period of maximum persecution was 1937.

This means the 1934–1938 Great Terror window **systematically undercounts** Terror-era deaths: workers arrested during the Terror but dying in Gulag camps throughout the 1940s and 1950s are spread across later period buckets. The period analysis captures direct executions and near-term deaths, not the full delayed mortality impact of repression. Readers should treat period death counts as lower bounds for repression-caused mortality in each window.

### 8.7 Birth Cohort Analysis

Workers were grouped by birth decade (1870s, 1880s, 1890s, 1900s, 1910s, 1920s). For each decade-of-birth cohort, average life expectancy was calculated separately for migrants and non-migrants, and the gap (migrant minus non-migrant) was reported.

Cohorts with fewer than 20 individuals in either the migrant or non-migrant group were flagged as underpowered; results for such cohorts should be interpreted with caution.

### 8.8 Profession-Level Analysis

For each of the six profession categories, average life expectancy was calculated separately for migrants and non-migrants. The same statistical approach (means, medians, gap) was applied. Full Mann-Whitney U testing was not performed at the profession level due to smaller sample sizes in some categories (particularly Theatre/Film migrants, n=53), but direction of effect was consistent across all categories.

### 8.9 Cox Proportional Hazards Model (Added V2.4)

**Python library:** `lifelines` (already used for Kaplan-Meier). Class: `CoxPHFitter(penalizer=0.01)`.

**Sample:** n = 8,643 (identical to OLS). All observations have `event_observed = 1` (confirmed deaths only; living individuals excluded, not right-censored — matches OLS sample).

**Models:**
- Model 1 (unadjusted): migration dummies only (reference = non_migrated)
- Model 2 (adjusted): + birth_decade (standardised z-score) + profession dummies + birth_region dummies

**Output:** Hazard ratios (HR), 95% CI, p-values. HR < 1 = lower mortality hazard = longer survival vs reference.

**Key results:** Migrated HR = 0.76 (Model 2, 95% CI [0.71–0.81]); Deported HR = 5.40 (Model 2, 95% CI [4.64–6.27]); Internal Transfer HR = 1.08 (Model 2, 95% CI [1.01–1.15]). Full output saved to `cox_output.txt`.

### 8.10 Propensity Score Matching (Added V2.4)

**Python library:** `sklearn.linear_model.LogisticRegression` (max_iter=500, solver='lbfgs').

**Purpose:** Partially address healthy-migrant selection effects on the migrated/non-migrated gap.

**Sample:** migrated (n=1,280) + non_migrated (n=6,030); internal transfer and deported excluded.

**Covariates:** birth_decade (continuous), profession_code (categorical integer), birth_region_code (categorical integer). Standardised before logistic regression.

**Method:** Estimate propensity score (P(migrated) given covariates) for each individual. Greedy nearest-neighbour matching: each migrated worker matched to the closest non-migrated worker by propensity score distance (no replacement). Matched n = 1,280 pairs.

**Uncertainty:** 95% CI estimated by bootstrap (2,000 resamples, random seed=42) of the matched-sample mean gap.

**Result:** PSM gap = +3.35 yrs (bootstrap 95% CI: [2.26, 4.45]). Full-sample gap for reference: +4.04 yrs. Gap attenuation after matching: 17%. Residual gap after matching is not explained by observable birth-cohort, profession, or region differences.

### 8.11 Right-Censored Cox PH Analysis — V2.4 (Supersedes V2.3/V2.5 approach)

**Purpose:** Fit a properly right-censored Cox PH model that includes all 6,314 living individuals with their migration status correctly classified, enabling valid survival inference across all four migration groups.

**Key change from V2.3/V2.5:** V2.3 assigned all living individuals to `non_migrated` (structural flaw — produced 52.2% censoring in non-migrated vs 0% in all other groups, making HRs non-comparable). V2.4 uses the same two-stage AI classification pipeline (Claude Haiku → Sonnet retry) applied to all 6,563 living individuals to determine migration status before including them in the extended dataset.

**Living cohort classification pipeline:**
- Input: `data/living_individuals_for_classification.csv` (6,563 rows, filtered from raw ESU: has birth_year, not flag_non_ukrainian, has notes)
- Method: `classify_living.py` — 30 parallel Claude Code subagents processing ~219-row chunks (API credit exhausted; subscription-covered subagent approach used as free alternative)
- Haiku first pass, Sonnet deep retry for unknowns
- Stage 3 edge-case review: Operation Vistula reclassification (Polish state, not Soviet deportation → non_migrated), post-Soviet emigrant flagging (64 individuals), implausibly alive flagging (185 born <1920)
- Output: `data/living_individuals_classified.csv` → `data/living_individuals_cleaned.csv`

**Extended dataset:** N = 15,053 (dead=8,739 + right-censored=6,314). Note: 246 dead rows dropped for null duration; 249 living rows dropped for filtering.
- Duration (dead): death_year − birth_year; event_observed = 1
- Duration (living): 2026 − birth_year; event_observed = 0
- Implausibly alive (born <1920, n=185): reclassified as event_observed=1, duration=80

**Censoring distribution (V2.4):**
| Group | n | % Dead | % Censored |
|-------|---|--------|-----------|
| non_migrated | 11,898 | 51.1% | 48.9% |
| migrated | 1,646 | 80.2% | 19.8% |
| internal_transfer | 1,313 | 88.3% | 11.7% |
| deported | 196 | 93.9% | 6.1% |

**Models:** `CoxPHFitter(penalizer=0.1)`. Model 1: migration dummies only. Model 2: migration + birth_decade dummies + profession dummies + region dummies. Reference: non_migrated.

**Results (Model 2 adjusted):**
| Group | HR | 95% CI | p |
|-------|----|--------|---|
| migrated | 0.832 | 0.778–0.889 | <0.0001 |
| internal_transfer | 1.105 | 1.033–1.182 | 0.0038 |
| deported | 4.646 | 3.908–5.524 | <0.0001 |

Concordance index (Model 2): 0.724.

**Unadjusted → adjusted reversal for migrated (HR 1.088 → 0.832):** The non-migrated group has ~49% right-censoring vs 20% for migrated. This asymmetry artificially lowers the non-migrated baseline hazard in unadjusted analysis. Covariate adjustment (birth cohort especially) corrects for this, restoring the migrated survival advantage.

**Schoenfeld residuals PH test:** PH violated for deported (p<0.0001) and migrated (p=0.011). Internal transfer borderline (p=0.066). Reported HRs are average effects over follow-up. Stratified Cox or time-varying coefficient models would be appropriate robustness checks.

**Sensitivity analyses (§8.12):** Three scenarios tested — see below.

**Figures generated:**
- `fig24_cox_forest_plot.png` / `fig24_interactive.html` — forest plot, Model 1 + Model 2 HR comparison
- `fig25_censoring_pattern.png` / `fig25_interactive.html` — stacked bar: % dead vs censored by group (V2.4)
- `fig26_km_censored.png` / `fig26_interactive.html` — KM survival curves with right-censored tick marks (V2.4)

**Code location:** `stage5_cox.py`, `stage7_figures.py`. Model output: `results/cox_censored_output.txt`.

### 8.12 Sensitivity Analyses for Right-Censored Cox Model (V2.4)

**Purpose:** Test robustness of the migrated HR (0.832) to three sources of potential misspecification.

**All sensitivity models use unadjusted Model 1** (migration dummies only) for computational tractability. The adjusted baseline is from §8.11 Model 2.

**Scenario A — Implausibly alive age assumption:**
185 individuals born before 1920 with no death record (would be 106+ in 2026) reclassified as deceased. Five assumed death ages tested: 70, 75, 80, 85, 90. Migrated HR stable at 1.067–1.100 across all assumptions (all unadjusted; direction consistent, magnitude stable).

**Scenario B — Post-Soviet emigrant classification:**
62 living migrants born after 1960 flagged as likely post-Soviet emigrants. Three sub-scenarios: include all (HR=1.088), exclude from migrated group (HR=1.094), reclassify as non_migrated (HR=1.094). Maximum change: 0.006 HR units — negligible.

**Scenario C — Bootstrap misclassification:**
AI classification validated at 3.2% error rate (V2.1 Phase 5b, n=62 review). Bootstrap simulation: 50 iterations × random misclassification at 5%, 10%, 15% of all rows (random label swap from uniform distribution across 4 groups). Migrated median HR: 5%=1.088 (2.5–97.5%: 1.064–1.109), 10%=1.077 (1.048–1.110), 15%=1.083 (1.050–1.111). Direction and magnitude stable across all rates.

**Figure generated:**
- `fig27_sensitivity_summary.png` / `fig27_interactive.html` — migrated HR across all 12 sensitivity scenarios + baseline

**Code location:** `stage6_sensitivity.py`. Output: `results/sensitivity_output.txt`, `results/sensitivity_results.json`.

### 8.13 Time-Varying Hazard Analysis — Landmark Cox by Age Band (V2.4)

**Purpose:** Address the Schoenfeld PH assumption violation for the deported group (§8.11) by decomposing the single overall HR into age-band-specific HRs. Instead of treating the PH violation as a limitation, the landmark approach treats it as information: the variation in HR across age bands reveals *when* the excess killing was concentrated.

**Method:** For each 10-year age band [lo, hi], only individuals alive at age `lo` contribute. Duration is truncated at `hi`; event is flagged if death occurred before `hi`. A separate unadjusted Cox PH model (migration dummies only) is fitted within each band. The deported HR from each band-model is the excess mortality rate for deportees *within that age window*, relative to non-migrated.

**Script:** `stage8_timevarying.py`. Output: `results/timevarying_output.txt`.

**Results — Deported group HR by age band:**

| Age band | n at risk | Dep events | HR | 95% CI | p |
|----------|-----------|------------|----|--------|---|
| 20–30 | 14,994 | 10 | 1.09 | [0.90, 1.33] | 0.36 |
| 30–40 | 14,921 | 42 | 1.50 | [1.23, 1.82] | <0.001 |
| **40–50** | **14,619** | **50** | **1.86** | **[1.49, 2.33]** | **<0.001** |
| 50–60 | 13,771 | 27 | 1.57 | [1.19, 2.06] | 0.001 |
| 60–70 | 12,060 | 19 | 1.40 | [1.02, 1.93] | 0.037 |
| 70–80 | 8,580 | 13 | 1.19 | [0.82, 1.73] | 0.37 |
| 80–90 | 4,061 | 6 | 0.89 | [0.54, 1.48] | 0.66 |

**Key summary:** Peak HR 1.86 at age 40–50; collapses to near-null (HR=0.89) by age 80–90. Workers born ~1890–1910 (Executed Renaissance generation) were in their 30s–40s during the 1937–38 Terror — exactly the peak band.

**Interpretation:** The single HR=4.646 in §8.11 is a lifetime average compressing a concentrated event. The landmark analysis shows the actual temporal structure: Soviet state killing was concentrated in a specific historical window (Terror + Gulag years), not a steady-state risk. Survivors who cleared that window converged back to baseline mortality by their 70s.

**Also generated:** Schoenfeld residual smoothed log-HR plot (fig28b), bootstrapped lowess confidence envelope. Confirms non-constant log-HR across age (positive slope in middle age, decline toward zero in old age).

**Figures generated:**
- `fig28_deported_hr_by_age.png` / `fig28_interactive.html` — landmark Cox HR by age band, deported group
- `fig28b_schoenfeld_smooth.png` — Schoenfeld residual smoothed log-HR, deported group

**Version note:** Added in V2.4, 2026-04-07. Directly addresses the Schoenfeld PH violation flagged in §8.11.

**Code location:** `stage8_timevarying.py`. Output: `results/timevarying_output.txt`.

---

## 9. AI Tools Used

### 9.1 Claude (Anthropic)

**Model:** claude-sonnet-4-6
**Provider:** Anthropic
**API endpoint:** `https://api.anthropic.com/v1/messages`
**Python library:** `anthropic` (latest version as of 2026)
**Temperature:** Default (1.0 for Claude models)

**Replication note on temperature:** Temperature 1.0 introduces sampling randomness — two runs of the same prompt on the same input text may return different classification results. For a fully deterministic and reproducible classification pipeline, future replications should use temperature=0. Additionally, best practice is to run each classification twice and report inter-run agreement; this was not done in the present study. This is a known reproducibility limitation that should be addressed in future work.
**Max output tokens:** 500 (for classification tasks)
**Top-p / Top-k:** Default
**System prompt:** None used (all instructions included in the user-turn prompt)

**Tasks performed:**
1. Nationality determination for 1,356 ambiguous entries (Section 6.4)
2. Migration classification for ambiguous entries (Section 7.3)

**Prompts:** Both verbatim prompts are documented in Sections 6.4 and 7.3 of this document.

**Cost:** API calls were billed per token. The nationality and migration review phases consumed approximately [X] million input tokens and [Y] thousand output tokens; exact figures available from the Anthropic API usage dashboard associated with the project account.

### 9.2 Claude as Writing Assistant

Claude was also used as a prose editing and writing assistance tool for the PAPER_DRAFT.md manuscript. All empirical content, analytical conclusions, and methodological decisions in the paper are those of the human authors. Claude's contribution was limited to phrasing, academic English style editing, and structural suggestions.

No AI tool was used to make decisions about study design, statistical methods, inclusion/exclusion criteria, or the interpretation of findings.

### 9.3 No Other AI Tools

No other AI tools (including GPT-4, Gemini, or other large language models) were used in this study. All classification tasks were performed by either deterministic rule application or Claude review.

---

## 10. Known Limitations

### 10.1 Source Limitations

**ESU is not a complete census.** The Encyclopedia of Modern Ukraine documents individuals whose work was considered significant enough for encyclopedic inclusion. This is not a random or representative sample of all Ukrainian creative workers. Specifically:
- Individuals who died young (especially by execution) may be underrepresented because they had less time to produce work justifying an encyclopedic entry.
- Very successful or long-lived individuals may be overrepresented.
- The ESU's editorial decisions about whom to include reflect scholarly and cultural priorities that may not be neutral with respect to migration status or political fate.

**The ESU is a living document.** Entries may be added, edited, or corrected over time. Our dataset reflects the state of the ESU at the time of our scraping. A replication using a different access date may yield different results due to editorial updates.

**Death date completeness.** Many individuals in the ESU do not have recorded death dates (either because they are still living or because the death date was not known to ESU editors). These individuals are excluded from our life expectancy analysis. If the individuals with missing death dates are systematically different from those with recorded death dates (e.g., if non-migrants who died in obscure circumstances during the Gulag are less likely to have confirmed death dates), this exclusion could bias our estimates.

### 10.2 Methodological Limitations

**Binary migration classification.** We classify individuals as either migrants or non-migrants, which is a simplification of a more complex reality. Some individuals emigrated temporarily; some emigrated late in life; some were expelled from the Soviet Union (effectively forced to emigrate) rather than choosing to leave; some lived in territories that changed sovereignty (Galicia, Bukovina) without having made any migratory choice. Our classification rules address the most common cases but cannot capture all of these nuances.

**Birth year as life expectancy denominator.** We calculate life expectancy as death year minus birth year. This captures age at death but does not account for period effects in mortality that would be captured by a more sophisticated demographic analysis using period life tables. Our measure is a retrospective biographical statistic, not a prospective actuarial estimate.

**Age at death vs. years lived under Soviet control.** Our primary measure is total age at death, not years lived under Soviet conditions. A non-migrant who lived 70 years but emigrated at age 60 would be classified as a migrant with 70 years of life expectancy, even though they experienced only 10 years of post-migration conditions. Conversely, a non-migrant who died at 70 experienced 70 years of Soviet conditions. This is a limitation of our measure; years lived under Soviet control would be a more direct measure of exposure but would require more detailed biographical data.

**AI classification errors.** As documented in Section 6.6, we estimate an error rate below 5% in Claude's nationality classifications. A 5% misclassification rate across 1,356 reviewed entries would mean approximately 68 individuals are in the wrong category. This is unlikely to substantially affect the overall life expectancy gap given the large dataset size (n=6,310), but it could affect subgroup estimates. Our estimates should be treated as having an error tolerance consistent with this classification uncertainty.

### 10.3 Causal Limitations

**No causal identification.** This is an observational study. We cannot randomly assign Ukrainian creative workers to migrate or stay. The life expectancy gap may reflect, in part or in whole, pre-migration differences between the groups:
- Migrants may have been wealthier, better-connected, or healthier at the time of emigration.
- Migrants from western Ukraine (Lviv, Ternopil, Chernivtsi) may have had different baseline health profiles from non-migrants in eastern Ukraine.
- The decision to migrate was correlated with ideological stance, social network, and professional activity — all of which may have been correlated with health behaviours.

The birth cohort analysis provides some evidence against a pure selection explanation (the gap nearly disappears for the 1920s cohort, who were subject to the same selection pressures as the 1880s and 1890s cohorts), but it does not fully resolve the question.

**No control group outside Ukraine.** We do not have life expectancy data for non-Ukrainian creative workers in the Soviet Union or for Ukrainian creative workers in countries without Soviet influence, which would be needed to separate the "Ukrainian creative worker" component of the mortality gap from the "Soviet conditions" component.

### 10.4 What This Study Can and Cannot Claim

**CAN claim:**
- There was a statistically robust and practically meaningful mean age at death gap of 4.04 years between Ukrainian creative workers who emigrated from the Soviet Union and those who remained, in a dataset of 8,643 individuals (V2.3).
- This gap is larger in cohorts born before 1910 (the Executed Renaissance generation) than in those born after 1920.
- Average age at death among non-migrant Ukrainian creative workers was anomalously low during the Great Terror (1934–1938) and World War II (1939–1945), consistent with mass political violence.
- Migration rates among Ukrainian creative workers were substantially higher in western Ukrainian cities than in eastern Ukrainian cities.

**CANNOT claim:**
- That the life expectancy gap is entirely caused by Soviet repression (selection effects cannot be ruled out).
- That the typical Ukrainian creative worker who stayed in the USSR lost exactly 4.77 years of life as a result of that choice.
- That findings about the ESU population generalise to all Ukrainian creative workers or all Soviet subjects.
- That there were no life expectancy costs of emigration (exile brought its own hardships; we measure outcomes, not mechanisms).

---

## 11. Data Availability

### 11.1 Primary Data File (V2.3)

**Filename:** `esu_creative_workers_v2_3.csv`
**Location:** `ukraine_v2/esu_creative_workers_v2_3.csv` (project git repository)
**Format:** CSV, UTF-8 encoded, comma-separated
**Rows:** 16,215 — one row per individual in the initial dataset
**Analysable rows:** 8,643 (migration_status in: migrated, non_migrated, internal_transfer, deported, AND valid birth/death years with age 10–110)

**Previous versions archived:**
- V2.2: `esu_creative_workers_v2_2.csv` (8,830 analysable — unchanged reference dataset; 19 impossible-age entries not yet excluded)
- V2.1: `archive/v2_1/esu_creative_workers_v2_1.csv` (6,106 analysable — contains date parsing errors)
- Raw scrape: `esu_creative_workers_raw.csv` (no classification, no date recovery)

### 11.2 Column Descriptions

| Column name | Data type | Description |
|---|---|---|
| `id` | integer | Internal numeric ID assigned during scraping |
| `esu_article_id` | integer | ESU article ID from the URL (esu.com.ua/article-XXXXX) |
| `name_ukrainian` | string | Full name in Ukrainian (as in ESU) |
| `name_transliterated` | string | Name transliterated to Latin characters |
| `birth_year` | integer or null | Year of birth (null if not available or uncertain) |
| `death_year` | integer or null | Year of death (null if not available, uncertain, or person is living) |
| `birth_city` | string or null | City of birth as listed in ESU |
| `birth_city_modern` | string or null | Standardised modern name of birth city |
| `professions_raw` | string | Profession labels as listed in ESU (pipe-separated if multiple) |
| `profession_category` | string | Our assigned profession category (from the 6-category taxonomy) |
| `nationality_tier` | integer | 1 = clean Ukrainian, 2 = Claude reviewed, 3 = auto-excluded |
| `nationality_decision` | string | INCLUDE, EXCLUDE, or UNCERTAIN |
| `nationality_reasoning` | string or null | Claude's one-sentence reasoning (for Tier 2 entries) |
| `migration_status` | string | MIGRANT, NON_MIGRANT, or EXCLUDED |
| `migration_source` | string | RULE (classified by rule) or CLAUDE (classified by Claude) |
| `migration_reasoning` | string or null | Claude's one-sentence reasoning (where applicable) |
| `age_at_death` | integer or null | Calculated as death_year - birth_year; null if either date missing |
| `included_in_analysis` | boolean | True if this row is included in the primary life expectancy analysis |
| `exclusion_reason` | string or null | Reason for exclusion (if included_in_analysis is False) |
| `esu_text_excerpt` | string | First 500 characters of the ESU biographical text (truncated for file size) |
| `scrape_date` | date | Date the ESU entry was scraped |

### 11.3 Raw Data File

**Filename:** `esu_creative_workers_raw.csv`
**Location:** `ukraine_v2/esu_creative_workers_raw.csv` (project git repository)
**Description:** The raw output from the scraper before any nationality or migration classification. Contains all entries that matched the creative profession keywords. This file is the starting point for any replication; all subsequent processing steps are applied to this file programmatically.

### 11.4 Reproducing the Dataset (V2.3 full pipeline)

> **Note on file locations:** All scripts and data files referenced below are available in the project git repository. Local paths used during development should be replaced with paths relative to the repository root when replicating.

To reproduce the V2.3 primary analysis dataset from scratch:

1. **Scrape ESU:** Run `esu_scraper.py` to re-scrape the ESU. Takes several days at a polite rate. Produces `esu_creative_workers_raw.csv`. Note: a fresh 2026+ scrape may differ from our snapshot due to ESU editorial updates. Use `diagnose_scraper.py` to verify that all letter-index pages were scraped correctly (checks pagination counts and presence of known entries).

2. **Classify nationality + migration:** Run `claude_review.py` to perform nationality (Tier 1/2/3) and migration classification using Claude Haiku. Produces intermediate classified CSV.

3. **Recover corrupted dates:** Run `fix_dates_v2.py --write --reclassify` on the classified CSV. This recovers birth/death years for entries where the ESU scraper's original regex failed (Old Style dates with nested parentheses; pseudonym prefixes). V2.2 recovered 8,971 entries this way. The script also flags entries needing migration re-classification.

4. **Re-classify flagged entries:** After date recovery, `fix_dates_v2.py` uses keyword shortcuts (Sandarmokh, розстріляний, ГУЛАГ signals) for obvious cases, then calls `claude_review.py`'s `run_migration_phase()` for the remainder. This brings previously "alive" or wrongly excluded entries back into the analysable dataset.

5. **Add death causes:** Run `add_death_cause.py` on the V2.2 CSV. Uses Claude Haiku to classify cause of death (natural / executed / gulag / exile / repression_other / wwii_combat / wwii_occupation / suicide / accident / unknown) from ESU biographical text.

6. **Add gender:** Run `add_gender.py` on the V2.2 CSV. Uses rule-based name-ending detection (Ukrainian feminine suffixes) + Claude Haiku fallback for ambiguous cases.

7. **Apply V2.3 corrections and reclassify unknowns:** Run `reclassify_unknowns.py` on the V2.2 output. This script: (a) applies three manual corrections (Куліш, Квітко, Маркіш — see AI_METHODOLOGY_LOG.md Phase V2.3-A); (b) reclassifies 19 impossible-age entries to `excluded_bad_dates`; (c) re-submits 196 `unknown` migration_status entries to Claude Haiku/Sonnet for a second classification attempt. Output: `esu_creative_workers_v2_3.csv`.

8. **Generate analysis + charts:** Run `generate_analysis.py` (with `CSV_PATH` pointing to `v2_3.csv`) to compute all LE statistics, run Mann-Whitney U tests, Cohen's d, and generate all 24 figures.

**Exact reproduction note:** Re-running `claude_review.py`, `add_death_cause.py`, and `reclassify_unknowns.py` will make new API calls to Claude and may produce slightly different classifications (stochastic LLM output). For exact numerical reproduction, use the archived `esu_creative_workers_v2_3.csv` directly.

**Estimated cost for full re-run from scratch:** ~$4–10 (Claude Haiku/Sonnet at current API pricing, 2026). V2.3 corrections step alone: ~$0.20.

---

## 12. Scripts

The following scripts are located in `/Users/symkinmark_/projects/Ai agent basic/ukraine_v2/`.

### 12.1 `esu_scraper.py`

**Purpose:** Scrapes biographical entries from esu.com.ua.

**What it does:**
1. Reads a list of target article IDs (either from a pre-built index or by iterating through a range).
2. For each article ID, makes an HTTP GET request to `https://esu.com.ua/article-XXXXX`.
3. Parses the HTML response using BeautifulSoup to extract: name, birth year, death year, birth city, profession labels, and the full biographical text.
4. Applies the creative worker profession keyword filter (Section 5) to identify potentially relevant entries.
5. Saves matching entries to `esu_creative_workers_raw.csv`.

**Key parameters:**
- `REQUEST_DELAY`: seconds between requests (set to 2.0 for polite scraping)
- `MAX_RETRIES`: number of retry attempts on failed requests (set to 3)
- `BACKOFF_FACTOR`: exponential backoff multiplier for rate-limited requests

**Runtime:** Several days for a full ESU scrape. The scraper saves progress incrementally so it can be stopped and resumed.

**Dependencies:** `requests`, `beautifulsoup4`, `lxml`, `pandas`

### 12.1b `fix_dates_v2.py` (V2.2 addition)



**Purpose:** Recovers birth/death years that were silently dropped by the original ESU scraper regex.

**Root cause fixed:** The original scraper used `\(([^)]{5,200})\)` to extract the biographical parenthetical containing birth–death dates. This fails in two cases:
1. **Old Style/New Style dual dates** like `14(26). 04. 1890` — the inner `)` terminates the regex prematurely
2. **Pseudonym prefixes** like `(справж. – Real Name; 1887 – 1937)` — the em-dash after the pseudonym marker splits incorrectly, giving `birth_part = "(справж."` and `birth_year = None`

**Fix:** Instead of bracket-matching, the script extracts the bio-header by finding `) –` (closing paren + em-dash), which marks the end of the date block and start of the profession description. Immune to nested parentheses.

**What it does:**
1. For every row in the CSV, runs `extract_years(notes)` using the corrected algorithm
2. If result improves on existing birth_year/death_year → fills in / corrects
3. Detects and corrects "Курбас-style swaps" (birth year stored in death_year field due to parsing order failure)
4. Resets migration_status from `alive`/`excluded_pre_soviet` to `unknown` for rows with newly recovered death years
5. Applies keyword shortcuts for obvious repression cases (Sandarmokh, розстріляний, ГУЛАГ signals) before calling Claude
6. Writes corrected dataset to `esu_creative_workers_v2_2.csv`
7. Adds columns: `dates_fixed` (bool), `needs_migration_reclassify` (bool)

**Key functions:**
```python
def extract_bio_header(notes: str) -> str:
    """Find ') –' separator instead of bracket-matching."""
    m = re.search(r'\)\s*[–—]\s', notes)
    return notes[:m.start() + 1] if m else notes[:500]

def clean_pseudonym_prefix(text: str) -> str:
    """Strip (справж. – Name; ...) or (псевд.: ...; ...) prefixes."""
    text = re.sub(r'\((?:справж(?:нє)?\.?|псевд\.?:?)[^;]{0,120};\s*', '(', text)
    return text
```

**Runtime:** ~30 seconds (pure Python, no API calls for date recovery)
**Dependencies:** `pandas`, `re` (stdlib)

### 12.1c `diagnose_scraper.py` (V2.3 addition)

**Purpose:** Read-only audit tool to verify ESU scraper coverage. Confirms that all letter-index pages were scraped and identifies specific named individuals as present or absent from the ESU source database.

**What it does:**
1. Fetches every page of the ESU letter-index listing for specified alphabet letters (e.g. С: 69 pages, Т: 30 pages)
2. Verifies pagination logic by comparing detected page count against known working letters
3. Searches page HTML for specified individual names
4. Reports: pagination count per letter, presence/absence of target individuals, HTML structure of listings

**Key finding from V2.3 run:** Several prominent Ukrainian cultural figures (Тичина Павло, Рильський Максим, Стус Василь, Хвильовий Микола, Симоненко Василь) were confirmed absent from the ESU source database entirely — not a scraper failure. ESU is an ongoing encyclopedia; these articles are not yet published.

**Makes HTTP GET requests only. Writes nothing.**
**Runtime:** ~10–15 minutes (reads 200+ pages across 8 letters at polite rate)

### 12.1d `reclassify_unknowns.py` (V2.3 addition)

**Purpose:** Re-classify `unknown` migration_status entries from V2.2 using a second Claude pass, and apply manual V2.3 corrections.

**What it does:**
1. Reads `esu_creative_workers_v2_3.csv`
2. Applies three manual corrections: Куліш Микола Гурович (`death_cause` gulag→executed), Квітко Лев (status unknown→non_migrated, cause→executed), Маркіш Перец Давидович (`death_cause` gulag→executed)
3. Flags 19 impossible-age entries (age_at_death 0–9 yrs) as `excluded_bad_dates`
4. For all 196 entries with `migration_status = 'unknown'` and a recorded death year: fetches full ESU article bio, submits to Claude Haiku-4.5 (first pass), then Claude Sonnet-4.6 (deep retry if still unknown)
5. Saves incrementally every 10 entries (safe to interrupt and resume)

**Prompts used:** Same four-category `MIGRATION_SYSTEM` and `MIGRATION_DEEP_SYSTEM` prompts as `claude_review.py` (reproduced in this script for self-containedness)

**V2.3 results:** 77 entries newly classified; 119 remain `unknown` (genuinely unresolvable biographies)
**Runtime:** ~8–12 minutes for 196 entries
**API cost:** ~$0.20

### 12.2 `claude_review.py`

**Purpose:** Uses Claude to classify ambiguous nationality and migration cases.

**What it does:**
1. Reads `esu_creative_workers_raw.csv`.
2. Applies the Tier 1 and Tier 3 nationality classification rules (Sections 6.2 and 6.5) deterministically.
3. Flags Tier 2 entries with ambiguity markers for Claude review.
4. For each flagged entry, calls the Claude API with the nationality review prompt (Section 6.4).
5. Saves Claude's INCLUDE/EXCLUDE/UNCERTAIN classification and one-sentence reasoning to the dataset.
6. For entries classified as INCLUDE, applies the migration classification rules (Section 7.2).
7. For migration-ambiguous entries, calls the Claude API with the migration classification prompt (Section 7.3).
8. Saves migration classifications (MIGRANT/NON-MIGRANT/INDETERMINATE) to the dataset.
9. Calculates `age_at_death` and `included_in_analysis` flags.
10. Saves the completed dataset to `esu_creative_workers_reviewed.csv`.

**Key parameters:**
- `ANTHROPIC_API_KEY`: set as environment variable (do not hardcode in script)
- `MODEL_NAME`: `"claude-sonnet-4-6"` (update to newer Claude version if replicating in future)
- `MAX_TOKENS`: 500
- `RATE_LIMIT_DELAY`: seconds between API calls (set to 0.5 to respect API rate limits)

**Dependencies:** `anthropic`, `pandas`, `time`

**Important note on reproducibility:** Because Claude is a stochastic model, re-running this script will produce slightly different classifications. For exact reproducibility, use the archived `esu_creative_workers_reviewed.csv` rather than re-running.

### 12.3 `generate_analysis.py`

**Purpose:** Performs all statistical analysis and generates figures.

**What it does:**
1. Reads `esu_creative_workers_reviewed.csv` and filters to the `included_in_analysis == True` rows.
2. Calculates overall mean and median life expectancy for migrants and non-migrants.
3. Runs the Mann-Whitney U test (`scipy.stats.mannwhitneyu`).
4. Calculates Cohen's d.
5. Generates profession-level life expectancy breakdowns.
6. Assigns non-migrant deaths to historical periods and calculates period statistics.
7. Generates the 1937 spotlight analysis.
8. Generates birth cohort analysis.
9. Generates geographic (city-level) migration rate analysis.
10. Generates age-at-death distribution statistics (premature death rates, age 90+ rates).
11. Calls matplotlib/seaborn to generate all 24 figures and saves them to the `charts/` subdirectory. Notable visualisation decisions: fig06 uses split violins by gender (seaborn `split=True`, `hue='gender'`) so the male and female LE distributions are visible within each migration group; fig10 uses per-group fixed label directions to prevent numeric annotations overlapping at shared x-positions.
12. Writes summary statistics to `esu_analysis_results.txt` and `analysis_extended.txt`.

**Dependencies:** `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`

---

## 13. Error Rate Tracking

### 13.1 Claude Nationality Classification Error Rate

**Status: Partially completed (Phase 5b, 2026-04-03). Full stratified validation pending (V3).**

**What was done:** An unstratified random sample of 63 entries was drawn (seed=99) from the full classified dataset. Each entry was reviewed by the author against the §6.4 criteria. Of 63 sampled, 62 were reviewable (1 indeterminate); 2 were judged incorrectly classified. Overall error rate: **3.2%** (95% CI: ~0.9%–7.9%, exact binomial).

**What was not done — deviation from recommended procedure:**

The procedure below specifies 100 INCLUDE + 100 EXCLUDE = 200 entries, stratified by classification outcome, reviewed by a Ukrainian-fluent researcher independent of the primary analysis. The completed validation deviates in three ways:

1. **Sample size:** 63 reviewed vs 200 recommended (31% of target)
2. **Stratification:** Single unstratified draw rather than 100 per outcome class — category-specific false positive and false negative rates cannot be computed
3. **Reviewer independence:** Validation conducted by the study author, not an independent reviewer

As a result, the 3.2% figure should be treated as a directional estimate, not a publication-grade error rate. It is sufficient to power the sensitivity analysis (Figure 14) and establish that the error rate is below 5%, but it cannot support category-level claims about which classification types are most error-prone.

**Recommended full procedure (for V3 prior to journal submission):**

1. Extract all INCLUDE decisions and all EXCLUDE decisions from the reviewed dataset separately.
2. Randomly sample 100 from each class (200 total, fixed seed for reproducibility).
3. For each entry, have a Ukrainian-fluent reviewer read the full ESU biographical text and classify it independently, without seeing Claude's classification.
4. After completing all 200 independent classifications, compare to Claude's.
5. Record disagreements for INCLUDEs and EXCLUDEs separately (false positive rate and false negative rate).
6. Report overall error rate, category-specific rates, and directional bias.

**Reviewer qualifications:** Fluent in Ukrainian; familiar with Ukrainian 20th-century cultural history; independent of the primary analysis.

**Acceptable threshold:** Overall error rate below 5% acceptable. 5–10% should be flagged as a limitation with impact discussion. Above 10% should trigger prompt revision and re-classification.

### 13.2 Claude Migration Classification Error Rate

**Status: Not yet completed. Recommended for V3.**

A parallel error rate assessment covering migration status classifications (migrated / non-migrated / internal transfer / deported) has not been conducted. Given that migration status is the primary independent variable, this is a higher priority for V3 than the nationality validation.

Recommended procedure:
1. Stratified sample: 50 entries per migration class = 200 total (or minimum 50 MIGRATED + 50 NON-MIGRATED for the primary comparison).
2. Human reviewer independently classifies each entry per §7.2 rules.
3. Report per-class agreement rates and directional bias (especially whether errors favour the migrated group).

### 13.3 Date Extraction Error Rate

The automatic date extraction from ESU entries is performed by regular expression parsing and is subject to errors when dates are embedded in unusual text formats. A sample check of 100 randomly selected entries with extracted birth and death years should be performed to verify that the extracted dates match the values stated in the ESU text.

Recommended procedure:
1. Select 100 random entries from the dataset with confirmed birth and death years.
2. Visit the corresponding ESU entry URL.
3. Manually verify the birth and death years against the entry text.
4. Report the number of extraction errors.

### 13.4 Profession Category Assignment Error Rate

A sample check of profession category assignments should be performed:

1. Select 50 random entries from each of the six profession categories (300 total).
2. For each entry, read the ESU profession labels and determine whether the assigned category is correct according to the keyword list in Section 5.
3. Report disagreement rates.

---

## Appendix A: Summary of Key Numbers for Verification (V2.3)

A replicating researcher who has successfully reproduced the dataset and analysis should obtain the following numbers. Significant deviation from these figures indicates an error in the replication.

**Dataset scale:**
| Metric | V2.1 (superseded) | V2.2 (reference) | V2.3 (current) |
|--------|-------------------|------------------|----------------|
| Total ESU entries | 16,215 | 16,215 | 16,215 |
| Analysable entries | 6,106 | 8,830 | **8,643** |
| Migrated | 927 | 1,273 | **1,280** |
| Non-migrated | 4,625 | 6,000 | **6,030** |
| Internal transfer | 479 | 1,155 | **1,150** |
| Deported | 75 | 178 | **183** |
| Excluded (alive/unknown/bad dates) | ~10,109 | ~7,385 | **~7,572** |

**Primary life expectancy statistics (V2.3):**
| Metric | Value |
|--------|-------|
| Migrated mean LE | **75.25 yrs** |
| Migrated median LE | 77 |
| Migrated SD | 13.89 |
| Migrated 95% CI | [74.49, 76.01] |
| Non-migrated mean LE | **71.22 yrs** |
| Non-migrated median LE | 73 |
| Non-migrated SD | 13.81 |
| Non-migrated 95% CI | [70.86, 71.57] |
| Internal transfer mean LE | 70.70 yrs |
| Deported mean LE | **48.35 yrs** |
| Deported median LE | 45 |
| **LE gap (migrated − non-migrated)** | **+4.04 yrs** |
| Mann-Whitney U p-value | < 0.001 (≈0.0) |
| **Cohen's d** | **0.292** |
| Deported vs non-migrated gap | −22.87 yrs |
| Deported Cohen's d | 1.656 |

**Two-group conservative framing (V2.3):**
| Metric | Value |
|--------|-------|
| Migrated n | 1,280 |
| Stayed (all others) n | 7,362 |
| Gap | +4.68 yrs |
| Cohen's d | 0.330 |

**Repression data (V2.3):**
| Metric | Value |
|--------|-------|
| 1937 deported deaths | **65 (35.5% of deported group, n=183)** |
| 1937 non-migrated deaths | 24 |
| 1937 combined creative deaths | **89** |
| Mean age at death, 1937 deported | 42.7 yrs |
| Deported with repression-cause death | ~90% |

**Date recovery (V2.2 fix — unchanged in V2.3):**
| Metric | Value |
|--------|-------|
| Entries with recovered dates | 8,971 |
| Entries re-classified after date recovery | ~2,000 |
| Script | `fix_dates_v2.py` |

**V2.3 corrections applied:**
| Metric | Value |
|--------|-------|
| Manual individual corrections | 3 (Куліш, Квітко, Маркіш) |
| Impossible-age entries excluded | 19 |
| Unknown entries re-classified | 77 of 196 |
| Scripts | `reclassify_unknowns.py`, `diagnose_scraper.py` |

---

*Document prepared 2026. Authors: Elza Berdnyk, Mark Symkin.*
*This methodology document is intended to accompany the PAPER_DRAFT.md and should be cited when this study is referenced in subsequent work.*

---

### 8.14 Emigration Wave Disaggregation (V2.5) — RETRACTED

**Purpose:** Test the self-selection critique structurally by disaggregating all 1,313 migrant entries into historically distinct emigration waves, each defined by a different selection mechanism.

**Script:** `stage9_wave_disaggregation.py` (retained; not re-run)

**Method attempted:** Rule-based year extraction (regex `\b1[89]\d\d\b`) from `migration_reasoning` (English biographical reasoning text) with keyword fallback (`"civil war"`, `"UNR"`, `"WWII"`, `"DP camp"`, `"Cold War"`, `"defect"`). Priority hierarchy: WAVE1 (pre-1922) > WAVE2 (1939–45) > WAVE3 (1946–91) > WAVE4 (post-1992) > UNKNOWN.

**Why the results were retracted:**

The `migration_reasoning` column was generated in Stage 4 to answer the question *"did this person migrate?"* — not *"when did this person emigrate?"*. The typical text reads: *"died in New York in 1972, indicating long-term settlement outside the Soviet sphere."* The year 1972 is the death year used as evidence of migration status, not a departure year. The Stage 9 classifier extracted this death year and assigned WAVE3 (1946–91) to someone who may have left Ukraine in 1944.

Three specific failure modes were confirmed by manual review of a 50-entry random sample:

1. **Death year as migration year (WAVE3/WAVE4 contamination):** The dominant year in `migration_reasoning` is almost always the death year. Individuals who emigrated during WWII but died in 1968 or 1998 are misassigned to WAVE3 or WAVE4 respectively.

2. **Birth year as migration year (WAVE1 contamination):** The WAVE1 trigger set {1917, 1918, 1919, 1920, 1921} overlaps with birth years common in this cohort. Individuals born in 1920 and dying in Philadelphia in 1999 — with `migration_reasoning` explicitly describing "post-Soviet emigration" — were classified as WAVE1 because their birth year triggered the classifier before any emigration signal appeared.

3. **Non-emigration events misread as departure signals:** Career milestones, award dates, publication years, and historical reference years all appear in biographical text and were treated as potential emigration years.

**Computed statistics (not reported — presented here for methodological record only):**

| Wave | n assigned | Mean age at death | Gap vs non-mig | p (MW) |
|------|------------|-------------------|----------------|--------|
| WAVE1 | 212 | 73.62 | +2.41 | 0.0002 |
| WAVE2 | 203 | 70.34 | −0.88 | 0.63 |
| WAVE3 | 632 | 75.66 | +4.44 | <0.001 |
| WAVE4 (excl.) | 172 | 86.62 | — | — |

These figures are not cited in the paper. The superficially plausible pattern (WAVE3 largest gap, WAVE2 null) cannot be distinguished from an artefact of the classifier preferentially assigning later-born or longer-lived individuals to later waves.

**Root cause — data not collected in Stage 4:** Departure-specific language was not extracted. Ukrainian emigration verbs (`"виїхав у"`, `"емігрував до"`, `"залишив Україну"`) and English equivalents (`"fled in [year]"`, `"emigrated to [country] in [year]"`) would need to be extracted in a dedicated pipeline pass over the original Ukrainian ESU article text. This was not done.

**Decision:** Findings retracted. Paper §5.1 wave analysis replaced with a methodology limitation note. Wave disaggregation is defined as a V3 data collection priority.

**Output files retained for reference:** `wave_assignments.csv`, `wave_stats.txt`, `charts/fig29_wave_km.png`, `charts/fig29b_wave_volume.png`, `charts/fig29c_wave_lifespan.png`

---

### 8.15 Missing Figures Bias Bounding (V2.5)

**Purpose:** Quantify the direction and plausible magnitude of ESU source undercoverage bias. ESU coverage gaps are not random: the encyclopedia systematically underrepresents individuals whose biographical documentation was destroyed along with them — exactly the most severely repressed non-migrants who died youngest.

**Script:** `stage10_missing_bias.py`

**Method:** Hardcoded named cases (verified absent from ESU by direct dataset lookup); sensitivity calculation using closed-form formula:

```
mean_nm_adj = (mean_nm × n_nm + Ā_missing × M) / (n_nm + M)
adjusted_gap = mean_mig − mean_nm_adj
```

Because `Ā_missing < mean_nm` under all historical assumptions, the gap widens monotonically with M. No LLM or web scraping required.

**Confirmed absent figures (all non-migrants, all meet study inclusion criteria):**

| Name | Birth | Death | Age | Mechanism |
|------|-------|-------|-----|-----------|
| Vasyl Stus | 1938 | 1985 | 47 | Perm-36 labour colony |
| Mykola Khvylovy | 1893 | 1933 | 39 | Suicide under political pressure |
| Vasyl Symonenko | 1935 | 1963 | 28 | Disputed KGB custody |
| Mykhailo Semenko | 1892 | 1937 | 45 | Shot, Great Terror |
| Yevhen Pluzhnyk | 1898 | 1936 | 38 | Shot, Solovki |
| Myroslav Irchan | 1897 | 1937 | 40 | Shot, Great Terror |
| Dmytro Falkivsky | 1898 | 1934 | 36 | Shot, NKVD |

Mean age at death (named cases): 39.0 years.

**Note:** Zerov, Kosynka, Pidmohylny, Kurbas ARE present in dataset as non_migrated — not missing.

**Sensitivity results (key scenarios):**

| M | Ā=38 | Ā=43 | Ā=50 |
|---|------|------|------|
| 7 | +4.08 | +4.07 | +4.06 |
| 50 | +4.31 | +4.27 | +4.21 |
| 200 | +5.10 | +4.94 | +4.72 |
| 500 | +6.58 | +6.20 | +5.66 |

**Conclusion:** Current estimate of 3.98 years (V3.0) is a conservative lower bound. No plausible (M, Ā) combination narrows or reverses the gap.

**Output files:** `named_missing_figures.csv`, `charts/fig30_sensitivity_gap.png`, `charts/fig30_interactive.html`

---

## §8.16 — Stage 11: Data Audit (V2.6 Pre-Fix)

**Purpose:** Systematic audit of all known data quality issues in `esu_creative_workers_v2_3.csv` before applying fixes, producing a structured report for the paper appendix.

**Script:** `stage11_data_audit.py` → `data_audit_report.md`

**Issues catalogued:**
1. Birth year stored as death year (ESU scraper stored single year in wrong field): ~102 entries
2. API-credit-error unknowns (billing error messages instead of classifications): 58 entries
3. Specific validation errors (7 named from manual review)
4. Non-Ukrainian inclusions: audited
5. Unknown group: residual unresolvable entries
6. Incomplete validation (118 of 200 not yet reviewed at time of audit)
7. Missing high-profile figures (Executed Renaissance): 7 confirmed absent

---

## §8.17 — Stage 12: Database Quality Pipeline (V2.6)

**Purpose:** Apply all identified fixes to produce the clean `esu_creative_workers_v2_6.csv` dataset.

**Script:** `stage12_fix_database.py` (B1–B5 sub-stages)

### B1 — Specific Validation Patches (7 hardcoded)
Direct dict of {article_url → corrected fields}. Applied first, before any scraping.

Key corrections:
- Керч Оксана: death_year 1911→1991, excluded_pre_soviet→migrated
- Антонович Катерина: death_year 1884→1975, excluded_pre_soviet→migrated
- Містраль Ґабрієла: excluded_pre_soviet→excluded_non_ukrainian (Chilean poet)
- Петровичева Людмила-Ванда: death_year 1882→1971, excluded_pre_soviet→non_migrated
- Кудравець Анатоль: non_migrated→excluded_non_ukrainian (Belarusian)

### B2 — Birth-Year-as-Death-Year Corrections (~97 entries)
For entries where birth_year=NaN and death_year matched the first year in ESU notes: re-fetched article HTML, parsed "Дата смерті:" and "Дата народження:" fields, applied corrected years. If corrected death_year ≥ 1921: reclassified via Claude. Rate-limited at 2 req/sec (esu.com.ua).

### B3 — API-Credit-Error Reclassification (57 entries)
For entries where migration_reasoning contained "credit balance is too low": fetched full bio, re-ran Claude classification (claude-haiku-4-5-20251001). Resolved all 57.

### B4 — Non-Ukrainian Audit
Checked all analysis-group entries with flag_non_ukrainian=True. Zero confirmed non-Ukrainians remained in analysis groups.

### B5 — Residual Unknown Resolution
Checked remaining unknown entries for bio availability. Applied classifications where possible.

**Output:** `esu_creative_workers_v2_6.csv` with `fix_applied` column recording each correction.

---

## §8.18 — Stage 13: Validation Review Corrections

**Purpose:** Apply corrections identified during the first 82-entry manual validation review.

**Script:** `stage13_apply_validation_fixes.py`

**Corrections applied (8 entries):**
- Черняхівська Вероніка: excluded_pre_soviet→migrated (confirmed emigrated, lived to 1966)
- Бойченко Микола: non_migrated→excluded_bad_dates (irreconcilable dates)
- Кейс Віталій: unknown→migrated (bio confirms emigration to USA 1951)
- Plus 5 additional boundary-case corrections

---

## §8.19 — Stage 14: API Authentication Failure Reclassification

**Purpose:** Re-classify 135 entries that failed during Stage 12 B3 due to API authentication errors (different error message than the original "credit balance" failures).

**Script:** `stage14_reclassify_api_failures.py`

**Model:** claude-haiku-4-5-20251001
**Protocol:** Same 2-step classification prompt as Stage 4
**Rate:** 0.3 seconds/entry API delay + 0.1 seconds/entry fetch delay
**Bio source:** Live fetch from esu.com.ua at time of classification

**Results:**
- 135 entries processed
- All resolved to valid classification status
- Entries recorded in `migration_reasoning` with prefix "S14-reclassified:"

**Manual review:** All 135 S14-reclassified entries were reviewed via the Stage 15 HTML reviewer (`validation/stage14_reviewer.html`). 125 correct, 8 wrong, 1 skip, 1 unseen.

---

## §8.20 — Stage 15: Stage-14-Review Corrections

**Purpose:** Apply corrections from the manual Stage 14 reviewer.

**Script:** `stage15_apply_s14_fixes.py`

**Corrections applied (6 entries):**

| Entry | Old status | New status | Reason |
|---|---|---|---|
| Глушаниця Павло | migrated | excluded_bad_dates | Bad data, unknown death date |
| Збіржховська Антоніна | migrated | excluded_galicia_pre_annexation | Galicia, died pre-Soviet annexation |
| Злоцький Феодосій | non_migrated | excluded_galicia_pre_annexation | Galicia, died pre-Soviet annexation |
| Камінський Віктор | non_migrated | excluded_galicia_pre_annexation | Galicia, died pre-Soviet annexation |
| Конрад Джозеф (Joseph Conrad) | migrated | excluded_pre_soviet | Emigrated pre-Soviet era, died 1924 |
| Лефлер Чарльз-Мартін (Charles Martin Loeffler) | migrated | excluded_non_ukrainian | Not Ukrainian |

**Note on Galicia pre-annexation classification:** Three individuals were active in Galicia (western Ukraine) under Polish/Austro-Hungarian administration before the Soviet annexation of 1939. Because their deaths preceded Soviet control of the region, Soviet demographic conditions did not apply to them. They are excluded from analysis — not because they are non-Ukrainian, but because the comparison requires Soviet-era exposure.

**Final dataset after Stage 15:**
- N=8,590 analysable (migrated=1,324 | non_migrated=5,960 | internal_transfer=1,111 | deported=195)
- check_paper_numbers.py: 177/177 PASS
- Primary gap: **3.98 years** (Cohen's d=0.292)

### Files Created/Modified in Stages 11–15

| File | Action |
|------|--------|
| `stage11_data_audit.py` | Created |
| `stage12_fix_database.py` | Created |
| `stage13_apply_validation_fixes.py` | Created |
| `stage14_reclassify_api_failures.py` | Created |
| `stage15_apply_s14_fixes.py` | Created |
| `stage15_build_s14_reviewer.py` | Created |
| `validation/stage14_reviewer.html` | Created |
| `data_audit_report.md` | Created |
| `esu_creative_workers_v2_6.csv` | Final dataset (N=8,590) |
| `PAPER_DRAFT.md` | Complete rewrite as V3.0 |
| `check_paper_numbers.py` | Updated — 177/177 PASS |
| `charts/fig01–fig30` | All regenerated on V2.6 dataset |
| `docs/index.html` | Rebuilt and pushed |

*This log phase completed: 2026-04-09*
