#!/usr/bin/env python3
"""
add_cliff_delta_ci.py
Adds Cliff's delta and 95% CI calculations to generate_analysis.py,
then runs it to capture the values needed for Script 3.
"""
import os, subprocess, sys

PROJECT = os.path.dirname(os.path.abspath(__file__))
GA_PATH = os.path.join(PROJECT, 'generate_analysis.py')

with open(GA_PATH, encoding='utf-8') as f:
    src = f.read()

# ── 1. Add cliffs_delta function after imports ────────────────────────────────
CLIFFS_FN = '''
def cliffs_delta(x, y):
    """Non-parametric effect size consistent with Mann-Whitney U.
    Returns P(X>Y) - P(Y>X). Range: -1 to +1. No distributional assumption."""
    x, y = list(x), list(y)
    n1, n2 = len(x), len(y)
    if n1 == 0 or n2 == 0:
        return float('nan')
    greater = sum(1 for xi in x for yj in y if xi > yj)
    less    = sum(1 for xi in x for yj in y if xi < yj)
    return (greater - less) / (n1 * n2)

'''

# Insert after the last import line
import_end = max(
    src.rfind('\nimport '),
    src.rfind('\nfrom '),
)
# Find the end of that import line
nl = src.find('\n', import_end + 1)
if nl == -1:
    nl = len(src)

if 'def cliffs_delta' not in src:
    src = src[:nl+1] + CLIFFS_FN + src[nl+1:]
    print('✓ cliffs_delta function added')
else:
    print('  cliffs_delta already exists — skipping')

# ── 2. Add CI + Cliff's delta output after Cohen's d print ────────────────────
# Find the Cohen's d output line and add new stats after it
COHEN_D_MARKER = "print(f\"Cohen's d"
CI_BLOCK = """
    # 95% CI for mean age at death
    from scipy import stats as _stats
    _ci_m  = _stats.t.interval(0.95, df=len(migrant_ages)-1,
                                loc=migrant_mean,
                                scale=_stats.sem(migrant_ages))
    _ci_nm = _stats.t.interval(0.95, df=len(nonmig_ages)-1,
                                loc=nonmig_mean,
                                scale=_stats.sem(nonmig_ages))
    _cd    = cliffs_delta(migrant_ages, nonmig_ages)
    print(f"95% CI migrants:     [{_ci_m[0]:.2f}, {_ci_m[1]:.2f}]")
    print(f"95% CI non-migrants: [{_ci_nm[0]:.2f}, {_ci_nm[1]:.2f}]")
    print(f"Cliff's delta (migrants vs non-migrants): {_cd:.4f}")
"""

# Find the Cohen's d print line and insert CI block after it
cd_idx = src.find(COHEN_D_MARKER)
if cd_idx != -1:
    nl2 = src.find('\n', cd_idx)
    if '95% CI migrants' not in src:
        src = src[:nl2+1] + CI_BLOCK + src[nl2+1:]
        print('✓ CI and Cliff\'s delta output added after Cohen\'s d')
    else:
        print('  CI block already exists — skipping')
else:
    print('  WARNING: Cohen\'s d print line not found — CI block NOT added')
    print('  Search for:', repr(COHEN_D_MARKER))

with open(GA_PATH, 'w', encoding='utf-8') as f:
    f.write(src)
print(f'✓ generate_analysis.py updated')

# ── 3. Run generate_analysis.py and capture output ───────────────────────────
print('\n' + '='*60)
print('Running generate_analysis.py...')
print('='*60)
result = subprocess.run(
    [sys.executable, GA_PATH],
    capture_output=True, text=True,
    cwd=PROJECT
)
print(result.stdout[-4000:] if len(result.stdout) > 4000 else result.stdout)
if result.returncode != 0:
    print('STDERR:', result.stderr[-2000:])
