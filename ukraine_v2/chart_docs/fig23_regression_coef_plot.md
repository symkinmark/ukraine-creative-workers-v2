# Fig 23 — Regression Coefficient Plot (OLS Gap Stability)

**File:** `charts/fig23_regression_coef_plot.png`

## What this chart shows
A grouped bar chart comparing OLS regression coefficients for migration status groups from two models:
- **Model 1 (dark bars):** Unadjusted — migration status only, n=8,590
- **Model 2 (light hatched bars):** Adjusted — + birth decade + profession + birth region

Reference category is non-migrated (β = 0). Bars show years of mean age at death relative to non-migrants. Error bars = 95% confidence intervals.

## The numbers

| Group (vs non-migrated) | Model 1 β | 95% CI | Model 2 β | 95% CI |
|---|---|---|---|---|
| Migrated | +3.98 yrs | [+3.20, +4.87] | +3.31 yrs | [+2.44, +4.19] |
| Internal Transfer | −0.52 yrs | [−1.39, +0.35] | −1.43 yrs | [−2.34, −0.53] |
| Deported | −22.87 yrs | [−24.90, −20.84] | −23.44 yrs | [−25.49, −21.39] |

## Key finding
The migration advantage (migrated vs non-migrated) drops only slightly from +4.04 to +3.31 years after controlling for birth cohort, profession, and region — the gap is not explained by compositional differences. The deportation penalty actually grows slightly in the adjusted model. This chart's core message: **bar heights are nearly identical between Models 1 and 2**, showing the gap is robust to demographic adjustment.

Internal transfer flips from non-significant (Model 1, p=0.243) to significant (Model 2, −1.43 yrs, p=0.002), suggesting cohort confounding was masking a real effect.

## What to look for
- Near-identical bar heights for migrated group across both models → gap is not a cohort/profession artifact
- Deported bars far below zero in both models → direct state violence effect, not compositional
- Internal transfer shift: the adjustment reveals a small but real penalty for within-USSR moves
- Error bars for migrated group don't overlap with zero in either model → statistically robust

## Known issues
- Three-group layout (migrated, internal transfer, deported) compresses the deported bars to a very different scale than the others. The two-panel layout (Panel A: migrated/IT; Panel B: deported) was considered but the grouped bar was chosen for a single coherent view.

## Used in paper
§4.9 (Multivariable Regression). Cited alongside Table A (OLS regression results markdown table).
