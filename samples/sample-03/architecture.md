# Architecture — Hiring Co-Pilot

## Overview

The core insight: hiring inconsistency comes from interviewers using different mental models. This system gives everyone the same grounded rubric — derived from the real role description and company values — then structures notes so comparison is apples-to-apples.

---

## Component Map

| Component | Module | File |
|-----------|--------|------|
| Question generator prompt | Prompt Library (HO2) | `01-prompt-library/screening-questions-prompt.md` |
| Candidate scoring prompt | Prompt Library (HO2) | `01-prompt-library/score-candidate-prompt.md` |
| Note compiler prompt | Prompt Library (HO2) | `01-prompt-library/note-compiler-prompt.md` |
| Role description | Context & Grounding (HO4) | `02-context-pack/role-description.txt` |
| Company values | Context & Grounding (HO4) | `02-context-pack/company-values.txt` |
| Scoring rubric | Context & Grounding (HO4) | `02-context-pack/scoring-rubric.txt` |
| Question generator | Automation (HO5) | `03-automation/generate_questions.py` |
| Candidate scorer | Automation (HO5) | `03-automation/score_candidates.py` |
| Comparison compiler | Automation (HO5-6) | `03-automation/compile_candidates.py` |

---

## Data Flow (ASCII)

```
 ┌────────────────────────────────────────────────────────────┐
 │              GROUNDING LAYER (HO4)                         │
 │                                                            │
 │  role-description.txt   company-values.txt                 │
 │  scoring-rubric.txt                                        │
 └──────────────────────┬─────────────────────────────────────┘
                        │  injected into every prompt
                        ▼
 ┌────────────────────────────────────────────────────────────┐
 │           STEP 1 — QUESTION GENERATION                     │
 │                                                            │
 │  generate_questions.py calls screening-questions-prompt    │
 │  Output: 20 structured interview questions per role        │
 │  Used by: all interviewers (consistent starting point)     │
 └──────────────────────┬─────────────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
    Candidate 1    Candidate 2    Candidate 3
    transcript     transcript     transcript
    (.txt files)   (.txt files)   (.txt files)
         │              │              │
         └──────────────┼──────────────┘
                        │
                        ▼
 ┌────────────────────────────────────────────────────────────┐
 │           STEP 2 — SCORING  (score_candidates.py)          │
 │                                                            │
 │  score-candidate-prompt.md + scoring-rubric.txt            │
 │  Input:  transcript text                                   │
 │  Output: JSON scores per dimension + overall + notes       │
 └──────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
 ┌────────────────────────────────────────────────────────────┐
 │         STEP 3 — COMPILE  (compile_candidates.py)          │
 │                                                            │
 │  note-compiler-prompt.md                                   │
 │  Input:  all candidate score JSONs                         │
 │  Output: candidate_comparison.md                           │
 └──────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
              candidate_comparison.md
              (share with hiring team)
```

---

## Key Design Decisions

**Why generate questions from role + values, not from a fixed bank?**
A fixed question bank goes stale and doesn't adapt to different roles. Grounding the question generator in the actual JD and values means questions are always role-relevant and culture-aligned.

**Why score transcripts rather than just summarise them?**
Summaries are still subjective. Numeric scores against defined dimensions let the hiring panel compare candidates on the same scale, catch biases, and justify decisions to candidates.

**Why a separate compile step?**
The comparison report is a team deliverable. Separating it means the pipeline can be run incrementally — score candidate 1 on Tuesday, candidate 2 on Thursday, compile on Friday.

---

## Extension Points

1. **ATS integration** — read transcripts from Greenhouse/Lever via API instead of text files
2. **Interviewer guidance** — generate a pre-call prep doc for each interviewer with role context + suggested questions
3. **Bias check** — add a fourth prompt that reviews the scoring notes for demographic language
4. **Offer modelling** — feed candidate scores into a compensation benchmarking prompt
