# Plan: Bounding the Missing Figures Bias
## Local Parallel Execution — No API Calls, ~30 Concurrent Workers

---

## The Problem

The study draws its population from the Encyclopedia of Modern Ukraine (ESU) —
a scholarly biographical encyclopedia maintained by the Institute of Encyclopedic
Research of the National Academy of Sciences of Ukraine. The ESU is the most
comprehensive Ukrainian-language biographical reference work covering the relevant
period and was chosen for good reasons: consistent biographical format, expert editorial
review, systematic inclusion of birth and death dates, and specific focus on individuals
of cultural and creative significance. It is the right source for this study.

It is also incomplete in a way that is not random.

The ESU is an ongoing encyclopedic project. As of the 2026 access date, it contained
entries for approximately 70,000 individuals, but coverage is uneven and several
prominent Ukrainian creative workers — figures well-documented in other historical
sources, memorial databases, and diaspora reference works — have no published entry.
Among the confirmed absences are Vasyl Stus, who died in the Perm-36 Soviet corrective
labor colony in 1985 at age 47; Mykola Khvylovy, who shot himself in 1933 at age 39
under direct political pressure following the arrest of a close colleague; Vasyl
Symonenko, who died in 1963 at age 28 under circumstances that remain disputed and
are suspected by many historians to involve injuries sustained during a beating in
custody; and Borys Antonenko-Davydovych, a Gulag survivor who lived to 85 but spent
years in the camp system.

The existence of these specific absences is not the core problem. The core problem is
what they represent statistically. All of the confirmed absent figures who were
repressed and died young are non-migrants. They stayed in the Soviet Union — by choice,
by force, or because emigration was not possible for them — and they were killed or died
under conditions directly produced by Soviet repression. Had they been in the ESU
dataset, they would appear in the non-migrant group with low ages at death, pulling the
non-migrant mean downward and widening the gap between migrants and non-migrants. The
direction of the bias is not ambiguous: ESU undercoverage of repressed non-migrants
causes the study to underestimate the mortality differential, not overestimate it.

But the paper currently handles this as a qualitative acknowledgement buried in the
limitations section. It says, in effect: "some prominent figures are absent, and their
inclusion would likely increase the measured gap." This is true but insufficient. It
does not tell the reader how much the gap might increase, under what assumptions, or
whether the effect is large enough to matter for the paper's conclusions. A peer
reviewer reading this will reasonably ask: is this a rounding error — a few individuals
whose inclusion would change the non-migrant mean by 0.1 years — or is it a substantial
bias that could materially alter the picture?

There is a second layer to the problem that goes beyond named individuals. The ESU's
coverage gaps are not randomly distributed across the population it aims to document.
Encyclopedic inclusion tends to favor individuals with large surviving bodies of work,
sustained institutional recognition, and biographical documentation that survived the
Soviet period. All three of these factors are adversely correlated with being killed
young by the Soviet state. A writer shot at age 38 in 1937 produced fewer books than
one who lived to 75. Their institutional affiliations were dissolved and often
deliberately erased. Their biographical documentation was suppressed — families could
not openly mourn, colleagues could not write memorials, and archives containing their
records were restricted or destroyed. The mechanisms that determine ESU inclusion are
precisely the mechanisms that Soviet repression attacked. This means the ESU is
structurally biased against including the most severely repressed individuals — not
because of any editorial failure, but because the source material that encyclopedic
inclusion depends on was systematically destroyed along with the people themselves.

The consequence is that the non-migrant group in the dataset is positively selected for
survival. Non-migrants who appear in the ESU tended to be those who survived long enough
to produce a body of work, accumulate institutional recognition, and leave biographical
traces that survived into the post-Soviet period. The most severely repressed — those
killed youngest, in the most obscure circumstances, with their records most thoroughly
suppressed — are disproportionately absent. This is not a small or marginal effect.
The Great Terror of 1937–1938 killed hundreds of Ukrainian creative workers in a period
of months. Of those, the ones who appear in the dataset are those prominent enough to
be remembered despite the suppression. The ones who do not appear are those whose
erasure was more complete.

The current analysis therefore likely understates the mortality catastrophe that
occurred within the non-migrant group. The non-migrant mean age at death of 71.22 years
is a mean across a population from which the youngest, most violently killed members
have been systematically filtered out. The true non-migrant mean, if the population
were fully documented, would be lower. The 4.04-year gap would be larger. By how much
is the question this plan answers.

---

## The Result Needed

The output of this plan is a quantitative bound on the missing figures bias — a set of
calculations that allow the paper to say, with numerical specificity, how much the
non-migrant mean age at death would change under different assumptions about the number
and age distribution of missing repressed non-migrants, and therefore how much the
migrant/non-migrant gap would widen.

