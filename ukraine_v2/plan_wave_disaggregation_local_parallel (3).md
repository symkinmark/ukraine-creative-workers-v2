# Plan: Emigration Wave Disaggregation
## Local Parallel Execution — No API Calls, ~30 Concurrent Workers

---

## The Problem

The study's central finding is a 4.04-year gap in mean age at death between Ukrainian
creative workers who emigrated from the Soviet Union (n=1,280, mean age at death 75.25
years) and those who remained (n=6,030, mean age at death 71.22 years). The study argues
this gap is evidence of a Soviet mortality penalty — that staying within the Soviet sphere
shortened the lives of Ukrainian creative workers relative to what they would have
experienced had they left.

The problem is that "emigrated" is not a single coherent category. It is a label applied
to three historically distinct populations who left Ukraine under radically different
circumstances, at different points in history, through different mechanisms, and who
arrived in very different material conditions afterward. Treating them as one group and
computing a single mean age at death conceals enormous internal variation that could
either strengthen or completely undermine the paper's argument, depending on what
that variation looks like.

The three populations hidden inside the "migrated" category are:

**First-wave emigrants (before 1922).** These are individuals who fled during or
immediately after the Russian Civil War, typically alongside or in the wake of the
Ukrainian People's Republic (UNR) military collapse. They were disproportionately from
the educated landowning, professional, and ecclesiastical classes — people with the
resources, foresight, and foreign contacts to leave before Bolshevik consolidation made
departure impossible. They settled primarily in Prague, Vienna, Paris, Warsaw, and later
North America, often within established Ukrainian diaspora communities and with access
to European intellectual networks. Their emigration was planned or semi-planned. They
did not experience the Holodomor, the Great Terror, or World War II on Ukrainian soil.
They were, as a group, positively selected for health, social capital, and life
expectancy in ways that had nothing to do with Soviet conditions.

**Second-wave emigrants (1939–1945).** These are individuals displaced during World War
II. Some left when Soviet forces first annexed western Ukraine in 1939–1941 under the
Molotov-Ribbentrop Pact. The majority fled westward with retreating German forces in
1943–1944, or escaped during the chaotic period of German occupation. They ended up in
Displaced Persons (DP) camps in Germany, Austria, and Italy — conditions that involved
severe malnutrition, disease exposure, overcrowding, psychological trauma from flight,
and substantial mortality before resettlement. Many spent years in DP camps before
reaching Canada, the United States, Australia, or South America. Unlike the first wave,
their emigration was reactive, terrifying, and materially devastating. A significant
fraction of those who attempted to flee did not survive the attempt and therefore do not
appear in the migrant group at all — they are absent from both groups, creating a
survivorship bias within the migrant category that suppresses the apparent mortality cost
of second-wave flight.

**Third-wave emigrants (1945–1991).** These are the Cold War-era emigrants: DP camp
survivors who resettled in the West after the war, Cold War defectors, dissidents who
managed to leave during the Thaw or later periods, and family reunification emigrants.
They experienced Soviet conditions for longer than the first wave but shorter than
non-migrants, and their emigration was typically possible only for individuals with
unusual courage, political capital, or luck. They are a self-selected group in yet a
different way — not selected for wealth and social position like the first wave, but
selected for political prominence, risk tolerance, and often for having already been
targeted by the Soviet state (making their lives in the Soviet Union dangerous but
also giving them reason to flee).

The critical analytical problem is this: **if the 4.04-year gap between migrants and
non-migrants is driven entirely by the first-wave emigrants** — who were selected for
privilege, health, and European social networks before Soviet conditions became fully
operative — **then the gap may reflect who chose to emigrate, not what the Soviet Union
did to those who stayed.** This would be a major threat to the paper's interpretation.
Conversely, **if the gap holds across all three waves** — including the second wave, who
experienced terrible material conditions during and after flight, and the third wave,
who lived under Soviet rule for much of their lives — **then the argument that Soviet
conditions drove the gap becomes dramatically more credible.** You cannot explain a
consistent mortality advantage across three groups with three completely different
selection mechanisms and three completely different emigration experiences by appealing
to a single pre-migration selection bias. The waves act, in effect, as natural
replications of the core comparison under different confounding structures.

