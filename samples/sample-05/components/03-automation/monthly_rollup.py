"""
OPTIONAL — ADVANCED AUTOMATION (not required for the course)
This script uses the Anthropic API, which needs an ANTHROPIC_API_KEY and is billed
per use — that is SEPARATE from your Claude.ai subscription. The hands-on is built
entirely in Claude.ai with NO API key. See the sample README's
"Use it with your Claude.ai subscription" section for the no-code version.

Monthly Roll-Up Report Generator
HO7 Capstone — Sample 05 (Step 3 of 3)

Reads categorised.csv, computes totals by category, and generates
a formatted monthly report using Claude.

Requirements:
    pip install anthropic python-dotenv

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python monthly_rollup.py
"""

import csv
import os
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

BASE = Path(__file__).parent
PROMPT_DIR = BASE.parent / "01-prompt-library"
CONTEXT_DIR = BASE.parent / "02-context-pack"
CATEGORISED_CSV = BASE / "categorised.csv"


def load_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}")
        sys.exit(1)


def extract_system_prompt(prompt_md: str) -> str:
    lines = prompt_md.split("\n")
    in_fence, captured = False, []
    for line in lines:
        if line.strip().startswith("```") and not in_fence:
            in_fence = True
            continue
        if line.strip() == "```" and in_fence:
            break
        if in_fence:
            captured.append(line)
    return "\n".join(captured).strip() if captured else prompt_md.strip()


def compute_summary(rows: list[dict]) -> dict:
    """Compute category totals and transaction counts from categorised rows."""
    category_totals = defaultdict(float)
    category_counts = defaultdict(int)
    total_income = 0.0
    total_spending = 0.0
    essential_total = 0.0
    non_essential_total = 0.0
    top_transactions = []

    for row in rows:
        try:
            amount = float(row.get("amount", 0))
            category = row.get("category", "other")
            is_essential_raw = row.get("is_essential", "False")
            is_essential = str(is_essential_raw).lower() in ("true", "1", "yes")

            if amount > 0:
                total_income += amount
            else:
                spending = abs(amount)
                total_spending += spending
                category_totals[category] += spending
                category_counts[category] += 1

                if is_essential:
                    essential_total += spending
                else:
                    non_essential_total += spending

                top_transactions.append({
                    "date": row.get("date", ""),
                    "description": row.get("description", ""),
                    "amount": spending,
                    "category": category,
                })
        except (ValueError, TypeError):
            continue

    top_transactions.sort(key=lambda x: x["amount"], reverse=True)

    return {
        "total_income": round(total_income, 2),
        "total_spending": round(total_spending, 2),
        "net": round(total_income - total_spending, 2),
        "essential_total": round(essential_total, 2),
        "non_essential_total": round(non_essential_total, 2),
        "category_totals": {k: round(v, 2) for k, v in sorted(category_totals.items(), key=lambda x: -x[1])},
        "category_counts": dict(category_counts),
        "top_5_transactions": top_transactions[:5],
    }


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    if not CATEGORISED_CSV.exists():
        print(f"ERROR: {CATEGORISED_CSV} not found. Run categorise.py first.")
        sys.exit(1)

    # Load data
    system = extract_system_prompt(load_file(PROMPT_DIR / "rollup-prompt.md"))
    financial_rules = load_file(CONTEXT_DIR / "financial-rules.txt")
    csv_content = CATEGORISED_CSV.read_text(encoding="utf-8")

    rows = list(csv.DictReader(csv_content.splitlines()))
    print(f"Loaded {len(rows)} categorised transactions")

    # Compute summary statistics
    summary = compute_summary(rows)

    print(f"  Total income:    £{summary['total_income']:.2f}")
    print(f"  Total spending:  £{summary['total_spending']:.2f}")
    print(f"  Net:             £{summary['net']:.2f}")
    print(f"  Categories: {len(summary['category_totals'])}")

    # Detect month from data
    dates = [r.get("date", "") for r in rows if r.get("date")]
    month_label = "Unknown Month"
    if dates:
        try:
            first_date = datetime.strptime(min(dates), "%Y-%m-%d")
            month_label = first_date.strftime("%B %Y")
        except ValueError:
            pass

    # Build user message with CSV + summary + budget rules
    user_msg = (
        f"## Month: {month_label}\n\n"
        f"## Summary Statistics\n"
        f"- Total income: £{summary['total_income']:.2f}\n"
        f"- Total spending: £{summary['total_spending']:.2f}\n"
        f"- Net: £{summary['net']:.2f}\n"
        f"- Essential spending: £{summary['essential_total']:.2f}\n"
        f"- Non-essential spending: £{summary['non_essential_total']:.2f}\n\n"
        f"## Spending by Category\n"
        + "\n".join(
            f"- {cat}: £{amt:.2f} ({summary['category_counts'].get(cat, 0)} transactions)"
            for cat, amt in summary["category_totals"].items()
        )
        + f"\n\n## Top 5 Individual Transactions\n"
        + "\n".join(
            f"- {t['date']} | {t['description']} | £{t['amount']:.2f} | {t['category']}"
            for t in summary["top_5_transactions"]
        )
        + f"\n\n## Budget Rules\n{financial_rules}"
    )

    print("\nGenerating monthly report...")
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=3000,
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    )
    report = response.content[0].text.strip()

    # Write report with date-stamped filename
    month_slug = month_label.replace(" ", "-").lower() if month_label != "Unknown Month" else "unknown"
    output_file = BASE / f"{month_slug}_monthly_report.md"
    output_file.write_text(report, encoding="utf-8")

    print(f"\nMonthly report written ({len(report):,} chars) -> {output_file}")


if __name__ == "__main__":
    main()
