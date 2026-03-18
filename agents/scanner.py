"""
scanner.py — reads sources.json, fetches all sources, returns raw_items list.

Called by run.py. Does not filter or score — just fetches and normalises.
"""

import json
import sys
from pathlib import Path

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.fetcher import fetch_rss, fetch_html

SOURCES_FILE = Path(__file__).parent.parent / "config" / "sources.json"


def run() -> list[dict]:
    """
    Fetch all sources. Returns flat list of normalised item dicts.
    Each item: {title, url, date, excerpt, source_name}
    """
    config = json.loads(SOURCES_FILE.read_text())
    sources = config.get("sources", [])

    all_items = []

    for source in sources:
        name = source["name"]
        url = source["url"]
        source_type = source.get("type", "rss")
        priority = source.get("priority", "medium")

        print(f"  [scanner] Fetching {name} ({source_type}, {priority})...")

        if source_type == "rss":
            items = fetch_rss(url, name)
        elif source_type == "html":
            selectors = source.get("selectors", {})
            items = fetch_html(url, name, selectors)
        else:
            print(f"  [scanner] Unknown type '{source_type}' for {name}, skipping")
            continue

        print(f"  [scanner] Got {len(items)} items from {name}")
        all_items.extend(items)

    print(f"\n  [scanner] Total raw items: {len(all_items)}")
    return all_items


if __name__ == "__main__":
    items = run()
    for item in items[:3]:
        print(f"\n  Title: {item['title'][:80]}")
        print(f"  Source: {item['source_name']} | Date: {item['date']}")
        print(f"  URL: {item['url'][:80]}")