There is an additional sub-problem specific to the second wave. Some individuals in the
dataset classified as "migrated" may have left Ukraine during the German occupation and
then returned — making them non-migrants who briefly appeared to be migrants. Others
were forcibly removed by German forces rather than voluntarily fleeing, which raises
questions about whether their emigration should be treated as the same kind of event
as voluntary departure. These edge cases are currently invisible inside the monolithic
migrant category and need explicit rules before wave classification begins.

---

## The Result Needed

The output of this plan is a new column in the primary dataset — `emigration_wave` —
populated for all 1,280 migrants, assigning each to WAVE1, WAVE2, WAVE3, WAVE4
(post-Soviet, excluded from primary analysis), or UNKNOWN (unresolvable).

From that column, the following must be computable:

**A wave-level descriptive table** reporting, for each wave and for non-migrants as
the reference group: n, mean age at death with 95% confidence interval, median age at
death, standard deviation, percentage dying before age 50, and percentage surviving
to age 80 or older. This table replaces the current two-row migrant/non-migrant
summary with a four-row breakdown that makes the internal heterogeneity of the migrant
group visible.

**Wave-specific statistical tests** — Mann-Whitney U, Cohen's d, Cliff's delta — for
each wave against the non-migrant reference group. Each wave needs its own p-value and
effect size. If any wave produces a non-significant result (p > 0.05) or a gap near
zero, that is a finding that must be reported and explained, not hidden.

**A regression model** with wave as a four-level factor, controlling for birth decade,
profession, and birth region, so that the gap for each wave can be stated after
adjustment for cohort composition. This is important because waves have systematically
different mean birth years — first-wave emigrants are older on average, which could
artificially inflate their mean age at death independent of emigration effects.

**A Kaplan-Meier figure** showing all four waves as separate survival curves alongside
the non-migrant reference curve. This figure should make visually immediate whether
the curves separate consistently or whether one wave drives the divergence.

**A written interpretation** — for inclusion in §5.1 (Interpreting the Mortality Gap)
and §5.4 (Limitations) — that states clearly what the wave-level results imply for the
self-selection critique. If the gap holds across waves: the paper's argument is
substantially strengthened and the self-selection critique is materially weakened.
If the gap is concentrated in one wave: the paper must narrow its claims and explain
why that specific wave shows the effect.

The result is not a new finding layered on top of the existing analysis. It is a
direct test of whether the existing finding survives disaggregation. The paper is
currently making a claim about migrants as a whole. This plan checks whether that
claim is valid by asking whether the sub-groups inside "migrants" all point in the
same direction.

---

## Why We Are Doing This

This plan exists because the paper's primary inferential vulnerability — the one a
peer reviewer or critic will identify first — is emigration self-selection bias. The
argument runs as follows: maybe Ukrainian creative workers who emigrated simply had
characteristics, prior to emigration, that independently predicted longer lives. Maybe
they were healthier, wealthier, better connected, less likely to drink heavily, less
likely to have pre-existing illness, more psychologically resilient. Maybe the 4.04-year
gap is not evidence of what the Soviet Union did to those who stayed — it is evidence
of who was capable of leaving in the first place. If this critique is correct, the
paper's historical argument collapses: you cannot use a mortality gap driven by
pre-existing population differences to make claims about Soviet mortality policy.

The paper currently responds to this critique with propensity score matching and
regression adjustment on birth decade, profession, and birth region. These adjustments
reduce the gap from 4.04 to 3.35 years, which the paper offers as evidence that the
gap is not simply an artefact of observable compositional differences. But this response
has a well-known limitation: propensity score matching only adjusts for observed
confounders. Unobserved confounders — health, social capital, political awareness,
pre-existing wealth — remain. A skeptic can always say: "You matched on birth decade
and profession, but you didn't match on the things that actually drove both emigration
and longevity."

