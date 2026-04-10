# Observed Age at Death Among Ukrainian Creative Workers Under Soviet Occupation: A Quantitative Study Using the Encyclopedia of Modern Ukraine

**Mark Symkin** | Independent Researcher | 2026

**Version:** V3.0 (Dataset: esu_creative_workers_v2_6.csv | N=8,590 analysable | All 177 numeric checks verified)

---

## Abstract

This study examines whether Ukrainian creative workers who emigrated from Soviet-controlled Ukraine lived longer than those who remained, using biographical data from the Encyclopedia of Modern Ukraine (ESU). The dataset covers 16,215 entries scraped from esu.com.ua, of which 8,590 deceased individuals with complete birth and death years form the analysable cohort. Workers are classified into four groups: *migrated* (left Soviet territory permanently; n=1,324), *non-migrated* (remained in Soviet Ukraine; n=5,960), *internal transfer* (moved within the USSR; n=1,111), and *deported* (forcibly relocated by the Soviet state; n=195).

Migrants died on average **3.98 years** later than non-migrants (75.42 yrs vs 71.44 yrs; Cohen's d=0.292; Cliff's δ=0.18; p<0.001). This gap persists across birth cohorts, professions, and genders, and survives propensity-score matching (3.43 yrs; 95% CI: 2.38–4.51). The primary finding is robust to a 10% AI classification error rate.

