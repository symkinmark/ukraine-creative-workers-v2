"""
copywriter.py — uses Claude Sonnet to write cold outreach emails for top 5 companies.

Reads the top 5 HIGH-scored items (or falls back to MEDIUM if fewer than 5 HIGH).
Writes output/YYYY-MM-DD/outreach_drafts.md
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

import anthropic
from dotenv import load_dotenv

load_dotenv()

SONNET_INPUT_COST_PER_1M = 3.00
SONNET_OUTPUT_COST_PER_1M = 15.00

SYSTEM_PROMPT = """You are writing outreach emails for AKS (Any Key Studio), a brand design studio specialising in the DSR (Defence, Security, Resilience) sector. AKS works with defence tech startups and scale-ups on brand identity, market positioning, and communications.

Your emails are direct, intelligent, and brief. You never use: "I hope this finds you well", "synergy", "leverage", "reaching out", "circle back", "touch base", "game-changer", "revolutionary", "innovative solution".

Rules:
- Hook: reference their specific raise, contract, or award in the first sentence — show you were paying attention
- AKS value: one specific, concrete reason their stage/moment needs brand work (not generic praise)
- CTA: one low-friction ask — a 20-minute call, a deck, or an intro
- Length: 150–200 words max per email
- Tone: peer-to-peer, not vendor-to-client

For each company, write:
- Subject line variant A
- Subject line variant B
- The email body

Format each company as:
## [Company Name]
**Subject A:** ...
**Subject B:** ...

[Email body]

---"""


def _select_top_companies(scored_items: list[dict], n: int = 5) -> list[dict]:
    """Pick top n items by score. HIGH first, then MEDIUM."""
    sorted_items = sorted(
        [i for i in scored_items if i.get("score", {}).get("total", 0) >= 3],
        key=lambda x: x.get("score", {}).get("total", 0),
        reverse=True,
    )
    return sorted_items[:n]


def _build_company_brief(item: dict) -> str:
    score = item.get("score", {})
    flags = ", ".join(score.get("uncertainty_flags", [])) or "none"
    return (
        f"Company/Item: {item['title']}\n"
        f"Source: {item['source_name']} | Date: {item['date']}\n"
        f"Score: {score.get('total', 0)}/5 | Confidence: {score.get('confidence', 'unknown')}\n"
        f"Uncertainty flags: {flags}\n"
        f"Details: {item.get('excerpt', '')[:600]}\n"
        f"URL: {item['url']}"
    )


def run(scored_items: list[dict], output_dir: Path) -> tuple[Path, float]:
    """
    Write outreach_drafts.md for top 5 companies.
    Returns (output_path, cost_usd).
    """
    top_companies = _select_top_companies(scored_items)
    output_path = output_dir / "outreach_drafts.md"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if not top_companies:
        print("  [copywriter] No companies scored ≥3 — skipping outreach drafts")
        output_path.write_text(
            f"# AKS Outreach Drafts — {today}\n\n"
            "No companies scored HIGH or MEDIUM today.\n"
        )
        return output_path, 0.0

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in .env")

    client = anthropic.Anthropic(api_key=api_key)

    print(f"\n  [copywriter] Writing outreach drafts for {len(top_companies)} companies...")

    companies_text = "\n\n===\n\n".join(_build_company_brief(c) for c in top_companies)

    user_message = (
        f"Today's date: {today}\n\n"
        f"Write cold outreach emails for AKS to the following {len(top_companies)} companies. "
        f"Each email must reference the specific signal (raise/contract/award) from the details provided.\n\n"
        f"{companies_text}"
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=3000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    drafts_content = response.content[0].text.strip()

    output_path.write_text(
        f"# AKS Outreach Drafts — {today}\n\n"
        f"**Companies:** {len(top_companies)}\n"
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        "> These are drafts. Review and personalise before sending. "
        "Verify any [unverified] data points before referencing them.\n\n"
        "---\n\n"
        f"{drafts_content}\n"
    )

    cost = (
        (response.usage.input_tokens / 1_000_000) * SONNET_INPUT_COST_PER_1M +
        (response.usage.output_tokens / 1_000_000) * SONNET_OUTPUT_COST_PER_1M
    )

    print(f"  [copywriter] outreach_drafts.md written ({response.usage.output_tokens} tokens | ${cost:.4f})")
    return output_path, cost
