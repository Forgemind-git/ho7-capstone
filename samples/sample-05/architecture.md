# Architecture — Personal Finance Copilot

## Overview

Three independent scripts that share the same data file (`categorised.csv`). Run them in sequence or independently after the first run. All processing happens locally — your financial data never leaves your machine except for the API call to Claude.

---

## Component Map

| Component | Module | File |
|-----------|--------|------|
| Transaction categoriser prompt | Prompt Library (HO2) | `01-prompt-library/categorise-prompt.md` |
| Grounded Q&A prompt | Prompt Library (HO2) | `01-prompt-library/qa-prompt.md` |
| Monthly roll-up prompt | Prompt Library (HO2) | `01-prompt-library/rollup-prompt.md` |
| Financial rules / budget targets | Context & Grounding (HO4) | `02-context-pack/financial-rules.txt` |
| Categoriser | Automation (HO5) | `03-automation/categorise.py` |
| Interactive Q&A | Automation (HO5) | `03-automation/ask.py` |
| Monthly roll-up | Automation (HO5-6) | `03-automation/monthly_rollup.py` |

---

## Data Flow (ASCII)

```
 ┌────────────────────────────────────────────────────────────┐
 │                     INPUT                                  │
 │  bank_export.csv  (downloaded from your bank)              │
 │  columns: date, description, amount, balance               │
 └──────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
 ┌────────────────────────────────────────────────────────────┐
 │         STEP 1 — CATEGORISE  (categorise.py)               │
 │                                                            │
 │  For each row:                                             │
 │    System: categorise-prompt.md                            │
 │    User:   description + amount                            │
 │    Output: category + subcategory + is_essential flag      │
 │                                                            │
 │  Writes: categorised.csv                                   │
 │  (original rows + category, subcategory, is_essential cols)│
 └──────────────────────────┬─────────────────────────────────┘
                            │  categorised.csv
              ┌─────────────┴──────────────┐
              ▼                            ▼
 ┌────────────────────────┐  ┌─────────────────────────────────┐
 │  STEP 2 — Q&A          │  │  STEP 3 — MONTHLY ROLL-UP       │
 │  (ask.py)              │  │  (monthly_rollup.py)            │
 │                        │  │                                 │
 │  System: qa-prompt.md  │  │  System: rollup-prompt.md       │
 │          + financial-  │  │          + financial-rules.txt  │
 │            rules.txt   │  │  User:   full categorised.csv   │
 │  User:   your question │  │          + spending summary     │
 │          + CSV data    │  │  Output: monthly_report.md      │
 │  Output: natural       │  │                                 │
 │          language      │  └─────────────────────────────────┘
 │          answer        │
 └────────────────────────┘
```

---

## Privacy Architecture

Your financial data is handled as follows:

1. `categorise.py` sends transaction descriptions and amounts to Claude API. No account numbers, no names, no bank details beyond the description field.
2. `ask.py` sends the full categorised CSV to Claude as context. If privacy is a concern, remove the description column after categorisation — the amounts and categories are sufficient for Q&A.
3. `monthly_rollup.py` sends aggregated totals (not individual transactions) to Claude.
4. All output files are written locally. Nothing is uploaded to a server.

---

## Key Design Decisions

**Why categorise row-by-row instead of sending the whole CSV?**
Row-by-row categorisation is more accurate — Claude can give full attention to each transaction. It's also safer — if categorisation fails on one row, the rest succeed. The cost is more API calls; for 30-50 transactions/month this is negligible.

**Why use a financial-rules.txt grounding file for Q&A?**
Without knowing your budget targets, Claude can only describe what you spent. With `financial-rules.txt`, it can tell you whether you're over or under budget — the question shifts from "what happened?" to "are you on track?"

**Why a separate roll-up script instead of Q&A?**
The roll-up is a document for record-keeping; Q&A is interactive. Separating them means the roll-up can be automated (e.g., via a cron job) while Q&A remains on-demand.

---

## Extension Points

1. **Multiple account support** — merge CSVs from multiple banks/cards before categorising
2. **Historical comparison** — store monthly reports and ask "how does October compare to September?"
3. **Budget alert automation** — run categorise.py weekly, check totals against budget rules, send a Slack message if you're over budget in any category
4. **Email delivery** — wrap monthly_report.md in an HTML email template and send via Gmail API or SendGrid
