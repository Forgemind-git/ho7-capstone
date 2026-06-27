"""
Content Production Pipeline
HO7 Capstone — Sample 04

Runs a 4-step content production pipeline:
  1. Research brief generation (grounded in trend signals + personas)
  2. Long-form blog post draft
  3. LinkedIn post repurposing
  3b. Twitter/X thread repurposing
  4. Email newsletter repurposing

Writes all outputs to the output/ directory.

Requirements:
    pip install anthropic python-dotenv

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python content_pipeline.py
    # or:
    python content_pipeline.py --topic "Your topic here"
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

BASE = Path(__file__).parent
PROMPT_DIR = BASE.parent / "01-prompt-library"
CONTEXT_DIR = BASE.parent / "02-context-pack"
OUTPUT_DIR = BASE / "output"


def load_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}")
        sys.exit(1)


def extract_system_prompt(prompt_md: str) -> str:
    lines = prompt_md.split("\n")
    in_fence, captured = False, []
    for line in lines:
        if line.strip().startswith("```") and not in_fence:
            in_fence = True
            continue
        if line.strip() == "```" and in_fence:
            break
        if in_fence:
            captured.append(line)
    return "\n".join(captured).strip() if captured else prompt_md.strip()


def inject_context(template: str, context: dict) -> str:
    """Replace {{KEY}} placeholders in a template string."""
    result = template
    for key, value in context.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result


def call_claude(client: anthropic.Anthropic, system: str, user: str, max_tokens: int = 2048) -> str:
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text.strip()


def word_count(text: str) -> int:
    return len(text.split())


def main():
    parser = argparse.ArgumentParser(description="Content Production Pipeline")
    parser.add_argument("--topic", type=str, help="Topic brief (overrides topic_brief.txt)")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Determine topic
    if args.topic:
        topic = args.topic
    else:
        topic_file = BASE / "topic_brief.txt"
        if topic_file.exists():
            topic = load_file(topic_file).strip()
        else:
            print("ERROR: No topic provided. Use --topic 'your topic' or create topic_brief.txt")
            sys.exit(1)

    print(f"\nContent Production Pipeline")
    print(f"Topic: \"{topic}\"")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("-" * 60)

    # Load context pack
    trend_signals = load_file(CONTEXT_DIR / "trend-signals.txt")
    audience_personas = load_file(CONTEXT_DIR / "audience-personas.txt")
    brand_voice = load_file(CONTEXT_DIR / "brand-voice.txt")

    context = {
        "TREND_SIGNALS": trend_signals,
        "AUDIENCE_PERSONAS": audience_personas,
        "BRAND_VOICE": brand_voice,
    }

    # Load prompt templates
    research_brief_template = extract_system_prompt(load_file(PROMPT_DIR / "research-brief-prompt.md"))
    blog_draft_template = extract_system_prompt(load_file(PROMPT_DIR / "blog-draft-prompt.md"))
    repurpose_template = extract_system_prompt(load_file(PROMPT_DIR / "repurpose-prompt.md"))

    # -----------------------------------------------------------------------
    # STEP 1: Research Brief
    # -----------------------------------------------------------------------
    print("\nStep 1/4: Generating research brief...")
    research_system = inject_context(research_brief_template, context)
    research_brief = call_claude(client, research_system, topic, max_tokens=2048)
    wc_brief = word_count(research_brief)
    print(f"  Research brief: {wc_brief} words")

    # -----------------------------------------------------------------------
    # STEP 2: Blog Post Draft
    # -----------------------------------------------------------------------
    print("\nStep 2/4: Drafting blog post...")
    blog_system = inject_context(blog_draft_template, context)
    blog_user = f"## Topic\n{topic}\n\n## Research Brief\n{research_brief}"
    blog_post = call_claude(client, blog_system, blog_user, max_tokens=3000)
    wc_blog = word_count(blog_post)
    print(f"  Blog post: {wc_blog} words")

    # -----------------------------------------------------------------------
    # STEP 3a: LinkedIn Post
    # -----------------------------------------------------------------------
    print("\nStep 3/4: Repurposing for LinkedIn...")
    linkedin_system = inject_context(repurpose_template, context)
    linkedin_user = f"Format: LinkedIn Post\n\n{blog_post}"
    linkedin_post = call_claude(client, linkedin_system, linkedin_user, max_tokens=800)
    wc_linkedin = word_count(linkedin_post)
    print(f"  LinkedIn post: {wc_linkedin} words")

    # -----------------------------------------------------------------------
    # STEP 3b: Twitter/X Thread
    # -----------------------------------------------------------------------
    print("\nStep 3b/4: Repurposing for Twitter/X thread...")
    twitter_user = f"Format: Twitter/X Thread\n\n{blog_post}"
    twitter_thread = call_claude(client, linkedin_system, twitter_user, max_tokens=800)
    wc_twitter = word_count(twitter_thread)
    print(f"  Twitter thread: {wc_twitter} words")

    # -----------------------------------------------------------------------
    # STEP 4: Email Newsletter
    # -----------------------------------------------------------------------
    print("\nStep 4/4: Repurposing for email newsletter...")
    email_user = f"Format: Email Newsletter\n\n## Blog Post\n{blog_post}\n\n## Research Brief (for additional context)\n{research_brief}"
    email_newsletter = call_claude(client, linkedin_system, email_user, max_tokens=1000)
    wc_email = word_count(email_newsletter)
    print(f"  Newsletter: {wc_email} words")

    # -----------------------------------------------------------------------
    # Write outputs
    # -----------------------------------------------------------------------
    OUTPUT_DIR.mkdir(exist_ok=True)

    outputs = {
        "research_brief.md": research_brief,
        "blog_post.md": blog_post,
        "linkedin_post.md": linkedin_post,
        "twitter_thread.md": twitter_thread,
        "email_newsletter.md": email_newsletter,
    }

    total_words = sum(word_count(v) for v in outputs.values())

    print(f"\n{'─'*60}")
    print(f"Output written to {OUTPUT_DIR}/")
    for filename, content in outputs.items():
        out_path = OUTPUT_DIR / filename
        out_path.write_text(content, encoding="utf-8")
        print(f"  {filename} ({word_count(content)} words)")

    print(f"\nTotal content produced: {total_words:,} words across {len(outputs)} files")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    main()
