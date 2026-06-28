"""
HO7 Sample 3 — Candidate Scorer
================================
TODO: Build a script that:
  1. Reads each transcript file from sample_transcripts/
  2. Calls Claude with the score-candidate prompt (injecting the rubric)
  3. Outputs a scorecard for each candidate
  4. Writes candidate_comparison.md comparing all candidates side-by-side

Starter skeleton below.
"""

# TODO: import anthropic and other needed libraries

def score_candidate(client, candidate_name, role, rubric, notes):
    """TODO: Call Claude and return the scorecard text."""
    pass

def main():
    # TODO: Load rubric from context-pack
    # TODO: Find all transcript files
    # TODO: Score each candidate
    # TODO: Write candidate_comparison.md
    print("TODO: implement main()")

if __name__ == "__main__":
    main()