The strongest signal is among deported workers, who died 22.05 years earlier than non-migrants (mean age 49.39 yrs; Cohen's d=1.613; p<0.001), with peak excess mortality at ages 40–50 (time-varying Cox hazard ratio: 1.86). The internal transfer group shows no significant difference from non-migrants (+0.35 yrs, p=0.271), functioning as a within-Soviet control condition. This null result supports the interpretation that geographic movement per se does not explain the migrant advantage — only exit from Soviet control does.

Cox proportional hazards modelling yields an adjusted hazard ratio of 0.778 (95% CI: 0.731–0.828) for migrants relative to non-migrants, meaning migrants had approximately 22% lower instantaneous mortality risk at any given age. AI classification quality was validated against a complete 200-entry stratified review, confirming an error rate of 3.2%. The ESU's known coverage bias (favouring culturally prominent figures) means the current 3.98-year estimate is a conservative lower bound.

---

## 1. Introduction

### 1.1 Soviet Cultural Policy and the Executed Renaissance

The Soviet occupation of Ukraine — conventionally dated from the consolidation of Bolshevik control in 1920 through Ukrainian independence in 1991 — was characterised by systematic state violence against Ukrainian cultural and intellectual life. Policies of Russification, enforced collectivisation, mass executions, forced labour, and ideological surveillance were not applied uniformly across Soviet society but were deployed with particular intensity against groups whose work produced and transmitted national identity: writers, poets, visual artists, composers, theatre directors, architects, and other creative workers.

The period known in Ukrainian historiography as the "Executed Renaissance" (*Розстріляне Відродження*, *Rozstriliane Vidrodzhennia*) — roughly 1917 to 1941 — saw the near-total physical destruction of an entire generation of Ukrainian cultural figures. Scholars and artists including Mykola Zerov, Mykhailo Khvylovy, Les Kurbas, Valerian Pidmohylny, and hundreds of others were arrested, tortured, imprisoned in the Gulag system, or executed outright during the Stalinist terror campaigns of the 1930s. The Great Terror of 1937–1938 was particularly lethal: Ukrainian cultural workers were disproportionately targeted as potential vectors of "bourgeois nationalism." Dozens were shot at Sandarmokh in 1937 alone. Survivors of these purge cohorts faced ongoing surveillance, forced recantations, and the permanent threat of rearrest.

Against this backdrop, emigration was not merely an economic or personal choice — for many Ukrainian creative workers, it was the difference between survival and destruction. Those who managed to leave — primarily through displacement during the First World War (Wave 1: pre-1922), wartime evacuation (Wave 2: 1939–45), or post-war displacement (Wave 3: 1946–91) — ended up in diaspora communities in Western Europe, North America, and Australia. Those who stayed faced a fundamentally different risk environment.

### 1.2 The Gap in Scholarship

Quantitative study of this mortality toll has been limited. Historical demography of Soviet persecution has relied heavily on archival records — many still restricted or destroyed — and has focused more on aggregate victim counts than on comparative life expectancy across survivor groups. Qualitative accounts of Soviet cultural repression are extensive and well-documented (Snyder 2010; Applebaum 2003; Conquest 1968; Grabowicz 1982; Shkandrij 2010), but almost no systematic quantitative evidence exists for the demographic consequences of Soviet cultural policy at the level of an entire professional class.

The question is tractable: the Encyclopedia of Modern Ukraine (ESU) provides biographical data for thousands of creative workers, including birth and death years for the vast majority. If the mortality gap is large and robust, it constitutes quantitative corroboration of what historians have documented through archival and testimonial evidence — not merely for individual victims, but for an entire professional class. The data exist almost nowhere else in this form: no other systematic biographical compendium covers Ukrainian creative workers across the full Soviet period with comparable depth.

### 1.3 Research Question and Study Scope

The central research question of this study is: **Did Ukrainian creative workers who emigrated from Soviet-controlled territory live measurably longer than those who remained?**

This is not a study of happiness, artistic output, or political freedom — it is a study of survival, measured in years of life. We use age at death as a single quantifiable outcome that collapses complex processes (physical safety, political persecution, access to nutrition and medical care, psychological stress, occupational disruption) into a single observable variable.

### 1.4 Political Sensitivity and Ethical Considerations

We approach this question with awareness of its political sensitivity. The quantification of repression is not a neutral exercise. Numbers, however carefully produced, risk obscuring the individual human realities they aggregate — the lives cut short, the works that were never written, the families destroyed. We proceed because we believe that quantitative evidence, when honestly presented alongside its limitations, can complement the archival and testimonial record. We make no causal claims that cannot be substantiated by the data. We acknowledge the significant selection effects inherent in emigration. And we situate our quantitative findings within the documented historical record of Soviet policy toward Ukrainian cultural workers, rather than treating the numbers as speaking for themselves.

### 1.5 Paper Organisation

The paper is organised as follows. Section 2 describes the prior study and the present expansion. Section 3 details data sources, inclusion criteria, and methods. Section 4 presents the core mortality findings. Section 5 examines patterns across professions, cohorts, genders, geography, and historical periods. Section 6 documents statistical robustness. Section 7 discusses findings and their historical interpretation. Section 8 documents limitations. Section 9 concludes.

---

## 2. Prior Study and Present Expansion

### 2.1 Prior Study (V1, n=415)

A prior version of this study (V1, 2025) examined a sample of 415 Ukrainian creative workers drawn from the ESU, classified manually into migrated and non-migrated groups. That study found a gap of approximately 9 years (migrants 72 yrs vs non-migrants 63 yrs). The V1 analysis applied a pre-1991 death cutoff — excluding all workers who died after the dissolution of the Soviet Union — which systematically removed the longest-lived non-migrants and inflated the gap. The V1 sample was also not systematically sampled and leaned heavily toward writers from the Executed Renaissance cohort — precisely the group most likely to have been killed young in the non-migrated category.

### 2.2 Present Study (V3.0, n=8,590)

The present study uses a complete scrape of the ESU — all 16,215 entries in the database as of early 2026 — combined with AI-assisted classification via the Claude API (Anthropic). Classification was performed using a structured two-step protocol that checks for forced displacement signals first (to correctly identify deportees and internal transfers), then assigns migration status. The full ESU scrape covers writers, visual artists, musicians, theatre figures, architects, photographers, and other creative professionals across the full Soviet period. It is not a curated sample.

V3.0 incorporates a systematic five-stage database quality pipeline:

- **Stage 12** (B1–B5): 8 hardcoded validation patches; 97 birth-year-as-death-year scraping corrections; 57 API-credit-error classification retries; non-Ukrainian audit; residual unknown resolution.
- **Stage 13**: Application of corrections from the first 82-entry manual validation review.
- **Stage 14**: Re-classification of 135 entries that had failed during Stage 12 due to API authentication errors, using claude-haiku-4-5 with live bio fetches.
- **Stage 15**: Application of 6 corrections identified during the Stage 14 manual review (3 Galicia pre-annexation reclassifications, 1 bad-dates exclusion, 1 pre-Soviet exclusion, 1 non-Ukrainian exclusion).

### 2.3 Key Differences Between V1 and V3.0

| Feature | V1 | V3.0 |
|---|---|---|
| Sample size (analysable) | 415 | 8,590 |
| Sampling | Manual, unsystematic | Complete ESU scrape |
| Classification | Manual | AI-assisted (Claude API) + validation |
| Groups | 2 (migrated / non-migrated) | 4 (+internal transfer + deported) |
| Validated error rate | Not assessed | 3.2% (n=200 reviewed; complete) |
| Primary gap | +9.0 yrs (with pre-1991 cutoff) | +3.98 yrs (no cutoff) |
| Cox PH | Not performed | HR=0.778 [0.731, 0.828] |
| PSM | Not performed | +3.43 yrs [2.38, 4.51] |

The gap narrowing from V1 (+9.0 yrs) to V3.0 (+3.98 yrs) is expected, not a weakness. V1's pre-1991 death cutoff excluded long-lived non-migrants who survived into Ukrainian independence, artificially depressing the non-migrant mean. V1's small size and non-systematic sampling also over-represented the most extreme cases. The present estimate is more conservative and more defensible precisely because it includes all post-Soviet deaths and covers the full ESU population with a validated error rate.

**Figure 3** shows the V1 vs V3 comparison.

---

## 3. Data and Methods

### 3.1 Data Source

The Encyclopedia of Modern Ukraine (ESU; *Енциклопедія Сучасної України*, esu.com.ua) is the principal biographical reference for modern Ukrainian cultural and intellectual history, published under the auspices of the National Academy of Sciences of Ukraine. As of 2026 it covers approximately 70,000 entries spanning the 19th and 20th centuries, with particular depth in creative professions. Entries typically include birth date, birth location, death date (where applicable), death location, profession, and a biographical summary of several hundred to several thousand words.

A complete scrape of the ESU was performed in late 2025 (17,527 entries retrieved; 16,215 retained after deduplication and encoding normalisation). For the primary analysis, we restrict attention to individuals with documented birth and death years.[^3]

### 3.2 Inclusion and Exclusion Criteria

**Included:** Any individual with (a) a recognised Ukrainian connection (birth, primary activity, or formative career in territory that became the Ukrainian SSR), (b) a creative profession (broadly defined: writer, poet, visual artist, musician, composer, theatre practitioner, filmmaker, architect, photographer, cultural organiser),[^1] (c) birth year ≥ 1840, and (d) documented death during or after the Soviet period (death year ≥ 1921).

**Excluded:**
- *Excluded pre-Soviet* (n=490): Died before 1921 — outside the Soviet-period study scope.
- *Excluded Galicia pre-annexation* (n=91): Active in Galicia before 1939 Soviet annexation; Galician institutions operated under Polish/Austro-Hungarian administration during most of these individuals' active careers. Soviet demographic conditions did not apply.
- *Excluded non-Ukrainian* (n=23): Confirmed non-Ukrainians with no substantive Ukrainian connection (e.g., Gabriela Mistral, Joseph Conrad, Charles Martin Loeffler — figures included in the ESU for comparative biographical entries).
- *Excluded bad dates* (n=74): Conflicting or irreconcilable birth/death year records.
- *Still alive* (n=6,680): No death year recorded — treated as right-censored in the Cox supplementary analysis but excluded from the primary mean-age-at-death comparison.
- *Unknown* (n=61): Insufficient biographical information to classify migration status despite full bio review.
- *Missing dates* (n=206): Migration status assigned but birth or death year not documented in ESU entry.

The CONSORT-style exclusion flowchart is shown in Figure 4.

### 3.3 Migration Classification Protocol

Each entry was classified by the Claude API using a two-step protocol:

**Step 1 — Check for forced displacement first.** The classifier checks for explicit signals of deportation (NKVD arrest/exile, labour camp, special settlement order), internal transfer (relocation within USSR under administrative or career pressure, without exit from Soviet jurisdiction), or wartime displacement, before assigning a migration status.

**Step 2 — Assign status.** The classifier assigns one of: *migrated* (left Soviet-controlled territory[^2], ended life outside USSR/post-Soviet states), *non_migrated* (entire life and death within Ukrainian SSR or adjacent Soviet territory), *internal_transfer* (moved within USSR, did not exit Soviet control), *deported* (explicitly deported or arrested and exiled by Soviet security services), *unknown* (insufficient information after full bio review).

Full classification prompts and model version history are documented in `AI_METHODOLOGY_LOG.md`.

### 3.4 Nationality Determination

Entries were flagged for non-Ukrainian review if their biographical text contained signals of non-Ukrainian national identity. A secondary Claude review confirmed or denied the flag. Confirmed non-Ukrainians were excluded from all analysis groups. Zero entries in the four analysis groups carry a confirmed non-Ukrainian flag in V3.0.

### 3.5 Outcome Variable

The primary outcome is **age at death** (death_year − birth_year). This is a simplification (ignores month/day) but standard in historical demography when exact dates are unavailable. All four analysis groups are restricted to deceased individuals with both birth and death years documented.

### 3.6 AI Classification Validation

A stratified random validation sample of 200 entries was drawn (100 from INCLUDE groups, 100 from EXCLUDE categories). All 200 entries were reviewed against full ESU biographical texts, completing the validation in V3.0. The observed error rate is **3.2%** — approximately 3 classification errors per 100 entries, primarily near-boundary cases where emigration details were sparse or the person lived in Galicia with ambiguous Soviet-era status. This rate is used in the sensitivity analysis (Section 6.5).

### 3.7 Statistical Methods

**Descriptive statistics:** Mean, median, standard deviation, 95% CI (t-distribution) per group.

**Non-parametric tests:** Mann-Whitney U (two-sided) for pairwise comparisons, robust to non-normality.

**Effect sizes:** Cohen's d (pooled-variance standardised mean difference — values of 0.2, 0.5, and 0.8 correspond to small, medium, and large effects respectively); Cliff's δ (non-parametric ordinal effect size, range −1 to +1).

**Regression:** OLS with age at death as dependent variable. Model 1: migration status only. Model 2: adds birth decade, profession category, and birth region.

**Propensity Score Matching (PSM):** Nearest-neighbour matching on estimated propensity to migrate (logistic model, covariates: birth decade, profession, birth region). 1:1 matching; gap estimated from matched sample. Bootstrap CI (2,000 resamples).

**Cox Proportional Hazards:** Complete-case model (n=8,590; all event_observed=1). Adjusted model adds birth decade, profession, region. PH assumption tested via Schoenfeld residuals. Right-censored supplementary analysis adds living individuals (n=15,220 total). A hazard ratio (HR) below 1.0 indicates lower mortality risk; above 1.0 indicates higher risk.

**Time-varying landmark Cox (deportees):** Landmark analysis in age bands (20–30, 30–40, … 80–90) to characterise the time-varying hazard profile of the deported group, for whom the global PH assumption is violated.

Full regression tables and alternative model specifications are provided in Appendix B.

---

## 4. The Mortality Gap

### 4.1 Migrants Lived 3.98 Years Longer

The complete ESU scrape yielded 16,215 entries. After applying inclusion/exclusion criteria (see §3.2), 8,590 deceased individuals with complete birth and death year data entered the analysis. Group composition: migrated 1,324 (15.4%), non-migrated 5,960 (69.4%), internal transfer 1,111 (12.9%), deported 195 (2.3%). Gender: 7,195 male (84.1%), 1,358 female (15.9%), 37 unknown (0.4%). Birth years range from 1840 to 1982; the majority were born between 1870 and 1940.

**Figure 1** shows the primary result.

**Table 1: Age at death by migration group**

| Group | n | Mean age at death | Median | SD | 95% CI |
|---|---|---|---|---|---|
| Migrated | 1,324 | 75.42 | 77 | 13.84 | [74.68, 76.17] |
| Non-migrated | 5,960 | 71.44 | 73 | 13.61 | [71.10, 71.79] |
| Internal transfer | 1,111 | 71.09 | 73 | 13.61 | [70.29, 71.89] |
| Deported | 195 | 49.39 | 46 | 15.38 | [47.22, 51.57] |

Migrants lived an average of **3.98 years** longer than non-migrants (Cohen's d=0.292; Cliff's δ=0.18; p<0.001). **Figure 2** shows Kaplan-Meier survival curves; the migrated group separates from non-migrated at approximately age 40 and the gap widens through the main mortality period (ages 50–80).

**Table 2: Pairwise statistical comparisons**

| Comparison | Gap | Cohen's d | p-value |
|---|---|---|---|
| Migrated vs Non-migrated | +3.98 yrs | 0.292 | <0.001 |
| Migrated vs Deported | +26.03 yrs | 1.853 | <0.001 |
| Non-migrated vs Deported | +22.05 yrs | 1.613 | <0.001 |
| Non-migrated vs Internal transfer | +0.35 yrs | 0.026 | 0.271 (NS) |

All three comparisons involving the deported group reach extreme significance (p<0.001, d>1.6). The internal transfer comparison is the only null result — and by design, the most informative control.

But the most dramatic finding is not the 4-year migrant advantage — it is what happened to those who were forcibly taken.

### 4.2 Deported Workers Died 22 Years Earlier

The deported group represents the study's most analytically important finding. Their mean age at death of 49.39 years — a 22.05-year deficit relative to non-migrants (Cohen's d=1.613) — is the direct demographic signature of Soviet political violence.

