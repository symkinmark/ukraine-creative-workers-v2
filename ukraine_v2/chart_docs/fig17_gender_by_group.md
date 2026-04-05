# Fig 17 — Gender Distribution by Migration Group

**File:** `charts/fig17_gender_by_group.png`

## What this chart shows
Bar chart showing how many men, women, and unknowns are in each migration group. Answers: "Are the groups gender-balanced, or is one group more male/female?"

## Key finding
All groups are **male-dominated**, which is expected for this era and domain. Public creative workers in early-to-mid 20th century Ukraine were overwhelmingly men. Female representation is highest in the non-migrated group; lowest in the deported group.

**V2.3 gender breakdown:**
| Group | Total | Male | Female | Unknown |
|-------|-------|------|--------|---------|
| Non-migrated | 6,030 | ~5,102 (85%) | ~911 (15%) | ~17 (<1%) |
| Migrated | 1,280 | 1,022 (80%) | 246 (19%) | ~12 (1%) |
| Internal transfer | 1,150 | ~978 (85%) | ~162 (14%) | ~10 (1%) |
| Deported | 183 | 167 (91%) | 13 (7%) | 3 (2%) |

## What to look for
- The deported group is the most male-dominated (92%) — reflecting that the Soviet state specifically targeted male cultural leaders
- Female % is highest in migrated (19%) — women who emigrated faced fewer barriers in exile
- Unknown/unclassified gender is minimal (<1% in most groups)

## Why gender matters for the study
Men and women have different life expectancies in every population. If one migration group was predominantly female, that could partially explain LE differences. The gender breakdown shows groups are similarly male-dominated, so this confound is minimal. Fig18 controls for it explicitly.

## ⚠️ Readability issue
The non-migrated group (n=6,030) is so much larger than the others that the smaller groups' bars are barely visible at the same Y-axis scale.

**Fix before publication:** Switch to **percentage within group** (% male / % female / % unknown) rather than raw counts. This makes all four groups directly comparable regardless of size.
