# Story — Content Production Engine

## The Problem

Yemi runs content for a B2B SaaS startup. Their audience is operations managers and team leads. The content brief for a single blog post takes half a day: research trends, check what competitors are publishing, understand what the audience cares about, then actually write the post. Then comes the repurposing — LinkedIn version, Twitter thread, email newsletter snippet — which takes another half day.

With one content person and a publishing target of three posts per week, the math doesn't work.

## The Approach

The bottleneck isn't writing speed — it's the research and context-gathering that happens before writing. If that work is done well and baked into a grounding context pack, the drafting step becomes much faster.

Yemi built a pipeline with three layers:

1. **Context pack** — a set of maintained text files: current trend signals in the SaaS operations space, two detailed audience personas, and a brand voice guide. Updated monthly, not per-post.
2. **Prompt library** — four prompts: one that turns a topic into a research brief, one that turns a research brief into a blog draft, and one that repurposes a draft into three different formats.
3. **Python pipeline** — runs all four steps in sequence, reads from the context pack, and produces five ready-to-review files.

The key insight: the context pack does the heavy lifting. Once it's maintained, every new topic benefits from the accumulated research.

## Tools Used

| Tool | How |
|------|-----|
| Claude (Anthropic API) | All four generation steps |
| Prompt Library (`01-prompt-library/`) | Research brief, blog draft, and repurposing prompts |
| Context pack (`02-context-pack/`) | Trend signals, personas, brand voice — grounding for every step |
| `content_pipeline.py` | Orchestrates all steps, writes output files |

## The Result

First run on topic "How to reduce meeting overload with async-first teams":

- Research brief: 850 words of structured angles, data points, and keyword targets — in 45 seconds
- Blog post: 1,200 words, on-brand, with a clear structure — in 90 seconds
- LinkedIn, Twitter, email newsletter: 3 more pieces from the blog draft — in 60 seconds total

Total: five content pieces in under 4 minutes.

Yemi still reviews and edits every piece — the pipeline doesn't remove human judgment. But the edit is now 20 minutes instead of 4 hours. Publishing three posts per week is now achievable with the same headcount.

## Next Steps

**Month 1:** Automate the trend signal updates — scrape 3-4 industry newsletters weekly and summarise them into `trend-signals.txt` using a separate Claude call.

**Month 2:** Add a publishing step that posts the LinkedIn content automatically (via LinkedIn API) and creates a Buffer-scheduled Twitter thread.

**Month 3:** Build a content calendar view — a simple CSV that tracks which topics have been drafted, reviewed, scheduled, and published.

**Longer term:** Track which pieces perform best (engagement, clicks, conversions) and feed that signal back into the research brief prompt as preference data.
