# Prompt: Severity Scorer

**Purpose:** Score a ticket from 1 (critical) to 4 (low) based on impact and urgency.

---

## System prompt

[TODO: Write a system prompt that instructs Claude to assess ticket severity.
Think about: what makes a ticket P1 vs P4 for your product? How should Claude
weigh "many users affected" vs "one user, data loss risk"? Should it return a
number only, or a number plus a one-line rationale?]

---

## User message template

```
Ticket subject: {{subject}}
Category tag: {{tag}}

Ticket body:
{{body}}
```

---

## Expected output format

[TODO: e.g. "Severity: 2\nRationale: affects login flow for all users"]

---

## Test it

Notes: [TODO]
