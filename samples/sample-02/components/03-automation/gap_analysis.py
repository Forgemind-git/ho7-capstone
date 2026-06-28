"""
OPTIONAL — ADVANCED AUTOMATION (not required for the course)
This script uses the Anthropic API, which needs an ANTHROPIC_API_KEY and is billed
per use — that is SEPARATE from your Claude.ai subscription. The hands-on is built
entirely in Claude.ai with NO API key. See the sample README's
"Use it with your Claude.ai subscription" section for the no-code version.

Competitor Intelligence Gap Analysis
HO7 Capstone — Sample 02

Reads competitor documents from 02-context-pack/, runs a three-pass analysis
using Claude, and writes:
  - gap_report.md   : formatted Markdown report
  - gap_report.json : structured data for downstream tools

Requirements:
    pip install anthropic python-dotenv

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python gap_analysis.py
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = Path(__file__).parent
PROMPT_DIR = BASE.parent / "01-prompt-library"
CONTEXT_DIR = BASE.parent / "02-context-pack"
OUTPUT_MD = BASE / "gap_report.md"
OUTPUT_JSON = BASE / "gap_report.json"

COMPETITOR_FILES = {
    "Acme Corp": "competitor-a-notes.txt",
    "Beta Tools": "competitor-b-notes.txt",
}
OUR_PRODUCT_FILE = "our-product-summary.txt"


def load_file(path: Path) -> str:
    """Read a text file."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}")
        sys.exit(1)


def extract_system_prompt(prompt_md: str) -> str:
    """Extract the content of the first ``` ``` code fence in a .md file."""
    lines = prompt_md.split("\n")
    in_fence = False
    captured = []
    for line in lines:
        if line.strip().startswith("```") and not in_fence:
            in_fence = True
            continue
        if line.strip() == "```" and in_fence:
            break
        if in_fence:
            captured.append(line)
    return "\n".join(captured).strip() if captured else prompt_md.strip()


def call_claude(client: anthropic.Anthropic, system: str, user: str, model: str = "claude-3-5-sonnet-20241022") -> str:
    """Call Claude and return the raw text response."""
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text.strip()


def extract_features(client: anthropic.Anthropic, system: str, competitor_name: str, doc_text: str) -> list[dict]:
    """Pass 1: Extract structured features from a competitor document."""
    user_msg = f"Competitor name: {competitor_name}\n\n---\n\n{doc_text}"
    raw = call_claude(client, system, user_msg)

    # Strip markdown fences if Claude wrapped the JSON
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:-1]).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  WARNING: Could not parse feature extraction JSON for {competitor_name}: {e}")
        print(f"  Raw output (first 200 chars): {raw[:200]}")
        return []


def run_gap_analysis(client: anthropic.Anthropic, system: str, features: list[dict], our_product: str) -> dict:
    """Pass 2: Compare extracted features against our product."""
    user_msg = (
        f"## Competitor Features (JSON)\n\n{json.dumps(features, indent=2)}\n\n"
        f"---\n\n## Our Product Summary\n\n{our_product}"
    )
    raw = call_claude(client, system, user_msg)

    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:-1]).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  WARNING: Could not parse gap analysis JSON: {e}")
        print(f"  Raw output (first 200 chars): {raw[:200]}")
        return {"gaps": [], "pricing_summary": "", "positioning_gaps": [], "quick_wins": []}


def assemble_report(client: anthropic.Anthropic, system: str, gap_data: dict) -> str:
    """Pass 3: Turn the gap JSON into a formatted Markdown report."""
    user_msg = json.dumps(gap_data, indent=2)
    return call_claude(client, system, user_msg)


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Load prompts
    extraction_system = extract_system_prompt(load_file(PROMPT_DIR / "research-extraction-prompt.md"))
    gap_system = extract_system_prompt(load_file(PROMPT_DIR / "gap-analysis-prompt.md"))
    report_system = extract_system_prompt(load_file(PROMPT_DIR / "report-assembly-prompt.md"))

    # Load our product summary
    our_product = load_file(CONTEXT_DIR / OUR_PRODUCT_FILE)

    # -----------------------------------------------------------------------
    # PASS 1: Extract features from each competitor document
    # -----------------------------------------------------------------------
    print("Loading competitor materials...")
    all_features: list[dict] = []

    for competitor_name, filename in COMPETITOR_FILES.items():
        doc_path = CONTEXT_DIR / filename
        doc_text = load_file(doc_path)
        print(f"  {competitor_name}: {filename} ({len(doc_text):,} chars)")

        print(f"\nRunning Pass 1 — Feature extraction for {competitor_name}...")
        features = extract_features(client, extraction_system, competitor_name, doc_text)
        all_features.extend(features)
        print(f"  Extracted {len(features)} features")

    print(f"\nOur product: {OUR_PRODUCT_FILE} ({len(our_product):,} chars)")
    print(f"Total competitor features extracted: {len(all_features)}")

    # -----------------------------------------------------------------------
    # PASS 2: Gap analysis
    # -----------------------------------------------------------------------
    print("\nRunning Pass 2 — Gap analysis...")
    gap_data = run_gap_analysis(client, gap_system, all_features, our_product)

    gaps = gap_data.get("gaps", [])
    high_priority = [g for g in gaps if g.get("priority") == "high"]
    dont_have = [g for g in gaps if g.get("our_status") == "dont-have"]

    print(f"  Total gap items: {len(gaps)}")
    print(f"  High-priority gaps: {len(high_priority)}")
    print(f"  Features we don't have: {len(dont_have)}")

    # -----------------------------------------------------------------------
    # PASS 3: Assemble report
    # -----------------------------------------------------------------------
    print("\nRunning Pass 3 — Report assembly...")
    report_md = assemble_report(client, report_system, gap_data)

    # Add header
    header = f"# Competitive Gap Analysis Report\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n\n"
    full_report = header + report_md

    # -----------------------------------------------------------------------
    # Write outputs
    # -----------------------------------------------------------------------
    OUTPUT_MD.write_text(full_report, encoding="utf-8")
    print(f"\ngap_report.md written ({len(full_report):,} chars) -> {OUTPUT_MD}")

    output_data = {
        "generated_at": datetime.now().isoformat(),
        "competitors_analysed": list(COMPETITOR_FILES.keys()),
        **gap_data,
    }
    OUTPUT_JSON.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    print(f"gap_report.json written ({len(gaps)} gap items) -> {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
