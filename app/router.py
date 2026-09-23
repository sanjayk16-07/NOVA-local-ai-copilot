def choose_model(query: str) -> str:
    """
    Decide whether NOVA should use local Qwen
    or cloud Gemini.
    """

    query_lower = query.lower()

    complex_keywords = [
        "architecture",
        "refactor entire",
        "analyze project",
        "multiple files",
        "compare",
        "optimize entire",
        "design",
        "debug entire",
    ]

    for keyword in complex_keywords:
        if keyword in query_lower:
            return "cloud"

    # Use Gemini for normal queries while local Ollama is unavailable
    return "cloud"