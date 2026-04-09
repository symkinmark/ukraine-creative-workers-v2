"""
stage15_build_s14_reviewer.py
Builds an HTML reviewer for the 135 Stage 14 reclassified entries.
Fetches bios from ESU and embeds them in the page.
"""

import csv, json, os, re, time
import requests

PROJECT = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(PROJECT, 'esu_creative_workers_v2_6.csv')
OUT_HTML = os.path.join(PROJECT, 'validation', 'stage14_reviewer.html')

# Load S14 entries
with open(CSV_PATH, encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

s14_entries = [r for r in rows if 'S14-reclassified' in r.get('migration_reasoning', '')]
print(f"Found {len(s14_entries)} Stage 14 entries")

# Fetch bios
SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'Mozilla/5.0 (research)'})

def fetch_bio(url, timeout=12):
    if not url or not url.startswith('http'):
        return ''
    try:
        resp = SESSION.get(url, timeout=timeout)
        resp.encoding = 'utf-8'
        html = resp.text
        clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.IGNORECASE)
        clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL|re.IGNORECASE)
        m = re.search(r'<div\b[^>]*\bitemprop=["\']articleBody["\'][^>]*>', clean, re.IGNORECASE)
        if m:
            start = m.end()
            end = clean.find('</article>', start)
            raw = clean[start:end] if end > start else clean[start:start+15000]
            text = re.sub(r'<[^>]+>', ' ', raw)
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text) > 100:
                return text[:5000]
        m2 = re.search(r'<meta[^>]+name=["\']citation_abstract["\'][^>]+content="([^"]+)"', html)
        if not m2:
            m2 = re.search(r'<meta[^>]+content="([^"]+)"[^>]+name=["\']citation_abstract["\']', html)
        if m2:
            return m2.group(1).strip()[:2000]
    except Exception as e:
        return f'[fetch error: {e}]'
    return ''

print("Fetching bios from ESU...")
entries_data = []
for i, row in enumerate(s14_entries):
    url = row.get('article_url', '')
    bio = fetch_bio(url)
    time.sleep(0.3)
    reasoning = row.get('migration_reasoning', '')
    # Strip S14-reclassified: prefix to get just the reasoning text
    if reasoning.startswith('S14-reclassified:'):
        reasoning = reasoning[len('S14-reclassified:'):].strip()
    entries_data.append({
        'idx': int(float(row.get('idx', i))),
        'name': row.get('name', ''),
        'birth_year': row.get('birth_year', ''),
        'death_year': row.get('death_year', ''),
        'migration_status': row.get('migration_status', ''),
        'reasoning': reasoning,
        'article_url': url,
        'bio': bio,
    })
    if (i+1) % 10 == 0:
        print(f"  {i+1}/{len(s14_entries)} fetched...")

print(f"Done fetching. Building HTML...")

