"""
Weights ):
    Cosine similarity  0.60
    Difficulty match  0.20
    Category match  0.10
    Author match  0.10
"""

from nlp.cosine import cosine_similarity, shared_terms


WEIGHT_COSINE     = 0.60
WEIGHT_DIFFICULTY = 0.10
WEIGHT_CATEGORY   = 0.10
WEIGHT_AUTHOR     = 0.10


def score_book(book, query_vec, book_vec, prefs):
    
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

       # 5. Negation handling (HARD REJECT)
    negated = prefs.get("negated") or set()
    if negated:
        book_text = " ".join([
            book.get("title", ""), book.get("description", ""),
            book.get("keywords", ""), book.get("subcategory", ""),
        ]).lower()
        hits = [w for w in negated if w in book_text]
        if hits:
            # If a negated word is in the book, reject it completely
            return 0.0, [f"Excluded (negated): {', '.join(hits)}"]

    # clamp
    if total < 0:
        total = 0.0
    return total, explanation


def rank_books(books, query_vec, book_vectors, prefs, top_n=5):
   
    scored = []
    for book, book_vec in zip(books, book_vectors):
        score, explanation = score_book(book, query_vec, book_vec, prefs)
        scored.append((book, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]

    scored.sort(key=lambda x: x[1], reverse=True)
    
    # Remove hard-rejected books (score 0.0)
    scored = [s for s in scored if s[1] > 0.0]
    
    return scored[:top_n]