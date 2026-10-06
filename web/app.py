"""
app.py
Flask web server for the Smart Library Book Discovery Chatbot.

Routes:
    GET  /              -> chat UI
    POST /api/search    -> accepts {"query": "..."} returns ranked results
                           Also handles casual chat + subcategory filters.
"""

import os
import sys

# --- allow "from nlp.engine import ..." when running from web/ ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, request, jsonify, render_template
from nlp.engine import LibraryEngine
from nlp.extractor import extract
from nlp.casual import detect_intent, casual_response
from nlp.session_state import (
    save_context, get_context, clear_context,
    match_subcategory, shorten_subcategories,
)


app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
)
app.secret_key = "smart-library-secret-key-change-me"

# Build the engine once at startup
print("📚 Loading library dataset...")
engine = LibraryEngine.from_csv()
print(f"✅ Loaded {len(engine.books)} books. Vocabulary size: {len(engine.vocabulary)}")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/search", methods=["POST"])
def search():
    try:
        data = request.get_json(force=True)
        query = (data.get("query") or "").strip()
        if not query:
            return jsonify({"error": "Empty query"}), 400

        # -------- 1. Is this a subcategory filter reply? --------
        ctx = get_context()
        if ctx["waiting"] and ctx["subcategories"]:
            matched = match_subcategory(query, ctx["subcategories"])
            if matched:
                filtered = [
                    r for r in ctx["results"]
                    if matched.lower() in r.get("subcategory", "").lower()
                ]
                clear_context()
                return jsonify({
                    "query":       query,
                    "intent":      "filtered",
                    "casual":      False,
                    "filtered_by": matched,
                    "preferences": {},
                    "results":     filtered,
                })
            # If the user changed topic, fall through to a fresh search
            clear_context()

        # -------- 2. Casual / off-topic intent --------
                # -------- 2. Casual / off-topic intent --------
        prefs = extract(query, engine.authors)
        intent = detect_intent(prefs["tokens"], query)
        if intent != "search":
            reply = casual_response(intent)

            # Convert `negated` set to list for JSON
            prefs_safe = dict(prefs)
            if isinstance(prefs_safe.get("negated"), set):
                prefs_safe["negated"] = sorted(prefs_safe["negated"])

            return jsonify({
                "query":       query,
                "intent":      intent,
                "casual":      True,
                "reply":       reply,
                "results":     [],
                "preferences": prefs_safe,
            })

        # -------- 3. Run the search --------
        top_n = int(data.get("top_n", 8))
        out = engine.search(query, top_n=top_n)

        results = []
        for book, score, explanation in out["results"]:
            results.append({
                "title":         book.get("title", ""),
                "author":        book.get("author", ""),
                "category":      book.get("category", ""),
                "subcategory":   book.get("subcategory", ""),
                "difficulty":    book.get("difficulty", ""),
                "call_number":   book.get("call_number", ""),
                "year":          book.get("year", ""),
                "availability":  book.get("availability", ""),
                "location":      book.get("location", ""),
                "description":   book.get("description", ""),
                "score":         round(score, 4),
                "score_percent": round(score * 100, 1),
                "explanation":   explanation,
            })

        # Fix JSON serialization for `negated` set
        prefs_out = dict(out["preferences"])
        if isinstance(prefs_out.get("negated"), set):
            prefs_out["negated"] = sorted(prefs_out["negated"])

        # -------- 4. Should we prompt for subcategory filtering? --------
        subcats = list(dict.fromkeys(
            r["subcategory"] for r in results if r["subcategory"]
        ))
        query_lower = query.lower()
        query_already_specific = any(sc.lower() in query_lower for sc in subcats)

        should_prompt = (
            len(subcats) >= 2
            and not query_already_specific
            and len(results) >= 3
            and results[0]["score"] > 0.10
        )

        if should_prompt:
            save_context(query, results, subcats)
            short_list, common_word = shorten_subcategories(subcats)
            return jsonify({
                "query":       out["query"],
                "intent":      "search_with_prompt",
                "casual":      False,
                "preferences": prefs_out,
                "results":     results,
                "prompt": {
                    "count":         len(results),
                    "subcategories": subcats,
                    "short_list":    short_list,
                    "common_word":   common_word,
                },
            })

        clear_context()
        return jsonify({
            "query":       out["query"],
            "intent":      "search",
            "casual":      False,
            "preferences": prefs_out,
            "results":     results,
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting server at http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)