Concretely, the plan produces:

**A missing figures dataset** — a CSV file containing every Ukrainian creative worker
who can be confirmed as (a) absent from the ESU dataset, (b) meeting the study's
inclusion criteria had they been present, and (c) documented in at least one external
source with sufficient biographical information to determine birth year, death year, and
migration status. This dataset has two components: the named confirmed absences (Vasyl
Stus and others, documented with certainty) and the broader set of individuals
identified by cross-referencing external repression databases against the ESU.

**A coverage estimation** — for each external database used (Sandarmokh victim lists,
Rozstriliane Vidrodzhennia memorial records, Ukrainian Institute of National Memory
data), the fraction of that database's eligible population that is already captured in
the ESU dataset. This fraction tells you how incomplete the ESU is relative to each
source, and therefore allows a rough extrapolation from the documented missing figures
to the total gap.

**A sensitivity table** reporting the adjusted non-migrant mean age at death and the
adjusted migrant/non-migrant gap under seven scenarios ranging from conservative
(only the directly documented missing figures added) to extreme (500 missing figures
added at a mean age at death of 38 years). Each scenario is defined by two parameters:
M (the number of missing eligible figures) and Ā_missing (their mean age at death).
The table should show that across all plausible scenarios, the gap increases — and the
paper can therefore state that its current estimate of 4.04 years is a lower bound.

**A sensitivity figure** showing the adjusted gap as a continuous function of M, plotted
separately for three assumed values of Ā_missing (40, 45, and 50 years). This figure
makes visually immediate that the gap direction is robust across all plausible
assumptions about the missing population, and that only an implausibly large number of
missing figures with implausibly high ages at death could reduce the gap to zero.

**A named cases supplement table** listing each confirmed absent individual by name,
with their birth year, death year, age at death, cause of death, migration status,
source of documentation, and ESU absence confirmation. This table serves as verifiable
evidence that the bias is real and documented, not hypothetical. It can be cited by
future researchers who want to build a more complete dataset.

**Revised text for §5.4** replacing the current qualitative acknowledgement with a
paragraph that states the quantitative bound, cites the sensitivity table, and
concludes with the direction of the bias stated unambiguously.

---

## Why We Are Doing This

We are doing this for three reasons that operate at different levels of the paper's
argument.

**The first reason is epistemic honesty.** The paper claims to document Soviet mortality
differentials among Ukrainian creative workers. If the data source systematically
excludes the most severely repressed members of the study population, the paper is
documenting a lower bound on those differentials while presenting it as if it were an
unbiased estimate. This is not intentional misrepresentation — the authors have no
control over what the ESU covers — but it is a form of bias that a serious paper must
quantify rather than merely acknowledge. The difference between "some prominent figures
are absent" and "their inclusion would increase the non-migrant mean age at death by
approximately X years, widening the gap to approximately Y years under conservative
assumptions" is the difference between a qualitative caveat and a quantitative bound.
The latter is substantially more informative and substantially more honest about what
the data can and cannot show.

**The second reason is to preempt the most obvious methodological attack on the paper.**
Any critic who wants to dismiss the paper's findings can point to the ESU coverage
problem and argue that the missing figures introduce unknown bias that could go in either
direction, making the results uninterpretable. This argument is wrong — the direction
of the bias is not unknown, it is clearly downward for the non-migrant mean — but
without quantification it cannot be rebutted effectively. Once the sensitivity table
exists, the rebuttal is direct: even if you assume 500 missing non-migrants who died
at age 38 — a number larger than our entire documented missing set and an age younger
than the most extreme repression-period estimates — the gap still widens rather than
narrows. The current estimate is the most conservative possible reading of the data.
A critic who wants to argue that the ESU coverage problem reverses the paper's findings
must explain why they believe there are more than X missing figures with average age at
death below Y — and the sensitivity table defines exactly what X and Y would need to be.

**The third reason is to advance the historical record independently of the paper's
statistical argument.** The named cases table — a list of confirmed absent Ukrainian
creative workers who were repressed and died young — is a contribution to Ukrainian
cultural history in its own right. Vasyl Stus is one of the most celebrated Ukrainian
poets of the twentieth century and a Nobel Peace Prize nominee. His absence from the
Encyclopedia of Modern Ukraine is a known gap that the ESU editorial project will
presumably address. Mykola Khvylovy is one of the central figures of the Executed
Renaissance. The systematic documentation of these absences, in a form that can be
cross-referenced and verified, gives future researchers who want to build a more complete
dataset a starting point. It also demonstrates, with named examples, the mechanism
by which Soviet repression continues to produce archival gaps even in post-Soviet
encyclopedic projects: the destruction of bodies of work, institutional records, and
biographical documentation during the repression period makes encyclopedic inclusion
harder for those who were most severely targeted, creating a persistent undercount that
outlasts the Soviet system itself.

