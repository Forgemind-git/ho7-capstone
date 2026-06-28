"""
OPTIONAL — ADVANCED AUTOMATION (not required for the course)
This script uses the Anthropic API, which needs an ANTHROPIC_API_KEY and is billed
per use — that is SEPARATE from your Claude.ai subscription. The hands-on is built
entirely in Claude.ai with NO API key. See the sample README's
"Use it with your Claude.ai subscription" section for the no-code version.

Interview Question Generator
HO7 Capstone — Sample 03 (Step 1 of 3)

Generates a structured interview question guide for a role, grounded in the
role description, company values, and scoring rubric.

Requirements:
    pip install anthropic python-dotenv

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python generate_questions.py
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
CONTEXT_DIR = BASE.parent / "02-context-pack"
OUTPUT_FILE = BASE / "interview_questions.json"


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

    # Load and build system prompt with injected context
    prompt_template = extract_system_prompt(load_file(PROMPT_DIR / "screening-questions-prompt.md"))
    role_desc = load_file(CONTEXT_DIR / "role-description.txt")
    company_values = load_file(CONTEXT_DIR / "company-values.txt")
    rubric = load_file(CONTEXT_DIR / "scoring-rubric.txt")

    system = (
        f"{prompt_template}\n\n"
        f"## Role Description\n{role_desc}\n\n"
        f"## Company Values\n{company_values}\n\n"
        f"## Scoring Rubric\n{rubric}"
    )

    role_title = "Senior Product Designer"
    print(f"Generating interview questions for: {role_title}")
    print("  Based on role description, 4 company values, and scoring rubric...")

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": f"Generate the interview question guide for: {role_title}"}],
    )
    raw = response.content[0].text.strip()

    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:-1]).strip()

    try:
        questions = json.loads(raw)
        total_q = sum(len(theme["questions"]) for theme in questions.get("question_guide", []))
        OUTPUT_FILE.write_text(json.dumps(questions, indent=2), encoding="utf-8")
        print(f"  {total_q} questions generated across {len(questions.get('question_guide', []))} themes")
        print(f"interview_questions.json written -> {OUTPUT_FILE}")
    except json.JSONDecodeError as e:
        print(f"WARNING: Could not parse JSON response: {e}")
        OUTPUT_FILE.write_text(raw, encoding="utf-8")
        print(f"Raw output saved -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
