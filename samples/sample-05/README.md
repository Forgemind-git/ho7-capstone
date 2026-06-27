# Sample 05 — Personal Finance Copilot

> **Problem:** No visibility into spending until month end

A personal finance AI that ingests your bank CSV export, categorises every transaction using Claude, lets you ask natural-language questions about your spending, and emails you a clean monthly roll-up — all running locally with no third-party finance app needed.

---

## Course Concepts Combined

| # | Concept | Where It Appears |
|---|---------|-----------------|
| 1 | **CSV Ingest + Prompt** | Reads bank export CSV, categorises each transaction with a structured prompt |
| 2 | **Grounded Q&A** | Ask natural-language questions about your own data; Claude answers from the categorised CSV |
| 3 | **Automation** | Monthly roll-up script generates a summary report and optional email digest |

---

## Architecture

```
Bank export (CSV)
       │
       ▼
┌──────────────────────────────┐
│  categorise.py               │  Step 1: tag every transaction
│  + 01-prompt-library/        │
│    categorise-prompt.md      │
└──────────────┬───────────────┘
               │  writes categorised.csv
               ▼
┌──────────────────────────────┐
│  ask.py                      │  Step 2: Q&A over your data
│  + 01-prompt-library/        │
│    qa-prompt.md              │
│  + 02-context-pack/          │
│    financial-rules.txt       │  (your budget targets)
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  monthly_rollup.py           │  Step 3: monthly summary
│  + 01-prompt-library/        │
│    rollup-prompt.md          │
└──────────────┬───────────────┘
               ▼
    monthly_report.md
```

---

## How to Reproduce

### Prerequisites

```bash
pip install anthropic python-dotenv
export ANTHROPIC_API_KEY=sk-ant-...
```

### Step 1: Categorise transactions

```bash
cd samples/sample-05/components/03-automation/
python categorise.py --input sample_transactions.csv
```

### Step 2: Ask questions about your spending

```bash
python ask.py
# Then type questions like:
# > How much did I spend on restaurants last month?
# > What were my top 3 spending categories?
# > Am I on track for my grocery budget?
```

### Step 3: Generate monthly roll-up

```bash
python monthly_rollup.py
```

---

## Expected Output (Step 1)

```
Categorising 23 transactions...
  Row 1: SAINSBURYS 28.45 -> groceries (confidence: 0.98)
  Row 2: NETFLIX 15.99 -> subscriptions (confidence: 0.99)
  Row 3: THE BREAKFAST CLUB 34.20 -> restaurants (confidence: 0.95)
  ...
categorised.csv written (23 rows)
```

## Expected Output (Step 2)

```
Finance Copilot — Q&A Mode
Your data: 23 transactions, Oct 2024
Type 'exit' to quit.

> How much did I spend eating out?
Based on your October transactions, you spent £178.40 on restaurants across 5 visits.

> What's my biggest non-essential expense?
Your biggest non-essential category is entertainment at £124.00 (3 transactions).
```