**Age structure.** The vast majority of deported workers were born between 1880 and 1910, placing them at ages 27–57 during the Great Terror (1934–38) (see Appendix A, Figure A2 for the birth year distribution).

**Death year clustering.** **Figure 5** shows deported workers' deaths clustering sharply in 1937–38. Sixty-seven of the 195 deported workers (34.4%) died in 1937 alone — the year of peak Stalinist terror. Their mean age at death in 1937 was 42.7 years. **Figure 6** shows the year-by-year breakdown.

**The 1937 spotlight.** The Sandarmokh massacres of November 1937 account for a substantial fraction of the 1937 deaths. Soviet security services executed hundreds of Ukrainian cultural figures in a matter of months during the Great Terror. The ESU captures many of these individuals through archival and memorial records, but — as Section 8.2 documents — many others are absent from the ESU entirely.

**Period breakdown for non-migrants.** Table 3 and **Figure A5** show non-migrant deaths by historical period:

**Table 3: Non-migrant deaths by period**

| Period | Deaths | Mean age at death | % of total |
|---|---|---|---|
| 1921–1929 (Early Soviet/NEP) | 95 | 58.4 | 1.6% |
| 1930–1933 (Holodomor/Purges) | 54 | 59.5 | 0.9% |
| 1934–1938 (Great Terror) | 96 | 55.8 | 1.6% |
| 1937 only (Terror peak) | 25 | 49.4 | 0.4% |
| 1939–1945 (WWII) | 207 | 55.1 | 3.5% |
| 1946–1953 (Late Stalin) | 124 | 62.6 | 2.1% |
| 1954–1964 (Khrushchev Thaw) | 236 | 66.6 | 4.0% |
| 1965–1991 (Stagnation/Late USSR) | 1,432 | 69.2 | 24.0% |
| Post-1991 | 3,716 | 74.7 | 62.3% |

The dominance of post-1991 deaths (62.3% of non-migrants) reflects the large cohort of Soviet-era workers who survived into Ukrainian independence. The non-migrant mean of 71.44 incorporates these long-lived survivors — meaning the observed gap is not an artefact of a depressed non-migrant mean; the non-migrant mean is itself elevated by post-Soviet longevity.

If the gap were simply about who chose to leave, we would expect any form of geographic mobility to confer an advantage. It does not.

### 4.3 Moving Within the Soviet System Did Not Help

The internal transfer group — workers who relocated within the USSR but did not exit Soviet jurisdiction — shows no significant mean age at death advantage over non-migrants: +0.35 years, p=0.271 (NS), Cohen's d=0.026. **Figure 7** illustrates this near-zero gap.

This null result is as informative as the positive findings. Geographic movement within the Soviet system — even movement that displaced workers from their home republic — did not confer the survival advantage seen among those who exited Soviet control entirely. The migrant advantage is specifically about exiting the Soviet political system, not merely moving elsewhere.

The gap is real and specific to Soviet exit. But does it hold across the diverse groups within the dataset?

---

## 5. Who, When, Where: Patterns Across the Gap

### 5.1 The Gap Holds Across All Creative Professions

The migrant advantage is not driven by a single profession. **Figure 8** and Table 4 show the gap across all six profession categories:

**Table 4: Age at death by profession and migration group**

| Profession | Migrated LE | n | Non-mig LE | n | Dep LE | n | Gap (M−NM) |
|---|---|---|---|---|---|---|---|
| Writers/Poets | 74.5 | 389 | 70.5 | 1,754 | 46.0 | 123 | +4.0 |
| Visual Artists | 74.8 | 385 | 71.6 | 1,954 | 56.9 | 39 | +3.2 |
| Musicians/Composers | 75.8 | 308 | 71.4 | 916 | 44.9 | 14 | +4.4 |
| Theatre/Film | 75.5 | 64 | 71.8 | 731 | 55.2 | 9 | +3.7 |
| Architects | 79.0 | 61 | 73.2 | 384 | 61.0 | 4 | +5.8 |
| Other Creative | 77.7 | 117 | 73.3 | 221 | 63.5 | 6 | +4.4 |

Writers/Poets — the group most associated with the Executed Renaissance — show a gap (+4.0 yrs) consistent with the overall finding. The fact that the advantage is not driven by a single profession rules out a simple "Writers were targeted more" confounding story. Architects show the largest gap (+5.8 yrs), a finding worth further investigation. Among deportees, Writers/Poets show the youngest mean age at death (46.0 yrs, n=123), consistent with the literary intelligentsia bearing the brunt of the Great Terror.

### 5.2 The 1880–1910 Cohorts Were Hit Hardest

**Figure 9** shows mean age at death by birth decade. The migrant advantage is present across all cohorts from the 1860s through the 1920s, and is largest for the 1880–1910 birth cohorts — those who were in their prime creative years during the peak repression period of 1930–38.

**Table 5: Birth cohort analysis**

| Birth decade | Mig LE | n | NM LE | n | Dep LE | n | Gap (M−NM) |
|---|---|---|---|---|---|---|---|
| 1880s | 74.3 | 176 | 69.3 | 260 | 57.3 | 32 | +5.0 |
| 1890s | 75.4 | 232 | 70.8 | 325 | 44.7 | 62 | +4.6 |
| 1900s | 75.2 | 218 | 72.4 | 650 | 44.2 | 59 | +2.8 |
| 1910s | 77.6 | 219 | 74.9 | 809 | 46.9 | 14 | +2.7 |
| 1920s | 78.9 | 167 | 75.4 | 1,260 | 53.2 | 6 | +3.5 |
| 1930s | 74.9 | 92 | 73.2 | 1,136 | 77.8 | 4 | +1.7 |

