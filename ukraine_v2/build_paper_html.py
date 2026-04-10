"""
build_paper_html.py
Converts PAPER_DRAFT.md → paper_preview.html + docs/index.html (GitHub Pages)
- Full markdown rendering (tables, bold, footnotes)
- Key figures (1, 9, 10, 14) rendered as interactive Plotly charts with hover tooltips
- Remaining figures embedded as base64 inline images
- Plotly loaded via CDN (requires internet); falls back to PNG if interactive HTML missing
"""

import re
import base64
import os

PROJECT = os.path.dirname(os.path.abspath(__file__))
MD_PATH  = os.path.join(PROJECT, 'PAPER_DRAFT.md')
OUT_PATH = os.path.join(PROJECT, 'paper_preview.html')
CHARTS   = os.path.join(PROJECT, 'charts')

# Map paper figure numbers to PNG filenames on disk.
# Paper restructured 2026-04-10: figures renumbered.
# Main body: Figures 1-15.  Appendix A: Figures A1-A18.
# File names on disk are UNCHANGED — only the paper reference numbers changed.
FIGURE_MAP = {
    # ── Main body figures (1–15) ──
    '1':   'fig01_primary_le_comparison.png',
    '2':   'fig02_kaplan_meier.png',
    '3':   'fig03_version_comparison.png',
    '4':   'fig16_consort_flowchart.png',           # was Fig 16
    '5':   'fig07b_deported_death_year.png',         # was Fig 7b
    '6':   'fig08_deported_deaths_by_year.png',      # was Fig 8
    '7':   'fig15_internal_transfer_null.png',       # was Fig 15
    '8':   'fig11_profession_grouped_bar.png',       # was Fig 11
    '9':   'fig10_birth_cohort_le.png',              # was Fig 10
    '10':  'fig23_regression_coef_plot.png',         # was Fig 23
    '11':  'fig24_cox_forest_plot.png',              # was Fig 24
    '12':  'fig28_deported_hr_by_age.png',           # was Fig 28
    '13':  'fig14_sensitivity_analysis.png',         # was Fig 14
    '14':  'fig30_sensitivity_gap.png',              # was Fig 30
    '15':  'fig19_ssr_population_context.png',       # was Fig 19
    # ── Appendix A figures (A1–A18) ──
    'A1':  'fig04_box_plots.png',                    # was Fig 4
    'A2':  'fig05_deported_age_histogram.png',       # was Fig 5
    'A3':  'fig06_violin_plots.png',                 # was Fig 6
    'A4':  'fig07_death_year_histogram.png',         # was Fig 7
    'A5':  'fig09_nonmigrant_deaths_by_period.png',  # was Fig 9
    'A6':  'fig12_geographic_migration_rates.png',   # was Fig 12
    'A7':  'fig17_gender_by_group.png',              # was Fig 17
    'A8':  'fig18_le_by_gender_group.png',           # was Fig 18
    'A9':  'fig21_soviet_republic_comparison.png',   # was Fig 21
    'A10': 'fig22_educated_urban_comparison.png',    # was Fig 22
    'A11': 'fig25_censoring_pattern.png',            # was Fig 25
    'A12': 'fig26_km_censored.png',                  # was Fig 26
    'A13': 'fig15b_all_groups_le_box.png',           # was Fig 15b
    'A14': 'fig13_birth_year_distribution.png',      # was Fig 13
    'A15': 'fig20_two_group_conservative.png',       # was Fig 20
    'A16': 'fig19b_simplified_death_rate.png',       # was Fig 19b
    'A17': 'fig27_sensitivity_summary.png',          # was Fig 27
    'A18': 'fig28b_schoenfeld_smooth.png',           # was Fig 28b
    # fig29/29b/29c retracted — wave disaggregation classifier unreliable (§8.7)
}

def img_b64(filename):
    path = os.path.join(CHARTS, filename)
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('ascii')
    return f'data:image/png;base64,{data}'

