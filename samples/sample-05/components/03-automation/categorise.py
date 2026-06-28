"""
HO7 Sample 5 — Transaction Categoriser
=======================================
TODO: Build a script that:
  1. Reads sample_transactions.csv (date, description, amount)
  2. Sends transactions to Claude in batches using the categorise prompt
  3. Writes categorised_transactions.csv (adds a 'category' column)

Starter skeleton below.
"""

import csv

# TODO: import anthropic

PROMPT_DIR = "../01-prompt-library/"

def categorise_batch(client, transactions_text):
    """TODO: Call Claude with the categorise prompt, return list of categories."""
    pass

def main():
    # TODO: Load categorise prompt
    # TODO: Read sample_transactions.csv
    # TODO: Send in batches of 20 rows (to stay within context)
    # TODO: Write categorised_transactions.csv
    print("TODO: implement main()")

if __name__ == "__main__":
    main()