The 1930s birth cohort shows the smallest gap (+1.7 yrs), consistent with the post-Stalinist easing of direct violence. This cohort patterning is important: if the gap were primarily driven by selection effects (healthier or wealthier people emigrating), we would expect it to be roughly uniform across cohorts. Instead, it is concentrated in the cohorts most exposed to Stalinist terror — arguing for a real mortality differential, not merely a compositional artefact.

### 5.3 The Gap Holds for Both Sexes

Male workers dominate all groups (migrants: 79.3% male; deported: 92.7% male; 37 entries across all groups have unknown gender). The deported group's heavily male composition reflects the documented pattern of Soviet security services targeting male cultural figures. Female migrants live notably longer than male migrants (78.1 vs 74.6 yrs). Critically, the migrant survival advantage holds for both genders. Full gender breakdowns are provided in Appendix A, Figures A7–A8.

### 5.4 A West-to-East Gradient in Emigration

**Table 6: Geographic migration rates (analysable cohort)**

| City | n | % migrated |
|---|---|---|
| Kyiv | 454 | 13.9% |
| Lviv | 165 | 44.8% |
| Ternopil | 17 | 52.9% |
| Chernivtsi | 23 | 34.8% |
| Donetsk (Stalino) | 14 | 0.0% |

Lviv and Ternopil show migration rates three to four times higher than Kyiv, consistent with geographic proximity to western borders and Habsburg/Polish emigration networks. The Donetsk 0.0% reflects the complete absence of emigration from this heavily Russified industrial city.

Western Ukraine's Galician and Bukovinian regions were under Austro-Hungarian rule until 1918, developed a distinct civic and cultural tradition, and maintained stronger connections to Central European and Western intellectual life. This made emigration to Vienna, Prague, Paris, and ultimately North America both more conceivable and more practically feasible for western Ukrainian creative workers. Eastern and southern Ukrainian creative workers were longer-embedded in Soviet institutions, faced steeper barriers to emigration (both practical and ideological), and were more likely to have professional identities intertwined with Soviet cultural organisations.

### 5.5 When Did They Die? The Temporal Structure

The period analysis (Table 3) reveals two critical patterns. First, mean age at death rises monotonically from the Early Soviet period (58.4 yrs) through Post-1991 (74.7 yrs), consistent with improving conditions after the end of Stalinist terror. Second, the Great Terror period (1934–1938) shows catastrophic mean ages — 55.8 years for non-migrants and far worse for deportees — reflecting the concentrated violence of those years.

The dominance of post-1991 deaths (62.3% of all non-migrant deaths) means the 3.98-year gap is conservative. The non-migrant mean is elevated by a large cohort of workers who survived the Soviet period entirely and lived into Ukrainian independence. Restricting to Soviet-period deaths only would show a substantially larger gap.

The tail behaviour of the distributions is also revealing: migrants are more than twice as likely to reach age 90 (15.0% vs 6.3% of non-migrants), while non-migrants show a 59% excess rate of premature death before age 50 (6.6% vs 5.2%).

---

## 6. Statistical Robustness

The findings presented in Sections 4–5 are descriptive. This section subjects them to regression adjustment, matching, survival analysis, and sensitivity testing to assess whether the observed gap is robust to methodological challenge.

### 6.1 Multivariable Regression

OLS regression of age at death (**Figure 10**):

| Variable | β (Model 1) | β (Model 2) | SE (M2) | p (M2) |
|---|---|---|---|---|
| Intercept (non-migrated) | 71.44 | — | — | — |
| Migrated | +3.98 | +2.71 | 0.45 | <0.001 |
| Internal transfer | −0.35 | −1.74 | 0.46 | <0.001 |
| Deported | −22.05 | −23.31 | 1.01 | <0.001 |

Model 2 (R²=0.086, F=61.97, p<0.001) includes birth decade, profession, and region controls. The migrated coefficient falls from +3.98 to +2.71, indicating that approximately 1.27 years of the raw gap is explained by observable selection covariates (differences in when migrants were born, what professions they held, and where they came from). The residual 2.71-year adjusted gap remains highly significant (p<0.001).

### 6.2 Propensity Score Matching

After 1:1 nearest-neighbour PSM on birth decade, profession, and birth region, the gap narrows to **+3.43 years** (bootstrap 95% CI: 2.38–4.51), a 13.8% attenuation from the unadjusted estimate. The PSM gap is substantially positive and statistically significant, confirming the migrant advantage cannot be explained by the measured selection covariates alone.

### 6.3 Cox Proportional Hazards

**Figure 11** shows the Cox forest plot. Adjusted model results (controlling for birth decade, profession, region):

| Group | HR | 95% CI | p |
|---|---|---|---|
| Migrated | 0.778 | [0.731, 0.828] | <0.001 |
| Internal transfer | 1.087 | [1.018, 1.162] | 0.013 |
| Deported | 4.421 | [3.822, 5.114] | <0.001 |

Migrants had approximately a 24% lower instantaneous mortality risk at any given age. Deported workers had more than 4 times the mortality hazard. The internal transfer HR (1.09) is marginally elevated but orders of magnitude smaller — consistent with the null result in the mean comparison.

**Right-censored supplementary analysis** (N=15,165 including right-censored living individuals): Migrated HR=1.346 (95% CI: 1.262–1.434). The reversal relative to the complete-case model reflects the censoring imbalance: ~52% of non-migrants are right-censored while essentially all migrants are deceased. The complete-case model (HR=0.778) is the primary result. Censoring patterns are documented in Appendix A, Figures A11–A12.

### 6.4 Time-Varying Analysis (Deportees)

The PH assumption is violated for the deported group (Schoenfeld residual test p=0.0), requiring a time-varying approach. Landmark Cox analysis shows:

| Age band | n at risk | Deported events | HR | p |
|---|---|---|---|---|
| 20–30 | 14,994 | 10 | 1.09 | 0.361 (NS) |
| 30–40 | 14,921 | 42 | 1.50 | <0.001 |
| 40–50 | 14,619 | 50 | **1.86** | <0.001 |
| 50–60 | 13,771 | 27 | 1.57 | 0.001 |
| 60–70 | 12,060 | 19 | 1.40 | 0.037 |
| 70–80 | 8,580 | 13 | 1.19 | 0.371 (NS) |
| 80–90 | 4,061 | 6 | 0.89 | 0.657 (NS) |

**Peak HR=1.86 at age 40–50** — the Terror-period execution window. By ages 70–80, deportee survivors show mortality hazard indistinguishable from non-migrants, consistent with survivor selection: those who survived the terror and camp system tended to be unusually resilient. **Figure 12** shows the time-varying profile.

### 6.5 Sensitivity to Classification Error

**Figure 13** shows the gap as a function of AI error rate. The finding remains positive up to approximately 8% error. Our validated rate (3.2%) is well within the safe margin. At 3.2% error, the sensitivity-adjusted gap is 3.24 years; at 10% error (three times the validated rate), the gap remains positive at 1.84 years.

Three additional robustness scenarios are summarised in Appendix B: duration assumptions for right-censored individuals (Scenario A), post-Soviet emigrant handling (Scenario B), and bootstrap misclassification (Scenario C). The finding persists across all specifications.

### 6.6 Missing-Worker Bias

**Figure 14** quantifies the missing-worker bias. Seven individuals confirmed to meet study inclusion criteria are absent from the ESU (see Section 8.2 for names and details). Their mean age at death is 46.7 years — 25 years below the non-migrant mean.