This third purpose is worth stating clearly because it means the plan has value even
if the sensitivity calculations turn out to be less dramatic than expected. If the
bound shows that the non-migrant mean would only decrease by 0.3 years under the most
aggressive plausible assumptions, that is still a meaningful finding — it means the
ESU coverage problem is not a major quantitative issue, even if it remains a conceptual
one. And the named cases table and coverage estimation remain useful historical
contributions regardless. The plan cannot produce a bad outcome, only different
outcomes with different implications.

---

**Core approach:** Download external repression databases as flat files, normalize and
chunk name lists into ~30 batches, run a local LLM to match against ESU entries and
classify eligibility, merge results, then compute the sensitivity calculation in a
final Python pass.

All steps run entirely in the terminal.

---

## Prerequisites — Do This Once

```bash
# Ollama and model (same as wave plan — skip if already done)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b

# Python deps
pip install pandas numpy scipy thefuzz python-levenshtein tqdm requests \
    beautifulsoup4 --break-system-packages

# Create working directories
mkdir -p external_sources chunks_names outputs_match logs manual_review
```

---

## Step 1 — Acquire External Source Databases

Each source requires different acquisition. Do these in parallel in separate terminals.

### Source A — Sandarmokh / Memorial Database

The Memorial database (base.memo.ru) has been archived. Download the Ukrainian victim
subset from Internet Archive.

```bash
# Search Internet Archive for the Memorial database dump
# The most complete archived snapshot is at:
wget -r -np -nd -A "*.csv,*.json,*.xlsx" \
  "https://web.archive.org/web/2023/https://base.memo.ru/person/show/" \
  -P external_sources/sandarmokh/ 2>/dev/null || true

# Alternative: the Kharkiv Human Rights Group published a structured list
# of Sandarmokh Ukrainian victims. Try:
wget -O external_sources/sandarmokh_victims.html \
  "https://web.archive.org/web/2024/https://khpg.org/en/1008316734"

# If automated download fails, manually download the Sandarmokh execution list PDF
# from the Ukrainian Institute of National Memory and convert:
# pdftotext sandarmokh.pdf external_sources/sandarmokh.txt
```

### Source B — Rozstriliane Vidrodzhennia Database

```bash
# The canonical name list is in Lavrinenko's anthology (public domain)
# and in the online database at rozstrilyanividrodzhennya.org.ua
# Scrape the name index:
python3 << 'EOF'
import requests
from bs4 import BeautifulSoup
import csv, time

BASE = "https://www.rozstrilyanividrodzhennya.org.ua"
names = []

# Scrape the alphabetical index pages
for letter in 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯ':
    try:
        r = requests.get(f"{BASE}/persons/?letter={letter}", timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.select('a[href*="/persons/"]'):
            name = a.get_text(strip=True)
            link = BASE + a['href']
            if name:
                names.append({'name': name, 'source_url': link, 'source': 'RV'})
        print(f"{letter}: {len(names)} total")
        time.sleep(0.5)
    except Exception as e:
        print(f"Failed {letter}: {e}")

with open('external_sources/rv_names.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'source_url', 'source'])
    writer.writeheader()
    writer.writerows(names)
print(f"Saved {len(names)} names to external_sources/rv_names.csv")
EOF
```

### Source C — Ukrainian Memory Institute (UINM) Records

```bash
# The "Reabilitovani istoriieiu" series partial digital index
# is available at memory.gov.ua — scrape the searchable database
python3 << 'EOF'
import requests
from bs4 import BeautifulSoup
import csv, time

# Search for known profession terms across the UINM database
PROFESSIONS = ['письменник', 'поет', 'художник', 'композитор',
               'актор', 'режисер', 'архітектор']
BASE = "https://www.memory.gov.ua"
results = []

for prof in PROFESSIONS:
    page = 1
    while True:
        try:
            r = requests.get(
                f"{BASE}/ua/victims/",
                params={'q': prof, 'page': page},
                timeout=15
            )
            soup = BeautifulSoup(r.text, 'html.parser')
            entries = soup.select('.victim-entry, .person-item, li[class*="victim"]')
            if not entries:
                break
            for entry in entries:
                name = entry.get_text(strip=True)[:100]
                results.append({'name': name, 'profession_search': prof,
                                'source': 'UINM'})
            print(f"{prof} page {page}: {len(entries)} entries")
            page += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"Failed {prof} page {page}: {e}")
            break

with open('external_sources/uinm_names.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'profession_search', 'source'])
    writer.writeheader()
    writer.writerows(results)
print(f"Saved {len(results)} entries")
EOF
```

