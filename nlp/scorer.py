"""
scorer.py
Step 7 of the NLP pipeline.

Purpose:
    Combine cosine similarity with rule-based bonuses to produce
    a final score for each book. Also generate a human-readable
    explanation of WHY a book matched.

Weights (must be defended during presentation):
    Cosine similarity .... 0.60
    Difficulty match ..... 0.20
    Category match ....... 0.10
    Author match ......... 0.10
"""

from nlp.cosine import cosine_similarity, shared_terms


WEIGHT_COSINE     = 0.60
WEIGHT_DIFFICULTY = 0.10
WEIGHT_CATEGORY   = 0.10
WEIGHT_AUTHOR     = 0.10


def score_book(book, query_vec, book_vec, prefs):
    """
    Score one book against the query.

    Args:
        book: dict — row from books.csv
        query_vec: dict {term: tfidf} for the query
        book_vec: dict {term: tfidf} for the book
        prefs: dict — output of extractor.extract()

    Returns:
        (score, explanation_list)
    """
    explanation = []

    # ---- 1. Cosine similarity ----
    cos = cosine_similarity(query_vec, book_vec)
    total = WEIGHT_COSINE * cos
    shared = shared_terms(query_vec, book_vec)
    if shared:
        explanation.append(f"TF-IDF keyword match: {', '.join(shared[:4])}")

    # ---- 2. Difficulty match ----
    if prefs.get("difficulty") and book.get("difficulty"):
        if prefs["difficulty"] == book["difficulty"]:
            total += WEIGHT_DIFFICULTY
            explanation.append(f"Difficulty matched: {book['difficulty']}")
        else:
            # small penalty if difficulty explicitly contradicts
            total -= WEIGHT_DIFFICULTY * 0.5
            explanation.append(
                f"Difficulty mismatch (wanted {prefs['difficulty']}, got {book['difficulty']})"
            )

    # ---- 3. Category match ----
    if prefs.get("category") and book.get("category"):
        if prefs["category"].lower() == book["category"].lower():
            total += WEIGHT_CATEGORY
            explanation.append(f"Category matched: {book['category']}")

    # ---- 4. Author match ----
    if prefs.get("author") and book.get("author"):
        if prefs["author"].lower() == book["author"].lower():
            total += WEIGHT_AUTHOR
            explanation.append(f"Author matched: {book['author']}")

    # ---- 5. Negation penalty ----
    negated = prefs.get("negated", set())
    if negated:
        book_text = " ".join([
            book.get("title", ""),
            book.get("description", ""),
            book.get("keywords", ""),
            book.get("subcategory", ""),
        ]).lower()
        hits = [w for w in negated if w in book_text]
        if hits:
            total -= 0.30
            explanation.append(f"Excluded terms present: {', '.join(hits)}")

    # clamp
    if total < 0:
        total = 0.0
    return total, explanation


def rank_books(books, query_vec, book_vectors, prefs, top_n=5):
    """
    Score and rank all books. Returns a list of (book, score, explanation)
    sorted by score, descending.
    """
    scored = []
    for book, book_vec in zip(books, book_vectors):
        score, explanation = score_book(book, query_vec, book_vec, prefs)
        scored.append((book, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]