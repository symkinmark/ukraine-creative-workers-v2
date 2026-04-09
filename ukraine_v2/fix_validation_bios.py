"""
fix_validation_bios.py
Re-fetches ESU bios for existing validation_v2_6_sample.csv with correct extractor,
then rebuilds the HTML reviewer.

The previous extraction was broken because:
  1. Fallback regex had no <div prefix — matched JS string $('[itemprop="articleBody"]')
  2. Primary regex used (.*?)</div> — stops at first nested inner div, not the outer body

Fix: strip <script> tags first, then find the opening <div> tag and take everything
until </article>.
"""

import csv
import os
import json
import re
import time
import requests

PROJECT  = os.path.dirname(os.path.abspath(__file__))
VAL_DIR  = os.path.join(PROJECT, 'validation')
CSV_IN   = os.path.join(VAL_DIR, 'validation_v2_6_sample.csv')
CSV_OUT  = os.path.join(VAL_DIR, 'validation_v2_6_sample.csv')   # overwrite
HTML_OUT = os.path.join(VAL_DIR, 'validation_v2_6_reviewer.html')

SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'Mozilla/5.0 (research; contact: research@example.com)'})

def fetch_bio(url, timeout=12):
    """
    Extract article text from an ESU article page.
    Strategy:
      1. Strip <script> and <style> tags to avoid matching JS strings.
      2. Find opening <div itemprop="articleBody"> tag.
      3. Grab everything from after that tag until </article>.
      4. Strip remaining HTML tags, collapse whitespace.
      Fallback: citation_abstract meta → description meta.
    """
    if not url or not url.startswith('http'):
        return ''
    try:
        resp = SESSION.get(url, timeout=timeout)
        resp.encoding = 'utf-8'
        html = resp.text

        # Strip scripts and styles so JS strings don't confuse our regex
        clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        clean = re.sub(r'<style[^>]*>.*?</style>',  '', clean, flags=re.DOTALL | re.IGNORECASE)

        # Find the opening <div itemprop="articleBody"> (any quote style, any extra attrs)
        m_open = re.search(r'<div\b[^>]*\bitemprop=["\']articleBody["\'][^>]*>',
                           clean, re.IGNORECASE)
        if m_open:
            start = m_open.end()
            # Grab until </article> (the article body sits directly inside <article>)
            close_idx = clean.find('</article>', start)
            if close_idx > start:
                raw = clean[start:close_idx]
            else:
                raw = clean[start:start + 15000]
            text = re.sub(r'<[^>]+>', ' ', raw)
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text) > 100:
                return text[:5000]

        # Fallback 1 — citation_abstract meta
        m2 = re.search(r'<meta[^>]+name=["\']citation_abstract["\'][^>]+content="([^"]+)"', html)
        if not m2:
            m2 = re.search(r'<meta[^>]+content="([^"]+)"[^>]+name=["\']citation_abstract["\']', html)
        if m2:
            return m2.group(1).strip()[:3000]

        # Fallback 2 — description meta
        m3 = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content="([^"]+)"', html)
        if m3:
            return m3.group(1).strip()[:2000]

        return '[bio not found]'
    except Exception as e:
        return f'[fetch error: {e}]'