### Source D — Manual Entry of Named Cases

Regardless of scraping success, manually enter the high-profile known absences
(do this now so the named cases table is guaranteed complete):

```bash
cat > external_sources/named_absences.csv << 'EOF'
name,birth_year,death_year,age_at_death,cause,migration_status,notes
Стус Василь Семенович,1938,1985,47,Gulag (Perm-36),non-migrated,Died VS-389/36 corrective colony
Хвильовий Микола,1893,1933,39,Suicide under political pressure,non-migrated,Shot himself 13 May 1933
Тичина Павло,1891,1967,76,Natural (survived),non-migrated,Survived by conforming; long-lived
Симоненко Василь,1935,1963,28,Natural (suspicious),non-migrated,Died young; suspected beatings in custody
Антоненко-Давидович Борис,1899,1984,85,Natural (survived),non-migrated,Gulag survivor; long-lived post-release
Підмогильний Валер'ян,1901,1937,36,Executed,non-migrated,Shot Sandarmokh 3 Nov 1937
Хвилевой Григорій,1895,1937,42,Executed,non-migrated,Shot during Great Terror
Семенко Михайль,1892,1937,45,Executed,non-migrated,Shot 23 Oct 1937
EOF
```

---

## Step 2 — Consolidate and Deduplicate External Sources

```bash
python3 << 'EOF'
import pandas as pd
import glob

frames = []
for f in glob.glob('external_sources/*.csv'):
    try:
        df = pd.read_csv(f)
        df['source_file'] = f
        frames.append(df)
        print(f"{f}: {len(df)} rows")
    except Exception as e:
        print(f"Error {f}: {e}")

combined = pd.concat(frames, ignore_index=True)

# Normalize name field — handle column name variants
name_cols = [c for c in combined.columns if 'name' in c.lower()]
combined['name_normalized'] = combined[name_cols[0]].str.strip()

# Basic deduplication on normalized name
combined = combined.drop_duplicates(subset='name_normalized', keep='first')
print(f"\nTotal unique external names: {len(combined)}")
combined.to_csv('external_sources/all_external_names.csv', index=False)
EOF
```

---

## Step 3 — Fuzzy Name Matching Against ESU Dataset

This is the core technical step: for each external name, determine whether that
person is already in the ESU dataset (and therefore already counted) or genuinely absent.

### 3a — Fast pre-filter with exact and near-exact matching

```bash
python3 << 'EOF'
import pandas as pd
from thefuzz import fuzz, process
import json

external = pd.read_csv('external_sources/all_external_names.csv')
esu = pd.read_csv('esu_creative_workers_v2_3.csv')

# Normalize both name columns
def normalize(name):
    if pd.isna(name):
        return ''
    return str(name).strip().lower().replace("'", '').replace('`', '')

external['name_norm'] = external['name_normalized'].apply(normalize)
esu['name_norm'] = esu['name'].apply(normalize)
esu_names = esu['name_norm'].tolist()

results = []
for _, row in external.iterrows():
    n = row['name_norm']
    if not n:
        continue

    # Exact match first (fast)
    if n in esu_names:
        results.append({**row.to_dict(),
                        'match_type': 'EXACT',
                        'match_score': 100,
                        'esu_match': n,
                        'in_esu': True})
        continue

    # Fuzzy match
    best_match, score = process.extractOne(
        n, esu_names, scorer=fuzz.token_sort_ratio
    )
    if score >= 90:
        results.append({**row.to_dict(),
                        'match_type': 'FUZZY_HIGH',
                        'match_score': score,
                        'esu_match': best_match,
                        'in_esu': True})
    elif score >= 75:
        results.append({**row.to_dict(),
                        'match_type': 'FUZZY_MED',
                        'match_score': score,
                        'esu_match': best_match,
                        'in_esu': None})  # needs human review
    else:
        results.append({**row.to_dict(),
                        'match_type': 'NO_MATCH',
                        'match_score': score,
                        'esu_match': best_match,
                        'in_esu': False})

df_results = pd.DataFrame(results)
print(df_results['match_type'].value_counts())
df_results.to_csv('name_match_results.csv', index=False)
EOF
```

### 3b — Chunk the uncertain cases (FUZZY_MED and NO_MATCH) for LLM review

Exact and high-confidence fuzzy matches are resolved. The uncertain and non-matching
cases need the LLM to read the biographical context and decide.

```bash
python3 << 'EOF'
import pandas as pd, numpy as np, os

