"""
HO7 Sample 5 — Finance Q&A REPL
=================================
TODO: Build a simple REPL (interactive loop) that:
  1. Loads categorised_transactions.csv and financial_rules.txt as context
  2. Lets you type questions in plain English
  3. Sends each question to Claude (injecting the data) and prints the answer
  4. Type 'quit' to exit

Starter skeleton below.
"""

# TODO: import anthropic

PROMPT_DIR = "../01-prompt-library/"
CONTEXT_DIR = "../02-context-pack/"

def ask_claude(client, question, categorised_data, financial_rules, qa_prompt):
    """TODO: Call Claude with the Q&A prompt + injected data, return the answer."""
    pass

def main():
    # TODO: Load qa prompt, financial rules, categorised transactions
    # TODO: Start loop: prompt for question, call ask_claude, print answer
    print("TODO: implement main()")
    while True:
        q = input("Your question (or 'quit'): ").strip()
        if q.lower() == "quit":
            break
        # TODO: call ask_claude and print the result

if __name__ == "__main__":
    main()
