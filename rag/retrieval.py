import math
from collections import Counter
from typing import List, Dict

from .indexing import load_index
from .text_utils import tokenize

def bm25_retrieve(query: str, top_k: int = 4, k1: float = 1.5, b: float = 0.75) -> List[Dict]:
    idx = load_index()
    N = idx["meta"]["N"]
    avgdl = idx["meta"]["avgdl"]
    df = idx["df"]
    chunks = idx["chunks"]

    q_tokens = tokenize(query)
    if not q_tokens:
        return []

    qtf = Counter(q_tokens)
    scored = []

    for c in chunks:
        doc_tokens = c["tokens"]
        dl = len(doc_tokens)
        tf = Counter(doc_tokens)

        score = 0.0
        for term, qcount in qtf.items():
            n = df.get(term, 0)
            if n == 0:
                continue
            idf = math.log(1 + (N - n + 0.5) / (n + 0.5))
            f = tf.get(term, 0)
            denom = f + k1 * (1 - b + b * (dl / avgdl))
            score += idf * (f * (k1 + 1) / denom) * qcount

        scored.append((score, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for s, c in scored[:top_k] if s > 0]
