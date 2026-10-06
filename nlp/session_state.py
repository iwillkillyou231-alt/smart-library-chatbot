"""
session_state.py
Remembers the last search so the user can reply with a single word
(e.g., "Civil") to filter results by subcategory.
"""

from flask import session


def save_context(query, results, subcategories):
    """Store the last search context in the session."""
    session["last_query"] = query
    session["last_results"] = results[:10]
    session["last_subcategories"] = list(subcategories)
    session["waiting_for_filter"] = True


def get_context():
    return {
        "query":         session.get("last_query"),
        "results":       session.get("last_results", []),
        "subcategories": session.get("last_subcategories", []),
        "waiting":       session.get("waiting_for_filter", False),
    }


def clear_context():
    for key in ("last_query", "last_results",
                "last_subcategories", "waiting_for_filter"):
        session.pop(key, None)


def match_subcategory(text, subcategories):
    """
    If the user's short reply matches one of the stored subcategories,
    return the matched subcategory string. Otherwise None.

    Uses word-prefix matching (not raw substring) to avoid false matches
    like "hi" matching "leadersHIp".
    """
    if not text or not subcategories:
        return None

    text = text.lower().strip().rstrip(".!?")

    # Too short to be a real filter (avoids "hi", "ok", "no")
    if len(text) < 4:
        return None

    # Remove filler words
    for filler in ("engineering", "nursing", "book", "books", "please", "the"):
        text = text.replace(filler, "").strip()

    if len(text) < 4:
        return None

    # Exact match
    for sub in subcategories:
        if text == sub.lower():
            return sub

    # Word-level prefix match — text must be a prefix of a WORD in sub
    for sub in subcategories:
        for word in sub.lower().split():
            if word.startswith(text) and len(text) >= 4:
                return sub

    return None


def shorten_subcategories(subcategories):
    """
    If all subcategories share a common last word (like "Engineering"),
    strip it out for the display prompt.

    Returns: (short_list, common_word)
        ["Civil Engineering", "Mechanical Engineering"] -> (["Civil", "Mechanical"], "Engineering")
    """
    if len(subcategories) < 2:
        return subcategories, None

    words_list = [s.split() for s in subcategories]
    last_words = [w[-1] for w in words_list if w]

    if last_words and len(set(last_words)) == 1 and len(last_words[0]) > 2:
        common = last_words[0]
        short = [" ".join(w[:-1]) if len(w) > 1 else w[0] for w in words_list]
        return short, common

    return subcategories, None