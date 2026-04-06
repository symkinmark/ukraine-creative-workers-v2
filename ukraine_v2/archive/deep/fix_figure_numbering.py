#!/usr/bin/env python3
"""
fix_figure_numbering.py
1. Rewrites build_paper_html.py FIGURE_MAP to correct file→number mapping
   (fig01=Figure 1 ... fig22=Figure 22, with 15b and 19b variants)
2. Fixes regex in build_paper_html.py to handle "15b", "19b" figure labels
3. Replaces §7 Figure Captions in PAPER_DRAFT.md with correctly-numbered captions
"""
import os, re

PROJECT = os.path.dirname(os.path.abspath(__file__))
BUILD   = os.path.join(PROJECT, 'build_paper_html.py')
PAPER   = os.path.join(PROJECT, 'PAPER_DRAFT.md')

# ── STEP 1: Patch build_paper_html.py ─────────────────────────────────────────

with open(BUILD, encoding='utf-8') as f:
    build_src = f.read()

# Replace FIGURE_MAP (integer keys → string keys, correct file order)
OLD_MAP = r'# Map each Figure N to its PNG filename.*?}'
NEW_MAP = '''# Map each Figure N to its PNG filename (file number = paper figure number)
FIGURE_MAP = {
    '1':   'fig01_primary_le_comparison.png',
    '2':   'fig02_kaplan_meier.png',
    '3':   'fig03_version_comparison.png',
    '4':   'fig04_box_plots.png',
    '5':   'fig05_deported_age_histogram.png',
    '6':   'fig06_violin_plots.png',
    '7':   'fig07_death_year_histogram.png',
    '8':   'fig08_deported_deaths_by_year.png',
    '9':   'fig09_nonmigrant_deaths_by_period.png',
    '10':  'fig10_birth_cohort_le.png',
    '11':  'fig11_profession_grouped_bar.png',
    '12':  'fig12_geographic_migration_rates.png',
    '13':  'fig13_birth_year_distribution.png',
    '14':  'fig14_sensitivity_analysis.png',
    '15':  'fig15_internal_transfer_null.png',
    '15b': 'fig15b_all_groups_le_box.png',
    '16':  'fig16_consort_flowchart.png',
    '17':  'fig17_gender_by_group.png',
    '18':  'fig18_le_by_gender_group.png',
    '19':  'fig19_ssr_population_context.png',
    '19b': 'fig19b_simplified_death_rate.png',
    '20':  'fig20_two_group_conservative.png',
    '21':  'fig21_soviet_republic_comparison.png',
    '22':  'fig22_educated_urban_comparison.png',
}'''
build_src = re.sub(OLD_MAP, NEW_MAP, build_src, flags=re.DOTALL)

# Fix IMAGES dict — string keys now, no int conversion
build_src = build_src.replace(
    'IMAGES = {n: img_b64(fn) for n, fn in FIGURE_MAP.items()}',
    'IMAGES = {k: img_b64(fn) for k, fn in FIGURE_MAP.items()}'
)

# Fix regex to match "Figure 15b", "Figure 19b" (add [ab]? to digit pattern)
build_src = build_src.replace(
    r"fig_m = re.search(r'\*\*Figure\s+(\d+)', para)",
    r"fig_m = re.search(r'\*\*Figure\s+(\d+[ab]?)', para)"
)

# Fix the int() cast — string keys need no cast
build_src = build_src.replace(
    '            fig_num = int(fig_m.group(1))',
    '            fig_num = fig_m.group(1)'
)

with open(BUILD, 'w', encoding='utf-8') as f:
    f.write(build_src)
print('✓ build_paper_html.py patched')

# ── STEP 2: Replace §7 in PAPER_DRAFT.md ──────────────────────────────────────

# New §7 section with captions in file-number order (fig01→Figure 1, etc.)
# Caption text reused from existing captions, renumbered to match files.

