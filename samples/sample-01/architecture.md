# Architecture — AI Support Triage System

## Overview

Three course modules wired together into a linear pipeline. No custom ML, no database — just prompts, grounding docs, and a Python script that any team member can run.

---

## Component Map

| Component | Module | File |
|-----------|--------|------|
| Tagging prompt | Prompt Library (HO2) | `01-prompt-library/tagging-prompt.md` |
| Severity scoring prompt | Prompt Library (HO2) | `01-prompt-library/severity-prompt.md` |
| Response drafting prompt | Prompt Library (HO2) | `01-prompt-library/response-draft-prompt.md` |
| Product documentation | Context & Grounding (HO4) | `02-context-pack/product-docs.txt` |
| Known issues index | Context & Grounding (HO4) | `02-context-pack/known-issues.txt` |
| Triage pipeline | Automation / Skills (HO5-6) | `03-automation/triage_pipeline.py` |
| Sample input data | — | `03-automation/sample_tickets.csv` |

---

## Data Flow (ASCII)

```
 ┌────────────────────────────────────────────────────────────┐
 │                     INPUT LAYER                            │
 │  sample_tickets.csv                                        │
 │  columns: ticket_id, subject, body, submitted_at           │
 └────────────────────┬───────────────────────────────────────┘
                      │  read row by row
                      ▼
 ┌────────────────────────────────────────────────────────────┐
 │              STEP 1 — TAGGING  (Prompt Library)            │
 │                                                            │
 │  System: tagging-prompt.md                                 │
 │  User:   ticket subject + body                             │
 │  Output: category tag  (e.g. "billing", "authentication")  │
 └────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
 ┌────────────────────────────────────────────────────────────┐
 │          STEP 2 — SEVERITY SCORING  (Prompt Library)       │
 │                                                            │
 │  System: severity-prompt.md                                │
 │  User:   ticket + category tag from Step 1                 │
 │  Output: severity 1–4 + one-line rationale                 │
 └────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
 ┌────────────────────────────────────────────────────────────┐
 │       STEP 3 — GROUNDED RESPONSE DRAFT  (HO4 Context)     │
 │                                                            │
 │  System: response-draft-prompt.md                          │
 │          + injected product-docs.txt                       │
 │          + injected known-issues.txt                       │
 │  User:   ticket body                                       │
 │  Output: 2-3 paragraph response draft with doc citations   │
 └────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
 ┌────────────────────────────────────────────────────────────┐
 │                   OUTPUT LAYER                             │
 │                                                            │
 │  triage_output.csv   — one row per ticket                  │
 │    ticket_id | tag | severity | rationale | draft_response │
 │                                                            │
 │  trend_report.md     — aggregated summary                  │
 │    top 3 tags, avg severity, P1 ticket list, next actions  │
 └────────────────────────────────────────────────────────────┘
```

---

## Key Design Decisions

**Why three separate prompts instead of one big prompt?**
Each prompt is independently testable and improvable. The tagging prompt can be iterated without touching the severity logic. This mirrors the Prompt Library module's "single-responsibility" principle.

**Why inject docs via system prompt (not retrieval)?**
For support use cases, the full product doc is typically under 4,000 tokens. A single context injection is simpler and more reliable than vector search for a first version. Swap to retrieval when docs exceed ~20 pages.

**Why CSV output instead of a dashboard?**
CSV is the universal format — paste into Google Sheets, import into Notion, open in Excel. The trend_report.md is human-readable immediately. Teams can build a richer UI on top once they trust the data.

---

## Extension Points

1. **Slack integration** — post P1 tickets to a #triage-alerts channel via Slack webhook
2. **Zendesk write-back** — use Zendesk API to update tag + priority fields automatically
3. **Weekly digest email** — wrap the trend_report.md in an email template and send via SendGrid
4. **RAG upgrade** — when docs grow, replace the context injection with a Chroma vector store query
