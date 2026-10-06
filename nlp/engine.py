"""
engine.py
Main entry point for the NLP pipeline.

Ties together:
    normalizer -> tokenizer -> extractor -> synonym_expander
    -> tfidf -> cosine -> scorer -> ranked results

Public API:
    engine = LibraryEngine.from_csv("data/books.csv")
    results = engine.search("I want a beginner book about hacking")
"""

import csv
import os

from nlp.extractor import extract
from nlp.synonym_expander import expand
from nlp.tfidf import build_vocabulary, compute_idf, tfidf_vector
from nlp.scorer import rank_books


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA = os.path.join(BASE_DIR, "data", "books.csv")


# Which fields go into the searchable "document" for each book
SEARCH_FIELDS = ["title", "author", "category", "subcategory",
                 "description", "keywords", "toc"]


class LibraryEngine:

    def __init__(self, books):
        self.books = books
        self.authors = [b["author"] for b in books]
        self._build_index()

    # ---------- construction ----------
    @classmethod
    def from_csv(cls, path=DEFAULT_DATA):
        with open(path, "r", encoding="utf-8") as f:
            books = list(csv.DictReader(f))
        return cls(books)

    # ---------- indexing ----------
    def _book_text(self, book):
        parts = []
        for field in SEARCH_FIELDS:
            val = book.get(field, "") or ""
            # keywords have commas -> convert to spaces
            parts.append(val.replace(",", " "))
        return " ".join(parts)

    def _build_index(self):
        # Tokenize every book once
        self.book_docs = []
        for book in self.books:
            text = self._book_text(book)
            tokens = self._tokenize_for_index(text)
            self.book_docs.append(tokens)

        self.vocabulary = build_vocabulary(self.book_docs)
        self.idf = compute_idf(self.book_docs)
        self.book_vectors = [
            tfidf_vector(doc, self.idf, self.vocabulary)
            for doc in self.book_docs
        ]

    @staticmethod
    def _tokenize_for_index(text):
        """
        Index tokenizer: lowercases, splits, removes very short tokens.
        Does NOT remove stopwords — TF-IDF's IDF already handles that.
        """
        import re
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        return [t for t in text.split() if len(t) >= 2]

    # ---------- search ----------
    def search(self, query, top_n=5):
        # 1. Extract preferences
        prefs = extract(query, self.authors)

        # 2. Expand query tokens with synonyms
        expanded = expand(prefs["tokens"])

        # 3. Build query vector using the same idf + vocabulary
        query_vec = tfidf_vector(expanded, self.idf, self.vocabulary)

        # 4. Rank
        results = rank_books(self.books, query_vec, self.book_vectors,
                             prefs, top_n=top_n)

        return {
            "query": query,
            "preferences": prefs,
            "expanded_tokens": expanded,
            "results": results,
        }


# ---------- quick manual test ----------
if __name__ == "__main__":
    engine = LibraryEngine.from_csv()
    tests = [
        "I want a beginner-friendly book about cybersecurity, especially network attacks.",
        "Something advanced about machine learning",
        "Do you have books by Alan Reyes?",
        "Easy python programming book",
        "Advanced topics in AI but not horror",
    ]
    for q in tests:
        print("=" * 70)
        print(f"QUERY: {q}")
        out = engine.search(q, top_n=3)
        print(f"Prefs: {out['preferences']}")
        for i, (book, score, expl) in enumerate(out["results"], 1):
            print(f"  #{i} [{score:.3f}] {book['title']} — {book['author']}")
            for line in expl:
                print(f"        • {line}")
        print()