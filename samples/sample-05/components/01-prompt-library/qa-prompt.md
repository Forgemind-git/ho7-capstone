# Prompt: Finance Q&A

**Purpose:** Answer natural-language questions about your spending data.

---

## System prompt

[TODO: Write a system prompt that instructs Claude to act as a personal finance analyst.
The full categorised transaction data will be injected as context.
Think about: what questions do you want to ask? (biggest categories, month-on-month changes,
"could I afford X?", "what if I cut Y?"). How should Claude handle missing data?]

---

## Context injection

```
--- MY TRANSACTIONS (categorised) ---
{{categorised_csv}}
--- END ---
```

---

## User message template

```
{{your_question}}
```

---

## Questions to try

[TODO: write 5-10 questions you actually want answered about your own spending]
1.
2.
3.
...

---

## Test it

Notes: [TODO]
