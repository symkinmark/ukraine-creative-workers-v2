# Fig 09 — Mean Age at Death by Soviet Historical Period

**File:** `charts/fig09_nonmigrant_deaths_by_period.png`

## What this chart shows
A grouped bar chart with **8 Soviet historical periods** on the x-axis and **mean age at death** on the y-axis. Each group (migrated, non-migrated, internal transfer, deported) gets its own bar per period, where enough data exists (n≥5 minimum). Bars with red outlines mark repression periods.

The 8 periods are:
1. NEP 1921-29 (relative liberalisation)
2. Holodomor 1930-33 (famine)
3. Terror 1934-38 (Stalinist purges)
4. WWII 1939-45
5. Late Stalin 1946-53
6. Thaw 1954-64 (post-Stalin liberalisation)
7. Stagnation 1965-91
8. Post-Soviet 1992+

## Key finding (V2.3)
Across **every period**, migrants who had left the USSR died older than those who stayed. The deported group shows catastrophically low mean ages in repression periods.

**V2.3 non-migrant period data (non-migrated n=5,960 total):**
| Period | Deaths | Avg age at death |
|--------|--------|-----------------|
| 1921–1929 (NEP) | 97 | 56.1 |
| 1930–1933 (Holodomor) | 53 | 59.1 |
| 1934–1938 (Great Terror) | 93 | 55.8 |
| 1939–1945 (WWII) | 196 | 55.3 |
| 1946–1953 (Late Stalin) | 120 | 62.1 |
| 1954–1964 (Thaw) | 234 | 66.4 |
| 1965–1991 (Stagnation) | 1,421 | 69.3 |
| Post-1991 | 3,692 | 74.7 |

**V2.3 deported Terror period (1934-38): n≈94, avg age ~43.5** — among the most extreme mortality concentration in the dataset. Deported group now n=195 total; period breakdown shifts marginally vs V2.2.

## What to look for
- **Missing bars** = that group had fewer than 5 deaths in that period (data suppressed for reliability)
- **Red-outlined bars** = the bar is in a repression period — this is where the state was actively killing people
- **Deported bars** are absent or very low in early periods (most were already dead)
- The migrated bar is consistently the tallest — even in the worst periods, diaspora who had already left lived longer

## How this differs from fig10
Fig09 is **period data** — it groups deaths by *when people died* (e.g., "who died during the Terror?"). Fig10 is **cohort data** — it groups by *when people were born* (e.g., "how long did people born in 1900 live?"). Different questions, different insights.

## Known issues / improvements
- Clean chart after redesign (removed the confusing raw-count top panel).
- Adding numeric labels to each bar (done) makes reading much easier.
- The n= values inside the bars help readers assess reliability.
