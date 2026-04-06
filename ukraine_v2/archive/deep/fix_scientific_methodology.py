#!/usr/bin/env python3
"""
fix_scientific_methodology.py
Applies all 7 text patches to SCIENTIFIC_METHODOLOGY.md in one pass.
"""
import os, re

PROJECT = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PROJECT, 'SCIENTIFIC_METHODOLOGY.md')

with open(PATH, encoding='utf-8') as f:
    text = f.read()

original = text
changes = []

# ── 1. Fix authorship ─────────────────────────────────────────────────────────
OLD = '**Authors:** Elza Berdnyk, Mark Symkin'
NEW = '**Author:** Mark Symkin'
if OLD in text:
    text = text.replace(OLD, NEW, 1)
    changes.append('1. Fixed authorship')
else:
    changes.append('1. SKIPPED authorship (not found)')

# ── 2. Update §2.4 sample sizes to V2.3 ──────────────────────────────────────
OLD2 = (
    '- **Entries usable for primary life expectancy analysis '
    '(birth date + death date + determinable migration status + confirmed Ukrainian nationality):** 6,310\n'
    '- **Of which non-migrants:** 5,272\n'
    '- **Of which migrants:** 1,038\n'
    '- **Entries excluded due to living status (no death date):** the majority of the excluded 9,905 entries\n'
    '- **Entries excluded due to non-Ukrainian nationality:** 1,218 (after Claude review)\n'
    '- **Entries excluded due to indeterminate migration status:** several hundred'
)
NEW2 = (
    '- **Entries usable for primary life expectancy analysis '
    '(birth date + death date + determinable migration status + confirmed Ukrainian nationality):** 8,643 (V2.3)\n'
    '- **Of which non-migrants:** 6,030\n'
    '- **Of which migrants:** 1,280\n'
    '- **Of which internal transfers:** 1,150\n'
    '- **Of which deported:** 183\n'
    '- **Entries excluded due to living status (no death date):** the majority of the excluded entries\n'
    '- **Entries excluded due to non-Ukrainian nationality:** 1,218 (after Claude review)\n'
    '- **Entries excluded due to indeterminate migration status:** several hundred'
)
if OLD2 in text:
    text = text.replace(OLD2, NEW2, 1)
    changes.append('2. Updated §2.4 sample sizes to V2.3')
else:
    changes.append('2. SKIPPED §2.4 (exact block not found — check whitespace)')

# ── 3. Add Cliff's delta note after Cohen's d section ─────────────────────────
OLD3 = ('**Implementation:** Calculated using `numpy` operations in Python; '
        'verified against `pingouin.compute_effsize` for consistency.')
NEW3 = (OLD3 + '\n\n'
        '**Note on distributional assumptions:** Cohen\'s d benchmarks (0.2 small / '
        '0.5 medium / 0.8 large) assume normality and are applied here for '
        'comparability with prior literature. For this demonstrably non-normal '
        'distribution (see §8.4), the appropriate non-parametric effect size is '
        'Cliff\'s delta (δ), which is calculated in the companion analysis script '
        'and reported alongside Cohen\'s d in the paper. Cliff\'s delta measures '
        'P(migrant > non-migrant) − P(non-migrant > migrant) and requires no '
        'distributional assumptions.')
if OLD3 in text:
    text = text.replace(OLD3, NEW3, 1)
    changes.append("3. Added Cliff's delta note to §8.5")
else:
    changes.append("3. SKIPPED Cliff's delta note (anchor not found)")

# ── 4. Strengthen period analysis caveat in §8.6 ─────────────────────────────
OLD4 = ('**Note:** The period assignment is based on year of death, not year of '
        'persecution. An individual executed in 1937 (Great Terror) is assigned to '
        'that period. An individual who was arrested in 1937, survived the Gulag, '
        'and died in 1961 is assigned to the Khrushchev Thaw period — their death '
        'occurred then, even if their period of maximum persecution was earlier. '
        'This is a limitation of the period analysis: it does not capture the '
        'delayed mortality effects of repression.')
