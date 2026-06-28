# HO7 Sample 02 — Competitor Intelligence Tracker

> **Problem:** the marketing team cannot keep up with what rivals are shipping.

## What you'll build
A competitor-intelligence brief you can refresh on demand — built entirely inside **Claude.ai**, no code, no API key. You load two competitors' materials and your own product summary into a Claude **Project**, then ask Claude to extract their features, compare them against yours, and write a cited gap analysis that tells you exactly where you're behind and what to do about it. It combines three course concepts: **research grounding** (NotebookLM-style), a **grounded assistant** that cites its sources, and a **skill-style automation** that assembles the final report.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login.

1. Open **Claude.ai** → **Projects** → **Create Project**. Call it "Competitor Tracker".
2. Click **Add content / Project knowledge** and upload the three files from `components/02-context-pack/`: `competitor-a-notes.txt`, `competitor-b-notes.txt`, and `our-product-summary.txt`. (Swap in your own rivals' release notes / pricing pages any time.)
3. Open the three prompt files in `components/01-prompt-library/` so you understand the three passes: extract features → analyse gaps → assemble report. You'll run them in order in one chat.
4. Start a new chat **inside the Project** and paste **The example prompt** below. Claude works through all three passes and produces a shareable Markdown brief.
5. Copy the brief into Notion, Confluence, or a Slack post. To refresh next month, just update the competitor files in step 2 and re-run the prompt.

## The example prompt
Copy this into a chat inside your "Competitor Tracker" Project:

```
You are a product strategist doing a competitive gap analysis. Use ONLY the competitor notes and our product summary in this Project's knowledge. Cite the specific source (competitor name + section) for every claim. If something isn't in the materials, mark it "not stated".

Work in three passes and show each:

PASS 1 — EXTRACT: list every notable feature each competitor offers, grouped by category (e.g. collaboration, integrations, pricing, AI). One line each, with the source.

PASS 2 — GAP ANALYSIS: for each competitor feature, mark our status as have / partial / don't-have, add a one-line note, and a priority (high / medium / low) based on how much it affects deals we lose.

PASS 3 — REPORT: write a shareable brief with these sections:
- Executive summary (3 sentences: where we lead, where we lag)
- Feature gap table (feature | competitor | our status | priority)
- Pricing & packaging comparison (2-3 sentences)
- Messaging / positioning opportunities (bullets)
- Quick wins we could ship this quarter (bullets)

Keep it factual and tied to the sources.
```

## Course concepts combined
| # | Concept | Where it appears |
|---|---------|-----------------|
| 1 | **Research grounding** | Competitor materials loaded as Project knowledge in `02-context-pack/` |
| 2 | **Grounded assistant** | Claude cites specific competitor doc sections in every finding |
| 3 | **Skill-style automation** | The 3-pass prompt assembles a finished, shareable report in one run |

See `architecture.md` for the component map and `story.md` for the real-world walkthrough.

## Make it your own
- Replace the competitor `.txt` files with real release notes, changelogs, and pricing pages.
- Keep `our-product-summary.txt` up to date — the analysis is only as good as your own feature list.
- Add a fourth pass: *"Draft 3 sales-battlecard talking points for the highest-priority gap."*

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you later want to regenerate the brief on a schedule, `components/03-automation/gap_analysis.py` shows how. It needs an Anthropic API key, which is **separate** from your Claude.ai subscription (billed per use), so it is optional and not part of the hands-on.
