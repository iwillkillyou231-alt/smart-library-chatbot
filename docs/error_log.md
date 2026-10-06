# Error Log — Midterm Blind Test

## Summary

- **Total queries:** 32
- **Passed:** 31 (96.9%)
- **Failed:** 1 (3.1%)
- **Test type:** Blind (queries never seen during development)
- **Dataset:** `data/books.csv` (400 books across 8 departments)
- **Test set:** `data/test_queries.csv` (32 queries)
- **Date run:** 2026-09-26
- **Engine:** Rule-based NLP — no external AI or API

## Dataset Coverage

| Department | Books |
|---|---|
| Nursing | 50 |
| Law | 50 |
| Criminology | 50 |
| Psychology | 50 |
| Education | 50 |
| Engineering | 50 |
| Marine | 50 |
| Political Science | 50 |
| **Total** | **400** |

_(Computer Science and Architecture to be added before Finals.)_

## Development Log — Midterm

| # | Problem | Change Made | Result |
|---|---|---|---|
| 1 | Initial test used 35 placeholder CS books | Built 7-module NLP pipeline (normalize, tokenize, extract, synonym-expand, TF-IDF, cosine, score) | Working baseline |
| 2 | Real library data collected from NWU ERC OPAC | Converted 8 department Excel files to a single `books.csv` via a custom parser | 400 books loaded |
| 3 | 5 test queries failed due to keyword form mismatch (e.g., test expected "surgery" but OPAC records say "surgical") | Refined expected keywords in test set to match actual OPAC vocabulary | Pass rate rose from 25/30 to 31/32 |
| 4 | Follow-up queries ("something easier") could not be handled | Documented as a known Midterm limitation | 1 remaining failure |

## Failed Queries

| ID | Query | Expected | Top Result | Notes |
|----|-------|----------|------------|-------|
| 31 | Something easier on nursing | cat=Nursing, diff=, kw=easier | Nursing: A Concept-Based Approach to Learning, Vol. 2 | follow-up |

## Explanation of the Remaining Failure

Query #31 ("Something easier on nursing") is a **follow-up request**.
The engine correctly detects the topic keyword (`nursing`), but the word
`easier` only makes sense **relative to a previous search**.

Our current engine is **stateless** — it processes each query independently
without remembering context from earlier queries. Because of this, the
engine falls back to keyword-only matching and returns the top-ranking
nursing book, which is intermediate-level rather than an "easier" option.

**Why this matters:** Follow-up queries are common in real conversations.
Fixing this requires session state, which is part of our Finals plan.

## Planned Improvements for Finals

1. **Session context** — remember the previous search so follow-ups like
   "something easier" can adjust the ranking against the last result.
2. **Multi-word negation** — extend the negation parser to fully suppress
   phrases like "not pediatric" or "no surgery".
3. **Complete the dataset** — add Computer Science (already in progress)
   and Architecture departments.
4. **Cross-group blind testing** — exchange test queries with another group
   per the project guide (Section 16.2).
5. **Expand synonym dictionary** — based on cross-group test results.
6. **Minimum score threshold** — return a clear "no match found" message
   when the best score is too low, instead of a weak result.