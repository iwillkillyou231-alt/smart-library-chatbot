import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYNONYMS_PATH = os.path.join(BASE_DIR, "data", "synonyms.json")

with open(SYNONYMS_PATH, "r", encoding="utf-8") as f:
    SYNONYMS = json.load(f)


def expand(tokens):
   
    expanded = list(tokens)
    seen = set(tokens)

    for tok in tokens:
        for syn in SYNONYMS.get(tok, []):
            # synonyms may be multi-word phrases -> split for token list
            for sub in syn.lower().split():
                if sub not in seen:
                    seen.add(sub)
                    expanded.append(sub)

    return expanded


def expand_string(text):
    return " ".join(expand(text.lower().split()))


# -------- quick manual test --------
if __name__ == "__main__":
    samples = [
        ["hacking", "beginner"],
        ["ai"],
        ["network", "advanced"],
        ["db", "easy"],
    ]
    for s in samples:
        print(f"IN : {s}")
        print(f"OUT: {expand(s)}")
        print("-" * 70)