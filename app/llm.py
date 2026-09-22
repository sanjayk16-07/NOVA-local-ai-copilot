import ollama

MODEL_NAME = "qwen2.5:3b"


async def generate_local_answer(
    query: str,
    context: str,
) -> str:

    prompt = f"""
You are NOVA, a local-first AI developer assistant.

Answer the user's question using the project context below.

User question:
{query}

Project context:
{context}

Give a clear and concise developer-friendly answer.
Do not invent information that is not present in the context.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]


async def generate_answer(
    question: str,
    context: str,
) -> str:

    return await generate_local_answer(
        question,
        context,
    )