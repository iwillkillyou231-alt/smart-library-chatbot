"""
normalizer.py
Step 1 of the NLP pipeline.

Purpose:
    Convert raw user input into a clean, standardized lowercase string
    that later steps can safely tokenize.

What it does:
    1. Lowercases the text.
    2. Expands common English contractions.
    3. Removes punctuation (except hyphens inside words like "state-of-the-art").
    4. Collapses multiple spaces into one.
    5. Strips leading/trailing whitespace.

This file is intentionally rule-based and fully explainable.
"""

import re

# Contraction map. Extend only when a real failure case requires it.
CONTRACTIONS = {
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "can't": "cannot",
    "won't": "will not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "i'm": "i am",
    "i've": "i have",
    "i'd": "i would",
    "i'll": "i will",
    "you're": "you are",
    "you've": "you have",
    "you'll": "you will",
    "it's": "it is",
    "that's": "that is",
    "there's": "there is",
    "what's": "what is",
    "let's": "let us",
}


def expand_contractions(text: str) -> str:
    """Replace contractions with their expanded forms."""
    for short, full in CONTRACTIONS.items():
        # word-boundary safe replacement
        text = re.sub(r"\b" + re.escape(short) + r"\b", full, text)
    return text


def remove_punctuation(text: str) -> str:
    """
    Remove punctuation but keep hyphens between letters
    (e.g., 'state-of-the-art' stays intact).
    """
    # Replace hyphens between letters with a space, then remove all other punctuation.
    # We do this so 'state-of-the-art' -> 'state of the art' and 'don't' -> 'dont'
    text = re.sub(r"(?<=\w)-(?=\w)", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    return text


def normalize(text: str) -> str:
    """
    Full normalization pipeline for one user input.
    Returns a clean lowercase string.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = expand_contractions(text)
    text = remove_punctuation(text)
    text = re.sub(r"\s+", " ", text)   # collapse whitespace
    return text.strip()


# -------- quick manual test (run: python nlp/normalizer.py) --------
if __name__ == "__main__":
    samples = [
        "I want a beginner-friendly book about cybersecurity, especially network attacks.",
        "Don't show me anything too advanced!",
        "State-of-the-art AI, please.",
        "  Extra   spaces   here  ",
    ]
    for s in samples:
        print(f"IN : {s}")
        print(f"OUT: {normalize(s)}")
        print("-" * 60)