NEW_SECTION_7 = '''## 7. Figure Captions

All figures were generated computationally from the dataset described in §3 and are available in the `/charts/` subdirectory of the project repository.

**Figure 1:** Mean age at death with 95% confidence interval error bars for each of the four migration groups: migrated (n=1,280, mean=75.25 yrs), non-migrated (n=6,030, mean=71.22 yrs), internal transfer (n=1,150, mean=70.70 yrs), and deported (n=183, mean=48.35 yrs). The primary 4.04-year gap between migrated and non-migrated, and the 22.87-year deficit of the deported group, are the headline findings of this study.

**Figure 2:** Kaplan-Meier survival curves for all four migration groups. The Y-axis shows the probability of survival to a given age; curves begin at 1.0 (all individuals alive) and descend with each recorded death. Shaded bands show 95% confidence intervals. The migrated group's curve remains highest throughout; the deported group's curve falls sharply in the 1930s and 1940s. Median survival ages: migrated=77, non-migrated=73, internal transfer=72, deported=45.

**Figure 3:** Grouped bar chart directly comparing the prior study's two-group results (Berdnyk et al. 2025[^4]: migrated mean=72 yrs, non-migrated mean=63 yrs, gap=9 yrs, n=415) against the present study's recalculated two-group results using identical grouping logic (migrated mean=75.25 yrs, stayed-in-Soviet-sphere mean=70.58 yrs, gap=4.68 yrs, n=8,643). Demonstrates that the gap narrows because the present dataset includes the long-lived post-Soviet non-migrants excluded by the prior study's 1991 cutoff, not because the underlying mortality differential has changed.

**Figure 4:** Notched box plots of age at death for each of the four migration groups. The central line marks the median; notches show the 95% confidence interval around the median; boxes span the interquartile range (IQR); whiskers extend to 1.5×IQR; points beyond whiskers are individual outliers. Median values are annotated directly on the plot. The deported group's box sits far below the other three, with a median of 45 and a compressed upper quartile reflecting mass non-natural mortality.

**Figure 5:** Histogram of age at death for the deported group only (n=183), in 5-year bins from 0 to 105. A dashed vertical line marks the group mean (48.35 yrs). The distribution is sharply left-skewed with a heavy mass below age 60 and a pronounced spike in the 35–50 range, consistent with mass execution and Gulag[^9] death concentrated in mid-career individuals. The small right tail (ages 70+) represents deported workers who survived into the post-Stalin release period.

**Figure 6:** Violin plots of age at death for all four groups, showing the full kernel density of the distribution alongside inner quartile lines. Violin plots reveal the shape of the data beyond what box plots show — in particular, the deported group's distribution is sharply left-skewed and truncated, consistent with a cohort subject to systematic early mortality rather than natural attrition. The migrated group's distribution shows the longest upper tail, extending into the 90s.

**Figure 7:** Stacked histogram of death years (2-year bins, 1900–2024) for the migrated and non-migrated groups, with vertical lines marking 1917 (Bolshevik Revolution) and 1991 (Soviet dissolution). Shows the temporal distribution of deaths across the two largest groups and makes visible the period clusters associated with Soviet mortality crises (peaks in the 1930s–1940s for non-migrants) versus the more gradual post-war distribution for migrants.

**Figure 8:** Year-by-year bar chart of recorded deaths in the deported group (n=183), 1920–2000. The 1937 spike — 65 deaths, 35.5% of the entire cohort in a single calendar year — is the visual centrepiece of the repression analysis and the strongest single-year mortality signal in the dataset. A secondary cluster in 1941–1945 reflects wartime Gulag conditions. After approximately 1950, deaths in the deported cohort drop to near-zero; the cohort is, in demographic terms, effectively destroyed.

**Figure 9:** Grouped bar chart of mean age at death by Soviet historical period (NEP 1921–1928, Holodomor 1929–1933, Great Terror 1934–1938, WWII 1939–1945, Late Stalinist 1946–1953, Thaw 1954–1964, Stagnation 1965–1991, Post-independence 1992–present) for each migration group. Repression-period bars are visually distinguished. The deported group's Terror-period bar (mean 43.4 yrs) is the lowest of any group in any period. The post-independence bar for non-migrants (74.7 yrs) is the highest, illustrating why excluding post-Soviet deaths systematically underestimates non-migrant longevity.

**Figure 10:** Line chart showing mean age at death by birth decade for migrants, non-migrants, internal transfers, and deported workers (minimum n=10 per data point to suppress noise). The 1880s and 1890s cohorts — the Executed Renaissance generation — show the largest between-group gaps (5.1 yrs for both). The deported 1890s cohort (mean LE 44.6 yrs, n=60) represents the most concentrated mortality event in the dataset. Gaps narrow for post-1920 cohorts, consistent with declining Soviet political targeting of creative workers after the Great Terror.

**Figure 11:** Grouped bar chart showing group sizes and mean life expectancy by creative profession (Writers/Poets, Visual Artists, Musicians/Composers, Theatre/Film, Architects, Other Creative). The migrated-versus-non-migrated gap is present in every profession category without exception. Writers/Poets contribute the largest deported sub-cohort (n=117), reflecting the particular intensity of Soviet targeting of Ukrainian-language literary production. Architects show the largest between-group gap (+6.1 yrs).

**Figure 12:** Horizontal bar chart ranking the top 20 birth cities by total number of creative workers in the dataset, with each bar subdivided to show the proportion who migrated. Migration rates are labelled numerically. Western Ukrainian cities (Lviv 17.3%, Ternopil 15.1%, Chernivtsi 14.8%) show dramatically higher emigration rates than eastern cities (Kharkiv, Dnipro, Zaporizhzhia: near zero). The geographic concentration of emigration in western Ukraine reflects proximity to pre-existing Central European cultural networks and the delayed Soviet annexation of Galicia (1939).

**Figure 13:** Overlaid histograms of birth year (5-year bins) for all four migration groups. This figure serves as a methodological check on selection bias: if the groups were born in systematically different eras, between-group comparisons would conflate cohort effects with migration-status effects. The distributions overlap substantially across all groups, supporting the validity of the cross-group comparison.

**Figure 14:** Sensitivity analysis showing how the primary life expectancy gap adjusts under hypothetical AI classification error rates from 0% to 15%, assuming worst-case directional bias (all errors systematically misclassify the longest-lived migrants as non-migrants). The gap remains positive at every tested error rate. At the measured error rate of 3.2%, the adjusted gap is approximately +3.28 years. At a hypothetical 15% error rate — nearly five times the measured rate — the gap remains +0.83 years. The finding is robust across the full range of plausible error scenarios.

**Figure 15:** Direct comparison of mean age at death for the internal transfer group (n=1,150, mean=70.70 yrs) versus the non-migrated group (n=6,030, mean=71.22 yrs), with Mann-Whitney U p-value displayed. The near-zero gap (+0.52 yrs) and non-significant test result are the null finding that anchors the paper's interpretation: geographic mobility within the Soviet system conferred no survival benefit; leaving the Soviet sphere entirely was the operative variable.

**Figure 15b:** Box plots for all four groups with written statistical conclusions embedded as a text overlay. Explicitly notes which between-group comparisons are statistically significant and which are null, serving as a standalone interpretive summary: the migrated-versus-non-migrated and migrated-versus-deported contrasts are large and significant; the internal-transfer-versus-non-migrated contrast is not.

**Figure 16:** CONSORT-style flowchart documenting the exclusion cascade from 16,215 raw ESU entries to the 8,643 analysable dataset. Each exclusion step is labelled with its criterion and the resulting n. The final box shows the four-way group split. Provided for full methodological transparency and to enable reviewers and replicators to account for all inclusion and exclusion decisions.

**Figure 17:** Grouped bar chart showing gender composition (male, female, unknown) within each of the four migration groups. Provided as a demographic transparency check: if gender balance differed substantially across groups, between-group life expectancy comparisons could be confounded by the well-documented gender gap in longevity. Male workers predominate in all groups, consistent with the ESU's historical composition; the male-to-female ratio is broadly similar across groups.

**Figure 18:** Grouped bar chart showing mean age at death ±1 standard error, separately for male and female creative workers within each migration group. Values are labelled above each bar. The migrated-versus-non-migrated gap holds for both sexes, confirming that the primary finding is not an artefact of differential gender composition across groups.

**Figure 19:** Contextualisation chart placing creative workers' mean age at death by decade of death against published life expectancy estimates for Soviet-era populations: the Ukrainian SSR general population (1925–1985), the Russian SFSR (1955–1985), and the Baltic SSRs average (1955–1985). Data sources: Andreev et al. (1998),[^7] Meslé and Vallin (2002).[^7] Non-migrant creative workers track the Ukrainian SSR general population closely in most periods; the deported group falls well below all comparison populations during the Terror years.

**Figure 19b:** Multi-line chart of normalised annual death rate (deaths per year as a percentage of each group's total size, 2-year bins, 1921–1992, minimum n=5 per bin) for all four migration groups. Normalisation allows fair visual comparison across groups of very different absolute sizes. The deported group's line shows the sharpest spike in 1937, far exceeding the normalised rate of any other group in any year. The migrated group's line remains flat and low throughout the Soviet period.

**Figure 20:** Conservative two-group comparison collapsing non-migrated, internal transfer, and deported into a single "remained in Soviet sphere" group (n=7,363, mean=70.58 yrs) versus migrated (n=1,280, mean=75.25 yrs). The gap of +4.68 years (Cohen's d=0.330, p<0.001) is the most conservative possible framing of the primary finding, designed to address reviewer objections about the four-group model. Even in this worst-case framing for the authors, the gap remains substantial and statistically significant.

**Figure 21:** Contextualisation chart placing creative workers' mean age at death against published life expectancy estimates for comparable Soviet-era republic populations. Non-migrant Ukrainian creative workers track the Ukrainian SSR general population closely in most periods; the migrated group tracks Western European populations. The gap between these two reference populations is itself a measure of the mortality cost of Soviet conditions.

**Figure 22:** Comparison of creative workers' mean age at death (by decade of death, minimum n=5 per point) against an estimated educated urban Ukrainian baseline — the Ukrainian SSR general LE plus a 3–5 year educational mortality premium (shaded band), following Shkolnikov et al. (1998) on the Soviet educational gradient in mortality. This controls for the socioeconomic profile of the dataset population: creative workers were disproportionately educated and urban, which would predict above-average longevity absent political targeting. Non-migrants in repression periods fall below even the general population baseline, indicating an excess mortality attributable to Soviet cultural policy rather than demographic composition.'''

with open(PAPER, encoding='utf-8') as f:
    paper = f.read()

# Find and replace the entire §7 block
SECTION_7_START = '## 7. Figure Captions'
SECTION_8_START = '## 8. AI Methodology Note'

start_idx = paper.find(SECTION_7_START)
end_idx   = paper.find(SECTION_8_START)

if start_idx == -1 or end_idx == -1:
    print('ERROR: Could not locate §7 or §8 in PAPER_DRAFT.md')
else:
    new_paper = paper[:start_idx] + NEW_SECTION_7 + '\n\n---\n\n' + paper[end_idx:]
    with open(PAPER, 'w', encoding='utf-8') as f:
        f.write(new_paper)
    print('✓ PAPER_DRAFT.md §7 replaced with correctly-numbered captions (Figures 1–22 + 15b, 19b)')

print('\nDone. Run build_paper_html.py next to verify "Figures embedded: 24".')
