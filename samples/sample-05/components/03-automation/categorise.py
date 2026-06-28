"""
OPTIONAL — ADVANCED AUTOMATION (not required for the course)
This script uses the Anthropic API, which needs an ANTHROPIC_API_KEY and is billed
per use — that is SEPARATE from your Claude.ai subscription. The hands-on is built
entirely in Claude.ai with NO API key. See the sample README's
"Use it with your Claude.ai subscription" section for the no-code version.

Transaction Categoriser
HO7 Capstone — Sample 05 (Step 1 of 3)

Reads a bank export CSV, categorises each transaction using Claude,
and writes a categorised CSV with added columns.

Requirements:
    pip install anthropic python-dotenv

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python categorise.py
    # or with a specific input file:
    python categorise.py --input my_bank_export.csv
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

BASE = Path(__file__).parent
PROMPT_DIR = BASE.parent / "01-prompt-library"
DEFAULT_INPUT = BASE / "sample_transactions.csv"
OUTPUT_FILE = BASE / "categorised.csv"


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


def categorise_transaction(client: anthropic.Anthropic, system: str, description: str, amount: str) -> dict:
    """Call Claude to categorise a single transaction."""
    user_msg = f"Description: {description}\nAmount: {amount}"
    response = client.messages.create(
        model="claude-3-haiku-20240307",  # Use Haiku for speed and cost on this high-volume task
        max_tokens=256,
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    )
    raw = response.content[0].text.strip()

    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:-1]).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: return "other" category
        return {
            "category": "other",
            "subcategory": "",
            "is_essential": False,
            "confidence": 0.0,
            "notes": f"Parse error: {raw[:100]}",
        }


def main():
    parser = argparse.ArgumentParser(description="Transaction Categoriser")
    parser.add_argument("--input", type=str, help="Path to input CSV file")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    input_file = Path(args.input) if args.input else DEFAULT_INPUT
    if not input_file.exists():
        print(f"ERROR: Input file not found: {input_file}")
        sys.exit(1)

    system = extract_system_prompt(load_file(PROMPT_DIR / "categorise-prompt.md"))

    with open(input_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Categorising {len(rows)} transactions from {input_file.name}...")

    results = []
    low_confidence_count = 0

    for i, row in enumerate(rows, 1):
        description = row.get("description", "")
        amount = row.get("amount", "0")

        result = categorise_transaction(client, system, description, amount)

        category = result.get("category", "other")
        confidence = result.get("confidence", 0.0)
        flag = " ← LOW CONFIDENCE" if confidence < 0.7 else ""

        print(f"  Row {i:2d}: {description[:35]:<35} {amount:>8} -> {category} ({confidence:.2f}){flag}")

        if confidence < 0.7:
            low_confidence_count += 1

        results.append({
            **row,
            "category": category,
            "subcategory": result.get("subcategory", ""),
            "is_essential": result.get("is_essential", False),
            "confidence": confidence,
            "categorisation_notes": result.get("notes", ""),
        })

    # Write output
    if results:
        fieldnames = list(results[0].keys())
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    print(f"\ncategorised.csv written ({len(results)} rows) -> {OUTPUT_FILE}")

    if low_confidence_count > 0:
        print(f"WARNING: {low_confidence_count} transaction(s) have low confidence (<0.7) — review manually.")

    print("\nNext steps:")
    print("  Run: python ask.py        (to ask questions about your spending)")
    print("  Run: python monthly_rollup.py  (to generate the monthly report)")


if __name__ == "__main__":
    main()