Wave disaggregation offers something that statistical adjustment cannot: a structural
argument. The three emigration waves selected individuals through completely different
mechanisms. First-wave selection favored the pre-revolutionary social elite. Second-wave
selection was largely forced by the collapse of military fronts and involved severe
material hardship during and after flight. Third-wave selection favored Cold War-era
political dissidents and defectors. If all three waves — despite these radically
different selection mechanisms — show longer survival than non-migrants, it becomes
implausible that a single unobserved pre-migration characteristic can explain all three
gaps simultaneously. What kind of characteristic would make someone simultaneously
(a) wealthy enough to flee in 1919, (b) willing to endure DP camps in 1944, and (c)
politically prominent enough to defect in 1968, and in all three cases independently
predict longer survival? The argument requires a confounder that operates identically
across three historically incommensurable selection processes. That is a much harder
case to make than the standard selection argument, which implicitly assumes a single
homogeneous emigrant population.

This is why wave disaggregation strengthens the paper beyond what any statistical
adjustment can achieve. Statistics can control for what you measure. Structural
argument — showing that the effect is consistent across groups defined by different
causal mechanisms — addresses what you cannot measure. The paper currently has the
statistics. This plan adds the structure.

There is a secondary reason this matters for the paper's honesty. If wave disaggregation
reveals that the gap is driven by the first wave only, the paper needs to know this and
say so. Concealing it would not make the paper better — it would make it wrong. A paper
that honestly reports "the gap is concentrated in first-wave emigrants and is near zero
for second and third wave" is a more credible and more useful contribution than a paper
that claims a uniform 4.04-year effect that doesn't actually exist across sub-groups.
The disaggregation either confirms the finding or corrects it. Both outcomes are
scientifically valuable.

---

**Core approach:** Chunk the 1,280 migrated entries into ~30 roughly equal batches (~43
entries each), run a local LLM (Ollama) on each batch in a separate terminal process,
merge outputs, then validate and compute statistics in a final pass.

All steps run entirely in the terminal. No internet connection required after initial
model pull.

---

## Prerequisites — Do This Once Before Anything Else

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model — llama3.1:8b balances speed and Ukrainian text comprehension
# For better Ukrainian: mistral-nemo or aya-expanse:8b (multilingual)
ollama pull llama3.1:8b
# Fallback multilingual option if llama3.1 struggles with Ukrainian text:
# ollama pull aya-expanse:8b

# Confirm it runs
ollama run llama3.1:8b "respond only with the word OK"

# Install Python deps (all standard)
pip install pandas numpy scipy tqdm --break-system-packages
```

---

## Step 1 — Define Wave Taxonomy and Write It Down First

Before touching data, lock in the boundaries in a plain text file.
This file becomes the ground truth for all 30 workers — they all read the same rules.

```bash
cat > wave_rules.txt << 'EOF'
WAVE CLASSIFICATION RULES
==========================

WAVE 1 — FIRST WAVE
  Date range: emigration before 1922-01-01
  Context: Flight from Bolshevik consolidation; UNR retreat; Russian Civil War
  Keywords in text: "емігрував 191", "виїхав 191", "після поразки УНР",
                    "з арміями УНР", "під час громадянської війни"

WAVE 2 — SECOND WAVE
  Date range: 1939-01-01 to 1945-05-08
  Context: WWII displacement; Soviet annexation 1939-41; westward flight 1943-44
  Keywords: "під час Другої світової", "виїхав 194", "опинився на Заході",
             "табір переміщених осіб", "ДП табір", "з відступом німецьких"
  EDGE CASE A: Left during German occupation AND returned → NOT a migrant, reclassify
  EDGE CASE B: Forcibly removed by Germans → still classify as Wave 2 if settled West

WAVE 3 — THIRD WAVE
  Date range: 1945-05-09 to 1991-12-31
  Context: DP camp survivors resettled West; Cold War defectors; dissidents
  Keywords: "після війни емігрував", "залишився на Заході", "виїхав у 195/196/197/198"

WAVE 4 — POST-SOVIET
  Date range: 1992-01-01 onward
  Context: Post-independence emigration — EXCLUDE from primary analysis
  Flag these for a separate control group, do not include in gap calculation

