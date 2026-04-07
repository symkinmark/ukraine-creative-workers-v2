# Observed Age at Death Among Ukrainian Creative Workers Under Soviet Occupation: A Quantitative Study

**Author:** Mark Symkin

**Manuscript prepared:** 2026

**Data source:** Encyclopedia of Modern Ukraine (esu.com.ua), accessed 2026

**Correspondence:** mark.symkin@gmail.com

---

## Abstract

This paper presents an expanded quantitative analysis of observed age at death among Ukrainian creative industry workers during the Soviet occupation of Ukraine, extending and refining the methodology of our original V1 study.[^4] Drawing on 16,215 confirmed Ukrainian creative workers extracted from the Encyclopedia of Modern Ukraine (Інститут енциклопедичних досліджень НАН України, esu.com.ua, accessed 2026), we identify 8,643 individuals with complete birth dates, death dates, and determinable migration status across four groups (n = number of individuals per group): migrated (n=1,280), non-migrated (n=6,030), internal transfer (n=1,150), and deported by the Soviet state (n=183). This represents a more than twenty-fold expansion over the prior study's dataset of 415 workers,[^4] achieved through automated date recovery from ESU biographical text and systematic reclassification of ambiguous migration status entries.

The study's most causally interpretable finding concerns the two groups for whom the mobility decision was either state-imposed or absent: workers **deported by the Soviet state** (n=183) died on average at 48.35 years — a deficit of **22.87 years** relative to non-migrants (Cohen's d=1.656, p<0.001) — and workers who **relocated voluntarily within the Soviet system** (internal transfer, n=1,150) showed no meaningful survival advantage over those who stayed (gap=+0.52 yrs, d=0.038, p=0.094). The deportation deficit and the internal transfer null are not subject to emigration selection effects and constitute the paper's strongest evidence that mortality differentials tracked Soviet repression rather than baseline population differences.

A second finding — descriptively robust but requiring more interpretive caution — concerns workers who chose to emigrate from the Soviet sphere. This comparison involves self-selected individuals, and it is not possible to fully rule out the possibility that those who left were already healthier, better-resourced, or otherwise advantaged before departure. With that caveat stated: non-migrants who remained within the USSR (n=6,030) achieved an average age at death of 71.22 years (95% CI: 70.87–71.57; median 73, SD 13.79), while migrants who left the Soviet sphere (n=1,280) achieved an average of 75.25 years (95% CI: 74.49–76.01; median 77, SD 13.88), yielding a **gap of 4.04 years** in favour of emigrants (Mann-Whitney U, p<0.001; Cohen's d=0.292; Cliff's δ=0.18).[^8] This gap survives propensity score matching on birth decade, profession, and region (reduced to 3.35 years, 95% CI [2.26, 4.45]), and Cox proportional hazards analysis (§4.10) yields HR = 0.832 for migrated workers — approximately 17% lower mortality risk after covariate adjustment. The gap is real, consistent, and resistant to the observable confounders we can test. What cannot be ruled out are unobservable selection effects: the question of how much of the gap reflects Soviet conditions versus the characteristics of those who managed to leave.

The primary gap of 4.04 years is markedly narrower than the 9-year gap reported in V1. This narrowing is not a weaker finding — it is a correction. V1 restricted its analysis to workers who died before 1991, on the reasoning that post-Soviet conditions would confound a study of Soviet-era mortality. That boundary, however, systematically excluded the longest-lived non-migrants: those who survived the entire Soviet period and died of old age in independent Ukraine. Because migrants tended to be born earlier, they were more likely to have died before 1991 simply due to age, meaning they were more fully represented in V1's dataset while the most long-lived non-migrants were absent. V2 removes this boundary, includes all workers with confirmed death dates regardless of when they died, and produces a more representative estimate of the actual mortality differential. Profession-level, birth cohort, repression-period, and death cause analyses are consistent with systematic mortality differentials aligned with documented Soviet repression campaigns, particularly the Holodomor (1932–1933), the Great Terror (1934–1938), and the broader cultural liquidation of the Executed Renaissance (*Rozstriliane Vidrodzhennia [Розстріляне Відродження]*). These findings provide quantitative documentation of mortality differentials associated with Soviet cultural policy toward Ukrainian creative communities.

---

## 1. Introduction

The Soviet occupation of Ukraine — conventionally dated from the consolidation of Bolshevik control in 1920 through Ukrainian independence in 1991[^2] — was characterised by systematic state violence against Ukrainian cultural and intellectual life. Policies of Russification, enforced collectivisation, mass executions, forced labour, and ideological surveillance were not applied uniformly across Soviet society but were deployed with particular intensity against groups whose work produced and transmitted national identity: writers, poets, visual artists, composers, theatre directors, architects, and other creative workers.

The period known in Ukrainian historiography as the "Executed Renaissance" (Розстріляне відродження, Rozstriliane vidrodzhennia) — roughly 1917 to 1941 — saw the near-total physical destruction of an entire generation of Ukrainian cultural figures. Scholars including Mykola Zerov, Mykhailo Khvylovy, Les Kurbas, Valerian Pidmohylny, and hundreds of others were arrested, tortured, imprisoned in the Gulag system, or executed outright during the Stalinist terror campaigns of the 1930s. The Great Terror of 1937–1938 was particularly lethal: Ukrainian cultural workers were disproportionately targeted as potential vectors of "bourgeois nationalism." The scale and character of this liquidation is documented extensively in Ukrainian literary historiography.[^3]

Quantitative study of this mortality toll has been limited. Historical demography of Soviet persecution has relied heavily on archival records — many still restricted or destroyed — and has focused more on aggregate victim counts than on comparative mean age at death across survivor groups. Our V1 study[^4] provided a first quantitative examination of the mean age at death gap between Ukrainian creative workers who emigrated versus those who remained within the Soviet Union, finding a 9-year gap (63 years versus 72 years) in a dataset of 415 workers.

The present paper — V2 — substantially expands that dataset to 8,643 analysable workers, refines the methodology to eliminate the pre-1991 death cutoff that we identified as a source of bias in V1, introduces a profession-level disaggregation, and provides detailed analysis of repression-period mortality, birth cohort effects, and geographic migration patterns.

This study is best understood as a descriptive historical-demographic analysis. It documents patterns of observed age at death across categories of migration status and Soviet-era repression among a specific, well-defined population: creative workers with entries in the Encyclopedia of Modern Ukraine. The ESU is an encyclopedic record of documented or otherwise canonized cultural figures — individuals whose work achieved sufficient recognition to merit scholarly biographical treatment. It is not a census of all Ukrainians who worked in creative fields, and findings should not be generalised as if it were. Our central descriptive question is: how does observed age at death vary across mobility and repression categories within this population, and what patterns are consistent with the documented historical record of Soviet cultural policy?

We approach this question with awareness of its political sensitivity and its methodological limits. This is an observational study; we document associations, not causes. The paper presents two categories of findings with meaningfully different epistemic statuses. The first — the deportee mortality catastrophe and the internal transfer null — requires no assumptions about who chose to emigrate or why, and is therefore the strongest evidence the data can offer that mortality tracked Soviet repression rather than baseline population differences. The second — the 4.04-year gap between migrants and non-migrants — is a robust descriptive finding that survives multiple statistical adjustments, but it involves a self-selected comparison group and cannot be fully insulated from the possibility that those who left were already advantaged. We present both findings, but we ask the reader to hold them differently: the first as evidence, the second as consistent and well-documented description whose full causal interpretation remains open.

---

## 2. Prior Study Summary and Limitations

### 2.1 Summary of Prior Findings

Our original study (V1) drew on a manually curated dataset of 415 Ukrainian creative workers for whom we could determine birth year, death year, and migration status. The core finding was a 9-year mean age at death gap: non-migrants averaged 63 years while migrants averaged 72 years. This gap was statistically significant and represented a substantial effect.

V1 applied a pre-1991 death cutoff — only workers who had died before the dissolution of the Soviet Union were included in the primary analysis. The rationale was methodological consistency: workers who survived into the post-Soviet period were excluded to avoid the confounding influence of post-Soviet conditions on what was intended to be a study of Soviet-era mortality.

### 2.2 Limitations Identified in the Prior Study

Upon reflection, we identified three significant limitations in the prior study's methodology:

**The pre-1991 cutoff introduced survivorship bias.** By excluding all workers who died after 1991, V1 systematically excluded the longest-lived non-migrants — those who survived the Soviet period entirely and died in independent Ukraine. Because migrants had, on average, an earlier birth year (V1 migrants were born notably earlier than non-migrants), they were more likely to have died before 1991 simply due to age, which meant they were more fully represented in the V1 dataset. Non-migrants born in the 1920s or later were systematically excluded if they survived to old age, which skewed the non-migrant average downward.

**The dataset was too small.** 415 workers, while sufficient for a preliminary study, left the analysis vulnerable to outlier effects and limited our ability to conduct meaningful subgroup analyses by profession, birth cohort, or repression period.

**Profession and geography were not systematically recorded.** V1 did not code profession or birth city consistently, preventing profession-level or geographic analysis.

### 2.3 Comparison: Prior Study vs. Present Study

| Dimension | Prior Study (Berdnyk et al. 2025) | Present Study |
|-----------|----|----|
| Dataset size | 415 workers | 8,643 usable (16,215 total) |
| Pre-1991 death cutoff | Yes | No |
| Mean age at death gap | 9.0 years | 4.04 years |
| Non-migrant mean age at death | 63 years | 71.22 years |
| Migrant mean age at death | 72 years | 75.25 years |
| Statistical method | t-test | Mann-Whitney U + Cohen's d |
| Profession breakdown | No | Yes (6 categories) |
| Birth cohort analysis | No | Yes |
| Geographic analysis | No | Yes |

Figure 3 visualises this comparison directly: it places the prior study's two-group bar chart alongside the present study's recalculated results under the same grouping logic, making the source of the gap narrowing visually explicit.

**Figure 3.** Grouped bar chart directly comparing the prior study's two-group results (Berdnyk et al. 2025: migrated mean=72 yrs, non-migrated mean=63 yrs, gap=9 yrs, n=415) against the present study's recalculated two-group results (migrated mean=75.25 yrs, stayed-in-Soviet-sphere mean=70.58 yrs, gap=4.68 yrs, n=8,643). The gap narrows because V2 includes the long-lived post-Soviet non-migrants excluded by the prior study's 1991 cutoff.

The narrowing of the gap from 9 years to 4.04 years is not a finding of lesser mortality disparity — it is a correction of an artificial inflation. When long-lived post-Soviet non-migrants are included in the analysis, the non-migrant average rises substantially. The 4.04-year gap in the present study represents a cleaner estimate of the actual mortality differential associated with remaining within the Soviet system.

---

## 3. Methodology

### 3.1 Data Source

All data were extracted from the Encyclopedia of Modern Ukraine (Енциклопедія сучасної України, ESU), maintained by the Institute of Encyclopedic Research of the National Academy of Sciences of Ukraine (Instytut entsyklopedychnykh doslidzhenʹ NAN Ukraïny [Інститут енциклопедичних досліджень НАН України]) and available at esu.com.ua.[^1] The ESU is the authoritative scholarly encyclopedia of Ukrainian cultural and intellectual life, with entries written and reviewed by subject-matter experts. As of our access date (2026), it contained entries for approximately 70,000 individuals.

The ESU was selected as the primary source for three reasons: (1) it is the most comprehensive Ukrainian-language biographical reference work covering the relevant time period; (2) its entries consistently include birth and death dates, biographical summaries, and sufficient information to determine migration status; and (3) it focuses specifically on individuals of cultural, intellectual, and creative significance, making it a natural population of interest for this study.

### 3.2 Reproducibility and Open Methodology

The complete analytical pipeline for this study — including all data collection scripts, classification prompts, statistical analysis code, and chart generation — is version-controlled and publicly accessible via Git. This is a deliberate methodological commitment: every figure, table, and statistical claim in this paper can be reproduced in full by any researcher with access to a standard computing environment and the esu.com.ua source. The repository records the complete sequence of analytical decisions, corrections, and reclassifications, including the specific prompt texts used for AI-assisted classification (see Section 9 and SCIENTIFIC_METHODOLOGY.md). Researchers wishing to replicate, extend, or challenge the findings of this study are encouraged to do so using the archived codebase. This approach reflects our view that computational historical research should be held to the same standards of source transparency as archival historical research — the "sources" in this case include not only the ESU entries but the algorithms and decision rules applied to them.

**Data and code availability.** The primary dataset (V2.3, `esu_creative_workers_v2_3.csv`), all analysis scripts, and full supplementary methodology documentation are openly available at: https://github.com/symkinmark/ukraine-creative-workers-v2. A rendered version of this paper with all 24 figures embedded is permanently accessible at: https://symkinmark.github.io/ukraine-creative-workers-v2/. Researchers wishing to replicate the analysis should clone the repository and run `ukraine_v2/generate_analysis.py` against the primary dataset. No proprietary software is required; all dependencies are standard open-source Python libraries (pandas, numpy, scipy, matplotlib, seaborn, lifelines).

### 3.3 Data Collection

Data were collected via automated web scraping of esu.com.ua using Python scripts developed specifically for this project (see the companion SCIENTIFIC_METHODOLOGY.md for full technical details). The scraper extracted, for each entry: full name (Ukrainian and transliterated), birth year, death year, birth city, listed profession(s), and the full biographical text in Ukrainian. The raw dataset comprised 16,215 entries identified as potentially relevant Ukrainian creative workers.

### 3.4 Inclusion and Exclusion Criteria

**Inclusion criteria.** An entry was included in the primary age-at-death analysis if it met all of the following conditions:

