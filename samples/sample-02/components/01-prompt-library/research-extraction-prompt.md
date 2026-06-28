# Prompt: Competitor Research Extractor

**Purpose:** Extract structured intelligence from raw competitor content (website copy, release notes, press releases).

---

## System prompt

[TODO: Write a system prompt that instructs Claude to read competitor content and extract:
- New features or product changes
- Pricing changes
- Target customer messaging
- Claims made vs your product (implicit or explicit)

Think about: what output format makes it easy to compare across competitors?
JSON? A bullet list? A markdown table?]

---

## User message template

```
Competitor: {{competitor_name}}
Source URL: {{url}}
Content scraped on: {{date}}

--- CONTENT ---
{{raw_content}}
---
```

---

## Expected output format

[TODO]

---

## Test it

Notes: [TODO]