entries_json = json.dumps(entries_data, ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Stage 14 Validation Reviewer</title>
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
  h1 {{ font-size: 1.3em; color: #333; }}
  #progress {{ background: #fff; padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,.1); display:flex; justify-content:space-between; align-items:center; }}
  #progress .counts span {{ margin-right: 16px; font-weight: 600; }}
  .correct-count {{ color: #2a7a2a; }}
  .wrong-count {{ color: #c0392b; }}
  .skip-count {{ color: #888; }}
  #card {{ background: #fff; border-radius: 10px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,.12); }}
  .meta {{ color: #555; font-size: 0.9em; margin-bottom: 8px; }}
  .status-badge {{ display:inline-block; padding: 3px 10px; border-radius: 4px; font-weight:700; font-size:0.85em; margin-bottom:12px; }}
  .migrated {{ background:#d4edda; color:#155724; }}
  .non_migrated {{ background:#e2e3e5; color:#383d41; }}
  .deported {{ background:#f8d7da; color:#721c24; }}
  .internal_transfer {{ background:#fff3cd; color:#856404; }}
  .excluded_pre_soviet {{ background:#e8d5f5; color:#4a235a; }}
  .excluded_non_ukrainian {{ background:#fdebd0; color:#7e5109; }}
  .excluded_bad_dates {{ background:#d6eaf8; color:#154360; }}
  .name {{ font-size: 1.4em; font-weight: 700; margin-bottom: 4px; }}
  .reasoning-box {{ background:#f8f9fa; border-left:4px solid #4a90d9; padding:10px 14px; border-radius:4px; font-size:0.9em; margin:12px 0; color:#333; }}
  .bio-box {{ background:#fffef5; border:1px solid #e0e0c0; border-radius:6px; padding:12px 16px; max-height:280px; overflow-y:auto; font-size:0.88em; line-height:1.6; color:#444; margin-top:10px; }}
  .bio-label {{ font-size:0.8em; font-weight:600; color:#888; text-transform:uppercase; letter-spacing:.05em; margin-top:12px; }}
  .buttons {{ display:flex; gap:12px; margin-top:20px; }}
  button {{ padding: 10px 28px; border:none; border-radius:6px; font-size:1em; font-weight:700; cursor:pointer; transition: transform .1s, opacity .1s; }}
  button:active {{ transform: scale(.97); }}
  #btn-correct {{ background:#27ae60; color:#fff; }}
  #btn-wrong {{ background:#e74c3c; color:#fff; }}
  #btn-skip {{ background:#95a5a6; color:#fff; }}
  #notes-section {{ margin-top:14px; }}
  #notes-section label {{ font-size:0.85em; font-weight:600; color:#555; display:block; margin-bottom:4px; }}
  #notes-section label.red {{ color:#c0392b; }}
  #note-input {{ width:100%; box-sizing:border-box; padding:8px 10px; border:1.5px solid #ccc; border-radius:6px; font-size:0.9em; resize:vertical; min-height:60px; }}
  #note-input:focus {{ border-color:#4a90d9; outline:none; }}
  #note-saved {{ font-size:0.8em; color:#27ae60; display:none; margin-left:8px; }}
  .nav {{ display:flex; gap:8px; margin-top:16px; }}
  .nav button {{ padding:6px 16px; font-size:0.85em; background:#ecf0f1; color:#333; font-weight:600; }}
  #esu-link {{ font-size:0.85em; color:#4a90d9; text-decoration:none; }}
  #esu-link:hover {{ text-decoration:underline; }}
  #sidebar {{ position:fixed; right:16px; top:16px; width:180px; background:#fff; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,.12); padding:12px; max-height:90vh; overflow-y:auto; }}
  #sidebar h3 {{ font-size:0.85em; margin:0 0 8px; color:#555; }}
  .sb-item {{ font-size:0.78em; padding:3px 6px; border-radius:4px; margin-bottom:2px; cursor:pointer; display:flex; justify-content:space-between; }}
  .sb-item:hover {{ background:#f0f0f0; }}
  .sb-correct {{ color:#27ae60; }}
  .sb-wrong {{ color:#e74c3c; font-weight:700; }}
  .sb-skip {{ color:#888; }}
  .sb-unseen {{ color:#bbb; }}
  .sb-current {{ background:#e8f0fe !important; font-weight:700; }}
  #export-btn {{ background:#3498db; color:#fff; padding:8px 14px; font-size:0.85em; border:none; border-radius:6px; cursor:pointer; margin-top:8px; width:100%; font-weight:700; }}
</style>
</head>
<body>
<h1>Stage 14 Validation — {len(entries_data)} entries</h1>

<div id="progress">
  <div class="counts">
    <span class="correct-count">✓ <span id="n-correct">0</span></span>
    <span class="wrong-count">✗ <span id="n-wrong">0</span></span>
    <span class="skip-count">– <span id="n-skip">0</span></span>
    <span style="color:#aaa">unseen: <span id="n-unseen">{len(entries_data)}</span></span>
  </div>
  <div><strong id="pos-label">1 / {len(entries_data)}</strong></div>
</div>

<div id="card">
  <div class="meta" id="meta-line"></div>
  <div class="name" id="entry-name"></div>
  <div id="status-badge"></div>
  <a id="esu-link" href="#" target="_blank">View on ESU →</a>
  <div class="bio-label">Haiku reasoning</div>
  <div class="reasoning-box" id="entry-reasoning"></div>
  <div class="bio-label">ESU bio</div>
  <div class="bio-box" id="entry-bio"></div>
  <div class="buttons">
    <button id="btn-correct" onclick="decide('correct')">✓ Correct</button>
    <button id="btn-wrong" onclick="decide('wrong')">✗ Wrong</button>
    <button id="btn-skip" onclick="decide('skip')">– Skip</button>
  </div>
  <div id="notes-section">
    <label id="note-label">Note (optional)</label>
    <textarea id="note-input" placeholder="What's wrong? What should it be?"></textarea>
    <span id="note-saved">saved</span>
  </div>
  <div class="nav">
    <button onclick="go(-1)">← Prev</button>
    <button onclick="go(1)">Next →</button>
  </div>
</div>

<div id="sidebar">
  <h3>Entries</h3>
  <div id="sb-list"></div>
  <button id="export-btn" onclick="exportData()">Export JSON</button>
</div>

<script>
const ENTRIES = {entries_json};
const STORAGE_KEY = 'ukraine_s14_decisions';
const NOTES_KEY   = 'ukraine_s14_notes';

let decisions = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}');
let userNotes  = JSON.parse(localStorage.getItem(NOTES_KEY)   || '{{}}');
let current    = 0;
let noteTimer  = null;

function saveDecision(idx, d) {{
  decisions[idx] = d;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(decisions));
}}
function saveNote(idx) {{
  const txt = document.getElementById('note-input').value;
  userNotes[idx] = txt;
  localStorage.setItem(NOTES_KEY, JSON.stringify(userNotes));
  const s = document.getElementById('note-saved');
  s.style.display = 'inline';
  setTimeout(() => s.style.display = 'none', 1200);
}}
function scheduleNoteSave(idx) {{
  clearTimeout(noteTimer);
  noteTimer = setTimeout(() => saveNote(idx), 600);
}}

const STATUS_COLORS = {{
  'migrated':'migrated','non_migrated':'non_migrated','deported':'deported',
  'internal_transfer':'internal_transfer','excluded_pre_soviet':'excluded_pre_soviet',
  'excluded_non_ukrainian':'excluded_non_ukrainian','excluded_bad_dates':'excluded_bad_dates'
}};

function render() {{
  const e = ENTRIES[current];
  const idx = e.idx;
  document.getElementById('pos-label').textContent = (current+1) + ' / ' + ENTRIES.length;
  document.getElementById('meta-line').textContent = 'idx=' + idx + ' | born ' + (e.birth_year||'?') + ' | died ' + (e.death_year||'?');
  document.getElementById('entry-name').textContent = e.name;
  const cls = STATUS_COLORS[e.migration_status] || '';
  document.getElementById('status-badge').innerHTML = '<span class="status-badge ' + cls + '">' + e.migration_status + '</span>';
  document.getElementById('entry-reasoning').textContent = e.reasoning || '(no reasoning)';
  document.getElementById('entry-bio').textContent = e.bio || '(no bio fetched)';
  const link = document.getElementById('esu-link');
  link.href = e.article_url || '#';
  link.style.display = e.article_url ? 'inline' : 'none';
  const noteEl = document.getElementById('note-input');
  noteEl.value = userNotes[idx] || '';
  const d = decisions[idx];
  const noteLabel = document.getElementById('note-label');
  noteLabel.className = (d === 'wrong') ? 'red' : '';
  noteLabel.textContent = (d === 'wrong') ? 'Note — describe the correct classification:' : 'Note (optional)';
  noteEl.oninput = () => scheduleNoteSave(idx);
  updateCounts();
  renderSidebar();
}}

function decide(d) {{
  const e = ENTRIES[current];
  saveDecision(e.idx, d);
  if (d === 'wrong') {{
    const noteLabel = document.getElementById('note-label');
    noteLabel.className = 'red';
    noteLabel.textContent = 'Note — describe the correct classification:';
    document.getElementById('note-input').focus();
  }} else {{
    if (current < ENTRIES.length - 1) {{
      setTimeout(() => {{ current++; render(); }}, 350);
    }}
  }}
  updateCounts();
  renderSidebar();
}}

function go(dir) {{
  const newIdx = current + dir;
  if (newIdx >= 0 && newIdx < ENTRIES.length) {{ current = newIdx; render(); }}
}}

function updateCounts() {{
  let correct=0, wrong=0, skip=0;
  for (const e of ENTRIES) {{
    const d = decisions[e.idx];
    if (d === 'correct') correct++;
    else if (d === 'wrong') wrong++;
    else if (d === 'skip') skip++;
  }}
  document.getElementById('n-correct').textContent = correct;
  document.getElementById('n-wrong').textContent = wrong;
  document.getElementById('n-skip').textContent = skip;
  document.getElementById('n-unseen').textContent = ENTRIES.length - correct - wrong - skip;
}}

function renderSidebar() {{
  const list = document.getElementById('sb-list');
  list.innerHTML = ENTRIES.map((e, i) => {{
    const d = decisions[e.idx] || 'unseen';
    const cls = 'sb-' + d + (i === current ? ' sb-current' : '');
    const note = userNotes[e.idx] ? ' 📝' : '';
    const label = d === 'correct' ? '✓' : d === 'wrong' ? '✗' : d === 'skip' ? '–' : '·';
    return '<div class="sb-item ' + cls + '" onclick="current=' + i + ';render()">' +
      '<span>' + label + ' ' + (e.name||'').substring(0,18) + '</span><span>' + e.migration_status.substring(0,6) + note + '</span></div>';
  }}).join('');
}}

function exportData() {{
  const out = ENTRIES.map(e => ({{
    idx: e.idx,
    name: e.name,
    migration_status: e.migration_status,
    article_url: e.article_url,
    decision: decisions[e.idx] || 'unseen',
    note: userNotes[e.idx] || '',
  }}));
  const blob = new Blob([JSON.stringify(out, null, 2)], {{type:'application/json'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'stage14_validation_results.json';
  a.click();
}}

render();
</script>
</body>
</html>"""

with open(OUT_HTML, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone → {OUT_HTML}")
print(f"Entries: {len(entries_data)} (migrated={sum(1 for e in entries_data if e['migration_status']=='migrated')}, "
      f"non_migrated={sum(1 for e in entries_data if e['migration_status']=='non_migrated')}, "
      f"deported={sum(1 for e in entries_data if e['migration_status']=='deported')}, "
      f"IT={sum(1 for e in entries_data if e['migration_status']=='internal_transfer')})")