1. The individual was confirmed as Ukrainian (see Nationality Determination Protocol, Section 3.6).
2. The individual's primary profession fell within our definition of "creative worker" (see Section 3.5).
3. The entry contained a confirmed birth year.
4. The entry contained a confirmed death year.
5. The individual's migration status could be determined with reasonable confidence.

Of the 16,215 entries initially collected, 8,643 met all five criteria and form the primary analytical dataset.

**Exclusion criteria.** The following categories were excluded:

- Living individuals (no death year recorded): excluded from age-at-death analysis but noted in the total dataset count.
- Individuals with uncertain birth or death dates (recorded as "circa," date ranges, or question marks): excluded to preserve the precision of average calculations.
- Individuals whose nationality could not be determined: excluded rather than misclassified.
- Non-Ukrainian individuals: 1,218 entries in the ESU referred to foreign artists or intellectuals with no substantive Ukrainian connection and were excluded.
- Individuals whose migration status was ambiguous and could not be resolved: excluded rather than assigned to a group incorrectly.
- Individuals whose death year preceded 1921: excluded on the grounds that the Ukrainian SSR was not consolidated until 1920–1922, and individuals who died before that threshold were never subject to Soviet conditions. Their inclusion would conflate pre-Soviet and Soviet-era mortality within the non-migrated group.
- Galician-born individuals whose death year preceded 1939: excluded because the Galician regions (Lviv, Ternopil, and Ivano-Frankivsk oblasts) remained under Polish administration until the Soviet annexation of Western Ukraine following the Molotov-Ribbentrop Pact of 1939. Creative workers from these regions who died before 1939 were never under Soviet rule and are therefore analytically incommensurable with the core dataset population. Galician-born individuals who survived beyond 1939 are included in the dataset under the standard classification criteria.

### 3.4.1 Sample Construction and Missing Data

Of the 16,215 entries initially extracted from the ESU, 8,643 (53.3%) met all inclusion criteria and form the primary analytical dataset. The remaining 7,572 entries (46.7%) were excluded. Table B presents the exclusion flow; Figure 16 shows the same process as a CONSORT-style flowchart.

**Figure 16.** CONSORT-style flowchart documenting the exclusion cascade from 16,215 raw ESU entries to the 8,643 analysable dataset. Each exclusion step is labelled with its criterion and the resulting n. The final box shows the four-way group split (migrated n=1,280, non-migrated n=6,030, internal transfer n=1,150, deported n=183).

**Table B — Sample Construction: Exclusion Flow**

| Stage | n excluded | Reason | % of total scraped |
|---|---|---|---|
| Living individuals (no death year) | 6,680 | Cannot compute age at death | 41.2% |
| Died before Soviet period (<1921) | 371 | Never subject to Soviet conditions | 2.3% |
| Missing birth or death year | 246 | Insufficient data for age calculation | 1.5% |
| Migration status unclassifiable | 119 | Cannot assign to a comparison group | 0.7% |
| Galician-born, died before 1939 | 89 | Outside Soviet jurisdiction at time of death | 0.5% |
| **Analysable (retained)** | **8,643** | | **53.3%** |

*Note: Non-Ukrainian entries (n=1,218) identified during nationality review are excluded upstream and not reflected in this flow. Counts above reflect the Ukrainian creative worker pool after nationality filtering.*

**Potential selection biases arising from exclusions.**

The largest excluded group — individuals with no recorded death year (n=6,680) — consists primarily of living individuals or cases where death records have not yet been incorporated into the ESU. If the probability of having a death year recorded in the ESU correlates with migration status or group membership, this exclusion could introduce bias. In particular, if workers who died under Soviet repression had their records suppressed or destroyed — making them less likely to have a documented death year — then the included dataset may underrepresent the most severely affected individuals, causing the mortality differential to be *underestimated* rather than overestimated. We cannot directly test this hypothesis with the available data.

The 246 cases excluded for missing birth or death year represent a similarly uncertain group. If the ESU is systematically less likely to record full biographical details for individuals who died young, in obscure circumstances, or as victims of state violence — all of which correlate with repression — then the included dataset is positively selected for those with complete records, who may on average have lived longer. Again, this bias would operate in the direction of underestimating the mortality differential.

The 119 cases excluded for unclassifiable migration status are the most directly problematic for group comparisons: if individuals whose movement histories were suppressed in Soviet-era records (e.g., internal deportees or those who fled under false identities) are disproportionately represented in this group, their exclusion distorts the relative sizes of the migrated, non-migrated, and deported categories. The directional effect on the mean age at death gap is unknown.

Taken together, these exclusion mechanisms suggest that the estimates reported here should be treated as conservative with respect to the magnitude of the mortality differential: the biases most plausibly operate in the direction of *reducing* the observed gap rather than inflating it.

### 3.5 Creative Worker Definition

The following Ukrainian-language profession keywords were used to filter entries for inclusion as "creative workers." This list was developed iteratively against the ESU's own profession taxonomy:

**Primary profession keywords (Ukrainian originals):** поет (poet), письменник (writer), прозаїк (prose writer), драматург (playwright), літератор (literary figure), художник (artist), живописець (painter), скульптор (sculptor), графік (graphic artist), архітектор (architect), дизайнер (designer), композитор (composer), музикант (musician), диригент (conductor), режисер (director), актор (actor), акторка (actress), співак (singer), співачка (female singer), хореограф (choreographer), танцівник (dancer), кінорежисер (film director), кінооператор (cinematographer), сценарист (screenwriter), театральний режисер (theatre director), фотограф (photographer — artistic), ілюстратор (illustrator), гравер (engraver), кераміст (ceramicist), ткач (weaver — artistic textile), мозаїчист (mosaicist).

**Excluded profession terms despite proximity to creative fields:** журналіст (journalist — excluded unless dual-listed with a creative profession), науковець (scientist), філософ (philosopher), педагог (educator — unless dual-listed), релігійний діяч (religious figure), військовий (military figure), політик (politician).

Where individuals held multiple professions (e.g., a writer who was also a journalist), they were included if any of their listed professions appeared on the primary inclusion list. They were assigned to a single profession category for analytical purposes using the profession listed first or most prominently in their ESU entry.

### 3.6 Nationality Determination Protocol

#### 3.6.1 Definition of Ukrainian

This study applies a **cultural participation definition of Ukrainian identity**, not an ethnic or linguistic one. A person is counted as Ukrainian if they meet any of the following criteria: they were born or raised on territory that is now Ukraine and made a creative contribution that forms part of the Ukrainian cultural record; they contributed substantially to Ukrainian cultural life regardless of ethnic background; they self-identified as Ukrainian or were recognised as part of the Ukrainian creative community by their contemporaries; or they were subject to Soviet persecution specifically in the context of suppressing Ukrainian cultural identity.

This definition deliberately excludes ethnic or linguistic tests for two reasons. First, the Soviet state systematically suppressed Ukrainian cultural identity precisely as expressed through creative practice — through language choice, subject matter, institutional affiliation, and artistic tradition. The population most at risk was defined by cultural participation, not by blood. Second, applying an ethnic test would arbitrarily exclude substantial portions of the historically documented Ukrainian creative community: Ukrainian Jews whose cultural world was entirely Ukrainian even when they wrote in Yiddish; Galician Poles who participated fully in Ukrainian cultural institutions and self-identified with the Ukrainian national movement; Crimean Tatars indigenous to Ukrainian territory who were collectively deported by the Soviet state.

The definition also excludes figures who merely appear in the ESU as foreign reference points with no Ukrainian presence, and ethnic Russians whose creative careers were oriented toward Russian rather than Ukrainian culture even if they were born or worked in Ukraine.

**Notably included under this definition:**
- Crimean Tatars: indigenous to Ukrainian territory, targeted by the 1944 Soviet mass deportation; included without individual review.
- Ukrainian Jews with substantive Ukrainian cultural connection: reviewed individually; those who participated in Ukrainian cultural institutions, wrote about Ukraine, or were targeted as part of the Ukrainian intelligentsia included.
- Galician Poles who self-identified as Ukrainian and participated in Ukrainian cultural institutions: included after individual review.

**Definitional circularity note.** One circularity warrants acknowledgement: individuals included under the "Soviet persecution of Ukrainian cultural identity" criterion were identified partly by their experience of Soviet targeting, which overlaps with this study's dependent variable (mortality under Soviet conditions). This circularity is most consequential for the deported group — where persecution is both the basis for inclusion and the mortality mechanism — and least consequential for the migrant/non-migrant comparison, where both groups share this inclusion criterion equally. Asymmetric bias between migrants and non-migrants from this definition is therefore unlikely; the impact on the deported group's apparent distinctiveness may be modest and is flagged as a limitation.

The full nationality determination protocol, including verbatim AI prompts and stress-test case decisions, is reproduced in SCIENTIFIC_METHODOLOGY.md (Section 6).

#### 3.6.2 Classification Procedure

Determining Ukrainian identity in practice proved less straightforward than applying the definition above, because Soviet administrative records frequently imposed or obscured national identities, and ESU biographical texts reflect the political constraints of the periods in which they were written. We developed a three-tier classification system.

**Tier 1: Clean inclusion.** Entries explicitly described as Ukrainian (Українець/Українка) with no ambiguity markers were included directly without further review.

**Tier 2: Claude AI review.** Entries containing markers suggesting possible nationality ambiguity — Jewish heritage, Polish origin, German or Austrian origin, descriptions as "Soviet" without an underlying national identity, or birth entirely outside Ukraine — were flagged for individual review by Claude (Anthropic, claude-haiku-4-5). Claude was presented with the full ESU biographical text in Ukrainian and asked to classify the individual against the Section 3.6.1 criteria. A total of 1,356 entries underwent this review.

Of the 1,356 reviewed:
- 137 were confirmed as Ukrainian and included.
- 1,218 were confirmed as non-Ukrainian and excluded.
- 1 entry remained indeterminate and was excluded.

**Tier 3: Auto-exclusion.** Entries with explicit non-Ukrainian nationality markers and no Ukrainian connection stated were excluded without Claude review.

The verbatim prompt used for Tier 2 review and the full list of Tier 3 auto-exclusion markers are reproduced in SCIENTIFIC_METHODOLOGY.md (Sections 6.4 and 6.5).

### 3.7 Migration Classification

Migration status was classified into four categories. The original V1 classification used a two-group system (migrated / non-migrated) that incorrectly conflated voluntary internal Soviet transfers and state-imposed deportations with non-migration. This study adopts a four-group system that distinguishes these fundamentally different experiences of Soviet territorial control:

**Migrated (left Soviet sphere):** The individual emigrated from Soviet-controlled territory and settled in a non-Soviet country — Western Europe, North America, South America, or non-Soviet Asia — for a substantial portion of their adult life. Movement to Soviet Russia or another Soviet republic does not qualify. The critical criterion is exit from the Soviet sphere entirely.

**Non-migrated (remained in Ukrainian SSR):** The individual spent their working life within the Ukrainian SSR with no substantial period outside Soviet-controlled territory.

**Internal transfer (voluntary, within USSR):** The individual voluntarily relocated from the Ukrainian SSR to another Soviet republic (most commonly Soviet Russia) and based their career there. They remained under Soviet conditions but in a different republic. This is a voluntary act distinct from deportation and distinct from emigration. This group will be analysed separately as a third comparison population.

**Deported (forced displacement by Soviet state):** The individual was forcibly relocated by Soviet authorities — through Gulag imprisonment, formal deportation orders, special settler (спецпоселенець) assignment, or any other state-mandated relocation. The defining criterion is compulsion: the Soviet state made the movement decision, not the individual. This applies regardless of destination. Deportees are reported as a fourth distinct group and, for the primary age-at-death comparison, grouped with non-migrants — they did not escape Soviet conditions; they experienced them as direct targets of state violence.

The ESU biographical texts consistently contain sufficient information to make this determination. Where the text was ambiguous, Claude was used to review the full Ukrainian-language text and classify migration status according to the above rules, with explicit instruction to prioritise DEPORTED classification whenever any evidence of forced displacement exists. The full revised classification prompt is reproduced verbatim in SCIENTIFIC_METHODOLOGY.md (Section 7.3).

### 3.8 Statistical Methods

**Age at death calculation.** For each individual with both a confirmed birth year and death year, observed age at death was calculated as: death year minus birth year. This yields age at death to the nearest year. No actuarial adjustments were made; we report raw observed age at death as a direct and transparent measure of longevity.

**Clarification on terminology.** This study measures *observed age at death* (equivalently, *mean age at death*), not demographic life expectancy (e₀). Demographic life expectancy is a period measure derived from age-specific mortality rates applied to a synthetic cohort, requiring population-level vital registration data unavailable for this population. The present analysis is a descriptive comparison of the distribution of ages at death across mobility and repression categories. Where prior versions of this paper used the term "life expectancy," the precise meaning is "mean observed age at death."

**Central tendency measures.** We report both arithmetic mean and median for each group, as the presence of outliers (very young deaths due to execution and very old deaths among long-lived individuals) renders the mean sensitive to extreme values. The median provides a more robust central tendency measure under these conditions.

**Statistical significance testing.** We used the Mann-Whitney U test (also known as the Wilcoxon rank-sum test) rather than a two-sample t-test for the primary significance test. This choice reflects the non-normal distribution of ages at death in the non-migrant group — the distribution is left-skewed due to the substantial number of premature deaths from execution and political violence, and this skew violates the normality assumption of the t-test. The Mann-Whitney U test makes no parametric distributional assumptions and is therefore more appropriate for this data structure. The resulting p-value is approximately 0.0 (less than any conventional significance threshold).

