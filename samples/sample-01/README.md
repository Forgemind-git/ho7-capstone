# HO7 Sample 01 — AI Support Triage System

> **Problem:** the support team is buried in tickets and leadership has no view of what is breaking.

## What you'll build
A complete support-triage helper, built entirely inside **Claude.ai** — no code, no API key. You give Claude your product documentation and a list of known issues once (as a Claude **Project**), then for every incoming ticket Claude tags it, scores how urgent it is, and drafts a warm reply grounded in your real docs. At the end of the week you ask Claude for a one-screen trend summary so you can see what is actually going wrong. It combines three course concepts: a **prompt library**, a **grounded assistant**, and a light **automation/skill**.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login.

1. Open **Claude.ai** and click **Projects** in the left sidebar, then **Create Project**. Call it "Support Triage".
2. Click **Add content / Project knowledge** and upload the two files from `components/02-context-pack/` — `product-docs.txt` and `known-issues.txt`. This is what keeps Claude's answers accurate instead of guessed.
3. Open the three prompt files in `components/01-prompt-library/` (`tagging-prompt.md`, `severity-prompt.md`, `response-draft-prompt.md`). These are your reusable instructions — keep them in a note so you can paste them whenever you need them.
4. Start a new chat **inside the Project** and paste **The example prompt** below (it already chains tag → severity → draft reply in one go). Paste a real ticket where shown.
5. Claude returns a tag, a severity (1–4), and a ready-to-send draft reply that cites your docs. Review it and send.
6. Once a week, paste your list of that week's tags into the same Project and ask: *"Summarise this week's tickets: top 3 categories, average severity, and the P1 issues I should act on first."* That is your trend view.

## The example prompt
Copy this into a chat inside your "Support Triage" Project, then paste one ticket where shown:

```
You are my support-triage assistant. Use ONLY the product documentation and known-issues list in this Project's knowledge — never invent feature names, dates, or workarounds. If something isn't covered, say so.

For the ticket below, do three things and label each clearly:

1. TAG — pick exactly one category: authentication, billing, mobile-bug, web-bug, performance, data-export, integration, feature-request, account-management, or other.

2. SEVERITY — score 1 to 4 (1 = outage / data loss / many users blocked, 2 = a core feature broken for one user, 3 = annoying but has a workaround, 4 = question or feature request) and give a one-line reason.

3. DRAFT REPLY — a warm, professional reply, max 3 short paragraphs. Address the customer's exact problem in the first sentence, reference the relevant doc section if there is one, acknowledge it if it's a known issue, and end with a clear next step.

Ticket:
"I upgraded to the Premium plan 5 days ago but my dashboard still shows Free. I've been charged twice and I'm worried I'm being billed for nothing. Please sort this out today."
```

## Course concepts combined
| # | Concept | Where it appears |
|---|---------|-----------------|
| 1 | **Prompt Library** | Tagging + severity + response-draft prompts in `01-prompt-library/` |
| 2 | **Grounded Assistant** | Claude reads `02-context-pack/` (product docs + known issues) before replying |
| 3 | **Automation / Skill** | The weekly trend summary — one prompt that rolls many tickets into a one-screen view |

See `architecture.md` for the full component map and `story.md` for the real-world walkthrough.

## Make it your own
- Replace `02-context-pack/product-docs.txt` and `known-issues.txt` with your own product's docs and bug list.
- Edit the tag list in the example prompt so the categories match your product.
- Add your own severity rules — e.g. anything mentioning "charged twice" is automatically severity 2.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you later want to process a whole CSV export of tickets automatically, `components/03-automation/triage_pipeline.py` shows how. It needs an Anthropic API key, which is **separate** from your Claude.ai subscription (it's billed per use), so it is optional and not part of the hands-on.
