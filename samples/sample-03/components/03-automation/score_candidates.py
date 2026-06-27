"""
Candidate Scorer
HO7 Capstone — Sample 03 (Step 2 of 3)

Scores each candidate transcript against the defined rubric.
Reads transcripts from sample_transcripts/ and writes per-candidate JSON files.

Requirements:
    pip install anthropic python-dotenv

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python score_candidates.py
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
TRANSCRIPTS_DIR = BASE / "sample_transcripts"
SCORES_DIR = BASE / "candidate_scores"


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


def score_transcript(client: anthropic.Anthropic, system: str, transcript: str) -> dict:
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": transcript}],
    )
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:-1]).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  WARNING: Could not parse score JSON: {e}")
        return {"error": "parse_failed", "raw": raw[:500]}


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    prompt_template = extract_system_prompt(load_file(PROMPT_DIR / "score-candidate-prompt.md"))
    rubric = load_file(CONTEXT_DIR / "scoring-rubric.txt")
    system = f"{prompt_template}\n\n## Scoring Rubric\n{rubric}"

    SCORES_DIR.mkdir(exist_ok=True)

    transcript_files = sorted(TRANSCRIPTS_DIR.glob("*.txt"))
    if not transcript_files:
        print(f"ERROR: No transcript .txt files found in {TRANSCRIPTS_DIR}")
        sys.exit(1)

    print(f"Scoring {len(transcript_files)} candidate transcript(s)...")

    for transcript_file in transcript_files:
        transcript_text = load_file(transcript_file)
        candidate_id = transcript_file.stem

        print(f"\n  Scoring: {transcript_file.name}")
        scores = score_transcript(client, system, transcript_text)

        name = scores.get("candidate_name", candidate_id)
        overall = scores.get("overall_score", "?")
        recommendation = scores.get("recommendation", "?")
        print(f"  -> {name}: Overall {overall}/5 — {recommendation}")

        output_file = SCORES_DIR / f"{candidate_id}-scores.json"
        output_file.write_text(json.dumps(scores, indent=2), encoding="utf-8")
        print(f"  -> Saved: {output_file.name}")

    print(f"\nAll scores written to {SCORES_DIR}/")
    print("Run compile_candidates.py to generate the comparison report.")


if __name__ == "__main__":
    main()
