# Story — Hiring Co-Pilot

## The Problem

Marcus runs talent acquisition at a 60-person tech company. They hired four people in the last quarter. Three are performing well. One is not — and in the debrief it became clear that the interviewers had used completely different mental models: one focused on cultural fit, one on technical depth, one on "gut feel."

There was no shared rubric. No structured notes. Just four people with four different impressions voting in a room.

---

## The Approach

Marcus didn't need a new ATS or an expensive hiring platform. He needed three things:

1. **A consistent set of interview questions** — generated from the real job description and company values, not a generic question bank.
2. **A structured scoring rubric** — so every interviewer scores the same dimensions the same way.
3. **An automated compiler** — that takes raw notes from each interviewer and produces a comparison document the panel can actually debate.

The prompt library handles consistency. The grounding context ensures the questions and scores are role-specific. The Python script handles the assembly.

---

## Tools Used

| Tool | How |
|------|-----|
| Claude (Anthropic API) | Generates questions, scores transcripts, compiles comparison |
| Prompt Library (`01-prompt-library/`) | Three prompts: question generator, scorer, compiler |
| Role + values docs (`02-context-pack/`) | Grounds all prompts in real company context |
| `generate_questions.py` | Creates the interview question guide |
| `score_candidates.py` | Scores each candidate transcript against the rubric |
| `compile_candidates.py` | Assembles the final comparison report |

---

## The Result

The next hiring cycle used the system for three candidates for a Senior Product Designer role.

- Questions were consistent across all three interviews (same five themes, adapted to each candidate's background)
- Scores came back with numeric ratings per dimension plus evidence quotes from the transcript
- The comparison report showed clearly that one candidate was strong on craft but weak on collaboration signals, while another was the reverse — a nuanced difference that would have been invisible in the old "gut feel" process

The hiring decision took 20 minutes in the debrief instead of 90. The panel had something concrete to discuss.

---

## Next Steps

**Month 1:** Connect to the Lever ATS API to pull transcripts automatically instead of pasting text files.

**Month 2:** Add a bias-check prompt that reviews scoring notes for language that correlates with demographic bias.

**Month 3:** Build a question bank that grows over time — store generated questions and good follow-ups in a shared Notion database.

**Longer term:** Track hired candidates' 90-day performance against their interview scores to calibrate the rubric over time.