UNKNOWN
  Use when: no emigration date or period can be inferred at all
  These entries are retained in the overall migrant aggregate but excluded
  from wave-level breakdowns.
EOF
```

---

## Step 2 — Prepare and Chunk the Data

```bash
# Assumes your dataset is esu_creative_workers_v2_3.csv
# Filter to migrated group only and split into 30 chunks

python3 << 'EOF'
import pandas as pd
import numpy as np
import os

df = pd.read_csv('esu_creative_workers_v2_3.csv')
migrants = df[df['migration_status'] == 'migrated'].copy()
migrants = migrants.reset_index(drop=True)

print(f"Total migrants: {len(migrants)}")

os.makedirs('chunks', exist_ok=True)
chunks = np.array_split(migrants, 30)

for i, chunk in enumerate(chunks):
    chunk.to_csv(f'chunks/chunk_{i:02d}.csv', index=False)
    print(f"Chunk {i:02d}: {len(chunk)} rows")
EOF
```

---

## Step 3 — Write the Extraction Script

This script processes one chunk. It will be called 30 times in parallel,
each on a different chunk file. It reads each row, queries Ollama locally,
and writes results to a corresponding output file.

```bash
cat > extract_wave.py << 'PYEOF'
#!/usr/bin/env python3
"""
Usage: python3 extract_wave.py <chunk_file> <output_file>
Processes one chunk of migrated entries and classifies emigration wave.
Reads wave_rules.txt for context. Queries Ollama locally.
"""

import sys
import json
import subprocess
import pandas as pd
import time

CHUNK_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
RULES = open('wave_rules.txt').read()
MODEL = 'llama3.1:8b'

PROMPT_TEMPLATE = """You are classifying Ukrainian emigration timing from encyclopedic text.

Rules for wave assignment:
{rules}

Entry to classify:
Name: {name}
Birth year: {birth_year}
Death year: {death_year}
Biographical text: {bio_text}

Respond ONLY with a JSON object, no other text, using this exact structure:
{{
  "emigration_year_est": <integer year or null>,
  "emigration_year_range": [<earliest int or null>, <latest int or null>],
  "wave": "<WAVE1|WAVE2|WAVE3|WAVE4|UNKNOWN>",
  "confidence": "<HIGH|MEDIUM|LOW>",
  "evidence_quote": "<verbatim phrase from text that grounds estimate, or null>",
  "edge_case_flag": "<RETURNED|FORCED|null>"
}}"""

def query_ollama(prompt, retries=3):
    for attempt in range(retries):
        try:
            result = subprocess.run(
                ['ollama', 'run', MODEL, prompt],
                capture_output=True, text=True, timeout=60
            )
            raw = result.stdout.strip()
            # Extract JSON block if surrounded by extra text
            start = raw.find('{')
            end = raw.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(raw[start:end])
        except (json.JSONDecodeError, subprocess.TimeoutExpired) as e:
            print(f"  Attempt {attempt+1} failed: {e}", flush=True)
            time.sleep(2)
    # Return failure record rather than crashing
    return {
        "emigration_year_est": None,
        "emigration_year_range": [None, None],
        "wave": "UNKNOWN",
        "confidence": "LOW",
        "evidence_quote": None,
        "edge_case_flag": None,
        "extraction_failed": True
    }

df = pd.read_csv(CHUNK_FILE)
results = []

for i, row in df.iterrows():
    bio = str(row.get('bio_text_uk', row.get('bio_text', '')))[:3000]  # truncate long texts
    prompt = PROMPT_TEMPLATE.format(
        rules=RULES,
        name=row.get('name_uk', row.get('name', 'Unknown')),
        birth_year=row.get('birth_year', 'unknown'),
        death_year=row.get('death_year', 'unknown'),
        bio_text=bio
    )

    print(f"[{CHUNK_FILE}] Row {i}: {row.get('name', '?')}", flush=True)
    result = query_ollama(prompt)
    result['original_index'] = row.name
    result['name'] = row.get('name', '')
    results.append(result)