def load_interactive(fig_num):
    """Load the Plotly HTML div for a figure, using FIGURE_MAP to find the file.
    Strips embedded <script> tags that load Plotly CDN — the main page loads it once."""
    if fig_num not in FIGURE_MAP:
        return None
    # Derive interactive filename from PNG filename:
    # fig01_primary_le_comparison.png → fig01_interactive.html
    # fig07b_deported_death_year.png  → fig07b_interactive.html
    png_name = FIGURE_MAP[fig_num]
    prefix = png_name.split('_')[0]  # 'fig01', 'fig07b', 'fig15b', etc.
    path = os.path.join(CHARTS, f'{prefix}_interactive.html')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            content = f.read()
        # Strip Plotly CDN script tags — the main page loads Plotly once via its own CDN
        content = re.sub(r'<script[^>]*src="https://cdn\.plot\.ly/[^"]*"[^>]*></script>\s*', '', content)
        content = re.sub(r'<script>window\.PlotlyConfig\s*=\s*\{[^}]*\};</script>\s*', '', content)
        return content
    return None

# Pre-encode all images (skip missing files gracefully)
IMAGES = {k: img_b64(fn) for k, fn in FIGURE_MAP.items() if img_b64(fn)}

# Load interactive HTML for ALL figures that have interactive versions
INTERACTIVE = {k: load_interactive(k) for k in FIGURE_MAP}
INTERACTIVE = {k: v for k, v in INTERACTIVE.items() if v is not None}

# ---------------------------------------------------------------------------
# Minimal markdown → HTML converter (covers everything in this paper)
# ---------------------------------------------------------------------------

def md_inline(text):
    """Convert inline markdown: bold, italic, code, links."""
    # Bold+italic ***
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold **
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic *
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code `…`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Footnote refs [^N]
    text = re.sub(r'\[\^(\w+)\](?!:)', r'<sup><a href="#fn\1" id="fnref\1">[\1]</a></sup>', text)
    return text

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def parse_table(lines):
    """Convert a markdown table block into HTML."""
    rows = [l.strip() for l in lines if l.strip()]
    html = ['<table>']
    for i, row in enumerate(rows):
        if re.match(r'^\|[-| :]+\|$', row):
            continue  # separator line
        cells = [c.strip() for c in row.strip('|').split('|')]
        tag = 'th' if i == 0 else 'td'
        html.append('  <tr>' + ''.join(f'<{tag}>{md_inline(c)}</{tag}>' for c in cells) + '</tr>')
    html.append('</table>')
    return '\n'.join(html)