# ---------------------------------------------------------------------------
# Load existing sample CSV
# ---------------------------------------------------------------------------
with open(CSV_IN, encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

print(f"Loaded {len(rows)} rows from {CSV_IN}")
print("Re-fetching bios with fixed extractor (200 @ 0.4s ≈ 1.5 min)...")

for i, row in enumerate(rows):
    bio = fetch_bio(row.get('article_url', ''))
    row['full_bio'] = bio
    if (i + 1) % 20 == 0:
        print(f"  {i+1}/{len(rows)} — last: {bio[:80].replace(chr(10),' ')!r}")
    time.sleep(0.4)

print("All bios re-fetched.")

# Spot-check: print first 3 bios
for row in rows[:3]:
    print(f"\n[{row['idx']}] {row['name']}")
    print(f"  bio[0:200]: {row['full_bio'][:200]}")

# ---------------------------------------------------------------------------
# Save updated CSV
# ---------------------------------------------------------------------------
fieldnames = ['idx', 'name', 'birth_year', 'death_year', 'migration_status',
              'migration_reasoning', 'notes', 'article_url', 'sample_group', 'full_bio']

with open(CSV_OUT, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow({k: row.get(k, '') for k in fieldnames})

print(f"\nCSV updated → {CSV_OUT}")

# ---------------------------------------------------------------------------
# Rebuild HTML reviewer
# ---------------------------------------------------------------------------
# Prepare entries JSON
entries = []
for row in rows:
    entries.append({
        'idx':       int(row.get('idx', 0)),
        'name':      row.get('name', ''),
        'by':        row.get('birth_year', ''),
        'dy':        row.get('death_year', ''),
        'status':    row.get('migration_status', ''),
        'reasoning': row.get('migration_reasoning', '')[:600],
        'notes':     row.get('notes', '')[:300],
        'url':       row.get('article_url', ''),
        'group':     row.get('sample_group', ''),
        'bio':       row.get('full_bio', '')[:3000],
    })

entries_json = json.dumps(entries, ensure_ascii=False)

HTML = f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<title>V2.6 Validation Reviewer (200 entries)</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 14px; background: #f0f2f5; color: #1a1a1a; height: 100vh; overflow: hidden; }}
#app {{ display: flex; height: 100vh; }}

/* ── Sidebar ── */
#sidebar {{ width: 280px; min-width: 200px; background: #1e2533; color: #c8cdd8;
            display: flex; flex-direction: column; overflow: hidden; }}
