"""
tokenizer.py
Step 2 of the NLP pipeline.

Purpose:
    Split a normalized string into meaningful tokens and remove stopwords.

What it does:
    1. Splits on whitespace.
    2. Removes stopwords (from stopwords.py).
    3. Keeps tokens of length >= 2.
    4. Returns the token list.

Why this matters:
    Tokens are what the extractor, synonym expander, and TF-IDF modules
    will work with. Garbage tokens produce garbage matches.
"""

from nlp.normalizer import normalize
from nlp.stopwords import STOPWORDS, KEEP_WORDS


def tokenize(text: str, keep_stopwords: bool = False) -> list:
    """
    Normalize then split into tokens.

    Args:
        text: raw user input
        keep_stopwords: if True, do not remove stopwords
                        (useful for follow-up detection later)

    Returns:
        list of tokens
    """
    normalized = normalize(text)
    raw_tokens = normalized.split()

    tokens = []
    for tok in raw_tokens:
        if len(tok) < 2:
            continue
        if not keep_stopwords:
            if tok in STOPWORDS and tok not in KEEP_WORDS:
                continue
        tokens.append(tok)
    return tokens


# -------- quick manual test (run: python -m nlp.tokenizer) --------
if __name__ == "__main__":
    samples = [
        "I want a beginner-friendly book about cybersecurity, especially network attacks.",
        "Don't show me anything too advanced!",
        "Something easier please.",
    ]
    for s in samples:
        print(f"IN : {s}")
        print(f"TOK: {tokenize(s)}")
        print("-" * 60)