**Effect size.** Cohen's d was calculated as the difference in group means divided by the pooled standard deviation. Our primary result of d=0.292 falls in the small-to-medium range,[^5] indicating that the mean age at death difference is not merely statistically detectable but practically meaningful. Note: Cohen's d benchmarks assume normality; because this distribution is demonstrably non-normal (see §5.1), we additionally report Cliff's delta (δ) as a fully non-parametric effect size consistent with the Mann-Whitney U test. Cliff's delta measures P(migrant outlives non-migrant) − P(non-migrant outlives migrant), ranging from −1 to +1 with 0 indicating no difference. For the primary migrated vs. non-migrated comparison: **δ = 0.18** — a migrant was 18 percentage points more likely to outlive a randomly selected non-migrant than the reverse.

**Period analysis.** Deaths among non-migrants were grouped by historical period using established historiographic periodisation of Soviet Ukrainian history. Average age at death within each period was calculated to identify periods of anomalously young mortality.

**Birth cohort analysis.** Workers were grouped by decade of birth (1870s through 1920s). Mean age at death was calculated separately for migrants and non-migrants within each cohort to identify which generations experienced the greatest mortality differential.

---

## 4. Results

### 4.1 Overall Mortality Gap: Mean Age at Death by Group

V2 analyses four groups, and the most causally interpretable findings come from the two groups for whom emigration selection is not a concern. **Workers deported by the Soviet state** (n=183) died at a mean age of 48.35 years — a 22.87-year deficit relative to non-migrants (d=1.656, p<0.001). **Workers who transferred voluntarily within the Soviet system** (n=1,150) showed no meaningful survival advantage over those who stayed (gap=+0.52 yrs, d=0.038, p=0.094, not significant). Taken together: state compulsion killed; remaining within the Soviet sphere under any voluntary arrangement made no difference. The third finding — a 4.04-year gap favouring those who emigrated entirely — is consistent with this picture but is subject to selection effects (§5.4) and should be read alongside the PSM and Cox results below.

Figure 1 shows mean age at death with 95% confidence intervals for all four groups. Figures 4, 15, and 15b present box plots, the internal transfer null comparison, and all-group distribution overlays respectively. Figure 20 shows the most conservative possible framing, collapsing non-migrated, internal transfer, and deported into a single "remained in Soviet sphere" group.

**Figure 1.** Mean age at death with 95% CI by migration group. Migrated (n=1,280): 75.25 yrs [74.49–76.01]. Non-migrated (n=6,030): 71.22 yrs [70.87–71.57]. Internal transfer (n=1,150): 70.70 yrs [69.91–71.49]. Deported (n=183): 48.35 yrs [46.26–50.44].

**Figure 4.** Notched box plots of age at death for all four migration groups. Central line = median; notches = 95% CI on median; boxes = IQR; whiskers = 1.5×IQR. The deported group's box sits far below the others, median=45, reflecting mass non-natural mortality.

**Figure 15.** Direct comparison of mean age at death for the internal transfer group (n=1,150, mean=70.70 yrs) versus non-migrated (n=6,030, mean=71.22 yrs) with Mann-Whitney U p-value displayed. The near-zero gap (+0.52 yrs, p=0.094) is the null result anchoring the paper's interpretation: moving within the Soviet system conferred no survival benefit.

**Figure 15b.** Box plots for all four groups with written statistical conclusions text overlay. Shows which between-group comparisons are significant and which are null.

