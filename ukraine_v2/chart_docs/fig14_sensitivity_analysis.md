# Fig 14 — Sensitivity Analysis: Finding Robustness vs AI Error Rate

**File:** `charts/fig14_sensitivity_analysis.png`

## What this chart shows
How the main LE gap (migrated vs non-migrated) would change if our AI classification had varying error rates — from 0% (perfect) to 10% (very bad). The x-axis is the hypothetical AI error rate; the y-axis is the resulting LE gap in years.

## Key finding
The finding remains statistically significant until the AI error rate exceeds **~8%**. Our actual measured error rate is **3.2%** (from Phase 5 human accuracy check). We have a comfortable margin.

## What to look for
- The horizontal dotted line = threshold where finding disappears (p>0.05)
- The shaded region = "finding still holds" zone
- The vertical line at 3.2% = our actual error rate — it sits safely in the "holds" zone
- The curve's slope — how sensitive is the finding to misclassification?

## Why this chart exists
A reviewer could ask: "What if your AI misclassified migration status for many people? Wouldn't that inflate the gap?" This chart preemptively answers that question. Even if the AI was 2.5x worse than it actually is, the finding would still hold.

## Technical note
Sensitivity analysis conducted by randomly flipping a % of migration status labels and re-running the Mann-Whitney U test 1,000 times at each error rate. The curve shows median gap across simulations.

## Known issues / improvements
- Clean chart, good scientific transparency.
- The x-axis label could read "Simulated AI misclassification rate (%)" for clarity.
- Adding a note "Our actual error rate: 3.2% (Phase 5 human review, n=63)" directly on the chart would make it fully self-contained.
