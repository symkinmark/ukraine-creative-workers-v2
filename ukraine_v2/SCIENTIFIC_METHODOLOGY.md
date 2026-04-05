# Scientific Methodology and Replication Guide

## Life Expectancy of Ukrainian Creative Industry Workers During the Soviet Occupation: An Expanded Study (V2)

**Authors:** Elza Berdnyk, Mark Symkin
**Study completed:** 2026
**Data source:** Encyclopedia of Modern Ukraine (esu.com.ua)
**This document version:** 1.1 — revised 2026-04-03 following Phase 5 human accuracy check

> **V2.3 CURRENT.** Primary dataset: `esu_creative_workers_v2_3.csv`. Analysable: **n=8,643**. V2.2 reference dataset archived (unchanged). See AI_METHODOLOGY_LOG.md Phase V2.3 for full correction log.

---

## Purpose of This Document

This document is written for a researcher with no prior knowledge of this project who wishes to fully replicate the study from scratch. It provides the exact research question, data sources, inclusion and exclusion criteria, classification protocols (including verbatim AI prompts), statistical methods, known limitations, and file descriptions. Nothing is assumed; everything is specified.

If you are replicating this study, you should read this document in its entirety before touching any data or code. The decisions made at each stage — particularly nationality determination and migration classification — are interdependent, and misapplying them out of sequence will produce incorrect results.

---

## 1. Research Question

### 1.1 Primary Research Question

**Did Ukrainian creative industry workers who emigrated from the Soviet Union live statistically significantly longer than those who remained within Soviet-controlled territory, and if so, by how much?**

### 1.2 Secondary Research Questions

1. Does the life expectancy gap vary by creative profession?
2. Does the gap vary by birth cohort, and if so, in which cohorts is it largest?
3. Are there identifiable historical periods of anomalously elevated premature mortality among non-migrant creative workers, consistent with documented Soviet repression campaigns?
4. Are there geographic patterns in migration rates among Ukrainian creative workers, and what is the likely explanation?
5. How do the V2 findings compare to the V1 findings, and what methodological factors account for the differences?

### 1.3 What This Study Does Not Claim to Answer

This study does not establish clean causal identification of the mortality effect of Soviet conditions. It establishes an observational association between migration status and life expectancy in a specific professional population. Selection effects — the possibility that migrants and non-migrants differed before emigration in ways correlated with longevity — cannot be fully controlled for in this observational design. Readers should not interpret the life expectancy gap as a precise estimate of "how many additional years you would have lived if you had emigrated" at the individual level.

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
- **Entries usable for primary life expectancy analysis (birth date + death date + determinable migration status + confirmed Ukrainian nationality):** 6,310
- **Of which non-migrants:** 5,272
- **Of which migrants:** 1,038
- **Entries excluded due to living status (no death date):** the majority of the excluded 9,905 entries
- **Entries excluded due to non-Ukrainian nationality:** 1,218 (after Claude review)
- **Entries excluded due to indeterminate migration status:** several hundred

---

## 3. Inclusion Criteria

An entry was included in the primary life expectancy analysis if and only if ALL of the following conditions were met:

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

Entries with no death year recorded were classified as potentially living and excluded from life expectancy analysis. Some of these individuals may in fact be deceased but lack a recorded death date in the ESU; this is a data availability issue, not a classification error.

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

**Estimated error rate (from our Phase 5 check):** Below 5%. Exact figure to be inserted after Phase 5 completion.

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

**Note:** The period assignment is based on year of death, not year of persecution. An individual executed in 1937 (Great Terror) is assigned to that period. An individual who was arrested in 1937, survived the Gulag, and died in 1961 is assigned to the Khrushchev Thaw period — their death occurred then, even if their period of maximum persecution was earlier. This is a limitation of the period analysis: it does not capture the delayed mortality effects of repression.

### 8.7 Birth Cohort Analysis

Workers were grouped by birth decade (1870s, 1880s, 1890s, 1900s, 1910s, 1920s). For each decade-of-birth cohort, average life expectancy was calculated separately for migrants and non-migrants, and the gap (migrant minus non-migrant) was reported.

