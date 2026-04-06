#!/usr/bin/env python3
"""
highlight_fix.py — rebuild paper HTML and jump to a fixed phrase in the browser.
Usage: python3 ukraine_v2/highlight_fix.py "exact phrase that was changed"
Run this after every edit to PAPER_DRAFT.md.
"""
import sys
import os
import subprocess

PROJECT = os.path.dirname(os.path.abspath(__file__))
HTML    = os.path.join(PROJECT, "paper_preview.html")
BUILD   = os.path.join(PROJECT, "build_paper_html.py")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 highlight_fix.py \"phrase to highlight\"")
        sys.exit(1)

    phrase = sys.argv[1]

    # Rebuild HTML
    subprocess.run(["python3", BUILD], check=True)

    with open(HTML, encoding="utf-8") as f:
        html = f.read()

    if phrase not in html:
        print(f"WARNING: phrase not found in HTML — check exact wording:\n  {phrase!r}")
        subprocess.run(["open", HTML])
        return

    highlighted = (
        f'<mark id="fix-highlight" style="background:#ffe066;'
        f'border-radius:3px;padding:1px 3px;">{phrase}</mark>'
    )
    html = html.replace(phrase, highlighted, 1)

    jump = (
        '<script>\nwindow.addEventListener("load",function(){\n'
        '  var el=document.getElementById("fix-highlight");\n'
        '  if(el){el.scrollIntoView({behavior:"smooth",block:"center"});}\n'
        '});\n</script>\n'
    )
    html = html.replace("</body>", jump + "</body>")

    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Highlight injected → opening browser")
    subprocess.run(["open", HTML])

if __name__ == "__main__":
    main()