out = pd.DataFrame(results)
out.to_csv(OUTPUT_FILE, index=False)
print(f"[DONE] {CHUNK_FILE} → {OUTPUT_FILE} ({len(results)} rows)", flush=True)
PYEOF

chmod +x extract_wave.py
```

---

## Step 4 — Launch 30 Workers in Parallel

Each worker gets its own terminal via `tmux` panes, or you can use `parallel`
if you prefer a single terminal. Both options are shown.

### Option A — tmux (recommended, you can watch all 30 live)

```bash
# Create a new tmux session with 30 panes
tmux new-session -d -s wave_extraction

# Split into 30 panes and launch each worker
for i in $(seq -w 0 29); do
  if [ "$i" -eq "00" ]; then
    tmux send-keys -t wave_extraction \
      "python3 extract_wave.py chunks/chunk_${i}.csv outputs/wave_${i}.csv 2>&1 | tee logs/wave_${i}.log" Enter
  else
    tmux split-window -t wave_extraction
    tmux send-keys -t wave_extraction \
      "python3 extract_wave.py chunks/chunk_${i}.csv outputs/wave_${i}.csv 2>&1 | tee logs/wave_${i}.log" Enter
  fi
done

mkdir -p outputs logs

# Attach to watch progress
tmux attach -t wave_extraction
```

### Option B — GNU parallel (single terminal, simpler)

```bash
mkdir -p outputs logs

seq -w 0 29 | parallel -j 30 \
  'python3 extract_wave.py chunks/chunk_{}.csv outputs/wave_{}.csv \
   > logs/wave_{}.log 2>&1'

# Watch progress live in another terminal:
# watch -n 5 'wc -l outputs/wave_*.csv'
```

### Option C — Background jobs (no extra tools needed)

```bash
mkdir -p outputs logs

for i in $(seq -w 0 29); do
  python3 extract_wave.py chunks/chunk_${i}.csv outputs/wave_${i}.csv \
    > logs/wave_${i}.log 2>&1 &
done

# Monitor
watch -n 10 'ls outputs/wave_*.csv 2>/dev/null | wc -l; echo "/ 30 done"'
wait  # Block until all background jobs finish
echo "All workers complete"
```

**Expected runtime:** With llama3.1:8b, each entry takes roughly 5–15 seconds.
43 entries per chunk × 10 sec average = ~7 minutes per chunk. With 30 parallel workers
on a machine with enough RAM (llama3.1:8b needs ~6GB), total wall-clock time
is approximately **7–15 minutes** for the full 1,280-entry migrant group.

If RAM is a bottleneck and you can't run 30 true parallel Ollama instances, run
in groups of 10 sequentially (10 at a time × 3 rounds = same coverage).

---

## Step 5 — Merge and Quality-Check Outputs

```bash
python3 << 'EOF'
import pandas as pd
import glob

files = sorted(glob.glob('outputs/wave_*.csv'))
print(f"Found {len(files)} output files")

dfs = []
for f in files:
    try:
        dfs.append(pd.read_csv(f))
    except Exception as e:
        print(f"ERROR reading {f}: {e}")

merged = pd.concat(dfs, ignore_index=True)
print(f"\nTotal rows merged: {len(merged)}")
print(f"\nWave distribution:")
print(merged['wave'].value_counts())
print(f"\nConfidence distribution:")
print(merged['confidence'].value_counts())
print(f"\nFailed extractions: {merged.get('extraction_failed', pd.Series()).sum()}")
print(f"\nEdge case flags:")
print(merged['edge_case_flag'].value_counts())

merged.to_csv('wave_assignments_merged.csv', index=False)
print("\nSaved: wave_assignments_merged.csv")
EOF
```

**Review the output before proceeding.** If UNKNOWN > 30% or LOW confidence > 40%,
the prompt needs revision — see Step 6 (retry pass).

---

## Step 6 — Retry Pass for LOW Confidence and UNKNOWN

LOW-confidence and UNKNOWN entries get a second pass with a more directive prompt.
This is cheaper than the full pass (typically 20–30% of entries) and runs faster.

```bash
python3 << 'EOF'
import pandas as pd