Cohorts with fewer than 20 individuals in either the migrant or non-migrant group were flagged as underpowered; results for such cohorts should be interpreted with caution.

### 8.8 Profession-Level Analysis

For each of the six profession categories, average life expectancy was calculated separately for migrants and non-migrants. The same statistical approach (means, medians, gap) was applied. Full Mann-Whitney U testing was not performed at the profession level due to smaller sample sizes in some categories (particularly Theatre/Film migrants, n=53), but direction of effect was consistent across all categories.

---

## 9. AI Tools Used

### 9.1 Claude (Anthropic)

**Model:** claude-sonnet-4-6
**Provider:** Anthropic
**API endpoint:** `https://api.anthropic.com/v1/messages`
**Python library:** `anthropic` (latest version as of 2026)
**Temperature:** Default (1.0 for Claude models)
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
- There was a statistically robust and practically meaningful life expectancy gap of 4.77 years between Ukrainian creative workers who emigrated from the Soviet Union and those who remained, in a dataset of 6,310 individuals.
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
**Location:** `/Users/symkinmark_/projects/Ai agent basic/ukraine_v2/esu_creative_workers_v2_3.csv`
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
**Location:** `/Users/symkinmark_/projects/Ai agent basic/ukraine_v2/esu_creative_workers_raw.csv`
**Description:** The raw output from the scraper before any nationality or migration classification. Contains all entries that matched the creative profession keywords. This file is the starting point for any replication; all subsequent processing steps are applied to this file programmatically.

### 11.4 Reproducing the Dataset (V2.3 full pipeline)

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
11. Calls matplotlib/seaborn to generate all seven figures and saves them to the `charts/` subdirectory.
12. Writes summary statistics to `esu_analysis_results.txt` and `analysis_extended.txt`.

**Dependencies:** `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`

---

## 13. Error Rate Tracking

### 13.1 Claude Nationality Classification Error Rate

The error rate of Claude's nationality classifications (Tier 2 decisions) should be estimated by the Phase 5 human sample check described in Section 6.6. The recommended procedure is:

1. Extract all 137 INCLUDE decisions and all 1,218 EXCLUDE decisions from the reviewed dataset.
2. Using a random number generator with a fixed seed (for reproducibility), select 100 entries from the INCLUDE set and 100 entries from the EXCLUDE set.
3. For each of the 200 entries, have a human reviewer read the full Ukrainian ESU biographical text and independently classify the entry as INCLUDE or EXCLUDE, without seeing Claude's classification.
4. After completing all 200 independent classifications, compare to Claude's classifications.
5. Record the number of disagreements for INCLUDEs and EXCLUDEs separately (as false positive rate and false negative rate).
6. Report the overall error rate as: disagreements / 200.

**Reviewer qualifications:** The human reviewer should be fluent in Ukrainian and familiar with Ukrainian 20th-century cultural history. If the primary researchers cannot perform this review, it should be delegated to a qualified research assistant with these qualifications.

**Acceptable threshold:** An overall error rate below 5% is considered acceptable for inclusion in the published paper. An error rate of 5–10% should be flagged as a limitation and the impact on study conclusions should be discussed. An error rate above 10% should trigger re-examination of the Claude prompt and potentially re-running the classifications.

**Expected directional bias:** If Claude's classifications are biased in a particular direction (e.g., systematically over-including Jewish-Ukrainian figures or systematically excluding Galician Polish-Ukrainians), the directional bias should be reported alongside the overall error rate.

### 13.2 Claude Migration Classification Error Rate

A parallel error rate assessment should be performed for Claude's migration classifications, using the same sample-check methodology:

1. Extract a random sample of 50 MIGRANT and 50 NON-MIGRANT Claude-classified entries (100 total).
2. Have a human reviewer independently classify each entry according to the migration classification rules in Section 7.2.
3. Report agreement rates and directional bias.

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
| Mean age at death, 1937 deported | 42.4 yrs |
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
