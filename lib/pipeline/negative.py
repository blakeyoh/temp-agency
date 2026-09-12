"""Frozen-wordlist leak detection shared by pipeline verification."""
from __future__ import annotations

import re
from typing import Iterable, List


def term_pattern(term: str) -> re.Pattern[str]:
    """Compile a case-insensitive whole-term pattern, including phrases."""
    if not isinstance(term, str) or not term.strip():
        raise ValueError("wordlist terms must be non-empty strings")
    return re.compile(r"(?<!\w)%s(?!\w)" % re.escape(term), re.IGNORECASE)


def leaks(text: str, words: Iterable[str]) -> List[str]:
    """Return each configured term found whole in text, preserving list order."""
    return [word for word in words if term_pattern(word).search(text)]
