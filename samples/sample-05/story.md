# Story — Personal Finance Copilot

## The Problem

Every month at about day 28, Tobi has the same moment of low-grade anxiety: how much did I actually spend this month? The bank app shows a number but not a breakdown. The credit card statement arrives as a PDF. There's a spreadsheet somewhere but it hasn't been updated since April.

By the time Tobi has full visibility, the month is over. There's nothing to do with the information except feel vaguely guilty about the number of restaurant receipts.

---

## The Approach

Tobi didn't want to use a third-party finance app — sharing bank credentials with a startup felt risky. What Tobi wanted was something simple, local, and under their own control.

Three scripts. That's it.

1. **Categorise** — download the monthly CSV from the bank (every bank offers this), run it through Claude to tag each transaction with a category. Takes 30 seconds.
2. **Ask** — ask natural-language questions about the categorised data. "Did I stay under my restaurant budget?" "What was my biggest unnecessary purchase?" "How much did I spend on subscriptions?"
3. **Roll-up** — at month end, generate a clean summary report.

The key insight: the hard part isn't writing code — it's the categorisation. Bank descriptions like "SQ *COFFEE SHOP 2847" are impossible to categorise manually at scale. Claude handles this effortlessly.

---

## Tools Used

| Tool | How |
|------|-----|
| Claude (Anthropic API) | Transaction categorisation, Q&A grounded in CSV data, roll-up generation |
| Prompt Library (`01-prompt-library/`) | Separate prompts for categorisation, Q&A, and roll-up |
| Financial rules (`02-context-pack/financial-rules.txt`) | Personal budget targets that ground the Q&A answers |
| `categorise.py` | Tags each bank transaction with a category |
| `ask.py` | Interactive Q&A mode over categorised data |
| `monthly_rollup.py` | Generates the monthly report |

---

## The Result

First run on October's bank statement (47 transactions):

- Categorisation: 45/47 correctly tagged (2 manual corrections needed — an obscure merchant description)
- Q&A revealed: groceries 18% over budget, restaurants exactly on track, two forgotten subscriptions adding up to £42/month
- Monthly report generated in 8 seconds, saved as a Markdown file

The forgotten subscriptions alone saved £504/year once cancelled.

Tobi now runs the categoriser weekly on Sunday evening. The Q&A takes 5 minutes. By mid-month, Tobi knows exactly where the budget stands — not at the end, when it's too late to adjust.

---

## Next Steps

**Week 2:** Run the categoriser weekly (not monthly) so course-corrections happen in real time.

**Month 2:** Add a budget alert — if any category exceeds 80% of the monthly target before the 20th of the month, send a reminder.

**Month 3:** Store monthly roll-ups and ask year-over-year comparison questions ("Am I spending more on restaurants than last year?").

**Longer term:** Build a simple web UI — a local Flask app — so other household members can view the dashboard without running Python scripts.
