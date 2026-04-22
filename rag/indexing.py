import os, glob, json
from collections import defaultdict
from typing import List, Tuple, Dict

from .config import DOCS_DIR, INDEX_FILE, die, check_env
from .text_utils import chunk_text, tokenize

def read_docs() -> List[Tuple[str, str]]:
    if not os.path.isdir(DOCS_DIR):
        die(f"Can't find the folder '{DOCS_DIR}'. Create it and add .txt files.")
    files = sorted(glob.glob(os.path.join(DOCS_DIR, "*.txt")))
    if not files:
        die(f"No .txt files found in '{DOCS_DIR}'. Add at least 2 documents.")
    docs = []
    for fp in files:
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            docs.append((os.path.basename(fp), f.read()))
    return docs

def build_index():
    check_env()
    docs = read_docs()

    chunks = []
    for fname, text in docs:
        for i, ch in enumerate(chunk_text(text)):
            tokens = tokenize(ch)
            if not tokens:
                continue
            chunks.append({
                "source": fname,
                "chunk_id": i,
                "text": ch,
                "tokens": tokens,
            })

    if not chunks:
        die("No chunks were created. Are your documents empty?")

    N = len(chunks)
    df = defaultdict(int)
    dl_sum = 0

    for c in chunks:
        dl_sum += len(c["tokens"])
        for t in set(c["tokens"]):
            df[t] += 1

    avgdl = dl_sum / N

    index = {
        "meta": {"N": N, "avgdl": avgdl},
        "df": dict(df),
        "chunks": chunks,
    }

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False)

    print(f"[OK] Index saved to {INDEX_FILE}")
    print(f"[DOCS] Documents: {len(docs)} | Chunks: {N} | avgdl: {avgdl:.1f}")

def load_index() -> Dict:
    if not os.path.isfile(INDEX_FILE):
        die(f"Can't find {INDEX_FILE}. Run: python rag_groq.py index")
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
