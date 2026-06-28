"""
HO7 Sample 1 — Support Triage Pipeline
=======================================
TODO: Build a script that:
  1. Reads tickets from a CSV (ticket_id, subject, body)
  2. Sends each ticket through the tagging prompt
  3. Sends each ticket through the severity-scoring prompt
  4. Sends each ticket through the response-draft prompt (with docs injected)
  5. Writes triage_output.csv and trend_report.md

Starter skeleton below — fill in the TODOs.
"""

import csv
# TODO: import anthropic and any other libraries you need

PROMPT_DIR = "../01-prompt-library/"
CONTEXT_DIR = "../02-context-pack/"

def load_file(path):
    """TODO: Read a text file and return its contents."""
    pass

def tag_ticket(client, subject, body):
    """TODO: Call Claude with the tagging prompt and return the category tag."""
    pass

def score_severity(client, subject, body, tag):
    """TODO: Call Claude with the severity prompt and return severity (1-4) + rationale."""
    pass

def draft_response(client, subject, body, product_docs, known_issues):
    """TODO: Call Claude with the response-draft prompt and return the draft."""
    pass

def main():
    # TODO: Initialise the Anthropic client
    # TODO: Load prompts and context files
    # TODO: Read sample_tickets.csv
    # TODO: Loop through tickets, call the three functions above
    # TODO: Write triage_output.csv
    # TODO: Write trend_report.md (top tags, avg severity, P1 list)
    print("TODO: implement main()")

if __name__ == "__main__":
    main()
