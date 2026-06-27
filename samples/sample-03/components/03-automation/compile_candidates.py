"""
Candidate Comparison Compiler
HO7 Capstone — Sample 03 (Step 3 of 3)

Reads per-candidate score JSON files and generates a formatted comparison report.

Requirements:
    pip install anthropic python-dotenv

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python compile_candidates.py
"""

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
SCORES_DIR = BASE / "candidate_scores"
OUTPUT_FILE = BASE / "candidate_comparison.md"


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


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    system = extract_system_prompt(load_file(PROMPT_DIR / "note-compiler-prompt.md"))

    score_files = sorted(SCORES_DIR.glob("*-scores.json"))
    if not score_files:
        print(f"ERROR: No score files found in {SCORES_DIR}. Run score_candidates.py first.")
        sys.exit(1)

    candidates = []
    for score_file in score_files:
        try:
            data = json.loads(score_file.read_text(encoding="utf-8"))
            candidates.append(data)
            print(f"  Loaded: {score_file.name} — {data.get('candidate_name', 'Unknown')}")
        except json.JSONDecodeError:
            print(f"  WARNING: Could not parse {score_file.name} — skipping")

    if not candidates:
        print("ERROR: No valid candidate score files found.")
        sys.exit(1)

    print(f"\nCompiling comparison report for {len(candidates)} candidate(s)...")

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": json.dumps(candidates, indent=2)}],
    )
    report = response.content[0].text.strip()

    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"\ncandidate_comparison.md written ({len(report):,} chars) -> {OUTPUT_FILE}")
    print("Share this report with your hiring panel.")


if __name__ == "__main__":
    main()
