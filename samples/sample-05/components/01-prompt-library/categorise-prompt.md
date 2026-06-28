# Prompt: Transaction Categoriser

**Purpose:** Assign a spending category to each bank transaction.

---

## System prompt

[TODO: Write a system prompt that instructs Claude to categorise transactions.
Think about: what spending categories make sense for your life or business?
(e.g. Rent, Groceries, Dining, Transport, Subscriptions, Shopping, Healthcare, Savings)
How should Claude handle ambiguous merchants? Should it return JSON or a CSV row?]

---

## User message template

```
Categorise these transactions. Return one category per line matching the input order.

Transactions:
{{transactions_csv}}
```

---

## Expected output format

[TODO: e.g. one category label per line, or JSON array, or updated CSV with category column]

---

## My spending categories

[TODO: list the categories you want Claude to use]
1.
2.
3.
...

---

## Test it

Notes: [TODO]
