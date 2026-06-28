# HO7 Sample 03 — Hiring Co-Pilot

> **Problem:** hiring is slow and unfair because every recruiter screens differently.

## What you'll build
A hiring co-pilot that gives every interviewer the same questions, the same rubric, and the same way of scoring — built entirely inside **Claude.ai**, no code, no API key. You load the role description, company values, and scoring rubric into a Claude **Project**, then Claude generates a consistent interview guide, scores each candidate's transcript against the rubric, and compiles a side-by-side comparison so the decision is fast and fair. It combines three course concepts: a **grounded assistant**, a **screening prompt library**, and an **automation** that compiles notes across candidates.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login.

1. Open **Claude.ai** → **Projects** → **Create Project**. Call it "Hiring Co-Pilot".
2. Click **Add content / Project knowledge** and upload the three files from `components/02-context-pack/`: `role-description.txt`, `company-values.txt`, and `scoring-rubric.txt`.
3. Open the three prompt files in `components/01-prompt-library/` (`screening-questions-prompt.md`, `score-candidate-prompt.md`, `note-compiler-prompt.md`) — these are the three steps you'll run.
4. **Before interviews:** start a chat in the Project and paste the **Generate questions** prompt below. You get one consistent interview guide every interviewer uses.
5. **After each interview:** paste the **Score a candidate** prompt and the interview notes/transcript (sample transcripts are in `components/03-automation/sample_transcripts/`). Claude scores each rubric dimension 1–5 with evidence.
6. **To decide:** paste all the candidate scores and ask Claude to compile the comparison (the **Compile comparison** prompt). You get a ranked side-by-side table.

## The example prompt
Step 1 — generate the interview guide. Paste this into a chat inside your "Hiring Co-Pilot" Project:

```
You are an expert hiring advisor. Use ONLY the role description, company values, and scoring rubric in this Project's knowledge.

Generate a structured interview guide for this role. The questions must:
- map to each rubric dimension and each company value
- be open-ended and behavioural ("Tell me about a time...") or situational ("How would you approach...")
- never be answerable yes/no

For every question, give:
- the rubric dimension / value it tests
- "what to listen for" (2-3 signals of a strong answer)
- "red flags" (1-2 signals of a weak answer)

Group the questions by rubric dimension so every interviewer covers the same ground in the same order.
```

Then, after an interview, score the candidate with:

```
Using the scoring rubric in this Project, score the candidate below. For each rubric dimension give a score 1-5, one sentence of evidence quoted or paraphrased from the transcript, and end with an overall score and a hire / no-hire / more-info recommendation. Be consistent — apply the same bar to every candidate.

Transcript:
[paste the interview transcript here]
```

## Course concepts combined
| # | Concept | Where it appears |
|---|---------|-----------------|
| 1 | **Grounded assistant** | Questions + scoring grounded in role, values, and rubric from `02-context-pack/` |
| 2 | **Screening prompt library** | Reusable question / score / compile prompts in `01-prompt-library/` |
| 3 | **Automation** | The compile step rolls per-candidate scores into one ranked comparison |

See `architecture.md` for the component map and `story.md` for the real-world walkthrough.

## Make it your own
- Replace the three context files with your own role, values, and rubric.
- Tighten the rubric wording until two interviewers scoring the same transcript land within one point.
- Add a bias check: *"Flag any score that relies on background, accent, or school rather than the rubric."*

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you later want to score a folder of transcripts in one batch, `components/03-automation/` has `generate_questions.py`, `score_candidates.py`, and `compile_candidates.py`. They need an Anthropic API key, which is **separate** from your Claude.ai subscription (billed per use), so they are optional and not part of the hands-on.
