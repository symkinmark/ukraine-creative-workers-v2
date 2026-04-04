# Fig 17 — Gender Distribution by Migration Group

**File:** `charts/fig17_gender_by_group.png`

## What this chart shows
Bar chart showing how many men, women, and unknowns are in each migration group. Answers: "Are the groups gender-balanced, or is one group more male/female?"

## Key finding
All groups are **male-dominated**, which is expected for this era and domain. Public creative workers in early-to-mid 20th century Ukraine were overwhelmingly men. Female representation is highest in the non-migrated group; lowest in the deported group.

## What to look for
- The massive non-migrated bar dwarfs the others — this is a raw count chart, and non-migrated is the largest group by far (n=4,625)
- The female bar is small but present in all groups
- Unknown/unclassified gender is minimal (Claude Haiku + rule-based engine covered ~99%)

## Why gender matters for the study
Men and women have different life expectancies in every population. If one migration group was predominantly female, that could partially explain LE differences. The gender breakdown shows groups are similarly male-dominated, so this confound is minimal. Fig18 controls for it explicitly.

## ⚠️ Readability issue
The non-migrated group (n=4,625) is so much larger than the others that the smaller groups' bars are barely visible at the same Y-axis scale. This makes the chart hard to use for comparing gender ratios across groups.

**Improvement:** Switch to **percentage within group** (% male / % female / % unknown) rather than raw counts. This would make all four groups directly comparable regardless of size difference.
