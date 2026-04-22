import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY", "").strip()
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip()

DOCS_DIR = "docs"
INDEX_FILE = "index_keyword.json"


def die(msg: str):
    raise SystemExit(f"\n[ERROR] {msg}\n")


def check_env():
    if not API_KEY:
        die("GROQ_API_KEY is missing in .env")
    if not MODEL:
        die("GROQ_MODEL is missing in .env")
    print("[OK] .env looks OK")
