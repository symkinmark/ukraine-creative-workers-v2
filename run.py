"""
run.py — AKS Market Research Agent, local MVP.

Usage:
  python run.py                   # run for today
  python run.py --date 2026-03-15 # reprocess a specific date (skips dedup)

Pipeline:
  scanner → memory filter → scorer → researcher → copywriter → memory update
"""

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

# Ensure imports work from any working directory
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()


def check_env():
    """Fail fast with a clear message if API key is missing."""
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key or key == "your-key-here":
        print("\n  ERROR: ANTHROPIC_API_KEY is not set.")
        print("  Open .env and add your key: ANTHROPIC_API_KEY=sk-ant-...")
        print("  Get one at: https://console.anthropic.com/\n")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="AKS Market Research Agent")
    parser.add_argument(
        "--date",
        help="Override date for output directory (YYYY-MM-DD). Skips dedup when set.",
        default=None,
    )
    args = parser.parse_args()

    check_env()

    today = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    reprocessing = bool(args.date)

    print(f"\n{'='*60}")
    print(f"  AKS Market Research Agent")
    print(f"  Date: {today}{' (reprocessing)' if reprocessing else ''}")
    print(f"{'='*60}\n")

    # ── Step 0: Init memory ──────────────────────────────────────
    from core.memory import init_memory
    init_memory()

    # ── Step 1: Create output directory ─────────────────────────
    output_dir = Path(__file__).parent / "output" / today
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"  Output → {output_dir}\n")

    # ── Step 2: Scan all sources ─────────────────────────────────
    print("STEP 1/4 — Scanning sources")
    print("-" * 40)
    from agents.scanner import run as scanner_run
    raw_items = scanner_run()

    if not raw_items:
        print("\n  No items fetched. Check your internet connection or source URLs.")
        sys.exit(0)

    # ── Step 3: Filter seen items ────────────────────────────────
    print("\nSTEP 2/4 — Deduplication")
    print("-" * 40)

    if reprocessing:
        print(f"  Reprocessing mode — skipping dedup, using all {len(raw_items)} items")
        new_items = raw_items
    else:
        from core.memory import is_seen
        new_items = [item for item in raw_items if not is_seen(item["url"])]
        skipped = len(raw_items) - len(new_items)
        print(f"  {len(raw_items)} fetched → {skipped} already seen → {len(new_items)} new items")

    if not new_items:
        print("\n  All items already processed. Run again tomorrow or use --date to reprocess.")
        from core.memory import append_agent_log
        append_agent_log({"fetched": len(raw_items), "new": 0, "high": 0, "medium": 0, "low": 0, "cost_est": 0})
        sys.exit(0)

    # ── Step 4: Score items ──────────────────────────────────────
    print(f"\nSTEP 3/4 — Scoring {len(new_items)} items")
    print("-" * 40)
    from agents.scorer import run as scorer_run
    scored_items, scorer_cost = scorer_run(new_items)

    # Log all scored items to raises-log.md
    from core.memory import append_raises_log
    for item in scored_items:
        append_raises_log(item, item.get("score", {}))

    # Count tiers
    high_items = [i for i in scored_items if i["score"]["total"] == 5]
    medium_items = [i for i in scored_items if 3 <= i["score"]["total"] <= 4]
    low_items = [i for i in scored_items if i["score"]["total"] <= 2]

    # ── Step 5: Research brief ───────────────────────────────────
    print(f"\nSTEP 4/4 — Research + Outreach")
    print("-" * 40)
    from agents.researcher import run as researcher_run
    research_path, researcher_cost = researcher_run(scored_items, output_dir)

    # ── Step 6: Outreach drafts ──────────────────────────────────
    from agents.copywriter import run as copywriter_run
    drafts_path, copywriter_cost = copywriter_run(scored_items, output_dir)

    # ── Step 7: Update memory ────────────────────────────────────
    if not reprocessing:
        from core.memory import mark_seen_batch
        mark_seen_batch(scored_items)
        print(f"\n  [memory] Marked {len(scored_items)} items as seen")

    # ── Step 8: Log run stats ────────────────────────────────────
    total_cost = scorer_cost + researcher_cost + copywriter_cost
    from core.memory import append_agent_log
    append_agent_log({
        "fetched": len(raw_items),
        "new": len(new_items),
        "high": len(high_items),
        "medium": len(medium_items),
        "low": len(low_items),
        "cost_est": total_cost,
    })

    # ── Done ─────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  DONE")
    print(f"{'='*60}")
    print(f"  Items fetched:    {len(raw_items)}")
    print(f"  New items scored: {len(new_items)}")
    print(f"  HIGH (5/5):       {len(high_items)}")
    print(f"  MEDIUM (3-4/5):   {len(medium_items)}")
    print(f"  LOW (0-2/5):      {len(low_items)}")
    print(f"  Total API cost:   ${total_cost:.4f}")
    print(f"\n  Research brief:   {research_path}")
    print(f"  Outreach drafts:  {drafts_path}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
