from spellchecker import SpellChecker

spell = SpellChecker()

def correct_spelling(tokens):
    # Only correct words longer than 3 letters so we don't break words like "AI" or "JS"
    corrected = []
    for t in tokens:
        if len(t) > 3 and t.isalpha():
            correction = spell.correction(t)
            corrected.append(correction if correction else t)
        else:
            corrected.append(t)
    return corrected