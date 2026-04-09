"""
build_validation_reviewer.py
Draws a fresh 200-entry stratified validation sample from esu_creative_workers_v2_6.csv,
fetches full ESU bios for each, and builds a self-contained HTML reviewer with export.

Sample design:
  - 100 INCLUDE  (from migrated/non_migrated/internal_transfer/deported)
     stratified by migration_status proportional to group size
  - 100 EXCLUDE  (from excluded_* / unknown / alive)
     40% excluded_pre_soviet, 30% unknown+alive, 30% other_excluded

Output: ukraine_v2/validation/validation_v2_6_reviewer.html
        ukraine_v2/validation/validation_v2_6_sample.csv
"""

import csv
import os
import random
import json
import time
import re
import requests
from collections import defaultdict

PROJECT   = os.path.dirname(os.path.abspath(__file__))
CSV_IN    = os.path.join(PROJECT, 'esu_creative_workers_v2_6.csv')
VAL_DIR   = os.path.join(PROJECT, 'validation')
CSV_OUT   = os.path.join(VAL_DIR, 'validation_v2_6_sample.csv')
HTML_OUT  = os.path.join(VAL_DIR, 'validation_v2_6_reviewer.html')

os.makedirs(VAL_DIR, exist_ok=True)

random.seed(2026)   # reproducible

# ---------------------------------------------------------------------------
# Load dataset
# ---------------------------------------------------------------------------
def safe_int(val):
    try:
        return int(float(str(val).strip()))
    except:
        return None

with open(CSV_IN, encoding='utf-8-sig') as f:
    all_rows = list(csv.DictReader(f))

INCLUDE_STATUSES = {'migrated', 'non_migrated', 'internal_transfer', 'deported'}
EXCLUDE_STATUSES = {'excluded_pre_soviet', 'excluded_galicia_pre_annexation',
                    'excluded_non_ukrainian', 'excluded_bad_dates', 'unknown', 'alive'}

include_pool = [r for r in all_rows
                if r.get('migration_status','').strip().lower() in INCLUDE_STATUSES
                and safe_int(r.get('birth_year')) and safe_int(r.get('death_year'))]

exclude_pool = [r for r in all_rows
                if r.get('migration_status','').strip().lower() in EXCLUDE_STATUSES]

print(f"INCLUDE pool: {len(include_pool)}, EXCLUDE pool: {len(exclude_pool)}")

# ---------------------------------------------------------------------------
# Stratified sample — INCLUDE: proportional to group size (total 100)
# ---------------------------------------------------------------------------
by_status = defaultdict(list)
for r in include_pool:
    by_status[r['migration_status'].strip().lower()].append(r)

# Target proportions: migrated ~14.8%, non_migrated ~69.7%, it ~13.3%, dep ~2.1%
# Scale to 100 entries
INCLUDE_TARGETS = {
    'migrated':          15,
    'non_migrated':      70,
    'internal_transfer': 13,
    'deported':           2,
}

sampled_include = []
for ms, target in INCLUDE_TARGETS.items():
    pool = by_status[ms]
    n = min(target, len(pool))
    sampled_include.extend(random.sample(pool, n))

# Fill to exactly 100 if rounding left us short
while len(sampled_include) < 100:
    extras = [r for r in include_pool if r not in sampled_include]
    sampled_include.append(random.choice(extras))

# ---------------------------------------------------------------------------
# Stratified sample — EXCLUDE: 100 entries
# ---------------------------------------------------------------------------
exc_pre_soviet = [r for r in exclude_pool if r.get('migration_status','').strip().lower() == 'excluded_pre_soviet']
exc_unknown    = [r for r in exclude_pool if r.get('migration_status','').strip().lower() in {'unknown', 'alive'}]
exc_other      = [r for r in exclude_pool if r.get('migration_status','').strip().lower() in
                  {'excluded_galicia_pre_annexation', 'excluded_non_ukrainian', 'excluded_bad_dates'}]

sampled_exclude = (
    random.sample(exc_pre_soviet, min(40, len(exc_pre_soviet))) +
    random.sample(exc_unknown,    min(30, len(exc_unknown))) +
    random.sample(exc_other,      min(30, len(exc_other)))
)

# top up to 100 if needed
all_exc = exc_pre_soviet + exc_unknown + exc_other
while len(sampled_exclude) < 100:
    extras = [r for r in all_exc if r not in sampled_exclude]
    if not extras: break
    sampled_exclude.append(random.choice(extras))

