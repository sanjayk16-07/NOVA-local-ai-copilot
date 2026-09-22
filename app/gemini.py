import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_BASE_URL = os.getenv(
    "GEMINI_BASE_URL",
    "https://llm.hidevs.xyz/v1"
)
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


async def generate_gemini_answer(
    question: str,
    context: str,
) -> str:

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    prompt = f"""
You are NOVA, a privacy-first AI developer assistant.

Answer the user's question using only the provided project context.

Rules:
- Do not invent files or code.
- If the context is insufficient, say so.
- Keep the answer concise and useful.
- Never reveal secrets or credentials.

User question:
{question}

Relevant project context:
{context}
"""

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GEMINI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{GEMINI_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
        )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]