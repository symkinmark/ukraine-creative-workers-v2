# Fig 12 — Migration Rate by Birth City (Top 20)

**File:** `charts/fig12_geographic_migration_rates.png`

## What this chart shows
A horizontal bar chart showing the top 20 **birth cities** by total number of creative workers in the dataset. Each city has two overlaid bars: grey = total workers born there; blue = how many of those workers migrated (left the USSR). The percentage label on the right shows the migration rate out of that city.

This is NOT a destinations chart — it shows where people were **born**, and what fraction of them eventually migrated.

## Key finding (V2.3)
Kyiv and Lviv dominate by total volume. However, Lviv shows a notably **higher migration rate** than Kyiv — consistent with Lviv's historical position as part of interwar Poland (outside Soviet control until 1939), giving its residents different exit opportunities. Cities in western Ukraine generally show higher migration rates than eastern cities.

## What to look for
- The ratio between blue bar and grey bar = migration rate (% who left)
- Cities with a small grey bar but proportionally large blue bar = high-emigration communities
- Cities from western Ukraine (Lviv, Stanislaviv/Ivano-Frankivsk) vs eastern (Kharkiv, Poltava) — migration rates differ systematically
- Hover over each bar to see exact counts and migration percentage

## Historical context
Two main emigration waves:
1. **Interwar (1917–1939):** Left after the Ukrainian People's Republic fell to the Bolsheviks; cities in eastern Ukraine had less opportunity
2. **WWII / DP era (1941–1948):** Fled occupation, ended up in DP camps in Germany/Austria, resettled in USA/Canada/UK/Australia; western Ukrainian cities had higher exposure to this wave

## Update history
- **V2.3 (2026-04-06):** Description completely rewritten — previous version incorrectly described this as a destinations chart showing Germany/USA/France. The chart has always shown birth cities (origin), not destinations. Interactive Plotly version added (hover shows total n, migrated n, and migration rate %).
