"""

Purpose:
    Extract structured preferences from a normalized user query.

      detoy met tay ano sir, about detection nu kasla "i want a book for 'nursing'" lets say sorted
"""

import json
import os
import re

from nlp.tokenizer import tokenize


# -------- load external rule files --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_json(rel_path):
    with open(os.path.join(BASE_DIR, rel_path), "r", encoding="utf-8") as f:
        return json.load(f)


DIFFICULTY_RULES = _load_json("data/difficulty_rules.json")


# Controlled categories (must match books.csv)
CATEGORIES = [
    # Health
    "nursing",
    "medicine",
    "pharmacy",
    "psychology",
    "physical therapy",

    # Sciences
    "computer science",
    "information technology",
    "mathematics",
    "natural sciences",
    "physics",
    "chemistry",
    "biology",
    "marine biology",
    "marine transportation",
    "marine engineering",

    # Engineering
    "engineering",
    "civil engineering",
    "electrical engineering",
    "mechanical engineering",
    "architecture",

    # Business
    "business",
    "accounting",
    "economics",
    "management",
    "marketing",
    "finance",
    "hospitality",

    # Law & Government
    "law",
    "political science",
    "criminology",
    "public administration",

    # Humanities
    "education",
    "literature",
    "english",
    "filipino",
    "history",
    "philosophy",
    "religion",
    "communication",

    # Social Sciences
    "sociology",
    "anthropology",
    "social work",
    "geography",

    # Other
    "agriculture",
    "tourism",
    "reference",
    "general",
    "other",
]


# Follow-up intent keywords
EASIER_WORDS   = {"easier", "easy", "simpler", "simple", "beginner", "basic"}
HARDER_WORDS   = {"harder", "advanced", "expert", "deeper"}
FOCUS_WORDS    = {"focused", "focus", "more", "specifically"}
NEGATION_WORDS = {"not", "no", "without", "except", "exclude", "avoid"}


#  difficulty detection 
def detect_difficulty(tokens):
    
    token_set = set(tokens)

    for level in ("beginner", "intermediate", "advanced"):
        for word in DIFFICULTY_RULES.get(level, []):
            if " " in word:
                continue
            if word in token_set:
                return level

    return None


# -------- author detection --------
def detect_author(raw_text, author_list):
    
    text = raw_text.lower()
    for full_name in author_list:
        for single in [a.strip().lower() for a in full_name.split(";")]:
            if not single:
                continue
            parts = single.split()
            if single in text:
                return full_name
            if len(parts) >= 2 and all(p in text for p in parts):
                return full_name
    return None


# -------- category detection --------
def detect_category(tokens):
    
    token_set = set(tokens)
    for cat in CATEGORIES:
        if cat in token_set or all(w in token_set for w in cat.split()):
            return cat
    return None


# -------- follow-up intent --------
def detect_followup(tokens):
    
    tset = set(tokens)
    if tset & EASIER_WORDS:
        return "easier"
    if tset & HARDER_WORDS:
        return "harder"
    if tset & FOCUS_WORDS:
        return "focused"
    return None


# -------- negation handling --------
def detect_negations(raw_text, tokens):
    
    normalized = raw_text.lower()
    negated = set()

    pattern = r"\b(?:not|no|without|except|avoid)\s+([a-z0-9\-]+)"
    for match in re.findall(pattern, normalized):
        negated.add(match)

    return negated


# -------- main entry --------
def extract(raw_text, author_list=None):
    
    tokens = tokenize(raw_text)
    return {
        "tokens":     tokens,
        "difficulty": detect_difficulty(tokens),
        "author":     detect_author(raw_text, author_list or []),
        "category":   detect_category(tokens),
        "followup":   detect_followup(tokens),
        "negated":    sorted(detect_negations(raw_text, tokens)),
    }


# -------- quick manual test --------
if __name__ == "__main__":
    samples = [
        "I want a beginner-friendly book about cybersecurity, especially network attacks.",
        "Advanced topics in AI, but not horror.",
        "Something easier please.",
        "Do you have anything by Alan Reyes?",
        "Books about databases without math.",
    ]
    fake_authors = ["Alan Reyes", "John Smith", "Jane Doe"]
    for s in samples:
        print(f"IN : {s}")
        print(f"OUT: {extract(s, fake_authors)}")
        print("-" * 70)