merged = pd.read_csv('wave_assignments_merged.csv')
retry = merged[
    (merged['confidence'] == 'LOW') |
    (merged['wave'] == 'UNKNOWN') |
    (merged.get('extraction_failed', False) == True)
].copy()

print(f"Entries for retry: {len(retry)}")
retry.to_csv('retry_queue.csv', index=False)
EOF
```

Now write a tighter retry prompt — the retry prompt should include the first pass
result and ask the model to try harder with explicit historical cues:

```bash
cat > extract_wave_retry.py << 'PYEOF'
#!/usr/bin/env python3
"""Retry pass with more directive prompt for LOW/UNKNOWN entries."""

import sys, json, subprocess, pandas as pd, time

INPUT = sys.argv[1]   # retry_queue.csv or a chunk of it
OUTPUT = sys.argv[2]
MODEL = 'llama3.1:8b'
RULES = open('wave_rules.txt').read()

RETRY_PROMPT = """A previous classification attempt returned LOW confidence or UNKNOWN
for the following Ukrainian creative worker. Try again using historical reasoning.

If the text mentions any of these, use them to infer wave:
- Publication dates of works → person was active → alive then
- Named events (UNR retreat, German occupation, DP camps, emigrated to Prague/Paris/NY)
- Membership in named diaspora organisations → implies emigration timing
- Death location (if died in Paris/NY/Toronto → survived to that city)

Rules: {rules}

Entry:
Name: {name} | Born: {birth} | Died: {death}
Text: {bio}

Previous result: wave={prev_wave}, confidence={prev_conf}

Respond ONLY with JSON, same schema as before."""

def query(prompt):
    for _ in range(3):
        try:
            r = subprocess.run(['ollama', 'run', MODEL, prompt],
                               capture_output=True, text=True, timeout=90)
            raw = r.stdout.strip()
            s, e = raw.find('{'), raw.rfind('}') + 1
            if s >= 0 and e > s:
                return json.loads(raw[s:e])
        except Exception:
            time.sleep(3)
    return {"wave": "UNKNOWN", "confidence": "LOW", "emigration_year_est": None,
            "emigration_year_range": [None, None], "evidence_quote": None,
            "edge_case_flag": None, "retry_failed": True}

df = pd.read_csv(INPUT)
# Need to re-join with original dataset to get bio text
orig = pd.read_csv('esu_creative_workers_v2_3.csv')
df = df.merge(orig[['name', 'bio_text_uk']], on='name', how='left',
              suffixes=('', '_orig'))

results = []
for _, row in df.iterrows():
    bio = str(row.get('bio_text_uk', ''))[:3000]
    prompt = RETRY_PROMPT.format(
        rules=RULES, name=row['name'],
        birth=row.get('birth_year', '?'), death=row.get('death_year', '?'),
        bio=bio, prev_wave=row.get('wave', '?'), prev_conf=row.get('confidence', '?')
    )
    print(f"Retry: {row['name']}", flush=True)
    res = query(prompt)
    res['original_index'] = row.get('original_index')
    res['name'] = row['name']
    results.append(res)

pd.DataFrame(results).to_csv(OUTPUT, index=False)
PYEOF
```

Split `retry_queue.csv` into 30 chunks and run in parallel exactly as in Step 4.
After retry, merge retry results back into `wave_assignments_merged.csv`,
overwriting entries where the retry produced MEDIUM or HIGH confidence.

---

## Step 7 — Manual Resolution of Residuals

After both passes, export what remains UNKNOWN or LOW:

```bash
python3 << 'EOF'
import pandas as pd

df = pd.read_csv('wave_assignments_merged.csv')
unresolved = df[df['wave'].isin(['UNKNOWN']) | (df['confidence'] == 'LOW')]
print(f"Unresolved after retry: {len(unresolved)} / {len(df)}")
unresolved[['name', 'birth_year', 'death_year', 'wave', 'confidence',
            'evidence_quote']].to_csv('manual_review.csv', index=False)