NEW4 = ('**Note — important caveat on death-year assignment:** Period assignment '
        'uses year of *death*, not year of *repression event*. An individual '
        'executed in 1937 is assigned to the Great Terror period (1934–1938). An '
        'individual arrested in 1937, who survived Gulag imprisonment and died in '
        '1961, is assigned to the Khrushchev Thaw period — even though their period '
        'of maximum persecution was 1937.\n\n'
        'This means the 1934–1938 Great Terror window **systematically undercounts** '
        'Terror-era deaths: workers arrested during the Terror but dying in Gulag '
        'camps throughout the 1940s and 1950s are spread across later period buckets. '
        'The period analysis captures direct executions and near-term deaths, not the '
        'full delayed mortality impact of repression. Readers should treat period '
        'death counts as lower bounds for repression-caused mortality in each window.')
if OLD4 in text:
    text = text.replace(OLD4, NEW4, 1)
    changes.append('4. Strengthened period analysis caveat in §8.6')
else:
    changes.append('4. SKIPPED period caveat (anchor not found)')

# ── 5. Add temperature replication note to §9.1 ──────────────────────────────
OLD5 = '**Temperature:** Default (1.0 for Claude models)'
NEW5 = ('**Temperature:** Default (1.0 for Claude models)\n\n'
        '**Replication note on temperature:** Temperature 1.0 introduces '
        'sampling randomness — two runs of the same prompt on the same input text '
        'may return different classification results. For a fully deterministic and '
        'reproducible classification pipeline, future replications should use '
        'temperature=0. Additionally, best practice is to run each classification '
        'twice and report inter-run agreement; this was not done in the present '
        'study. This is a known reproducibility limitation that should be addressed '
        'in future work.')
if OLD5 in text:
    text = text.replace(OLD5, NEW5, 1)
    changes.append('5. Added temperature replication note to §9.1')
else:
    changes.append('5. SKIPPED temperature note (anchor not found)')

# ── 6. Fix §10.4 stale V2.1 numbers ──────────────────────────────────────────
OLD6 = ('- There was a statistically robust and practically meaningful life '
        'expectancy gap of 4.77 years between Ukrainian creative workers who '
        'emigrated from the Soviet Union and those who remained, in a dataset of '
        '6,310 individuals.')
NEW6 = ('- There was a statistically robust and practically meaningful mean age at '
        'death gap of 4.04 years between Ukrainian creative workers who emigrated '
        'from the Soviet Union and those who remained, in a dataset of 8,643 '
        'individuals (V2.3).')
if OLD6 in text:
    text = text.replace(OLD6, NEW6, 1)
    changes.append('6. Fixed §10.4 V2.1 numbers → V2.3')
else:
    changes.append('6. SKIPPED §10.4 numbers (exact text not found — may need manual check)')

# ── 7. Add version history block after header ─────────────────────────────────
VERSION_BLOCK = """
## Version History

| Version | Date | Key change |
|---|---|---|
| 1.0 | 2025 | Initial V1 methodology (2-group, n=415, Harvard Masterclass) |
| 2.0 | 2026 | V2 expanded dataset (4-group, n=8,643), full AI disclosure |
| 2.1 | 2026-04-03 | Phase 5 human check; pre-1921 and Galicia filters added |
| 2.2 | 2026-04 | Author corrected to Mark Symkin; sample sizes updated to V2.3; Cliff's delta and CI added |

---
"""
HEADER_END = '> **V2.3 CURRENT.**'
if HEADER_END in text and '## Version History' not in text:
    # Insert version block before the V2.3 note
    text = text.replace(HEADER_END, VERSION_BLOCK + HEADER_END, 1)
    changes.append('7. Added version history block')
elif '## Version History' in text:
    changes.append('7. SKIPPED version history (already exists)')
else:
    changes.append('7. SKIPPED version history (anchor not found)')

# ── Write and report ──────────────────────────────────────────────────────────
if text != original:
    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'Written: {PATH}')
else:
    print('No changes made.')

print('\nChange log:')
for c in changes:
    print(f'  {c}')
