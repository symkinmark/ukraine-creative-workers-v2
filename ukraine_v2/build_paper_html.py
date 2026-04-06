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

# Figures that have interactive Plotly versions (figXX_interactive.html)
INTERACTIVE_FIGS = {
    '1', '2', '3', '4', '5', '6', '7', '7b', '8', '9', '10',
    '11', '12', '13', '14', '15', '15b', '17', '18', '19', '19b',
    '20', '21', '22', '23', '24', '25', '26',
}

# Map each Figure N to its PNG filename (file number = paper figure number)
FIGURE_MAP = {
    '1':   'fig01_primary_le_comparison.png',
    '2':   'fig02_kaplan_meier.png',
    '3':   'fig03_version_comparison.png',
    '4':   'fig04_box_plots.png',
    '5':   'fig05_deported_age_histogram.png',
    '6':   'fig06_violin_plots.png',
    '7':   'fig07_death_year_histogram.png',
    '7b':  'fig07b_deported_death_year.png',
    '8':   'fig08_deported_deaths_by_year.png',
    '9':   'fig09_nonmigrant_deaths_by_period.png',
    '10':  'fig10_birth_cohort_le.png',
    '11':  'fig11_profession_grouped_bar.png',
    '12':  'fig12_geographic_migration_rates.png',
    '13':  'fig13_birth_year_distribution.png',
    '14':  'fig14_sensitivity_analysis.png',
    '15':  'fig15_internal_transfer_null.png',
    '15b': 'fig15b_all_groups_le_box.png',
    '16':  'fig16_consort_flowchart.png',
    '17':  'fig17_gender_by_group.png',
    '18':  'fig18_le_by_gender_group.png',
    '19':  'fig19_ssr_population_context.png',
    '19b': 'fig19b_simplified_death_rate.png',
    '20':  'fig20_two_group_conservative.png',
    '21':  'fig21_soviet_republic_comparison.png',
    '22':  'fig22_educated_urban_comparison.png',
    '23':  'fig23_regression_coef_plot.png',
    '24':  'fig24_cox_forest_plot.png',
    '25':  'fig25_censoring_pattern.png',
    '26':  'fig26_km_censored.png',
}

def img_b64(filename):
    path = os.path.join(CHARTS, filename)
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('ascii')
    return f'data:image/png;base64,{data}'

def load_interactive(fig_num):
    """Load the Plotly HTML div for a figure number, or None if not available."""
    # Handle suffixed numbers like '15b', '19b' — keep suffix, zero-pad numeric prefix
    import re as _re
    m = _re.match(r'^(\d+)([a-z]*)$', str(fig_num))
    if m:
        num_part = f'{int(m.group(1)):02d}'
        suffix   = m.group(2)
    else:
        num_part = str(fig_num)
        suffix   = ''
    path = os.path.join(CHARTS, f'fig{num_part}{suffix}_interactive.html')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return f.read()
    return None

# Pre-encode all images (skip missing files gracefully)
IMAGES = {k: img_b64(fn) for k, fn in FIGURE_MAP.items() if img_b64(fn)}

# Load interactive HTML for key figures
INTERACTIVE = {k: load_interactive(k) for k in INTERACTIVE_FIGS}
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

        # Check if this paragraph is a figure caption → inject image
        fig_m = re.search(r'\*\*Figure\s+(\d+[ab]?)', para)
        if fig_m:
            fig_num = fig_m.group(1)
            if fig_num in INTERACTIVE:
                # Interactive Plotly chart — embed div directly
                html_parts.append(
                    f'<figure class="interactive-fig">'
                    f'{INTERACTIVE[fig_num]}'
                    f'</figure>'
                )
            elif fig_num in IMAGES:
                html_parts.append(
                    f'<figure>'
                    f'<img src="{IMAGES[fig_num]}" alt="Figure {fig_num}">'
                    f'</figure>'
                )

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
<title>Life Expectancy of Ukrainian Creative Workers — V2.3</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js" charset="utf-8"></script>
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