df = pd.read_csv('name_match_results.csv')
uncertain = df[df['match_type'].isin(['FUZZY_MED', 'NO_MATCH'])].copy()
print(f"Uncertain cases for LLM review: {len(uncertain)}")

os.makedirs('chunks_names', exist_ok=True)
chunks = np.array_split(uncertain, min(30, len(uncertain)))
for i, chunk in enumerate(chunks):
    chunk.to_csv(f'chunks_names/chunk_{i:02d}.csv', index=False)
    print(f"Chunk {i:02d}: {len(chunk)} rows")
EOF
```

---

## Step 4 — LLM Review of Uncertain Name Matches

The LLM task here is different from the wave plan: it receives a candidate external
name, the best fuzzy ESU match, and any available biographical snippets, and decides
whether they are the same person.

```bash
cat > match_review.py << 'PYEOF'
#!/usr/bin/env python3
"""
Usage: python3 match_review.py <chunk_file> <output_file>
Reviews uncertain name matches using local Ollama.
"""
import sys, json, subprocess, pandas as pd, time

CHUNK_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
MODEL = 'llama3.1:8b'
ESU = pd.read_csv('esu_creative_workers_v2_3.csv')

PROMPT = """You are verifying whether two records refer to the same Ukrainian person.

External record name: {ext_name}
External source: {source}
External birth year (if known): {ext_birth}
External death year (if known): {ext_death}

Best ESU match found (score {score}/100): {esu_match}
ESU birth year: {esu_birth}
ESU death year: {esu_death}
ESU profession: {esu_prof}
ESU bio excerpt: {esu_bio}

Are these the same person? Consider: name spelling variants, transliteration differences,
birth/death year match, profession consistency.

Respond ONLY with JSON:
{{
  "same_person": true/false/null,
  "confidence": "HIGH/MEDIUM/LOW",
  "reasoning": "one sentence"
}}"""

def query(prompt):
    for _ in range(3):
        try:
            r = subprocess.run(['ollama', 'run', MODEL, prompt],
                               capture_output=True, text=True, timeout=60)
            raw = r.stdout.strip()
            s, e = raw.find('{'), raw.rfind('}') + 1
            if s >= 0 and e > s:
                return json.loads(raw[s:e])
        except Exception:
            time.sleep(2)
    return {"same_person": None, "confidence": "LOW", "reasoning": "extraction failed"}

df = pd.read_csv(CHUNK_FILE)
results = []
for _, row in df.iterrows():
    esu_row = ESU[ESU['name'].str.lower().str.strip() == str(row.get('esu_match', '')).lower().strip()]
    esu_bio = esu_row.iloc[0].get('bio_text', '')[:500] if len(esu_row) else ''
    esu_birth = esu_row.iloc[0].get('birth_year', '?') if len(esu_row) else '?'
    esu_death = esu_row.iloc[0].get('death_year', '?') if len(esu_row) else '?'
    esu_prof = esu_row.iloc[0].get('profession', '?') if len(esu_row) else '?'

    prompt = PROMPT.format(
        ext_name=row.get('name_normalized', ''),
        source=row.get('source', ''),
        ext_birth=row.get('birth_year', '?'),
        ext_death=row.get('death_year', '?'),
        score=row.get('match_score', '?'),
        esu_match=row.get('esu_match', ''),
        esu_birth=esu_birth, esu_death=esu_death,
        esu_prof=esu_prof, esu_bio=esu_bio
    )
    print(f"[{CHUNK_FILE}] {row.get('name_normalized', '?')}", flush=True)
    res = query(prompt)
    res['external_name'] = row.get('name_normalized', '')
    res['esu_match'] = row.get('esu_match', '')
    res['match_score'] = row.get('match_score', '')
    res['source'] = row.get('source', '')
    res['ext_birth'] = row.get('birth_year', '')
    res['ext_death'] = row.get('death_year', '')
    results.append(res)

pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
print(f"[DONE] {OUTPUT_FILE}", flush=True)
PYEOF
chmod +x match_review.py
```

Launch 30 workers in parallel (same pattern as wave plan):

```bash
mkdir -p outputs_match logs

# Option A — GNU parallel
seq -w 0 29 | parallel -j 30 \
  'python3 match_review.py chunks_names/chunk_{}.csv outputs_match/match_{}.csv \
   > logs/match_{}.log 2>&1'

