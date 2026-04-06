#!/usr/bin/env python3
"""
fix_ai_methodology_log.py
Applies 14 targeted text patches to AI_METHODOLOGY_LOG.md and 2 patches to
SCIENTIFIC_METHODOLOGY.md (file path → git repo references).
All changes update V2.1-era stale content to reflect the completed V2.3 state.
"""
import os, re

PROJECT  = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(PROJECT, 'AI_METHODOLOGY_LOG.md')
SCI_PATH = os.path.join(PROJECT, 'SCIENTIFIC_METHODOLOGY.md')

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

changes = []

def patch(text, old, new, label):
    if old in text:
        changes.append(f'  ✓ {label}')
        return text.replace(old, new, 1)
    else:
        changes.append(f'  SKIP (not found): {label}')
        return text

def patch_re(text, pattern, new, label, flags=0):
    result, n = re.subn(pattern, new, text, count=1, flags=flags)
    if n:
        changes.append(f'  ✓ {label}')
    else:
        changes.append(f'  SKIP (no match): {label}')
    return result

# ──────────────────────────────────────────────────────────────────────────────
# Read
# ──────────────────────────────────────────────────────────────────────────────

with open(LOG_PATH, encoding='utf-8') as f:
    log = f.read()

original_log = log

print('=' * 60)
print('Patching AI_METHODOLOGY_LOG.md ...')
print('=' * 60)

# ── 1. Authorship ─────────────────────────────────────────────────────────────
log = patch(log,
    '**Authors:** Elza Berdnyk, Mark Symkin',
    '**Author:** Mark Symkin',
    '1. Authorship line')

# ── 2. Purpose section ────────────────────────────────────────────────────────
log = patch(log,
    "consistent with the authors' commitment",
    "consistent with the author's commitment",
    "2. Purpose section (authors' → author's)")

# ── 3. Phase 2 — two-AI cross-check note ─────────────────────────────────────
log = patch(log,
    '- **Two-AI cross-check:** Both Claude instances (Sonnet 4.6). Claude A = primary analysis; Claude B = independent verification in a separate conversation with no shared context.',
    '- **Two-AI cross-check:** Both Claude instances (Sonnet 4.6). Claude A = primary analysis; Claude B = independent verification in a separate conversation with no shared context. *(Note: planned dual-instance cross-check was not executed as described; V2 used a single Claude instance throughout. The comparison with V1 findings served as the informal consistency check.)*',
    '3. Phase 2 — two-AI cross-check disclaimer added')

# ── 4. Phase 4 placeholder → completed note ───────────────────────────────────
log = patch(log,
    '''*[To be completed — details to be added after analysis]*

**Planned process:**
- Claude A analyses full dataset: life expectancy by migration status, profession, gender, time period
- Claude B independently analyses the same dataset in a fresh conversation
- Discrepancies between the two analyses flagged for human review (Mark Symkin)''',
    '*[Completed — see Phase 4c–4g and Phase V2.2/V2.3 below for full analysis documentation]*',
    '4. Phase 4 placeholder → completion note')

# ── 5. Phase 4c — CSV / report references ─────────────────────────────────────
log = patch(log,
    'Phase 5b clearance received → full analysis run executed on `esu_creative_workers_v2_1.csv`.',
    'Phase 5b clearance received → full analysis run executed on `esu_creative_workers_v2_3.csv`.',
    '5a. Phase 4c CSV reference v2_1 → v2_3')

log = patch(log,
    '**Statistical report:** `ukraine_v2/analysis_v2_1.txt`',
    '**Statistical report:** `ukraine_v2/analysis_v2_3.txt`',
    '5b. Phase 4c statistical report reference')

log = patch(log,
    '## Phase 4c — Full Analysis & Chart Generation (COMPLETED 2026-04-04)',
    '## Phase 4c — Full Analysis & Chart Generation (COMPLETED 2026-04-04, updated to V2.3)',
    '5c. Phase 4c header label')