sampled_exclude = sampled_exclude[:100]

# ---------------------------------------------------------------------------
# Merge + shuffle
# ---------------------------------------------------------------------------
for r in sampled_include:
    r['_sample_group'] = 'INCLUDE'
for r in sampled_exclude:
    r['_sample_group'] = 'EXCLUDE'

sample = sampled_include + sampled_exclude
random.shuffle(sample)

# Assign sequential index
for i, r in enumerate(sample):
    r['_idx'] = i

print(f"Sample: {len(sample)} entries "
      f"({sum(1 for r in sample if r['_sample_group']=='INCLUDE')} INCLUDE, "
      f"{sum(1 for r in sample if r['_sample_group']=='EXCLUDE')} EXCLUDE)")

# ---------------------------------------------------------------------------
# Fetch full ESU bios
# ---------------------------------------------------------------------------
SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'Mozilla/5.0 (research; contact: research@example.com)'})

def fetch_bio(url, timeout=12):
    """
    Extract article text from an ESU article page.
    Priority:
      1. <div itemprop="articleBody"> — full article text
      2. <meta name="citation_abstract"> — condensed version (always present)
      3. <meta name="description"> — shortest fallback
    """
    if not url or not url.startswith('http'):
        return ''
    try:
        resp = SESSION.get(url, timeout=timeout)
        resp.encoding = 'utf-8'
        html = resp.text

        # 1. Full article body
        m = re.search(r'<div[^>]+itemprop="articleBody"[^>]*>(.*?)</div>\s*</article>',
                      html, re.DOTALL | re.IGNORECASE)
        if not m:
            m = re.search(r'itemprop="articleBody"[^>]*>(.*?)</div>', html, re.DOTALL)
        if m:
            raw = m.group(1)
            text = re.sub(r'<[^>]+>', ' ', raw)
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text) > 100:
                return text[:5000]

        # 2. citation_abstract meta
        m2 = re.search(r'<meta[^>]+name="citation_abstract"[^>]+content="([^"]+)"', html)
        if not m2:
            m2 = re.search(r'<meta[^>]+content="([^"]+)"[^>]+name="citation_abstract"', html)
        if m2:
            return m2.group(1).strip()[:3000]

        # 3. description meta
        m3 = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
        if m3:
            return m3.group(1).strip()[:2000]

        return '[bio not found]'
    except Exception as e:
        return f'[fetch error: {e}]'

print("Fetching ESU bios (200 requests @ 0.5s each ≈ 2 min)...")
for i, r in enumerate(sample):
    bio = fetch_bio(r.get('article_url', ''))
    r['_full_bio'] = bio
    if (i + 1) % 20 == 0:
        print(f"  {i+1}/200 fetched")
    time.sleep(0.5)

print("All bios fetched.")

# ---------------------------------------------------------------------------
# Save CSV
# ---------------------------------------------------------------------------
fieldnames = ['idx', 'name', 'birth_year', 'death_year', 'migration_status',
              'migration_reasoning', 'notes', 'article_url', 'sample_group', 'full_bio']