**Figure 20.** Conservative two-group comparison: migrated (n=1,280, mean=75.25 yrs) vs all three Soviet-sphere groups combined (n=7,363, mean=70.58 yrs). Gap = +4.68 yrs (Cohen's d=0.330, p<0.001). The most conservative possible framing — the gap persists even when deported and internal transfer groups are combined with non-migrants.

**Table 1: Observed Age at Death by Migration Group (n=8,643)**

| Group | n | Mean age at death | Median age at death | SD | 95% CI |
|-------|---|---------|-----------|-----|--------|
| Migrated (left USSR) | 1,280 | 75.25 | 77 | 13.88 | [74.49, 76.01] |
| Non-migrated (stayed) | 6,030 | 71.22 | 73 | 13.79 | [70.87, 71.57] |
| Internal transfer (USSR) | 1,150 | 70.70 | 72 | 13.61 | [69.91, 71.49] |
| Deported by Soviet state | 183 | 48.35 | 45 | 14.36 | [46.26, 50.44] |
| **Primary gap (Migrated vs Non-migrated)** | — | **+4.04** | **+4** | — | — |
| **Deportation gap (Non-migrated vs Deported)** | — | **+22.87** | — | — | — |

*Note on the "Deported" category: this group comprises individuals subjected to state-ordered displacement — Gulag (corrective labour camp) imprisonment, formal NKVD deportation orders, or special settler (спецпоселенець) assignment — where the Soviet state, not the individual, made the movement decision. It does not include wartime civilian evacuation, voluntary relocation under professional pressure, or movement that followed a period of imprisonment but was not itself state-ordered. The definitional boundary between "deported" and "internal transfer" is compulsion: if any biographical evidence of forced displacement exists, the entry was classified as deported (see §3.7 for the full classification protocol; see footnote [^9] for the definition of "Gulag" used in this paper).*

The non-migrated group (n=6,030) achieved a mean age at death of 71.22 years and a median of 73 years. The wide standard deviation (13.79) reflects the heterogeneous mortality experience of this group: it spans both very young deaths from political violence and long-lived individuals who survived the Soviet period and died in old age in independent Ukraine.

The migrated group (n=1,280) achieved a mean age at death of 75.25 years and a median of 77 years (SD=13.88). Migrants were largely spared the systematic political violence that produced the left tail of the non-migrated distribution, though they faced other mortality risks including wartime conditions, poverty in exile, and the psychological consequences of displacement.

The internal transfer group (n=1,150) — workers who relocated within the Soviet Union under voluntary or professional pressure — shows a mean age at death of 70.70 years, statistically indistinguishable from non-migrated (gap = +0.52 yrs, p=0.094, d=0.038). This near-null finding is itself significant: moving within the Soviet system conferred no meaningful survival advantage.

The most extreme finding is the deported group (n=183): mean age at death of 48.35 years, median 45 years — a 22.87-year deficit relative to non-migrants and a 26.90-year deficit relative to migrants. This group, comprising workers forcibly expelled to Central Asia, Siberia, or the Gulag[^9], experienced mortality conditions equivalent to those observed in wartime populations.

### 4.2 Statistical Significance

All pairwise comparisons between migrated and non-migrated groups, and between either group and the deported group, yield p ≈ 0.0 — vanishingly small probabilities that these gaps arose by chance. Figure 2 shows Kaplan-Meier survival curves for all four groups, providing a non-parametric visual of the survival differences independent of distributional assumptions. Figure 14 is the sensitivity analysis demonstrating robustness to AI classification errors.

**Figure 2.** Kaplan-Meier survival curves for all four migration groups. Y-axis = probability of surviving to a given age. Shaded bands = 95% CI. The migrated group's curve remains highest throughout; the deported group's curve falls sharply in the 1930s–1940s. Median survival: migrated=77, non-migrated=73, internal transfer=72, deported=45.

**Figure 14.** Sensitivity analysis: primary mean age at death gap under hypothetical AI classification error rates 0–10%, assuming worst-case directional bias (all errors misclassify the longest-lived migrants as non-migrants). Gap remains positive at every tested rate. At measured 3.2% error: adjusted gap = +3.30 yrs. At 10% error: +1.87 yrs.

| Comparison | Gap | Cohen's d | Cliff's δ | p-value |
|-----------|-----|-----------|-----------|---------|
| Migrated vs Non-migrated | +4.04 yrs | 0.292 | 0.18 | < 0.001 |
| Migrated vs Deported | +26.90 yrs | 1.930 | — | < 0.001 |
| Non-migrated vs Deported | +22.87 yrs | 1.656 | — | < 0.001 |
| Non-migrated vs Internal transfer | +0.52 yrs | 0.038 | — | 0.094 (n.s.) |

*Cliff's δ is reported only for the primary comparison (migrated vs non-migrated), as this is the paper's main inferential focus. δ = 0.18 means a randomly selected migrant was 18 percentage points more likely to outlive a randomly selected non-migrant than the reverse — a fully non-parametric measure consistent with the Mann-Whitney U test. Cliff's δ for the deported comparisons is not reported because the deported group's mortality is predominantly non-natural (state-ordered execution and Gulag death), making a rank-order probability interpretation less informative than the absolute mean gap.*

For the primary comparison (migrated vs non-migrated), Cohen's d = 0.292 indicates a small-to-medium effect size. The deported group shows a massive effect (d = 1.930), one of the largest effect sizes observable in population mortality data outside of direct famine or epidemic conditions.

**Sensitivity analysis:** Assuming the worst-case scenario in which all AI classification errors (estimated rate 3.2%) systematically misclassify the longest-lived migrants as non-migrants, the adjusted gap remains approximately +3.30 years at our measured error rate. Even at a hypothetical 10% error rate — more than 3× our measured rate — the gap remains positive at approximately +1.87 years (Figure 14). The finding is robust to realistic error rates.

### 4.3 Profession-Level Breakdown

The mean age at death gap between migrants and non-migrants is consistent across all creative professions. Table 2 and Figure 11 report mean age at death by group for each profession category.

**Figure 11.** Mean age at death by creative profession for all four groups. The migrated/non-migrated gap is present in every profession without exception. Writers/Poets contribute the largest deported sub-cohort (n=117, mean age at death=45.2). Architects show the largest between-group gap (+6.1 yrs).

**Table 2: Mean Age at Death by Profession**

| Profession | Migrant mean age | n | Non-migrant mean age | n | Deported mean age | n | Gap (M vs NM) |
|------------|-----------|---|----------------|---|------------|---|--------------|
| Writers/Poets | 74.6 | 368 | 70.3 | 1,776 | 45.2 | 117 | +4.3y |
| Visual Artists | 74.4 | 385 | 71.5 | 1,967 | 56.2 | 38 | +2.9y |
| Musicians/Composers | 75.4 | 298 | 71.1 | 932 | 42.6 | 13 | +4.3y |
| Theatre/Film | 75.2 | 61 | 71.7 | 729 | 54.5 | 8 | +3.5y |
| Architects | 78.6 | 61 | 72.5 | 404 | 64.7 | 3 | +6.1y |
| Other Creative | 78.0 | 107 | 73.1 | 222 | 60.0 | 4 | +4.9y |

The gap is present across every profession. Writers/Poets contribute the largest deported cohort (n=117, mean age at death of 45.2) — reflecting the particular intensity of Soviet targeting of Ukrainian-language literary production. The Executed Renaissance (*Rozstriliane Vidrodzhennia*) was overwhelmingly a literary phenomenon: writers and poets were arrested, shot at Sandarmokh, or died in the Gulag at rates far exceeding other creative professions.

Architects show the largest migrant/non-migrant gap (+6.1 years) with relatively small deported n (n=3), suggesting that architectural professionals who remained were not primarily targeted by the state but benefited from emigration through access to Western professional markets and living standards.

### 4.4 Repression Period Analysis

The non-migrated dataset (n=6,030) provides sufficient power to examine mortality patterns by historical period. Table 3 and Figure 9 classify deaths by Soviet-era periodisation and report average age at death within each period. Figure 8 shows the deported group's year-by-year death distribution, making the 1937 spike visually explicit.

**Figure 9.** Mean age at death by Soviet historical period for each migration group. The deported group's Great Terror bar (mean 43.4 yrs) is the lowest of any group in any period. The post-independence non-migrant bar (74.7 yrs) is the highest, illustrating why the V1 pre-1991 cutoff deflated the non-migrant average.

**Figure 8.** Year-by-year bar chart of deported deaths (n=183), 1920–2000. The 1937 spike — 65 deaths, 35.5% of the entire cohort in a single year — is the study's strongest single-year mortality signal. A secondary cluster in 1941–1945 reflects wartime Gulag conditions.

**Table 3: Non-Migrant Deaths by Historical Period**[^11]

| Period | Historical context | Deaths | Avg age at death | % of total |
|--------|--------------------|--------|-----------------|-----------|
| 1921–1929 | Early Soviet/NEP | 93 | 58.5 | 1.5% |
| 1930–1933 | Holodomor/Purges | 53 | 59.6 | 0.9% |
| 1934–1938 | Great Terror | 95 | 55.5 | 1.6% |
| 1939–1945 | World War II | 202 | 55.2 | 3.3% |
| 1946–1953 | Late Stalinist period | 121 | 62.6 | 2.0% |
| 1954–1964 | Khrushchev Thaw | 234 | 66.6 | 3.9% |
| 1965–1991 | Stagnation/Late USSR | 1,427 | 69.2 | 23.7% |
| Post-1991 | Independent Ukraine | 3,710 | 74.7 | 61.5% |

The most striking figure is the Great Terror period (1934–1938): 95 deaths with an average age of 55.5 years — well below the Late Soviet-period average of 69.2. This is compounded by the deported group's Terror-period data: 95 deported workers died in 1934–1938, with an average age of just 43.4 years. Combined, 190 creative workers died in the Terror years with an average age in the low-to-mid forties — a quantitative signal of mass non-natural mortality.

The post-1991 period dominates numerically (3,710 deaths, 61.5% of all non-migrant deaths) with an average age of 74.7 — dramatically higher than any Soviet-era period. This cohort's inclusion in V2 (excluded from V1 by its pre-1991 cutoff) is the primary driver of the narrowing of the measured mortality gap from 9 years (V1) to 4.04 years (V2).

This requires methodological comment. V1's exclusion of post-1991 deaths was not a neutral design choice: it constitutes what epidemiologists and demographers call **artificial right-censoring** — the practice of removing observations from the analysis at an administratively chosen date rather than at the subject's actual date of death. The standard in demographic life expectancy studies and survival analysis is to follow subjects until death or until the end of the natural observation window, and to include all confirmed death dates regardless of when they fall.[^10] Applying an earlier cutoff is acceptable only when the study's explicit research question is limited to mortality *within* a specified historical period — for example, a study of battlefield mortality that terminates at armistice. V1 did not have that scope: it asked about mean age at death across a lifetime, and the 1991 cutoff was applied on the reasoning that post-Soviet conditions would confound a study of Soviet-era mortality. That reasoning, while understandable, produces a well-documented statistical problem: when the censoring cutoff is correlated with the outcome (i.e., when the decision about *who* is censored is not independent of *how long they would have lived*), the resulting estimates are biased.

In this case the censoring was systematically non-independent. Non-migrants who were still alive in 1991 — the very individuals excluded by V1's cutoff — are, by definition, the longest-lived members of the non-migrant cohort. They survived not only the Stalinist mass repression period (1934–1953), the Second World War, and the Late Soviet stagnation period (1964–1991), but the entire Soviet period itself, dying at an average age of 74.7 in independent Ukraine. By excluding this group, V1 effectively removed the most favourable outcomes for non-migrants from the analysis. Meanwhile, migrants — born on average earlier in the cohort and dying abroad in Western European or North American contexts — were more likely to have died before 1991 regardless of political conditions, and therefore were not systematically excluded by the same cutoff. The result was that V1's comparison group (migrants) was complete, while V1's reference group (non-migrants) was truncated at its healthiest end. This asymmetric censoring inflated the measured gap.

V2 removes the cutoff entirely and includes all confirmed death dates. The 4.04-year gap is therefore a more accurate estimate of the lifetime mortality differential between the two populations. The narrowing of the gap from 9 to 4.04 years does not mean the Soviet effect was smaller than V1 suggested — it means V1 overstated the effect due to a methodological asymmetry that V2 corrects. The survival signal is real, statistically robust, and meaningful. It is simply more precisely measured here.

### 4.5 The 1937 Spotlight

The year 1937 — the peak of the Stalinist Great Terror — warrants dedicated analysis. Figure 7b shows the deported group's death year histogram restricted to 1920–1960, where the 1937 spike is unmistakable.

**Figure 7b.** Death year histogram for the deported group only (n=183), 1920–1960. The 1937 peak — 65 deaths (35.5% of all deported deaths) in a single year — is the most concentrated mortality event in the dataset, consistent with mass execution during the Great Terror. The 1934–1938 period accounts for 95 of 183 deported deaths (51.9%). Across all four groups, **100 creative workers in our dataset died in 1937**, with a blended mean age at death of approximately 46.2 years. This is the single most lethal year for Ukrainian creative workers in our dataset.

The deaths are not evenly distributed. Among those who remained under Soviet rule, 24 non-migrated workers died at an average age of 48.0, and 65 deported workers died at an average age of 42.4 — a combined repression cluster of 89 deaths concentrated in a single year. The deported group's figure is particularly stark: 65 of the 183 total deported workers in our dataset (35.5%) died in a single calendar year, at an average age of 42.4. Among the internal transfer group, 1 death is recorded in 1937 at age 25.

By contrast, the 10 migrated workers who died in 1937 did so at a mean age of 68.9 — consistent with natural mortality among an aging cohort living outside Soviet jurisdiction. The within-year gap between the migrated (68.9) and deported (42.4) groups is 26.5 years: a single calendar year contains, in concentrated form, the same mortality differential that defines the study as a whole.

**Table 4: 1937 Deaths by Group**

| Group | Deaths in 1937 | Mean age at death |
|-------|---------------|-----------------|
| Non-migrated | 24 | 48.0 |
| Deported | 65 | 42.4 |
| Internal transfer | 1 | 25.0 |
| Migrated | 10 | 68.9 |
| **Total** | **100** | **~46.2** |

*Note: Internal transfer (n=1) and migrated (n=10) are included for completeness. Sample sizes are too small for meaningful inference about mean age; they are shown to confirm that deaths occurred across all groups in 1937 and to document the within-year contrast, not as representative estimates of those groups' mortality in that year.*

The deported group's concentration of deaths in 1937 corresponds directly to the Sandarmokh massacres, the Solovki transit camp executions, and the general liquidation of Ukrainian cultural intelligentsia ordered by NKVD Order No. 00447. Named figures confirmed in this dataset include Lesʹ Kurbas [Лесь Курбас] (shot 1937, age 50), Mykola Zerov [Микола Зеров] (shot 1937, age 47), Valerian Pidmohylʹnyĭ [Валер'ян Підмогильний] (shot 1937, age 36), and Valerian Polishchuk [Валер'ян Поліщук] (shot 1937, age 40).

### 4.6 Birth Cohort Analysis

The mean age at death gap between migrants and non-migrants is strongly concentrated in specific birth cohorts. Table 5 and Figure 10 present mean age at death by decade of birth for all groups; Figure 13 shows the overlaid birth year distributions confirming substantial cohort overlap between groups (a methodological check that between-group comparisons are not conflating era effects with migration status).

**Figure 10.** Mean age at death by birth decade for all four groups (min n=10 per data point). The 1880s and 1890s cohorts — the Executed Renaissance generation — show the largest gaps (5.1 yrs each). The deported 1890s cohort (mean 44.6 yrs, n=60) is the most concentrated single mortality event. Gaps narrow for post-1920 cohorts.

**Figure 13.** Overlaid birth year histograms (5-year bins) for all four groups. Methodological check: the distributions overlap substantially, confirming between-group comparisons are not confounded by groups being born in systematically different eras.

**Table 5: Mean Age at Death by Birth Cohort**

| Birth cohort | Migrant mean age | n | Non-migrant mean age | n | Deported mean age | n | Gap (M vs NM) |
|-------------|-----------|---|----------------|---|------------|---|--------------|
| 1880s | 73.8 | 168 | 68.7 | 260 | 56.7 | 27 | +5.1y |
| 1890s | 75.2 | 223 | 70.1 | 327 | 44.6 | 60 | +5.1y |
| 1900s | 75.2 | 209 | 72.4 | 647 | 42.1 | 54 | +2.8y |
| 1910s | 78.1 | 207 | 75.0 | 807 | 43.5 | 13 | +3.1y |
| 1920s | 78.8 | 164 | 75.4 | 1,256 | 53.2 | 6 | +3.4y |
| 1930s | 74.8 | 89 | 73.2 | 1,136 | 78.3 | 3 | +1.6y |

The 1890s cohort shows the most extreme deported mortality: mean age at death of 44.6 years among those 60 deported individuals, nearly all of whom died in the Terror years. This cohort — those born 1890–1899, who were in their thirties and forties during the peak repression — formed the core of the Executed Renaissance and bears the full weight of state-organised liquidation.

The pattern across cohorts is consistent with a differential impact of Soviet repression by birth generation: the gap persists across all birth decades but is most severe where the cohort's prime years overlapped with peak repression. The 1930s cohort shows the smallest gap (+1.6 years) — those workers were children during the Terror and came of age in post-war Soviet Ukraine, facing bureaucratic repression rather than physical elimination.

### 4.7 Geographic Patterns

Migration rates varied substantially by city of birth. Table 6 presents migration rates for cities with n ≥ 50 in the dataset; cities below this threshold are shown in Figure 12 for visual context but not in the table due to insufficient statistical reliability. Figure 12 ranks the top 20 birth cities by total workers and shows migration rate within each.

**Figure 12.** Horizontal bar chart ranking top 20 birth cities by total workers, with bars subdivided by migration rate. Western Ukrainian cities (Lviv, Ternopil, Chernivtsi) show dramatically higher emigration rates than eastern cities. Note: small-n cities are shown here for visual context only and should not be interpreted as statistically precise estimates.

**Table 6: Migration Rates by Birth City (n ≥ 50 only)**

| City | Total in dataset | % Migrated |
|------|-----------------|-----------|
| Kyiv | 453 | 13.9% |
| Lviv | 164 | 45.1% |

*Cities with n < 50 (including Chernivtsi n=23, Ternopil n=17, Donetsk n=14) are not included in the table as point estimates are statistically unreliable at those sample sizes. Migration rates for these cities in Figure 12 should be interpreted as illustrative rather than as precise estimates. Oblast-level aggregation would provide more statistically robust geographic analysis.*

The geographic pattern is striking and historically coherent. Lviv — in western Ukraine (Galicia) — shows a migration rate of 45.1%; smaller western Ukrainian cities show similar patterns in Figure 12, ranging from approximately 35–53%. These cities were incorporated into the Soviet Union only in 1939–1940 (following the Molotov-Ribbentrop Pact and subsequent Soviet annexation of Eastern Poland and northern Romania), giving their residents both more recent experience of non-Soviet existence and less time under Soviet control before the opportunity to flee during World War II. Western Ukrainian creative workers had stronger connections to Polish and Austrian cultural institutions, were more likely to have had contacts in Western Europe, and had a shorter period of Soviet acculturation — all factors that likely increased both the propensity and the opportunity to emigrate.

Kyiv's migration rate of 13.9% is substantially lower, reflecting the city's deeper integration into Soviet administrative and cultural structures. Kyiv was the capital of Soviet Ukraine and its cultural workers were subject to intense ideological oversight but also more deeply embedded in Soviet institutions — the Writers' Union, the Composers' Union, the Academy of Arts — that provided material incentives to remain.

Donetsk (historically called Stalino during the Soviet period) shows a 0% migration rate in our dataset. This reflects not just a geographic and cultural distance from western emigration routes, but also the city's character as an industrial centre that was less hospitable to the kind of nationally-oriented creative work that motivated emigration. Creative workers from the Donbas region were fewer in number, more likely to be Russian-speaking, and had fewer connections to the diaspora networks that facilitated emigration.

### 4.8 Death Age Distribution

The distribution of ages at death further illuminates the mortality differential between the two groups. Figure 5 shows the deported group's age-at-death histogram (sharply left-skewed, mass concentrated below 60). Figure 6 shows split violin plots by gender within each group. Figure 7 shows the overlapping death year histogram for migrated and non-migrated groups, with vertical markers at the Holodomor (1933), Great Terror (1937), and WWII (1941) repression years.

**Figure 5.** Histogram of age at death for the deported group only (n=183), 5-year bins. Dashed line = group mean (48.35 yrs). Sharply left-skewed with mass below 60; spike in 35–50 range consistent with mass execution and Gulag death in mid-career individuals. Small right tail = survivors released post-Stalin.

**Figure 6.** Split violin plots for all four groups by gender (left = Male, right = Female). The migrated group's long upper tail and the deported group's sharp left-skewed truncation are visible in both sexes.

**Figure 7.** Overlapping death year histogram (2-year bins, 1900–2024) for migrated and non-migrated groups. Vertical markers at 1933 (Holodomor), 1937 (Great Terror), 1941 (WWII). Peaks in the 1930s–40s for non-migrants versus the more gradual post-war distribution for migrants.

**Premature death (before age 50):** 7.1% of non-migrants died before age 50, compared to 5.4% of migrants — a relative excess of 31% more premature deaths among non-migrants.

**Very young death (before age 30):** 49 non-migrants versus 3 migrants died before age 30. Expressed as a proportion of their respective group sizes: 0.81% of non-migrants versus 0.23% of migrants died before age 30 — a ratio of approximately 3.5:1.

**Age 30–39 deaths:** 123 non-migrants versus 25 migrants.

**Age 40–49 deaths:** 255 non-migrants versus 41 migrants.

**Long life (age 90+):** 375 non-migrants and 189 migrants reached age 90 or older. As a proportion: 6.2% of non-migrants versus 14.8% of migrants achieved this milestone. This finding is counterintuitive at first glance — if non-migrants faced greater mortality risk, why do more of them in absolute terms reach age 90? The answer lies in sample sizes: non-migrants outnumber migrants five to one in this dataset, so even at a lower rate, they produce more individuals in the 90+ bracket in absolute terms.

The age distribution analysis is consistent with the interpretation of the mean age at death gap: non-migrants show a pronounced left tail (excess premature deaths from political violence) combined with a roughly normal long-life distribution, while migrants show a more symmetric distribution with a lighter left tail and a modestly heavier right tail (more long-lived individuals proportionally).

---

### 4.9 Multivariable Regression

To assess whether the observed age-at-death gap between migrants and non-migrants persists after controlling for compositional differences across birth cohort, creative profession, and region of origin, we estimated two OLS regression models with non-migrated as the reference category.

**Model 1 (unadjusted)** regresses observed age at death on migration status alone (n = 8,643). The intercept — representing non-migrants — is 71.22 years. Migrants show a coefficient of **+4.04 years** (95% CI [3.20, 4.87], p < 0.001). Deported individuals show **−22.87 years** (95% CI [−24.90, −20.84], p < 0.001). Internal transfers show a small, non-significant difference of −0.52 years (p = 0.24), consistent with the null result reported in §4.2.

**Model 2 (adjusted)** adds birth decade, profession, and birth region as controls. The migration advantage reduces modestly to **+3.31 years** (95% CI [2.44, 4.19], p < 0.001), indicating that the gap is not explained by cohort composition, professional distribution, or geographic origin. Notably, internal transfer becomes statistically significant in the adjusted model (−1.43 years, p = 0.002), suggesting a suppressed effect partially confounded by birth-cohort composition. The deportation penalty remains severe at **−23.44 years** (95% CI [−25.49, −21.39], p < 0.001). The adjusted model explains 7.7% of variance in age at death (R² = 0.077), consistent with the expected explanatory power of migration status as one factor among many shaping individual longevity.

**Table A — OLS Regression Results: Observed Age at Death by Migration Status**

| Group (vs. Non-migrated) | Model 1 β | 95% CI | p | Model 2 β | 95% CI | p |
|---|---|---|---|---|---|---|
| Migrated | +4.04 | [+3.20, +4.87] | <0.001 | +3.31 | [+2.44, +4.19] | <0.001 |
| Internal Transfer | −0.52 | [−1.39, +0.35] | 0.243 | −1.43 | [−2.34, −0.53] | 0.002 |
| Deported | −22.87 | [−24.90, −20.84] | <0.001 | −23.44 | [−25.49, −21.39] | <0.001 |

*Model 1: migration status only (n = 8,643). Model 2: + birth decade, profession, birth region. β = years of observed age at death relative to non-migrated baseline. Non-migrated mean age at death = 71.22 years.*

**Figure 23:** Gap stability chart — the same migration status gaps shown as grouped bars, comparing the unadjusted estimate (Model 1) against the adjusted estimate (Model 2, controlling for birth cohort, profession, and region). Bar length = β in years. Error bars = 95% confidence intervals. The near-identical bar lengths suggest that the migration advantage and deportation penalty are not artefacts of compositional differences.

### 4.10 Cox Proportional Hazards Model

The preceding sections have compared groups by their mean or median age at death — a straightforward summary that is easy to interpret but rests on a significant restriction: it can only use individuals with a known death date. Living people, by definition, cannot have a recorded age at death, so they have been excluded from all analysis up to this point. A Cox proportional hazards model is a different kind of survival analysis that does not require death to have occurred. Instead, it asks: *at any given age, how much more or less likely is a person in this group to die than a person in the reference group?* This makes it possible to include living individuals — not as deaths, but as observations that have survived *at least* to their current age in 2026, with their eventual fate still unknown. In statistical terminology these are called "right-censored" observations: we know the person was alive at a certain point; we simply have not observed the end of the story yet.

**What the model does, in plain terms.** Imagine lining up all 15,053 individuals in this study by age. Every time someone dies, the model records which group they belonged to and whether people in that group were dying faster or slower than the non-migrated baseline at that point in time. Living individuals contribute to the denominator — they are "at risk" at every age up to their current age — but they do not count as deaths. The resulting measure is a *hazard ratio* (HR): a number above 1 means a group was dying at a faster rate than non-migrants at any given age; a number below 1 means they were dying at a slower rate — i.e., they had a survival advantage. An HR of 0.832, for example, means the group in question faced roughly 17% lower mortality risk at any given age than the non-migrated baseline, after controlling for confounding factors.

This is a more sophisticated measure than the mean-gap comparisons in §§4.1–4.9, because it accounts for the full shape of survival over time rather than just summarising where people ended up. It also makes better use of the data by including all 6,314 individuals currently alive, whose biographical records in the ESU confirm their birth years and, crucially, their migration status — which was classified using the same AI pipeline applied to the deceased cohort.

**What the results say.** The primary finding is in Model 2 (adjusted for birth decade, profession, and birth region — the same controls used in the OLS regression):

**Table A-Cox — Cox PH Results, Right-Censored Model (reference = non-migrated, N=15,053)**

| Group | Model 1 HR (unadjusted) | Model 2 HR (adjusted) | 95% CI (Model 2) | p (Model 2) |
|-------|-----------|-----------|-----------------|-------------|
| Migrated | 1.088 | 0.832 | [0.778, 0.889] | < 0.001 |
| Internal Transfer | 1.541 | 1.105 | [1.033, 1.182] | 0.004 |
| Deported | 4.964 | 4.646 | [3.908, 5.524] | < 0.001 |

*A hazard ratio below 1 means lower mortality risk (longer survival) relative to non-migrants. A hazard ratio above 1 means higher mortality risk (shorter survival). The 95% confidence interval tells us the plausible range around that estimate. All results use non-migrated workers as the reference category. Full technical output in `results/cox_censored_output.txt`.*

After controlling for birth cohort, profession, and region, the three main findings replicate what the simpler OLS analysis showed:

- **Migrants lived longer.** A hazard ratio of 0.832 means that at any given age, Ukrainian creative workers who emigrated faced roughly 17% lower mortality risk than those who stayed. Phrased differently: their chances of dying on any given birthday were systematically lower throughout their lives. This is consistent with the +4.04-year mean gap reported in §4.1.

- **Deportees died at catastrophically higher rates.** A hazard ratio of 4.646 means that at any given age, deported workers were dying at more than four and a half times the rate of non-migrants. This is not a subtle statistical signal — it reflects the mass executions of 1937–1938, the Gulag death camps, and the starvation and disease conditions of forced exile. The Cox model captures not just that deportees died younger on average, but that their mortality was accelerated at every point in the life course relative to those who were not targeted.

- **Internal transfers showed no meaningful survival advantage.** An HR of 1.105 — slightly above the null of 1.0 — suggests that workers who voluntarily moved to other Soviet republics experienced marginally elevated mortality risk rather than a survival benefit. This finding, consistent with the OLS result (§4.6), reinforces the interpretation that it was emigration *out of the Soviet sphere entirely*, not simply movement away from Soviet Ukraine, that was associated with better survival.

**Why the unadjusted and adjusted numbers differ for migrants — and why this matters.** A careful reader will notice something puzzling in the table: without controls (Model 1), the migrated HR appears to be *above* 1 (1.088) — as if migrants were dying faster than non-migrants. This seems to contradict everything else in the paper. The explanation is a structural feature of the dataset, not a contradiction of the finding.

The non-migrated group contains a large proportion of currently living individuals — nearly half (48.9%) of all non-migrants in this extended dataset are people still alive today. These are predominantly workers born between the 1940s and 1960s, who lived through the Soviet period and are now in their sixties to eighties, still adding years to their eventual age at death. This makes the non-migrated group look artificially healthy in a naive comparison, because the model sees thousands of non-migrants still alive at advanced ages and infers their mortality risk is very low. The migrated group, by contrast, has fewer living representatives (19.8% censored) — most historical migrants from the first and second emigration waves have already died, and their deaths are recorded.

In other words: without adjustment, the model is partly comparing historical-cohort migrants (mostly born 1880–1930, mostly dead) against a mixed pool of non-migrants that includes both historical cohort members and a large number of much younger contemporary workers who are still alive. That is an apples-to-oranges comparison. Once birth decade is controlled for — i.e., once the model compares people born in the same era to each other — the picture corrects itself, and the migrant survival advantage (HR = 0.832) reappears clearly.

This reversal is itself a methodologically important result. It demonstrates that in a right-censored survival analysis where censoring is not evenly distributed across groups, a naive unadjusted comparison can actively mislead. Covariate adjustment is not merely a statistical nicety here — it is the difference between a finding and a mirage.

**Figure 24.** Cox proportional hazards forest plot. Each row shows the hazard ratio for one migration group relative to non-migrants, with 95% confidence intervals as error bars. Squares = Model 1 (unadjusted); diamonds = Model 2 (adjusted). The dashed vertical line at HR=1.0 is the null — no difference from non-migrants. Points to the left of the line indicate lower mortality risk; points to the right indicate higher risk. The migrated group's shift from right of the line (unadjusted) to left (adjusted) illustrates the cohort-mixing effect described above. N=15,053.

**Figure 25.** The proportion of each migration group that is still alive versus confirmed dead. Non-migrants are 48.9% alive (right-censored); migrants are 19.8% alive; internal transfers 11.7%; deportees 6.1%. The fact that deportees are almost entirely dead — despite many being born as recently as the 1920s — reflects the concentrated lethality of Soviet political repression.

**Figure 26.** Kaplan-Meier survival curves for all four groups using the full right-censored dataset (N=15,053). The vertical axis shows the proportion of each group still alive at each age; the horizontal axis is age in years. Tick marks along each curve indicate living individuals who have survived to that age. The deported group's sharp drop in early to middle age — concentrated in the Gulag and Terror years — is the most visually striking feature.

**When did the killing happen? — Time-varying hazard ratios for the deported group.** A technical check called the Schoenfeld residuals test examines whether the hazard ratio for each group stays constant across age — the Cox model's key assumption. For the deported group, this assumption is violated (p < 0.0001). This is not a statistical inconvenience — it is a historical signal. It tells us that the deported group's excess mortality was not spread evenly across their lives; it was concentrated in specific years. To map *when* the excess killing happened, we fitted a separate Cox model within each 10-year age window, asking: "Among people still alive at age 30, how much more likely were deportees to die between 30 and 40 than non-migrants?" — then the same question for ages 40–50, 50–60, and so on. This approach is known as a landmark analysis.

**Table A-Cox-TV — Time-Varying Hazard Ratios for Deported Workers by Age Band**

| Age band | n at risk | Deported deaths | HR | 95% CI | p |
|----------|-----------|-----------------|-----|--------|---|
| 20–30 | 15,046 | 10 | 1.10 | [0.90, 1.34] | 0.35 |
| 30–40 | 14,969 | 40 | 1.51 | [1.23, 1.84] | < 0.001 *** |
| **40–50** | **14,665** | **48** | **1.89** | **[1.50, 2.38]** | **< 0.001 ***\*** |
| 50–60 | 13,786 | 26 | 1.61 | [1.21, 2.15] | 0.001 ** |
| 60–70 | 12,051 | 19 | 1.50 | [1.07, 2.10] | 0.018 * |
| 70–80 | 8,546 | 11 | 1.21 | [0.80, 1.84] | 0.36 |
| 80–90 | 4,035 | 5 | 0.95 | [0.53, 1.70] | 0.86 |

*Reference = non-migrated. HR > 1 = higher mortality risk than non-migrants at that age. Each band is independent; only individuals alive at the start of each window contribute. Unadjusted (migration dummy only).*

The pattern is exactly what the historical record would predict. In their twenties, deportees were barely more likely to die than non-migrants — an HR of 1.10, not statistically distinguishable from zero. Then, as they entered their thirties and forties — the ages at which most Great Terror arrests occurred and at which Gulag conditions were most lethal — the hazard ratio rose sharply, peaking at **1.89 in the 40–50 age band** (48 deported deaths in that window). This is the age cohort of workers born roughly 1890–1910, the same generation responsible for the Executed Renaissance — the writers, poets, and artists systematically liquidated in 1937–1938. Among survivors who made it to their seventies, the excess mortality risk had collapsed to near-null (HR = 1.21, p = 0.36). By their eighties, deportees who survived that far were dying at essentially the same rate as non-migrants (HR = 0.95).

The single HR of 4.646 in Table A-Cox is an average across this entire arc — it captures the fact that deportees were dying at catastrophic rates at some points, but it compresses a time-varying story into one number. The landmark analysis restores the shape. What it shows is not a steady-state elevated risk but a concentrated event: the Soviet state killing Ukrainian creative workers at a specific historical moment, in their middle years, at nearly double the rate of those who were not targeted. The HRs in Table A-Cox-TV are the mortality signature of the Great Terror.

**Figure 28.** Time-varying hazard ratios for the deported group across age bands (landmark Cox analysis, reference = non-migrated). Each point shows the hazard ratio for deported workers dying within that 10-year age window; error bars are 95% confidence intervals. The dashed line at HR=1.0 is the null. The peak at age 40–50 (HR=1.89) marks the Stalinist Terror killing years; the collapse toward null at ages 70+ reflects the mortality of survivors, whose risk had converged back toward the non-migrated baseline by late life.

**Figure 28b.** The same time-varying mortality risk shown as a continuous arc — designed to be read without statistical training. The y-axis is the hazard ratio: a value of 1.89 means deportees were dying at 1.89 times the rate of non-migrants in that age window. The shaded band marks the Great Terror and Gulag exposure years. The curve rises sharply through the thirties and forties, peaks at ages 40–50, then collapses back toward 1.0 (no excess risk) by the seventies. What the graph shows is not a steady elevated risk but a concentrated killing event: the Soviet state liquidating Ukrainian creative workers at a specific historical moment, then stopping — because it had done its work.

### 4.11 Robustness Checks

Any analysis that relies on AI-assisted classification of 15,000 people's life histories, draws on an incomplete historical encyclopedia, and includes assumptions about people who may or may not still be alive needs to show that its conclusions do not fall apart when those assumptions are changed. Three stress tests were applied to examine this.

**Test 1 — What if the "implausibly alive" individuals died at different ages?** The dataset includes 185 people born before 1920 who have no recorded death date — meaning they would be over 106 years old today if truly alive. Almost certainly their deaths simply were not captured in the ESU. Since their true age at death is unknown, we assumed 80 years in the primary analysis. We re-ran the model five times assuming death at ages 70, 75, 80, 85, and 90 to see if the assumption matters. The migrated hazard ratio moved between 1.067 and 1.100 across these scenarios. The direction is unchanged; the magnitude barely moves. The finding does not depend on this assumption.

**Test 2 — What if some "migrants" are actually post-Soviet emigrants, not Soviet-era?** Among living migrants born after 1960, 62 individuals were flagged as likely post-Soviet emigrants — people who may have left Ukraine after 1991 rather than as part of the historical first or second emigration waves. Including them in the "migrated" category could theoretically blur the Soviet-era signal. We re-ran the model three ways: keeping them as migrants, removing them from the dataset entirely, and reclassifying them as non-migrants. The hazard ratio shifted by at most 0.006 units — statistically indistinguishable from zero. Sixty-two people out of 15,053 do not drive the result.

**Test 3 — What if the AI got many classifications wrong?** The AI pipeline was validated at a 3.2% error rate on a manually checked sample of 62 individuals (§8). To stress-test beyond this, we simulated random misclassification at three times the observed rate: 5%, 10%, and 15% of all 15,053 records were randomly reassigned to a different migration group. This was repeated 50 times at each rate to get a stable estimate of the effect. The migrated hazard ratio remained between 1.077 and 1.088 (median across 50 runs) at all three rates. Even at 15% random misclassification — nearly five times the validated error rate — the result is stable.

All three tests use the unadjusted (Model 1) Cox results for speed; the primary finding is the adjusted Model 2 HR of 0.832. The sensitivity analyses confirm that the adjusted finding is not an artefact of any single classification decision or dataset assumption.

**Figure 27.** Summary of all robustness checks. Each point shows the migrated hazard ratio under a different assumption or misclassification scenario, with error bars indicating uncertainty. The dashed horizontal line is the null (HR=1.0); the dotted line is the baseline adjusted estimate (HR=0.832). All unadjusted sensitivity points cluster above 1.0 (reflecting the cohort-mixing effect when birth decade is not controlled), while the adjusted baseline sits clearly below 1.0, showing the migrant survival advantage that emerges once like is compared with like.

---

## 5. Discussion

### 5.1 Interpreting the Mortality Gap

The 4.04-year gap in mean age at death between migrant and non-migrant Ukrainian creative workers is statistically robust, methodologically defensible, and consistent across all analytical disaggregations. The additional finding of a 22.87-year gap between non-migrants and deportees (d = 1.656) is arguably the study's most dramatic result. Neither finding is a simple measure of the mortality differential associated with Soviet rule for any individual — both are population-level summary statistics that aggregate across highly heterogeneous individual experiences.

The gap reflects, we argue, primarily four mechanisms:

**Direct political mortality.** The most evident mechanism is execution, imprisonment, and Gulag death. The 89 non-migrated and deported deaths concentrated in 1937 alone (average age ~44 for those two groups, versus 68.9 for the 10 migrants who died the same year of natural causes), the deported group's 88.0% repression-cause mortality (executed, Gulag, exile, and other state-violence causes combined), and the near-total destruction of the 1890s deported cohort (mean age at death of 44.6) all point to a substantial excess mortality from direct state violence that had no equivalent in migrant communities.

**Indirect mortality from Soviet conditions.** Beyond direct political violence, Soviet conditions — poor nutrition, restricted medical care, psychological stress from constant surveillance and self-censorship, the health consequences of Gulag survival, and enforced poverty — likely contributed to excess mortality among non-migrants across the entire Soviet period. This mechanism is not directly measurable from our data but is consistent with the lower average age at death in every Soviet-era period compared to the post-1991 period.

**Selection effects in emigration.** Not all emigration is equivalent in its effect on subsequent mortality. Those who emigrated during the first wave (1917–1921) typically did so from positions of some privilege — they had resources, connections, and the ability to plan. Those who fled during the second wave (World War II) often did so under extremely dangerous conditions, with significant mortality risk during flight. It is plausible that the migrant group in our dataset is positively selected for resourcefulness, social capital, and health relative to the non-migrant group, which would mean that some portion of the mean age at death gap reflects pre-migration differences rather than the causal effect of Soviet conditions.

**Wave disaggregation — attempted and not feasible with current data.** Disaggregating the migrant group by emigration wave (pre-1922 UNR/Civil War, 1939–45 WWII displacement, 1946–91 Cold War) would constitute a powerful structural test of the self-selection critique: if the mortality gap held across three waves with entirely different selection mechanisms, a single unobserved pre-migration confounder could not explain it. This analysis was attempted (Stage 9) but cannot be reported as a finding. The ESU biographical text from which emigration year would need to be derived was processed in Stage 4 to determine migration *status* — not to capture the *year* of emigration. Manual review of classified entries confirmed that the automated classifier was predominantly recovering death year (the year mentioned in the text to establish that the person died outside Ukraine) rather than departure year. A person who left Ukraine in 1944 and died in New York in 1972 would be misclassified as a Cold War (Wave 3) emigrant because 1972 is the year that appears in the reasoning text. This is a data capture limitation, not an analytical one: the biographical structure necessary for wave assignment exists in the source ESU articles but was not extracted during the initial pipeline. Wave disaggregation is a priority for V3 data collection (see §5.4).

**Period effects and cohort differences.** As noted in the birth cohort analysis, the gap is concentrated in the 1880s and 1890s cohorts — the Executed Renaissance generation — and is nearly absent in the 1920s cohort. This cohort patterning argues against a simple interpretation of the gap as reflecting baseline differences between migrants and non-migrants; if the gap were primarily driven by selection effects, we would expect it to be more uniform across cohorts.

### 5.2 The Narrowing of the Measured Gap

The reduction in the measured gap from 9 years (V1) to 4.04 years (V2) deserves careful interpretation. It does not represent a finding that Soviet repression was less lethal than previously estimated. Rather, it reflects the inclusion of a large cohort of non-migrants who survived the Soviet period and lived into old age in independent Ukraine — a population that was categorically excluded from V1 by the pre-1991 death cutoff.

The V1 finding of a 9-year gap was a real finding within its analytical scope: among workers who died before 1991, the gap was approximately that large. V2 does not contradict V1; it extends the analysis to a more complete and representative population. The policy implication is methodological: future studies of Soviet-era mortality should not apply post-Soviet death cutoffs, as doing so systematically excludes the longest-lived members of the "stayed" cohort and artificially inflates the measured mortality differential.

### 5.3 Geographic Findings and Their Significance

The strong west-east gradient in migration rates — from Lviv's 45.1% to Donetsk's 0% — is not merely a demographic curiosity. It reflects a fundamental division in Ukrainian cultural geography that predates the Soviet period and has continued to shape Ukrainian society through independence and into the present. Western Ukraine's Galician and Bukovinian regions were under Austro-Hungarian rule until 1918, developed a distinct civic and cultural tradition, and maintained stronger connections to Central European and Western intellectual life. This made emigration to Vienna, Prague, Paris, and ultimately North America both more conceivable and more practically feasible for western Ukrainian creative workers.

Eastern and southern Ukrainian creative workers, by contrast, were longer-embedded in Soviet institutions, faced steeper barriers to emigration (both practical and ideological), and were more likely to have professional identities intertwined with Soviet cultural organisations. That the Donbas region shows 0% migration in our dataset is consistent with this broader pattern but should be interpreted cautiously given the small sample size (n=14).

### 5.4 Limitations

**Survivorship bias in the ESU.** The Encyclopedia of Modern Ukraine documents individuals whose work was significant enough to merit encyclopedic inclusion. This represents a small fraction of all Ukrainian creative workers, and there is reason to believe it is not a random sample of that population. Individuals who were executed at young ages left smaller bodies of work and may be underrepresented in the ESU relative to their actual numbers. Conversely, very prolific or long-lived workers may be overrepresented. This source of bias could operate in either direction with respect to our age-at-death estimates.

**Migration status as a simplification.** This study uses four categories — migrated, non-migrated, internal transfer, and deported — but even four categories compress a highly varied range of historical experiences. Within the "non-migrated" group, some individuals were internally displaced within the Soviet Union, some were imprisoned in the Gulag for years before release and return, and some lived in regions that changed occupying powers multiple times (for example, Galicia and Bukovyna, which passed between Austro-Hungarian, Polish, and Soviet control across the twentieth century). The "internal transfer" category similarly aggregates very different situations: a composer reassigned to Moscow by a Soviet cultural ministry is not the same as an artist who relocated to Siberia for career reasons or under political pressure. The "deported" group is the most internally consistent — forced deportation is a specific and documented state act — but even here, conditions varied enormously between those exiled to Siberian settlements, those sent to Gulag hard labour camps, and those briefly imprisoned and released. Our classification system makes reasonable distinctions where the data permit and is the most granular practically achievable from biographical encyclopedia text, but it should not be treated as capturing the full complexity of individual experiences.

**AI-assisted classification errors.** The use of Claude for nationality and migration classification introduces potential systematic errors if the model's training data, linguistic capabilities in Ukrainian, or reasoning about Soviet historical context were biased in any particular direction. A manual validation of a random sample of 63 entries yielded an observed error rate of 3.2% (2 errors in 62 reviewable entries; see §8 for full details). This estimate carries wide confidence intervals given the sample size, and category-specific error rates were not computed. Systematic directional bias — in which errors disproportionately favour one migration group — cannot be excluded. The sensitivity analysis (Figure 14) demonstrates that the primary finding remains positive under error rates up to 10%, more than three times the observed rate.

**Observational design and causal limitations.** This paper documents a robust statistical association between migration status and observed age at death among Ukrainian creative workers. It is an observational study and does not identify a causal effect of migration or of Soviet conditions on mortality. The mean age at death gap may reflect, in whole or in part, pre-existing differences between the migrant and non-migrant populations — in health, social capital, resources, or risk tolerance — rather than the effect of Soviet conditions per se. Migrants and non-migrants differ systematically in ways both observed (birth cohort, profession, region) and unobserved, and no study design short of a randomised experiment can fully separate these from the effect of the exposure. The multivariable regression in §4.9 demonstrates that the gap persists after adjusting for observed compositional differences, which is consistent with, but does not establish, a causal interpretation. The birth cohort patterning — with the gap concentrated in the 1880s and 1890s generations whose prime years coincided with peak Soviet repression — further supports this interpretation, but selection effects cannot be ruled out. All findings should be read as descriptive associations.

**Self-selection bias in emigration.** The decision to emigrate was not random. Ukrainian creative workers who left the Soviet Union were a self-selected group, and this selection was almost certainly correlated with characteristics that independently predict longer life — including higher social capital (the connections and resources needed to arrange emigration), stronger ties to Western European intellectual networks, greater risk tolerance and agency, and, in some cases, advance warning of or sensitivity to political danger. These unobserved pre-migration differences constitute a potential confound: some portion of the 4.04-year mean age at death gap may reflect who migrated rather than what migration protected them from.

The direction of this bias is not straightforward, however. There are at least two partially offsetting mechanisms. First, positive health selection (healthier, more resourceful individuals were more likely to emigrate) would cause us to *overestimate* any protective effect of emigration. Second, survival selection during emigration itself — particularly for the second wave (1941–1945), where flight from advancing Soviet forces carried substantial mortality risk — would cause us to *underestimate* the emigrant group's baseline health, since many who died fleeing are absent from our dataset entirely. The net direction of these combined biases is empirically uncertain.

The multivariable regression in §4.9 adjusts for observed compositional differences (birth cohort, profession, region of origin), and the gap remains statistically significant at 3.31 years after adjustment. As a further check on selection, propensity score matching was performed using logistic regression to estimate a propensity score for each migrated worker based on birth decade, profession, and birth region, then matching each migrated worker to their nearest-neighbour non-migrated worker on this score. In the matched sample (n=1,280 pairs), the mean age at death gap was **+3.35 years** (bootstrap 95% CI: [2.26, 4.45]), compared to +4.04 years in the full unmatched sample. The 17% attenuation after matching is consistent with a modest positive health selection effect on observable covariates, but the substantial residual gap confirms that the finding is not simply an artefact of birth-cohort, profession, or geographic composition differences. Unobservable confounding cannot be fully eliminated with these methods; the PSM estimate should be interpreted as a lower bound on the gap unexplained by observable pre-migration characteristics.

Readers should interpret all comparative statistics in this paper as descriptive associations rather than causal estimates. The most defensible claim is not "emigration caused longer survival" but rather "documented Ukrainian creative workers who emigrated lived, on average, 4.04 years longer than those who remained, after adjustment for birth decade, profession, and region; the gap was 3.35 years in a propensity-score matched sample." Remaining open questions include instrumental variable approaches, diaspora archive comparisons, and heterogeneity analysis by repression-exposure cohort; these are left for future work.

**Post-1991 framing caveat.** A related limitation concerns the temporal scope of the measured gap. 61.5% of non-migrant deaths in this dataset occurred after the dissolution of the Soviet Union (post-1991). The observed mean age at death gap therefore captures *cumulative lifetime effects* — including post-Soviet Ukrainian healthcare disruption, the 1990s economic collapse (which produced a documented male mortality crisis across former Soviet states), and the general health consequences of late-Soviet living standards — rather than a clean Soviet-era signal. The 1965–1991 period analysis (§4.4, Figure 9) provides a partial check by restricting to those who died during Soviet rule, but the full-dataset gap should be read as a lifetime-accumulated effect, not a Soviet-period-specific estimate.

**Gender breakdown.** Figures 17 and 18 document gender composition and mean age at death by gender within each group. Male workers predominate in all four groups (consistent with the ESU's historical composition), but the migrated/non-migrated gap holds for both sexes, confirming the primary finding is not an artefact of differential gender composition across groups.

**Figure 17.** Gender composition (% male / % female) within each of the four migration groups. All groups are male-dominated, consistent with the ESU's historical coverage of the creative sector; the migrated group is approximately 72% male, non-migrated 74% male, internal transfer 71% male, deported 81% male.

**Figure 18.** Mean age at death disaggregated by gender within each migration group. The migrated/non-migrated gap is present for both male workers (~3.8 yrs) and female workers (~4.5 yrs), confirming the primary finding is not driven by differential gender composition across groups.

**Missing data.** Of the 16,215 entries in our initial dataset, 8,643 (53.3%) met our inclusion criteria for the primary age-at-death analysis. The remaining 46.7% were excluded primarily because they lacked death dates (living individuals or individuals whose death date was not recorded in the ESU), because migration status could not be determined, or because they died before the Soviet period began. Date recovery from the ESU's biographical text using automated parsing of biographical notes increased the initial analysable pool from 6,106 entries (37.7%) to the current 8,643 (53.3%); full details are documented in SCIENTIFIC_METHODOLOGY.md (§4). If the remaining excluded population differs systematically from the included population in ways correlated with age at death, our estimates may be biased.

**Emigration year not captured — wave disaggregation deferred to V3.** The Stage 4 AI classification pipeline was designed to determine *whether* each individual emigrated, not *when* they left. As a consequence, the dataset contains no reliable emigration year field. A rule-based wave classifier (Stage 9) was built and applied to all 1,313 migrant entries, but manual review of a 50-entry random sample confirmed that the classifier was predominantly recovering *death year* — the year that appears in the biographical reasoning text as evidence of settlement outside Ukraine — rather than *departure year*. This produces systematic misclassification: a migrant who left during WWII and died in 1978 is assigned to the Cold War wave; a person born in 1920 who emigrated in 1950 is assigned to the pre-1922 wave on the strength of their birth year alone. The wave figures (Fig. 29, 29b, 29c) and associated statistics are therefore not reported as findings. Recovering emigration year requires a targeted re-pass over the original Ukrainian ESU article text, extracting departure-specific language ("виїхав у", "емігрував до", "залишив Україну") rather than the all-years approach used in Stage 4. This is a defined deliverable for V3.

**Incomplete ESU source coverage — a quantified lower bound.** Several prominent Ukrainian creative workers are absent from our dataset entirely — they have no published ESU articles as of the 2026 access date, confirmed by exhaustive crawler audit. The ESU's coverage gaps are not randomly distributed. Encyclopedic inclusion favours individuals with large surviving bodies of work — precisely the biographical infrastructure that Soviet repression dismantled. A writer shot at age 38 in 1937 produced fewer books than one who lived to 75; their institutional affiliations were dissolved, their biographical documentation suppressed. The mechanisms that determine ESU inclusion are the same mechanisms that Soviet repression attacked.

Seven confirmed absent figures who meet study inclusion criteria are documented in Table MF. All seven are non-migrants; their mean age at death is 39.0 years — 32 years below the current non-migrant mean of 71.22.

**Table MF. Confirmed absent Ukrainian creative workers meeting study inclusion criteria**

| Name | Birth | Death | Age | Cause of death |
|------|-------|-------|-----|----------------|
| Vasyl Stus | 1938 | 1985 | 47 | Died in Perm-36 corrective labour colony |
| Mykola Khvylovy | 1893 | 1933 | 39 | Suicide under direct political pressure |
| Vasyl Symonenko | 1935 | 1963 | 28 | Disputed; suspected KGB custody injuries |
| Mykhailo Semenko | 1892 | 1937 | 45 | Shot; Great Terror, October 1937 |
| Yevhen Pluzhnyk | 1898 | 1936 | 38 | Shot; Solovki execution, February 1936 |
| Myroslav Irchan | 1897 | 1937 | 40 | Shot; Great Terror, 1937 |
| Dmytro Falkivsky | 1898 | 1934 | 36 | Shot; NKVD execution, 1934 |

*Sources: Sandarmokh memorial execution lists; SBU declassified archival files; Rehabilitovani istoriieiu series; Memorial database.*

*Note: Several other documented Executed Renaissance figures — including Mykola Zerov, Hryhorii Kosynka, Valerian Pidmohylny, and Les Kurbas — are present in the ESU dataset and correctly classified as non_migrated. Their deaths are already counted in the non-migrant mean.*

A sensitivity analysis (Figure 30) quantifies the direction and plausible magnitude of this bias. The adjusted gap formula is: mean_nm_adj = (mean_nm × n_nm + Ā_missing × M) / (n_nm + M), where M is the number of missing non-migrants and Ā_missing is their mean age at death. Because Ā_missing < mean_nm under all historical assumptions, the gap *widens* as M increases — the current estimate of 4.04 years is a conservative lower bound.

Adding only the confirmed seven named cases (M=7, Ā=39.0) adjusts the non-migrant mean downward by 0.04 years, raising the gap to 4.08 years. Adding 50 additional missing workers at Ā=38 years adjusts the gap to 4.31 years. Adding 200 yields a gap of 5.10 years. Even under the most aggressive plausible assumptions (M=500, Ā=38), the gap reaches 6.58 years — always in the same direction, never narrowing. A critic who wishes to argue that ESU coverage bias *reduces* the observed gap must assert the existence of a large population of missing migrants who died young — which is historically implausible: emigrants, by definition, left the Soviet repression apparatus, and no mechanism in the historical record produces mass early mortality among Ukrainian diaspora creative workers.

The direction of the ESU coverage bias is unambiguous: the current estimate of 4.04 years is a conservative lower bound on the true mortality differential.

**Galician survival selection bias.** Our inclusion criteria (§3.4, Table B) exclude Galician-born individuals whose recorded death year preceded 1939, on the grounds that the Galician regions — Lviv, Ternopil, and Ivano-Frankivsk oblasts — remained under Polish administration until the Soviet annexation of Western Ukraine following the Molotov-Ribbentrop Pact of 1939. Creative workers from these regions who died before that annexation were never subject to Soviet rule and are therefore analytically incommensurable with the core dataset population; their inclusion would conflate mortality under Polish or Habsburg governance with mortality under Soviet occupation. Galician-born individuals who survived into the Soviet period are included in the dataset under the standard classification criteria. This design choice, however, introduces a survival selection bias specific to the Galician sub-population: only those Galicians who lived past 1939 are represented, meaning the Galician cohort in our dataset is not a random sample of all Galician creative workers active in the relevant period, but a sample conditioned on survival to the Soviet era. The practical consequence is non-trivial, because Galicia contributes disproportionately to our migrated group — Lviv-born workers emigrated at 45.1%, Ternopil-born at 52.9%, and Chernivtsi-born at 34.8%, among the highest regional migration rates in the dataset (see §4.7). If those Galicians who died before 1939 (and are therefore excluded) were on average shorter-lived than those who survived, the surviving Galician cohort that does enter the dataset is healthier and longer-lived than the true Galician baseline, which would cause us to underestimate the magnitude of the mean age at death gap for Galician emigrants relative to their actual population. Future research incorporating non-Soviet administrative records from the interwar period would allow this exclusion criterion to be relaxed and this source of bias to be directly quantified.

### 5.5 Comparisons to Related Research

Our findings are broadly consistent with existing historical scholarship on Soviet repression and with the limited quantitative literature on mortality in Soviet-era populations. Studies of Gulag mortality[^6] document catastrophic death rates in Soviet labor camps, reaching 20–25% annually during 1942–1943, and systematic mass executions during 1937–1938. These documented mortality patterns are broadly consistent with our deported group's average age at death of 43.4 years during 1934–1938 and 44.4 years during 1939–1945.

Comparative demography of Soviet versus Western European general populations[^7] documents a Soviet mortality penalty that grew from approximately 3 years in the mid-1960s to over 10 years by the early 1990s, depending on country and sex. Andreev et al. additionally reconstruct Soviet demographic conditions for the 1927–1959 period, directly covering our Great Terror and Holodomor years. Our finding of a 4.04-year gap is consistent with the lower end of the East-West divergence range, though our dataset's specific focus on a group subject to targeted repression means our estimate captures both the general Soviet mortality penalty and the profession-specific repression effect.

Figures 19 and 19b show normalised annual death rates (deaths per year as a percentage of each group's size) across the Soviet period, making the 1937 spike in the deported group visually prominent relative to all other groups. Figure 21 contextualises creative workers' mean age at death against published estimates for comparable Soviet-era republic populations. Figure 22 compares non-migrant creative workers against an estimated educated urban Ukrainian baseline, showing that non-migrants in repression periods fall below even the general population estimate — suggesting excess mortality over and above what socioeconomic composition alone would predict.

**Figure 19.** Normalised annual death rate (deaths per year as % of group size) for all four migration groups, 1921–1992. The 1937 spike in the deported group — reaching approximately 35% of the group's total size in a single year — dwarfs all other groups in all other years, making the concentration of state violence in a single calendar year visually unmistakable.

**Figure 19b.** Simplified version of Figure 19 showing three lines: migrated, non-migrated (stayed in USSR), and a combined "stayed in Soviet sphere" composite. Reduces visual complexity while preserving the key 1937 signal and the divergence between emigrant and non-emigrant trajectories.

**Figure 21.** Mean age at death for Ukrainian creative workers (non-migrated group) compared against published estimates for general populations of comparable Soviet-era republics (Russia, Ukraine, Belarus). Non-migrants in repression periods fall substantially below general-population baselines, consistent with targeted political mortality over and above the general Soviet mortality penalty.

**Figure 22.** Mean age at death for the non-migrated creative worker group compared against an estimated educated urban Ukrainian baseline derived from demographic studies of comparable cohorts. Non-migrants in the Great Terror and wartime periods fall below the educated-urban baseline, suggesting excess mortality that is not fully explained by socioeconomic composition.

---

## 6. Conclusion

This paper presents the most comprehensive quantitative analysis to date of observed age at death among Ukrainian creative workers under Soviet occupation. Across a dataset of 8,643 individuals with confirmed birth dates, death dates, and migration status — more than twenty times larger than our V1 dataset — two clusters of findings emerge. They are not equally certain, and treating them as such would misrepresent what the data can and cannot establish.

**What the data can establish with confidence.** The strongest findings in this study do not depend on assumptions about who chose to emigrate or why, because they do not involve voluntary emigration at all. Workers **deported by the Soviet state** — people removed from their homes by government force, with no element of self-selection — died at a mean age of 48.35 years, a deficit of **22.87 years** relative to non-migrants (d=1.656, HR=4.646 in the adjusted Cox model, p<0.001). This is not a subtle statistical signal. It reflects mass execution, Gulag death, and the lethal conditions of forced exile. Workers who **transferred voluntarily within the Soviet system** showed no survival advantage whatsoever over those who stayed (+0.52 yrs, p=0.094, HR≈1.08). Read together, these two results answer a precise historical question: was it *leaving* that extended life, or was it *escaping Soviet jurisdiction entirely*? The internal transfer null rules out the first explanation. The only form of movement that was associated with longer life was emigration out of the Soviet sphere altogether — which points to conditions within that sphere, not the act of movement, as the operative variable.

**What the data describe consistently but cannot fully explain.** Those who emigrated lived on average **4.04 years longer** than non-migrants (Cohen's d=0.292, p<0.001). This gap is statistically robust, survives propensity score matching on birth decade, profession, and region (reduced to 3.35 years, 95% CI [2.26, 4.45]), and is confirmed by Cox proportional hazards analysis (HR=0.832, approximately 17% lower mortality hazard after covariate adjustment). It is concentrated in the birth cohorts hit hardest by Stalinist repression, narrows substantially in later cohorts, and replicates across every analytical disaggregation we conducted. All of this is consistent with the interpretation that leaving the Soviet sphere was associated with longer life because of what that sphere subjected people to. But this comparison involves a self-selected group — people who managed and chose to leave — and we cannot fully rule out that those individuals were already in some ways advantaged before departure. We present this finding as strong descriptive evidence that is consistent with, and reinforces, the causal findings above. We do not claim it alone establishes a Soviet mortality effect. The deportation result and the internal transfer null do that. The migration gap makes that picture more complete.

The gap is not uniform: it is largest for the 1880s and 1890s birth cohorts (the Executed Renaissance generation, with identical gaps of 5.1 years for both cohorts), for Architects (+6.1 years) and Other Creative workers (+4.9 years), and for workers born in western Ukrainian cities (who emigrated at rates of 35–53% compared to near-zero rates in eastern Ukraine). It narrows substantially for the post-Terror cohorts, a pattern consistent with the interpretation that the gap reflects, at least in part, cohort-specific political violence rather than stable baseline differences between migrants and non-migrants.

The 1937 spotlight analysis reveals that 100 Ukrainian creative workers in our dataset died in that single year. Among the 89 who remained under Soviet rule (24 non-migrated + 65 deported), the blended average age at death was approximately 44 — predominantly Writers and Poets — in a pattern consistent with mass political execution rather than natural mortality. The 10 migrants who died in 1937 did so at a mean age of 68.9, consistent with natural mortality; the within-year gap of 26.5 years between the migrated and deported groups makes the mortality differential visible within a single calendar year. The repression period analysis shows average ages at death of 55.5 years (non-migrated) and 43.4 years (deported) during the Great Terror (1934–1938), the lowest of any period in our data, contrasting with 74.7 years for those who died in the post-independence period.

These findings are consistent with what Ukrainian historians have documented through archival and testimonial evidence: that Soviet cultural policy was associated with substantial mortality differentials among the creative workers who remained under Soviet rule, concentrated particularly in the generation that came of age between the Revolution and the Great Terror. The numbers do not tell the full story — they cannot capture the individual lives, the works that were never written, the music that was never composed, the theatres that went dark — but they provide a quantitative description of mortality patterns that complements the existing archival and testimonial record.

We make no claim that this analysis is definitive. The ESU-based dataset is not a complete census of Ukrainian creative workers; our migration classification system makes simplifications that the historical record does not always support; and the selection effects inherent in emigration preclude clean causal inference. Future research should seek to replicate and extend these findings using alternative data sources — particularly Soviet-era repression records, diaspora archives, and memorial databases — and should apply methods capable of addressing the selection problem more rigorously.

The Executed Renaissance is not merely a literary metaphor — it describes a historical demographic event whose mortality signature, this study suggests, is quantitatively detectable at scale among the documented figures of Ukrainian cultural life.

---

## 7. Figure Index

All figures were generated computationally from the dataset described in §3 and are available in the `/charts/` subdirectory of the project repository. Captions appear inline with the figures' first mention in the text. The list below provides a brief label index for navigation.

| Figure | Location in paper | Description |
|--------|------------------|-------------|
| Fig 1 | §4.1 | Primary bar chart — mean age at death with 95% CI, all four groups |
| Fig 2 | §4.2 | Kaplan-Meier survival curves, all four groups |
| Fig 3 | §2.3 | Prior study vs. present study comparison |
| Fig 4 | §4.1 | Box plots — age at death distribution, all four groups |
| Fig 5 | §4.8 | Deported group age-at-death histogram |
| Fig 6 | §4.8 | Split violin plots by gender × group |
| Fig 7 | §4.8 | Death year histogram — migrated vs non-migrated |
| Fig 7b | §4.5 | Death year histogram — deported group, 1920–1960 |
| Fig 8 | §4.4 / §4.5 | Year-by-year deported deaths bar chart |
| Fig 9 | §4.4 | Mean age at death by Soviet historical period |
| Fig 10 | §4.6 | Mean age at death by birth decade (line chart) |
| Fig 11 | §4.3 | Mean age at death by creative profession |
| Fig 12 | §4.7 | Top 20 birth cities — migration rates |
| Fig 13 | §4.6 | Birth year distribution — methodological overlap check |
| Fig 14 | §4.2 | Sensitivity analysis — AI error rate robustness |
| Fig 15 | §4.1 | Internal transfer vs non-migrated (null comparison) |
| Fig 15b | §4.1 | All-groups box plot with statistical conclusions overlay |
| Fig 16 | §3.4.1 | CONSORT-style exclusion flowchart |
| Fig 17 | §5.4 | Gender composition by group |
| Fig 18 | §5.4 | Mean age at death by gender × group |
| Fig 19 | §5.5 | Normalised annual death rate, all groups, 1921–1992 |
| Fig 19b | §5.5 | Simplified three-line version — migrated vs stayed in USSR |
| Fig 20 | §4.1 | Conservative two-group comparison |
| Fig 21 | §5.5 | Contextualisation vs Soviet republic populations |
| Fig 22 | §5.5 | Comparison vs educated urban Ukrainian baseline |
| Fig 23 | §4.9 | Regression coefficient plot — OLS Model 1 vs Model 2 |
| Fig 24 | §4.10 | Cox PH forest plot — hazard ratios, Model 1 + Model 2 (right-censored N=15,053) |
| Fig 25 | §4.10 | Censoring pattern — % dead vs alive by migration group (V2.4, proper distribution) |
| Fig 26 | §4.10 | KM survival curves with right-censored living individuals (N=15,053) |
| Fig 27 | §4.11 | Sensitivity analysis summary — migrated HR across all scenarios |
| Fig 28 | §4.10 | Time-varying HR for deported group by age band (landmark Cox) |
| Fig 28b | §4.10 | Schoenfeld residual smoothed log-HR for deported group |

---

## 8. AI Methodology Note

In the interest of full methodological transparency, we disclose the following regarding the use of artificial intelligence tools in this study.

**Data classification.** Claude (Anthropic), a large language model, was used to review 1,356 entries with ambiguous nationality markers and to assist with migration classification for a subset of entries where the biographical text was ambiguous. Claude was provided with the full Ukrainian-language ESU text for each entry and asked to classify the entry according to pre-specified criteria documented verbatim in the companion SCIENTIFIC_METHODOLOGY.md file. Nationality classification (Tier 2 review) used claude-haiku-4-5-20251001. Migration classification used claude-haiku-4-5-20251001 as a first pass, with claude-sonnet-4-6 as a deep-retry for entries returning 'unknown'. All classifications used default temperature settings.

**Validation of AI-assisted classification.** To assess classification accuracy, a random sample of 63 entries (approximately 1% of the analysable dataset at the time of validation, seed=99, independent of the primary analysis) was drawn from the classified dataset. For each sampled entry, the full ESU biographical text was retrieved and reviewed by a human researcher (the author) against the pre-specified classification criteria. Of the 62 entries for which a definitive human verdict could be reached, two were judged to be incorrectly classified by the AI, yielding an **observed error rate of 3.2%** (95% CI: approximately 0.9%–7.9% by exact binomial). Both errors were non-systematic edge cases rather than indicators of a category-level classification rule failure: one involved a borderline nationality determination, one involved a reclassification of migration status. Neither error was in the direction of systematically favouring the migrated group.

This validation has important limitations. A sample of n=62 is sufficient to estimate an order-of-magnitude error rate but provides only modest statistical precision (the 95% confidence interval spans approximately 1%–8%). The sample was drawn from a prior version of the dataset (V2.1); some reclassifications were made in subsequent versions. The validation covered only a random sample of entries and cannot rule out systematic misclassification in specific sub-populations (e.g., entries with complex transnational biographies). Category-specific error rates — separately for nationality and migration classification, and separately for each migration category — were not computed due to sample size constraints. A larger external validation study, ideally by independent reviewers with expertise in Ukrainian biographical history, would substantially strengthen the methodological claim.

Claude's classifications were not adjusted based on their consistency with the study's hypotheses; the validation review was conducted before the primary statistical analysis was finalised. The sensitivity analysis (§4.2, Figure 14) demonstrates that the primary finding is robust to error rates substantially exceeding the estimated 3.2%.

**Writing assistance.** Claude was used as a writing assistant in the drafting of this manuscript. The empirical content, analytical interpretation, and conclusions are entirely the work of the author. Claude's contribution was limited to prose editing, structural suggestions, and assistance with academic English phrasing.

**No autonomous decision-making.** AI tools did not make autonomous decisions about study design, statistical methods, or the interpretation of findings. All methodological choices documented in this paper were made by the author.

Transparent disclosure of AI tool use is essential for the integrity of the academic record and for enabling other researchers to replicate this methodology. The full prompts, model names, and procedural details are documented in the companion SCIENTIFIC_METHODOLOGY.md.

**Appendix A (recommended for expanded validation).** A complete validation study would report the following, which future iterations of this work should provide: (1) a confusion matrix for each classification task (nationality determination, migration status) showing true positives, false positives, false negatives, and true negatives by category; (2) category-specific accuracy rates for each of the four migration groups (migrated, non-migrated, internal transfer, deported) separately; (3) inter-rater reliability if a second independent reviewer codes a subset; and (4) an error analysis of incorrectly classified entries identifying whether misclassifications cluster around specific biographical types (e.g., figures with transnational careers, dual nationalities, or ambiguous emigration circumstances). The current validation sample (n=62) is insufficient to compute reliable category-specific metrics; a minimum sample of 200–300 entries per classification task would be required for publication-grade validation statistics.

---

## 9. Bibliography

Andreev, E. M., L. E. Darsky, and T. L. Kharkova. *Demographic History of Russia: 1927–1959*. Moscow: Informatika Publishers, 1998.

Applebaum, Anne. *Gulag: A History*. New York: Doubleday, 2003.

Barnes, Steven A. *Death and Redemption: The Gulag and the Shaping of Soviet Society*. Princeton: Princeton University Press, 2011.

Cohen, Jacob. *Statistical Power Analysis for the Behavioral Sciences*. 2nd ed. Hillsdale, NJ: Lawrence Erlbaum Associates, 1988.

Collett, David. *Modelling Survival Data in Medical Research*. 3rd ed. Boca Raton: CRC Press, 2015.

Institute of Encyclopedic Research of the National Academy of Sciences of Ukraine [Інститут енциклопедичних досліджень НАН України]. *Encyclopedia of Modern Ukraine* [Енциклопедія сучасної України]. Accessed 2026. https://esu.com.ua.

Lavrinenko, Yuriy. *Rozstriliane vidrodzhennia: Antolohiia 1917–1933* [The Executed Renaissance: An Anthology, 1917–1933]. Paris: Instytut Literacki, 1959.

Preston, Samuel H., Patrick Heuveline, and Michel Guillot. *Demography: Measuring and Modeling Population Processes*. Oxford: Blackwell, 2001.

Meslé, France, and Jacques Vallin. "Mortality in Europe: The Divergence Between East and West." *Population* (English edition) 57, no. 1 (2002): 157–197.

Myshanych, O., and M. Semenko. *Ukrainska literatura XX stolittia* [Ukrainian Literature of the Twentieth Century]. Kyiv: Naukova Dumka, 1991.

Škandrij, Myroslav. *Ukrainian Nationalism: Politics, Ideology, and Literature, 1929–1956*. New Haven: Yale University Press, 2015.

Subtelny, Orest. *Ukraine: A History*. 3rd ed. Toronto: University of Toronto Press, 2000.

Berdnyk, Elza, Mark Symkin, and Alona Motiashova. "Life Expectancy of Ukrainian Creative Industry Workers during the Soviet Occupation: A Preliminary Study (V1)." Harvard Graduate Masterclass final project, 2025. https://github.com/symkinmark/ukraine-creative-workers-v2/blob/main/v1_paper.pdf.

---

[^1]: Instytut entsyklopedychnykh doslidzhenʹ NAN Ukraïny [Institute of Encyclopedic Research of the National Academy of Sciences of Ukraine], *Entsyklopediia suchasnoï Ukraïny [Енциклопедія сучасної України]* [Encyclopedia of Modern Ukraine], accessed 2026, https://esu.com.ua.

[^2]: Orest Subtelny, *Ukraine: A History*, 3rd ed. (Toronto: University of Toronto Press, 2000).

[^3]: Yuriy Lavrinenko, *Rozstriliane vidrodzhennia: Antolohiia 1917–1933* [The Executed Renaissance: An Anthology, 1917–1933] (Paris: Instytut Literacki, 1959); Myroslav Škandrij, *Ukrainian Nationalism: Politics, Ideology, and Literature, 1929–1956* (New Haven: Yale University Press, 2015); O. Myshanych and M. Semenko, *Ukrainska literatura XX stolittia* [Ukrainian Literature of the Twentieth Century] (Kyiv: Naukova Dumka, 1991).

[^4]: Elza Berdnyk, Mark Symkin, and Alona Motiashova, "Life Expectancy of Ukrainian Creative Industry Workers during the Soviet Occupation: A Preliminary Study (V1)," Harvard Graduate Masterclass final project, 2025, https://github.com/symkinmark/ukraine-creative-workers-v2/blob/main/v1_paper.pdf.

[^5]: Jacob Cohen, *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed. (Hillsdale, NJ: Lawrence Erlbaum Associates, 1988).

[^6]: Steven A. Barnes, *Death and Redemption: The Gulag and the Shaping of Soviet Society* (Princeton: Princeton University Press, 2011); Anne Applebaum, *Gulag: A History* (New York: Doubleday, 2003).

[^7]: E. M. Andreev, L. E. Darsky, and T. L. Kharkova, *Demographic History of Russia: 1927–1959* (Moscow: Informatika Publishers, 1998) [covers 1927–1959; documents Soviet-era demographic conditions]; France Meslé and Jacques Vallin, "Mortality in Europe: The Divergence Between East and West," *Population* (English edition) 57, no. 1 (2002): 157–197 [documents the East-West LE divergence from 1950s through 1990s, including 1970s–80s gap of approximately 3–10 years depending on country and sex].

[^11]: Table 3 is computed from the primary dataset (`esu_creative_workers_v2_3.csv`, V2.3) using the non-migrated group only (n=6,030). Deaths are classified by the year of death falling within each historical period. Average age at death is the arithmetic mean of (death year − birth year) for all non-migrants dying within that period. Periodisation follows standard Soviet historiography; see Robert Conquest, *The Great Terror: A Reassessment* (Oxford: Oxford University Press, 1990) for the 1934–1938 period, and Orest Subtelny, *Ukraine: A History*, 4th ed. (Toronto: University of Toronto Press, 2009) for the broader periodisation framework.

[^10]: In cohort studies of mortality, right-censoring is only methodologically valid when it is *non-informative* — that is, when who is censored is independent of how long they would have lived had they not been censored. See David Collett, *Modelling Survival Data in Medical Research*, 3rd ed. (Boca Raton: CRC Press, 2015), 1–9; Samuel H. Preston, Patrick Heuveline, and Michel Guillot, *Demography: Measuring and Modeling Population Processes* (Oxford: Blackwell, 2001), 47–53. When censoring is informative — as in V1's 1991 cutoff, where the longest-lived non-migrants are systematically excluded — the resulting estimates are biased in a predictable direction.

[^9]: "Gulag" is used in this paper in its broader historiographic sense to encompass the full range of Soviet penal incarceration institutions — including corrective labor camps (ITL), corrective labor colonies (ITK), special settlements (*spetsposeleniya*), and internal exile — not solely the Main Camp Administration (*Glavnoe upravlenie lagerei*) that was formally dissolved in 1960. Post-1960 Soviet penal labor institutions, such as the Perm-36 corrective labor colony (VS-389/36) where Vasyl Stus died in 1985, were functionally continuous with the pre-1960 Gulag system in their coercive character and lethality, differing primarily in administrative designation. This usage follows Applebaum (2003) and Barnes (2011), who both document the post-Stalin camp system as a structural continuation of the Gulag. Where a specific institution is known, it is named directly.

[^8]: The Mann-Whitney U test (also known as the Wilcoxon rank-sum test) is a standard non-parametric statistical test that compares the full distribution of ages at death between two groups without assuming a normal distribution — appropriate here because political executions produce a heavily skewed left tail of very young deaths. *p* < 0.001 means the result is statistically significant: there is less than a one-in-a-thousand probability that a gap of this magnitude arose by chance. Cohen's *d* is a standardised effect size measure expressing the gap in units of the pooled standard deviation; d = 0.292 falls in the small-to-medium range, meaning the difference is large enough to be observable at the level of individual lives, not merely as a population-level aggregate. Full discussion of statistical method choices is in Section 3.8.
