# Data Dictionary — Smart Library Book Discovery Chatbot

## Dataset Name
`books.csv` — Smart Library Book Collection (Version 1, Midterm)

## Purpose
Store the library's book records so the NLP engine can match natural-language
requests to relevant books based on topic, difficulty, author, and category.

## Source
[School Name] Library OPAC / catalog export.
Collected by: [Your Name]
Date collected: [YYYY-MM-DD]
Date verified: [YYYY-MM-DD]
Verified by: [Librarian Name / Staff]

## Number of Records
Target for Midterm: 250+ usable records.

## Field Descriptions

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| id | int | Yes | Unique internal identifier | 1 |
| title | string | Yes | Full book title | "Introduction to Cybersecurity" |
| author | string | Yes | Author(s), separated by semicolon | "John Smith; Jane Doe" |
| category | string | Yes | Broad subject area | "Computer Science" |
| subcategory | string | No | Narrower topic | "Cybersecurity" |
| description | string | Yes | Short summary (1–3 sentences) | "A beginner's guide to protecting networks from attacks." |
| keywords | string | Yes | Team-generated keywords, comma-separated | "cybersecurity, network, beginner, security" |
| difficulty | string | Yes | Team-assigned: beginner / intermediate / advanced | "beginner" |
| call_number | string | No | Library call number | "QA76.9.A25" |
| year | int | No | Publication year | 2021 |
| toc | string | No | Table of contents (short form) | "Ch1: Intro; Ch2: Attacks" |
| availability | string | No | Current status | "Available" |
| source | string | Yes | Where the record came from | "OPAC export 2025-09-12" |

## Team-Generated Fields (Important for Defense)
The following fields do **not** exist in the library catalog. They are
**generated and reviewed by the group** as part of the NLP work:

- `keywords` — extracted from title + description + subject headings,
  then expanded with synonyms by the team.
- `difficulty` — assigned using a rule-based classifier:
  - **beginner** → contains words like "introduction", "basics", "for beginners"
  - **intermediate** → general subject matter without beginner/advanced markers
  - **advanced** → contains "advanced", "research", "graduate", "in-depth"

## Cleaning Rules Summary
1. Trim whitespace, remove double spaces.
2. Standardize capitalization: Title Case for titles, Proper Case for names.
3. Normalize categories to a controlled vocabulary (see category list).
4. Remove duplicate records (same title + same author).
5. Remove records missing `title`, `author`, or `description`.
6. Replace empty fields with an empty string, never "N/A".
7. Store `keywords` as lowercase, comma-separated, deduplicated.

## Controlled Vocabulary — Categories
Use only these categories (add new ones only if approved):
- Computer Science
- Information Technology
- Mathematics
- Natural Sciences
- Engineering
- Business
- Education
- Literature
- History
- Philosophy
- Psychology
- Reference
- Other

## Known Limitations
- Availability data may be outdated.
- Not all books have a `subcategory` or `toc`.
- Difficulty is team-assigned and may be revised between Midterm and Finals.

## Version History
| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | [YYYY-MM-DD] | Initial data dictionary | [Name] |