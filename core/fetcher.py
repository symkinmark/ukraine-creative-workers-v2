"""
fetcher.py — pulls content from RSS feeds and simple HTML pages.

Returns normalised item dicts: {title, url, date, excerpt, source_name}
No Playwright, no JavaScript rendering — requests + feedparser + bs4 only.
"""

import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import time


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
TIMEOUT = 15  # seconds per request


def _normalise_date(raw_date) -> str:
    """Convert feedparser time struct or string to ISO date string."""
    if not raw_date:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if hasattr(raw_date, "tm_year"):
        try:
            dt = datetime(*raw_date[:6], tzinfo=timezone.utc)
            return dt.strftime("%Y-%m-%d")
        except Exception:
            pass
    return str(raw_date)[:10]


def fetch_rss(url: str, source_name: str) -> list[dict]:
    """
    Fetch an RSS/Atom feed. Returns list of normalised item dicts.
    Empty list on any error — never raises.
    """
    items = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        feed = feedparser.parse(response.text)

        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "")
            date = _normalise_date(entry.get("published_parsed") or entry.get("updated_parsed"))
            excerpt = ""

            # Try summary, then content
            if entry.get("summary"):
                excerpt = BeautifulSoup(entry.summary, "html.parser").get_text(separator=" ").strip()
            elif entry.get("content"):
                excerpt = BeautifulSoup(entry.content[0].value, "html.parser").get_text(separator=" ").strip()

            # Truncate excerpt to 500 chars
            excerpt = excerpt[:500]

            if title and link:
                items.append({
                    "title": title,
                    "url": link,
                    "date": date,
                    "excerpt": excerpt,
                    "source_name": source_name,
                })

    except Exception as e:
        print(f"  [fetcher] RSS error — {source_name}: {e}")

    return items


def fetch_html(url: str, source_name: str, selectors: dict) -> list[dict]:
    """
    Scrape a simple HTML page using CSS selectors from sources.json.
    Returns list of normalised item dicts. Empty list on any error.
    """
    items = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        item_selector = selectors.get("items", "article")
        title_selector = selectors.get("title", "h2")
        excerpt_selector = selectors.get("excerpt", "p")
        date_selector = selectors.get("date", "time")

        for container in soup.select(item_selector)[:20]:  # max 20 items
            # Title
            title_el = container.select_one(title_selector)
            if not title_el:
                continue
            title = title_el.get_text(separator=" ").strip()
            if not title:
                continue

            # URL — look for <a> in title or container
            link = ""
            a_tag = title_el.find("a") or container.find("a")
            if a_tag and a_tag.get("href"):
                href = a_tag["href"]
                if href.startswith("http"):
                    link = href
                else:
                    # Relative URL — build from base
                    from urllib.parse import urlparse, urljoin
                    base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
                    link = urljoin(base, href)

            # Excerpt
            excerpt_el = container.select_one(excerpt_selector)
            excerpt = excerpt_el.get_text(separator=" ").strip()[:500] if excerpt_el else ""

            # Date
            date_el = container.select_one(date_selector)
            raw_date = ""
            if date_el:
                raw_date = date_el.get("datetime") or date_el.get_text().strip()
            date = _normalise_date(raw_date) if raw_date else datetime.now(timezone.utc).strftime("%Y-%m-%d")

            items.append({
                "title": title,
                "url": link or url,
                "date": date,
                "excerpt": excerpt,
                "source_name": source_name,
            })

        time.sleep(1)  # polite crawl delay

    except Exception as e:
        print(f"  [fetcher] HTML error — {source_name}: {e}")

    return items
