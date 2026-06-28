# Prompt: Candidate Scorer

**Purpose:** Score a candidate against the rubric after reading interview notes or a CV.

---

## System prompt

[TODO: Write a system prompt that instructs Claude to score a candidate.
The scoring rubric will be injected as context. Claude should output a score
per rubric dimension plus an overall recommendation (advance/hold/reject).]

---

## Context injection

```
--- SCORING RUBRIC ---
{{scoring_rubric}}
---
```

---

## User message template

```
Candidate: {{candidate_name}}
Role: {{role_title}}

Interview notes / CV:
{{notes}}
```

---

## Expected output format

[TODO: e.g. markdown table with rubric row | score | evidence | then overall recommendation]

---

## Test it

Notes: [TODO]
