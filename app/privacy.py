import re


SECRET_PATTERNS = [
    r"(?i)(api[_-]?key)\s*[:=]\s*[\"']?[\w\-]+[\"']?",
    r"(?i)(secret)\s*[:=]\s*[\"']?[\w\-]+[\"']?",
    r"(?i)(password)\s*[:=]\s*[\"']?[\w\-]+[\"']?",
    r"(?i)(token)\s*[:=]\s*[\"']?[\w\-]+[\"']?",
]


def redact_sensitive_data(text: str) -> str:
    """
    Redact common secrets before data can be sent externally.
    """

    for pattern in SECRET_PATTERNS:
        text = re.sub(
            pattern,
            r"\1=[REDACTED]",
            text,
        )

    return text


def prepare_cloud_context(context: str) -> str:
    """
    Prepare retrieved context for cloud reasoning.
    """

    safe_context = redact_sensitive_data(context)

    return safe_context