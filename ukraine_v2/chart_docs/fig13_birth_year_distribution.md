# Fig 13 — Birth Year Distribution by Group

**File:** `charts/fig13_birth_year_distribution.png`

## What this chart shows
Histogram of birth years for each migration group. Answers the question: "Are the groups comparable in age, or is one group systematically younger/older?" This is a confound check — if migrants were all born later (and thus died in a better medical era), that alone could explain longer lives.

## Key finding
All four groups have broadly overlapping birth year distributions, concentrated roughly 1860-1940. This means the groups are comparable in generation — the mean age at death difference cannot be explained simply by migrants being from a different birth era.

## What to look for
- Whether the distributions overlap substantially (they do)
- Whether any group is systematically offset to the right (younger births) or left (older births)
- The deported group may be slightly clustered in a narrower birth range — they represent a specific political target cohort (active cultural figures in the 1930s)

## Why this chart matters methodologically
If migrants were systematically younger, they would have benefited from modern medicine regardless of where they lived — and the mean age at death difference would be a statistical artifact, not a real effect. This chart shows that's not the case. Groups are generation-matched.

## Known issues / improvements
- Clean chart.
- Consider showing median birth year per group with a vertical line for easy comparison.
- Overlapping histograms can be hard to read — consider switching to KDE (kernel density) curves for clearer shape comparison.
