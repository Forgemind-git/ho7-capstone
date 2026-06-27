# Sample 03 — Hiring Co-Pilot

> **Problem:** Inconsistent screening slows hiring

A structured AI hiring assistant that gives every interviewer the same rubric, generates consistent screening notes from raw interview transcripts, and compiles a candidate comparison report — so hiring decisions are faster and fairer.

---

## Course Concepts Combined

| # | Concept | Where It Appears |
|---|---------|-----------------|
| 1 | **Grounded Assistant** | Claude grounded in role description + company values before generating questions |
| 2 | **Screening Prompt Library** | Consistent rubric prompts used by every interviewer on every call |
| 3 | **Automation** | Python script compiles interview notes across candidates into a comparison report |

---

## Architecture

```
Role Description + Company Values
           │
           ▼
┌──────────────────────────────┐
│  02-context-pack/            │
│  role-description.txt        │
│  company-values.txt          │
│  scoring-rubric.txt          │
└──────────────┬───────────────┘
               │  grounding context
               ▼
┌──────────────────────────────┐
│  01-prompt-library/          │  used by interviewers
│  screening-questions-prompt  │  to generate questions
│  score-candidate-prompt      │  to score transcripts
│  note-compiler-prompt        │  to structure notes
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  03-automation/              │
│  compile_candidates.py       │  reads per-candidate notes,
│                              │  generates comparison report
└──────────────┬───────────────┘
               ▼
    candidate_comparison.md
```

---

## How to Reproduce

### Prerequisites

```bash
pip install anthropic python-dotenv
export ANTHROPIC_API_KEY=sk-ant-...
```

### Step 1: Generate interview questions (interactive)

```bash
cd samples/sample-03/components/03-automation/
python generate_questions.py
```

### Step 2: Score candidate transcripts

```bash
python score_candidates.py
```

### Step 3: Compile comparison report

```bash
python compile_candidates.py
```

Each step reads from `02-context-pack/` for grounding and uses prompts from `01-prompt-library/`. Sample candidate transcripts are included in `03-automation/sample_transcripts/`.

---

## Expected Output

```
Generating interview questions for: Senior Product Designer
  Based on role + 4 company values...
  20 questions generated (5 per value + 5 role-specific)

Scoring candidate transcripts...
  Candidate 1 (Sarah M.): Overall 4.2/5 — Strong on collaboration, needs growth on data
  Candidate 2 (James T.): Overall 3.6/5 — Technical depth strong, culture fit uncertain
  Candidate 3 (Anika R.): Overall 4.7/5 — Exceptional across all dimensions

candidate_comparison.md written
```
