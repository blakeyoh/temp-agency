"""A5 targeted withholding without printing the sealed fact."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Optional

from lib.pipeline import PrepareResult
from lib.pipeline.negative import term_pattern


def apply(brief_text: str, config: Dict[str, Any],
          persona: Optional[str]) -> PrepareResult:
    """Remove the selected exact span once and emit only safe audit metadata."""
    name = config.get("condition")
    conditions = config.get("conditions", {})
    if not isinstance(conditions, dict) or name not in conditions:
        raise ValueError("withhold config names an unknown condition")
    condition = conditions[name]
    if not isinstance(condition, dict):
        raise ValueError("withhold condition must be an object")
    span = condition.get("withhold")
    if not isinstance(span, str) or not span or brief_text.count(span) != 1:
        raise ValueError("withheld span must occur exactly once")
    visible = brief_text.replace(span, "", 1)
    digest = hashlib.sha256(span.encode("utf-8")).hexdigest()
    negative = condition.get("negative_words", [])
    if not isinstance(negative, list) or not negative:
        raise ValueError("negative_words must be a non-empty list")
    for word in negative:
        term_pattern(word)
    if not isinstance(condition.get("key"), str) or not condition["key"].strip():
        raise ValueError("withhold condition must seal a key")
    records = [
        "condition=%s" % name,
        "withheld_sha256=%s" % digest,
        "negative_words=%s" % json.dumps(negative, ensure_ascii=False),
    ]
    return PrepareResult(visible=visible, record_lines=records)
