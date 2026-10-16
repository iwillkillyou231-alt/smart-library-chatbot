"""
Why this matters:
    Common words like "book" or "introduction" appear in many documents.
    Rare words like "cryptography" appear in few. IDF automatically
    down-weights common terms and boosts distinctive terms.
"""

import math
from collections import Counter


def build_vocabulary(documents):
    
    vocab = set()
    for doc in documents:
        vocab.update(doc)
    return vocab


def compute_idf(documents):
    
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
    
    if not tokens:
        return {}
    counts = Counter(tokens)
    total = len(tokens)
    return {term: cnt / total for term, cnt in counts.items()}


def tfidf_vector(tokens, idf, vocabulary=None):
    
    tf = compute_tf(tokens)
    vec = {}
    for term, tf_val in tf.items():
        if vocabulary is not None and term not in vocabulary:
            continue
        vec[term] = tf_val * idf.get(term, 0.0)
    return vec