"""
synonym_expander.py
Step 4 of the NLP pipeline.

Purpose:
    Given a token list, add synonyms from data/synonyms.json so that
    different phrasings of the same idea match the same books.

Example:
    tokens:  ['hacking', 'beginner']
    expanded: ['hacking', 'beginner', 'cybersecurity', 'security',
               'intro', 'easy', 'basic', 'fundamentals']

Why this matters:
    Without expansion, "hacking" and "cybersecurity" would be treated as
    unrelated words even though they mean the same thing in this domain.
"""

import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYNONYMS_PATH = os.path.join(BASE_DIR, "data", "synonyms.json")

with open(SYNONYMS_PATH, "r", encoding="utf-8") as f:
    SYNONYMS = json.load(f)


def expand(tokens):
    """
    Return a new token list that includes the original tokens plus
    all synonyms mapped in synonyms.json.

    - Preserves order (original tokens first, then new synonyms).
    - Deduplicates.
    """
    expanded = list(tokens)
    seen = set(tokens)

    for tok in tokens:
        for syn in SYNONYMS.get(tok, []):
            # synonyms may be multi-word phrases -> split for token list
            for sub in syn.lower().split():
                if sub not in seen:
                    seen.add(sub)
                    expanded.append(sub)

    return expanded


def expand_string(text):
    """Convenience: expand a raw string instead of a token list."""
    return " ".join(expand(text.lower().split()))


# -------- quick manual test --------
if __name__ == "__main__":
    samples = [
        ["hacking", "beginner"],
        ["ai"],
        ["network", "advanced"],
        ["db", "easy"],
    ]
    for s in samples:
        print(f"IN : {s}")
        print(f"OUT: {expand(s)}")
        print("-" * 70)