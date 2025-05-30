from typing import Optional


def extract_reasoning_text(text: str) -> Optional[str]:
    """
    Extract the reasoning block of a reasoning model like deepseek.
    """
    if text is None:
        return None

    start_tag = "<think>"
    end_tag = "</think>"

    start_idx = text.find(start_tag) + 8
    end_idx = text.rfind(end_tag)

    return text[start_idx:end_idx]