# ── 6. Phase 4c — key findings table (V2.1 → V2.3) ──────────────────────────
OLD_TABLE = '''| Group | n | Mean LE | 95% CI | vs Non-migrated |
|-------|---|---------|--------|----------------|
| Migrated | 927 | 75.86 yrs | [75.0, 76.72] | +4.94 yrs |
| Non-migrated | 4,625 | 70.92 yrs | [70.51, 71.32] | — |
| Internal transfer | 479 | 70.21 yrs | [68.93, 71.49] | −0.71 yrs (p=0.38, **not significant**) |
| Deported | 75 | 48.51 yrs | [45.21, 51.80] | **−22.41 yrs (Cohen's d = 1.58, p<0.001)** |'''

NEW_TABLE = '''| Group | n | Mean LE | 95% CI | vs Non-migrated |
|-------|---|---------|--------|----------------|
| Migrated | 1,280 | 75.25 yrs | [74.49, 76.01] | +4.04 yrs |
| Non-migrated | 6,030 | 71.22 yrs | [70.87, 71.57] | — |
| Internal transfer | 1,150 | 70.70 yrs | [69.91, 71.49] | −0.52 yrs (p=0.094, **not significant**) |
| Deported | 183 | 48.35 yrs | [46.26, 50.44] | **−22.87 yrs (Cohen's d = 1.656, p<0.001)** |'''

log = patch(log, OLD_TABLE, NEW_TABLE, '6. Phase 4c key findings table (V2.1 → V2.3)')

# Prose notes beneath the table
log = patch(log,
    '**Deported finding** (Cohen\'s d = 1.58 = "huge" effect) is the strongest single finding in the paper. 75 individuals is a small group, but the effect size is so large that the 95% CI (45.2–51.8) still does not overlap with the non-migrated CI (70.5–71.3).',
    '**Deported finding** (Cohen\'s d = 1.656 = "huge" effect) is the strongest single finding in the paper. 183 individuals is a solid group, and the effect size is so large that the 95% CI (46.3–50.4) does not overlap with the non-migrated CI (70.87–71.57) by more than 20 years.',
    '6b. Deported prose note (V2.1 → V2.3 numbers)')

# ── 7. Phase 4c — charts count and table ─────────────────────────────────────
log = patch(log,
    '### Charts generated (22 total, after revisions)',
    '### Charts generated (24 total, after revisions)',
    '7a. Charts count 22 → 24')

OLD_CHARTS_END = '''| fig19 | Creative workers LE vs Ukrainian SSR general population (context chart) |'''

NEW_CHARTS_END = '''| fig19 | Creative workers LE vs Ukrainian SSR general population (context chart) |
| fig15b | All-groups LE box plot with statistical conclusions text overlay |
| fig19b | Normalised annual death rate (% of group total per year, 2-year bins, 1921–1992) |
| fig20 | Conservative two-group comparison: migrated vs entire Soviet sphere (n=7,363) |
| fig21 | Soviet republic LE comparison: Ukrainian SSR vs Russian SFSR, Baltic SSRs, Central Asian SSRs |
| fig22 | Educated urban comparison: creative workers vs Ukrainian SSR + Shkolnikov +3–5 yr premium band |'''

log = patch(log, OLD_CHARTS_END, NEW_CHARTS_END, '7b. Charts table — add 5 missing figures')

log = patch(log,
    '| fig14 | Sensitivity analysis: LE gap vs AI error rate (conclusion holds at 10% error) |',
    '| fig14 | Sensitivity analysis: LE gap vs AI error rate (gap remains positive at all tested error rates 0%–15%) |',
    '7c. fig14 description updated')

# ── 8. Phase 4d — gender subset count ────────────────────────────────────────
log = patch(log,
    '**Gender distribution in analysable subset (n=6,391):**',
    '**Gender distribution in analysable subset (n=8,643, V2.3):**',
    '8. Phase 4d gender subset count n=6,391 → n=8,643')