def md_to_html(md_text):
    lines = md_text.split('\n')
    html_parts = []
    i = 0
    footnote_defs = {}  # id -> content

    # First pass: collect footnote definitions
    fn_pattern = re.compile(r'^\[\^(\w+)\]:\s*(.*)')
    body_lines = []
    for line in lines:
        m = fn_pattern.match(line)
        if m:
            footnote_defs[m.group(1)] = m.group(2)
        else:
            body_lines.append(line)

    lines = body_lines
    _embedded_figs = set()  # Track which figures have been embedded to avoid duplicates
    i = 0
    while i < len(lines):
        line = lines[i]

        # Blank line
        if not line.strip():
            i += 1
            continue

        # Horizontal rule ---
        if re.match(r'^-{3,}$', line.strip()):
            html_parts.append('<hr>')
            i += 1
            continue

        # Headings
        m = re.match(r'^(#{1,4})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text  = md_inline(m.group(2))
            html_parts.append(f'<h{level}>{text}</h{level}>')
            i += 1
            continue

        # Blockquote >
        if line.startswith('>'):
            content = line.lstrip('> ').strip()
            html_parts.append(f'<blockquote><p>{md_inline(content)}</p></blockquote>')
            i += 1
            continue

        # Table: line starts with |
        if line.strip().startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            html_parts.append(parse_table(table_lines))
            continue

        # Unordered list
        if re.match(r'^[-*]\s', line):
            html_parts.append('<ul>')
            while i < len(lines) and re.match(r'^[-*]\s', lines[i]):
                item = lines[i][2:].strip()
                html_parts.append(f'  <li>{md_inline(item)}</li>')
                i += 1
            html_parts.append('</ul>')
            continue

        # Paragraph (including bold-leadin figure captions)
        # Collect consecutive non-empty, non-special lines
        para_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith('#') \
              and not lines[i].startswith('>') and not lines[i].strip().startswith('|') \
              and not re.match(r'^-{3,}$', lines[i].strip()) \
              and not re.match(r'^[-*]\s', lines[i]):
            para_lines.append(lines[i])
            i += 1
        para = ' '.join(para_lines)
        html_parts.append(f'<p>{md_inline(para)}</p>')

        # Check if this paragraph is a figure caption → inject static PNG (once per figure)
        # Static PNGs are used for all figures — always renders, no CDN dependency.
        # Interactive Plotly versions remain available as standalone HTML files in charts/.
        fig_m = re.search(r'\*\*Figure\s+(A?\d+[ab]?)', para)
        if fig_m:
            fig_num = fig_m.group(1)
            if fig_num in _embedded_figs:
                pass  # Already embedded — skip duplicate
            elif fig_num in IMAGES:
                html_parts.append(
                    f'<figure>'
                    f'<img src="{IMAGES[fig_num]}" alt="Figure {fig_num}">'
                    f'</figure>'
                )
                _embedded_figs.add(fig_num)

    # Footnotes section
    if footnote_defs:
        html_parts.append('<hr>')
        html_parts.append('<section class="footnotes"><h2>Notes</h2><ol>')
        for fid, content in footnote_defs.items():
            html_parts.append(
                f'<li id="fn{fid}">{md_inline(content)}'
                f' <a href="#fnref{fid}">↩</a></li>'
            )
        html_parts.append('</ol></section>')

    return '\n'.join(html_parts)

# ---------------------------------------------------------------------------
# Build HTML
# ---------------------------------------------------------------------------

with open(MD_PATH, encoding='utf-8') as f:
    md = f.read()

body = md_to_html(md)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Life Expectancy of Ukrainian Creative Workers — V2.6</title>
<!-- Interactive Plotly versions available as standalone files in charts/ -->
<style>
  body {{
    font-family: 'Georgia', serif;
    font-size: 16px;
    line-height: 1.7;
    max-width: 860px;
    margin: 48px auto;
    padding: 0 24px;
    color: #1a1a1a;
    background: #fff;
  }}
  h1 {{ font-size: 1.9em; margin-top: 1.2em; border-bottom: 2px solid #333; padding-bottom: 0.3em; }}
  h2 {{ font-size: 1.4em; margin-top: 2em; border-bottom: 1px solid #ccc; padding-bottom: 0.2em; }}
  h3 {{ font-size: 1.15em; margin-top: 1.6em; color: #333; }}
  h4 {{ font-size: 1em; margin-top: 1.2em; color: #555; }}
  blockquote {{
    border-left: 4px solid #e0c040;
    margin: 1em 0;
    padding: 0.5em 1.2em;
    background: #fffbf0;
    font-style: italic;
    color: #555;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 1.2em 0;
    font-size: 0.92em;
  }}
  th, td {{
    border: 1px solid #ccc;
    padding: 7px 12px;
    text-align: left;
  }}
  th {{ background: #f0f0f0; font-weight: bold; }}
  tr:nth-child(even) {{ background: #f9f9f9; }}
  code {{
    background: #f4f4f4;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 0.88em;
    font-family: 'Menlo', 'Courier New', monospace;
  }}
  figure {{
    margin: 1.8em 0;
    text-align: center;
    background: #fafafa;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 16px;
  }}
  figure img {{
    max-width: 100%;
    height: auto;
    border-radius: 4px;
  }}
  figure.interactive-fig {{
    padding: 8px;
    text-align: left;
  }}
  figure.interactive-fig .plotly-graph-div {{
    width: 100% !important;
  }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 2em 0; }}
  sup a {{ color: #a00; text-decoration: none; font-size: 0.8em; }}
  sup a:hover {{ text-decoration: underline; }}
  .footnotes {{ font-size: 0.88em; color: #444; }}
  .footnotes h2 {{ font-size: 1em; color: #555; }}
  .footnotes ol {{ padding-left: 1.5em; }}
  .footnotes li {{ margin-bottom: 0.5em; }}
  ul {{ margin: 0.8em 0; padding-left: 2em; }}
  li {{ margin-bottom: 0.3em; }}
  strong {{ font-weight: bold; }}
  @media print {{
    body {{ max-width: 100%; margin: 0; padding: 20px; }}
    figure {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>
{body}
</body>
</html>
"""

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(HTML)

# Also write to docs/index.html for GitHub Pages
DOCS_PATH = os.path.join(os.path.dirname(PROJECT), 'docs', 'index.html')
os.makedirs(os.path.dirname(DOCS_PATH), exist_ok=True)
with open(DOCS_PATH, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"Done → {OUT_PATH}")
print(f"Done → {DOCS_PATH}")
print(f"Figures embedded: {len(IMAGES)} static PNGs + {len(INTERACTIVE)} interactive Plotly")
