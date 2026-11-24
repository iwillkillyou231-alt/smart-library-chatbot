from spellchecker import SpellChecker

spell = SpellChecker()

def correct_spelling(tokens):
    corrected = []
    for t in tokens:
        if len(t) > 3 and t.isalpha():
            correction = spell.correction(t)
            corrected.append(correction if correction else t)
        else:
            corrected.append(t)
    return corrected