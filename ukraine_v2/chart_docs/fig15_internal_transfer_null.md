# Fig 15 — Internal Transfer: Null Result Check

**File:** `charts/fig15_internal_transfer_null.png`

## What this chart shows
A focused comparison of the internal transfer group (people who moved within the USSR, not westward) against the non-migrated group. The question being asked: "Does moving around inside the USSR give any LE benefit similar to leaving entirely?"

## Key finding (V2.3)
**Near-null difference** between internal transfer and non-migrated LE: gap = +0.52 yrs (V2.3), Cohen's d ≈ 0.037. The effect size is negligible — essentially zero. This supports the interpretation that *leaving the Soviet sphere specifically* was what mattered, not just "moving somewhere new."

- Internal transfer mean LE: 70.70 yrs (n=1,150)
- Non-migrated mean LE: 71.22 yrs (n=6,030)
- Gap: +0.52 yrs vs **+4.04 yrs** for migrated vs non-migrated

Note: gap direction inverted slightly vs V2.2 (+0.96 → +0.52) because internal_transfer mean rose more than non-migrated. Null result conclusion unchanged.

## What to look for
- The bars should be close together with overlapping error bars (no real gap)
- This rules out "geographical mobility" as an explanation for the migrated group's advantage
- If internal movers had lived significantly longer, we'd need to rethink what's driving the main finding

## Why this null result matters
It's a key confound control. Someone could argue: "Maybe creative people who are active and mobile just live longer — nothing to do with leaving the USSR." The internal transfer group tests this: they were also mobile, but stayed inside the Soviet system — and their LE is the same as those who didn't move at all.

## ⚠️ Y-axis bug — check generate_analysis.py
fig04 and fig06 Y-axis bugs were fixed. Verify fig15 also has `ax.set_ylim(bottom=0)` before final publication.