#sidebar-header {{ padding: 12px 14px; background: #161b27; }}
#sidebar-header h2 {{ font-size: 13px; color: #e8ecf4; margin-bottom: 6px; }}
#stats-bar {{ font-size: 11px; color: #8892a4; line-height: 1.6; }}
#stats-bar span {{ display: inline-block; margin-right: 8px; }}
.stat-correct  {{ color: #4caf50; }}
.stat-wrong    {{ color: #f44336; }}
.stat-skip     {{ color: #ff9800; }}
.stat-unseen   {{ color: #8892a4; }}
#search-box {{ margin: 8px 14px; padding: 5px 8px; background: #2a3248;
               border: 1px solid #3a4460; border-radius: 4px; color: #c8cdd8; font-size: 12px;
               width: calc(100% - 28px); }}
#filter-bar {{ display: flex; gap: 4px; padding: 0 14px 8px; flex-wrap: wrap; }}
.filter-btn {{ font-size: 10px; padding: 2px 7px; border: 1px solid #3a4460; border-radius: 12px;
               background: transparent; color: #8892a4; cursor: pointer; }}
.filter-btn.active {{ background: #3a5bcc; border-color: #3a5bcc; color: #fff; }}
#entry-list {{ flex: 1; overflow-y: auto; }}
.entry-item {{ padding: 8px 14px; border-bottom: 1px solid #252c3f; cursor: pointer;
               transition: background 0.1s; }}
.entry-item:hover {{ background: #252c3f; }}
.entry-item.active {{ background: #2a3a6a; }}
.entry-item.decided-correct {{ border-left: 3px solid #4caf50; }}
.entry-item.decided-wrong   {{ border-left: 3px solid #f44336; }}
.entry-item.decided-skip    {{ border-left: 3px solid #ff9800; }}
.entry-name {{ font-size: 12px; color: #d0d5e0; white-space: nowrap;
               overflow: hidden; text-overflow: ellipsis; }}
.entry-meta {{ font-size: 10px; color: #5a6480; margin-top: 2px; }}
.badge {{ display: inline-block; font-size: 9px; padding: 1px 5px; border-radius: 3px;
          font-weight: 600; margin-right: 4px; }}
.badge-inc {{ background: #1a3a2a; color: #4caf50; }}
.badge-exc {{ background: #3a1a1a; color: #ef5350; }}

/* ── Main panel ── */
#main {{ flex: 1; display: flex; flex-direction: column; overflow: hidden; }}
#toolbar {{ background: #fff; border-bottom: 1px solid #e0e4ed; padding: 10px 20px;
             display: flex; align-items: center; gap: 12px; flex-shrink: 0; }}
#toolbar h1 {{ font-size: 15px; color: #333; flex: 1; }}
.kbd-hint {{ font-size: 11px; color: #888; }}
kbd {{ background: #f0f0f0; border: 1px solid #ccc; border-radius: 3px; padding: 1px 5px;
       font-size: 11px; font-family: monospace; }}
#nav-btns {{ display: flex; gap: 6px; }}
.nav-btn {{ padding: 4px 12px; border: 1px solid #d0d5e0; border-radius: 4px;
             background: #fff; cursor: pointer; font-size: 12px; color: #444; }}
.nav-btn:hover {{ background: #f5f7fb; }}
#progress-bar {{ height: 3px; background: #e8ecf5; flex-shrink: 0; }}
#progress-fill {{ height: 3px; background: #3a5bcc; transition: width 0.3s; width: 0%; }}
#content-area {{ flex: 1; overflow-y: auto; padding: 20px 28px; }}
#entry-card {{ background: #fff; border-radius: 8px; box-shadow: 0 1px 6px rgba(0,0,0,0.08);
               padding: 24px; max-width: 860px; }}
#entry-card h2 {{ font-size: 20px; color: #111; margin-bottom: 4px; }}
.meta-row {{ font-size: 12px; color: #666; margin-bottom: 14px; }}
.meta-row a {{ color: #3a5bcc; text-decoration: none; }}
.meta-row a:hover {{ text-decoration: underline; }}
.section-label {{ font-size: 10px; font-weight: 700; text-transform: uppercase;
                   letter-spacing: 0.05em; color: #999; margin-bottom: 4px; }}
.section-box {{ background: #f7f9fc; border-left: 3px solid #d0d8f0; padding: 10px 14px;
                border-radius: 0 6px 6px 0; margin-bottom: 14px; font-size: 13px;
                line-height: 1.55; color: #333; max-height: 160px; overflow-y: auto; }}
.bio-box {{ background: #f7f9fc; border-left: 3px solid #b0c4de; padding: 12px 14px;
            border-radius: 0 6px 6px 0; margin-bottom: 20px; font-size: 13px;
            line-height: 1.6; color: #333; max-height: 280px; overflow-y: auto; }}
#decision-row {{ display: flex; gap: 10px; margin-top: 6px; flex-wrap: wrap; }}
.dec-btn {{ flex: 1; min-width: 120px; padding: 12px; border-radius: 6px; border: 2px solid transparent;
             font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.15s; }}
.dec-btn.correct {{ background: #e8f5e9; color: #2e7d32; border-color: #a5d6a7; }}
.dec-btn.correct:hover, .dec-btn.correct.active {{ background: #4caf50; color: #fff; border-color: #4caf50; }}
.dec-btn.wrong {{ background: #ffebee; color: #c62828; border-color: #ef9a9a; }}
.dec-btn.wrong:hover, .dec-btn.wrong.active {{ background: #f44336; color: #fff; border-color: #f44336; }}
.dec-btn.skip {{ background: #fff8e1; color: #e65100; border-color: #ffe082; }}
.dec-btn.skip:hover, .dec-btn.skip.active {{ background: #ff9800; color: #fff; border-color: #ff9800; }}

/* ── Export modal ── */
#export-overlay {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 100; }}
#export-modal {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                 background: #fff; border-radius: 10px; padding: 28px; min-width: 400px;
                 box-shadow: 0 8px 40px rgba(0,0,0,0.3); }}
#export-modal h3 {{ font-size: 16px; margin-bottom: 16px; }}
.export-btn {{ display: block; width: 100%; padding: 10px 14px; margin-bottom: 10px;
               border: 1px solid #d0d5e0; border-radius: 6px; background: #f5f7fb;
               cursor: pointer; font-size: 13px; text-align: left; }}
.export-btn:hover {{ background: #e8ecf5; }}
.export-close {{ margin-top: 8px; background: #fff; border: 1px solid #ccc; padding: 8px;
                 border-radius: 6px; cursor: pointer; width: 100%; font-size: 13px; }}
</style>
</head>
<body>
<div id="app">

  <!-- Sidebar -->
  <div id="sidebar">
    <div id="sidebar-header">
      <h2>Validation Reviewer v2.6</h2>
      <div id="stats-bar">
        <span class="stat-correct">✓ <span id="s-correct">0</span></span>
        <span class="stat-wrong">✗ <span id="s-wrong">0</span></span>
        <span class="stat-skip">~ <span id="s-skip">0</span></span>
        <span class="stat-unseen">? <span id="s-unseen">200</span></span>
        <br>
        <span id="s-pct">0%</span> complete
      </div>
    </div>
    <input id="search-box" type="text" placeholder="Search name…" oninput="filterList()">
    <div id="filter-bar">
      <button class="filter-btn active" onclick="setFilter('all',this)">All</button>
      <button class="filter-btn" onclick="setFilter('unseen',this)">Unseen</button>
      <button class="filter-btn" onclick="setFilter('correct',this)">Correct</button>
      <button class="filter-btn" onclick="setFilter('wrong',this)">Wrong</button>
      <button class="filter-btn" onclick="setFilter('INCLUDE',this)">INCLUDE</button>
      <button class="filter-btn" onclick="setFilter('EXCLUDE',this)">EXCLUDE</button>
    </div>
    <div id="entry-list"></div>
  </div>

  <!-- Main -->
  <div id="main">
    <div id="toolbar">
      <h1 id="toolbar-title">Select an entry</h1>
      <span class="kbd-hint">
        <kbd>C</kbd> Correct &nbsp;
        <kbd>W</kbd> Wrong &nbsp;
        <kbd>S</kbd> Skip &nbsp;
        <kbd>←</kbd><kbd>→</kbd> Navigate
      </span>
      <div id="nav-btns">
        <button class="nav-btn" onclick="navigate(-1)">← Prev</button>
        <button class="nav-btn" onclick="navigate(1)">Next →</button>
        <button class="nav-btn" onclick="document.getElementById('export-overlay').style.display='block'">Export ↗</button>
      </div>
    </div>
    <div id="progress-bar"><div id="progress-fill"></div></div>
    <div id="content-area">
      <div id="entry-card">
        <p style="color:#999;text-align:center;padding:40px 0">Select an entry from the sidebar to begin reviewing.</p>
      </div>
    </div>
  </div>

</div>

<!-- Export modal -->
<div id="export-overlay" onclick="if(event.target===this)this.style.display='none'">
  <div id="export-modal">
    <h3>Export Results</h3>
    <button class="export-btn" onclick="downloadJSON()">⬇ Download JSON</button>
    <button class="export-btn" onclick="downloadCSV()">⬇ Download CSV</button>
    <button class="export-btn" onclick="copyToClipboard()">📋 Copy JSON to clipboard</button>
    <div id="export-count" style="font-size:12px;color:#888;margin:8px 0"></div>
    <button class="export-close" onclick="document.getElementById('export-overlay').style.display='none'">Close</button>
  </div>
</div>

<script>
const ENTRIES = {entries_json};
const STORAGE_KEY = 'ukraine_v26_validation_decisions';

// Load decisions from localStorage
let decisions = {{}};
try {{ decisions = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}'); }} catch(e) {{}}

let currentIdx = null;
let activeFilter = 'all';
let searchQuery = '';

// ── Render sidebar list ──
function renderList() {{
  const list = document.getElementById('entry-list');
  const q = searchQuery.toLowerCase();
  list.innerHTML = '';
  ENTRIES.forEach((e, i) => {{
    const dec = decisions[e.idx];
    // filter
    if (activeFilter === 'unseen'   && dec) return;
    if (activeFilter === 'correct'  && dec !== 'correct') return;
    if (activeFilter === 'wrong'    && dec !== 'wrong') return;
    if (activeFilter === 'INCLUDE'  && e.group !== 'INCLUDE') return;
    if (activeFilter === 'EXCLUDE'  && e.group !== 'EXCLUDE') return;
    if (q && !e.name.toLowerCase().includes(q)) return;

    const div = document.createElement('div');
    div.className = 'entry-item' +
      (dec === 'correct' ? ' decided-correct' : dec === 'wrong' ? ' decided-wrong' : dec === 'skip' ? ' decided-skip' : '') +
      (currentIdx === e.idx ? ' active' : '');
    div.dataset.idx = e.idx;
    div.innerHTML = `<div class="entry-name">${{e.idx + 1}}. ${{e.name}}</div>
      <div class="entry-meta">
        <span class="badge ${{e.group === 'INCLUDE' ? 'badge-inc' : 'badge-exc'}}">${{e.group}}</span>
        ${{e.status}} · ${{e.by||'?'}}–${{e.dy||'?'}}
        ${{dec ? ' · <b>' + (dec==='correct'?'✓':dec==='wrong'?'✗':'~') + '</b>' : ''}}
      </div>`;
    div.onclick = () => showEntry(e.idx);
    list.appendChild(div);
  }});
}}

// ── Show entry ──
function showEntry(idx) {{
  currentIdx = idx;
  const e = ENTRIES.find(x => x.idx === idx);
  if (!e) return;
  document.getElementById('toolbar-title').textContent = `[${{idx+1}}/200] ${{e.name}}`;

  const dec = decisions[idx] || '';
  const card = document.getElementById('entry-card');
  card.innerHTML = `
    <h2>${{e.name}}</h2>
    <div class="meta-row">
      ${{e.by||'?'}} – ${{e.dy||'?'}} &nbsp;|&nbsp; <b>${{e.status}}</b>
      &nbsp;|&nbsp; <span class="badge ${{e.group==='INCLUDE'?'badge-inc':'badge-exc'}}">${{e.group}}</span>
      &nbsp;|&nbsp; <a href="${{e.url}}" target="_blank">ESU article ↗</a>
    </div>
    ${{e.bio ? `<div class="section-label">ESU Bio</div><div class="bio-box">${{e.bio.replace(/</g,'&lt;')}}</div>` : ''}}
    ${{e.notes ? `<div class="section-label">Classifier Notes</div><div class="section-box">${{e.notes.replace(/</g,'&lt;')}}</div>` : ''}}
    ${{e.reasoning ? `<div class="section-label">Migration Reasoning</div><div class="section-box">${{e.reasoning.replace(/</g,'&lt;')}}</div>` : ''}}
    <div id="decision-row">
      <button class="dec-btn correct ${{dec==='correct'?'active':''}}" onclick="decide(${{idx}},'correct')">✓ Correct <small>(C)</small></button>
      <button class="dec-btn wrong   ${{dec==='wrong'  ?'active':''}}" onclick="decide(${{idx}},'wrong'  )">✗ Wrong   <small>(W)</small></button>
      <button class="dec-btn skip    ${{dec==='skip'   ?'active':''}}" onclick="decide(${{idx}},'skip'   )">~ Skip    <small>(S)</small></button>
    </div>`;
  renderList();
  updateStats();
}}

// ── Decision ──
function decide(idx, verdict) {{
  decisions[idx] = verdict;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(decisions));
  updateStats();
  renderList();

  // Auto-advance after 400ms
  setTimeout(() => {{
    const visible = [...document.querySelectorAll('.entry-item')].map(el => parseInt(el.dataset.idx));
    const pos = visible.indexOf(idx);
    if (pos >= 0 && pos < visible.length - 1) showEntry(visible[pos+1]);
    else if (pos >= 0 && pos > 0) showEntry(visible[pos-1]);
    else renderList();
  }}, 400);
}}

// ── Navigate ──
function navigate(dir) {{
  const all = ENTRIES.map(e => e.idx);
  const pos = all.indexOf(currentIdx);
  const next = pos + dir;
  if (next >= 0 && next < all.length) showEntry(all[next]);
}}

// ── Stats ──
function updateStats() {{
  const decided = Object.values(decisions);
  const correct = decided.filter(d => d==='correct').length;
  const wrong   = decided.filter(d => d==='wrong').length;
  const skip    = decided.filter(d => d==='skip').length;
  const unseen  = 200 - correct - wrong - skip;
  document.getElementById('s-correct').textContent = correct;
  document.getElementById('s-wrong').textContent   = wrong;
  document.getElementById('s-skip').textContent    = skip;
  document.getElementById('s-unseen').textContent  = unseen;
  const pct = Math.round((correct+wrong+skip)/200*100);
  document.getElementById('s-pct').textContent = pct + '%';
  document.getElementById('progress-fill').style.width = pct + '%';
}}

// ── Filter / Search ──
function setFilter(f, btn) {{
  activeFilter = f;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderList();
}}
function filterList() {{
  searchQuery = document.getElementById('search-box').value;
  renderList();
}}

// ── Keyboard shortcuts ──
document.addEventListener('keydown', e => {{
  if (['INPUT','TEXTAREA'].includes(e.target.tagName)) return;
  if (currentIdx === null) return;
  if (e.key === 'c' || e.key === 'C') decide(currentIdx, 'correct');
  if (e.key === 'w' || e.key === 'W') decide(currentIdx, 'wrong');
  if (e.key === 's' || e.key === 'S') decide(currentIdx, 'skip');
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') navigate(1);
  if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   navigate(-1);
}});

// ── Export functions ──
function getExportData() {{
  return ENTRIES.map(e => ({{
    idx: e.idx,
    name: e.name,
    birth_year: e.by,
    death_year: e.dy,
    migration_status: e.status,
    sample_group: e.group,
    decision: decisions[e.idx] || 'unseen',
    url: e.url,
  }}));
}}
function downloadJSON() {{
  const data = getExportData();
  const blob = new Blob([JSON.stringify(data, null, 2)], {{type: 'application/json'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'validation_v2_6_results.json';
  a.click();
  document.getElementById('export-count').textContent =
    `${{Object.keys(decisions).length}} decisions exported.`;
}}
function downloadCSV() {{
  const data = getExportData();
  const header = ['idx','name','birth_year','death_year','migration_status','sample_group','decision','url'];
  const lines = [header.join(',')];
  data.forEach(r => lines.push(header.map(k => JSON.stringify(r[k]??'')).join(',')));
  const blob = new Blob([lines.join('\\n')], {{type: 'text/csv'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'validation_v2_6_results.csv';
  a.click();
}}
function copyToClipboard() {{
  navigator.clipboard.writeText(JSON.stringify(getExportData(), null, 2))
    .then(() => {{ document.getElementById('export-count').textContent = 'Copied!'; }});
}}

// ── Init ──
renderList();
updateStats();
// Open first entry automatically
if (ENTRIES.length > 0) showEntry(ENTRIES[0].idx);
</script>
</body>
</html>"""

with open(HTML_OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"\nHTML reviewer rebuilt → {HTML_OUT}")
print(f"Open in browser to start reviewing.")

# Quick sanity check on bio quality
broken = sum(1 for r in rows if not r.get('full_bio') or r['full_bio'].startswith('[') or 'itemprop' in r['full_bio'] or len(r.get('full_bio','')) < 50)
good   = len(rows) - broken
print(f"\nBio quality: {good}/200 look good, {broken} may be broken/empty")
