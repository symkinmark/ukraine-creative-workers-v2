# Fig 18 — Mean Life Expectancy by Gender and Migration Group

**File:** `charts/fig18_le_by_gender_group.png`

## What this chart shows
A grouped bar chart with migration group on the x-axis and mean LE on the y-axis, split by gender (blue = male, red = female). Error bars show ±1 standard error.

## Key finding
**Females consistently outlive males in every group** — matching the universal pattern seen in all modern populations. But crucially, the **LE gap between migrated and non-migrated holds for both sexes.** Even when you look only at men, or only at women, migrants lived longer. Gender doesn't explain the finding.

Approximate values:
| Group | Male LE | Female LE |
|---|---|---|
| Migrated | ~75.1 | ~79.5 |
| Non-migrated | ~70.4 | ~72.2 |
| Internal transfer | ~69.1 | ~72.5 |
| Deported | ~56.5 | ~60.5 |

## What to look for
- Female bars are taller than male bars in every group (normal)
- The gap between migrated and non-migrated is visible within both male and female bars
- Deported bars are dramatically lower for both sexes
- Error bars on deported are wide (small n) — treat those values as directional

## Why this chart matters
It's a gender-controlled robustness check. If you're sceptical that gender composition differences drive the result, this chart shows the gap holds even within each gender separately.

## Known issues / improvements
- Clean chart, no bugs.
- Consider adding the male-only and female-only gap numbers as annotations between bars.
- The deported error bars are large — worth flagging n in the caption.
