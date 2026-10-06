"""
tfidf.py
Step 5 of the NLP pipeline.

Purpose:
    Build TF-IDF vectors from scratch. No external ML libraries.

Definitions:
    TF  (Term Frequency)       = count(term in doc) / total_terms_in_doc
    IDF (Inverse Doc Frequency) = ln( (1 + N) / (1 + df) ) + 1   [smoothed]
    TF-IDF = TF * IDF

Why this matters:
    Common words like "book" or "introduction" appear in many documents.
    Rare words like "cryptography" appear in few. IDF automatically
    down-weights common terms and boosts distinctive terms.
"""

import math
from collections import Counter


def build_vocabulary(documents):
    """
    Return a set of all unique terms across all documents.

    Args:
        documents: list of token lists (each token list = one document)
    """
    vocab = set()
    for doc in documents:
        vocab.update(doc)
    return vocab


def compute_idf(documents):
    """
    Smoothed inverse document frequency.
    idf(t) = ln( (1 + N) / (1 + df(t)) ) + 1

    Args:
        documents: list of token lists

    Returns:
        dict {term: idf_value}
    """
    N = len(documents)
    df = Counter()
    for doc in documents:
        for term in set(doc):   # count each term once per document
            df[term] += 1

    idf = {}
    for term, freq in df.items():
        idf[term] = math.log((1 + N) / (1 + freq)) + 1.0
    return idf


def compute_tf(tokens):
    """
    Term frequency for one document.
    tf(t) = count(t) / total_tokens
    """
    if not tokens:
        return {}
    counts = Counter(tokens)
    total = len(tokens)
    return {term: cnt / total for term, cnt in counts.items()}


def tfidf_vector(tokens, idf, vocabulary=None):
    """
    Return a dict {term: tfidf_score} for one document or query.

    Args:
        tokens: list of tokens
        idf: dict from compute_idf
        vocabulary: optional set — terms not in vocab are ignored
    """
    tf = compute_tf(tokens)
    vec = {}
    for term, tf_val in tf.items():
        if vocabulary is not None and term not in vocabulary:
            continue
        vec[term] = tf_val * idf.get(term, 0.0)
    return vec