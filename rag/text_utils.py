import re
from typing import List

_word_re = re.compile(r"[A-Za-zÅÄÖåäö0-9]+", re.UNICODE)

def tokenize(s: str) -> List[str]:
    return [w.lower() for w in _word_re.findall(s)]

def chunk_text(text: str, max_chars: int = 1200, overlap: int = 200) -> List[str]:
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return []
    chunks = []
    i = 0
    while i < len(text):
        end = min(len(text), i + max_chars)
        chunk = text[i:end].strip()
        if chunk:
            chunks.append(chunk)
        i = end - overlap
        if i < 0:
            i = 0
        if end == len(text):
            break
    return chunks
