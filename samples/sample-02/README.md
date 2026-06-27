# Sample 02 — Competitor Intelligence Tracker

> **Problem:** Marketing team cannot keep up with competitor releases

A structured competitor intelligence workflow that turns raw competitor materials (release notes, feature pages, pricing pages) into a grounded gap analysis with citations, then automatically generates a formatted report your team can share in Slack or send as a PDF.

---

## Course Concepts Combined

| # | Concept | Where It Appears |
|---|---------|-----------------|
| 1 | **NotebookLM Research** | Competitor materials loaded into `02-context-pack/` as grounding sources |
| 2 | **Grounded Assistant** | Claude produces gap analysis citing specific competitor doc sections |
| 3 | **Skill-Driven Automation** | Python script orchestrates ingestion → analysis → report generation |

---

## Architecture

```
Competitor Materials (release notes, feature pages, pricing)
           │
           ▼
┌──────────────────────────────┐
│  02-context-pack/            │
│  competitor-A-notes.txt      │
│  competitor-B-notes.txt      │
│  our-product-summary.txt     │
└──────────────┬───────────────┘
               │  injected as grounding context
               ▼
┌──────────────────────────────┐
│  03-automation/              │
│  gap_analysis.py             │  ← orchestration script
└──────────┬───────────────────┘
           │  uses prompts from 01-prompt-library/
           ▼
┌──────────────────────────────┐
│  Gap Analysis Output         │
│  • feature gap table         │
│  • pricing comparison        │
│  • messaging opportunities   │
│  • recommended actions       │
└──────────┬───────────────────┘
           ▼
    gap_report.md + gap_report.json
```

---

## How to Reproduce

### Prerequisites

```bash
pip install anthropic python-dotenv
export ANTHROPIC_API_KEY=sk-ant-...
```

### Run the analysis

```bash
cd samples/sample-02/components/03-automation/
python gap_analysis.py
```

The script reads competitor materials from `02-context-pack/`, runs three analysis passes (feature gaps, pricing, messaging), and writes:
- `gap_report.md` — formatted Markdown report ready to paste into Notion/Confluence
- `gap_report.json` — structured data for downstream automation

### Customise

1. Replace the `.txt` files in `02-context-pack/` with real competitor release notes.
2. Update `our-product-summary.txt` with your current feature list.
3. Edit `01-prompt-library/gap-analysis-prompt.md` to adjust the analysis framework.

---

## Expected Output

```
Loading competitor materials...
  Competitor A: acme-corp-notes.txt (4,312 chars)
  Competitor B: beta-tools-notes.txt (3,891 chars)
  Our product: our-product-summary.txt (2,104 chars)

Running analysis pass 1/3: Feature gap identification...
Running analysis pass 2/3: Pricing & packaging comparison...
Running analysis pass 3/3: Messaging & positioning opportunities...

gap_report.md written (2,847 chars)
gap_report.json written (15 findings)
```