with open(CSV_OUT, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in sample:
        writer.writerow({
            'idx':               r['_idx'],
            'name':              r.get('name', ''),
            'birth_year':        r.get('birth_year', ''),
            'death_year':        r.get('death_year', ''),
            'migration_status':  r.get('migration_status', ''),
            'migration_reasoning': r.get('migration_reasoning', ''),
            'notes':             r.get('notes', ''),
            'article_url':       r.get('article_url', ''),
            'sample_group':      r['_sample_group'],
            'full_bio':          r.get('_full_bio', ''),
        })

print(f"CSV saved → {CSV_OUT}")

# ---------------------------------------------------------------------------
# Build HTML reviewer
# ---------------------------------------------------------------------------
def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

entries_json = []
for r in sample:
    entries_json.append({
        'idx':       r['_idx'],
        'name':      r.get('name', ''),
        'by':        r.get('birth_year', ''),
        'dy':        r.get('death_year', ''),
        'status':    r.get('migration_status', ''),
        'reasoning': r.get('migration_reasoning', ''),
        'notes':     r.get('notes', ''),
        'url':       r.get('article_url', ''),
        'group':     r['_sample_group'],
        'bio':       r.get('_full_bio', ''),
    })

DATA_JS = json.dumps(entries_json, ensure_ascii=False)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>V2.6 Validation Reviewer — 200 Entries</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #f0f2f5;
    color: #1a1a1a;
    min-height: 100vh;
  }}

  /* ── Header ── */
  #header {{
    background: #1a1a2e;
    color: #fff;
    padding: 14px 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
  }}
  #header h1 {{ font-size: 1.1em; font-weight: 700; flex: 1; }}
  #progress-bar-wrap {{
    flex: 2;
    background: rgba(255,255,255,0.15);
    border-radius: 8px;
    height: 10px;
    overflow: hidden;
  }}
  #progress-bar {{
    height: 100%;
    background: #4caf50;
    width: 0%;
    transition: width 0.3s;
  }}
  #progress-text {{ font-size: 0.85em; white-space: nowrap; }}

  /* ── Main layout ── */
  #main {{
    display: grid;
    grid-template-columns: 220px 1fr;
    gap: 0;
    max-width: 1400px;
    margin: 0 auto;
    min-height: calc(100vh - 52px);
  }}

  /* ── Sidebar ── */
  #sidebar {{
    background: #fff;
    border-right: 1px solid #ddd;
    overflow-y: auto;
    height: calc(100vh - 52px);
    position: sticky;
    top: 52px;
  }}
  #sidebar-controls {{
    padding: 10px;
    border-bottom: 1px solid #eee;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  #sidebar-controls input {{
    width: 100%;
    padding: 6px 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 0.82em;
  }}
  #sidebar-controls select {{
    width: 100%;
    padding: 5px 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 0.82em;
  }}
  .sidebar-entry {{
    padding: 8px 12px;
    border-bottom: 1px solid #f0f0f0;
    cursor: pointer;
    font-size: 0.8em;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: background 0.1s;
  }}
  .sidebar-entry:hover {{ background: #f5f8ff; }}
  .sidebar-entry.active {{ background: #e8f0fe; font-weight: 600; }}
  .dot {{
    width: 9px; height: 9px;
    border-radius: 50%;
    flex-shrink: 0;
  }}
  .dot-correct {{ background: #4caf50; }}
  .dot-wrong   {{ background: #e53935; }}
  .dot-skip    {{ background: #ff9800; }}
  .dot-unseen  {{ background: #ccc; }}
  .badge {{
    font-size: 0.7em;
    padding: 1px 5px;
    border-radius: 10px;
    margin-left: auto;
    font-weight: 600;
  }}
  .badge-inc {{ background: #e3f2fd; color: #1565c0; }}
  .badge-exc {{ background: #fce4ec; color: #880e4f; }}

  /* ── Card ── */
  #card-area {{
    padding: 24px;
    overflow-y: auto;
  }}
  #card {{
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    max-width: 820px;
    margin: 0 auto;
  }}
  #card-header {{
    padding: 20px 24px 16px;
    border-bottom: 1px solid #eee;
    display: flex;
    align-items: flex-start;
    gap: 12px;
  }}
  #idx-badge {{
    background: #1a1a2e;
    color: #fff;
    font-size: 0.85em;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    white-space: nowrap;
  }}
  #entry-name {{
    font-size: 1.2em;
    font-weight: 700;
    flex: 1;
  }}
  #group-chip {{
    font-size: 0.78em;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 12px;
  }}
  .chip-inc {{ background: #e3f2fd; color: #1565c0; }}
  .chip-exc {{ background: #fce4ec; color: #880e4f; }}

  #card-meta {{
    padding: 14px 24px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px 24px;
    border-bottom: 1px solid #f0f0f0;
    font-size: 0.85em;
  }}
  .meta-row {{ display: flex; gap: 6px; }}
  .meta-label {{ color: #888; font-weight: 600; min-width: 80px; }}
  .meta-val {{ word-break: break-all; }}
  .status-chip {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.85em;
    font-weight: 600;
  }}
  .s-migrated          {{ background: #e3f2fd; color: #1565c0; }}
  .s-non_migrated      {{ background: #fce4ec; color: #b71c1c; }}
  .s-internal_transfer {{ background: #fff3e0; color: #e65100; }}
  .s-deported          {{ background: #fbe9e7; color: #bf360c; }}
  .s-unknown           {{ background: #f3e5f5; color: #6a1b9a; }}
  .s-excluded          {{ background: #efebe9; color: #4e342e; }}
  .s-alive             {{ background: #e8f5e9; color: #1b5e20; }}

  #reasoning-box {{
    padding: 14px 24px;
    border-bottom: 1px solid #f0f0f0;
    font-size: 0.83em;
    color: #555;
    line-height: 1.6;
  }}
  #reasoning-box strong {{ color: #333; }}

  #bio-box {{
    padding: 14px 24px;
    border-bottom: 1px solid #f0f0f0;
    font-size: 0.82em;
    color: #444;
    line-height: 1.65;
    max-height: 280px;
    overflow-y: auto;
    background: #fafafa;
  }}
  #bio-box strong {{ color: #333; display: block; margin-bottom: 4px; }}
  #bio-toggle {{
    color: #1976d2;
    cursor: pointer;
    font-size: 0.8em;
    padding: 0 24px 8px;
    display: block;
    background: none;
    border: none;
  }}

  #decision-area {{
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }}
  #decision-label {{ font-weight: 700; font-size: 0.9em; color: #444; margin-right: 4px; }}

  .btn {{
    padding: 10px 22px;
    border: none;
    border-radius: 8px;
    font-size: 0.9em;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .btn:hover {{ transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
  .btn:active {{ transform: translateY(0); }}
  .btn-correct {{ background: #4caf50; color: #fff; }}
  .btn-wrong   {{ background: #e53935; color: #fff; }}
  .btn-skip    {{ background: #ff9800; color: #fff; }}
  .btn-nav     {{ background: #eee; color: #333; padding: 10px 16px; }}
  .btn-export  {{
    background: #1a1a2e; color: #fff;
    padding: 10px 24px;
    font-size: 0.88em;
  }}
  .selected-correct {{ outline: 3px solid #4caf50; }}
  .selected-wrong   {{ outline: 3px solid #e53935; }}
  .selected-skip    {{ outline: 3px solid #ff9800; }}

  #comment-row {{
    padding: 0 24px 16px;
    display: flex;
    gap: 8px;
    align-items: center;
  }}
  #comment-row input {{
    flex: 1;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 0.85em;
  }}
  #comment-row label {{ font-size: 0.82em; color: #666; white-space: nowrap; }}

  #nav-row {{
    padding: 12px 24px 20px;
    display: flex;
    gap: 10px;
    justify-content: flex-end;
    border-top: 1px solid #f0f0f0;
  }}

  /* ── Bottom toolbar ── */
  #bottom-bar {{
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: #fff;
    border-top: 1px solid #ddd;
    padding: 10px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    z-index: 100;
    box-shadow: 0 -2px 8px rgba(0,0,0,0.06);
  }}
  #stats-row {{
    display: flex;
    gap: 12px;
    font-size: 0.83em;
    flex: 1;
    flex-wrap: wrap;
  }}
  .stat {{ color: #555; }}
  .stat strong {{ color: #222; }}

  /* ── Export modal ── */
  #modal-overlay {{
    display: none;
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.5);
    z-index: 200;
    align-items: center;
    justify-content: center;
  }}
  #modal-overlay.show {{ display: flex; }}
  #modal {{
    background: #fff;
    border-radius: 12px;
    padding: 28px 32px;
    max-width: 520px;
    width: 90%;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  }}
  #modal h2 {{ font-size: 1.1em; margin-bottom: 16px; }}
  #modal p {{ font-size: 0.85em; color: #555; margin-bottom: 16px; line-height: 1.5; }}
  #modal-buttons {{ display: flex; gap: 10px; flex-wrap: wrap; }}
  .btn-modal-dl {{ background: #1976d2; color: #fff; }}
  .btn-modal-copy {{ background: #555; color: #fff; }}
  .btn-modal-close {{ background: #eee; color: #333; }}
  #export-preview {{
    background: #f5f5f5;
    border-radius: 6px;
    padding: 10px;
    font-size: 0.75em;
    font-family: monospace;
    max-height: 140px;
    overflow-y: auto;
    margin-bottom: 14px;
    white-space: pre-wrap;
  }}

  /* ── ESU link ── */
  .esu-link {{ color: #1976d2; text-decoration: none; font-size: 0.8em; }}
  .esu-link:hover {{ text-decoration: underline; }}
</style>
</head>
<body>

<!-- HEADER -->
<div id="header">
  <h1>V2.6 Validation Reviewer</h1>
  <div id="progress-bar-wrap"><div id="progress-bar"></div></div>
  <span id="progress-text">0 / 200</span>
  <button class="btn btn-export" onclick="openExportModal()">⬇ Export Results</button>
</div>

<!-- MAIN -->
<div id="main">

  <!-- SIDEBAR -->
  <div id="sidebar">
    <div id="sidebar-controls">
      <input type="text" id="search-box" placeholder="Search name…" oninput="renderSidebar()">
      <select id="filter-status" onchange="renderSidebar()">
        <option value="all">All entries</option>
        <option value="unseen">Not yet reviewed</option>
        <option value="correct">✓ Correct</option>
        <option value="wrong">✗ Wrong</option>
        <option value="skip">— Skipped</option>
        <option value="INCLUDE">INCLUDE group</option>
        <option value="EXCLUDE">EXCLUDE group</option>
      </select>
    </div>
    <div id="sidebar-list"></div>
  </div>

  <!-- CARD AREA -->
  <div id="card-area">
    <div id="card">
      <div id="card-header">
        <span id="idx-badge">#0</span>
        <span id="entry-name">—</span>
        <span id="group-chip" class="chip-inc">INCLUDE</span>
      </div>
      <div id="card-meta">
        <div class="meta-row"><span class="meta-label">Status:</span>
          <span id="meta-status">—</span></div>
        <div class="meta-row"><span class="meta-label">Birth:</span>
          <span id="meta-by" class="meta-val">—</span></div>
        <div class="meta-row"><span class="meta-label">Death:</span>
          <span id="meta-dy" class="meta-val">—</span></div>
        <div class="meta-row"><span class="meta-label">ESU:</span>
          <span id="meta-url" class="meta-val">—</span></div>
      </div>
      <div id="reasoning-box">
        <strong>AI Reasoning:</strong>
        <span id="reasoning-text">—</span>
      </div>
      <div id="bio-box">
        <strong>Full ESU bio (fetched):</strong>
        <span id="bio-text">—</span>
      </div>
      <button id="bio-toggle" onclick="toggleBio()">▼ Show more</button>
      <div id="decision-area">
        <span id="decision-label">Your verdict:</span>
        <button class="btn btn-correct" id="btn-correct" onclick="decide('correct')">✓ Correct</button>
        <button class="btn btn-wrong"   id="btn-wrong"   onclick="decide('wrong')">✗ Wrong</button>
        <button class="btn btn-skip"    id="btn-skip"    onclick="decide('skip')">— Skip</button>
      </div>
      <div id="comment-row">
        <label>Note:</label>
        <input type="text" id="comment-input" placeholder="Optional: what's wrong, correct status, etc."
               oninput="saveComment()">
      </div>
      <div id="nav-row">
        <button class="btn btn-nav" onclick="navigate(-1)">← Prev</button>
        <button class="btn btn-nav" onclick="navigate(1)">Next →</button>
      </div>
    </div>
  </div>

</div><!-- /main -->

<!-- BOTTOM STATS BAR -->
<div id="bottom-bar">
  <div id="stats-row">
    <span class="stat">Reviewed: <strong id="st-reviewed">0</strong>/200</span>
    <span class="stat">✓ Correct: <strong id="st-correct">0</strong></span>
    <span class="stat">✗ Wrong: <strong id="st-wrong">0</strong></span>
    <span class="stat">— Skip: <strong id="st-skip">0</strong></span>
    <span class="stat">Error rate: <strong id="st-error-rate">—</strong></span>
    <span class="stat">INCLUDE errors: <strong id="st-inc-errors">0</strong>/100</span>
    <span class="stat">EXCLUDE errors: <strong id="st-exc-errors">0</strong>/100</span>
  </div>
</div>

<!-- EXPORT MODAL -->
<div id="modal-overlay" onclick="closeModalIfBackground(event)">
  <div id="modal">
    <h2>⬇ Export Validation Results</h2>
    <p>Your reviews are saved in your browser automatically. Use one of the export options below to save them permanently.</p>
    <div id="export-preview"></div>
    <div id="modal-buttons">
      <button class="btn btn-modal-dl" onclick="downloadJSON()">Download JSON</button>
      <button class="btn btn-modal-dl" onclick="downloadCSV()">Download CSV</button>
      <button class="btn btn-modal-copy" onclick="copyToClipboard()">Copy JSON to clipboard</button>
      <button class="btn btn-modal-close" onclick="closeModal()">Close</button>
    </div>
  </div>
</div>

<script>
// ── DATA ──────────────────────────────────────────────────────────────────
const ENTRIES = {DATA_JS};

// ── STATE ─────────────────────────────────────────────────────────────────
const STORAGE_KEY = 'validation_v26_reviews';

function loadReviews() {{
  try {{
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : {{}};
  }} catch(e) {{ return {{}}; }}
}}

function saveReviews(reviews) {{
  localStorage.setItem(STORAGE_KEY, JSON.stringify(reviews));
}}

let reviews = loadReviews();
let currentIdx = 0;
let bioExpanded = false;

// ── RENDER HELPERS ────────────────────────────────────────────────────────
const STATUS_CLASSES = {{
  'migrated':          's-migrated',
  'non_migrated':      's-non_migrated',
  'internal_transfer': 's-internal_transfer',
  'deported':          's-deported',
  'unknown':           's-unknown',
  'alive':             's-alive',
}};

function statusChip(status) {{
  const cls = STATUS_CLASSES[status] || 's-excluded';
  return `<span class="status-chip ${{cls}}">${{status}}</span>`;
}}

// ── MAIN CARD RENDER ──────────────────────────────────────────────────────
function renderCard(idx) {{
  currentIdx = idx;
  bioExpanded = false;
  const e = ENTRIES[idx];
  const r = reviews[idx] || {{}};

  document.getElementById('idx-badge').textContent = `#${{idx + 1}} of 200`;
  document.getElementById('entry-name').textContent = e.name || '—';

  const grpChip = document.getElementById('group-chip');
  grpChip.textContent = e.group;
  grpChip.className = 'group-chip ' + (e.group === 'INCLUDE' ? 'chip-inc' : 'chip-exc');

  document.getElementById('meta-status').innerHTML = statusChip(e.status);
  document.getElementById('meta-by').textContent = e.by || '—';
  document.getElementById('meta-dy').textContent = e.dy || '—';

  const urlEl = document.getElementById('meta-url');
  if (e.url) {{
    urlEl.innerHTML = `<a class="esu-link" href="${{e.url}}" target="_blank">Open ESU article ↗</a>`;
  }} else {{
    urlEl.textContent = '—';
  }}

  document.getElementById('reasoning-text').textContent = e.reasoning || '—';

  const bioEl = document.getElementById('bio-text');
  const bio = e.bio || '(no bio fetched)';
  bioEl.textContent = bioExpanded ? bio : bio.slice(0, 600) + (bio.length > 600 ? '…' : '');
  document.getElementById('bio-toggle').textContent = bioExpanded ? '▲ Show less' : '▼ Show more';
  document.getElementById('bio-box').style.maxHeight = bioExpanded ? 'none' : '280px';

  // Decision buttons
  ['correct','wrong','skip'].forEach(d => {{
    const btn = document.getElementById('btn-' + d);
    btn.className = `btn btn-${{d}}`;
    if (r.decision === d) btn.className += ` selected-${{d}}`;
  }});

  // Comment
  document.getElementById('comment-input').value = r.comment || '';

  // Highlight sidebar
  renderSidebar();
  updateStats();
  scrollSidebarToActive();
}}

function toggleBio() {{
  bioExpanded = !bioExpanded;
  const e = ENTRIES[currentIdx];
  const bio = e.bio || '(no bio fetched)';
  document.getElementById('bio-text').textContent = bioExpanded ? bio : bio.slice(0, 600) + (bio.length > 600 ? '…' : '');
  document.getElementById('bio-toggle').textContent = bioExpanded ? '▲ Show less' : '▼ Show more';
  document.getElementById('bio-box').style.maxHeight = bioExpanded ? 'none' : '280px';
}}

// ── DECISIONS ─────────────────────────────────────────────────────────────
function decide(decision) {{
  reviews[currentIdx] = reviews[currentIdx] || {{}};
  reviews[currentIdx].decision = decision;
  reviews[currentIdx].name = ENTRIES[currentIdx].name;
  reviews[currentIdx].status = ENTRIES[currentIdx].status;
  reviews[currentIdx].group = ENTRIES[currentIdx].group;
  saveReviews(reviews);
  renderCard(currentIdx);
  // Auto-advance to next unreviewed entry
  const next = findNextUnreviewed(currentIdx + 1);
  if (next !== null) {{
    setTimeout(() => renderCard(next), 350);
  }}
}}

function saveComment() {{
  reviews[currentIdx] = reviews[currentIdx] || {{}};
  reviews[currentIdx].comment = document.getElementById('comment-input').value;
  reviews[currentIdx].name = ENTRIES[currentIdx].name;
  reviews[currentIdx].status = ENTRIES[currentIdx].status;
  reviews[currentIdx].group = ENTRIES[currentIdx].group;
  saveReviews(reviews);
}}

function findNextUnreviewed(startFrom) {{
  for (let i = startFrom; i < ENTRIES.length; i++) {{
    if (!reviews[i] || !reviews[i].decision) return i;
  }}
  for (let i = 0; i < startFrom; i++) {{
    if (!reviews[i] || !reviews[i].decision) return i;
  }}
  return null;
}}

// ── NAVIGATION ────────────────────────────────────────────────────────────
function navigate(dir) {{
  let next = currentIdx + dir;
  if (next < 0) next = ENTRIES.length - 1;
  if (next >= ENTRIES.length) next = 0;
  renderCard(next);
}}

document.addEventListener('keydown', (e) => {{
  if (['INPUT','TEXTAREA'].includes(e.target.tagName)) return;
  if (e.key === 'ArrowRight' || e.key === 'l') navigate(1);
  if (e.key === 'ArrowLeft'  || e.key === 'h') navigate(-1);
  if (e.key === 'c' || e.key === 'y') decide('correct');
  if (e.key === 'w' || e.key === 'n') decide('wrong');
  if (e.key === 's') decide('skip');
}});

// ── SIDEBAR ───────────────────────────────────────────────────────────────
function renderSidebar() {{
  const search = document.getElementById('search-box').value.toLowerCase();
  const filter = document.getElementById('filter-status').value;
  const list = document.getElementById('sidebar-list');

  const filtered = ENTRIES.filter((e, i) => {{
    if (search && !e.name.toLowerCase().includes(search)) return false;
    if (filter === 'unseen')  return !reviews[i] || !reviews[i].decision;
    if (filter === 'correct') return reviews[i]?.decision === 'correct';
    if (filter === 'wrong')   return reviews[i]?.decision === 'wrong';
    if (filter === 'skip')    return reviews[i]?.decision === 'skip';
    if (filter === 'INCLUDE') return e.group === 'INCLUDE';
    if (filter === 'EXCLUDE') return e.group === 'EXCLUDE';
    return true;
  }});

  list.innerHTML = filtered.map(e => {{
    const i = e._idx !== undefined ? e._idx : ENTRIES.indexOf(e);
    // find real index
    const realIdx = ENTRIES.findIndex(x => x === e);
    const r = reviews[realIdx] || {{}};
    const dotCls = r.decision === 'correct' ? 'dot-correct'
                 : r.decision === 'wrong'   ? 'dot-wrong'
                 : r.decision === 'skip'    ? 'dot-skip'
                 : 'dot-unseen';
    const active = realIdx === currentIdx ? ' active' : '';
    const badge = e.group === 'INCLUDE'
      ? '<span class="badge badge-inc">IN</span>'
      : '<span class="badge badge-exc">EX</span>';
    return `<div class="sidebar-entry${{active}}" onclick="renderCard(${{realIdx}})">
      <div class="dot ${{dotCls}}"></div>
      <span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${{e.name}}</span>
      ${{badge}}
    </div>`;
  }}).join('');
}}

function scrollSidebarToActive() {{
  const active = document.querySelector('.sidebar-entry.active');
  if (active) active.scrollIntoView({{block: 'nearest'}});
}}

// ── STATS ─────────────────────────────────────────────────────────────────
function updateStats() {{
  const all = Object.values(reviews).filter(r => r.decision);
  const correct = all.filter(r => r.decision === 'correct').length;
  const wrong   = all.filter(r => r.decision === 'wrong').length;
  const skip    = all.filter(r => r.decision === 'skip').length;

  const incWrong = Object.values(reviews).filter(r => r.decision === 'wrong' && r.group === 'INCLUDE').length;
  const excWrong = Object.values(reviews).filter(r => r.decision === 'wrong' && r.group === 'EXCLUDE').length;
  const incReviewed = Object.values(reviews).filter(r => r.decision && r.group === 'INCLUDE').length;
  const excReviewed = Object.values(reviews).filter(r => r.decision && r.group === 'EXCLUDE').length;

  document.getElementById('st-reviewed').textContent  = all.length;
  document.getElementById('st-correct').textContent   = correct;
  document.getElementById('st-wrong').textContent     = wrong;
  document.getElementById('st-skip').textContent      = skip;
  document.getElementById('st-inc-errors').textContent = `${{incWrong}}/${{incReviewed}}`;
  document.getElementById('st-exc-errors').textContent = `${{excWrong}}/${{excReviewed}}`;

  const reviewed_nonSkip = correct + wrong;
  const errRate = reviewed_nonSkip > 0
    ? (100 * wrong / reviewed_nonSkip).toFixed(1) + '%'
    : '—';
  document.getElementById('st-error-rate').textContent = errRate;

  const pct = (100 * all.length / 200).toFixed(0);
  document.getElementById('progress-bar').style.width = pct + '%';
  document.getElementById('progress-text').textContent = `${{all.length}} / 200`;
}}

// ── EXPORT ────────────────────────────────────────────────────────────────
function buildExportData() {{
  return ENTRIES.map((e, i) => {{
    const r = reviews[i] || {{}};
    return {{
      idx:             i,
      name:            e.name,
      birth_year:      e.by,
      death_year:      e.dy,
      migration_status: e.status,
      sample_group:    e.group,
      decision:        r.decision || 'unreviewed',
      comment:         r.comment || '',
      article_url:     e.url,
    }};
  }});
}}

function buildCSV(data) {{
  const cols = ['idx','name','birth_year','death_year','migration_status','sample_group','decision','comment','article_url'];
  const esc = v => `"${{String(v).replace(/"/g, '""')}}"`;
  return [cols.join(','), ...data.map(r => cols.map(c => esc(r[c])).join(','))].join('\\n');
}}

function openExportModal() {{
  const data = buildExportData();
  const reviewed = data.filter(d => d.decision !== 'unreviewed');
  const wrong    = data.filter(d => d.decision === 'wrong');
  const preview  = JSON.stringify({{
    summary: {{
      total: 200, reviewed: reviewed.length,
      correct: data.filter(d => d.decision === 'correct').length,
      wrong: wrong.length, skip: data.filter(d => d.decision === 'skip').length,
      error_rate_pct: reviewed.filter(d => d.decision !== 'skip').length > 0
        ? (100 * wrong.length / reviewed.filter(d => d.decision !== 'skip').length).toFixed(2)
        : 'N/A',
    }},
    entries: data.slice(0, 5),
  }}, null, 2) + '\\n  ... (truncated)';
  document.getElementById('export-preview').textContent = preview;
  document.getElementById('modal-overlay').classList.add('show');
}}

function closeModal() {{
  document.getElementById('modal-overlay').classList.remove('show');
}}

function closeModalIfBackground(e) {{
  if (e.target.id === 'modal-overlay') closeModal();
}}

function downloadJSON() {{
  const data = buildExportData();
  const blob = new Blob([JSON.stringify(data, null, 2)], {{type: 'application/json'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'validation_v2_6_results.json';
  a.click();
}}

function downloadCSV() {{
  const data = buildExportData();
  const blob = new Blob([buildCSV(data)], {{type: 'text/csv;charset=utf-8;'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'validation_v2_6_results.csv';
  a.click();
}}

function copyToClipboard() {{
  const data = buildExportData();
  navigator.clipboard.writeText(JSON.stringify(data, null, 2)).then(() => {{
    alert('Copied to clipboard!');
  }});
}}

// ── INIT ──────────────────────────────────────────────────────────────────
// Assign real indices to entries
ENTRIES.forEach((e, i) => {{ e._idx = i; }});

renderCard(0);
renderSidebar();
updateStats();
</script>

</body>
</html>
"""

with open(HTML_OUT, 'w', encoding='utf-8') as f:
    f.write(HTML.replace('{DATA_JS}', DATA_JS))

print(f"HTML reviewer → {HTML_OUT}")
print(f"CSV sample    → {CSV_OUT}")
print("Done!")
