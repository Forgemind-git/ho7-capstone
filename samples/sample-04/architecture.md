# Architecture — Content Production Engine

## Overview

Four sequential steps: research grounding, research brief generation, long-form draft, and multi-format repurposing. Each step's output feeds the next, meaning the LinkedIn post is derived from the same research and voice guidelines as the blog post — not written independently.

---

## Component Map

| Component | Module | File |
|-----------|--------|------|
| Research brief prompt | Prompt Library (HO2) | `01-prompt-library/research-brief-prompt.md` |
| Blog draft prompt | Prompt Library (HO2) | `01-prompt-library/blog-draft-prompt.md` |
| Repurposing prompt | Prompt Library (HO2) | `01-prompt-library/repurpose-prompt.md` |
| Trend signals | Context & Grounding (HO4) | `02-context-pack/trend-signals.txt` |
| Audience personas | Context & Grounding (HO4) | `02-context-pack/audience-personas.txt` |
| Brand voice | Context & Grounding (HO4) | `02-context-pack/brand-voice.txt` |
| Content pipeline | Automation (HO5-6) | `03-automation/content_pipeline.py` |

---

## Data Flow (ASCII)

```
 ┌──────────────────────────────────────────────────────────────┐
 │                  INPUT                                       │
 │  Topic brief (CLI flag or topic_brief.txt)                   │
 └───────────────────────────┬──────────────────────────────────┘
                             │
 ┌───────────────────────────▼──────────────────────────────────┐
 │              GROUNDING LAYER (HO4)                           │
 │                                                              │
 │  trend-signals.txt      — current trends in the topic area   │
 │  audience-personas.txt  — who we're writing for              │
 │  brand-voice.txt        — tone, style, do's and don'ts       │
 │                                                              │
 │  All three injected into every prompt's system context       │
 └───────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
 ┌──────────────────────────────────────────────────────────────┐
 │           STEP 1 — RESEARCH BRIEF (Prompt Library)           │
 │                                                              │
 │  System: research-brief-prompt.md + grounding                │
 │  Input:  topic brief                                         │
 │  Output: research_brief.md                                   │
 │          - key angles to cover                               │
 │          - data points and statistics to include             │
 │          - common misconceptions to address                  │
 │          - target keyword phrases                            │
 └───────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
 ┌──────────────────────────────────────────────────────────────┐
 │           STEP 2 — BLOG DRAFT (Prompt Library)               │
 │                                                              │
 │  System: blog-draft-prompt.md + grounding                    │
 │  Input:  topic + research_brief.md                           │
 │  Output: blog_post.md (800-1200 words)                       │
 └───────────────────────────┬──────────────────────────────────┘
                             │  blog post as input
                     ┌───────┴───────┐
                     ▼               ▼
 ┌──────────────────────────┐ ┌──────────────────────────┐
 │  STEP 3a — LINKEDIN      │ │  STEP 3b — TWITTER/X     │
 │  repurpose-prompt.md     │ │  repurpose-prompt.md     │
 │  format=linkedin         │ │  format=twitter_thread   │
 │  Output: linkedin_post.md│ │  Output: twitter_thread  │
 └──────────────────────────┘ └──────────────────────────┘
                     │               │
                     └───────┬───────┘
                             ▼
 ┌──────────────────────────────────────────────────────────────┐
 │           STEP 4 — EMAIL NEWSLETTER (Prompt Library)         │
 │                                                              │
 │  repurpose-prompt.md  format=email_newsletter                │
 │  Input:  blog post + research brief                          │
 │  Output: email_newsletter.md                                 │
 └───────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
                    output/ (5 files)
```

---

## Key Design Decisions

**Why generate a research brief before drafting?**
Separating "what to say" from "how to say it" produces better content. The research brief step ensures the draft is comprehensive; the draft step focuses on voice and structure. Combined prompts tend to sacrifice one for the other.

**Why pass the blog post to repurposing instead of re-running from the brief?**
Consistency. The LinkedIn post should reflect what the blog post actually says, not a new interpretation of the brief. Repurposing from the long-form piece ensures all formats tell the same story.

**Why inject brand voice into every prompt?**
Voice consistency is the most common failure mode in AI content. Injecting it as a system-level constraint into every step means even the research brief and repurposed tweets stay on-brand.

---

## Extension Points

1. **NotebookLM integration** — replace `trend-signals.txt` with an exported NotebookLM summary for richer research grounding
2. **Publishing automation** — add a `publish.py` step that posts the LinkedIn content via LinkedIn API and schedules the Twitter thread via Buffer API
3. **SEO optimisation** — add a fifth prompt that rewrites the blog post with specific keyword insertion based on the research brief's target phrases
4. **Image brief** — add a prompt that generates a creative brief for a designer or image generation tool based on the blog post content
