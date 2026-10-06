# Smart Library Book Discovery Chatbot

**Group 1 — CS Elective 3**
**Northwestern University**

A rule-based NLP book discovery chatbot for the NWU library.
No AI APIs, no pretrained models — everything is built from scratch.

---

## Table of Contents

1. [Project Scope](#1-project-scope)
2. [Dataset Sources](#2-dataset-sources)
3. [Data Dictionary](#3-data-dictionary)
4. [Cleaning Rules](#4-cleaning-rules)
5. [NLP Pipeline](#5-nlp-pipeline)
6. [Error Log — Midterm Blind Test](#6-error-log--midterm-blind-test)

---

## 1. Project Scope

### Group
Group 1 — CS Elective 3

### Project Title
Smart Library Book Discovery Chatbot

### Problem Statement
Students often know **what they want to learn** but not the **exact title**
of a book. Traditional library catalogs require exact-title or exact-author
searches, which fails when the student only has a topic in mind. This project
builds a natural-language interface that lets students describe what they
want in plain English and returns ranked matching books.

### Users
- Students of the school
- Library staff who want a smarter discovery tool
- Teachers recommending reading materials

### Supported Natural-Language Input

| Input Type | Example |
|---|---|
| Topic only | "I want a book about cybersecurity" |
| Topic + difficulty | "Beginner-friendly book on networking" |
| Author search | "Books by Alan Reyes" |
| Keyword focus | "Cybersecurity, especially network attacks" |
| Follow-up: easier | "Something easier" |
| Follow-up: harder | "More advanced please" |
| Follow-up: narrower | "More focused on networking" |
| Negation | "Advanced AI but not horror" |

### Out of Scope (System Boundaries)

The system **does NOT**:
- Answer questions from inside book contents
- Digitize full copyrighted books
- Handle requests unrelated to books ("what's the weather?")
- Support languages other than English (Midterm)
- Provide live availability guarantees
- Cover every library in the country — only the approved collection

### NLP Techniques Used
- Text normalization
- Tokenization + stopword removal
- Rule-based information extraction (difficulty, author, category, negation, follow-up intent)
- Synonym / query expansion
- TF-IDF term weighting
- Cosine similarity
- Weighted scoring and ranking with explanation

### What Makes This NLP (Not Just Search)
The system does not perform exact keyword matching. It transforms
natural-language requests through a full preprocessing pipeline,
extracts structured preferences, expands vocabulary with a custom
synonym dictionary, computes statistical similarity, and produces
explainable ranked results.

---

## 2. Dataset Sources

### Primary Source
- **Name**: NWU Educational Resource Center (ERC) Library OPAC
- **URL / Location**: NWU ERC OPAC portal
- **Access method**: Excel export per department
- **Date collected**: September 2026
- **Verified by**: Group 1 members

### Test Query Source (Blind Set)
- **File**: `data/test_queries.csv`
- **Authors**: Group members
- **Rule**: None of these queries appear in `books.csv` or in the dev set

### Team-Written Resources
- `data/synonyms.json` — authored by the group
- `data/difficulty_rules.json` — authored by the group

### Known Limitations
- Some records may lack `description`
- Availability may be outdated
- Categories were normalized to a controlled vocabulary; some nuance is lost

---

## 3. Data Dictionary

### Dataset Name
`books.csv` — Smart Library Book Collection (Version 1, Midterm)

### Purpose
Store the library's book records so the NLP engine can match natural-language
requests to relevant books based on topic, difficulty, author, and category.

### Number of Records
400 books across 8 departments (Nursing, Law, Criminology, Psychology,
Education, Engineering, Marine, Political Science).
Computer Science and Architecture to be added for Finals.

### Field Descriptions

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| id | int | Yes | Unique internal identifier | 1 |
| title | string | Yes | Full book title | "Introduction to Cybersecurity" |
| author | string | Yes | Author(s), separated by semicolon | "John Smith; Jane Doe" |
| category | string | Yes | Broad subject area | "Computer Science" |
| subcategory | string | No | Narrower topic | "Cybersecurity" |
| description | string | Yes | Short summary (1–3 sentences) | "A beginner's guide to protecting networks." |
| keywords | string | Yes | Team-generated keywords, comma-separated | "cybersecurity, network, security" |
| difficulty | string | Yes | Team-assigned: beginner / intermediate / advanced | "beginner" |
| call_number | string | No | Library call number | "QA76.9.A25" |
| year | int | No | Publication year | 2021 |
| toc | string | No | Table of contents (short form) | "Ch1: Intro; Ch2: Attacks" |
| availability | string | No | Current status | "available" / "borrowed" |
| location | string | No | Where to find it | "portal" / "on the shelf" |
| source | string | Yes | Where the record came from | "NWU ERC OPAC" |

### Team-Generated Fields (Important for Defense)
The following fields do **not** exist in the library catalog. They are
**generated and reviewed by the group** as part of the NLP work:

- `keywords` — extracted from title + description + subject headings,
  then expanded with synonyms by the team.
- `difficulty` — assigned using a rule-based classifier.

### Controlled Vocabulary — Categories
- Computer Science, Information Technology, Mathematics, Natural Sciences
- Engineering, Business, Education, Literature, History, Philosophy
- Psychology, Reference
- Nursing, Law, Criminology, Marine, Political Science, Architecture
- Other

---

## 4. Cleaning Rules

### Purpose
Define exactly how raw library data is cleaned before entering the NLP engine.
Every rule must be reproducible and explainable during defense.

### Rules

**R1 — Whitespace Normalization**
- Strip leading/trailing whitespace
- Collapse multiple spaces into one
- Remove tabs and non-breaking spaces

**R2 — Capitalization**
- `title`: Title Case (preserve original acronyms if recognizable)
- `author`: "First Last; First Last" format
- `category`, `subcategory`, `difficulty`: lowercase for matching

**R3 — Punctuation**
- Keep commas, periods, and hyphens in `description`
- Remove trailing periods from `title` and `author`

**R4 — Duplicates**
- A duplicate = same `title` (case-insensitive) AND same `author`
- Keep the record with the most complete fields

**R5 — Missing Values**
- Drop records missing `title`, `author`, or `description`
- For optional fields, use empty string

**R6 — Category Normalization**
- Map variations to the controlled vocabulary
- "CS", "Comp Sci" → "Computer Science"
- "IT", "Info Tech" → "Information Technology"

**R7 — Keywords Generation**
- Source text: `title` + `description` + `subcategory` + `toc`
- Tokenize, lowercase, remove stopwords, remove punctuation
- Keep tokens with length ≥ 3
- Deduplicate, sort alphabetically, join with commas

**R8 — Difficulty Assignment**
- If text contains "introduction", "basics", "beginner", "fundamentals" → `beginner`
- Else if text contains "advanced", "research", "in-depth", "expert" → `advanced`
- Else → `intermediate`

**R9 — Encoding**
- Save all CSV files as UTF-8
- Use comma separator, double-quote enclosure

**R10 — Verification**
- Spot-check 10 random records against the OPAC

### Reproducibility
Any group member can re-run the parser (`scripts/parse_library_excel.py`)
and get the same `books.csv` from the raw source files in `data/raw/`.

---

## 5. NLP Pipeline

### Overview
The system converts a natural-language book request into a ranked list of
matching books. **Every step is rule-based or statistical — no external AI
or pretrained model is used for the core NLP task.**

### Pipeline Diagram

USER INPUT (natural language)
        ↓
[1] NORMALIZER
    lowercase, expand contractions, remove punctuation
        ↓
[2] TOKENIZER
    split + remove stopwords
        ↓
[3] EXTRACTOR (rule-based)
    • difficulty (beginner / intermediate / advanced)
    • author (match vs dataset)
    • category (controlled vocabulary)
    • follow-up intent (easier / harder / focused)
    • negations (words after "not", "no", "without")
        ↓
[4] SYNONYM EXPANDER
    map tokens via data/synonyms.json
    e.g. "hacking" → cybersecurity, security, ethical
        ↓
[5] TF-IDF
    • build vocab from all books
    • idf(t) = ln((1 + N) / (1 + df(t))) + 1
    • tf(t)  = count / total
    • vector per book + query
        ↓
[6] COSINE SIMILARITY
    compare query vector to each book vector
        ↓
[7] SCORER
    +0.60 × cosine similarity
    +0.20 × difficulty match
    +0.10 × category match
    +0.10 × author match
    −0.30 × negation penalty
        ↓
[8] RANK + EXPLAIN
    sort by score
    return top N with explanation lines
```

## Step-by-Step Explanation

### Step 1 — Normalizer (`nlp/normalizer.py`)
- Converts to lowercase
- Expands contractions ("don't" → "do not")
- Removes punctuation (keeps hyphens between letters)
- Collapses whitespace

**Why:** Ensures "Beginner" and "beginner" match, and removes noise that would break tokenization.

### Step 2 — Tokenizer (`nlp/tokenizer.py`)
- Splits on whitespace
- Removes stopwords from `nlp/stopwords.py`
- Keeps tokens of length ≥ 2

**Why:** Stopwords like "the", "a", "is" don't help distinguish books.

### Step 3 — Extractor (`nlp/extractor.py`)
Detects five structured preferences:
1. **Difficulty** — matched against `data/difficulty_rules.json`
2. **Author** — matched against the dataset's author list
3. **Category** — matched against a controlled vocabulary
4. **Follow-up intent** — "easier", "harder", "more focused"
5. **Negations** — words after "not", "no", "without"

**Why:** These become bonus/penalty signals in the scorer, so the system understands "beginner book" differently from "advanced book".

### Step 4 — Synonym Expander (`nlp/synonym_expander.py`)
- Loads `data/synonyms.json`
- Expands tokens: "hacking" → cybersecurity, security, ethical
- Deduplicates

**Why:** Users may not use the exact vocabulary of the dataset.

### Step 5 — TF-IDF (`nlp/tfidf.py`)
- Builds vocabulary from all book documents
- Computes IDF with smoothing: `idf(t) = ln((1 + N) / (1 + df(t))) + 1`
- Computes TF per book: `tf(t) = count(t) / total_tokens`
- Produces a vector of `{term: tf × idf}` for the query and each book

**Why:** Rare terms (e.g., "cybersecurity") are more informative than common terms (e.g., "book").

### Step 6 — Cosine Similarity (`nlp/cosine.py`)
```
cos(a, b) = (a · b) / (||a|| × ||b||)
```
- 1.0 = identical direction (perfect match)
- 0.0 = no shared terms

**Why:** Measures similarity regardless of vector length.

### Step 7 — Scorer (`nlp/scorer.py`)
Combines signals into a final score:

| Signal | Weight |
|---|---|
| TF-IDF cosine similarity | 0.60 |
| Difficulty match | +0.20 |
| Category match | +0.10 |
| Author match | +0.10 |
| Negation hit | −0.30 |

Each book also gets an **explanation list** stating exactly which signals fired.

### Step 8 — Ranking + Explanation
Books are sorted by score. Top N are returned with:
- Match score (%)
- Which keywords matched
- Which preference matched

## Why This Counts as NLP (Not Just Search)

- **Normalization** and **tokenization** = text preprocessing
- **Stopword removal** = classic IR technique
- **Synonym expansion** = query expansion
- **Difficulty/author/category/negation extraction** = rule-based information extraction
- **TF-IDF** = statistical term weighting
- **Cosine similarity** = vector-space model

Everything is implemented by the group. No pretrained model, no API.

## Known Limitations

- Cannot understand completely out-of-scope requests ("what is the weather").
- Only handles English.
- Author detection may produce false positives if a name matches a common word.
- Negation handling is simple (only catches the word immediately after "not/no").
- Follow-up queries need session context (planned for Finals).

## Sources for Techniques

- TF-IDF: Salton & Buckley (1988), *Term-Weighting Approaches in Automatic Text Retrieval*
- Cosine similarity: standard vector-space model (Manning, Raghavan, Schütze, *Introduction to Information Retrieval*, 2008)