EOF
```

Open `manual_review.csv` and resolve each row manually. For each entry, record:
- Your wave assignment
- Your reasoning (one sentence)
- Source consulted if any

Target: unresolved should be under 5% of the migrant group (~64 entries).
If it is higher, the model may not be reading Ukrainian well — switch to
`aya-expanse:8b` (pull with `ollama pull aya-expanse:8b`) and re-run chunks
where Ukrainian comprehension seemed to fail.

---

## Step 8 — Validation Spot-Check

Before computing statistics, validate a stratified random sample.

```bash
python3 << 'EOF'
import pandas as pd

df = pd.read_csv('wave_assignments_merged.csv')

# 40 per wave, stratified
sample = df.groupby('wave', group_keys=False).apply(
    lambda x: x.sample(min(40, len(x)), random_state=42)
)
sample[['name', 'birth_year', 'death_year', 'wave', 'confidence',
        'evidence_quote', 'bio_text_excerpt']].to_csv('validation_sample.csv', index=False)
print(f"Validation sample: {len(sample)} entries across waves")
print(sample['wave'].value_counts())
EOF
```

Review `validation_sample.csv` manually against the original ESU text.
Record your verdict (Correct / Wrong-wave / Wrong-migrant) and compute:

```
error_rate_per_wave = wrong_assignments / sample_size_for_wave
```

Document these rates in SCIENTIFIC_METHODOLOGY.md. If any wave has error > 15%,
re-examine the prompt for that wave's signal words and re-run only that wave's
chunks with a corrected prompt before proceeding.

---

## Step 9 — Merge Wave Assignments into Main Dataset and Compute Statistics

```bash
python3 << 'EOF'
import pandas as pd
import numpy as np
from scipy import stats

# Load main dataset and wave assignments
main = pd.read_csv('esu_creative_workers_v2_3.csv')
waves = pd.read_csv('wave_assignments_merged.csv')[
    ['original_index', 'wave', 'emigration_year_est', 'confidence']
]

# Join
main.loc[waves['original_index'], 'emigration_wave'] = waves['wave'].values
main.loc[waves['original_index'], 'emigration_year_est'] = waves['emigration_year_est'].values

main['age_at_death'] = main['death_year'] - main['birth_year']
nm = main[main['migration_status'] == 'non-migrated']['age_at_death'].dropna()

print("=" * 60)
print("WAVE-LEVEL MEAN AGE AT DEATH vs NON-MIGRATED")
print("=" * 60)
print(f"{'Group':<20} {'n':>6} {'Mean':>7} {'Median':>8} {'SD':>7} {'Gap':>7} {'p':>10}")
print("-" * 60)

nm_mean = nm.mean()
print(f"{'Non-migrated':<20} {len(nm):>6} {nm_mean:>7.2f} {nm.median():>8.1f} "
      f"{nm.std():>7.2f} {'—':>7} {'—':>10}")

for wave in ['WAVE1', 'WAVE2', 'WAVE3', 'WAVE4']:
    grp = main[main['emigration_wave'] == wave]['age_at_death'].dropna()
    if len(grp) < 10:
        print(f"{wave:<20} {len(grp):>6}  (too small for inference)")
        continue
    gap = grp.mean() - nm_mean
    u, p = stats.mannwhitneyu(grp, nm, alternative='two-sided')
    print(f"{wave:<20} {len(grp):>6} {grp.mean():>7.2f} {grp.median():>8.1f} "
          f"{grp.std():>7.2f} {gap:>+7.2f} {p:>10.4f}")

print(f"\nReference: non-migrated mean = {nm_mean:.2f} yrs, n={len(nm)}")

# Save augmented dataset
main.to_csv('esu_creative_workers_v2_4_waves.csv', index=False)
print("\nSaved: esu_creative_workers_v2_4_waves.csv")
EOF
```

---

## Step 10 — Generate Kaplan-Meier Figure

```bash
python3 << 'EOF'
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Simple KM estimator (no external library required)
def km_curve(ages, max_age=100):
    ages_sorted = sorted(ages.dropna())
    n = len(ages_sorted)
    survival = 1.0
    curve = [(0, 1.0)]
    for i, age in enumerate(ages_sorted):
        survival *= (n - i - 1) / (n - i) if (n - i) > 0 else survival
        curve.append((age, survival))
    return zip(*curve)

