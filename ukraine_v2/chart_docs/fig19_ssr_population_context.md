# Fig 19 — Annual Death Rate by Group, 1921-1992 (Normalised)

**File:** `charts/fig19_ssr_population_context.png`

## What this chart shows
A time-series line chart showing the **% of each group dying per year** from 1921 to 1992. Each data point = (deaths in group that year) ÷ (total group size) × 100. This normalises for the fact that groups are different sizes — so you're seeing mortality rate, not raw death count.

## Key finding
**The deported group shows a catastrophic mortality spike during 1938-1945** — at its peak, roughly 25-30% of all deportees died in a single year. This is the Great Terror and WWII combined. The other groups show relatively flat lines throughout. The deported spike is so severe it dominates the entire chart visually.

## What to look for
- The deported line (dark/purple) spiking violently in 1938-1943
- All other lines staying close to 0-2% per year — normal background mortality
- The shaded period labels (Holodomor, Great Terror, WWII, Late Stalin) — these mark which historical crises produced which mortality spikes
- After 1950, the deported line returns to flat (near-zero) because most deportees were already dead

## Why normalisation was necessary
Earlier version of this chart showed raw death counts. The problem: non-migrated has n=4,625 vs deported n=75. A raw count chart would show a huge non-migrated bar simply because there are more of them — which would make the deported catastrophe invisible. Normalising to % lets you compare fairly.

## Known issues / improvements
- Clean after redesign. No bugs.
- The note at the bottom explaining normalisation is essential — make sure it's legible at all print sizes.
- Consider adding numeric peak labels on the deported spike (e.g., "~28% per year, 1940").