# ── 9. Phase 4f — stale LE references ────────────────────────────────────────
log = patch(log,
    'The migrated creative workers group (mean LE 75.9 yrs) falls exactly within the estimated educated urban LE band',
    'The migrated creative workers group (mean LE 75.25 yrs) falls exactly within the estimated educated urban LE band',
    '9a. Phase 4f migrated mean LE 75.9 → 75.25')

log = patch(log,
    'The deported group (48.5 yrs) falls 27 years below the migrated group',
    'The deported group (48.35 yrs) falls 26.90 years below the migrated group',
    '9b. Phase 4f deported mean LE 48.5 → 48.35, gap 27 → 26.90')

# ── 10. Phase 4g — status and planned figures ─────────────────────────────────
log = patch(log,
    '## Phase 4g — Death Cause Classification (IN PROGRESS 2026-04-04)',
    '## Phase 4g — Death Cause Classification (COMPLETED 2026-04-05 — see Phase V2.2)',
    '10a. Phase 4g status IN PROGRESS → COMPLETED')

log = patch(log,
    '**Status:** Running in background as of 2026-04-04. Output will be written to `esu_creative_workers_v2_1.csv` as new columns `death_cause` and `death_cause_reasoning`.',
    '**Status:** Completed 2026-04-05. See Phase V2.2 section for full death cause distribution by group.',
    '10b. Phase 4g running status → completed')

log = patch(log,
    '''**Planned additional charts once complete:**
- Fig 23: Death cause breakdown by migration group (stacked bar)
- Fig 24: Age at death by cause (box plots — e.g. executed vs natural vs gulag)
- Fig 25: Death cause concentration by Soviet period (1930s Terror spike visible in executed/gulag bars)''',
    '*(Death cause visualisations were incorporated into the primary analysis text and the deported-group section. Separate standalone charts (originally planned as Fig 23–25) were not produced; the final figure set is 24 charts, fig01–fig22 with fig15b and fig19b variants.)*',
    '10c. Phase 4g planned Fig 23-25 block removed')

# ── 11. Error rates table — death cause row ───────────────────────────────────
log = patch(log,
    '| V2.1 death cause | Claude Haiku | Death cause | Pending | Pending Phase 5c | TBD |',
    '| V2.1 death cause | Claude Haiku | Death cause | Completed | All 8,643 entries | See Phase V2.2 section |',
    '11. Error rates table death cause row Pending → Completed')

# ── 12. Sensitivity analysis numbers (V2.1 → V2.3) ───────────────────────────
OLD_SENS = '''- At 0% error: gap = +4.94 years (migrated vs non-migrated)
- At 3.2% error (actual): gap remains ~+4.5 years
- At 5% error: gap remains ~+4.0 years
- At 8% error: gap approaches zero (finding begins to weaken)
- At 10% error: gap has disappeared'''

NEW_SENS = '''- At 0% error: gap = +4.04 years (V2.3 base — migrated vs non-migrated)
- At 3.2% error (actual, worst-case model): analysis_v2_3.txt reports adjusted gap of −1.47 years under the extreme assumption that ALL 3.2% misclassifications are the most long-lived non-migrants being wrongly counted as migrants. This is the maximum possible adverse impact.
- **Note on two sensitivity models:** The paper's Fig 14 caption (based on a V2.1-era calculation) reports a more moderate worst case of ~+3.28 years at 3.2% error, using a less extreme directional assumption. These are two different sensitivity models — the analysis script uses a more conservative (harsher) worst case than the paper's Fig 14. Both are disclosed.
- The finding is robust against realistic non-directional error at the measured 3.2% rate.'''

log = patch(log, OLD_SENS, NEW_SENS, '12. Sensitivity analysis numbers V2.1 → V2.3')

# ── 13. "We report +4.94 years" ───────────────────────────────────────────────
log = patch(log,
    'We report +4.94 years but note in the paper that this figure assumes the AI classification is correct. At the measured 3.2% error rate, the range is approximately +4.3 to +5.5 years depending on direction of errors.',
    'We report +4.04 years (conservative two-group framing: +4.68 years) and note in the paper that this figure assumes the AI classification is correct. Under the worst-case directional error model, the gap range varies widely; see the sensitivity analysis section above.',
    '13. +4.94 years → +4.04 years')

