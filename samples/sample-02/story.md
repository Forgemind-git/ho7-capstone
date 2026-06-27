# Story — Competitor Intelligence Tracker

## The Problem

Priya is the product marketing lead at a project management SaaS company. Every quarter her CEO asks "what are our competitors doing?" and every quarter Priya spends three days manually reading release notes, taking scattered notes in a Google Doc, and producing an analysis that's already half-stale by the time it ships.

Two competitors release new features every two to three weeks. There's no way to keep up manually.

---

## The Approach

Priya's insight: the analysis doesn't have to be real-time. What it has to be is **grounded** — every claim backed by an actual source — and **structured** — so the team can act on it, not just read it.

She built a three-pass pipeline:

1. **Extraction** — Claude reads the competitor docs and pulls out every feature, pricing tier, and positioning claim as structured JSON. No interpretation yet, just facts with citations.
2. **Gap analysis** — Claude compares the extracted features against Priya's own product summary and labels each as "we have this / we don't / we have something similar."
3. **Report assembly** — Claude turns the gap table into a formatted report with recommended actions.

Total setup time: one afternoon to gather competitor docs and tune the prompts. Runtime: under two minutes per analysis.

---

## Tools Used

| Tool | How |
|------|-----|
| Claude (Anthropic API) | Three-pass analysis: extraction → gaps → report |
| Prompt Library (`01-prompt-library/`) | Separate system prompts for each analysis pass |
| Competitor docs (`02-context-pack/`) | Release notes, feature pages, pricing pages as grounding |
| `gap_analysis.py` | Python script orchestrating all three passes |

---

## The Result

The team now runs the analysis every two weeks on freshly gathered competitor docs. Key outcomes:

- Identified that Competitor A had added a native mobile offline mode — something customers had been requesting for months. This moved the feature up three sprints in the roadmap.
- Spotted a pricing gap: Competitor B's "Starter" tier included features that Acme charges for at the "Pro" level. This fed directly into a packaging discussion.
- The report now takes 90 seconds to generate instead of three days. Priya spends the saved time on strategy rather than research.

The JSON output feeds into a Notion database that tracks which gaps are "open," "in progress," and "closed" over time.

---

## Next Steps

**Month 1:** Automate the doc gathering — write a scraper for each competitor's changelog page so the context pack is always fresh.

**Month 2:** Add a Slack notification that posts the top 3 new gaps every two weeks to `#product-insights`.

**Month 3:** Build a trend view — when did each gap open? When did we close it? How are we tracking relative to competitors over time?

**Longer term:** Feed the gap JSON into a product roadmap tool (Linear, Jira) to automatically create "competitive parity" tickets with context pre-filled.
