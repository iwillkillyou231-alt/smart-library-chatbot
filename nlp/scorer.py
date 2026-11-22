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
            total -= WEIGHT_DIFFICULTY * 0.5
            explanation.append(f"Difficulty mismatch (wanted {prefs['difficulty']}, got {book['difficulty']})")

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

                # 4.5 Year match (HARD REJECT)
    if prefs.get("year"):
        book_year = str(book.get("year", "")).strip()
        if book_year != str(prefs["year"]):
            return 0.0, [f"Excluded (wrong year: {book_year})"]

    # 5. Negation handling (HARD REJECT)
    negated = prefs.get("negated") or set()
    if negated:
        # ADDED "category" here to ensure nursing books are rejected!
        book_text = " ".join([
            book.get("title", ""), 
            book.get("description", ""),
            book.get("keywords", ""), 
            book.get("subcategory", ""),
            book.get("category", ""), # <--- THIS FIXES NURSING
        ]).lower()
        
        hits = [w for w in negated if w in book_text]
        if hits:
            return 0.0, [f"Excluded (negated): {', '.join(hits)}"]

    if total < 0:
        total = 0.0
    return total, explanation


def rank_books(books, query_vec, book_vectors, prefs, top_n=5):
    scored = []
    for book, book_vec in zip(books, book_vectors):
        score, explanation = score_book(book, query_vec, book_vec, prefs)
        scored.append((book, score, explanation))
    
    scored.sort(key=lambda x: x[1], reverse=True)
    
    # NEW: If the user asked for a specific limit (like "10 books" or "300 books"),
    # OR if they asked for a huge number, bypass the score filter.
    if prefs.get("limit") or top_n >= 100:
        filtered = scored
    else:
        filtered = [s for s in scored if s[1] > 0.0]
    
    return filtered[:top_n]