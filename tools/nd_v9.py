# tools/nd_v9.py
# Nd_v9 minimal reference implementation for testing and examples.
# Output: Nd ∈ [0.0, 14.0]

import math
from collections import Counter
import re

def tokenize(text):
    tokens = re.findall(r"\w+", text.lower())
    return tokens

def shannon_entropy(tokens):
    counts = Counter(tokens)
    total = sum(counts.values()) or 1
    return -sum((c/total) * math.log2(c/total) for c in counts.values())

def compressibility_estimate(text):
    tokens = tokenize(text)
    unique = len(set(tokens)) or 1
    return max(0.1, len(text) / unique)

def extract_concepts(tokens):
    return set(t for t in tokens if len(t) > 3)

def estimate_relations(concepts):
    return max(1, int(len(concepts) * 0.5))

def nd_v9(text):
    tokens = tokenize(text)
    concepts = extract_concepts(tokens)
    relations = estimate_relations(concepts)
    H = shannon_entropy(tokens)
    K = compressibility_estimate(text)
    nd_raw = math.log2(1 + (H * len(concepts) * relations) / (K + 1e-9))
    nd = max(0.0, min(14.0, nd_raw))
    return round(nd, 3)

if __name__ == "__main__":
    short_text = "Nel 1900 fu depositato un brevetto per un sistema di trasmissione radio. Il documento descrive un trasmettitore a onde corte e un ricevitore a bobina."
    long_text = " ".join([short_text] * 60)
    print("Short text Nd_v9:", nd_v9(short_text))
    print("Long text Nd_v9:", nd_v9(long_text))