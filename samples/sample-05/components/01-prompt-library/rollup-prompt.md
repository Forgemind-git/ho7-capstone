# Prompt: Monthly Roll-Up

**Purpose:** Generate a structured monthly spending summary with insights and a chart-ready data block.

---

## System prompt

[TODO: Write a system prompt that instructs Claude to generate a monthly summary.
It should include: total spend by category, top 3 insights, one saving opportunity,
and a JSON data block that can be used to render a bar or pie chart in an Artifact.]

---

## Context injection

```
--- MY TRANSACTIONS ---
{{categorised_csv}}
---
```

---

## User message template

```
Generate my monthly spending summary for {{month_year}}.
Include a JSON data block for chart rendering.
```

---

## Expected output format

[TODO: e.g. markdown summary + ```json chart-data block at the end]

---

## Test it

Notes: [TODO]
