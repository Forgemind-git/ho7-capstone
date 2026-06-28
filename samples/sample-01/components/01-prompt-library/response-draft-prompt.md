# Prompt: Response Drafter

**Purpose:** Draft a first-response email to a support ticket, grounded on product docs.

---

## System prompt

[TODO: Write a system prompt that instructs Claude to draft a helpful, empathetic
support reply. It should use the injected product documentation as its source of truth.
Think about: tone (friendly vs formal), length (short acknowledgement vs full answer),
how to cite the docs, what to do when the answer is not in the docs.]

---

## Context injection

Before the user message, inject:

```
--- PRODUCT DOCUMENTATION ---
{{product_docs}}

--- KNOWN ISSUES ---
{{known_issues}}
---
```

---

## User message template

```
Write a first-response draft for this ticket:

Subject: {{subject}}
Body: {{body}}
```

---

## Test it

Notes: [TODO]
