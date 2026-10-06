# Project Scope — Smart Library Book Discovery Chatbot

## Group
Group 1 — CS Elective 3

## Project Title
Smart Library Book Discovery Chatbot

## Problem Statement
Students often know **what they want to learn** but not the **exact title**
of a book. Traditional library catalogs require exact-title or exact-author
searches, which fails when the student only has a topic in mind. This project
builds a natural-language interface that lets students describe what they
want in plain English and returns ranked matching books.

## Users
- Students of the school
- Library staff who want a smarter discovery tool
- Teachers recommending reading materials

## Supported Natural-Language Input

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

## Out of Scope (System Boundaries)

The system **does NOT**:

- Answer questions from inside book contents
- Digitize full copyrighted books
- Handle requests unrelated to books ("what's the weather?")
- Support languages other than English (Midterm)
- Provide live availability guarantees
- Cover every library in the country — only the approved collection

## NLP Techniques Used
- Text normalization
- Tokenization + stopword removal
- Rule-based information extraction (difficulty, author, category, negation, follow-up intent)
- Synonym / query expansion
- TF-IDF term weighting
- Cosine similarity
- Weighted scoring and ranking with explanation

## What Makes This NLP (Not Just Search)
The system does not perform exact keyword matching. It transforms
natural-language requests through a full preprocessing pipeline,
extracts structured preferences, expands vocabulary with a custom
synonym dictionary, computes statistical similarity, and produces
explainable ranked results.