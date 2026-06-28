"""
HO7 Sample 2 — Competitor Gap Analysis Script
==============================================
TODO: Build a script that:
  1. Reads each competitor notes file from 02-context-pack/
  2. Runs the research-extraction-prompt on each competitor's content
  3. Runs the gap-analysis-prompt comparing each competitor to our product
  4. Runs the report-assembly-prompt to generate a weekly report
  5. Saves the output as weekly_report_YYYY-MM-DD.md

Starter skeleton below — fill in the TODOs.
"""

import os
from datetime import date

# TODO: import anthropic

PROMPT_DIR = "../01-prompt-library/"
CONTEXT_DIR = "../02-context-pack/"

def load_file(path):
    """TODO: Read a text file and return its contents."""
    pass

def extract_intelligence(client, competitor_name, content):
    """TODO: Call Claude with the research-extraction prompt."""
    pass

def analyse_gap(client, our_product, competitor_name, intel):
    """TODO: Call Claude with the gap-analysis prompt."""
    pass

def assemble_report(client, week_date, all_analyses):
    """TODO: Call Claude with the report-assembly prompt."""
    pass

def main():
    # TODO: Initialise Anthropic client
    # TODO: Load our product summary
    # TODO: Find all competitor-*.txt files in context-pack
    # TODO: For each competitor, extract intel and analyse gap
    # TODO: Assemble weekly report
    # TODO: Save to weekly_report_YYYY-MM-DD.md
    print("TODO: implement main()")

if __name__ == "__main__":
    main()
