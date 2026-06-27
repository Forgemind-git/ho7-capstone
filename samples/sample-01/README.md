# Sample 01 — AI Support Triage System

> **Problem:** Support team buried in tickets with no trends view

A complete AI-assisted support triage pipeline that automatically tags incoming tickets, assigns severity levels, answers common questions using product documentation as grounding context, and surfaces weekly trend reports — all without building a single ML model.

---

## Course Concepts Combined

| # | Concept | Where It Appears |
|---|---------|-----------------|
| 1 | **Prompt Library** | Tagging prompt + severity-scoring prompt in `01-prompt-library/` |
| 2 | **Grounded Assistant** | Claude reads `02-context-pack/product-docs.txt` before answering; citations included |
| 3 | **No-Code Automation** | Python script processes a CSV of tickets and produces a triage report + trend CSV |

---

## Architecture

```
Incoming Tickets (CSV)
        │
        ▼
┌──────────────────┐
│  Triage Script   │  ← 03-automation/triage_pipeline.py
│  (Python)        │
└────────┬─────────┘
         │  calls prompts from 01-prompt-library/
         │  grounded by 02-context-pack/product-docs.txt
         ▼
┌──────────────────────────────┐
│  Per-ticket output           │
│  • category tag              │
│  • severity (1–4)            │
│  • suggested response draft  │
└────────────┬─────────────────┘
             ▼
    triage_output.csv + trend_report.md
```

---

## How to Reproduce

### Prerequisites

```bash
pip install anthropic python-dotenv
export ANTHROPIC_API_KEY=sk-ant-...
```

### Run the pipeline

```bash
cd samples/sample-01/components/03-automation/
python triage_pipeline.py
```

The script reads `sample_tickets.csv` (bundled), processes each ticket through the prompt library, grounds answers in the product docs, then writes:
- `triage_output.csv` — every ticket with tag + severity + response draft
- `trend_report.md` — top categories, avg severity, recommended actions

### Customise

1. Replace `02-context-pack/product-docs.txt` with your own product documentation.
2. Edit `01-prompt-library/tagging-prompt.md` to match your category taxonomy.
3. Swap the CSV input for a Zendesk/Freshdesk export.

---

## Expected Output

```
Processing ticket 1/8: "Cannot log in after password reset"
  → Tag: authentication  Severity: 2
Processing ticket 2/8: "App crashes on iOS 17"
  → Tag: mobile-bug  Severity: 1
...
triage_output.csv written (8 rows)
trend_report.md written
```
