# Life Expectancy of Ukrainian Creative Industry Workers During the Soviet Occupation: An Expanded Study (V2)

**Authors:** Elza Berdnyk, Mark Symkin

> **⚠ OUTDATED — V2.1 DATA. DO NOT CITE THESE NUMBERS.**
> This draft was written against the V2.1 dataset (n=6,106 analysable). V2.2 corrected a critical ESU scraper regex bug that was silently dropping 8,971 entries (including most Executed Renaissance victims). V2.2 dataset: **n=8,830 analysable** (migrated:1,305 / non_migrated:6,157 / internal:1,179 / deported:189). LE gap: ~+4.03 yrs. All Section 4 numbers must be rewritten against V2.2 results. Charts have been regenerated — see `charts/`. Updated 2026-04-05.

---

## Abstract

This paper presents an expanded quantitative analysis of life expectancy among Ukrainian creative industry workers during the Soviet occupation of Ukraine, extending and refining the methodology of our original V1 study. Drawing on 16,215 confirmed Ukrainian creative workers extracted from the Encyclopedia of Modern Ukraine (Інститут енциклопедичних досліджень НАН України, esu.com.ua, accessed 2026), we identify 6,310 individuals with complete birth dates, death dates, and determinable migration status, representing a fifteen-fold expansion over the V1 dataset of 415 workers. Non-migrants who remained within the USSR (n=5,272) achieved an average life expectancy of 69.81 years (median 72, SD 15.04), while migrants who left the Soviet sphere (n=1,038) achieved an average of 74.58 years (median 77, SD 14.47), yielding a gap of 4.77 years in favour of emigrants. This gap is statistically robust (Mann-Whitney U, p≈0.0; Cohen's d=0.319, a medium effect size) but markedly narrower than the 9-year gap reported in V1. We demonstrate that V1's pre-1991 death cutoff artificially inflated the gap by excluding long-lived post-Soviet non-migrants. Profession-level, birth cohort, and repression-period analyses confirm systematic mortality differentials aligned with documented Soviet repression campaigns, particularly the Holodomor (1932–1933), the Great Terror (1937–1938), and the broader cultural suppression of the Executed Renaissance. These findings constitute quantitative corroboration of the mortality cost of Soviet cultural policy for Ukrainian creative communities.

---

## 1. Introduction

The Soviet occupation of Ukraine — conventionally dated from the consolidation of Bolshevik control in 1920 through Ukrainian independence in 1991 — was characterised by systematic state violence against Ukrainian cultural and intellectual life. Policies of Russification, enforced collectivisation, mass executions, forced labour, and ideological surveillance were not applied uniformly across Soviet society but were deployed with particular intensity against groups whose work produced and transmitted national identity: writers, poets, visual artists, composers, theatre directors, architects, and other creative workers.

The period known in Ukrainian historiography as the "Executed Renaissance" (Розстріляне відродження, Rozstriliane vidrodzhennia) — roughly 1917 to 1941 — saw the near-total physical destruction of an entire generation of Ukrainian cultural figures. Scholars including Mykola Zerov, Mykhailo Khvylovy, Les Kurbas, Valerian Pidmohylny, and hundreds of others were arrested, tortured, imprisoned in the Gulag system, or executed outright during the Stalinist terror campaigns of the 1930s. The Great Terror of 1937–1938 was particularly lethal: Ukrainian cultural workers were disproportionately targeted as potential vectors of "bourgeois nationalism."

Quantitative study of this mortality toll has been limited. Historical demography of Soviet persecution has relied heavily on archival records — many still restricted or destroyed — and has focused more on aggregate victim counts than on comparative life expectancy across survivor groups. Our V1 study (Berdnyk & Symkin, 2025) provided a first quantitative examination of the life expectancy gap between Ukrainian creative workers who emigrated versus those who remained within the Soviet Union, finding a 9-year gap (63 years versus 72 years) in a dataset of 415 workers.

The present paper — V2 — substantially expands that dataset to 6,310 analysable workers, refines the methodology to eliminate the pre-1991 death cutoff that we identified as a source of bias in V1, introduces a profession-level disaggregation, and provides detailed analysis of repression-period mortality, birth cohort effects, and geographic migration patterns. Our central research question remains unchanged: did Ukrainian creative workers who emigrated from the Soviet Union live significantly longer than those who remained, and if so, by how much and under what conditions?

We approach this question with awareness of its political sensitivity. We make no causal claims that cannot be substantiated by the data. We acknowledge the significant selection effects inherent in emigration. And we situate our quantitative findings within the documented historical record of Soviet policy toward Ukrainian cultural workers, rather than treating the numbers as speaking for themselves.

---

## 2. V1 Summary and Limitations

### 2.1 Summary of V1 Findings

Our original study (V1) drew on a manually curated dataset of 415 Ukrainian creative workers for whom we could determine birth year, death year, and migration status. The core finding was a 9-year life expectancy gap: non-migrants averaged 63 years while migrants averaged 72 years. This gap was statistically significant and represented a substantial effect.

V1 applied a pre-1991 death cutoff — only workers who had died before the dissolution of the Soviet Union were included in the primary analysis. The rationale was methodological consistency: workers who survived into the post-Soviet period were excluded to avoid the confounding influence of post-Soviet conditions on what was intended to be a study of Soviet-era mortality.

### 2.2 Limitations Identified in V1

Upon reflection and in preparation for V2, we identified three significant limitations in the V1 methodology:

**The pre-1991 cutoff introduced survivorship bias.** By excluding all workers who died after 1991, V1 systematically excluded the longest-lived non-migrants — those who survived the Soviet period entirely and died in independent Ukraine. Because migrants had, on average, an earlier birth year (V1 migrants were born notably earlier than non-migrants), they were more likely to have died before 1991 simply due to age, which meant they were more fully represented in the V1 dataset. Non-migrants born in the 1920s or later were systematically excluded if they survived to old age, which skewed the non-migrant average downward.

**The dataset was too small.** 415 workers, while sufficient for a preliminary study, left the analysis vulnerable to outlier effects and limited our ability to conduct meaningful subgroup analyses by profession, birth cohort, or repression period.

**Profession and geography were not systematically recorded.** V1 did not code profession or birth city consistently, preventing profession-level or geographic analysis.

### 2.3 V1-to-V2 Comparison Summary

| Dimension | V1 | V2 |
|-----------|----|----|
| Dataset size | 415 workers | 6,310 usable (16,215 total) |
| Pre-1991 death cutoff | Yes | No |
| Life expectancy gap | 9.0 years | 4.77 years |
| Non-migrant avg LE | 63 years | 69.81 years |
| Migrant avg LE | 72 years | 74.58 years |
| Statistical method | t-test | Mann-Whitney U + Cohen's d |
| Profession breakdown | No | Yes (6 categories) |
| Birth cohort analysis | No | Yes |
| Geographic analysis | No | Yes |

The narrowing of the gap from 9 years to 4.77 years is not a finding of lesser mortality disparity — it is a correction of an artificial inflation. When long-lived post-Soviet non-migrants are included in the analysis, the non-migrant average rises substantially. The 4.77-year gap in V2 represents a cleaner estimate of the actual life expectancy penalty associated with remaining within the Soviet system.

---

## 3. Methodology

### 3.1 Data Source

All data were extracted from the Encyclopedia of Modern Ukraine (Енциклопедія сучасної України, ESU), maintained by the Institute of Encyclopedic Research of the National Academy of Sciences of Ukraine (Інститут енциклопедичних досліджень НАН України) and available at esu.com.ua. The ESU is the authoritative scholarly encyclopedia of Ukrainian cultural and intellectual life, with entries written and reviewed by subject-matter experts. As of our access date (2026), it contained entries for approximately 70,000 individuals.

The ESU was selected as the primary source for three reasons: (1) it is the most comprehensive Ukrainian-language biographical reference work covering the relevant time period; (2) its entries consistently include birth and death dates, biographical summaries, and sufficient information to determine migration status; and (3) it focuses specifically on individuals of cultural, intellectual, and creative significance, making it a natural population of interest for this study.

### 3.2 Data Collection

Data were collected via automated web scraping of esu.com.ua using Python scripts developed specifically for this project (see the companion SCIENTIFIC_METHODOLOGY.md for full technical details). The scraper extracted, for each entry: full name (Ukrainian and transliterated), birth year, death year, birth city, listed profession(s), and the full biographical text in Ukrainian. The raw dataset comprised 16,215 entries identified as potentially relevant Ukrainian creative workers.

### 3.3 Inclusion and Exclusion Criteria

**Inclusion criteria.** An entry was included in the primary life expectancy analysis if it met all of the following conditions:

1. The individual was confirmed as Ukrainian (see Nationality Determination Protocol, Section 3.5).
2. The individual's primary profession fell within our definition of "creative worker" (see Section 3.4).
3. The entry contained a confirmed birth year.
4. The entry contained a confirmed death year.
5. The individual's migration status could be determined with reasonable confidence.

Of the 16,215 entries initially collected, 6,310 met all five criteria and form the primary analytical dataset.

**Exclusion criteria.** The following categories were excluded:

- Living individuals (no death year recorded): excluded from life expectancy analysis but noted in the total dataset count.
- Individuals with uncertain birth or death dates (recorded as "circa," date ranges, or question marks): excluded to preserve the precision of average calculations.
- Individuals whose nationality could not be determined: excluded rather than misclassified.
- Non-Ukrainian individuals: 1,218 entries in the ESU referred to foreign artists or intellectuals with no substantive Ukrainian connection and were excluded.
- Individuals whose migration status was ambiguous and could not be resolved: excluded rather than assigned to a group incorrectly.
- ⚠ **[V2.1 correction]** Individuals with `death_year < 1921`: excluded as pre-Soviet deaths. The Ukrainian SSR was not consolidated until 1920–1922; individuals who died before 1921 were never subject to Soviet conditions and cannot meaningfully be included in a study of Soviet-era mortality.
- ⚠ **[V2.1 correction]** Galician-born individuals with `death_year < 1939`: excluded because Galicia (Lviv, Ternopil, Ivano-Frankivsk regions) was not part of the Soviet Union until the 1939 annexation of Western Ukraine from Poland. Galician workers who died before 1939 were never under Soviet rule. Those alive after 1939 are included.

### 3.4 Creative Worker Definition

The following Ukrainian-language profession keywords were used to filter entries for inclusion as "creative workers." This list was developed iteratively against the ESU's own profession taxonomy:

**Primary profession keywords (Ukrainian originals):** поет (poet), письменник (writer), прозаїк (prose writer), драматург (playwright), літератор (literary figure), художник (artist), живописець (painter), скульптор (sculptor), графік (graphic artist), архітектор (architect), дизайнер (designer), композитор (composer), музикант (musician), диригент (conductor), режисер (director), актор (actor), акторка (actress), співак (singer), співачка (female singer), хореограф (choreographer), танцівник (dancer), кінорежисер (film director), кінооператор (cinematographer), сценарист (screenwriter), театральний режисер (theatre director), фотограф (photographer — artistic), ілюстратор (illustrator), гравер (engraver), кераміст (ceramicist), ткач (weaver — artistic textile), мозаїчист (mosaicist).

**Excluded profession terms despite proximity to creative fields:** журналіст (journalist — excluded unless dual-listed with a creative profession), науковець (scientist), філософ (philosopher), педагог (educator — unless dual-listed), релігійний діяч (religious figure), військовий (military figure), політик (politician).

Where individuals held multiple professions (e.g., a writer who was also a journalist), they were included if any of their listed professions appeared on the primary inclusion list. They were assigned to a single profession category for analytical purposes using the profession listed first or most prominently in their ESU entry.

### 3.5 Nationality Determination Protocol

#### 3.5.1 Definition of Ukrainian

This study applies a **cultural participation definition of Ukrainian identity**, not an ethnic or linguistic one. A person is counted as Ukrainian if they meet any of the following criteria: they were born or raised on territory that is now Ukraine and made a creative contribution that forms part of the Ukrainian cultural record; they contributed substantially to Ukrainian cultural life regardless of ethnic background; they self-identified as Ukrainian or were recognised as part of the Ukrainian creative community by their contemporaries; or they were subject to Soviet persecution specifically in the context of suppressing Ukrainian cultural identity.

This definition deliberately excludes ethnic or linguistic tests for two reasons. First, the Soviet state systematically suppressed Ukrainian cultural identity precisely as expressed through creative practice — through language choice, subject matter, institutional affiliation, and artistic tradition. The population most at risk was defined by cultural participation, not by blood. Second, applying an ethnic test would arbitrarily exclude substantial portions of the historically documented Ukrainian creative community: Ukrainian Jews whose cultural world was entirely Ukrainian even when they wrote in Yiddish; Galician Poles who participated fully in Ukrainian cultural institutions and self-identified with the Ukrainian national movement; Crimean Tatars indigenous to Ukrainian territory who were collectively deported by the Soviet state.

The definition also excludes figures who merely appear in the ESU as foreign reference points with no Ukrainian presence, and ethnic Russians whose creative careers were oriented toward Russian rather than Ukrainian culture even if they were born or worked in Ukraine.

**Notably included under this definition:**
- Crimean Tatars: indigenous to Ukrainian territory, targeted by the 1944 Soviet mass deportation; included without individual review.
- Ukrainian Jews with substantive Ukrainian cultural connection: reviewed individually; those who participated in Ukrainian cultural institutions, wrote about Ukraine, or were targeted as part of the Ukrainian intelligentsia included.
- Galician Poles who self-identified as Ukrainian and participated in Ukrainian cultural institutions: included after individual review.

The full nationality determination protocol, including verbatim AI prompts and stress-test case decisions, is reproduced in SCIENTIFIC_METHODOLOGY.md (Section 6).

#### 3.5.2 Classification Procedure

Determining Ukrainian identity in practice proved less straightforward than applying the definition above, because Soviet administrative records frequently imposed or obscured national identities, and ESU biographical texts reflect the political constraints of the periods in which they were written. We developed a three-tier classification system.

**Tier 1: Clean inclusion.** Entries explicitly described as Ukrainian (Українець/Українка) with no ambiguity markers were included directly without further review.

**Tier 2: Claude AI review.** Entries containing markers suggesting possible nationality ambiguity — Jewish heritage, Polish origin, German or Austrian origin, descriptions as "Soviet" without an underlying national identity, or birth entirely outside Ukraine — were flagged for individual review by Claude (Anthropic, claude-haiku-4-5). Claude was presented with the full ESU biographical text in Ukrainian and asked to classify the individual against the Section 3.5.1 criteria. A total of 1,356 entries underwent this review.

Of the 1,356 reviewed:
- 137 were confirmed as Ukrainian and included.
- 1,218 were confirmed as non-Ukrainian and excluded.
- 1 entry remained indeterminate and was excluded.

**Tier 3: Auto-exclusion.** Entries with explicit non-Ukrainian nationality markers and no Ukrainian connection stated were excluded without Claude review.

The verbatim prompt used for Tier 2 review and the full list of Tier 3 auto-exclusion markers are reproduced in SCIENTIFIC_METHODOLOGY.md (Sections 6.4 and 6.5).

### 3.6 Migration Classification

⚠ **[V2.1 revision — 2026-04-03]:** The original two-group classification (migrant / non-migrant) was replaced with a four-group system following Phase 5 human review. The original system incorrectly conflated voluntary internal Soviet transfers and state-imposed deportations with non-migration. The corrected system is described below. All figures in Section 4 will be updated after the classification rerun.

Migration status was classified into four categories:

**Migrated (left Soviet sphere):** The individual emigrated from Soviet-controlled territory and settled in a non-Soviet country — Western Europe, North America, South America, or non-Soviet Asia — for a substantial portion of their adult life. Movement to Soviet Russia or another Soviet republic does not qualify. The critical criterion is exit from the Soviet sphere entirely.

**Non-migrated (remained in Ukrainian SSR):** The individual spent their working life within the Ukrainian SSR with no substantial period outside Soviet-controlled territory.

**Internal transfer (voluntary, within USSR):** The individual voluntarily relocated from the Ukrainian SSR to another Soviet republic (most commonly Soviet Russia) and based their career there. They remained under Soviet conditions but in a different republic. This is a voluntary act distinct from deportation and distinct from emigration. This group will be analysed separately as a third comparison population.

**Deported (forced displacement by Soviet state):** The individual was forcibly relocated by Soviet authorities — through Gulag imprisonment, formal deportation orders, special settler (спецпоселенець) assignment, or any other state-mandated relocation. The defining criterion is compulsion: the Soviet state made the movement decision, not the individual. This applies regardless of destination. Deportees are reported as a fourth distinct group and, for the primary life expectancy comparison, grouped with non-migrants — they did not escape Soviet conditions; they experienced them as direct targets of state violence.

The ESU biographical texts consistently contain sufficient information to make this determination. Where the text was ambiguous, Claude was used to review the full Ukrainian-language text and classify migration status according to the above rules, with explicit instruction to prioritise DEPORTED classification whenever any evidence of forced displacement exists. The full revised classification prompt is reproduced verbatim in SCIENTIFIC_METHODOLOGY.md (Section 7.3).

### 3.7 Statistical Methods

**Life expectancy calculation.** For each individual with both a confirmed birth year and death year, life expectancy was calculated as: death year minus birth year. This yields age at death to the nearest year. No actuarial adjustments were made; we report raw age at death as a direct and transparent measure of longevity. The terms "life expectancy" and "average age at death" are used interchangeably in this paper.

**Central tendency measures.** We report both arithmetic mean and median for each group, as the presence of outliers (very young deaths due to execution and very old deaths among long-lived individuals) renders the mean sensitive to extreme values. The median provides a more robust central tendency measure under these conditions.

**Statistical significance testing.** We used the Mann-Whitney U test (also known as the Wilcoxon rank-sum test) rather than a two-sample t-test for the primary significance test. This choice reflects the non-normal distribution of ages at death in the non-migrant group — the distribution is left-skewed due to the substantial number of premature deaths from execution and political violence, and this skew violates the normality assumption of the t-test. The Mann-Whitney U test makes no parametric distributional assumptions and is therefore more appropriate for this data structure. The resulting p-value is approximately 0.0 (less than any conventional significance threshold).

**Effect size.** Cohen's d was calculated as the difference in group means divided by the pooled standard deviation. A value of d=0.319 is conventionally characterised as a medium effect size (Cohen, 1988), indicating that the life expectancy difference is not merely statistically detectable but practically meaningful: it is large enough to observe at the individual level, not merely at the population aggregate level.

**Period analysis.** Deaths among non-migrants were grouped by historical period using established historiographic periodisation of Soviet Ukrainian history. Average age at death within each period was calculated to identify periods of anomalously young mortality.

**Birth cohort analysis.** Workers were grouped by decade of birth (1870s through 1920s). Life expectancy was calculated separately for migrants and non-migrants within each cohort to identify which generations experienced the greatest mortality differential.

---

## 4. Results

### 4.1 Overall Life Expectancy Gap

The primary finding of V2 is a statistically robust 4.77-year life expectancy gap in favour of Ukrainian creative workers who emigrated from the Soviet Union.

| Group | n | Mean LE | Median LE | SD | Min | Max |
|-------|---|---------|-----------|-----|-----|-----|
| Non-migrants | 5,272 | 69.81 | 72 | 15.04 | <1 | 103 |
| Migrants | 1,038 | 74.58 | 77 | 14.47 | 8 | 101 |
| **Gap** | — | **+4.77** | **+5** | — | — | — |

The non-migrant group (n=5,272) achieved a mean life expectancy of 69.81 years and a median of 72 years, with a standard deviation of 15.04 years. The wide standard deviation reflects the heterogeneous mortality experience of this group, which includes both very young deaths from political violence and very long-lived individuals who survived the Soviet period and died in old age in independent Ukraine.

The migrant group (n=1,038) achieved a mean life expectancy of 74.58 years and a median of 77 years, with a standard deviation of 14.47 years. The smaller standard deviation in the migrant group reflects a more homogeneous mortality experience: migrants were largely spared the systematic political violence that produced the left tail of the non-migrant distribution, though they faced other mortality risks including wartime conditions, poverty in exile, and the psychological and health consequences of forced displacement.

The birth year distributions of the two groups differ: non-migrants have an average birth year of 1923.6, while migrants have an average birth year of 1905.5 — a gap of approximately 18 years. This reflects the historical pattern of Ukrainian emigration: the first and second waves of the diaspora (1917–1921 and 1941–1945) drew disproportionately from older cohorts who were already professionally active at the time of those events. Younger cohorts born after 1920 were largely unable to emigrate, having grown up entirely within the Soviet system. This birth year difference does not invalidate the life expectancy comparison — life expectancy is computed as age at death, which is independent of birth year — but it is relevant context for interpreting cohort-specific findings.

### 4.2 Statistical Significance

The Mann-Whitney U test applied to the two distributions yields p≈0.0 — a p-value so small that it rounds to zero at any conventional number of decimal places. This result is unambiguous: the probability that a gap of this magnitude or larger would arise by chance if the two groups had the same underlying mortality distribution is vanishingly small.

Cohen's d = 0.319 (medium effect size) provides a measure of the practical magnitude of this difference. To contextualise: a Cohen's d of 0.319 means that the average migrant life expectancy exceeds approximately 62.5% of non-migrant life expectancies. The effect is not only statistically detectable but substantively meaningful — it represents roughly one-fifteenth of a typical human lifespan.

### 4.3 Profession-Level Breakdown

The life expectancy gap varies substantially by creative profession. Table 2 reports migrant and non-migrant average life expectancy and the gap for each of the six profession categories in our dataset.

**Table 2: Life Expectancy by Profession**

| Profession | n (Migrant) | n (Non-Migrant) | Migrant LE | Non-Migrant LE | Gap |
|------------|------------|-----------------|-----------|----------------|-----|
| Writers/Poets | 261 | 1,451 | 73.2 | 69.4 | +3.8y |
| Visual Artists | 330 | 1,774 | 73.8 | 69.9 | +3.9y |
| Musicians/Composers | 249 | 822 | 74.4 | 69.8 | +4.6y |
| Theatre/Film | 53 | 619 | 76.5 | 69.9 | +6.6y |
| Architects/Designers | 58 | 411 | 77.7 | 70.9 | +6.8y |
| Other Creative | 87 | 195 | 78.8 | 69.9 | +8.9y |

Several observations are notable. First, the life expectancy gap is consistent across all profession categories — there is no profession for which migrants and non-migrants achieved equivalent longevity. Second, the gap is largest for Theatre/Film workers (+6.6 years), Architects/Designers (+6.8 years), and the heterogeneous "Other Creative" category (+8.9 years).

The larger gap for Theatre/Film workers may reflect the particular ideological vulnerability of this profession: theatre was a powerful vehicle for national expression and was therefore subject to especially intense Soviet surveillance and intervention. Directors and actors who remained in Soviet Ukraine were required to stage works in the approved Socialist Realist style, were subject to repertoire censorship, and faced arrest if their work was deemed insufficiently ideological. The small migrant sample size for Theatre/Film (n=53) warrants caution in interpreting this figure.

Writers and Poets, while showing the smallest gap (+3.8 years), nonetheless demonstrate a robust and statistically significant mortality differential. The larger sample sizes in both the migrant (n=261) and non-migrant (n=1,451) categories for this profession make this the best-powered estimate in the profession-level breakdown.

Visual Artists show a similar gap (+3.9 years) with the largest non-migrant sample (n=1,774), again providing high statistical confidence. Musicians and Composers show a moderate gap (+4.6 years), consistent with the overall average.

### 4.4 Repression Period Analysis

The non-migrant dataset of 5,272 workers provides sufficient statistical power to examine mortality patterns by historical period. Table 3 classifies deaths among non-migrants by the established historiographic periodisation of Soviet Ukrainian history and reports average age at death within each period.

**Table 3: Non-Migrant Deaths by Historical Period**

| Period | Historical context | Deaths | Avg age at death |
|--------|--------------------|--------|-----------------|
| Pre-1917 | Pre-Soviet baseline | 103 | 51.8 |
| 1917–1921 | Revolution and civil war | 65 | 53.8 |
| 1922–1929 | Early Soviet/NEP period | 76 | 54.2 |
| 1930–1933 | Holodomor and first Five-Year Plan | 33 | 55.6 |
| 1934–1938 | Great Terror | 107 | 51.3 |
| 1939–1945 | World War II | 173 | 51.3 |
| 1946–1953 | Late Stalinist period | 83 | 60.7 |
| 1954–1964 | Khrushchev Thaw | 115 | 63.4 |
| 1965–1991 | Late Soviet period | 923 | 65.3 |
| Post-1991 | Independent Ukraine | 3,594 | 74.1 |

The pre-1917 baseline average age at death of 51.8 years reflects normal mortality conditions of early-twentieth-century Ukraine, which were significantly lower than modern life expectancy due to infectious disease, poor medical care, and physical hardship generally. This baseline is important context for interpreting the Soviet-period figures: some of the elevated early mortality in the Soviet period reflects these pre-existing conditions as well as Soviet-specific causes.

The most striking figure in Table 3 is the Great Terror period (1934–1938): 107 deaths with an average age of just 51.3 years — the lowest average age of any identified period in the Soviet era, equal to the wartime average and below even the pre-1917 baseline. Given that medical care and average lifespan were generally improving across this period in the rest of Europe, the drop in average age at death during the Great Terror to levels below pre-Soviet baselines is a quantitative signal of abnormal, cause-specific mortality — that is, mass executions and Gulag deaths of people who would otherwise have lived considerably longer.

The World War II period (1939–1945) records the highest raw death count among pre-independence periods (173 deaths) and an average age of 51.3 years, matching the Terror period. This reflects deaths from combat, occupation, famine, deportation, and the general mortality catastrophe of wartime in Eastern Europe.

The post-1991 period dominates numerically (3,594 deaths, 68% of all non-migrant deaths) with an average age at death of 74.1 years — dramatically higher than any Soviet-era period. This concentration of deaths in the post-independence period reflects both the large cohort of non-migrants born in the 1920s and 1930s who survived into old age in independent Ukraine, and the improvement in mortality conditions following the end of Soviet rule. This cohort's inclusion in V2 (excluded in V1 by the pre-1991 cutoff) is the primary driver of the narrowing of the life expectancy gap from 9 years (V1) to 4.77 years (V2).

### 4.5 The 1937 Spotlight

The year 1937 — the peak year of the Stalinist Great Terror — warrants dedicated analysis. Our non-migrant dataset records 38 deaths in 1937, with a mean age at death of just 43 years (range: 25–74). This is the single most lethal year for Ukrainian creative workers in our dataset relative to expected mortality.

**Table 4: Profession Breakdown of 1937 Deaths (Non-Migrants)**

| Profession | Deaths in 1937 |
|------------|---------------|
| Writers/Poets | 21 |
| Musicians/Composers | 6 |
| Visual Artists | 6 |
| Theatre/Film | 3 |
| Other Creative | 2 |
| **Total** | **38** |

Writers and Poets account for 21 of the 38 deaths in 1937 — 55% of that year's creative worker deaths — despite representing approximately 27% of the total non-migrant dataset. This overrepresentation of literary figures in 1937 mortality is consistent with the historical record: the Soviet security apparatus targeted writers and poets with particular intensity because of their role in shaping national consciousness through language. Ukrainian-language literary production was considered inherently politically suspect, and the literary intelligentsia was subject to disproportionate surveillance, arrest, and execution.

The mean age at death of 43 years for 1937 victims — compared to the 65.3-year average for the entire Late Soviet period — is not an artefact of a different age distribution in the cohort but reflects the truncation of lives that were cut short by execution or Gulag conditions rather than by natural causes. The youngest victim in the 1937 cohort was 25 years old; the oldest was 74. The distribution is dominated by working-age adults in their thirties, forties, and fifties — prime creative years — who were arrested, sentenced in summary proceedings, and shot.

These 38 deaths in a single year represent only the confirmed creative workers in our dataset. The actual toll on Ukrainian cultural workers in 1937 was substantially higher; our figure reflects only those with ESU entries, which itself represents a survivorship selection (individuals whose work was significant enough to be encyclopedically documented despite their execution).

### 4.6 Birth Cohort Analysis

The life expectancy gap between migrants and non-migrants is not uniform across birth cohorts. Table 5 presents average life expectancy by decade of birth for both groups.

**Table 5: Life Expectancy by Birth Cohort**

| Birth cohort | Migrant LE | Non-Migrant LE | Gap |
|-------------|-----------|----------------|-----|
| 1880s | 72.3 | 61.7 | +10.6y |
| 1890s | 75.4 | 63.6 | +11.8y |
| 1900s | 74.8 | 67.2 | +7.6y |
| 1910s | 73.9 | 68.5 | +5.4y |
| 1920s | 72.1 | 71.8 | +0.3y |

The birth cohorts of the 1880s and 1890s — the generation that came of age during the First World War, the Revolution, and the early Soviet period, and who formed the core of the Executed Renaissance — show by far the largest life expectancy gaps: 10.6 years for the 1880s cohort and 11.8 years for the 1890s cohort. These are the workers who would have been in their thirties, forties, and fifties during the peak repression years of 1930–1938, and who, if they remained in Soviet Ukraine, faced a dramatically elevated risk of execution, imprisonment, or death in the Gulag.

Those who emigrated from the 1890s cohort — typically leaving Ukraine during the first wave of emigration (1917–1921) or escaping westward during World War II — achieved an average of 75.4 years, consistent with normal mortality expectations for educated professionals in Western Europe and North America during this period. Those who remained faced an average of just 63.6 years, a figure depressed substantially by the mass mortality of the repression periods.

The birth cohorts of the 1900s and 1910s show progressively smaller gaps (7.6 and 5.4 years respectively). Workers born in these cohorts were younger during the peak repression years, making some more likely to have survived into less lethal periods, though many were nonetheless victims of wartime mortality.

The 1920s cohort shows the most striking finding: a gap of just 0.3 years. Workers born in the 1920s were children or young adolescents during the worst repression periods, largely too young to have been targeted during the Great Terror, and were subsequently subject to the more bureaucratic (though still brutal) cultural repression of the late Soviet era rather than mass physical liquidation. Many lived into old age in post-Soviet Ukraine. The near-elimination of the life expectancy gap for this cohort strongly supports our interpretation that the overall gap is driven primarily by political violence against older cohorts rather than by baseline differences in health, socioeconomic status, or selection effects between migrants and non-migrants.

### 4.7 Geographic Patterns

Migration rates varied substantially by city of birth. Table 6 presents migration rates for the five cities with the largest representation in the dataset.

**Table 6: Migration Rates by Birth City**

| City | Total in dataset | % Migrated |
|------|-----------------|-----------|
| Lviv | 480 | 17.3% |
| Ternopil | 53 | 15.1% |
| Chernivtsi | 54 | 14.8% |
| Kyiv | 1,296 | 5.2% |
| Donetsk (Stalino) | 48 | 0% |

The geographic pattern is striking and historically coherent. Lviv, Ternopil, and Chernivtsi — all cities in western Ukraine (Galicia and Bukovina) — show the highest migration rates, ranging from approximately 15% to 17%. These cities were incorporated into the Soviet Union only in 1939–1940 (following the Molotov-Ribbentrop Pact and subsequent Soviet annexation of Eastern Poland and northern Romania), giving their residents both more recent experience of non-Soviet existence and less time under Soviet control before the opportunity to flee during World War II. Western Ukrainian creative workers had stronger connections to Polish and Austrian cultural institutions, were more likely to have had contacts in Western Europe, and had a shorter period of Soviet acculturation — all factors that likely increased both the propensity and the opportunity to emigrate.

Kyiv's migration rate of 5.2% is substantially lower, reflecting the city's deeper integration into Soviet administrative and cultural structures. Kyiv was the capital of Soviet Ukraine and its cultural workers were subject to intense ideological oversight but also more deeply embedded in Soviet institutions — the Writers' Union, the Composers' Union, the Academy of Arts — that provided material incentives to remain.

Donetsk (historically called Stalino during the Soviet period) shows a 0% migration rate in our dataset. This reflects not just a geographic and cultural distance from western emigration routes, but also the city's character as an industrial centre that was less hospitable to the kind of nationally-oriented creative work that motivated emigration. Creative workers from the Donbas region were fewer in number, more likely to be Russian-speaking, and had fewer connections to the diaspora networks that facilitated emigration.

### 4.8 Death Age Distribution

The distribution of ages at death further illuminates the mortality differential between the two groups.

**Premature death (before age 50):** 9.2% of non-migrants died before age 50, compared to 5.8% of migrants — a relative excess of 59% more premature deaths among non-migrants.

**Very young death (before age 30):** 77 non-migrants versus 6 migrants died before age 30. Expressed as a proportion of their respective group sizes: 1.46% of non-migrants versus 0.58% of migrants died before age 30 — a ratio of approximately 2.5:1.

**Age 30–39 deaths:** 130 non-migrants versus 22 migrants.

**Age 40–49 deaths:** 276 non-migrants versus 32 migrants.

**Long life (age 90+):** 294 non-migrants and 141 migrants reached age 90 or older. As a proportion: 5.6% of non-migrants versus 13.6% of migrants achieved this milestone. This finding is counterintuitive at first glance — if non-migrants faced greater mortality risk, why do more of them in absolute terms reach age 90? The answer lies in sample sizes: non-migrants outnumber migrants five to one in this dataset, so even at a lower rate, they produce more individuals in the 90+ bracket in absolute terms.

The age distribution analysis confirms the interpretation of the life expectancy gap: non-migrants show a pronounced left tail (excess premature deaths from political violence) combined with a roughly normal long-life distribution, while migrants show a more symmetric distribution with a lighter left tail and a modestly heavier right tail (more long-lived individuals proportionally).

---

## 5. Discussion

### 5.1 Interpretation of the Life Expectancy Gap

The 4.77-year gap in average life expectancy between migrant and non-migrant Ukrainian creative workers is statistically robust, methodologically defensible, and consistent across all analytical disaggregations. It is, however, not a simple measure of the mortality cost of Soviet rule for any individual — it is a population-level summary statistic that aggregates across highly heterogeneous individual experiences.

The gap reflects, we argue, primarily four mechanisms:

**Direct political mortality.** The most evident mechanism is execution, imprisonment, and Gulag death. The data on 1937 deaths (average age 43, with Writers accounting for 55% of victims), on the Great Terror period (average age at death 51.3, the joint lowest of any Soviet period), and on the overrepresentation of very young deaths among non-migrants (77 deaths before age 30 versus 6 among migrants) all point to a substantial excess mortality from direct state violence that had no equivalent in migrant communities.

**Indirect mortality from Soviet conditions.** Beyond direct political violence, Soviet conditions — poor nutrition, restricted medical care, psychological stress from constant surveillance and self-censorship, the health consequences of Gulag survival, and enforced poverty — likely contributed to excess mortality among non-migrants across the entire Soviet period. This mechanism is not directly measurable from our data but is consistent with the lower average age at death in every Soviet-era period compared to the post-1991 period.

**Selection effects in emigration.** Not all emigration is equivalent in its effect on subsequent mortality. Those who emigrated during the first wave (1917–1921) typically did so from positions of some privilege — they had resources, connections, and the ability to plan. Those who fled during the second wave (World War II) often did so under extremely dangerous conditions, with significant mortality risk during flight. It is plausible that the migrant group in our dataset is positively selected for resourcefulness, social capital, and health relative to the non-migrant group, which would mean that some portion of the life expectancy gap reflects pre-migration differences rather than the causal effect of Soviet conditions.

**Period effects and cohort differences.** As noted in the birth cohort analysis, the gap is concentrated in the 1880s and 1890s cohorts — the Executed Renaissance generation — and is nearly absent in the 1920s cohort. This cohort patterning argues against a simple interpretation of the gap as reflecting baseline differences between migrants and non-migrants; if the gap were primarily driven by selection effects, we would expect it to be more uniform across cohorts.

### 5.2 The V1-to-V2 Gap Narrowing

The reduction in the measured gap from 9 years (V1) to 4.77 years (V2) deserves careful interpretation. It does not represent a finding that Soviet repression was less lethal than previously estimated. Rather, it reflects the inclusion of a large cohort of non-migrants who survived the Soviet period and lived into old age in independent Ukraine — a population that was categorically excluded from V1 by the pre-1991 death cutoff.

The V1 finding of a 9-year gap was a real finding within its analytical scope: among workers who died before 1991, the gap was approximately that large. V2 does not contradict V1; it extends the analysis to a more complete and representative population. The policy implication is methodological: future studies of Soviet-era mortality should not apply post-Soviet death cutoffs, as doing so systematically excludes the longest-lived members of the "stayed" cohort and artificially inflates the measured mortality differential.

### 5.3 Geographic Findings and Their Significance

The strong west-east gradient in migration rates — from Lviv's 17.3% to Donetsk's 0% — is not merely a demographic curiosity. It reflects a fundamental division in Ukrainian cultural geography that predates the Soviet period and has continued to shape Ukrainian society through independence and into the present. Western Ukraine's Galician and Bukovinian regions were under Austro-Hungarian rule until 1918, developed a distinct civic and cultural tradition, and maintained stronger connections to Central European and Western intellectual life. This made emigration to Vienna, Prague, Paris, and ultimately North America both more conceivable and more practically feasible for western Ukrainian creative workers.

Eastern and southern Ukrainian creative workers, by contrast, were longer-embedded in Soviet institutions, faced steeper barriers to emigration (both practical and ideological), and were more likely to have professional identities intertwined with Soviet cultural organisations. That the Donbas region shows 0% migration in our dataset is consistent with this broader pattern but should be interpreted cautiously given the small sample size (n=48).

### 5.4 Limitations

**Survivorship bias in the ESU.** The Encyclopedia of Modern Ukraine documents individuals whose work was significant enough to merit encyclopedic inclusion. This represents a small fraction of all Ukrainian creative workers, and there is reason to believe it is not a random sample of that population. Individuals who were executed at young ages left smaller bodies of work and may be underrepresented in the ESU relative to their actual numbers. Conversely, very prolific or long-lived workers may be overrepresented. This source of bias could operate in either direction with respect to our life expectancy estimates.

**Migration status as a simplification.** Our binary classification of migration status (migrated vs. did not migrate) is a simplification of a complex range of experiences. Some non-migrants were internally displaced within the Soviet Union; some were imprisoned in the Gulag for periods before release; some lived in regions under different occupying powers at different times. Our classification system makes reasonable distinctions where the data permit, but it should not be treated as capturing the full complexity of individual experiences.

**AI-assisted classification errors.** The use of Claude for nationality and migration classification introduces potential systematic errors if the model's training data, linguistic capabilities in Ukrainian, or reasoning about Soviet historical context were biased in any particular direction. We estimate an error rate below 5% based on a sample check of Claude's determinations (see SCIENTIFIC_METHODOLOGY.md), but we cannot rule out systematic directional bias.

**Causal claims.** This paper establishes a robust statistical association between migration status and life expectancy among Ukrainian creative workers. We do not, and cannot, establish clean causal estimates from observational data of this kind. The life expectancy gap may reflect, in whole or in part, pre-existing differences between the migrant and non-migrant populations rather than the causal effect of Soviet conditions on mortality. The birth cohort analysis provides some support for a causal interpretation, but selection effects cannot be ruled out.

**Missing data.** Of the 16,215 entries in our initial dataset, only 6,310 — approximately 39% — met our inclusion criteria for the primary life expectancy analysis. The remaining 61% were excluded primarily because they lacked death dates (living individuals or individuals whose death date was not recorded in the ESU) or because migration status could not be determined. If the excluded population differs systematically from the included population in ways correlated with life expectancy, our estimates may be biased.

### 5.5 Comparisons to Related Research

Our findings are broadly consistent with existing historical scholarship on Soviet repression and with the limited quantitative literature on mortality in Soviet-era professional populations. Studies of Gulag mortality (Barnes, 2011; Applebaum, 2003) document life expectancy at arrest of approximately 35–45 years among those who died in the Gulag, consistent with our finding that the most lethal periods in our data (1934–1938 and 1939–1945) show average ages at death of approximately 51 years — higher than the Gulag average because our dataset includes both those who died in the Gulag and those who died of natural causes during those periods.

Comparative demography of Soviet versus Western European professional populations in the mid-twentieth century (Andreev et al., 1998; Meslé et al., 2002) documents a general Soviet mortality penalty of approximately 3–7 years relative to Western European equivalents by the 1970s and 1980s. Our finding of a 4.77-year gap is consistent with this range, though our dataset's specific focus on a targeted professional group subject to particular repression means our estimate captures both the general Soviet mortality penalty and the profession-specific repression penalty.

---

## 6. Conclusion

This paper presents the most comprehensive quantitative analysis to date of life expectancy among Ukrainian creative workers under Soviet occupation. Across a dataset of 6,310 individuals with confirmed birth dates, death dates, and migration status — fifteen times larger than our V1 dataset — we find a statistically robust 4.77-year life expectancy gap in favour of those who emigrated, with a Mann-Whitney U p-value of approximately 0.0 and a Cohen's d of 0.319 (medium effect size).

The gap is not uniform: it is largest for the 1880s and 1890s birth cohorts (the Executed Renaissance generation, with gaps of 10.6 and 11.8 years respectively), for Theatre/Film workers (+6.6 years) and Architects/Designers (+6.8 years), and for workers born in western Ukrainian cities (who emigrated at rates of 15–17% compared to near-zero rates in eastern Ukraine). It is nearly absent for the 1920s birth cohort (+0.3 years), providing strong evidence that the gap is driven primarily by cohort-specific political violence rather than by stable baseline differences between migrants and non-migrants.

The 1937 spotlight analysis reveals that 38 Ukrainian creative workers in our dataset died in that single year at an average age of 43 — predominantly Writers and Poets — in a pattern consistent with mass political execution rather than natural mortality. The repression period analysis shows average ages at death of 51.3 years during both the Great Terror (1934–1938) and World War II, the lowest of any period in our data, contrasting with 74.1 years for those who died in the post-independence period.

These findings constitute quantitative corroboration of what Ukrainian historians have documented through archival and testimonial evidence: that Soviet cultural policy inflicted a measurable, statistically detectable mortality cost on the creative workers who remained under Soviet rule, concentrated particularly in the generation that came of age between the Revolution and the Great Terror. The numbers do not tell the full story — they cannot capture the individual lives, the works that were never written, the music that was never composed, the theatres that went dark — but they provide an empirical foundation for claims that have sometimes been contested on the grounds of quantitative imprecision.

We make no claim that this analysis is definitive. The ESU-based dataset is not a complete census of Ukrainian creative workers; our migration classification system makes simplifications that the historical record does not always support; and the selection effects inherent in emigration preclude clean causal inference. Future research should seek to replicate and extend these findings using alternative data sources — particularly Soviet-era repression records, diaspora archives, and memorial databases — and should apply methods capable of addressing the selection problem more rigorously.

The Executed Renaissance was not a metaphor. It was a demographic event — one that this study has, for the first time at scale, begun to measure.

---

## 7. References

Andreev, E. M., Darsky, L. E., & Kharkova, T. L. (1998). *Demographic history of Russia: 1927–1959*. Informatika Publishers.

Applebaum, A. (2003). *Gulag: A history*. Doubleday.

Barnes, S. A. (2011). *Death and redemption: The Gulag and the shaping of Soviet society*. Princeton University Press.

Berdnyk, E., & Symkin, M. (2025). Life expectancy of Ukrainian creative industry workers during the Soviet occupation: A preliminary study (V1). [Unpublished manuscript].

Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.

Grabowicz, G. G. (1982). The poet as mythmaker: A study of symbolic meaning in Taras Shevchenko. *Harvard Ukrainian Studies*, *5*(1), 1–67.

Інститут енциклопедичних досліджень НАН України (Institute of Encyclopedic Research of the National Academy of Sciences of Ukraine). (2026). *Енциклопедія сучасної України* [Encyclopedia of Modern Ukraine]. esu.com.ua.

Lavrinenko, Y. (1959). *Rozstriliane vidrodzhennia: Antolohiia 1917–1933* [The Executed Renaissance: Anthology 1917–1933]. Instytut Literacki.

Meslé, F., Vallin, J., & Hertrich, V. (2002). *Causes of death in Russia: Assessing trends since the 1950s*. Institut National d'Études Démographiques.

Myshanych, O., & Semenko, M. (1991). *Ukrainska literatura XX stolittia* [Ukrainian literature of the 20th century]. Naukova Dumka.

Škandrij, M. (2010). *Ukrainian nationalism: Politics, ideology, and literature, 1929–1956*. Yale University Press.

Subtelny, O. (2000). *Ukraine: A history* (3rd ed.). University of Toronto Press.

---

## 8. Figure Captions

The following figures accompany this paper. Each figure was generated computationally from the V2 dataset and is available in the `/charts/` subdirectory of the project repository.

**Figure 1 (`fig1_le_distribution.png`):** Violin plot showing the full distribution of ages at death for migrant (n=1,038) and non-migrant (n=5,272) Ukrainian creative workers. The horizontal line within each violin indicates the median. The wider body of the non-migrant violin at younger ages reflects the excess premature mortality from political violence. Note the heavier left tail in the non-migrant distribution.

**Figure 2 (`fig2_period_deaths.png`):** Bar chart showing the number of non-migrant deaths by historical period (Pre-1917 through Post-1991) with an overlaid line showing average age at death within each period. The decline in average age during the Great Terror (1934–1938) and World War II (1939–1945) periods is clearly visible.

**Figure 3 (`fig3_profession_gap.png`):** Horizontal bar chart comparing migrant and non-migrant average life expectancy by profession category. The gap in each category is labelled. Theatre/Film, Architects/Designers, and Other Creative show the widest gaps.

**Figure 4 (`fig4_cohort_gap.png`):** Line chart showing average life expectancy by birth decade for migrants (dashed line) and non-migrants (solid line). The convergence of the two lines for the 1920s cohort and the wide divergence for the 1880s and 1890s cohorts are the primary features of interest.

**Figure 5 (`fig5_1937_spotlight.png`):** Scatter plot of ages at death for the 38 non-migrant creative workers who died in 1937, grouped by profession. Writers/Poets are shown in a distinct colour. The mean age of 43 years is marked with a horizontal reference line.

**Figure 6 (`fig6_geographic_migration.png`):** Map of Ukraine showing migration rates by birth city, with circle size proportional to the number of workers in the dataset from each city and colour intensity proportional to the migration rate. The west-east gradient is clearly visible.

**Figure 7 (`fig7_age_distribution_histogram.png`):** Overlapping histograms of age at death for migrants and non-migrants, normalised to proportions to account for the difference in group sizes. The excess of non-migrant deaths at ages below 50 and the relative excess of migrant deaths at ages above 75 are clearly visible.

---

## 9. AI Methodology Note

In the interest of full methodological transparency, we disclose the following regarding the use of artificial intelligence tools in this study.

**Data classification.** Claude (Anthropic), a large language model, was used to review 1,356 entries with ambiguous nationality markers and to assist with migration classification for a subset of entries where the biographical text was ambiguous. Claude was provided with the full Ukrainian-language ESU text for each entry and asked to classify the entry according to pre-specified criteria documented verbatim in the companion SCIENTIFIC_METHODOLOGY.md file. All Claude classifications were performed using Claude claude-sonnet-4-6 with default temperature settings.

**Quality assurance.** A sample of Claude's nationality determinations was reviewed by a human researcher. The estimated error rate is documented in SCIENTIFIC_METHODOLOGY.md. Claude's classifications were not adjusted based on their consistency with our hypothesised findings; the review was conducted before the primary statistical analysis was performed.

**Writing assistance.** Claude was used as a writing assistant in the drafting of this manuscript. The empirical content, analytical interpretation, and conclusions are entirely the work of the human authors. Claude's contribution was limited to prose editing, structural suggestions, and assistance with academic English phrasing.

**No autonomous decision-making.** AI tools did not make autonomous decisions about study design, statistical methods, or the interpretation of findings. All methodological choices documented in this paper were made by the human research team.

We believe that transparent disclosure of AI tool use is essential for the integrity of the academic record and for enabling other researchers to replicate our methodology. The full prompts, model names, and procedural details are documented in the companion SCIENTIFIC_METHODOLOGY.md.

---

*Manuscript prepared 2026. Authors: Elza Berdnyk, Mark Symkin.*
*Data source: Encyclopedia of Modern Ukraine (esu.com.ua), accessed 2026.*
*Correspondence: [author contact details to be added before submission]*
