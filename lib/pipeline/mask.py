"""C8 frozen noun masking."""
from __future__ import annotations

import re
from typing import Any, Dict, Optional

from lib.pipeline import PrepareResult
from lib.pipeline.negative import term_pattern


def _mapping(config):
    mapping = config.get("map")
    if not isinstance(mapping, dict) or not mapping:
        raise ValueError("mask config map must be a non-empty object")
    for noun, token in mapping.items():
        term_pattern(noun)
        if not isinstance(token, str) or not re.fullmatch(
                r"(?:ENTITY|MECHANISM|BEHAVIOR|PLACE|RESOURCE)_[A-Z]+", token):
            raise ValueError("invalid opaque mask token")
    if len(set(mapping.values())) != len(mapping):
        raise ValueError("mask tokens must be unique")
    if len({noun.lower() for noun in mapping}) != len(mapping):
        raise ValueError("mask nouns must be unique ignoring case")
    return mapping


def apply(brief_text: str, config: Dict[str, Any],
          persona: Optional[str]) -> PrepareResult:
    """Replace configured nouns longest-first with unique opaque tokens."""
    noun_map = _mapping(config)
    ordered = sorted(noun_map.items(), key=lambda item: len(item[0]), reverse=True)
    lookup = {noun.lower(): token for noun, token in ordered}
    pattern = re.compile(r"(?<!\w)(?:%s)(?!\w)" % "|".join(
        re.escape(noun) for noun, _token in ordered), re.IGNORECASE)
    visible, masked = pattern.subn(lambda match: lookup[match[0].lower()], brief_text)
    records = ["%s => %s" % (noun, token) for noun, token in ordered]
    records.append("masked_nouns=%d" % masked)
    return PrepareResult(visible=visible, record_lines=records)
