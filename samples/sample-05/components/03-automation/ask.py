"""
OPTIONAL — ADVANCED AUTOMATION (not required for the course)
This script uses the Anthropic API, which needs an ANTHROPIC_API_KEY and is billed
per use — that is SEPARATE from your Claude.ai subscription. The hands-on is built
entirely in Claude.ai with NO API key. See the sample README's
"Use it with your Claude.ai subscription" section for the no-code version.

Finance Q&A — Interactive Mode
HO7 Capstone — Sample 05 (Step 2 of 3)

Loads categorised.csv and financial-rules.txt, then lets you ask natural-language
questions about your spending in a multi-turn conversation.

Requirements:
    pip install anthropic python-dotenv

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python ask.py
"""

import csv
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


def load_categorised_csv(path: Path) -> tuple[str, int]:
    """Read the categorised CSV and return it as a string + row count."""
    try:
        content = path.read_text(encoding="utf-8")
        rows = list(csv.DictReader(content.splitlines()))
        return content, len(rows)
    except FileNotFoundError:
        return "", 0


def build_system_prompt(prompt_template: str, csv_content: str, financial_rules: str) -> str:
    """Inject context into the system prompt."""
    return (
        prompt_template
        .replace("{{TRANSACTIONS_CSV}}", csv_content)
        .replace("{{FINANCIAL_RULES}}", financial_rules)
    )


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Check if categorised CSV exists
    if not CATEGORISED_CSV.exists():
        print(f"ERROR: categorised.csv not found.")
        print("Run categorise.py first to process your transactions.")
        sys.exit(1)

    # Load data
    prompt_template = extract_system_prompt(load_file(PROMPT_DIR / "qa-prompt.md"))
    financial_rules = load_file(CONTEXT_DIR / "financial-rules.txt")
    csv_content, row_count = load_categorised_csv(CATEGORISED_CSV)

    if row_count == 0:
        print("ERROR: categorised.csv is empty. Run categorise.py first.")
        sys.exit(1)

    # Detect date range from CSV for display
    try:
        rows = list(csv.DictReader(csv_content.splitlines()))
        dates = [r.get("date", "") for r in rows if r.get("date")]
        date_range = f"{min(dates)} to {max(dates)}" if dates else "unknown date range"
    except Exception:
        date_range = "unknown date range"

    system = build_system_prompt(prompt_template, csv_content, financial_rules)

    print("\nFinance Copilot — Q&A Mode")
    print(f"Your data: {row_count} transactions ({date_range})")
    print("Type 'exit' or 'quit' to stop. Press Ctrl+C at any time.")
    print("-" * 50)

    conversation_history = []

    while True:
        try:
            user_input = input("\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if user_input.lower() in ("exit", "quit", "q", "bye"):
            print("Goodbye!")
            break

        if not user_input:
            continue

        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=system,
                messages=conversation_history,
            )
            answer = response.content[0].text.strip()
            conversation_history.append({"role": "assistant", "content": answer})
            print(f"\n{answer}")

        except anthropic.APIError as e:
            print(f"\nAPI Error: {e}")
            # Remove the last user message so the conversation stays valid
            conversation_history.pop()

        except Exception as e:
            print(f"\nUnexpected error: {e}")
            conversation_history.pop()


if __name__ == "__main__":
    main()
