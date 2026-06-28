# HO7 Sample 05 — Personal Finance Copilot

> **Problem:** you never know where your money goes until the month ends.

## What you'll build
A personal finance copilot that reads your bank export, sorts every transaction into a category, answers plain-English questions about your spending, and gives you a clean monthly roll-up — built entirely inside **Claude.ai**, no code, no API key. You paste your bank CSV into a Claude **Project** (or just a chat), set your budget targets once, and then ask things like *"How much did I spend eating out last month?"* and get a sourced answer. It combines three course concepts: a **CSV-ingest prompt**, a **grounded Q&A assistant** over your own data, and an **automation** that produces the monthly summary.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login.

1. Export your transactions from your bank as a CSV (most banks have a "download/export" button). A sample is in `components/03-automation/sample_transactions.csv` if you want to try it first.
2. Open **Claude.ai** → **Projects** → **Create Project**. Call it "Finance Copilot". Upload `components/02-context-pack/financial-rules.txt` (your budget targets) as Project knowledge, and edit it to match your real budget.
3. Start a chat in the Project and paste the **Categorise** prompt below, then paste your CSV rows. Claude returns each transaction with a category. Copy that categorised list back into the chat (or save it as a note) so the rest of the session can use it.
4. **Ask anything:** type natural questions like *"What were my top 3 spending categories?"* or *"Am I on track for my grocery budget?"* Claude answers using your numbers and cites the figures.
5. **Monthly roll-up:** ask *"Give me a monthly summary: total spent, spend by category, biggest non-essential expense, and how I did against each budget target."* That's your report.

Your data stays in your own Claude chat — nothing is sent to a third-party finance app.

## The example prompt
Step 1 — categorise. Paste this into a chat inside your "Finance Copilot" Project, then paste your CSV rows underneath:

```
You are my personal finance assistant. Categorise each bank transaction below using ONLY these categories: groceries, restaurants, transport, utilities, subscriptions, rent-mortgage, shopping, health, entertainment, travel, education, savings-investment, insurance, income, other.

For each transaction return a row: date | description | amount | category | essential? (yes/no). If a description is ambiguous, pick the most likely category and add "(uncertain)".

Transactions:
SAINSBURYS, -28.45, 2024-10-03
NETFLIX, -15.99, 2024-10-05
THE BREAKFAST CLUB, -34.20, 2024-10-06
UBER, -12.40, 2024-10-07
SALARY ACME LTD, 2400.00, 2024-10-25
```

Then ask questions in plain English, for example:

```
Using the categorised transactions above and my budget rules in this Project, answer: How much did I spend on restaurants this month, how does that compare to my eating-out budget, and what's my single biggest non-essential expense? Cite the figures.
```

## Course concepts combined
| # | Concept | Where it appears |
|---|---------|-----------------|
| 1 | **CSV-ingest prompt** | The categorise prompt in `01-prompt-library/categorise-prompt.md` |
| 2 | **Grounded Q&A** | Claude answers from your categorised data + `02-context-pack/financial-rules.txt` |
| 3 | **Automation** | The monthly roll-up prompt turns the data into a shareable summary |

See `architecture.md` for the component map and `story.md` for the real-world walkthrough.

## Make it your own
- Edit `financial-rules.txt` with your real budget targets and currency.
- Add categories that fit your life (e.g. `childcare`, `pets`, `hobbies`).
- Ask for a savings nudge: *"Suggest one realistic change that would save me £50 next month, based on my actual spend."*

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you later want to categorise and report on large exports automatically, `components/03-automation/` has `categorise.py`, `ask.py`, and `monthly_rollup.py`. They need an Anthropic API key, which is **separate** from your Claude.ai subscription (billed per use), so they are optional and not part of the hands-on.
