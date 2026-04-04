"""
generate_phase5_review.py

Phase 5 — Human Accuracy Check
Berdnyk & Symkin, Ukrainian Creative Workers V2

Pulls a random sample from the analysable dataset, fetches the full ESU article
text for each entry, and generates a clean HTML review sheet served via a local
HTTP server (avoids browser file:// security restrictions).

Usage:
    python ukraine_v2/generate_phase5_review.py           # sample 63 entries
    python ukraine_v2/generate_phase5_review.py --n 100   # custom sample size
    python ukraine_v2/generate_phase5_review.py --no-serve  # just write HTML, don't serve

Output:
    ukraine_v2/phase5_review.html
    Served at: http://localhost:8765/phase5_review.html
"""

import csv
import random
import os
import time
import argparse
import threading
import webbrowser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

INPUT_CSV = os.path.join(os.path.dirname(__file__), "esu_creative_workers_v2_1.csv")
OUTPUT_HTML = os.path.join(os.path.dirname(__file__), "phase5b_review.html")
SERVE_DIR = os.path.dirname(__file__)
PORT = 8765
SEED = 99  # different seed from Phase 5 (42) — fresh independent sample

# All valid migration statuses — includes four-way system from V2.1
VALID_STATUSES = {"migrated", "non_migrated", "internal_transfer", "deported"}


# ── Data loading ──────────────────────────────────────────────────────────────

def load_analysable(path):
    """Return rows that have birth_year, death_year, and a real migration status."""
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            birth = row.get("birth_year", "").strip()
            death = row.get("death_year", "").strip()
            status = row.get("migration_status", "").strip().lower()
            if birth and birth.isdigit() and death and death.isdigit() and status in VALID_STATUSES:
                rows.append(row)
    return rows


# ── ESU article fetcher ───────────────────────────────────────────────────────

def fetch_full_text(url):
    """Fetch and return the main article body text from an ESU article page."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (research project; Ukrainian Creative Workers V2)"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for selector in [".article-body", ".entry-content", "article", ".content", "main"]:
            el = soup.select_one(selector)
            if el:
                text = el.get_text(separator=" ", strip=True)
                if len(text) > 100:
                    return text[:3000]
        paras = soup.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paras if len(p.get_text(strip=True)) > 30)
        return text[:3000] if text else "Could not fetch article text."
    except Exception as e:
        return f"Fetch failed: {e}"


# ── HTML builder ──────────────────────────────────────────────────────────────

BADGE_COLOURS = {
    "migrated":          ("badge-migrated",          "MIGRATED"),
    "non_migrated":      ("badge-non-migrated",       "NON-MIGRATED"),
    "internal_transfer": ("badge-internal-transfer",  "INTERNAL TRANSFER"),
    "deported":          ("badge-deported",           "DEPORTED"),
}

def migration_badge(status):
    cls, label = BADGE_COLOURS.get(status.lower(), ("badge-unknown", status.upper()))
    return f'<span class="badge {cls}">{label}</span>'


def build_cards(sample, full_texts):
    """Build HTML card markup for each sampled entry."""
    cards = []
    for i, row in enumerate(sample, start=1):
        name      = row.get("name", "—")
        birth     = row.get("birth_year", "—")
        death     = row.get("death_year", "—")
        age       = int(death) - int(birth) if birth.isdigit() and death.isdigit() else "—"
        profession = row.get("profession_raw", "—")
        status    = row.get("migration_status", "—")
        reasoning = row.get("migration_reasoning", "—")
        url       = row.get("article_url", "")
        bio       = full_texts.get(url, "—")

        # Escape angle brackets so raw ESU text doesn't break HTML
        bio_safe       = bio.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        reasoning_safe = reasoning.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        name_safe      = name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        cards.append(f"""
<div class="card" id="row-{i}">
  <div class="card-header">
    <span class="num">#{i}</span>
    <span class="name">{name_safe}</span>
    {migration_badge(status)}
    <span class="life">{birth} &ndash; {death} &nbsp;&middot;&nbsp; age {age}</span>
    <a class="esu-link" href="{url}" target="_blank">Open ESU &nearr;</a>
  </div>
  <div class="card-body">
    <div class="field"><label>Profession</label><span>{profession}</span></div>
    <div class="field"><label>AI reasoning</label><span class="reasoning">{reasoning_safe}</span></div>
    <div class="field full"><label>Full ESU article text</label><pre class="bio-text">{bio_safe}</pre></div>
  </div>
  <div class="verdict">
    <strong>Your verdict:</strong>
    <label><input type="radio" name="v{i}" value="correct"> &#10003; Correct</label>
    <label><input type="radio" name="v{i}" value="dates_wrong"> &#10007; Dates wrong</label>
    <label><input type="radio" name="v{i}" value="migration_wrong"> &#10007; Migration status wrong</label>
    <label><input type="radio" name="v{i}" value="not_ukrainian"> &#10007; Not Ukrainian / wrong person</label>
    <label><input type="radio" name="v{i}" value="other"> &#10007; Other error</label>
    <textarea name="note{i}" placeholder="Optional note — e.g. correct status is deported, died 1943 not 1944"></textarea>
  </div>
