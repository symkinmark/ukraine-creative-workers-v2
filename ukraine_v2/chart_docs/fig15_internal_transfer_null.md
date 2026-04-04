# Fig 15 — Internal Transfer: Null Result Check

**File:** `charts/fig15_internal_transfer_null.png`

## What this chart shows
A focused comparison of the internal transfer group (people who moved within the USSR, not westward) against the non-migrated group. The question being asked: "Does moving around inside the USSR give any LE benefit similar to leaving entirely?"

## Key finding
**No significant difference** between internal transfer and non-migrated LE. This is a null result — and it's important. It supports the interpretation that *leaving the Soviet sphere specifically* was what mattered, not just "moving somewhere new."

## What to look for
- The bars should be close together with overlapping error bars (no real gap)
- This rules out "geographical mobility" as an explanation for the migrated group's advantage
- If internal movers had lived significantly longer, we'd need to rethink what's driving the main finding

## Why this null result matters
It's a key confound control. Someone could argue: "Maybe creative people who are active and mobile just live longer — nothing to do with leaving the USSR." The internal transfer group tests this: they were also mobile, but stayed inside the Soviet system — and their LE is the same as those who didn't move at all.

## ⚠️ Known bug — Y-axis goes negative
**Same bug as fig04 and fig06.** The Y-axis extends below zero, which is physically impossible for age at death.

**Fix needed:** Add `ax.set_ylim(bottom=0)` in `generate_analysis.py` for this chart.

Must fix before publication.
