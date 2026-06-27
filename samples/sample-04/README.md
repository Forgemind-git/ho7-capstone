# Sample 04 — Content Production Engine

> **Problem:** Content team cannot scale research + production

A full content production pipeline that takes a raw topic brief, pulls in trend research and audience insights, drafts original content, and repurposes it across formats — all in one automated run.

---

## Course Concepts Combined

| # | Concept | Where It Appears |
|---|---------|-----------------|
| 1 | **Trend Research** | NotebookLM-style context pack with trend signals and audience data as grounding |
| 2 | **Prompt Library** | Drafting and repurposing prompts for each content format |
| 3 | **Automation** | Python pipeline: research → draft → repurpose → output bundle |

---

## Architecture

```
Topic Brief (input)
       │
       ▼
┌─────────────────────────┐
│  02-context-pack/       │
│  trend-signals.txt      │  ← research grounding
│  audience-personas.txt  │
│  brand-voice.txt        │
└──────────┬──────────────┘
           │  injected as context
           ▼
┌─────────────────────────┐
│  01-prompt-library/     │
│  research-brief-prompt  │
│  blog-draft-prompt      │
│  repurpose-prompt       │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  03-automation/         │
│  content_pipeline.py    │
└──────────┬──────────────┘
           ▼
  output/
  ├── research_brief.md
  ├── blog_post.md
  ├── linkedin_post.md
  ├── twitter_thread.md
  └── email_newsletter.md
```

---

## How to Reproduce

### Prerequisites

```bash
pip install anthropic python-dotenv
export ANTHROPIC_API_KEY=sk-ant-...
```

### Run the pipeline

```bash
cd samples/sample-04/components/03-automation/
python content_pipeline.py --topic "How to reduce meeting overload with async-first teams"
```

Or edit `topic_brief.txt` and run without the flag:

```bash
python content_pipeline.py
```

The script will create an `output/` folder with five content pieces ready to review and publish.

### Customise

1. Update `02-context-pack/brand-voice.txt` with your brand guidelines.
2. Update `02-context-pack/audience-personas.txt` with your actual personas.
3. Edit any prompt in `01-prompt-library/` to adjust tone, length, or format.

---

## Expected Output

```
Content Production Pipeline
Topic: "How to reduce meeting overload with async-first teams"

Step 1/4: Generating research brief...
  Research brief: 847 words

Step 2/4: Drafting blog post...
  Blog post: 1,203 words

Step 3/4: Repurposing for LinkedIn...
  LinkedIn post: 312 words

Step 3b/4: Repurposing for Twitter/X thread...
  Twitter thread: 8 tweets

Step 4/4: Repurposing for email newsletter...
  Newsletter: 423 words

Output written to output/ (5 files)
Total content produced: 2,785 words
```
