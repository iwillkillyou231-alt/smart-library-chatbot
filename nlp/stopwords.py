"""
stopwords.py
Common English stopwords + domain filler words that don't help book search.
"""

STOPWORDS = {
    # core English stopwords
    "a", "an", "the", "and", "or", "but", "if", "then", "else",
    "of", "in", "on", "at", "to", "for", "from", "by", "with", "about",
    "is", "are", "was", "were", "be", "been", "being",
    "do", "does", "did", "have", "has", "had",
    "i", "me", "my", "we", "our", "you", "your", "he", "she", "it",
    "they", "them", "this", "that", "these", "those",
    "so", "as", "up", "down", "out", "over", "under", "again",
    "can", "could", "should", "would", "may", "might", "will",
    "just", "not", "no", "yes", "also", "very", "too", "more", "most",
    "some", "any", "all", "each", "every", "few", "many", "much",
    "please", "want", "need", "looking", "find", "give", "show",

    # filler / generic words that hurt topic matching
    "book", "books", "textbook", "textbooks", "guide", "guides",
    "manual", "reading", "read", "something", "anything",
    "someone", "everything", "like", "want", "wanted",
}

KEEP_WORDS = {"not"}