</div>""")
    return "\n".join(cards)


# JS is built as a plain string (NOT inside a Python f-string) to avoid
# conflicts between Python f-string escaping and JavaScript syntax.
def build_js(sample_size, date_str):
    return """
<script>
function showSummary() {
    var total = """ + str(sample_size) + """;
    var results = {};
    var errors = [];
    var notes = [];

    for (var i = 1; i <= total; i++) {
        var card = document.getElementById("row-" + i);
        var name = card ? card.querySelector(".name").textContent.trim() : "?";
        var radios = document.querySelectorAll("input[name=v" + i + "]");
        var verdict = "not_reviewed";
        for (var j = 0; j < radios.length; j++) {
            if (radios[j].checked) { verdict = radios[j].value; break; }
        }
        results[verdict] = (results[verdict] || 0) + 1;
        if (verdict !== "correct" && verdict !== "not_reviewed") {
            errors.push("#" + i + " [" + verdict + "] " + name);
        }
        var ta = document.querySelector("textarea[name=note" + i + "]");
        var note = ta ? ta.value.trim() : "";
        if (note) notes.push("#" + i + " " + name + ": " + note);
    }

    var correct = results["correct"] || 0;
    var reviewed = total - (results["not_reviewed"] || 0);
    var errCount = reviewed - correct;
    var rate = reviewed > 0 ? ((errCount / reviewed) * 100).toFixed(1) : "0";

    var lines = [
        "PHASE 5 ACCURACY CHECK RESULTS",
        "================================",
        "Date reviewed: """ + date_str + """",
        "Sample size:   " + total,
        "Reviewed:      " + reviewed,
        "Not reviewed:  " + (results["not_reviewed"] || 0),
        "",
        "VERDICT BREAKDOWN",
        "-----------------",
        "Correct:              " + correct,
        "Dates wrong:          " + (results["dates_wrong"] || 0),
        "Migration wrong:      " + (results["migration_wrong"] || 0),
        "Not Ukrainian/wrong:  " + (results["not_ukrainian"] || 0),
        "Other:                " + (results["other"] || 0),
        "",
        "ERROR RATE: " + rate + "%"
    ];

    if (errors.length > 0) {
        lines.push("", "FLAGGED ENTRIES:", "----------------");
        for (var k = 0; k < errors.length; k++) { lines.push(errors[k]); }
    }
    if (notes.length > 0) {
        lines.push("", "NOTES:", "------");
        for (var m = 0; m < notes.length; m++) { lines.push(notes[m]); }
    }

    var out = lines.join("\\n");
    var box = document.getElementById("summary-output");
    box.value = out;
    box.style.display = "block";
    box.select();
    box.scrollIntoView({ behavior: "smooth" });
}
</script>
"""


def build_html(sample, full_texts):
    date_str = datetime.now().strftime("%Y-%m-%d")
    cards_html = build_cards(sample, full_texts)
    js = build_js(len(sample), date_str)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Phase 5 &mdash; Human Accuracy Check</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: #f4f4f4; color: #222; padding: 24px; max-width: 960px; margin: 0 auto; }}
h1 {{ font-size: 1.4rem; margin-bottom: 4px; }}
.subtitle {{ color: #666; font-size: 0.9rem; margin-bottom: 16px; }}

.card {{ background: #fff; border-radius: 8px; margin-bottom: 16px;
         box-shadow: 0 1px 4px rgba(0,0,0,0.1); overflow: hidden; }}
.card-header {{ display: flex; align-items: center; gap: 12px; padding: 14px 16px;
                background: #fafafa; border-bottom: 1px solid #eee; flex-wrap: wrap; }}
.num {{ font-weight: 700; color: #999; font-size: 0.85rem; min-width: 28px; }}
.name {{ font-weight: 600; font-size: 1rem; flex: 1; }}
.life {{ color: #666; font-size: 0.85rem; }}
.esu-link {{ margin-left: auto; font-size: 0.85rem; color: #0066cc; text-decoration: none;
             font-weight: 500; white-space: nowrap; }}
.esu-link:hover {{ text-decoration: underline; }}

.badge {{ font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 12px; white-space: nowrap; }}
.badge-migrated          {{ background: #dff0d8; color: #2d6a1f; }}
.badge-non-migrated      {{ background: #f2dede; color: #8b1a1a; }}
.badge-internal-transfer {{ background: #fdf2cd; color: #7a5c00; }}
.badge-deported          {{ background: #e8d5f5; color: #5a0080; }}

.card-body {{ padding: 12px 16px; display: flex; flex-direction: column; gap: 8px; }}
.field {{ display: flex; gap: 8px; font-size: 0.88rem; }}
.field label {{ min-width: 160px; color: #888; font-weight: 500; flex-shrink: 0; }}
.field.full {{ flex-direction: column; gap: 4px; }}
.field.full label {{ min-width: unset; }}
.reasoning {{ color: #444; font-style: italic; }}
.bio-text {{ color: #333; line-height: 1.55; background: #f7f7f7; border-left: 3px solid #ddd;
             padding: 8px 12px; border-radius: 4px; font-size: 0.85rem;
             white-space: pre-wrap; word-wrap: break-word; font-family: inherit; }}

.verdict {{ padding: 12px 16px; background: #f9f9f9; border-top: 1px solid #eee;
            display: flex; flex-wrap: wrap; gap: 12px; align-items: flex-start; }}
.verdict strong {{ width: 100%; font-size: 0.85rem; color: #555; }}
.verdict label {{ font-size: 0.88rem; display: flex; align-items: center; gap: 5px; cursor: pointer; }}
.verdict textarea {{ width: 100%; margin-top: 4px; font-size: 0.85rem;
                     padding: 6px 8px; border: 1px solid #ddd; border-radius: 4px;
                     resize: vertical; min-height: 36px; font-family: inherit; }}

#summary-btn {{ display: block; margin: 24px auto; padding: 12px 32px;
                background: #0066cc; color: #fff; font-size: 1rem; font-weight: 600;
                border: none; border-radius: 6px; cursor: pointer; }}
#summary-btn:hover {{ background: #0055aa; }}
#summary-output {{ width: 100%; min-height: 260px; margin-top: 16px; padding: 16px;
                   font-family: monospace; font-size: 0.88rem; border: 1px solid #ccc;
                   border-radius: 8px; background: #fff; display: none; resize: vertical; }}
</style>
</head>
<body>

<h1>Phase 5 &mdash; Human Accuracy Check</h1>
<p class="subtitle">Ukrainian Creative Workers V2 &nbsp;&middot;&nbsp; Berdnyk &amp; Symkin
  &nbsp;&middot;&nbsp; {len(sample)} random entries &nbsp;&middot;&nbsp; Generated {date_str}</p>
<p class="subtitle">
  For each entry read the bio text, check: (1) right person? (2) dates correct?
  (3) migration status correct? Then pick a verdict. When done, click the button below.
</p>

{cards_html}

<button id="summary-btn" onclick="showSummary()">Generate Summary Report</button>
<textarea id="summary-output" readonly></textarea>

{js}

</body>
</html>"""


# ── Local server ──────────────────────────────────────────────────────────────

class QuietHandler(SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler with logging suppressed."""
    def log_message(self, format, *args):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVE_DIR, **kwargs)


def start_server():
    server = HTTPServer(("localhost", PORT), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Phase 5 review sheet generator")
    parser.add_argument("--n", type=int, default=63, help="Sample size (default 63 = 1%%)")
    parser.add_argument("--no-serve", action="store_true", help="Write HTML only, don't start server")
    args = parser.parse_args()

    print("Loading CSV...")
    all_rows = load_analysable(INPUT_CSV)
    print(f"  Analysable rows: {len(all_rows)}")

    random.seed(SEED)
    sample = random.sample(all_rows, min(args.n, len(all_rows)))
    print(f"  Sample size: {len(sample)}")

    print(f"\nFetching full article text for {len(sample)} entries (~1 min)...")
    full_texts = {}
    for j, row in enumerate(sample, start=1):
        url = row.get("article_url", "")
        if url:
            print(f"  [{j}/{len(sample)}] {row.get('name', '')} ...", end=" ", flush=True)
            full_texts[url] = fetch_full_text(url)
            print("done")
            time.sleep(0.5)
        else:
            full_texts[url] = "No URL available."

    html = build_html(sample, full_texts)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nHTML written to: {OUTPUT_HTML}")

    if args.no_serve:
        print("Open the file manually in your browser.")
        return

    print(f"\nStarting local server on port {PORT}...")
    start_server()
    url = f"http://localhost:{PORT}/phase5_review.html"
    print(f"  Open: {url}")
    time.sleep(0.5)
    webbrowser.open(url)
    print("\nServer running. Press Ctrl+C to stop.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
