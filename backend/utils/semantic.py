from difflib import SequenceMatcher

def semantic_match(text1, text2):
    similarity = SequenceMatcher(
        None,
        text1.lower(),
        text2.lower()
    ).ratio()

    return round(similarity * 100, 2)