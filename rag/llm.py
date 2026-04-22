from groq import Groq
from .config import API_KEY, MODEL

_client = None

def groq_chat(system_prompt: str, user_prompt: str) -> str:
    global _client
    if _client is None:
        _client = Groq(api_key=API_KEY)

    resp = _client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content
