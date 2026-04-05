# Chart Documentation Index
**Ukrainian Creative Workers V2.2 — Berdnyk & Symkin 2026**

> ⚠️ **V2.2 DATA** — Charts regenerated 2026-04-05 from `esu_creative_workers_v2_2.csv` (n=8,830 analysable). Individual .md files may still reference V2.1 numbers in their "key finding" sections — treat those as approximate until each is updated. V2.2 headline: migrated:1,305 / non_migrated:6,157 / internal:1,179 / deported:189. LE gap: +4.03 yrs, Cohen's d = 0.288.

One file per figure. Each explains: what the chart shows, the key finding, what to look for, and any known issues.

---

## Core Results
| File | Chart | What it is |
|---|---|---|
| [fig01](fig01_primary_le_comparison.md) | Primary LE Comparison | **THE headline result.** 4 bars, 4 groups, mean LE |
| [fig02](fig02_kaplan_meier.md) | Kaplan-Meier Survival | Survival curves — probability alive at each age |
| [fig20](fig20_two_group_conservative.md) | Two-Group Conservative | Most sceptic-resistant framing: migrated vs everyone else |

## Dataset Validation & Transparency
| File | Chart | What it is |
|---|---|---|
| [fig03](fig03_version_comparison.md) | V1 vs V2.1 Version Comparison | Gap narrowed from +9.0→+5.4 yrs as dataset grew 15x |
| [fig13](fig13_birth_year_distribution.md) | Birth Year Distribution | Confound check — groups are generation-matched |
| [fig14](fig14_sensitivity_analysis.md) | Sensitivity Analysis | Finding holds until AI error rate >8% (ours is 3.2%) |
| [fig16](fig16_consort_flowchart.md) | CONSORT Flowchart | How 16,215 entries → 8,830 analysable (V2.2 updated) |

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
| [fig08](fig08_deported_deaths_by_year.md) | Deported Deaths by Year | Year-by-year deported deaths — 1937 spike visible |
| [fig09](fig09_nonmigrant_deaths_by_period.md) | Deaths by Soviet Period | Mean age at death per Soviet political era, all 4 groups |
| [fig10](fig10_birth_cohort_le.md) | Birth Cohort LE | LE by birth decade — cohort view |
| [fig19](fig19_ssr_population_context.md) | Normalised Annual Death Rate | % of each group dying per year 1921-1992 |

## Robustness Checks & Controls
| File | Chart | What it is |
|---|---|---|
| [fig15](fig15_internal_transfer_null.md) | Internal Transfer Null | Moving inside USSR gives no LE benefit — ⚠️ Y-axis bug |
| [fig17](fig17_gender_by_group.md) | Gender Distribution | Male/female split per group — ⚠️ Raw counts misleading |
| [fig18](fig18_le_by_gender_group.md) | LE by Gender × Group | Gap holds for both men and women separately |

## External Benchmarking
| File | Chart | What it is |
|---|---|---|
| [fig21](fig21_soviet_republic_comparison.md) | Soviet Republic Comparison | Our groups vs Baltic/Ukrainian/Russian/Central Asian SSR LE |
| [fig22](fig22_educated_urban_comparison.md) | Educated Urban Comparison | Our groups vs estimated educated Ukrainian LE band |

## Descriptive / Contextual
| File | Chart | What it is |
|---|---|---|
| [fig11](fig11_profession_grouped_bar.md) | Profession × Group | Migration rates differ by creative profession |
| [fig12](fig12_geographic_migration_rates.md) | Geographic Migration | Where the diaspora went |

---

## Known Bugs to Fix Before Publication
1. **fig04, fig06, fig15** — Y-axis extends below 0 (physically impossible). Fix: `ax.set_ylim(bottom=0)`
2. **fig02** — "V1 avg (63)" annotation is outdated. V2.2 non_migrated avg is ~65.x — update after death_cause pipeline completes.
3. **fig11** — No numeric labels on bars.
4. **fig17** — Raw counts mislead due to group size difference. Should be % within group.
5. **fig03** — Version comparison uses V2.1 gap (+5.4 yrs). V2.2 gap is +4.03 yrs — update description text.
6. **All fig .md files** — "Key finding" sections reference V2.1 numbers. Update each before submission.

## V2.2 Status (2026-04-05)
- Charts regenerated from V2.2 data ✅
- fig16 CONSORT numbers updated ✅
- repressed_names_for_review.csv regenerated (190 entries) ✅
- Death cause pipeline still running (~2,451 entries queued) — **regenerate charts one more time when done**
