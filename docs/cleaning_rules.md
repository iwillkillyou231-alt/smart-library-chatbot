# Cleaning Rules — Smart Library Book Discovery Chatbot

## Purpose
Define exactly how raw library data is cleaned before entering the NLP engine.
Every rule must be reproducible and explainable during defense.

## Rules

### R1 — Whitespace Normalization
- Strip leading/trailing whitespace.
- Collapse multiple spaces into one.
- Remove tabs and non-breaking spaces.

### R2 — Capitalization
- `title`: Title Case (preserve original acronyms if recognizable).
- `author`: "First Last; First Last" format.
- `category`, `subcategory`, `difficulty`: lowercase for matching; original case kept in `display_*` fields if needed.

### R3 — Punctuation
- Keep commas, periods, and hyphens in `description`.
- Remove trailing periods from `title` and `author`.
- Do not remove punctuation from `description` (needed for TF-IDF tokens).

### R4 — Duplicates
- A duplicate = same `title` (case-insensitive) AND same `author`.
- Keep the record with the most complete fields.
- Log removed duplicates in `docs/removed_duplicates.log`.

### R5 — Missing Values
- Drop records missing `title`, `author`, or `description`.
- For optional fields (`toc`, `call_number`, `year`, `availability`), use empty string.

### R6 — Category Normalization
- Map variations to the controlled vocabulary:
  - "CS", "Comp Sci", "Computer science" → "Computer Science"
  - "IT", "Info Tech" → "Information Technology"
  - "Math", "Maths" → "Mathematics"

### R7 — Keywords Generation
- Source text: `title` + `description` + `subcategory` + `toc`.
- Tokenize, lowercase, remove stopwords, remove punctuation.
- Keep tokens with length ≥ 3.
- Remove pure numbers unless they are meaningful (e.g., "python3").
- Deduplicate, sort alphabetically, join with commas.

### R8 — Difficulty Assignment
Rule-based, applied after R7:
- If text contains any of: "introduction", "basics", "for beginners", "beginner", "fundamentals", "getting started" → `beginner`
- Else if text contains any of: "advanced", "graduate", "research", "in-depth", "expert" → `advanced`
- Else → `intermediate`

### R9 — Encoding
- Save all CSV files as UTF-8.
- Use comma separator, double-quote enclosure.

### R10 — Verification
- After cleaning, spot-check 10 random records against the OPAC.
- Record the check in `docs/verification_log.md`.

## Reproducibility
Any group member must be able to re-run the cleaning script
(`nlp/clean_dataset.py`) and get the same `books.csv` from the raw source.