"""Deterministic pre-persona context adapters."""
from __future__ import annotations

from typing import Any, Dict, List, NamedTuple, Optional


class PrepareResult(NamedTuple):
    """The text a persona may see and its inspectable transformation record."""

    visible: str
    record_lines: List[str]


def run(adapter: str, brief_text: str, config: Dict[str, Any],
        persona: Optional[str]) -> PrepareResult:
    """Run one named adapter over a brief using only its committed config."""
    from lib.pipeline import mask, transform, withhold

    if not isinstance(config, dict):
        raise ValueError("pipeline config must be an object")
    adapters = {
        "transform": transform.apply,
        "mask": mask.apply,
        "withhold": withhold.apply,
    }
    if adapter not in adapters:
        raise ValueError("unknown pipeline adapter: %s" % adapter)
    return adapters[adapter](brief_text, config, persona)
