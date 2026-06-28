"""
HO7 Sample 4 — Content Pipeline
=================================
TODO: Build a script that:
  1. Reads topic_brief.txt for the topic and any gathered notes
  2. Calls Claude with the research-brief-prompt (injecting brand voice + personas)
  3. Calls Claude with the blog-draft-prompt (injecting the brief + notes)
  4. Calls Claude with the repurpose-prompt to generate LinkedIn + email + tweet
  5. Saves all outputs to a dated folder

Starter skeleton below.
"""

from datetime import date
import os

# TODO: import anthropic

PROMPT_DIR = "../01-prompt-library/"
CONTEXT_DIR = "../02-context-pack/"

def generate_brief(client, topic, brand_voice, personas):
    """TODO: Call Claude with the research-brief prompt."""
    pass

def draft_blog(client, brief, sources, brand_voice):
    """TODO: Call Claude with the blog-draft prompt."""
    pass

def repurpose(client, blog_post):
    """TODO: Call Claude with the repurpose prompt."""
    pass

def main():
    # TODO: Load brand voice and personas
    # TODO: Read topic_brief.txt
    # TODO: Generate research brief
    # TODO: Draft blog post
    # TODO: Repurpose to LinkedIn + email + tweet
    # TODO: Save outputs to output_YYYY-MM-DD/
    print("TODO: implement main()")

if __name__ == "__main__":
    main()
