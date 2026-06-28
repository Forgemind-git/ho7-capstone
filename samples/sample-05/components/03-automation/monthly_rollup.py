"""
HO7 Sample 5 — Monthly Roll-Up Generator
==========================================
TODO: Build a script that:
  1. Reads categorised_transactions.csv
  2. Calls Claude with the rollup prompt to generate a summary + chart JSON
  3. Saves monthly_summary_YYYY-MM.md (the text) and chart_data.json (the data block)

Starter skeleton below.
"""

import json

# TODO: import anthropic

PROMPT_DIR = "../01-prompt-library/"

def generate_rollup(client, categorised_csv_text, month_year, financial_rules):
    """TODO: Call Claude with the rollup prompt, return (summary_text, chart_json)."""
    pass

def main():
    # TODO: Load rollup prompt and financial rules
    # TODO: Read categorised_transactions.csv
    # TODO: Determine month_year (e.g. from the data or argv)
    # TODO: Generate roll-up
    # TODO: Parse chart JSON from response and save separately
    print("TODO: implement main()")

if __name__ == "__main__":
    main()