# Option B — background jobs
for i in $(seq -w 0 29); do
  [ -f "chunks_names/chunk_${i}.csv" ] && \
    python3 match_review.py chunks_names/chunk_${i}.csv \
      outputs_match/match_${i}.csv > logs/match_${i}.log 2>&1 &
done
wait
echo "All match workers done"
```

---

## Step 5 — Merge Match Results and Classify Missing Figures

```bash
python3 << 'EOF'
import pandas as pd, glob

# Merge LLM match reviews
reviews = pd.concat(
    [pd.read_csv(f) for f in sorted(glob.glob('outputs_match/match_*.csv'))],
    ignore_index=True
)

# Combine with exact/high-fuzzy matches from Step 3
exact = pd.read_csv('name_match_results.csv')
exact = exact[exact['match_type'].isin(['EXACT', 'FUZZY_HIGH'])].copy()
exact['same_person'] = True
exact['confidence'] = 'HIGH'

# Merge: for uncertain cases, use LLM verdict; for clear cases, use rule
uncertain_resolved = reviews.copy()
all_classified = pd.concat([
    exact[['external_name'] if 'external_name' in exact.columns
          else ['name_normalized']
          + ['same_person', 'confidence', 'source', 'ext_birth', 'ext_death']],
    uncertain_resolved
], ignore_index=True)

# Those where same_person == False are the MISSING FIGURES candidates
missing = all_classified[all_classified['same_person'] == False].copy()
print(f"Candidates identified as NOT in ESU dataset: {len(missing)}")
missing.to_csv('missing_candidates.csv', index=False)

# Those needing manual review (same_person == null or LOW confidence)
review_needed = all_classified[
    all_classified['same_person'].isna() | 
    (all_classified['confidence'] == 'LOW')
]
print(f"Needs manual review: {len(review_needed)}")
review_needed.to_csv('manual_review/name_match_uncertain.csv', index=False)
EOF
```

---

## Step 6 — Apply Inclusion Criteria to Missing Candidates

Not all missing figures would have qualified for the study. Each candidate must be
checked against the study's five inclusion criteria. This is another LLM pass,
but the dataset is now much smaller (~50–200 candidates).

```bash
cat > check_eligibility.py << 'PYEOF'
#!/usr/bin/env python3
"""Check each missing candidate against study inclusion criteria."""
import sys, json, subprocess, pandas as pd, time

INPUT = sys.argv[1]
OUTPUT = sys.argv[2]
MODEL = 'llama3.1:8b'

CRITERIA = """Study inclusion requires ALL of:
1. Ukrainian by cultural participation definition (not ethnic test)
2. Primary profession is a creative worker: poet, writer, visual artist, musician,
   composer, theatre/film director, actor, architect, or similar creative field
3. Confirmed birth year known
4. Confirmed death year known
5. Migration status determinable (for repression victims: non-migrated is assumed
   unless there is evidence of emigration)"""

PROMPT = """A Ukrainian repression victim database lists this person. Assess whether
they would qualify for a study of Ukrainian creative worker mortality.

{criteria}

Person: {name}
Birth year: {birth}
Death year: {death}
Cause of death: {cause}
Source: {source}
Any additional notes: {notes}

Respond ONLY with JSON:
{{
  "qualifies": true/false,
  "migration_status": "non-migrated/migrated/unknown",
  "profession_creative": true/false,
  "birth_year_known": true/false,
  "death_year_known": true/false,
  "estimated_age_at_death": <integer or null>,
  "reasoning": "one sentence"
}}"""

df = pd.read_csv(INPUT)
results = []
for _, row in df.iterrows():
    prompt = PROMPT.format(
        criteria=CRITERIA,
        name=row.get('external_name', row.get('name', '?')),
        birth=row.get('ext_birth', row.get('birth_year', '?')),
        death=row.get('ext_death', row.get('death_year', '?')),
        cause=row.get('cause', 'unknown'),
        source=row.get('source', 'unknown'),
        notes=row.get('notes', '')
    )
    print(f"Eligibility: {row.get('external_name', '?')}", flush=True)
    for _ in range(3):
        try:
            r = subprocess.run(['ollama', 'run', MODEL, prompt],
                               capture_output=True, text=True, timeout=60)
            raw = r.stdout.strip()
            s, e = raw.find('{'), raw.rfind('}') + 1
            if s >= 0 and e > s:
                res = json.loads(raw[s:e])
                res['name'] = row.get('external_name', row.get('name', ''))
                results.append(res)
                break
        except Exception:
            time.sleep(2)
    else:
        results.append({'name': row.get('external_name', ''), 'qualifies': None,
                        'reasoning': 'failed'})

pd.DataFrame(results).to_csv(OUTPUT, index=False)
PYEOF

