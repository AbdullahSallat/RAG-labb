import time
from typing import Dict, List

from .config import check_env
from .llm import groq_chat
from .retrieval import bm25_retrieve

def cmd_check():
    check_env()
    t0 = time.time()
    ans = groq_chat("Reply with exactly one word.", "OK")
    dt = time.time() - t0
    print("[OK] Groq replied:", ans.strip())
    print(f"[TIME] {dt:.2f}s")

def cmd_baseline(question: str):
    check_env()
    system = "You are a helpful IT support assistant. Answer in English. If you are unsure, say so."
    t0 = time.time()
    answer = groq_chat(system, question)
    dt = time.time() - t0
    print("\n=== BASELINE (no RAG) ===")
    print(answer)
    print(f"\n[TIME] {dt:.2f}s")

def cmd_rag(question: str, top_k: int = 4):
    check_env()
    hits = bm25_retrieve(question, top_k=top_k)

    if not hits:
        print("\n=== RAG (with documents) ===")
        print("I couldn't find anything in the documents that matches the question (keyword search).")
        return

    context_lines: List[str] = []
    for h in hits:
        tag = f"[{h['source']}#chunk{h['chunk_id']}]"
        context_lines.append(f"{tag}\n{h['text']}\n")
    context = "\n".join(context_lines)

    system = (
        "You are an IT support assistant. Answer in English."
        "Use the CONTEXT below to answer the QUESTION."
    )

    user = f"QUESTION:\n{question}\n\n<context>\n{context}\n</context>"

    t0 = time.time()
    answer = groq_chat(system, user)
    dt = time.time() - t0

    print("\n=== RAG (with documents) ===")
    print(answer)

    print("\n[RETRIEVED SOURCES]")
    for h in hits:
        print(f"- {h['source']}#chunk{h['chunk_id']}")

    print(f"\n[TIME] {dt:.2f}s")