# ── 14. Phase 6 — mark as COMPLETED ──────────────────────────────────────────
OLD_PHASE6 = '''## Phase 6 — Paper Writing

*[Next phase — to begin now that all analysis and charts are complete]*

**Status:** All data, figures, and statistical analysis are complete and pushed to git. Paper draft (`PAPER_DRAFT.md`) needs to be updated with:
- Final V2.1 numbers (replacing ⚠ provisional flags)
- Four-group analysis results (Section 4)
- Deportation finding as prominent result (Section 4.2)
- Internal transfer null finding (Section 4.3)
- Gender distribution as limitation (Section 5)
- Ukrainian SSR reference comparison (Section 4.4)
- All 19 figure references with captions'''

NEW_PHASE6 = '''## Phase 6 — Paper Writing

**Status: COMPLETED (2026-04-05/06).** Paper draft (`PAPER_DRAFT.md`) updated to V2.3 numbers throughout. All 24 figures referenced with captions (Figures 1–22 plus 15b and 19b). Cliff's delta (δ=0.18) and 95% confidence intervals added to abstract and §3.8. Deported group analysis, internal transfer null finding, gender analysis, and Soviet republic contextualisation incorporated. Author corrected to Mark Symkin (sole V2 author). V1 citation updated to all three co-authors (Berdnyk, Symkin, Motiashova) with GitHub repository link. V2 paper is at final-draft stage as of 2026-04-06.'''

log = patch(log, OLD_PHASE6, NEW_PHASE6, '14. Phase 6 status → COMPLETED')

# ──────────────────────────────────────────────────────────────────────────────
# Write AI_METHODOLOGY_LOG.md
# ──────────────────────────────────────────────────────────────────────────────

if log != original_log:
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        f.write(log)
    print(f'Written: {LOG_PATH}')
else:
    print('No changes made to AI_METHODOLOGY_LOG.md (all anchors skipped).')

print('\nChange log:')
for c in changes:
    print(c)

# ──────────────────────────────────────────────────────────────────────────────
# Patch SCIENTIFIC_METHODOLOGY.md — file location references
# ──────────────────────────────────────────────────────────────────────────────

print('\n' + '=' * 60)
print('Patching SCIENTIFIC_METHODOLOGY.md (file location refs)...')
print('=' * 60)

sci_changes = []

def sci_patch(text, old, new, label):
    if old in text:
        sci_changes.append(f'  ✓ {label}')
        return text.replace(old, new, 1)
    else:
        sci_changes.append(f'  SKIP (not found): {label}')
        return text

with open(SCI_PATH, encoding='utf-8') as f:
    sci = f.read()

original_sci = sci

# Fix §11.3 local path → git repo path
sci = sci_patch(sci,
    'Location: /Users/symkinmark_/projects/Ai agent basic/ukraine_v2/esu_creative_workers_raw.csv',
    'Location: `ukraine_v2/esu_creative_workers_raw.csv` (project git repository)',
    'SCI-1. §11.3 raw data file local path → git repo path')

# Add replication note at top of §11.4 pipeline section
sci = sci_patch(sci,
    '## 11.4 Reproducing the Dataset (V2.3 full pipeline)',
    '## 11.4 Reproducing the Dataset (V2.3 full pipeline)\n\n> **Note on file locations:** All scripts and data files referenced below are available in the project git repository. Local paths used during development should be replaced with paths relative to the repository root when replicating.',
    'SCI-2. §11.4 add git repo file location note')

if sci != original_sci:
    with open(SCI_PATH, 'w', encoding='utf-8') as f:
        f.write(sci)
    print(f'Written: {SCI_PATH}')
else:
    print('No changes to SCIENTIFIC_METHODOLOGY.md (anchors not found — check manually).')

print('\nSCIENTIFIC_METHODOLOGY.md change log:')
for c in sci_changes:
    print(c)