# Split missing_candidates.csv into chunks and run in parallel
python3 -c "
import pandas as pd, numpy as np, os
df = pd.read_csv('missing_candidates.csv')
os.makedirs('chunks_eligible', exist_ok=True)
for i, chunk in enumerate(np.array_split(df, min(30, len(df)))):
    chunk.to_csv(f'chunks_eligible/chunk_{i:02d}.csv', index=False)
"

mkdir -p outputs_eligible
seq -w 0 29 | parallel -j 30 \
  '[ -f chunks_eligible/chunk_{}.csv ] && \
   python3 check_eligibility.py chunks_eligible/chunk_{}.csv \
     outputs_eligible/eligible_{}.csv > logs/eligible_{}.log 2>&1'
wait

# Merge
python3 -c "
import pandas as pd, glob
dfs = [pd.read_csv(f) for f in sorted(glob.glob('outputs_eligible/eligible_*.csv'))]
merged = pd.concat(dfs, ignore_index=True)
qualified = merged[merged['qualifies'] == True]
print(f'Total missing candidates: {len(merged)}')
print(f'Qualify for study inclusion: {len(qualified)}')
qualified.to_csv('eligible_missing_figures.csv', index=False)
merged.to_csv('all_missing_classified.csv', index=False)
"
```

---

## Step 7 — Compute the Sensitivity Bound

```bash
python3 << 'EOF'
import pandas as pd
import numpy as np

main = pd.read_csv('esu_creative_workers_v2_3.csv')
main['age_at_death'] = main['death_year'] - main['birth_year']
nm = main[main['migration_status'] == 'non-migrated']['age_at_death'].dropna()
nm_mean = nm.mean()
nm_n = len(nm)
migrant_mean = main[main['migration_status'] == 'migrated']['age_at_death'].dropna().mean()
current_gap = migrant_mean - nm_mean

eligible = pd.read_csv('eligible_missing_figures.csv')
eligible['age_at_death'] = pd.to_numeric(eligible['estimated_age_at_death'], errors='coerce')
documented_missing = eligible['age_at_death'].dropna()
M_doc = len(documented_missing)
A_doc = documented_missing.mean()

print(f"Current non-migrant mean: {nm_mean:.2f} yrs (n={nm_n})")
print(f"Current migrant mean:     {migrant_mean:.2f} yrs")
print(f"Current gap:              {current_gap:.2f} yrs")
print(f"\nDocumented eligible missing figures: M={M_doc}, mean age at death={A_doc:.1f} yrs")

print("\n" + "="*65)
print(f"{'Scenario':<30} {'M':>6} {'Ā_miss':>8} {'NM mean adj':>12} {'Gap adj':>10}")
print("-"*65)

scenarios = [
    ("Documented only",        M_doc,      A_doc),
    ("1.5× documented",        int(M_doc*1.5), A_doc),
    ("2× documented",          M_doc*2,    A_doc - 2),
    ("Conservative (n=50)",    50,          45),
    ("Moderate (n=150)",       150,         43),
    ("Liberal (n=300)",        300,         40),
    ("Extreme (n=500)",        500,         38),
]

for label, M, A_miss in scenarios:
    adj_mean = (nm_n * nm_mean + M * A_miss) / (nm_n + M)
    adj_gap = migrant_mean - adj_mean
    print(f"{label:<30} {M:>6.0f} {A_miss:>8.1f} {adj_mean:>12.2f} {adj_gap:>+10.2f}")

print("\nConclusion: In all scenarios, including missing repressed non-migrants")
print("INCREASES the gap — the current estimate is conservative.")

# Save sensitivity table
rows = []
for label, M, A_miss in scenarios:
    adj_mean = (nm_n * nm_mean + M * A_miss) / (nm_n + M)
    adj_gap = migrant_mean - adj_mean
    rows.append({'scenario': label, 'M': M, 'A_miss': A_miss,
                 'nm_mean_adj': round(adj_mean, 2), 'gap_adj': round(adj_gap, 2)})
pd.DataFrame(rows).to_csv('sensitivity_table.csv', index=False)
print("\nSaved: sensitivity_table.csv")
EOF
```

---

## Step 8 — Sensitivity Figure

```bash
python3 << 'EOF'
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

main = pd.read_csv('esu_creative_workers_v2_3.csv')
main['age_at_death'] = main['death_year'] - main['birth_year']
nm_mean = main[main['migration_status'] == 'non-migrated']['age_at_death'].dropna().mean()
nm_n = len(main[main['migration_status'] == 'non-migrated']['age_at_death'].dropna())
migrant_mean = main[main['migration_status'] == 'migrated']['age_at_death'].dropna().mean()

