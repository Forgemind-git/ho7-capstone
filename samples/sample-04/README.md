# HO7 Sample 04 — Content Production Engine

> **Problem:** content output stalls because research, drafting, and repurposing are all manual.

## What you'll build
A content engine that takes one topic from research to a finished blog post plus three repurposed formats (LinkedIn, an X/Twitter thread, and an email newsletter) — built entirely inside **Claude.ai**, no code, no API key. You load your brand voice, audience personas, and current trend signals into a Claude **Project**, then Claude writes a research brief, drafts the post in your voice, and spins it into every channel format in one session. It combines three course concepts: **trend research grounding**, a **prompt library** of drafting prompts, and an **automation** that repurposes one piece into many.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login.

1. Open **Claude.ai** → **Projects** → **Create Project**. Call it "Content Engine".
2. Click **Add content / Project knowledge** and upload the three files from `components/02-context-pack/`: `brand-voice.txt`, `audience-personas.txt`, and `trend-signals.txt`. This is what makes the output sound like *you*, not generic AI.
3. Open the three prompt files in `components/01-prompt-library/` (`research-brief-prompt.md`, `blog-draft-prompt.md`, `repurpose-prompt.md`) — these are the three steps.
4. Start a chat **inside the Project** and paste **The example prompt** below, swapping in your topic. Claude produces a research brief, then a full blog post, then the three repurposed formats — all in your brand voice.
5. Copy each output into your CMS / scheduler. Reuse the same prompt for the next topic; the brand voice stays consistent because it lives in the Project.

## The example prompt
Copy this into a chat inside your "Content Engine" Project and change the topic line:

```
You are my content production engine. Use the brand voice, audience personas, and trend signals in this Project's knowledge. Write to the primary persona, in our brand voice, and avoid buzzwords (leverage, synergy, game-changer).

TOPIC: "How to reduce meeting overload with async-first teams"

Produce these four pieces, clearly labelled:

1. RESEARCH BRIEF — the angle, the persona pain it solves, 3-4 key points to make, and one relevant trend signal to reference.

2. BLOG POST — 800-1,200 words. Hook intro with a concrete scenario (not "in today's world"), 3-4 H2 sections each with a real example, short paragraphs, and a specific low-friction call to action.

3. LINKEDIN POST — ~200 words, first-person, one strong hook line, 3 takeaways, ends with a question to drive comments.

4. X / TWITTER THREAD — 6-8 tweets, each under 280 characters, first tweet is the hook, last tweet has the CTA.

5. EMAIL NEWSLETTER — ~400 words, subject line + preview text + body, conversational, one clear CTA button line.
```

## Course concepts combined
| # | Concept | Where it appears |
|---|---------|-----------------|
| 1 | **Trend research grounding** | Trend signals + personas loaded as Project knowledge in `02-context-pack/` |
| 2 | **Prompt library** | Research-brief, blog-draft, and repurpose prompts in `01-prompt-library/` |
| 3 | **Automation** | One run takes a topic to five finished, on-brand pieces |

See `architecture.md` for the component map and `story.md` for the real-world walkthrough.

## Make it your own
- Replace `brand-voice.txt` and `audience-personas.txt` with your own — this is the highest-leverage change.
- Add or remove output formats (e.g. a YouTube script or an Instagram caption) by editing the numbered list.
- Refresh `trend-signals.txt` monthly so the posts reference what's current.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you later want to run the whole pipeline from the command line, `components/03-automation/content_pipeline.py` shows how (it reads `topic_brief.txt` or a `--topic` flag). It needs an Anthropic API key, which is **separate** from your Claude.ai subscription (billed per use), so it is optional and not part of the hands-on.
