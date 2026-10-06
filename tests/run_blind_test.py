"""
run_blind_test.py
Runs the blind test set (data/test_queries.csv) against the NLP engine
and reports which queries worked and which failed.

A query "passes" if at least one of the top-3 results matches the expected:
    - category
    - difficulty
    - any expected keyword

Usage:
    python tests/run_blind_test.py
"""

import csv
import os
import sys

# Allow imports from project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from nlp.engine import LibraryEngine


TEST_FILE = os.path.join(ROOT, "data", "test_queries.csv")
TOP_N = 3


def normalize_list(s):
    return [x.strip().lower() for x in (s or "").split(",") if x.strip()]


def book_matches(book, expected):
    """Return (passed, reasons) for one book against one test row."""
    reasons = []

    cat = (expected.get("expected_category") or "").strip().lower()
    if cat and cat not in (book.get("category", "") + " " + book.get("subcategory", "")).lower():
        return False, [f"category mismatch (wanted {cat})"]
    if cat:
        reasons.append(f"category ✓ {cat}")

    diff = (expected.get("expected_difficulty") or "").strip().lower()
    if diff and diff != book.get("difficulty", "").lower():
        return False, [f"difficulty mismatch (wanted {diff})"]
    if diff:
        reasons.append(f"difficulty ✓ {diff}")

    expected_kw = normalize_list(expected.get("expected_keywords", ""))
    if expected_kw:
        book_text = " ".join([
            book.get("title", ""),
            book.get("description", ""),
            book.get("keywords", ""),
            book.get("subcategory", ""),
        ]).lower()
        hits = [k for k in expected_kw if k in book_text]
        if not hits:
            return False, [f"keyword mismatch (wanted any of {expected_kw})"]
        reasons.append(f"keywords ✓ {hits}")

    return True, reasons


def main():
    engine = LibraryEngine.from_csv()
    print(f"📚 Engine loaded: {len(engine.books)} books")
    print(f"🧪 Running blind test set: {TEST_FILE}\n")

    with open(TEST_FILE, "r", encoding="utf-8") as f:
        tests = list(csv.DictReader(f))

    passed = 0
    failed = 0
    failures_log = []

    for t in tests:
        q = t["query"]
        out = engine.search(q, top_n=TOP_N)
        results = out["results"]

        # Did any of top-N match?
        hit = False
        match_reasons = []
        for book, score, explanation in results:
            ok, reasons = book_matches(book, t)
            if ok:
                hit = True
                match_reasons = reasons
                break

        status = "✅ PASS" if hit else "❌ FAIL"
        print(f"[{t['id']:>2}] {status}  {q}")
        if hit:
            passed += 1
            print(f"        ↳ matched on: {', '.join(match_reasons)}")
        else:
            failed += 1
            top = results[0][0]["title"] if results else "(none)"
            top_reasons = results[0][2] if results else []
            print(f"        ↳ top result: {top}")
            print(f"        ↳ reasons: {top_reasons}")
            failures_log.append({
                "id": t["id"],
                "query": q,
                "expected": f"cat={t.get('expected_category')}, diff={t.get('expected_difficulty')}, kw={t.get('expected_keywords')}",
                "top_result": top,
                "notes": t.get("notes", ""),
            })
        print()

    total = passed + failed
    print("=" * 70)
    print(f"RESULTS: {passed}/{total} passed  ({failed} failed)")
    print("=" * 70)

    # Write failure log
    log_path = os.path.join(ROOT, "docs", "error_log.md")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("# Error Log — Midterm Blind Test\n\n")
        f.write(f"**Total queries:** {total}  \n")
        f.write(f"**Passed:** {passed}  \n")
        f.write(f"**Failed:** {failed}  \n\n")
        f.write("## Failed Queries\n\n")
        if failures_log:
            f.write("| ID | Query | Expected | Top Result | Notes |\n")
            f.write("|----|-------|----------|------------|-------|\n")
            for fl in failures_log:
                f.write(f"| {fl['id']} | {fl['query']} | {fl['expected']} | {fl['top_result']} | {fl['notes']} |\n")
        else:
            f.write("_No failures._\n")
    print(f"📝 Failure log written to: {log_path}")


if __name__ == "__main__":
    main()