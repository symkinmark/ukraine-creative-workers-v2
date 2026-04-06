# Fig 10 — Birth Cohort Mean Age at Death by Birth Decade (Cohort Data)

**File:** `charts/fig10_birth_cohort_le.png`

## What this chart shows
Each data point = "people born in this decade, how long did they live?" This is **cohort analysis** — tracking groups of people born in the same era through their entire lives. The x-axis is decade of birth; the y-axis is mean age at death.

Minimum 10 people per data point (n≥10) — sparser points are suppressed.

## Key finding (V2.3)
People born in the **1890s–1910s** (who came of age during the Terror) show the starkest mortality differences. The deported line for 1890s births shows mean age at death of **44.6 years** (n=60) — the cohort most destroyed by the Executed Renaissance liquidations. The migrated line stays high across all birth decades.

**V2.3 key cohort values:**
| Birth decade | Migrated mean age at death (n) | Non-migrated mean age at death (n) | Deported mean age at death (n) |
|-------------|----------------|---------------------|----------------|
| 1880s | 73.8 (168) | 68.7 (260) | 56.7 (27) |
| 1890s | 75.2 (223) | 70.3 (326) | **44.6 (60)** |
| 1900s | 75.2 (209) | 72.4 (647) | 42.1 (54) |
| 1910s | 78.1 (207) | 75.0 (807) | 43.5 (13) |
| 1920s | 78.8 (164) | 75.4 (1,256) | n/a (<10) |

## What to look for
- The shaded region "Born 1890–1910: peak repression victim cohort" — this birth decade produced the people who were in their 30s-50s during the Terror (prime target age for Soviet authorities)
- Where lines are absent = not enough data to plot (n<10)
- The deported line drops off at later birth decades because very few deportees were born after 1920 and survived to provide data points
- The migrated line trends upward for later cohorts (later-born emigrants lived longer — they left earlier in the Soviet period, or survived into better medical eras)

## How this differs from fig09
Fig10 is **cohort data** (grouped by birth decade). Fig09 is **period data** (grouped by death decade). They ask different questions:
- Fig10: "Did being born in a certain era affect your total lifespan?"
- Fig09: "How old were people who died in a certain political period?"

## Known issues / improvements
- Clean after redesign (removed the Ukrainian SSR period data overlay, which was methodologically incompatible with cohort x-axis).
- The deported line drops sharply at the right side (1960s birth decade) — this reflects very sparse data (likely 10-15 people). Worth noting in the caption.

## Update history
- **V2.3 (2026-04-06):** Fixed overlapping numeric labels. Previous code used a per-index alternating above/below offset, which caused same-decade labels from different groups to stack on top of each other. Replaced with per-group fixed directions: migrated always up-left, non_migrated always down-right, internal_transfer up, deported down. Small x-nudge per group added to further separate annotations.
