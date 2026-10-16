import math

def cosine_similarity(vec_a, vec_b):
   
    if not vec_a or not vec_b:
        return 0.0

    # Dot product: only iteate over shared terms
    dot = 0.0
    for term, val_a in vec_a.items():
        val_b = vec_b.get(term)
        if val_b is not None:
            dot += val_a * val_b

    if dot == 0.0:
        return 0.0

    # Magnitudes
    mag_a = math.sqrt(sum(v * v for v in vec_a.values()))
    mag_b = math.sqrt(sum(v * v for v in vec_b.values()))

    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0

    return dot / (mag_a * mag_b)


def shared_terms(vec_a, vec_b):
   
    shared = []
    for term in vec_a:
        if term in vec_b:
            shared.append((term, vec_a[term] * vec_b[term]))
    shared.sort(key=lambda x: x[1], reverse=True)
    return [term for term, _ in shared]