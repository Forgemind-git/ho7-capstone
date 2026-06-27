# Story — AI Support Triage System

## The Problem

Anika manages a five-person support team for a B2B SaaS product. By Tuesday each week her team is already behind. Tickets pile up, high-severity bugs get the same queue position as billing questions, and every sprint planning meeting starts with "we have no idea what the top issues actually are this week."

The team tried tagging tickets manually. It lasted two weeks before people stopped doing it consistently.

---

## The Approach

Instead of building a custom classifier or buying an expensive tool, Anika's team used three things they already had access to:

1. **A Claude prompt library** with a tagging prompt and a severity rubric — defined once, used every time.
2. **Their existing product documentation** loaded as grounding context, so the AI could draft accurate responses without hallucinating feature names.
3. **A short Python script** that wired everything together: read tickets from a CSV export, run each through the prompts, write the results back.

Total build time: one afternoon. Total new infrastructure: zero.

---

## Tools Used

| Tool | How |
|------|-----|
| Claude (Anthropic API) | Runs all three prompts — tagging, severity, response draft |
| Prompt Library (`01-prompt-library/`) | Reusable, versioned system prompts stored as Markdown files |
| Product docs (`02-context-pack/`) | Injected into Claude's context window so responses cite real features |
| `triage_pipeline.py` | Python glue: reads CSV, calls API, writes output files |

---

## The Result

After running the script on a week's worth of tickets:

- Every ticket had a category tag and a 1-4 severity score with a one-line rationale
- P1 tickets (severity 1) were listed at the top of `trend_report.md` for immediate action
- The top three issue categories that week were visible in seconds: `authentication` (34%), `mobile-bug` (21%), `billing` (18%)
- Draft responses — grounded in real documentation — were ready for agents to review and send, cutting average handle time by roughly 40%

The team now runs the script every Monday morning on the previous week's export. The trend report goes into their sprint planning doc automatically.

---

## Next Steps

**Week 2:** Connect directly to the Zendesk API so the script reads and writes tickets in real time — no CSV export needed.

**Month 2:** Add a Slack webhook so P1 tickets post to `#support-alerts` the moment they're classified.

**Month 3:** Replace the full-doc context injection with a small vector store (Chroma) so the system scales as the product documentation grows beyond 20 pages.

**Longer term:** Build a lightweight dashboard (a Google Sheet with a chart) that auto-populates from `triage_output.csv` — management gets a live trend view without touching the script.
