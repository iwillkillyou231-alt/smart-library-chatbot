import csv
import os

from nlp.extractor import extract
from nlp.synonym_expander import expand
from nlp.tfidf import build_vocabulary, compute_idf, tfidf_vector
from nlp.scorer import rank_books
from nlp.spell_corrector import correct_spelling

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA = os.path.join(BASE_DIR, "data", "books.csv")

# FIXED: changed "call number" to "call_number"
SEARCH_FIELDS = ["title", "author", "category", "subcategory",
                 "description", "keywords", "toc", "call_number"]


class LibraryEngine:

    def __init__(self, books):
        self.books = books
        self.authors = [b["author"] for b in books]
        self._build_index()

    @classmethod
    def from_csv(cls, path=DEFAULT_DATA):
        with open(path, "r", encoding="utf-8") as f:
            books = list(csv.DictReader(f))
        return cls(books)

    def _book_text(self, book):
        parts = []
        for field in SEARCH_FIELDS:
            val = book.get(field, "") or ""
            parts.append(val.replace(",", " "))
        return " ".join(parts)

    def _build_index(self):
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
        import re
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        return [t for t in text.split() if len(t) >= 2]

    # ---------- search ----------
    def search(self, query, top_n=5):
        # 1. Extract preferences
        prefs = extract(query, self.authors)

                # --- 1. Check for Exact Call Number Match ---
        if prefs.get("call_number"):
            target_cn = prefs["call_number"].replace(" ", "").lower()
            print(f"DEBUG: Looking for call number -> '{target_cn}'")
            
            exact_call = [
                b for b in self.books 
                if b.get('call_number', '').replace(" ", "").lower() == target_cn
            ]
            
            if exact_call:
                print("DEBUG: FOUND IT!")
                return {
                    "query": query,
                    "preferences": prefs,
                    "expanded_tokens": [],
                    "results": [(exact_call[0], 1.0, ["Exact call number match"])]
                }
            else:
                print("DEBUG: NOT FOUND IN CSV")
                # NEW: If they search for a call number and it's wrong, return NOTHING.
                return {
                    "query": query,
                    "preferences": prefs,
                    "expanded_tokens": [],
                    "results": [] 
                }

        # --- 2. Check for Exact Title Match ---
        exact_matches = [
            b for b in self.books 
            if b['title'].strip().lower() == query.strip().lower()
        ]
        if exact_matches:
            return {
                "query": query,
                "preferences": prefs,
                "expanded_tokens": [],
                "results": [(exact_matches[0], 1.0, ["Exact title match"])]
            }

        # --- 3. Override top_n if the user asked for a specific number or "all" ---
        if prefs.get("limit"):
            top_n = prefs["limit"]

        # --- 4. Correct Spelling ---
        corrected_tokens = correct_spelling(prefs["tokens"])

        # --- 5. Expand query tokens with synonyms ---
        expanded = expand(corrected_tokens)

        # --- 6. Build query vector ---
        query_vec = tfidf_vector(expanded, self.idf, self.vocabulary)

        # --- 7. Rank ---
        results = rank_books(self.books, query_vec, self.book_vectors,
                             prefs, top_n=top_n)

        return {
            "query": query,
            "preferences": prefs,
            "expanded_tokens": expanded,
            "results": results,
        }