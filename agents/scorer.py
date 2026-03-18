"""
scorer.py — uses Claude Haiku to score each item 0–5 against AKS criteria.

Scoring criteria (1 point each):
  1. Sector match — defence/miltech/dual-use/deep tech/cyber/space/drone/C2/ISR/AI-for-defence
  2. Stage match — startup or scale-up (NOT primes like Lockheed, BAE, Raytheon, etc.)
  3. Geography match — EU / UK / Israel / Ukraine / NATO-aligned country
  4. Signal type — Seed/Series A/B / grant / contract award (not just opinion piece)
  5. Signal freshness — published within last 7 days

HIGH = 5/5, MEDIUM = 3–4/5, LOW = 0–2/5
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

import anthropic
from dotenv import load_dotenv

load_dotenv()

# Approximate cost tracking (Haiku input/output token prices)
HAIKU_INPUT_COST_PER_1M = 0.80   # USD per 1M input tokens
HAIKU_OUTPUT_COST_PER_1M = 4.00  # USD per 1M output tokens

SYSTEM_PROMPT = """You are a defence-sector investment analyst screening news items for AKS (Any Key Studio), a DSR brand/design studio.

Score this item on 5 binary criteria. Return ONLY valid JSON with no extra text.

Criteria:
1. sector: 1 if the item is about defence / miltech / dual-use / deep tech / cyber / space / drone / C2 / ISR / AI-for-defence. 0 otherwise.
2. stage: 1 if the company involved is a startup or scale-up (NOT a prime contractor like Lockheed Martin, BAE Systems, Raytheon, Airbus, Leonardo, Rheinmetall, MBDA, Thales, Boeing, Northrop Grumman). 0 otherwise.
3. geography: 1 if the company or award is in EU / UK / Israel / Ukraine / NATO-aligned country. 0 if US-only or unclear.
4. signal_type: 1 if the item reports a funding round (Seed/Series A/B/C), grant award, or contract award. 0 if it's an opinion piece, product launch, or industry analysis.
5. freshness: 1 if the item was published within the last 7 days. 0 if older or date is unclear.

Also return:
- confidence: "high" if this is a primary announcement, "medium" if inferred or aggregated, "low" if vague or secondhand
- uncertainty_flags: list of strings describing what data is unverified or uncertain (empty list if none)

JSON format (return ONLY this, no markdown):
{"sector":0,"stage":0,"geography":0,"signal_type":0,"freshness":0,"total":0,"confidence":"high","uncertainty_flags":[]}"""


def _build_user_message(item: dict) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return (
        f"Today's date: {today}\n\n"
        f"Source: {item.get('source_name', '')}\n"
        f"Title: {item.get('title', '')}\n"
        f"Date: {item.get('date', '')}\n"
        f"URL: {item.get('url', '')}\n"
        f"Excerpt: {item.get('excerpt', '')[:400]}"
    )


def score_item(client: anthropic.Anthropic, item: dict) -> tuple[dict, int, int]:
    """
    Score one item with Claude Haiku.
    Returns (score_dict, input_tokens, output_tokens).
    score_dict keys: sector, stage, geography, signal_type, freshness, total, confidence, uncertainty_flags
    """
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": _build_user_message(item)}],
        )

        raw = response.content[0].text.strip()
        score = json.loads(raw)

        # Validate and clamp
        for key in ["sector", "stage", "geography", "signal_type", "freshness"]:
            score[key] = int(bool(score.get(key, 0)))
        score["total"] = sum(score[k] for k in ["sector", "stage", "geography", "signal_type", "freshness"])
        if "confidence" not in score:
            score["confidence"] = "medium"
        if "uncertainty_flags" not in score:
            score["uncertainty_flags"] = []

        return score, response.usage.input_tokens, response.usage.output_tokens

    except json.JSONDecodeError as e:
        print(f"    [scorer] JSON parse error for '{item.get('title', '')[:40]}': {e}")
        return {"sector":0,"stage":0,"geography":0,"signal_type":0,"freshness":0,"total":0,"confidence":"low","uncertainty_flags":["scoring failed"]}, 0, 0
    except Exception as e:
        print(f"    [scorer] Error for '{item.get('title', '')[:40]}': {e}")
        return {"sector":0,"stage":0,"geography":0,"signal_type":0,"freshness":0,"total":0,"confidence":"low","uncertainty_flags":["scoring failed"]}, 0, 0


def run(items: list[dict]) -> tuple[list[dict], float]:
    """
    Score all items. Returns (scored_items, total_cost_usd).
    Each item gets a 'score' key added with the scoring dict.
    """
    if not items:
        print("  [scorer] No items to score")
        return [], 0.0

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in .env")

    client = anthropic.Anthropic(api_key=api_key)

    scored = []
    total_input_tokens = 0
    total_output_tokens = 0

    print(f"\n  [scorer] Scoring {len(items)} items with Claude Haiku...")

    for i, item in enumerate(items):
        score, in_tok, out_tok = score_item(client, item)
        item["score"] = score
        scored.append(item)
        total_input_tokens += in_tok
        total_output_tokens += out_tok

        tier = "HIGH" if score["total"] == 5 else "MED" if score["total"] >= 3 else "low"
        print(f"    [{i+1}/{len(items)}] {tier} {score['total']}/5 — {item['title'][:60]}")

        # Small delay to avoid rate limiting
        if i < len(items) - 1:
            time.sleep(0.3)

    cost = (
        (total_input_tokens / 1_000_000) * HAIKU_INPUT_COST_PER_1M +
        (total_output_tokens / 1_000_000) * HAIKU_OUTPUT_COST_PER_1M
    )

    high = sum(1 for i in scored if i["score"]["total"] == 5)
    medium = sum(1 for i in scored if 3 <= i["score"]["total"] <= 4)
    low = sum(1 for i in scored if i["score"]["total"] <= 2)
    print(f"\n  [scorer] Done. HIGH={high} MEDIUM={medium} LOW={low} | Cost: ${cost:.4f}")

    return scored, cost
