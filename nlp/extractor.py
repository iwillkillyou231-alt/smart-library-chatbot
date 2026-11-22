import json
import os
import re
from nlp.tokenizer import tokenize

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _load_json(rel_path):
    with open(os.path.join(BASE_DIR, rel_path), "r", encoding="utf-8") as f:
        return json.load(f)

DIFFICULTY_RULES = _load_json("data/difficulty_rules.json")

CATEGORIES = [
    "nursing", "medicine", "pharmacy", "psychology", "physical therapy",
    "computer science", "information technology", "mathematics", "natural sciences",
    "physics", "chemistry", "biology", "marine biology", "marine transportation",
    "marine engineering", "engineering", "civil engineering", "electrical engineering",
    "mechanical engineering", "architecture", "business", "accounting", "economics",
    "management", "marketing", "finance", "hospitality", "law", "political science",
    "criminology", "public administration", "education", "literature", "english",
    "filipino", "history", "philosophy", "religion", "communication", "sociology",
    "anthropology", "social work", "geography", "agriculture", "tourism", "reference",
    "general", "other",
]

EASIER_WORDS   = {"easier", "easy", "simpler", "simple", "beginner", "basic"}
HARDER_WORDS   = {"harder", "advanced", "expert", "deeper", "hardest", "hard", "difficult", "complex"}
FOCUS_WORDS    = {"focused", "focus", "more", "specifically"}
NEGATION_WORDS = {"not", "no", "without", "except", "exclude", "avoid"}

def detect_difficulty(tokens):
    token_set = set(tokens)
    for level in ("beginner", "intermediate", "advanced"):
        for word in DIFFICULTY_RULES.get(level, []):
            if " " in word:
                continue
            if word in token_set:
                return level
    return None

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

def detect_category(tokens):
    token_set = set(tokens)
    for cat in CATEGORIES:
        if cat in token_set or all(w in token_set for w in cat.split()):
            return cat
    return None

def detect_followup(tokens):
    tset = set(tokens)
    if tset & EASIER_WORDS:
        return "easier"
    if tset & HARDER_WORDS:
        return "harder"
    if tset & FOCUS_WORDS:
        return "focused"
    return None

def detect_negations(raw_text):
    text = raw_text.lower()
    text = text.replace("dont", "do not").replace("doesnt", "does not")
    
    negated = set()
    pattern = r"\b(?:not|no|without|except|exclude|avoid)\s+(?:(?:related|about|for|in|on|the|a|an)\s+)*([a-z0-9\-]+)"
    
    for match in re.findall(pattern, text):
        if match not in {"want", "need", "book", "books", "looking", "find"}:
            negated.add(match)
            
    return negated

def detect_limit(raw_text):
    text = raw_text.lower()
    
    # If they are asking for a call number, IGNORE numbers in the query
    if "call number" in text or "call no" in text:
        return None
        
    if "all" in text or "whole" in text:
        return 500 
        
    # Only grab numbers that are completely standalone
    numbers = re.findall(r'(?<![a-zA-Z])\b\d+\b(?![a-zA-Z])', text)
    if numbers:
        num = int(numbers[0])
        # If the number is a year (1900-2099), DO NOT treat it as a limit!
        if 1900 <= num <= 2099:
            return None
        return num
        
    return None

def detect_year(raw_text):
    text = raw_text.lower()
    # Look specifically for a 4-digit year
    match = re.search(r'\b(19\d{2}|20\d{2})\b', text)
    if match:
        return match.group(1)
    return None

def extract(raw_text, author_list=None):
    tokens = tokenize(raw_text)
    return {
        "tokens":     tokens,
        "difficulty": detect_difficulty(tokens),
        "author":     detect_author(raw_text, author_list or []),
        "category":   detect_category(tokens),
        "followup":   detect_followup(tokens),
        "negated":    sorted(detect_negations(raw_text)),
        "limit":      detect_limit(raw_text),
        "year":       detect_year(raw_text),
    }