main = pd.read_csv('esu_creative_workers_v2_4_waves.csv')
fig, ax = plt.subplots(figsize=(10, 6))

colors = {'WAVE1': '#1f77b4', 'WAVE2': '#ff7f0e',
          'WAVE3': '#2ca02c', 'WAVE4': '#9467bd',
          'non-migrated': '#d62728'}

labels = {'WAVE1': 'First wave (pre-1922)',
          'WAVE2': 'Second wave (1939–45)',
          'WAVE3': 'Third wave (1945–91)',
          'WAVE4': 'Post-Soviet (1992+)',
          'non-migrated': 'Non-migrated (reference)'}

for group, color in colors.items():
    if group == 'non-migrated':
        ages = main[main['migration_status'] == 'non-migrated']['age_at_death']
    else:
        ages = main[main['emigration_wave'] == group]['age_at_death']
    if len(ages.dropna()) < 10:
        continue
    xs, ys = km_curve(ages)
    n = len(ages.dropna())
    ax.step(list(xs), list(ys), where='post', color=color,
            label=f"{labels[group]} (n={n})", linewidth=1.8)

ax.set_xlabel('Age (years)', fontsize=12)
ax.set_ylabel('Proportion surviving', fontsize=12)
ax.set_title('Kaplan-Meier Survival Curves by Emigration Wave\nvs Non-migrated (reference)',
             fontsize=13)
ax.legend(fontsize=10)
ax.set_xlim(0, 100)
ax.set_ylim(0, 1)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('fig_wave_km_curves.png', dpi=150)
print("Saved: fig_wave_km_curves.png")
EOF
```

---

## Step 11 — OLS Regression with Wave as Factor

```bash
python3 << 'EOF'
import pandas as pd
import numpy as np
from scipy import stats

main = pd.read_csv('esu_creative_workers_v2_4_waves.csv')
main['age_at_death'] = main['death_year'] - main['birth_year']
main['birth_decade'] = (main['birth_year'] // 10) * 10

# Create wave variable combining non-migrants and each migrant wave
main['group'] = main['migration_status'].copy()
mask = main['migration_status'] == 'migrated'
main.loc[mask, 'group'] = main.loc[mask, 'emigration_wave'].fillna('UNKNOWN')

# Dummy encode and run OLS
from numpy.linalg import lstsq
dummies = pd.get_dummies(
    main[['group', 'birth_decade']].dropna(), drop_first=False
)
dummies = dummies.drop(columns=[c for c in dummies.columns if 'non-migrated' in c],
                       errors='ignore')
y = main.loc[dummies.index, 'age_at_death']
X = dummies.astype(float)
X.insert(0, 'intercept', 1.0)

coef, _, _, _ = lstsq(X.values, y.values, rcond=None)
for name, c in zip(X.columns, coef):
    if 'group' in name or name == 'intercept':
        print(f"{name:<35} {c:>+8.2f} yrs")
EOF
```

---

## Summary of Files Produced

| File | Contents |
|------|----------|
| `chunks/chunk_NN.csv` | 30 input chunks (migrated entries) |
| `outputs/wave_NN.csv` | 30 raw LLM output files |
| `wave_assignments_merged.csv` | Merged wave assignments |
| `manual_review.csv` | Residual unresolved entries for human review |
| `validation_sample.csv` | Stratified spot-check sample |
| `esu_creative_workers_v2_4_waves.csv` | Main dataset + wave field |
| `fig_wave_km_curves.png` | KM figure for paper |

---

## Estimated Wall-Clock Time

| Phase | Time |
|-------|------|
| Prerequisites (ollama install + model pull) | 10–20 min |
| Data prep and chunking | 5 min |
| Main extraction pass (30 workers) | 7–20 min |
| Retry pass (~300 entries, 30 workers) | 2–6 min |
| Manual residual review | 2–6 hours |
| Validation spot-check | 2–4 hours |
| Statistics + figure generation | 15 min |
| **Total excluding manual review** | **~1 hour** |
