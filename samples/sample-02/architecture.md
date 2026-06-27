# Architecture — Competitor Intelligence Tracker

## Overview

Three passes of grounded analysis over competitor materials, each producing structured output that feeds into a final compiled report. The grounding context is the key differentiator — without it, Claude produces generic analysis; with it, findings are specific and citable.

---

## Component Map

| Component | Module | File |
|-----------|--------|------|
| Research extraction prompt | Prompt Library (HO2) | `01-prompt-library/research-extraction-prompt.md` |
| Gap analysis prompt | Prompt Library (HO2) | `01-prompt-library/gap-analysis-prompt.md` |
| Report assembly prompt | Prompt Library (HO2) | `01-prompt-library/report-assembly-prompt.md` |
| Competitor A materials | Context & Grounding (HO4) | `02-context-pack/competitor-a-notes.txt` |
| Competitor B materials | Context & Grounding (HO4) | `02-context-pack/competitor-b-notes.txt` |
| Our product summary | Context & Grounding (HO4) | `02-context-pack/our-product-summary.txt` |
| Gap analysis script | Automation / Skills (HO5-6) | `03-automation/gap_analysis.py` |

---

## Data Flow (ASCII)

```
 ┌────────────────────────────────────────────────────────────────┐
 │                    GROUNDING LAYER (HO4)                       │
 │                                                                │
 │  competitor-a-notes.txt    competitor-b-notes.txt              │
 │  (release notes, feature   (feature pages, pricing)           │
 │   announcements, pricing)                                      │
 │                                                                │
 │  our-product-summary.txt                                       │
 │  (our features, pricing, positioning)                          │
 └─────────────────────────┬──────────────────────────────────────┘
                           │  all injected into system context
                           ▼
 ┌────────────────────────────────────────────────────────────────┐
 │         PASS 1 — FEATURE EXTRACTION  (Prompt Library)          │
 │                                                                │
 │  System: research-extraction-prompt.md + all context           │
 │  Output: JSON list of competitor features with source cite     │
 └─────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
 ┌────────────────────────────────────────────────────────────────┐
 │         PASS 2 — GAP ANALYSIS  (Prompt Library + HO4)          │
 │                                                                │
 │  System: gap-analysis-prompt.md                                │
 │  User:   extracted feature list + our product summary          │
 │  Output: JSON gap table (have/don't have/partial)              │
 └─────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
 ┌────────────────────────────────────────────────────────────────┐
 │         PASS 3 — REPORT ASSEMBLY  (Automation)                 │
 │                                                                │
 │  System: report-assembly-prompt.md                             │
 │  User:   gap table + pricing diff + positioning notes          │
 │  Output: Markdown report with citations                        │
 └─────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
 ┌────────────────────────────────────────────────────────────────┐
 │                     OUTPUT LAYER                               │
 │                                                                │
 │  gap_report.md    — human-readable Markdown (share in Notion)  │
 │  gap_report.json  — machine-readable (feed into dashboards)    │
 └────────────────────────────────────────────────────────────────┘
```

---

## Key Design Decisions

**Why three passes instead of one big prompt?**
Extraction, analysis, and report assembly are distinct cognitive tasks. Splitting them produces more reliable output and makes it easy to inspect intermediate results. If the gap table looks wrong, you can fix Pass 2 without touching Pass 3.

**Why inject full competitor docs instead of using a search tool?**
Competitor materials are typically short (1,000–5,000 tokens each). Full injection ensures Claude has everything needed to make cross-document comparisons without retrieval latency or missed chunks.

**Why output both Markdown and JSON?**
Markdown goes directly to humans (Notion, Confluence, Slack). JSON feeds machines — you can pipe it into a spreadsheet formula, a dashboard widget, or a Zapier automation to update a competitor tracking sheet.

---

## Extension Points

1. **Automated scraping** — use `requests` + `BeautifulSoup` to scrape competitor changelog pages weekly, feed fresh content into the context pack
2. **Notion integration** — POST the Markdown report to a Notion database via Notion API
3. **Slack digest** — summarise the top 3 gaps into a Slack message sent to `#product-insights`
4. **Version history** — store each `gap_report.json` with a date stamp to track how gaps open and close over time
