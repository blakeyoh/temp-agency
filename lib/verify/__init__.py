"""Verifier logic behind bin/verify: replay, bind, and the all-receipts gate."""
from __future__ import annotations

from typing import List, NamedTuple


class Line(NamedTuple):
    """One report line. level is PASS, FAIL, WARN, or INFO."""

    level: str
    message: str


def has_failure(lines: List[Line]) -> bool:
    return any(line.level == "FAIL" for line in lines)
