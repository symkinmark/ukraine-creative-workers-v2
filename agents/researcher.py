"""
researcher.py — uses Claude Sonnet to synthesise HIGH/MEDIUM items into a research brief.

Writes output/YYYY-MM-DD/research.md
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

SYSTEM_PROMPT = """You are a senior defence-sector analyst writing a daily intelligence brief for AKS (Any Key Studio), a DSR brand/design studio.

AKS works with defence tech startups and scale-ups (NOT prime contractors) on:
- Brand identity and visual systems
- Market positioning and messaging
- Investor communications and pitch collateral
- Exhibition and event materials
- Website and digital presence

For each company/item provided, write a structured research brief with:
1. **Company name** + one-sentence technical description (what they actually build, not marketing language)
2. **Signal**: the specific raise, contract, or grant — amount, type, lead investor/awarding body
3. **Why relevant to AKS**: the specific brand/positioning opportunity (be concrete — e.g. "series A positions them for European market entry, needs investor-facing brand" not just "needs branding")
4. **Confidence**: High/Medium/Low + any [unverified] flags on specific data points

Be direct and analytical. No filler. If data is uncertain, mark it [unverified] inline.
Write in plain English. No bullet soup — use the structure above per company."""


def _build_items_text(items: list[dict]) -> str:
    parts = []
    for i, item in enumerate(items, 1):
        score = item.get("score", {})
        flags = ", ".join(score.get("uncertainty_flags", [])) or "none"
        parts.append(
            f"ITEM {i}\n"
            f"Title: {item['title']}\n"
            f"Source: {item['source_name']} | Date: {item['date']}\n"
            f"URL: {item['url']}\n"
            f"Score: {score.get('total', 0)}/5 | Confidence: {score.get('confidence', 'unknown')}\n"
            f"Uncertainty flags: {flags}\n"
            f"Excerpt: {item.get('excerpt', '')[:600]}\n"
        )
    return "\n---\n".join(parts)


def run(scored_items: list[dict], output_dir: Path) -> tuple[Path, float]:
    """
    Takes scored items (score >= 3), writes research.md.
    Returns (output_path, cost_usd).
    """
    # Filter to HIGH and MEDIUM
    relevant = [i for i in scored_items if i.get("score", {}).get("total", 0) >= 3]

    if not relevant:
        print("  [researcher] No HIGH/MEDIUM items — skipping research brief")
        output_path = output_dir / "research.md"
        output_path.write_text(
            f"# AKS Daily Research Brief — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n\n"
            "No items scored HIGH or MEDIUM today.\n"
        )
        return output_path, 0.0

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in .env")

    client = anthropic.Anthropic(api_key=api_key)

    print(f"\n  [researcher] Writing research brief for {len(relevant)} items...")

    items_text = _build_items_text(relevant)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    user_message = (
        f"Today's date: {today}\n\n"
        f"Write a research brief for AKS covering the following {len(relevant)} items. "
        f"Focus on companies that are actual prospects for brand/design work.\n\n"
        f"{items_text}"
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    brief_content = response.content[0].text.strip()

    # Write output file
    output_path = output_dir / "research.md"
    output_path.write_text(
        f"# AKS Daily Research Brief — {today}\n\n"
        f"**Items reviewed:** {len(relevant)} (HIGH/MEDIUM score)\n"
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        "---\n\n"
        f"{brief_content}\n"
    )

    cost = (
        (response.usage.input_tokens / 1_000_000) * SONNET_INPUT_COST_PER_1M +
        (response.usage.output_tokens / 1_000_000) * SONNET_OUTPUT_COST_PER_1M
    )

    print(f"  [researcher] research.md written ({response.usage.output_tokens} tokens | ${cost:.4f})")
    return output_path, cost