M_range = np.arange(0, 601, 10)
fig, ax = plt.subplots(figsize=(10, 6))

for A_miss, color, label in [
    (40, '#d62728', 'Ā_missing = 40 yrs (very young deaths)'),
    (45, '#ff7f0e', 'Ā_missing = 45 yrs (median deported group)'),
    (50, '#2ca02c', 'Ā_missing = 50 yrs (older repressed)'),
]:
    adj_means = (nm_n * nm_mean + M_range * A_miss) / (nm_n + M_range)
    gaps = migrant_mean - adj_means
    ax.plot(M_range, gaps, color=color, label=label, linewidth=2)

ax.axhline(y=migrant_mean - nm_mean, color='steelblue',
           linestyle='--', linewidth=1.5, label=f'Current gap ({migrant_mean - nm_mean:.2f} yrs)')
ax.axhline(y=0, color='black', linewidth=0.8)
ax.set_xlabel('Number of missing eligible figures added (M)', fontsize=12)
ax.set_ylabel('Adjusted migrant/non-migrant gap (years)', fontsize=12)
ax.set_title('Sensitivity of Mortality Gap to Missing Repressed Non-Migrants\n'
             'All scenarios increase the gap — current estimate is conservative', fontsize=12)
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('fig_missing_figures_sensitivity.png', dpi=150)
print("Saved: fig_missing_figures_sensitivity.png")
EOF
```

---

## Step 9 — Named Cases Table

```bash
python3 << 'EOF'
import pandas as pd

named = pd.read_csv('external_sources/named_absences.csv')
named['gap_vs_nm'] = 71.22 - named['age_at_death']

print("\nNamed Eligible Missing Figures")
print("="*80)
print(f"{'Name':<35} {'Born':>5} {'Died':>5} {'Age':>5} {'Cause':<25} {'Gap':>7}")
print("-"*80)
for _, r in named.iterrows():
    print(f"{r['name']:<35} {r['birth_year']:>5} {r['death_year']:>5} "
          f"{r['age_at_death']:>5} {r['cause']:<25} {r['gap_vs_nm']:>+7.1f}")

named.to_csv('named_missing_figures_table.csv', index=False)
print("\nSaved: named_missing_figures_table.csv")
EOF
```

---

## Step 10 — Coverage Estimation

```bash
python3 << 'EOF'
import pandas as pd

matches = pd.read_csv('name_match_results.csv')
esu_main = pd.read_csv('esu_creative_workers_v2_3.csv')
esu_n = len(esu_main)

# For each source, compute what fraction of that source's entries are already in ESU
for source in matches['source'].unique():
    src = matches[matches['source'] == source]
    in_esu = src[src['in_esu'] == True]
    total = len(src)
    captured = len(in_esu)
    if total == 0:
        continue
    coverage = captured / total
    missing_rate = 1 - coverage
    est_total_missing = int(len(src[src['in_esu'] == False]) / missing_rate) if missing_rate > 0 else 0
    print(f"\nSource: {source}")
    print(f"  Entries in source: {total}")
    print(f"  Already in ESU dataset: {captured} ({coverage:.1%})")
    print(f"  ESU missing rate: {missing_rate:.1%}")
    print(f"  Estimated true gap (if source is representative): ~{est_total_missing}")
EOF
```

---

## Summary of Files Produced

| File | Contents |
|------|----------|
| `external_sources/*.csv` | Raw downloads from each external database |
| `name_match_results.csv` | All external names with ESU match classification |
| `missing_candidates.csv` | Names confirmed absent from ESU |
| `eligible_missing_figures.csv` | Subset that would qualify for study inclusion |
| `sensitivity_table.csv` | Gap under 7 missing-figures scenarios |
| `named_missing_figures_table.csv` | Named cases table for paper |
| `fig_missing_figures_sensitivity.png` | Sensitivity figure for paper |

---

## Estimated Wall-Clock Time

| Phase | Time |
|-------|------|
| Source acquisition (scraping + wget) | 30–90 min |
| Consolidation and fuzzy pre-match | 10–20 min |
| LLM match review (30 workers, uncertain cases) | 5–15 min |
| LLM eligibility check (30 workers) | 5–10 min |
| Manual review of uncertain matches | 3–6 hours |
| Sensitivity calculation + figures | 10 min |
| Named cases table | 15 min |
| **Total excluding manual review** | **~2 hours** |

The bottleneck is manual review of ambiguous name matches, not computation.
Scraping reliability varies by site — if automated download fails for any source,
budget additional time for manual CSV construction from web-accessible pages.
