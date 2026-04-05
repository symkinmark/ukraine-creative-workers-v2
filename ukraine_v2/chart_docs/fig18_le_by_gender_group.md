# Fig 18 — Mean Life Expectancy by Gender and Migration Group

**File:** `charts/fig18_le_by_gender_group.png`

## What this chart shows
A grouped bar chart with migration group on the x-axis and mean LE on the y-axis, split by gender (blue = male, red = female). Error bars show ±1 standard error.

## Key finding (V2.2)
**Females consistently outlive males in every group** — matching the universal pattern seen in all modern populations. But crucially, the **LE gap between migrated and non-migrated holds for both sexes.** Even when you look only at men, or only at women, migrants lived longer. Gender doesn't explain the finding.

| Group | Male LE | n | Female LE | n |
|-------|---------|---|-----------|---|
| Migrated | 74.6 | 1,016 | 78.0 | 245 |
| Non-migrated | 70.9 | 5,067 | 73.7 | 909 |
| Internal transfer | 69.9 | 983 | 74.6 | 162 |
| Deported | 47.6 | 163 | 49.7 | 12 |

**Gap within males (migrated vs non-migrated): +3.7 yrs**
**Gap within females (migrated vs non-migrated): +4.3 yrs**

## What to look for
- Female bars are taller than male bars in every group (normal)
- The migration gap is visible within both male and female bars — gender doesn't drive it
- Deported bars are dramatically lower for both sexes (~47-50 yrs vs ~70-78 yrs for others)
- Deported female n=12 — error bars on that bar will be very wide; treat as directional only

## Why this chart matters
Gender-controlled robustness check. If sceptics argue that gender composition differences drive the LE gap, this chart shows the gap holds within each gender separately.

## Known issues / improvements
- Consider adding the male-only and female-only gap numbers (+3.7 / +4.3) as annotations between bars.
- Caption should note deported female n=12 so readers understand the wide CI.
