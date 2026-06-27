"""
AI Support Triage Pipeline
HO7 Capstone — Sample 01

Reads support tickets from sample_tickets.csv, runs each through three prompts
(tagging, severity scoring, response drafting) using Claude, and writes:
  - triage_output.csv  : per-ticket results
  - trend_report.md    : aggregated summary

Requirements:
    pip install anthropic python-dotenv

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python triage_pipeline.py
"""

import csv
import json
import os
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

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
TICKETS_CSV = BASE / "sample_tickets.csv"
OUTPUT_CSV = BASE / "triage_output.csv"
TREND_MD = BASE / "trend_report.md"


def load_file(path: Path) -> str:
    """Read a text file and return its contents."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: Required file not found: {path}")
        sys.exit(1)


def extract_system_prompt(prompt_md: str) -> str:
    """
    Extract the content between the first ```  ``` code fence in a prompt .md file.
    Falls back to the full file if no fence found.
    """
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


def call_claude(client: anthropic.Anthropic, system: str, user: str, model: str = "claude-3-haiku-20240307") -> str:
    """Call Claude and return the text response."""
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text.strip()


def tag_ticket(client: anthropic.Anthropic, system: str, ticket: dict) -> dict:
    """Run the tagging prompt and parse the JSON result."""
    user_msg = f"Subject: {ticket['subject']}\n\nBody: {ticket['body']}"
    raw = call_claude(client, system, user_msg)
    try:
        result = json.loads(raw)
        return {"tag": result.get("tag", "other"), "tag_confidence": result.get("confidence", 0.0)}
    except json.JSONDecodeError:
        print(f"    WARNING: Could not parse tagging JSON: {raw[:80]}")
        return {"tag": "other", "tag_confidence": 0.0}


def score_severity(client: anthropic.Anthropic, system: str, ticket: dict, tag: str) -> dict:
    """Run the severity prompt and parse the JSON result."""
    user_msg = f"Subject: {ticket['subject']}\n\nBody: {ticket['body']}\n\nCategory tag: {tag}"
    raw = call_claude(client, system, user_msg)
    try:
        result = json.loads(raw)
        return {
            "severity": int(result.get("severity", 3)),
            "rationale": result.get("rationale", ""),
        }
    except (json.JSONDecodeError, ValueError):
        print(f"    WARNING: Could not parse severity JSON: {raw[:80]}")
        return {"severity": 3, "rationale": "Could not parse severity response."}


def draft_response(client: anthropic.Anthropic, system_template: str, ticket: dict, product_docs: str, known_issues: str) -> str:
    """Inject context docs into the system prompt and draft a response."""
    system = system_template.replace("{{PRODUCT_DOCS}}", product_docs).replace("{{KNOWN_ISSUES}}", known_issues)
    user_msg = f"Subject: {ticket['subject']}\n\nBody: {ticket['body']}"
    return call_claude(client, system, user_msg, model="claude-3-5-sonnet-20241022")


def build_trend_report(results: list[dict]) -> str:
    """Generate a Markdown trend report from processed ticket results."""
    total = len(results)
    if total == 0:
        return "# Trend Report\n\nNo tickets processed."

    tags = Counter(r["tag"] for r in results)
    severities = [r["severity"] for r in results]
    avg_sev = sum(severities) / len(severities)
    p1_tickets = [r for r in results if r["severity"] == 1]
    p2_tickets = [r for r in results if r["severity"] == 2]

    top_tags = tags.most_common(5)

    lines = [
        f"# Support Triage — Trend Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"",
        f"## Summary",
        f"- **Total tickets processed:** {total}",
        f"- **Average severity:** {avg_sev:.1f} (1=Critical, 4=Low)",
        f"- **Critical (P1) tickets:** {len(p1_tickets)}",
        f"- **High (P2) tickets:** {len(p2_tickets)}",
        f"",
        f"## Top Issue Categories",
    ]

    for tag, count in top_tags:
        pct = count / total * 100
        lines.append(f"- `{tag}`: {count} tickets ({pct:.0f}%)")

    if p1_tickets:
        lines.extend(["", "## Critical Tickets — Immediate Action Required"])
        for t in p1_tickets:
            lines.append(f"- **{t['ticket_id']}**: {t['subject']} — _{t['rationale']}_")

    lines.extend([
        "",
        "## Recommended Actions",
        f"1. Address {len(p1_tickets)} critical tickets before end of day.",
        f"2. The `{top_tags[0][0]}` category accounts for {top_tags[0][1]} tickets — review for systemic issues.",
        "3. Share this report in sprint planning to prioritise engineering fixes.",
    ])

    return "\n".join(lines)


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Load prompts
    tagging_md = load_file(PROMPT_DIR / "tagging-prompt.md")
    severity_md = load_file(PROMPT_DIR / "severity-prompt.md")
    response_md = load_file(PROMPT_DIR / "response-draft-prompt.md")

    tagging_system = extract_system_prompt(tagging_md)
    severity_system = extract_system_prompt(severity_md)
    response_system_template = extract_system_prompt(response_md)

    # Load context docs
    product_docs = load_file(CONTEXT_DIR / "product-docs.txt")
    known_issues = load_file(CONTEXT_DIR / "known-issues.txt")

    # Load tickets
    with open(TICKETS_CSV, newline="", encoding="utf-8") as f:
        tickets = list(csv.DictReader(f))

    print(f"Loaded {len(tickets)} tickets from {TICKETS_CSV.name}")
    print("-" * 60)

    results = []
    for i, ticket in enumerate(tickets, 1):
        print(f"Processing ticket {i}/{len(tickets)}: \"{ticket['subject']}\"")

        # Step 1: Tag
        tag_result = tag_ticket(client, tagging_system, ticket)
        tag = tag_result["tag"]
        print(f"  -> Tag: {tag}  (confidence: {tag_result['tag_confidence']:.2f})")

        # Step 2: Severity
        sev_result = score_severity(client, severity_system, ticket, tag)
        severity = sev_result["severity"]
        print(f"  -> Severity: {severity}  ({sev_result['rationale'][:60]}...)")

        if severity == 1:
            print(f"  *** CRITICAL TICKET — IMMEDIATE ATTENTION REQUIRED ***")

        # Step 3: Draft response
        draft = draft_response(client, response_system_template, ticket, product_docs, known_issues)
        print(f"  -> Response draft: {len(draft)} chars")

        results.append({
            "ticket_id": ticket["ticket_id"],
            "subject": ticket["subject"],
            "submitted_at": ticket["submitted_at"],
            "tag": tag,
            "tag_confidence": tag_result["tag_confidence"],
            "severity": severity,
            "rationale": sev_result["rationale"],
            "draft_response": draft,
        })

    # Write output CSV
    fieldnames = ["ticket_id", "subject", "submitted_at", "tag", "tag_confidence", "severity", "rationale", "draft_response"]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("-" * 60)
    print(f"triage_output.csv written ({len(results)} rows) -> {OUTPUT_CSV}")

    # Write trend report
    trend_md = build_trend_report(results)
    TREND_MD.write_text(trend_md, encoding="utf-8")
    print(f"trend_report.md written -> {TREND_MD}")


if __name__ == "__main__":
    main()
