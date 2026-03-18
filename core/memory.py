"""
memory.py — manages seen.json dedup, raises-log.md, and agent-log.md.

All memory files live in memory/. This module creates them if missing.
"""

import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

MEMORY_DIR = Path(__file__).parent.parent / "memory"
SEEN_FILE = MEMORY_DIR / "seen.json"
RAISES_LOG = MEMORY_DIR / "raises-log.md"
AGENT_LOG = MEMORY_DIR / "agent-log.md"


def init_memory():
    """Create memory directory and files if they don't exist."""
    MEMORY_DIR.mkdir(exist_ok=True)

    if not SEEN_FILE.exists():
        SEEN_FILE.write_text("{}\n")
        print("  [memory] Created seen.json")

    if not RAISES_LOG.exists():
        RAISES_LOG.write_text("# Raises Log\n\nAppend-only log of all scored items.\n\n")
        print("  [memory] Created raises-log.md")

    if not AGENT_LOG.exists():
        AGENT_LOG.write_text("# Agent Run Log\n\n")
        print("  [memory] Created agent-log.md")


def _load_seen() -> dict:
    try:
        return json.loads(SEEN_FILE.read_text())
    except Exception:
        return {}


def _save_seen(data: dict):
    SEEN_FILE.write_text(json.dumps(data, indent=2) + "\n")


def is_seen(item_url: str, window_days: int = 90) -> bool:
    """
    Returns True if this URL was already processed within window_days.
    Uses URL as the dedup key (more reliable than company name).
    """
    seen = _load_seen()
    if item_url not in seen:
        return False

    first_seen_str = seen[item_url].get("first_seen", "")
    if not first_seen_str:
        return True

    try:
        first_seen = datetime.fromisoformat(first_seen_str)
        cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
        # Make first_seen timezone-aware if it isn't
        if first_seen.tzinfo is None:
            first_seen = first_seen.replace(tzinfo=timezone.utc)
        return first_seen > cutoff
    except Exception:
        return True


def mark_seen(item_url: str, data: dict):
    """Record a URL as processed."""
    seen = _load_seen()
    seen[item_url] = {
        "first_seen": datetime.now(timezone.utc).isoformat(),
        "title": data.get("title", ""),
        "source": data.get("source_name", ""),
        "score": data.get("score", {}).get("total", 0),
    }
    _save_seen(seen)


def mark_seen_batch(items: list[dict]):
    """Mark multiple items as seen in one write."""
    seen = _load_seen()
    for item in items:
        url = item.get("url", "")
        if url:
            seen[url] = {
                "first_seen": datetime.now(timezone.utc).isoformat(),
                "title": item.get("title", ""),
                "source": item.get("source_name", ""),
                "score": item.get("score", {}).get("total", 0) if isinstance(item.get("score"), dict) else item.get("score", 0),
            }
    _save_seen(seen)


def append_raises_log(item: dict, score: dict):
    """Append one scored item to raises-log.md regardless of score."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total = score.get("total", 0)
    confidence = score.get("confidence", "unknown")
    flags = ", ".join(score.get("uncertainty_flags", [])) or "none"

    line = (
        f"## [{today}] {item.get('title', 'Untitled')} — Score {total}/5\n"
        f"- Source: {item.get('source_name', '')}\n"
        f"- URL: {item.get('url', '')}\n"
        f"- Date: {item.get('date', '')}\n"
        f"- Confidence: {confidence} | Flags: {flags}\n"
        f"- Breakdown: sector={score.get('sector',0)} stage={score.get('stage',0)} "
        f"geo={score.get('geography',0)} signal={score.get('signal_type',0)} "
        f"fresh={score.get('freshness',0)}\n\n"
    )

    with open(RAISES_LOG, "a") as f:
        f.write(line)


def append_agent_log(run_stats: dict):
    """Append one line per run to agent-log.md."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    stats = (
        f"**{now}** | "
        f"fetched={run_stats.get('fetched', 0)} | "
        f"new={run_stats.get('new', 0)} | "
        f"high={run_stats.get('high', 0)} | "
        f"medium={run_stats.get('medium', 0)} | "
        f"low={run_stats.get('low', 0)} | "
        f"cost_est=${run_stats.get('cost_est', 0):.4f}\n"
    )
    with open(AGENT_LOG, "a") as f:
        f.write(stats)
