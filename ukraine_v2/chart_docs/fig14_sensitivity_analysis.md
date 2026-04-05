# Fig 14 — Sensitivity Analysis: Finding Robustness vs AI Error Rate

**File:** `charts/fig14_sensitivity_analysis.png`

## What this chart shows
How the main LE gap (migrated vs non-migrated) would change if our AI classification had varying error rates — from 0% (perfect) to 15% (very bad). The x-axis is the hypothetical AI error rate; the y-axis is the resulting LE gap in years.

## Key finding (V2.2)
The finding remains positive even at unrealistically high error rates. Our actual measured error rate is **3.2%** (Phase 5 human accuracy check, n=63). The gap under various error scenarios:

| Simulated error rate | Adjusted gap |
|---------------------|-------------|
| 0% (perfect) | +4.03 yrs |
| 3% (≈ our actual) | +3.27 yrs |
| 5% | +2.85 yrs |
| 8% | +2.23 yrs |
| 10% | +1.82 yrs |
| 15% | +0.82 yrs |

At our actual 3.2% error rate the gap is +3.27 yrs. Even at 15% error — nearly 5× worse than reality — a positive gap remains. The finding does not disappear at any plausible error rate.

**Note:** The worst-case assumption is used throughout: all misclassifications are the most long-lived migrants being incorrectly counted as migrated (most unfavourable direction for the finding).

## What to look for
- The gap at our 3.2% actual error rate: still +3.27 yrs
- The curve stays positive across the entire realistic range
- Steeper slopes = more sensitive findings; this curve is gradual (robust)

## Why this chart exists
A reviewer could ask: "What if your AI misclassified migration status for many people? Wouldn't that inflate the gap?" This chart preemptively answers that question. Even if the AI was 5× worse than it actually is, a meaningful gap would remain.

## Technical note
Sensitivity analysis conducted by moving the top X% of migrants (longest-lived) to the non-migrated group and recalculating the gap. Conservative worst-case directional assumption.

## Known issues / improvements
- The x-axis label could read "Simulated AI misclassification rate (%)" for clarity.
- Adding a note "Our actual error rate: 3.2% (Phase 5 human review, n=63)" directly on the chart would make it fully self-contained.
