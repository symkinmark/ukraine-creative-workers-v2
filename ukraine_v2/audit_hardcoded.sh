#!/bin/bash
# audit_hardcoded.sh — Quick grep for potentially hardcoded stats in analysis scripts
# Run after any dataset update to catch stale numbers before they reach the paper.
# Usage: bash ukraine_v2/audit_hardcoded.sh

echo "=== 'prior run' / 'hardcoded' / TODO / FIXME comments ==="
grep -rn "prior run\|hardcoded\|TODO\|FIXME\|HACK\|# fixed\|# from" ukraine_v2/*.py 2>/dev/null || echo "  (none found)"

echo ""
echo "=== Suspicious literal numbers inside string appends/prints ==="
grep -n 'lines\.append.*[0-9]\{4,\}\|print.*[0-9]\{4,\}' ukraine_v2/stage5_cox.py ukraine_v2/stage7_figures.py ukraine_v2/stage8_timevarying.py 2>/dev/null || echo "  (none found)"

echo ""
echo "=== Hardcoded year/gap refs in print/write statements ==="
grep -n 'print.*+[0-9]\.[0-9][0-9] yrs\|write.*+[0-9]\.[0-9][0-9] yrs\|_full_gap\s*=\s*[0-9]' ukraine_v2/generate_analysis.py 2>/dev/null || echo "  (none found)"

echo ""
echo "=== penalizer values in Cox scripts ==="
grep -n 'penalizer' ukraine_v2/stage5_cox.py ukraine_v2/generate_analysis.py 2>/dev/null

echo ""
echo "Done. Review any flagged lines above before publishing."
