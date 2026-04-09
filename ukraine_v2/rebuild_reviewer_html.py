"""
rebuild_reviewer_html.py
Rebuilds validation_v2_6_reviewer.html from the existing CSV (no re-fetching bios).
Run this whenever the reviewer template changes.
"""

import csv, os, json

PROJECT  = os.path.dirname(os.path.abspath(__file__))
VAL_DIR  = os.path.join(PROJECT, 'validation')
CSV_IN   = os.path.join(VAL_DIR, 'validation_v2_6_sample.csv')
HTML_OUT = os.path.join(VAL_DIR, 'validation_v2_6_reviewer.html')

with open(CSV_IN, encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

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
.stat-correct {{ color: #4caf50; }}
.stat-wrong   {{ color: #f44336; }}
.stat-skip    {{ color: #ff9800; }}
.stat-unseen  {{ color: #8892a4; }}
#search-box {{ margin: 8px 14px; padding: 5px 8px; background: #2a3248;
               border: 1px solid #3a4460; border-radius: 4px; color: #c8cdd8; font-size: 12px;
               width: calc(100% - 28px); }}
#filter-bar {{ display: flex; gap: 4px; padding: 0 14px 8px; flex-wrap: wrap; }}
.filter-btn {{ font-size: 10px; padding: 2px 7px; border: 1px solid #3a4460; border-radius: 12px;
               background: transparent; color: #8892a4; cursor: pointer; }}
.filter-btn.active {{ background: #3a5bcc; border-color: #3a5bcc; color: #fff; }}
#entry-list {{ flex: 1; overflow-y: auto; }}
.entry-item {{ padding: 8px 14px; border-bottom: 1px solid #252c3f; cursor: pointer;
               transition: background 0.1s; border-left: 3px solid transparent; }}
.entry-item:hover {{ background: #252c3f; }}
.entry-item.active {{ background: #2a3a6a; }}
.entry-item.decided-correct {{ border-left-color: #4caf50; }}
.entry-item.decided-wrong   {{ border-left-color: #f44336; }}
.entry-item.decided-skip    {{ border-left-color: #ff9800; }}
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
#decision-row {{ display: flex; gap: 10px; margin-top: 6px; flex-wrap: wrap; align-items: flex-start; }}
.dec-btn {{ flex: 1; min-width: 120px; padding: 12px; border-radius: 6px; border: 2px solid transparent;
             font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.15s; }}
.dec-btn.correct {{ background: #e8f5e9; color: #2e7d32; border-color: #a5d6a7; }}
.dec-btn.correct:hover, .dec-btn.correct.active {{ background: #4caf50; color: #fff; border-color: #4caf50; }}
.dec-btn.wrong {{ background: #ffebee; color: #c62828; border-color: #ef9a9a; }}
.dec-btn.wrong:hover, .dec-btn.wrong.active {{ background: #f44336; color: #fff; border-color: #f44336; }}
.dec-btn.skip {{ background: #fff8e1; color: #e65100; border-color: #ffe082; }}
.dec-btn.skip:hover, .dec-btn.skip.active {{ background: #ff9800; color: #fff; border-color: #ff9800; }}

/* ── Notes box ── */
#notes-section {{ margin-top: 16px; }}
#notes-label {{ font-size: 10px; font-weight: 700; text-transform: uppercase;
                letter-spacing: 0.05em; color: #999; margin-bottom: 5px; }}
#notes-label.is-wrong {{ color: #c62828; }}
#reviewer-notes {{ width: 100%; padding: 10px 12px; font-size: 13px; font-family: inherit;
                   border: 2px solid #e0e4ed; border-radius: 6px; resize: vertical;
                   min-height: 70px; line-height: 1.5; color: #333; background: #fafbfd;
                   transition: border-color 0.15s; }}
#reviewer-notes:focus {{ outline: none; border-color: #3a5bcc; background: #fff; }}
#reviewer-notes.is-wrong {{ border-color: #f44336; background: #fff8f8; }}
#reviewer-notes.is-wrong:focus {{ border-color: #c62828; }}
#notes-saved {{ font-size: 11px; color: #4caf50; margin-top: 4px; opacity: 0;
                transition: opacity 0.3s; height: 16px; }}

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
        <button class="nav-btn" onclick="openExport()">Export ↗</button>
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
    <div id="export-summary" style="font-size:12px;color:#555;margin-bottom:14px;line-height:1.6"></div>
    <button class="export-btn" onclick="downloadJSON()">⬇ Download JSON</button>
    <button class="export-btn" onclick="downloadCSV()">⬇ Download CSV</button>
    <button class="export-btn" onclick="copyToClipboard()">📋 Copy JSON to clipboard</button>
    <div id="export-count" style="font-size:12px;color:#888;margin:8px 0"></div>
    <button class="export-close" onclick="document.getElementById('export-overlay').style.display='none'">Close</button>
  </div>
</div>

<script>
const ENTRIES = {entries_json};
const STORAGE_KEY       = 'ukraine_v26_validation_decisions';
const NOTES_STORAGE_KEY = 'ukraine_v26_validation_notes';

// Load from localStorage
let decisions = {{}};
let userNotes = {{}};
try {{ decisions = JSON.parse(localStorage.getItem(STORAGE_KEY)       || '{{}}'); }} catch(e) {{}}
try {{ userNotes = JSON.parse(localStorage.getItem(NOTES_STORAGE_KEY) || '{{}}'); }} catch(e) {{}}

let currentIdx  = null;
let activeFilter = 'all';
let searchQuery  = '';
let noteTimer    = null;

// ── Render sidebar list ──
function renderList() {{
  const list = document.getElementById('entry-list');
  const q = searchQuery.toLowerCase();
  list.innerHTML = '';
  ENTRIES.forEach(e => {{
    const dec = decisions[e.idx];
    if (activeFilter === 'unseen'  && dec)               return;
    if (activeFilter === 'correct' && dec !== 'correct') return;
    if (activeFilter === 'wrong'   && dec !== 'wrong')   return;
    if (activeFilter === 'INCLUDE' && e.group !== 'INCLUDE') return;
    if (activeFilter === 'EXCLUDE' && e.group !== 'EXCLUDE') return;
    if (q && !e.name.toLowerCase().includes(q)) return;

    const hasNote = !!userNotes[e.idx];
    const div = document.createElement('div');
    div.className = 'entry-item' +
      (dec === 'correct' ? ' decided-correct' : dec === 'wrong' ? ' decided-wrong' : dec === 'skip' ? ' decided-skip' : '') +
      (currentIdx === e.idx ? ' active' : '');
    div.dataset.idx = e.idx;
    div.innerHTML = `<div class="entry-name">${{e.idx + 1}}. ${{e.name}}${{hasNote ? ' 📝' : ''}}</div>
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

  const dec      = decisions[idx] || '';
  const noteText = userNotes[idx] || '';
  const isWrong  = dec === 'wrong';

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
    </div>
    <div id="notes-section">
      <div id="notes-label" class="${{isWrong ? 'is-wrong' : ''}}">
        ${{isWrong ? '✗ What is wrong? (required for wrong decisions)' : 'Notes (optional)'}}
      </div>
      <textarea id="reviewer-notes"
        class="${{isWrong ? 'is-wrong' : ''}}"
        placeholder="e.g. should be migrated — emigrated to Paris 1922; or: death year wrong, correct is 1991"
        oninput="scheduleNoteSave(${{idx}})"
      >${{noteText}}</textarea>
      <div id="notes-saved"></div>
    </div>`;

  // Focus notes area automatically when wrong
  if (isWrong) {{
    setTimeout(() => {{
      const ta = document.getElementById('reviewer-notes');
      if (ta) ta.focus();
    }}, 50);
  }}

  renderList();
  updateStats();
  // Scroll to top of card
  document.getElementById('content-area').scrollTop = 0;
}}

// ── Note saving (debounced) ──
function scheduleNoteSave(idx) {{
  clearTimeout(noteTimer);
  noteTimer = setTimeout(() => saveNote(idx), 600);
}}

function saveNote(idx) {{
  const ta = document.getElementById('reviewer-notes');
  if (!ta) return;
  const text = ta.value.trim();
  if (text) {{
    userNotes[idx] = text;
  }} else {{
    delete userNotes[idx];
  }}
  localStorage.setItem(NOTES_STORAGE_KEY, JSON.stringify(userNotes));
  const saved = document.getElementById('notes-saved');
  if (saved) {{
    saved.textContent = 'saved';
    saved.style.opacity = '1';
    setTimeout(() => {{ if (saved) saved.style.opacity = '0'; }}, 1500);
  }}
  renderList();  // update 📝 indicator in sidebar
}}

// ── Decision ──
function decide(idx, verdict) {{
  decisions[idx] = verdict;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(decisions));
  updateStats();

  // Re-render card to update button states + notes styling
  showEntry(idx);

  // Auto-advance after short delay — but NOT for wrong (user needs to write a note)
  if (verdict !== 'wrong') {{
    setTimeout(() => {{
      const visible = [...document.querySelectorAll('.entry-item')].map(el => parseInt(el.dataset.idx));
      const pos = visible.indexOf(idx);
      if (pos >= 0 && pos < visible.length - 1) showEntry(visible[pos + 1]);
    }}, 350);
  }}
}}

// ── Navigate ──
function navigate(dir) {{
  // Save any pending note before navigating
  if (currentIdx !== null) saveNote(currentIdx);
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

// ── Export ──
function openExport() {{
  if (currentIdx !== null) saveNote(currentIdx);
  const decided   = Object.values(decisions);
  const correct   = decided.filter(d => d==='correct').length;
  const wrong     = decided.filter(d => d==='wrong').length;
  const skip      = decided.filter(d => d==='skip').length;
  const withNotes = Object.keys(userNotes).length;
  document.getElementById('export-summary').innerHTML =
    `<b>${{correct+wrong+skip}}/200</b> decisions recorded &nbsp;·&nbsp; ` +
    `✓ ${{correct}} correct &nbsp; ✗ ${{wrong}} wrong &nbsp; ~ ${{skip}} skip<br>` +
    `📝 ${{withNotes}} entries have notes`;
  document.getElementById('export-overlay').style.display = 'block';
}}

function getExportData() {{
  return ENTRIES.map(e => ({{
    idx:              e.idx,
    name:             e.name,
    birth_year:       e.by,
    death_year:       e.dy,
    migration_status: e.status,
    sample_group:     e.group,
    decision:         decisions[e.idx] || 'unseen',
    note:             userNotes[e.idx] || '',
    url:              e.url,
  }}));
}}

function downloadJSON() {{
  const blob = new Blob([JSON.stringify(getExportData(), null, 2)], {{type:'application/json'}});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
  a.download = 'validation_v2_6_results.json'; a.click();
  document.getElementById('export-count').textContent = 'Downloaded.';
}}

function downloadCSV() {{
  const data   = getExportData();
  const header = ['idx','name','birth_year','death_year','migration_status','sample_group','decision','note','url'];
  const lines  = [header.join(',')];
  data.forEach(r => lines.push(header.map(k => JSON.stringify(r[k]??'')).join(',')));
  const blob = new Blob([lines.join('\\n')], {{type:'text/csv'}});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
  a.download = 'validation_v2_6_results.csv'; a.click();
}}

function copyToClipboard() {{
  navigator.clipboard.writeText(JSON.stringify(getExportData(), null, 2))
    .then(() => {{ document.getElementById('export-count').textContent = 'Copied to clipboard!'; }});
}}

// ── Init ──
renderList();
updateStats();
if (ENTRIES.length > 0) showEntry(ENTRIES[0].idx);
</script>
</body>
</html>"""

with open(HTML_OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"Reviewer rebuilt → {HTML_OUT}")
print(f"Loaded {len(rows)} entries from CSV.")