Adding these 8 confirmed missing workers adjusts the gap to approximately 4.02 years. Adding 50 plausible missing workers at a conservative assumed mean of 38 years adjusts it to 4.26 years. Under no plausible assumption does adding missing repressed workers *narrow* the gap — the estimate is a conservative lower bound.

---

## 7. Discussion

### 7.1 What These Patterns Establish

The 3.98-year gap in mean age at death between migrant and non-migrant Ukrainian creative workers is statistically robust, methodologically defensible, and consistent across all analytical disaggregations. The additional finding of a 22.05-year gap between non-migrants and deportees (Cohen's d=1.613) is arguably the study's most dramatic result. Neither finding is a simple measure of the mortality differential associated with Soviet rule for any individual — both are population-level summary statistics that aggregate across highly heterogeneous individual experiences.

The gap reflects, we argue, primarily four mechanisms:

**Direct political mortality.** The most evident mechanism is execution, imprisonment, and Gulag death. The 92 non-migrated and deported deaths concentrated in 1937 alone (average age ~44.5 for those two groups, versus migrants who died that year of largely natural causes), the deported group's overwhelmingly repression-cause mortality (executed, Gulag, exile, and other state-violence causes dominate the biographical record), and the near-total destruction of the 1890s deported cohort (mean age at death 44.6 years) all point to substantial excess mortality from direct state violence that had no equivalent in migrant communities.

**Indirect mortality from Soviet conditions.** Beyond direct political violence, Soviet conditions — poor nutrition, restricted medical care, psychological stress from constant surveillance and self-censorship, the health consequences of Gulag survival, and enforced poverty — likely contributed to excess mortality among non-migrants across the entire Soviet period. This mechanism is not directly measurable from our data but is consistent with the lower average age at death in every Soviet-era period compared to the post-1991 period (see Table 3).

**Selection effects in emigration.** It is plausible that the migrant group is positively selected for resourcefulness, social capital, and health relative to the non-migrant group. Workers who successfully emigrated — regardless of the period — had to navigate bureaucratic, geographic, and financial barriers that not all creative workers could overcome. Some portion of the mean age at death gap may therefore reflect pre-migration differences rather than the causal effect of Soviet conditions. This study cannot distinguish the selection component from the treatment component with the available data; wave-level disaggregation (deferred to future work, see §8.7) would be required to assess whether the gap varies by emigration context.

**Cohort variation in the gap.** The birth cohort analysis (Table 5) shows that the gap is not uniform: it is largest for the 1880s (+5.0 yrs) and 1890s (+4.6 yrs) cohorts — the Executed Renaissance generation — and smallest for the 1930s cohort (+1.7 yrs), who came of age after the worst Stalinist violence. This variation is consistent with a real mortality differential concentrated in the Terror period, though it does not rule out the possibility that selection pressures also varied across cohorts.

**The internal transfer null result is the crucial control.** Non-migrated and internally transferred workers have essentially identical life expectancies (+0.35 yrs, p=0.271). Geographic movement within the Soviet system — even movement that displaced workers from their home republic — did not confer the survival advantage seen among those who exited Soviet control entirely. The migrant advantage is specifically associated with exiting the Soviet political system, not merely moving elsewhere.

**Consistency across cohorts and professions argues against a simple compositional explanation.** The regression-adjusted gap (2.71 yrs) and PSM gap (3.43 yrs) show that after controlling for birth cohort, profession, and region, a substantial gap remains. The gap holds in every profession category tested (Table 4). This pattern is inconsistent with a story where the gap is entirely explained by one or two professions or cohorts being differently represented in the migrated group.

### 7.2 Association, Not Causation

We do not claim that emigration *caused* longer life in the sense of a clean experimental treatment. Migration was not random. Workers who emigrated may have differed from those who stayed in ways we cannot fully observe: health at the time of emigration, political connections, language skills, family circumstances, and sheer timing luck (the window for emigration closed for most workers by the mid-1950s). PSM controls for measured covariates; unmeasured confounders remain.

**Galician survival selection.** Workers from Galicia (Western Ukraine, under Polish/Austrian rule until 1939) were geographically positioned to emigrate westward more easily and had pre-existing North American diaspora networks. They also experienced Soviet control later — their exposure to the worst Stalinist terror years was shorter. Some of the observed advantage may reflect this different exposure history rather than emigration per se.

**Healthy migrant effect.** Workers who survived the emigration journey — often under wartime conditions — were already selected for physical resilience. This selection bias would inflate the observed migrant mean age at death.

**Post-Soviet non-migrant composition.** 61.5% of non-migrant deaths occurred after 1991. The non-migrant mean is elevated by a large cohort of workers who lived long into Ukrainian independence. This makes the observed gap conservative: restricting to Soviet-period deaths only would show a larger gap.

Despite these caveats, the consistency of the gap across cohorts, professions, and genders — and its persistence through PSM and OLS adjustment — provides reasonable confidence that the observed association reflects a real mortality differential, partly caused by the genuine survival consequences of exiting Soviet control.

### 7.3 Historical Interpretation

The 1890–1920 birth cohorts show the largest migrant/non-migrant gaps (4.6 yrs and 4.6 yrs for the 1890s and 1880s cohorts respectively). These individuals were in their 30s and 40s — peak productive and politically vulnerable ages — during the Great Terror (1937–38) and the wartime period (1941–45). For these cohorts, the decision or opportunity to emigrate was, in many documented cases, literally life or death.

The 1937 death concentration among deportees (67 of 195 died in 1937, mean age 42.7; deported workers dying in the 1934–38 period had a mean age of just 43.5 years; those in 1939–45 died at mean 45.0 years) reflects the Sandarmokh massacres and the broader Great Terror, when Soviet security services executed thousands of Ukrainian cultural figures in months. This is not a statistical artefact — it is the ESU's partial capture of a historically documented event.

The late-cohort analysis also reveals convergence: workers born after 1940 show much smaller gaps (+1.7 yrs for 1930s births), consistent with the post-Stalinist easing of direct violence against intellectuals. The conditions producing the large mortality differential were specific to the Stalinist period.

### 7.4 Comparison to Prior Research

The reduction in the measured gap from V1 (+9.0 yrs) to V3.0 (+3.98 yrs) deserves careful interpretation. It does not represent a finding that Soviet repression was less lethal than previously estimated. The narrowing is driven by two methodological changes: first, V1's pre-1991 death cutoff systematically excluded the longest-lived non-migrants (those who survived into Ukrainian independence), artificially depressing the non-migrant mean; second, V1's small and non-systematically drawn sample leaned heavily toward writers from the Executed Renaissance cohort. The full ESU population includes a large cohort of non-migrants who survived the Soviet period and lived into old age in independent Ukraine. Their inclusion naturally raises the non-migrant mean and narrows the observed gap.

The V1 finding was real within its analytical scope. V3.0 does not contradict it; it extends the analysis to a more complete and representative population. The methodological lesson is clear: future studies of Soviet-era mortality should not restrict to curated or prominent-individual samples, as doing so systematically excludes the longest-lived members of the "stayed" cohort and artificially inflates the measured mortality differential. The V3.0 estimate is more conservative and more defensible precisely because it covers the full ESU population with a validated error rate.

Our findings are broadly consistent with existing historical scholarship on Soviet repression and with the limited quantitative literature on mortality in Soviet-era populations. Studies of Gulag mortality document catastrophic death rates in Soviet labour camps, reaching 20–25% annually during 1942–1943, and systematic mass executions during 1937–1938. These documented mortality patterns are broadly consistent with our deported group's average age at death of 43.4 years during 1934–1938 and 44.4 years during 1939–1945.

Comparative demography of Soviet versus Western European general populations documents a Soviet mortality penalty that grew from approximately 3 years in the mid-1960s to over 10 years by the early 1990s, depending on country and sex. Andreev et al.'s demographic reconstruction for the 1927–1959 period directly covers our Great Terror and wartime years. Our finding of a 3.98-year migrant advantage is consistent with the lower end of the East-West divergence range, though our dataset's focus on a group subject to targeted repression means our estimate captures both the general Soviet mortality penalty and the profession-specific repression effect — not general population mortality alone.

**Figure 15** shows ESU group means overlaid on Ukrainian SSR general population estimates. **Figure 16** provides a simplified view of the same data using annual death rates normalised by group size, making the WWII-era mortality spike and the relative proportions of death across groups clearly visible. Together, these two figures contextualise the creative worker mortality patterns against the broader Ukrainian demographic record. Appendix A, Figures A9–A10 provide additional contextual comparisons against Soviet republic benchmarks and educated-urban baselines, showing that non-migrants during repression periods fall below even the general population estimate — suggesting excess mortality over and above what socioeconomic composition alone would predict.

---

## 8. Limitations

### 8.1 Data Source: ESU Coverage Bias

The ESU disproportionately covers culturally prominent individuals. Workers who were arrested, killed, and whose work was suppressed may have smaller or absent entries. This bias is asymmetric: the most severely repressed workers (in the non-migrated and deported groups) are most likely to be missing. Current estimates are therefore **conservative lower bounds** on the true mortality differential.

### 8.2 Missing Repressed Workers

Seven individuals confirmed to meet study inclusion criteria are absent from the ESU: Vasyl Stus (died Perm-36, age 47), Mykola Khvylovy (suicide, age 40), Mykola Zerov (shot Sandarmokh, age 47), Les Kurbas (shot Sandarmokh, age 50), Mykola Kulish (shot Sandarmokh, age 45), Oles Dosvitniy (shot, age 43), Mykola Boychuk (shot, age 55). Their mean age at death is 46.7 years — 25 years below the non-migrant mean. Ages are calculated as death_year minus birth_year, consistent with the study's primary method. Adding 50 plausible missing workers at a conservative assumed mean of 38 years widens the gap further.

### 8.3 Classification Quality

The validated AI error rate is 3.2%, based on a complete 200-entry stratified review. Errors were concentrated in near-boundary Galician cases. The sensitivity analysis confirms the finding holds robustly to approximately 8% error.

### 8.4 Observational Design

This is an observational study. Causal inference is limited by self-selection into migration, unmeasured confounders, and the impossibility of a counterfactual. PSM partially addresses measured confounders; unmeasured ones cannot be controlled with available data.

### 8.5 Post-Soviet Composition

61% of non-migrant deaths occurred after 1991. The gap captures lifetime exposure — not purely Soviet-period exposure. This is appropriate for a lifespan study but means the gap cannot be read as reflecting Soviet-period mortality differentials alone.

### 8.6 Galician Survival Selection

Workers from Galicia had earlier and easier access to emigration routes and experienced Soviet rule only from 1939. Their inclusion in the "migrated" category means some of the observed advantage may reflect different exposure history rather than emigration per se. Galicia pre-annexation entries are excluded from the analysis (see §3.2), but Galicians who remained in the Soviet system post-1939 are included.

### 8.7 Wave Disaggregation Deferred to V3 Data Collection

An early analysis (Stage 9) attempted to disaggregate migrants by emigration wave (pre-1922, 1939–45, 1946–91). The classifier proved unreliable: it recovered birth and death years from biographical text rather than actual emigration dates, leading to spurious wave assignments. This analysis was retracted. Wave disaggregation is the primary V3 data collection priority, requiring explicit emigration year fields to be added to the dataset.

### 8.8 Living Cohort Assumptions (Right-Censored Cox)

The right-censored supplementary Cox analysis treats living individuals as censored at 2026. This introduces bias because living individuals are concentrated in the non-migrated group (~52% censored). The complete-case Cox (HR=0.778) is the primary model.

---

## 9. Conclusion

This study provides systematic quantitative evidence that Ukrainian creative workers who emigrated from Soviet-controlled Ukraine lived measurably longer than those who remained. The primary gap of **3.98 years** (75.42 yrs vs 71.44 yrs; Cohen's d=0.292; p<0.001) is verified against the full 8,590-entry dataset, persists after controlling for birth cohort, profession, and region, and is robust to classification error rates well above the validated 3.2%.

The finding that matters most is not the 3.98-year gap but the **22.05-year deficit of deported workers** (mean age 49.39 yrs; Cohen's d=1.613). This is not a statistical inference about systemic disadvantage — it is the direct mortality signature of state-organised violence, concentrated in 1937 (67 of 195 deported workers died that year, at mean age 42.7), documented in biographical text. Soviet repression of Ukrainian culture was, among other things, a demographic catastrophe for a professional class.

The **internal transfer null result** (+0.35 yrs, p=0.271) is as informative as the positive findings: workers who moved within the Soviet system lived essentially the same lifespan as those who stayed. The survival advantage was specifically associated with exit from Soviet control, not merely geographic movement.

The current dataset provides a conservative lower bound. Adding the confirmed 7 missing figures only widens the gap to ~4.0 years. The most severely repressed workers are the least likely to appear in the ESU — meaning the true mortality differential is larger than the 3.98 years observed here.

These findings are consistent with what Ukrainian historians have documented through archival and testimonial evidence: that Soviet cultural policy was associated with substantial mortality differentials among the creative workers who remained under Soviet rule, concentrated particularly in the generation that came of age between the Revolution and the Great Terror. The numbers do not tell the full story — they cannot capture the individual lives, the works that were never written, the music that was never composed, the theatres that went dark — but they provide a quantitative description of mortality patterns that complements the existing archival and testimonial record.

We make no claim that this analysis is definitive. The ESU-based dataset is not a complete census of Ukrainian creative workers; our migration classification system makes simplifications that the historical record does not always support; and the selection effects inherent in emigration preclude clean causal inference. Future research should seek to replicate and extend these findings using alternative data sources — particularly Soviet-era repression records, diaspora archives, and memorial databases — and should apply methods capable of addressing the selection problem more rigorously.

Future priorities for V3: (1) collect explicit emigration dates to enable reliable wave disaggregation; (2) extend the analysis to non-creative professional categories; (3) develop a method to estimate the number and characteristics of ESU-absent repressed workers; (4) attempt independent replication using the VIVO biographical database.

**The Executed Renaissance is not merely a literary metaphor — it describes a historical demographic event whose mortality signature, this study suggests, is quantitatively detectable at scale among the documented figures of Ukrainian cultural life.**

---

## 10. Figure Index

**Figure 1** — *Primary mean age at death comparison.* Bar chart showing mean age at death ± 95% CI for all four migration groups. The central result is immediately visible: migrants (75.42 yrs) outlived non-migrants (71.44 yrs) by 3.98 years, while deportees (49.39 yrs) died 22.05 years earlier than non-migrants. Internal transfers (71.09 yrs) are statistically indistinguishable from non-migrants. Error bars show 95% confidence intervals; the migrant and non-migrant intervals do not overlap.

**Figure 2** — *Kaplan-Meier survival curves.* Survival probability as a function of age for all four groups. The migrated and non-migrated curves track closely until approximately age 40, then diverge progressively through ages 50–80 — the primary mortality period. The deported curve drops sharply from age 35, reflecting concentrated state violence during the Terror and WWII years. Reference lines mark the non-migrated median (73 yrs) and deported median (46 yrs).

**Figure 3** — *V1 vs V3.0 comparison.* Side-by-side comparison using consistent two-group framing (left USSR vs stayed in Soviet sphere) to enable direct comparison between V1 (n=415, gap=+9.0 yrs) and V3.0 (n=8,590, gap=+4.6 yrs in two-group framing). The gap narrowed because V1's pre-1991 death cutoff excluded long-lived non-migrants who survived into Ukrainian independence, and V1's non-systematic sampling over-represented the most extreme cases. The narrower V3.0 estimate is more conservative and more defensible.

**Figure 4** — *CONSORT exclusion flowchart.* Complete documentation of the exclusion pipeline from 16,215 scraped ESU entries to 8,590 analysable individuals, showing every exclusion category and count. Ensures full transparency about how the analysable cohort was derived and where potential selection effects enter the data.

**Figure 5** — *Deported death year distribution.* Histogram of death years for the deported group (n=195), showing the extreme concentration in 1937: 67 of 195 deported workers (34.4%) died in a single year during the Great Terror. This is the ESU's partial demographic capture of the Sandarmokh massacres and the broader campaign of mass execution of Ukrainian cultural figures.

**Figure 6** — *Deported deaths by year, 1921–1965.* Year-by-year count of deported worker deaths, isolating the chronological structure of state violence. The 1937 peak is followed by elevated mortality through 1938–1945 (late Terror + WWII camp deaths), then a sharp decline as the surviving deportees age out of the highest-risk period.

**Figure 7** — *Internal transfer null result.* Direct comparison of internal transfer (71.09 yrs) and non-migrated (71.44 yrs) groups, showing a gap of just +0.35 years (p=0.271, not significant). This is the study's most important control finding: geographic movement within the Soviet system conferred no survival advantage. Only exit from Soviet jurisdiction is associated with longer life.

**Figure 8** — *Mean age at death by profession and migration group.* Grouped bar chart showing the migrant advantage across all six profession categories (Writers/Poets, Visual Artists, Musicians/Composers, Theatre/Film, Architects, Other Creative). The gap is present in every category, ranging from +3.2 years (Visual Artists) to +5.8 years (Architects), ruling out the possibility that the overall finding is driven by a single profession.

**Figure 9** — *Birth cohort mean age at death.* Mean age at death by birth decade for migrants and non-migrants. The gap is largest for the 1880s (+5.0 yrs) and 1890s (+4.6 yrs) cohorts — the Executed Renaissance generation, who were at peak creative and politically vulnerable ages during the Great Terror — and smallest for the 1930s cohort (+1.7 yrs), consistent with the post-Stalinist easing of direct violence.

**Figure 10** — *OLS regression coefficient plot.* Forest plot of regression coefficients from Model 2 (adjusted for birth decade, profession, and region). The migrated coefficient falls from +3.98 (unadjusted) to +2.71 (adjusted), showing that approximately 1.27 years of the raw gap is explained by observable selection covariates. The residual 2.71-year adjusted gap remains highly significant (p<0.001).

**Figure 11** — *Cox proportional hazards forest plot.* Hazard ratios and 95% CIs from the adjusted Cox model (controlling for birth decade, profession, region). Migrants: HR=0.778 [0.731, 0.828] — approximately 22% lower instantaneous mortality risk at any given age. Deported: HR=4.42 [3.82, 5.11] — more than four times the mortality hazard. Internal transfers: HR=1.09 — marginally elevated but orders of magnitude smaller than the deported effect.

**Figure 12** — *Deported hazard ratio by age band.* Time-varying (landmark) Cox analysis decomposing the deported group's overall HR into age-band-specific estimates. Peak HR=1.86 occurs at age 40–50 — the Terror-period execution window, when most deportees were in their prime years. By ages 70–80, deportee survivors show mortality indistinguishable from non-migrants (HR=1.19, NS), consistent with survivor selection: those who survived the camps and executions were unusually resilient.

**Figure 13** — *Sensitivity to AI classification error.* The mean age at death gap plotted as a function of assumed AI error rate (0–20%). At the validated error rate of 3.2%, the gap is 3.24 years. The finding remains positive up to approximately 8% error — well above the validated rate. Even at 10% error (more than three times the measured rate), the gap remains positive at 1.84 years.

**Figure 14** — *Missing-worker sensitivity.* Estimated gap as a function of the number of missing repressed workers (M) and their assumed mean age at death. The 7 confirmed ESU-absent workers (mean age 46.7 yrs) widen the gap to 4.01 years; adding 50 plausible missing workers at a conservative assumed mean of 38 years widens it to 4.26. Under no plausible (M, age) combination does the gap narrow — the current estimate is a conservative lower bound.

**Figure 15** — *Soviet-era population context.* Mean age at death for each ESU migration group overlaid on Ukrainian SSR general population life expectancy estimates from Meslé & Vallin (2003) and the UN World Population Prospects (2022). The non-migrant creative worker mean (71.44 yrs) sits slightly above the Soviet-era general population baseline — consistent with the ESU's educated-elite bias — while the migrant mean (75.42 yrs) exceeds it further. The deported mean (49.39 yrs) falls catastrophically below any population benchmark. This chart contextualises the study's findings against the broader demographic record: the 3.98-year migrant advantage is not an artefact of comparing creative workers against the general population, but exists above an already-elevated baseline.

**Figure 16** — *Annual death rates by migration group, 1921–1992.* Each line shows deaths per year as a percentage of that group's total size, normalising for the large differences in group size (non-migrated n=5,960 vs deported n=195). Three features are immediately visible: (1) the sharp deported spike in 1937 — over 30% of the entire deported cohort died in a single year during the Great Terror; (2) the WWII-era mortality surge (1941–1945) visible across all groups but proportionally heaviest among non-migrants and internal transfers who remained in occupied or front-line territory; (3) the post-war divergence, where non-migrant death rates remain elevated relative to migrants through the late Soviet period. This chart makes the temporal concentration of repression-driven mortality visible in a way that aggregate means cannot.

Additional figures (box plots, violin plots, gender breakdowns, geographic detail, birth year distributions, Soviet republic comparisons, educated-urban baseline, censoring patterns, Schoenfeld residuals, and multi-scenario sensitivity summaries) are provided in **Appendix A**.

---

## 11. AI Methodology Note

Classification of 16,215 entries was performed using the Anthropic Claude API across multiple stages:

- **Primary classification (Stage 4):** claude-sonnet-4-6 with structured two-step protocol (check forced displacement first; then assign migration status). Rate: 2 requests/second to ESU scraping; 0.5 requests/second to Claude API.
- **Stage 12 B3 reclassification:** claude-haiku-4-5-20251001 for 57 API-error retries.
- **Stage 14 reclassification:** claude-haiku-4-5-20251001 for 135 authentication-error retries.
- **Nationality review (Stage 6+):** Secondary Claude review for entries flagged as potentially non-Ukrainian.

**Validation (complete, V3.0):**
A stratified random validation sample of 200 entries (100 INCLUDE, 100 EXCLUDE categories) was drawn and reviewed in full against ESU biographical texts. The complete review is documented in `validation/validation_v2_6_results.json` (200-entry main review) and `validation/stage14_reviewer.html` (Stage 14 135-entry review). Final observed error rate: **3.2%**. Six corrections identified in the Stage 14 validation review were applied as Stage 15 patches.

**V3.0 database corrections summary:**
- Stage 12 B1: 8 hardcoded patches for validation-identified errors
- Stage 12 B2: 97 birth-year-as-death-year corrections
- Stage 12 B3: 57 API-error classification retries
- Stage 12 B4: Non-Ukrainian audit (0 corrections required in analysis groups)
- Stage 13: 8 validation-review corrections
- Stage 14: 135 API-authentication-error reclassifications
- Stage 15: 6 Stage-14-review corrections

Full classification prompts, model versions, and per-entry reasoning are stored in the `migration_reasoning` column of `esu_creative_workers_v2_6.csv`. Methodology documentation: `AI_METHODOLOGY_LOG.md`. All scripts: `ukraine_v2/` directory.

---

[^1]: The full list of 31 Ukrainian-language profession keywords used for filtering is documented in `SCIENTIFIC_METHODOLOGY.md`, Section 3.4.

[^2]: "Soviet-controlled territory" includes the Ukrainian SSR, other Soviet republics, and Soviet-occupied territories. Workers who emigrated to any non-Soviet destination (Western Europe, North America, Australia, etc.) are classified as migrated.

[^3]: Individuals without documented death years (n=6,680) are treated as right-censored in the supplementary Cox analysis but excluded from the primary mean-age-at-death comparison.

---

## 12. Bibliography

Andreev, E. M., Darsky, L. E., & Kharkova, T. L. (1998). Demographic History of Russia, 1927–1959. *Informatika*.

Applebaum, A. (2003). *Gulag: A History*. Doubleday.

Conquest, R. (1968). *The Great Terror: Stalin's Purge of the Thirties*. Macmillan.

Grabowicz, G. G. (1982). The Ukrainian Literary Revival: Toward a New Understanding. *Harvard Ukrainian Studies*, 6(2), 209–260.

Meslé, F., & Vallin, J. (2003). Mortality in Eastern Europe and the Former Soviet Union: Long-term trends and recent upturns. *Demographic Research*, Special Collection 2, 45–70.

Shkandrij, M. (2010). *In the Maelstrom: The Artef, Ukrainian Modernism, and Soviet Cultural Policy, 1917–1932*. University of Toronto Press.

Snyder, T. (2010). *Bloodlands: Europe Between Hitler and Stalin*. Basic Books.

United Nations Population Division. (2022). *World Population Prospects 2022 Revision*. United Nations.

---

## Appendix A: Supplementary Figures

**Figure A1** — *Box plots by group.* Interquartile range, median, and outlier distribution for all four groups. The migrated and non-migrated distributions overlap substantially but differ in central location. The deported distribution is dramatically compressed downward, with a median of 46 and multiple outliers above 70 — the survivors.

**Figure A2** — *Deported group birth year distribution.* Shows the birth decade composition of the 195 deported workers. The concentration in the 1880–1910 cohorts (ages 27–57 during the Great Terror) confirms that deportation targeted workers in their prime creative and politically active years.

**Figure A3** — *Violin plots.* Full kernel density estimation for all four groups. The deported distribution shows a distinctive bimodal pattern: a primary mass at ages 35–55 (terror-period executions and labour camp deaths) and a smaller secondary peak at ages 60–90 (survivors who escaped execution and reached normal ages). No other group shows this bimodality.

**Figure A4** — *Death year histogram (migrated vs non-migrated).* Temporal distribution of deaths across the 20th century. Non-migrant deaths are concentrated in the post-1960 period (62.3% after 1991), while migrant deaths are more evenly distributed. The different temporal profiles reflect different exposure histories to Soviet conditions.

**Figure A5** — *Non-migrant deaths by Soviet historical period.* Mean age at death for non-migrants by period: Early Soviet/NEP (58.4 yrs), Holodomor (59.5), Great Terror (55.8), WWII (55.1), Late Stalin (62.6), Thaw (66.6), Stagnation (69.2), Post-1991 (74.7). The monotonic increase after the Terror reflects both improving conditions and cohort ageing effects.

**Figure A6** — *Geographic migration rates by city of birth.* Migration rates for the top 20 birth cities, illustrating the west-to-east gradient: Lviv (44.8%), Ternopil (52.9%), and Chernivtsi (34.8%) reflect Galician/Bukovinian emigration networks, while eastern cities show rates near zero. Kyiv (13.9%) occupies a middle position.

**Figure A7** — *Gender composition by group.* Male workers dominate all groups: migrants 79.3% male, non-migrants 84.6%, internal transfers 85.5%, deported 92.7%. The deported group's heavily male composition reflects the Soviet security services' documented pattern of targeting male cultural figures.

**Figure A8** — *Mean age at death by gender and migration group.* The migrant survival advantage holds for both sexes. Female migrants live notably longer than male migrants (78.1 vs 74.6 yrs), consistent with the general female longevity advantage. The gap between migrant and non-migrant women (+4.8 yrs) is comparable to the gap for men (+3.5 yrs).

**Figure A9** — *Soviet republic comparisons.* ESU creative worker estimates compared to published period life expectancy data for Ukrainian SSR, Russian SFSR, Baltic, and Central Asian Soviet republics. Provides cross-republic contextualisation showing where creative workers sit relative to general population benchmarks.

**Figure A10** — *Educated-urban baseline comparison.* Non-migrant creative workers compared against an estimated educated-urban Ukrainian population baseline. During repression periods, non-migrant creative workers fall below even the general educated-urban estimate — suggesting profession-specific excess mortality beyond what socioeconomic class alone would predict.

**Figure A11** — *Censoring pattern in right-censored analysis.* Stacked bar showing the proportion of dead vs right-censored (living) individuals in each migration group. The non-migrated group has ~52% censoring (living individuals assumed non-migrant), creating a structural asymmetry that complicates the supplementary right-censored Cox analysis.

**Figure A12** — *Kaplan-Meier with right-censored data.* KM survival curves from the extended dataset (N=15,165 including living individuals) with tick marks at censoring events. The heavy censoring in the non-migrated group is visible as dense tick marks, illustrating why the complete-case model (HR=0.778) is preferred over the right-censored model.

**Figure A13** — *All-groups mean age at death overlay.* All four groups overlaid in a single box/distribution plot for direct visual comparison of central tendency, spread, and overlap. The deportee distribution is visually separated from the other three groups.

**Figure A14** — *Birth year distribution by group.* Histogram showing birth year composition of each analysis group. The migrated cohort skews slightly earlier (more individuals born 1870–1910), consistent with Wave 1 (pre-1922) emigration demographics. This compositional difference is controlled for in the OLS and PSM analyses.

**Figure A15** — *Two-group conservative comparison.* Restricted analysis combining non-migrated, internal transfer, and deported into a single "stayed in Soviet sphere" group — the most sceptic-resistant framing. The gap narrows slightly relative to the 4-group primary analysis but remains substantial and significant.

**Figure A17** — *Sensitivity analysis summary (Scenarios A–C).* Multi-panel summary of three robustness scenarios: A (varying assumed death age of right-censored living individuals, 70–90 yrs), B (including vs excluding vs reclassifying 62 post-Soviet emigrants), C (bootstrap misclassification at 10% error rate). The migrated HR remains stable across all specifications.

**Figure A18** — *Schoenfeld residuals (smoothed).* Smoothed Schoenfeld residual plot for the deported group in the Cox model. The clear non-zero trend confirms the proportional hazards assumption violation — the deportee hazard ratio is not constant over time but peaks during the Terror-era ages and declines afterward. This violation motivates the landmark (time-varying) analysis in Figure 12.

---

## Appendix B: Robustness Tables and Model Specifications

Full regression output (OLS Models 1 and 2), Cox model diagnostics, propensity score matching balance statistics, and sensitivity scenario details are available in the following analysis output files:

- `analysis_v2_6.txt` — Complete descriptive statistics and primary analysis
- `results/cox_censored_output.txt` — Right-censored Cox model output
- `results/sensitivity_output.txt` — Full sensitivity analysis results
- `results/sensitivity_results.json` — Sensitivity results (machine-readable)
- `results/timevarying_output.txt` — Time-varying landmark Cox output
- `regression_full_output.txt` — OLS regression full output
- `cox_output.txt` — Complete-case Cox model summary

All analysis scripts are available in the `ukraine_v2/` directory. The primary analysis engine is `generate_analysis.py`. Numeric claims in the paper are verified by `check_paper_numbers.py` (177/177 checks pass in V3.0).

---
