"""
casual.py
Rule-based casual conversation handler.

Detects non-search intents and returns friendly canned responses.
No AI used — everything is pattern-matching + templates.
"""

import random


GREETING = ["hi", "hello", "hey", "yo", "sup", "good morning",
            "good afternoon", "good evening", "hiya", "howdy"]

CASUAL = ["casual", "talk", "chat", "chill", "vibe", "relax",
          "how are you", "how's it going", "what's up", "whats up",
          "kamusta", "kumusta", "how are u", "hows you"]

THANKS = ["thank", "thanks", "ty", "salamat", "appreciate"]

BYE = ["bye", "goodbye", "see you", "see ya", "later", "exit", "quit"]

HELP = ["help", "what can you do", "how do you work",
        "what do you do", "guide me", "instructions"]

WHO = ["who are you", "what are you", "your name", "who made you"]


RESPONSES = {
    "greeting": [
        "Hey there! I'm Bobet Butterbonia. Ready to help you find a good book. What topic are you into?",
        "Hello! I'm Bobet Butterbonia. What kind of book are you looking for today?",
        "Hi! I'm Bobet Butterbonia. Tell me what you want to learn or read about ",
        "Hey! I'm Bobet Butterbonia. What's on your reading list today?",
    ],
    "casual": [
        "Of course We can just chill and talk — no school stuff, no technical explanations, no serious agenda. What's on your mind right now?",
        "Sure! I'm all ears no rush, no pressure. What's up?",
        "Totally down for a chill chat  What's going on?",
        "Cool! I'm here to talk too, not just books  What's on your mind?",
    ],
    "thanks": [
        "You're welcome! Want me to look up another book?",
        "Anytime! Just tell me when you want to search again.",
        "Happy to help!  Anything else you'd like to explore?",
    ],
    "bye": [
        "See you around! Come back anytime you need a book.",
        "Bye! Happy reading ",
        "Take care! I'll be here if you need book recommendations.",
    ],
    "help": [
        "Here's what I can do \n\n"
        "• Find books by topic — try \"beginner nursing book\"\n"
        "• Match by difficulty — say \"advanced\" or \"beginner\"\n"
        "• Filter by category — Nursing, Law, Psychology, Engineering, etc.\n"
        "• Author search — \"books by [author]\"\n\n"
        "Just type naturally — I'll figure it out!",
    ],
    
    "who": [
        "I'm Bobet Butterbonia — a rule-based NLP assistant built to help NWU students find books by describing what they want in plain English.",
        "I'm a book discovery chatbot for the NWU library. I use TF-IDF and cosine similarity — no AI APIs ",
    ],
}


def detect_intent(tokens, raw_text):
    """
    Detect what kind of message this is.
    Returns: greeting, casual, thanks, bye, help, who, or search
    """
    text = raw_text.lower()
    tset = set(tokens)

    for word in WHO:
        if word in text:
            return "who"
    for word in HELP:
        if word in text:
            return "help"
    for word in CASUAL:
        if word in text or word in tset:
            return "casual"
    for word in THANKS:
        if word in tset or word in text:
            return "thanks"
    for word in BYE:
        if word in tset:
            return "bye"
    for word in GREETING:
        if word in tset:
            return "greeting"

    return "search"


def casual_response(intent):
    """Return a random response for the given intent."""
    if intent in RESPONSES:
        return random.choice(RESPONSES[intent])
    return None