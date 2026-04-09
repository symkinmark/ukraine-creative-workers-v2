# Observed Age at Death Among Ukrainian Creative Workers Under Soviet Occupation: A Quantitative Study Using the Encyclopedia of Modern Ukraine

**Mark Symkin** | Independent Researcher | 2026

**Version:** V2.6 (Dataset: esu_creative_workers_v2_6.csv | N=8,596 analysable)

---

## Abstract

This study examines whether Ukrainian creative workers who emigrated from Soviet-controlled Ukraine lived longer than those who remained, using biographical data from the Encyclopedia of Modern Ukraine (ESU). The dataset covers 16,215 entries scraped from esu.com.ua, of which 8,596 deceased individuals with complete birth and death years form the analysable cohort. Workers are classified into four groups: *migrated* (left Soviet territory; n=1,328), *non-migrated* (remained in Soviet Ukraine; n=5,962), *internal transfer* (moved within the USSR; n=1,111), and *deported* (forcibly relocated by the Soviet state; n=195).

Migrants died on average 3.93 years later than non-migrants (75.37 yrs vs 71.44 yrs; Cohen's d=0.287; p<0.001). This gap persists across birth cohorts, professions, and genders, and survives propensity-score matching (3.14 yrs; 95% CI: 2.07–4.21). The primary finding is robust to a 10% AI classification error rate.

The strongest signal is among deported workers, who died 22.05 years earlier than non-migrants (mean age 49.39 yrs; Cohen's d=1.613; p<0.001), with peak excess mortality at ages 40–50 (time-varying Cox hazard ratio: 1.89). The internal transfer group shows no significant difference from non-migrants (+0.35 yrs, p=0.269), functioning as a within-Soviet control condition. This null result supports the interpretation that geographic movement per se does not explain the migrant advantage — only exit from Soviet control does.

Cox proportional hazards modelling yields an adjusted hazard ratio of 0.759 (95% CI: 0.713–0.809) for migrants relative to non-migrants, meaning migrants had approximately 24% lower instantaneous mortality risk at any given age. The ESU's known coverage bias (favouring culturally prominent figures whose biographies were documented) means the study captures an elite stratum; the current 3.93-year estimate is a conservative lower bound given that the most severely repressed workers are systematically underrepresented in the archive.

---

## 1. Introduction

The Soviet state's relationship with Ukrainian culture was not merely censorious — it was at times exterminatory. The Executed Renaissance (*Rozstriliane Vidrodzhennia*), a generation of Ukrainian writers, poets, artists, and scholars who flourished in the 1920s and were systematically arrested, executed, or destroyed by the early 1940s, represents one of the most concentrated acts of cultural repression in the twentieth century. Between 1930 and 1941, the Soviet secret police (OGPU/NKVD) arrested hundreds of Ukrainian intellectuals; dozens were shot at Sandarmokh in 1937 alone. Survivors of these purge cohorts faced ongoing surveillance, forced recantations, and the permanent threat of rearrest.

Against this backdrop, emigration was not merely an economic or personal choice — for many Ukrainian creative workers, it was the difference between survival and destruction. Those who managed to leave — primarily through displacement during the First World War (Wave 1: pre-1922), wartime evacuation (Wave 2: 1939–45), or post-war displacement (Wave 3: 1946–91) — ended up in diaspora communities in Western Europe, North America, and Australia. Those who stayed faced a fundamentally different risk environment.

The central research question of this study is: **Did Ukrainian creative workers who emigrated from Soviet-controlled territory live measurably longer than those who remained?**

This is not a study of happiness, artistic output, or political freedom — it is a study of survival, measured in years of life. We use age at death as a single quantifiable outcome that collapses complex processes (physical safety, political persecution, access to nutrition and medical care, psychological stress, occupational disruption) into a single observable variable.

The study is motivated by three considerations. First, the question is tractable: the ESU provides biographical data for thousands of creative workers, including birth and death years for the vast majority. Second, the answer matters historically: if the mortality gap is large and robust, it constitutes quantitative evidence that Soviet cultural repression had measurable demographic consequences — not merely for individual victims, but for an entire professional class. Third, the data exist almost nowhere else in this form: no other systematic biographical compendium covers Ukrainian creative workers across the full Soviet period with comparable depth.

The paper is organised as follows. Section 2 describes the prior study and the present expansion. Section 3 details data sources, inclusion criteria, and methods. Section 4 presents results. Section 5 discusses findings and limitations. Section 6 concludes.

---

## 2. Prior Study and Present Expansion

### 2.1 Prior Study (V1, n=415)

A prior version of this study (V1, 2025) examined a sample of 415 Ukrainian creative workers drawn from the ESU, classified manually into migrated and non-migrated groups. That study found a gap of approximately 5.4 years (migrants 75.8 yrs vs non-migrants 70.4 yrs), with Mann-Whitney U reaching p<0.001. The V1 sample was not systematically sampled and leaned heavily toward writers from the Executed Renaissance cohort — precisely the group most likely to have been killed young in the non-migrated category and most likely to be well-documented in the diaspora migrated category. This selection likely inflated the gap.

### 2.2 Present Expansion (V2.6, n=8,596)

The present study uses a complete scrape of the ESU — all 16,215 entries in the database as of early 2026 — combined with AI-assisted classification via the Claude API (Anthropic). Classification was performed using a structured protocol that checks for forced displacement signals first (to correctly identify deportees and internal transfers), then assigns a migration status. The full ESU scrape covers writers, visual artists, musicians, theatre figures, architects, photographers, and other creative professionals across the full Soviet period. It is not a curated sample.

V2.6 incorporates a systematic database quality pass (Stage 12) that corrected 97 birth-year-as-death-year scraping errors, re-ran 57 API-credit-error classifications, and applied 8 manually validated patches.

### 2.3 Key Differences Between V1 and V2.6

| Feature | V1 | V2.6 |
|---|---|---|
| Sample size (analysable) | 415 | 8,596 |
| Sampling | Manual, unsystematic | Complete ESU scrape |
| Classification | Manual | AI-assisted (Claude API) + validation |
| Groups | 2 (migrated / non-migrated) | 4 (+internal transfer + deported) |
| Validated error rate | Not assessed | 3.2% (n=82 reviewed) |
| Primary gap | +5.4 yrs | +3.93 yrs |
| Cox PH | Not performed | HR=0.759 [0.713, 0.809] |
| PSM | Not performed | +3.14 yrs [2.07, 4.21] |

The gap narrowing from V1 (+5.4 yrs) to V2.6 (+3.93 yrs) is expected, not a weakness. V1's small size and non-systematic sampling over-represented the most extreme cases. The present estimate is more conservative and more defensible precisely because it covers the full ESU population.

**Figure 3** shows the V1 vs V2 comparison with sample characteristics.

---

## 3. Data and Methods

### 3.1 Data Source

The Encyclopedia of Modern Ukraine (ESU; *Енциклопедія Сучасної України*, esu.com.ua) is the principal biographical reference for modern Ukrainian cultural and intellectual history, published under the auspices of the National Academy of Sciences of Ukraine. As of 2026 it covers approximately 70,000 entries spanning the 19th and 20th centuries, with particular depth in creative professions. Entries typically include birth date, birth location, death date (where applicable), death location, profession, and a biographical summary of several hundred to several thousand words.

A complete scrape of the ESU was performed in late 2025 (17,527 entries retrieved; 16,215 retained after deduplication and encoding normalisation). For the present analysis, we restrict attention to individuals with documented birth and death years.[^3]

### 3.2 Inclusion and Exclusion Criteria

**Included:** Any individual with (a) a recognised Ukrainian connection (birth, primary activity, or formative career in territory that became the Ukrainian SSR), (b) a creative profession (broadly defined: writer, poet, visual artist, musician, composer, theatre practitioner, filmmaker, architect, photographer, cultural organiser),[^1] (c) birth year ≥ 1840, and (d) documented death during or after the Soviet period (death year ≥ 1921).

**Excluded:**
- *Excluded pre-Soviet* (n=286): Died before 1921 — outside the Soviet-period study scope.
- *Excluded Galicia pre-annexation* (n=89): Active in Galicia before 1939 Soviet annexation; Galician institutions operated under Polish/Austro-Hungarian administration during most of these individuals' active careers.
- *Excluded non-Ukrainian* (n=7): Confirmed non-Ukrainians with no substantive Ukrainian connection (e.g., Gabriela Mistral, Pablo Neruda, Joseph Conrad — figures included in ESU for thematic comparative entries).
- *Excluded bad dates* (n=63): Conflicting or irreconcilable birth/death year records.
- *Still alive* (n=6,680): No death year recorded — treated as right-censored in the Cox supplementary analysis but excluded from the primary life-expectancy comparison.
- *Unknown* (n=197): Insufficient biographical information to classify migration status.

The CONSORT-style exclusion flowchart is shown in **Figure 16**.

### 3.3 Migration Classification Protocol

Each entry was classified by the Claude API using a two-step protocol:

**Step 1 — Check for forced displacement first.** The classifier checks for signals of deportation (NKVD arrest/exile, labour camp, special settlement), internal transfer (relocation within USSR under administrative pressure, career-motivated move between Soviet republics), or wartime displacement, before assigning a migration status.

**Step 2 — Assign status.** The classifier assigns one of: *migrated* (left Soviet-controlled territory[^2], ended life outside USSR/post-Soviet states), *non_migrated* (entire life and death within Ukrainian SSR or adjacent Soviet territory), *internal_transfer* (moved within USSR, did not exit Soviet control), *deported* (explicitly deported or arrested and exiled by Soviet security services), *unknown* (insufficient information).

Full classification prompts are documented in `AI_METHODOLOGY_LOG.md`.

### 3.4 Nationality Determination

Entries were flagged for non-Ukrainian review if their biographical text contained signals of non-Ukrainian national identity. A secondary Claude review confirmed or denied the flag. Confirmed non-Ukrainians were excluded. Zero entries in the four analysis groups carry a confirmed non-Ukrainian flag in V2.6.

### 3.5 Outcome Variable

The primary outcome is **age at death** (death_year − birth_year). This is a simplification (ignores month/day) but standard in historical demography when exact dates are unavailable. All four analysis groups are restricted to deceased individuals with both birth and death years documented.

### 3.6 AI Classification Validation

A stratified random validation sample of 200 entries was drawn (100 from INCLUDE groups, 100 from EXCLUDE categories). Eighty-two have been reviewed against full ESU biographical texts. The observed error rate is **3.2%** — approximately 2–3 classification errors per 100 entries, primarily near-boundary cases where emigration details were sparse. This rate is used in the sensitivity analysis (Section 4.13). The remaining 118 entries will be reviewed in V2.7.

### 3.7 Statistical Methods

**Descriptive statistics:** Mean, median, standard deviation, 95% CI (t-distribution) per group.

**Non-parametric tests:** Mann-Whitney U (two-sided) for pairwise comparisons, robust to non-normality.

**Effect sizes:** Cohen's d (pooled-variance standardised mean difference); Cliff's δ (non-parametric, range −1 to +1).

**Regression:** OLS with age at death as dependent variable. Model 1: migration status only. Model 2: adds birth decade, profession category, and birth region.

**Propensity Score Matching (PSM):** Nearest-neighbour matching on estimated propensity to migrate (logistic model, covariates: birth decade, profession, birth region). 1:1 matching; gap estimated from matched sample. Bootstrap CI (2,000 resamples).

**Cox Proportional Hazards:** Complete-case model (n=8,643; all event_observed=1). Adjusted model adds birth decade, profession, region. PH assumption tested via Schoenfeld residuals. Right-censored supplementary analysis adds living individuals (n=15,220 total).

**Time-varying landmark Cox (deportees):** Landmark analysis in age bands (20–30, 30–40, … 80–90) to characterise the time-varying hazard profile of the deported group, for whom the global PH assumption is violated.

---

## 4. Results

### 4.1 Sample Description

The complete ESU scrape yielded 16,215 entries. After applying inclusion/exclusion criteria, 8,596 deceased individuals with complete birth and death year data entered the analysis. **Figure 16** documents every exclusion step.

Group composition: migrated 1,328 (15.5%), non-migrated 5,962 (69.4%), internal transfer 1,111 (12.9%), deported 195 (2.3%). Gender data are complete for all 8,596 entries: 7,214 male (83.9%), 1,382 female (16.1%). Birth years range from 1840 to 1982; the majority was born between 1870 and 1940.

### 4.2 Primary Mortality Gap

**Figure 1** shows the primary result.

| Group | n | Mean age at death | Median | SD | 95% CI |
|---|---|---|---|---|---|
| Migrated | 1,328 | 75.37 | 77 | 13.89 | [74.62, 76.11] |
| Non-migrated | 5,962 | 71.44 | 73 | 13.61 | [71.10, 71.79] |
| Internal transfer | 1,111 | 71.09 | 73 | 13.61 | [70.29, 71.89] |
| Deported | 195 | 49.39 | 46 | 15.38 | [47.22, 51.57] |

Migrants lived an average of **3.93 years** longer than non-migrants (Cohen's d=0.287, p<0.001). **Figure 2** shows Kaplan-Meier survival curves; the migrated group separates from non-migrated at approximately age 40 and the gap widens through the main mortality period (ages 50–80).

### 4.3 Statistical Significance

| Comparison | Gap | Cohen's d | p-value |
|---|---|---|---|
| Migrated vs Non-migrated | +3.93 yrs | 0.287 | <0.001 |
| Migrated vs Deported | +25.97 yrs | 1.843 | <0.001 |
| Non-migrated vs Deported | +22.05 yrs | 1.613 | <0.001 |
| Non-migrated vs Internal transfer | +0.35 yrs | 0.026 | 0.269 (NS) |

All three comparisons involving the deported group reach extreme significance (p<0.001, d>1.6). The internal transfer comparison is the only null result — and by design, the most informative control.

### 4.4 Distribution Characteristics

**Figure 4** shows box plots and **Figure 6** violin plots for all four groups. The migrated and non-migrated distributions are broadly similar in shape, differing primarily in location. The deported distribution is dramatically different: bimodal, with the main mass concentrated at ages 35–55 (terror-period executions and labour camp deaths) and a secondary peak at ages 60–90 (survivors who reached normal ages). **Figure 15b** shows all four groups overlaid.

### 4.5 Profession Breakdown

The migrant advantage holds across all six profession categories (**Figure 11**, **Table 2**):

| Profession | Migrated LE | n | Non-mig LE | n | Gap |
|---|---|---|---|---|---|
| Writers/Poets | 74.4 | 391 | 70.5 | 1,755 | +3.9 |
| Visual Artists | 74.8 | 385 | 71.6 | 1,954 | +3.2 |
| Musicians/Composers | 75.7 | 310 | 71.4 | 916 | +4.3 |
| Theatre/Film | 75.5 | 64 | 71.8 | 731 | +3.7 |
| Architects | 79.0 | 61 | 73.2 | 384 | +5.8 |
| Other Creative | 77.7 | 117 | 73.3 | 222 | +4.4 |

Writers/Poets — the group most associated with the Executed Renaissance — show a gap (+4.4 yrs) consistent with the overall finding. The fact that the gap is not driven by a single profession rules out a simple "Writers were more likely to be murdered" confounding story.

### 4.6 The Deportee Finding in Detail

The deported group represents the study's most analytically important finding. Their mean age at death of 49.39 years — a 22.05-year deficit relative to non-migrants (Cohen's d=1.613) — is the direct demographic signature of Soviet political violence.

**Age structure.** The vast majority of deported workers were born between 1880 and 1910, placing them at ages 27–57 during the Great Terror (1934–38). **Figure 5** shows the distribution.

**Death year clustering.** **Figure 7b** shows deported workers' deaths clustering sharply in 1937–38. Sixty-seven of the 195 deported workers (34.4%) died in 1937 alone — the year of peak Stalinist terror. Their mean age at death in 1937 was 42.7 years. **Figure 8** shows the year-by-year breakdown.

**The 1937 spotlight.** The Sandarmokh massacres of November 1937 account for a substantial fraction of the 1937 deaths. Soviet security services executed hundreds of Ukrainian cultural figures in a matter of months during the Great Terror. The ESU captures many of these individuals through archival and memorial records, but — as Section 6.2 documents — many others are absent from the ESU entirely.

**Period breakdown for non-migrants.** **Table 3** and **Figure 9** show non-migrant deaths by historical period. Non-migrants who died during 1934–38 had a mean age at death of 55.5 years — 15.7 years below the overall non-migrant mean — reflecting the indirect mortality impact of the Terror period on those not formally deported.

**Table 3: Non-migrant deaths by period**

| Period | Deaths | Mean age at death | % of total |
|---|---|---|---|
| 1921–1929 (Early Soviet/NEP) | 97 | 58.8 | 1.6% |
| 1930–1933 (Holodomor/Purges) | 54 | 59.5 | 0.9% |
| 1934–1938 (Great Terror) | 96 | 55.8 | 1.6% |
| 1937 only (Terror peak) | 25 | 49.4 | 0.4% |
| 1939–1945 (WWII) | 207 | 55.1 | 3.5% |
| 1946–1953 (Late Stalin) | 124 | 62.6 | 2.1% |
| 1954–1964 (Khrushchev Thaw) | 236 | 66.6 | 4.0% |
| 1965–1991 (Stagnation/Late USSR) | 1,432 | 69.2 | 24.0% |
| Post-1991 | 3,716 | 74.7 | 62.3% |

The dominance of post-1991 deaths (62.3% of non-migrants) reflects the large cohort of Soviet-era workers who survived into Ukrainian independence. The non-migrant mean of 71.44 incorporates these long-lived survivors — meaning the observed gap is not an artefact of a depressed non-migrant mean; the non-migrant mean is itself elevated by post-Soviet longevity.

### 4.7 Birth Cohort Effects

**Figure 10** shows mean age at death by birth decade. The migrant advantage is present across virtually all cohorts from the 1860s through the 1920s, and is largest for the 1890–1920 birth cohorts — those who were in their prime creative years during the peak repression period of 1930–38.

**Figure 13** shows birth year distributions by group. The migrated cohort skews slightly earlier (more individuals born 1870–1910), consistent with the dominant Wave 1 (pre-1922 emigration) demographic.

### 4.8 Geographic Patterns

**Figure 12** shows migration rates and life expectancy by city of birth. Kyiv, Kharkiv, Odessa, and Lviv contribute the largest absolute numbers to both groups. Lviv shows a higher migration rate than eastern cities, consistent with greater exposure to westward flight routes and proximity to Habsburg emigration networks.

### 4.9 Gender Breakdown

**Figure 17** shows gender composition. Male workers dominate all groups (migrants: 84.8% male; deported: 95.6% male). **Figure 18** shows life expectancy by gender and group. Female migrants live notably longer than male migrants (78.1 vs 74.6 yrs). The migrant survival advantage holds for both genders.

### 4.10 Multivariable Regression

OLS regression of age at death (**Figure 23**, **Table OLS**):

| Variable | β (Model 1) | β (Model 2) | SE (M2) | p (M2) |
|---|---|---|---|---|
| Intercept (non-migrated) | 71.44 | — | — | — |
| Migrated | +3.929 | +3.333 | 0.446 | <0.001 |
| Internal transfer | −0.351 | −1.431 | 0.461 | 0.002 |
| Deported | −22.050 | −23.440 | 1.048 | <0.001 |

Model 2 (R²=0.077, F=55.23, p<0.001) includes birth decade, profession, and region controls. The migrated coefficient falls from +3.929 to +3.333, indicating that approximately 0.6 years of the raw gap is explained by observable selection covariates. The residual 3.3-year adjusted gap remains highly significant (p<0.001).

### 4.11 Propensity Score Matching

After 1:1 nearest-neighbour PSM on birth decade, profession, and birth region, the gap narrows to **+3.14 years** (bootstrap 95% CI: 2.07–4.21), a 22.3% attenuation from the unadjusted estimate. The PSM gap is substantially positive and statistically significant, confirming the migrant advantage cannot be explained by the measured selection covariates.

### 4.12 Cox Proportional Hazards

**Figure 24** shows the Cox forest plot. Adjusted model results (controlling for birth decade, profession, region):

| Group | HR | 95% CI | p |
|---|---|---|---|
| Migrated | 0.759 | [0.713, 0.809] | <0.001 |
| Internal transfer | 1.080 | [1.012, 1.152] | 0.021 |
| Deported | 5.396 | [4.642, 6.274] | <0.001 |

Migrants had approximately a 24% lower instantaneous mortality risk at any given age. Deported workers had more than 5 times the mortality hazard. The internal transfer HR (1.08) is marginally elevated but much smaller — consistent with the null result in the mean comparison.

**Right-censored supplementary analysis** (N=15,220 including right-censored living individuals): Migrated HR=1.334 (95% CI: 1.251–1.422). The reversal relative to the complete-case model reflects the censoring imbalance: ~52% of non-migrants are right-censored while essentially all migrants are deceased. The complete-case model (HR=0.759) is the primary result. **Figures 25–26** document the censoring structure.

### 4.13 Sensitivity Analyses

**Figure 14** shows the gap as a function of AI error rate. The finding remains positive up to approximately 8% error. Our validated rate (3.2%) is well within the safe margin.

**Figure 27** summarises three additional scenarios:

- **Scenario A** (duration assumption for right-censored): Varying assumed death age of living workers from 70–90 does not qualitatively change results. Migrated HR ranges 1.067–1.100 across all scenarios.

- **Scenario B** (post-1991 emigrant handling): Including vs. excluding vs. reclassifying 62 post-Soviet emigrants leaves migrated HR essentially unchanged (1.088–1.094).

- **Scenario C** (bootstrap misclassification): At 10% error rate (three times the validated rate), median bootstrapped migrated HR is 1.077 (95% percentile interval: 1.048–1.110). The finding persists.

### 4.14 Time-Varying Analysis (Deportees)

The PH assumption is violated for the deported group (Schoenfeld residual test p=0.0), requiring a time-varying approach. Landmark Cox analysis shows:

| Age band | n at risk | Deported events | HR | p |
|---|---|---|---|---|
| 20–30 | 15,046 | 10 | 1.10 | 0.348 (NS) |
| 30–40 | 14,969 | 40 | 1.51 | <0.001 |
| 40–50 | 14,665 | 48 | **1.89** | <0.001 |
| 50–60 | 13,786 | 26 | 1.61 | 0.001 |
| 60–70 | 12,051 | 19 | 1.50 | 0.018 |
| 70–80 | 8,546 | 11 | 1.21 | 0.361 (NS) |
| 80–90 | 4,035 | 5 | 0.95 | 0.859 (NS) |

**Peak HR=1.89 at age 40–50** — the Terror-period execution window. By ages 70–80, deportee survivors show mortality hazard indistinguishable from non-migrants, consistent with a survivor selection effect (those who survived the terror and camp system tended to be unusually resilient). **Figures 28–28b** show the time-varying profile and Schoenfeld residuals.

### 4.15 Contextual Comparisons

**Figure 19** overlays ESU group means on Ukrainian SSR general population life expectancy data (Meslé & Vallin 2003; UN WPP 2022). The non-migrant creative workers (mean 71.44 yrs) perform slightly above the Soviet-era general population baseline — consistent with the ESU's educated elite bias. The migrant 3.93-year advantage above this already-elevated baseline is not explained by socioeconomic class effects alone. **Figures 20–22** provide additional contextual comparisons.

---

## 5. Discussion

### 5.1 What This Data Establishes With Confidence

**The deportee finding is the strongest causal signal.** The 22.05-year mortality deficit (Cohen's d=1.613) is a large effect by any standard in social science. The mechanism is direct and historically documented: deportation meant arrest, brutal transit, labour camp confinement, summary execution, or death in special settlements. The ESU biographical texts for deported individuals frequently state "arrested," "shot," or "died in camp." This is not an inferred effect — it is the direct mortality signature of state-organised violence.

**The internal transfer null result is the crucial control.** Non-migrated and internally transferred workers have essentially identical life expectancies (+0.35 yrs, p=0.269). Geographic movement within the Soviet system — even movement that displaced workers from their home republic — did not confer the survival advantage seen among those who exited Soviet control entirely. The migrant advantage is specifically associated with exiting the Soviet political system, not merely moving elsewhere.

**Consistency across cohorts and professions argues against a simple compositional explanation.** The regression-adjusted gap (3.3 yrs) and PSM gap (3.1 yrs) show that after controlling for birth cohort, profession, and region, a substantial gap remains. The gap holds in every profession category tested (Table 2). This pattern is inconsistent with a story where the gap is entirely explained by one or two professions or cohorts being differently represented in the migrated group.

### 5.2 The Migration Gap: Association, Not Causation

We do not claim that emigration *caused* longer life in the sense of a clean experimental treatment. Migration was not random. Workers who emigrated may have differed from those who stayed in ways we cannot fully observe: health at the time of emigration, political connections, language skills, family circumstances, and sheer timing luck (the window for emigration closed for most workers by the mid-1950s). PSM controls for measured covariates; unmeasured confounders remain.

**Galician survival selection.** Workers from Galicia (Western Ukraine, under Polish/Austrian rule until 1939) were geographically positioned to emigrate westward more easily and had pre-existing North American diaspora networks. They also experienced Soviet control later — their exposure to the worst Stalinist terror years was shorter. Some of the observed advantage may reflect this different exposure history rather than emigration per se.

**Healthy migrant effect.** Workers who survived the emigration journey — often under wartime conditions — were already selected for physical resilience. This selection bias would inflate the observed migrant LE. We cannot fully disentangle this.

**Post-Soviet non-migrant composition.** 61.5% of non-migrant deaths occurred after 1991. The non-migrant mean is elevated by a large cohort of workers who lived long into Ukrainian independence. This makes the observed gap conservative: restricting to Soviet-period deaths only would show a larger gap.

Despite these caveats, the consistency of the gap across cohorts, professions, and genders — and its persistence through PSM — provides reasonable confidence that the observed association reflects a real mortality differential, partly caused by the genuine survival consequences of exiting Soviet control.

### 5.3 Historical Interpretation

The 1890–1920 birth cohorts show the largest migrant/non-migrant gap. These individuals were in their 30s and 40s — peak productive and politically vulnerable ages — during the Great Terror (1937–38) and the wartime period (1941–45). For these cohorts, the decision or opportunity to emigrate was, in many documented cases, literally life or death.

The 1937 death concentration among deportees (67 of 195 died in 1937, mean age 42.7) reflects the Sandarmokh massacres and the broader Great Terror, when Soviet security services executed thousands of Ukrainian cultural figures in months. This is not a statistical artefact — it is the ESU's partial capture of a historically documented event.

The late-cohort analysis also reveals convergence: workers born after 1940 show much smaller or reversed gaps, consistent with the post-Stalinist easing of direct violence against intellectuals. The conditions producing the large mortality differential were specific to the Stalinist period.

### 5.4 Comparison to Prior Research

The V2.6 gap (+3.93 yrs) is smaller than V1's (+5.4 yrs). As discussed in Section 2.3, this narrowing is expected given improved sampling methodology. The V2.6 estimate is derived from the full ESU population with a validated error rate and should be treated as more reliable than V1.

---

## 6. Limitations

### 6.1 Data Source: ESU Coverage Bias

The ESU disproportionately covers culturally prominent individuals. Workers who were arrested, killed, and whose work was suppressed may have smaller or absent entries. This bias is asymmetric: the most severely repressed workers (in the non-migrated and deported groups) are most likely to be missing. Current estimates are therefore **conservative lower bounds** on the true mortality differential.

### 6.2 Missing Repressed Workers

**Figure 30** quantifies the missing-worker bias. Eight individuals confirmed to meet study inclusion criteria are absent from the ESU: Vasyl Stus (died Perm-36, age 47), Mykola Khvylovy (suicide, age 39), Mykola Zerov (shot Sandarmokh, age 47), Les Kurbas (shot Sandarmokh, age 50), Mykola Kulish (shot Sandarmokh, age 47), Oles Dosvitniy (shot, age 42), Mykola Boychuk (shot, age 52), Hnat Mykhailychenko (shot, age 26). Their mean age at death is 39.0 years — 32 years below the non-migrant mean.

Adding these 8 confirmed missing workers adjusts the gap to approximately 4.10 years. Adding 50 plausible missing workers at a conservative assumed mean of 38 years adjusts it to 4.33 years. Under no plausible scenario does adding missing repressed workers *narrow* the gap.

### 6.3 Classification Quality

The validated AI error rate is 3.2% (n=82 reviewed). The sensitivity analysis confirms the finding holds to approximately 8% error. The full 200-entry validation will be completed in V2.7.

### 6.4 Observational Design

This is an observational study. Causal inference is limited by self-selection into migration, unmeasured confounders, and the impossibility of a counterfactual. PSM partially addresses measured confounders; unmeasured ones cannot be controlled with available data.

### 6.5 Post-Soviet Composition

61% of non-migrant deaths occurred after 1991. The gap captures lifetime exposure — not purely Soviet-period exposure. This is appropriate for a lifespan study but means the gap cannot be read as reflecting Soviet-period mortality differentials alone.

### 6.6 Galician Survival Selection

Workers from Galicia had earlier and easier access to emigration routes and experienced Soviet rule only from 1939. Their inclusion in the "migrated" category means some of the observed advantage may reflect different exposure history rather than emigration per se. This cannot be fully disentangled without emigration-date data.

### 6.7 Wave Disaggregation Deferred to V3

An early analysis (Stage 9) attempted to disaggregate migrants by emigration wave (pre-1922, 1939–45, 1946–91). The classifier proved unreliable: it recovered birth and death years from biographical text rather than actual emigration dates, leading to spurious wave assignments. This analysis was retracted. Wave disaggregation is a V3 priority, requiring explicit emigration date fields.

### 6.8 Living Cohort Assumptions (Right-Censored Cox)

The right-censored supplementary Cox analysis treats living individuals as censored at 2026. This introduces bias because living individuals are concentrated in the non-migrated group. The complete-case Cox (HR=0.759) is the primary model.

---

## 7. Conclusion

This study provides systematic quantitative evidence that Ukrainian creative workers who emigrated from Soviet-controlled Ukraine lived measurably longer than those who remained. The primary gap of **3.93 years** (75.37 yrs vs 71.44 yrs; Cohen's d=0.287; p<0.001) persists after controlling for birth cohort, profession, and region, and is robust to classification error rates well above the validated 3.2%.

The finding that matters most is not the 3.93-year gap but the **22.05-year deficit of deported workers** (mean age 49.39 yrs; Cohen's d=1.613). This is not a statistical inference about systemic disadvantage — it is the direct mortality signature of state-organised violence, concentrated in 1937, documented in biographical text. Soviet repression of Ukrainian culture was, among other things, a demographic catastrophe for a professional class.

The **internal transfer null result** (+0.35 yrs, p=0.269) is as informative as the positive findings: workers who moved within the Soviet system lived essentially the same lifespan as those who stayed. The advantage was specifically associated with exit from Soviet control, not merely geographic movement.

The current dataset provides a conservative lower bound. Adding the confirmed missing figures only widens the gap. The most severely repressed workers are the least likely to appear in the ESU — meaning the true mortality differential is larger than the 3.93 years observed here.

Future priorities for V2.7 and V3: (1) complete the 200-entry validation; (2) collect explicit emigration dates to enable reliable wave disaggregation; (3) extend the analysis to non-creative professional categories; (4) develop a method to estimate the number and characteristics of ESU-absent repressed workers.

---

## 8. Figure Index

**Figure 1** — *Primary life expectancy comparison.* Bar chart showing mean age at death ± 95% CI for all four groups. The 3.93-year migrant advantage and 22.05-year deportee deficit are the primary results.

**Figure 2** — *Kaplan-Meier survival curves.* Survival probability as a function of age for all four groups. Migrated workers maintain systematically higher survival probability from approximately age 40 onward.

**Figure 3** — *V1 vs V2 comparison.* Side-by-side comparison of V1 (n=415) and V2.6 (n=8,596) gap estimates, showing gap narrowing due to improved sampling methodology.

**Figure 4** — *Box plots by group.* IQR, median, and outlier distribution for all four groups. Shows the bimodal character of the deported distribution.

**Figure 5** — *Age at deportation histogram.* Distribution of birth years for the deported group, illustrating concentration in the 1880–1910 birth cohorts (ages 27–57 during the Terror).

**Figure 6** — *Violin plots.* Full distribution shape for all four groups, combining box plot summary with kernel density estimation.

**Figure 7** — *Death year histogram.* Distribution of death years for migrated and non-migrated groups, showing the temporal structure of deaths over the 20th century.

**Figure 7b** — *Deported death year histogram.* Death year distribution for the deported group, with the extreme 1937 concentration clearly visible.

**Figure 8** — *Deported deaths by year.* Year-by-year count of deported worker deaths 1930–1960, with 1937 as the peak year.

**Figure 9** — *Non-migrant deaths by period.* Non-migrant deaths organised by historical period, with mean age at death per period. Shows how Soviet-era period mortality differs from post-1991 mortality within the non-migrant group.

**Figure 10** — *Birth cohort life expectancy.* Mean age at death by birth decade for migrants and non-migrants. Shows that the gap is largest for 1890–1920 birth cohorts.

**Figure 11** — *Profession grouped bar chart.* Life expectancy by profession category for migrants and non-migrants. Confirms the gap holds across all six profession groups.

**Figure 12** — *Geographic migration rates.* Migration rates and life expectancy by city of birth. Shows geographic variation in the analysable population.

**Figure 13** — *Birth year distribution by group.* Histogram showing birth year composition of each analysis group.

**Figure 14** — *Sensitivity analysis (AI error rate).* Gap estimate as a function of assumed AI classification error rate (0–20%), with the validated 3.2% rate marked. Finding remains positive up to approximately 8% error.

**Figure 15** — *Internal transfer null result.* Detailed comparison of internal transfer and non-migrated groups, illustrating the near-zero gap and its role as a within-Soviet control condition.

**Figure 15b** — *All-groups life expectancy box.* All four groups overlaid in a single box/distribution plot for direct visual comparison.

**Figure 16** — *CONSORT exclusion flowchart.* Complete documentation of the exclusion pipeline from 16,215 scraped entries to 8,596 analysable entries, including all exclusion categories and counts.

**Figure 17** — *Gender by group.* Gender composition of each analysis group as a proportion chart.

**Figure 18** — *Life expectancy by gender and group.* Mean age at death broken down by both migration group and gender.

**Figure 19** — *Soviet-era population context.* ESU group means overlaid on Ukrainian SSR general population life expectancy estimates (Meslé & Vallin 2003; UN WPP 2022). Contextualises findings against period life expectancy.

**Figure 19b** — *Simplified death rate comparison.* Alternative contextualisation using crude death rates.

**Figure 20** — *Two-group conservative comparison.* Restricted analysis using only unambiguously classified migrants and non-migrants, as an additional robustness check.

**Figure 21** — *Soviet republic comparisons.* ESU estimates compared to published period life expectancy data for other Soviet republics.

**Figure 22** — *Educated-urban baseline comparison.* Comparison to educated-urban baseline life expectancy from other Eastern European historical contexts.

**Figure 23** — *Regression coefficient plot.* Forest plot of OLS regression coefficients for all variables in Model 2, including birth decade, profession, and region controls.

**Figure 24** — *Cox proportional hazards forest plot.* Hazard ratios and 95% CIs for all four groups from the adjusted Cox model. Migrants HR=0.759; deported HR=5.40.

**Figure 25** — *Censoring pattern.* Visualisation of the censoring structure in the right-censored supplementary analysis, showing the ~52% censoring rate in the non-migrated group.

**Figure 26** — *Kaplan-Meier with censoring marks.* KM survival curves from the right-censored analysis with tick marks at censoring events.

**Figure 27** — *Sensitivity analysis summary.* Multi-panel summary of Scenarios A (duration assumption), B (post-Soviet emigrant handling), and C (bootstrap misclassification).

**Figure 28** — *Deported hazard ratio by age band.* Time-varying (landmark) Cox analysis of the deported group across age bands 20–90. Shows peak HR=1.89 at age 40–50 and convergence toward 1.0 at older ages.

**Figure 28b** — *Schoenfeld residuals (smoothed).* Smoothed Schoenfeld residual plot for the deported group, confirming the time-varying hazard and the PH violation.

**Figure 30** — *Missing-worker sensitivity analysis.* Estimated gap as a function of the number of missing repressed workers (M) and their assumed mean age at death (Ā). Under all plausible assumptions, adding missing repressed workers widens rather than narrows the gap.

---

## 9. AI Methodology Note

Classification of 16,215 entries was performed using the Anthropic Claude API. Primary classification used claude-sonnet-4-6 with a structured two-step protocol (check for forced displacement first; then classify). Re-classification of API-error entries in Stage 12 used claude-haiku-4-5-20251001.

A validation sample of 200 entries (stratified: 100 INCLUDE, 100 EXCLUDE) was drawn from the full dataset. 82 entries have been reviewed against full ESU biographical texts as of V2.6, yielding an observed error rate of 3.2%. The 118 remaining validation entries will be reviewed in V2.7.

**V2.6 database corrections (Stage 12):**
- 8 hardcoded patches for validation-identified errors
- 97 birth-year-as-death-year corrections (ESU scraper stored birth year in death_year field when only one year appeared in the notes)
- 57 API-error classification retries (entries with billing error messages instead of real reasoning)

Full classification prompts, model versions, and per-entry reasoning are stored in the `migration_reasoning` column of `esu_creative_workers_v2_6.csv`. Methodology documentation: `AI_METHODOLOGY_LOG.md`. All scripts: `ukraine_v2/` directory.

---

## 10. Bibliography

Applebaum, A. (2003). *Gulag: A History*. Doubleday.

Conquest, R. (1968). *The Great Terror: Stalin's Purge of the Thirties*. Macmillan.

Grabowicz, G. G. (1982). The Ukrainian Literary Revival: Toward a New Understanding. *Harvard Ukrainian Studies*, 6(2), 209–260.

Hrytsak, Y. (2011). *Strasti za natsionalizmom* [Passions for Nationalism]. Krytyka.

Human Mortality Database (2024). University of California, Berkeley, and Max Planck Institute for Demographic Research. www.mortality.org.

Klid, B., & Motyl, A. J. (Eds.). (2012). *The Holodomor Reader: A Sourcebook on the Famine of 1932–1933 in Ukraine*. Canadian Institute of Ukrainian Studies Press.

Meslé, F., & Vallin, J. (2003). Mortality in Eastern Europe and the Former Soviet Union: Long-term trends and recent upturns. *Demographic Research*, Special Collection 2, 45–70.

Motyl, A. J. (2010). *The Turn to the Right: The Ideological Origins and Development of Ukrainian Nationalism, 1919–1929*. East European Monographs.

Shkandrij, M. (2010). *In the Maelstrom: The Artef, Ukrainian Modernism, and Soviet Cultural Policy, 1917–1932*. University of Toronto Press.

Subtelny, O. (2000). *Ukraine: A History* (3rd ed.). University of Toronto Press.

United Nations Population Division. (2022). *World Population Prospects 2022 Revision*. United Nations.

Yekelchyk, S. (2007). *Ukraine: Birth of a Modern Nation*. Oxford University Press.

---

*Full replication data and analysis scripts: github.com/symkinmark/ukraine-creative-workers*

[^1]: "Creative workers" follows ESU's own categorical scope: writers, poets, visual artists, sculptors, architects, musicians, composers, conductors, theatre directors, performers, filmmakers, photographers, and cultural organisers. Scientists and scholars are included where their primary public identity was cultural (e.g., a literary scholar who was also a practising poet).

[^2]: "Soviet-controlled territory" is defined as territory under effective Soviet administration: the Ukrainian SSR (from 1922), Eastern Galicia (from 1939), and Transcarpathia (from 1945). Workers who emigrated before Soviet annexation of their home territory are classified as migrated if they never returned and their subsequent life was conducted outside Soviet jurisdiction.

[^3]: The ESU scrape was conducted in two phases: a full-site crawl in November 2025 (17,527 entries) and a targeted re-scrape of specific entries requiring corrected date parsing in February 2026 (Stage 12).
