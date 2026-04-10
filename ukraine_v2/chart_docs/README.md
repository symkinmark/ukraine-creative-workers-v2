# Chart Documentation Index
**Ukrainian Creative Workers V3.0 — Symkin 2026**

> **V3.0 CURRENT** — All charts regenerated on V2.6 dataset. N=8,590 analysable (migrated=1,324, non_migrated=5,960, internal_transfer=1,111, deported=195). Primary gap: +3.98 yrs, Cohen's d=0.292, Cliff's δ=0.18.
>
> **Paper restructured 2026-04-10:** Figures renumbered. 15 main-body figures (Fig 1–15) + 18 supplementary figures in Appendix A (Fig A1–A18). Chart **file names on disk** are unchanged (`fig01_...`, `fig02_...`); only the paper's reference numbers changed. See the renumbering table in `AI_METHODOLOGY_LOG.md` Phase 16.

One file per figure. Each explains: what the chart shows, the key finding, what to look for, and any known issues.

---

## Core Results
| File | Chart | What it is |
|---|---|---|
| [fig01](fig01_primary_le_comparison.md) | Primary Mean Age at Death Comparison | **THE headline result.** 4 bars, 4 groups, mean age at death |
| [fig02](fig02_kaplan_meier.md) | Kaplan-Meier Survival | Survival curves — probability alive at each age |
| [fig20](fig20_two_group_conservative.md) | Two-Group Conservative | Most sceptic-resistant framing: migrated vs everyone else |

## Dataset Validation & Transparency
| File | Chart | What it is |
|---|---|---|
| [fig03](fig03_version_comparison.md) | V1 vs V2.1 Version Comparison | Gap narrowed from +9.0→+5.4 yrs as dataset grew 15x |
| [fig13](fig13_birth_year_distribution.md) | Birth Year Distribution | Confound check — groups are generation-matched |
| [fig14](fig14_sensitivity_analysis.md) | Sensitivity Analysis | Finding holds until AI error rate >8% (ours is 3.2%) |
| [fig16](fig16_consort_flowchart.md) | CONSORT Flowchart | How 16,215 entries → 8,590 analysable (V2.3 updated) |

## Distribution & Shape
| File | Chart | What it is |
|---|---|---|
| [fig04](fig04_box_plots.md) | Box Plots | Distribution per group — ⚠️ Y-axis bug (goes negative) |
| [fig05](fig05_deported_age_histogram.md) | Deported Histogram | Zoom into just the deported group's age-of-death shape |
| [fig06](fig06_violin_plots.md) | Violin Plots | Like box plots but shows full shape — ⚠️ Y-axis bug |

## Temporal Analysis
| File | Chart | What it is |
|---|---|---|
| [fig07](fig07_death_year_histogram.md) | Death Year Histogram | When did each group die (calendar time) |
| [fig07b](fig07b_deported_death_year.md) | Deported Death Year Histogram | Deported group only: 1920–1960, 1937 spike dominant |
| [fig08](fig08_deported_deaths_by_year.md) | Deported Deaths by Year | Year-by-year deported deaths — 1937 spike visible |
| [fig09](fig09_nonmigrant_deaths_by_period.md) | Deaths by Soviet Period | Mean age at death per Soviet political era, all 4 groups |
| [fig10](fig10_birth_cohort_le.md) | Birth Cohort Mean Age at Death | Mean age at death by birth decade — cohort view |
| [fig19](fig19_ssr_population_context.md) | Normalised Annual Death Rate | % of each group dying per year 1921-1992 |

## Robustness Checks & Controls
| File | Chart | What it is |
|---|---|---|
| [fig15](fig15_internal_transfer_null.md) | Internal Transfer Null | Moving inside USSR gives no mean age at death benefit — ⚠️ Y-axis bug |
| [fig17](fig17_gender_by_group.md) | Gender Distribution | Male/female split per group — ⚠️ Raw counts misleading |
| [fig18](fig18_le_by_gender_group.md) | Mean Age at Death by Gender × Group | Gap holds for both men and women separately |

## Statistical Methods
| File | Chart | What it is |
|---|---|---|
| [fig23](fig23_regression_coef_plot.md) | Regression Coefficient Plot | OLS Models 1 & 2: migration gaps before and after controlling for cohort/profession/region |

## External Benchmarking
| File | Chart | What it is |
|---|---|---|
| [fig21](fig21_soviet_republic_comparison.md) | Soviet Republic Comparison | Our groups vs Baltic/Ukrainian/Russian/Central Asian SSR LE (e₀) |
| [fig22](fig22_educated_urban_comparison.md) | Educated Urban Comparison | Our groups vs estimated educated Ukrainian LE band (e₀) |

## Descriptive / Contextual
| File | Chart | What it is |
|---|---|---|
| [fig11](fig11_profession_grouped_bar.md) | Profession × Group | Migration rates differ by creative profession |
| [fig12](fig12_geographic_migration_rates.md) | Geographic Migration | Where the diaspora went |

---

## Known Bugs to Fix Before Publication
1. **fig04, fig06, fig15** — Y-axis extends below 0 (physically impossible). Fix: `ax.set_ylim(bottom=0)`
2. **fig02** — "V1 avg (63)" annotation is outdated. V2.3 non_migrated median is 73 yrs — update before submission.
3. **fig11** — No numeric labels on bars.
4. **fig17** — Raw counts mislead due to group size difference. Should be % within group.
5. **fig03** — Version comparison chart image may lag behind; description text updated to V2.3.
6. **All fig .md files** — Updated to V2.3 terminology and numbers 2026-04-06.

## V3.0 Status (2026-04-10)
- All charts regenerated on V2.6 dataset (Stages 12–15 corrections applied) ✅
- 33 static PNGs + 31 interactive Plotly HTMLs ✅
- Paper restructured with new figure numbering (15 main body + 18 appendix) ✅
- Chart file names on disk unchanged ✅
- 177/177 numeric claims in paper verified ✅
