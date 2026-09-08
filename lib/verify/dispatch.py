"""Dispatch log: the seeds and input hashes the orchestrator committed before dispatch.

Plan section 4, commit-before-reveal. An entry pins one (entrant, seed) pair to the
exact set of input files that run may read, so an agent can neither shop the seed nor
shape a pools file after seeing it (plan v4 section 11, hole 1).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

from lib.errors import HarnessError
from lib.paths import relative_to_root
from lib.tools import require_clean
from lib.verify import Line

Key = Tuple[str, int]


class DispatchLog(NamedTuple):
    given: bool
    entries: Dict[Key, Dict[str, str]]
    lines: List[Line]


NO_LOG = DispatchLog(False, {}, [])


def _entry_inputs(index: int, entry: Dict[str, Any]) -> Dict[str, str]:
    inputs = entry.get("inputs", {})
    if inputs is None:
        return {}
    if not isinstance(inputs, dict) or not all(
            isinstance(k, str) and isinstance(v, str) for k, v in inputs.items()):
        raise HarnessError(f"dispatch log entry {index} inputs must map paths to sha256 strings")
    return dict(inputs)


def _parse_entries(data: Any) -> Dict[Key, Dict[str, str]]:
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        raise HarnessError("dispatch log must be an object with an 'entries' list")
    parsed: Dict[Key, Dict[str, str]] = {}
    for index, entry in enumerate(entries):
        entrant = entry.get("entrant") if isinstance(entry, dict) else None
        seed = entry.get("seed") if isinstance(entry, dict) else None
        if not isinstance(entrant, str) or not isinstance(seed, int) or isinstance(seed, bool):
            raise HarnessError(f"dispatch log entry {index} needs a string entrant and an integer seed")
        parsed = {**parsed, (entrant, seed): _entry_inputs(index, entry)}
    return parsed


def load_dispatch_log(root: Path, path: Optional[str]) -> DispatchLog:
    """Load a committed, clean dispatch log. Problems become FAIL lines."""
    if path is None:
        return NO_LOG
    try:
        rel = relative_to_root(root, root / path)
        require_clean(root, [rel])
        data = json.loads((root / rel).read_text(encoding="utf-8"))
        return DispatchLog(True, _parse_entries(data), [Line("PASS", f"dispatch log {rel}: committed and clean")])
    except (HarnessError, OSError, ValueError) as exc:
        return DispatchLog(True, {}, [Line("FAIL", f"dispatch log {path}: {exc}")])


def _seed_under_log(receipt: Dict[str, Any], seed: Dict[str, Any],
                    log: DispatchLog, tag: str) -> Tuple[str, List[Line]]:
    source = seed.get("source")
    if source == "os-entropy":
        return "FAIL", [Line("FAIL", f"{tag}: seed source os-entropy is unattested under a dispatch log")]
    if source != "argument":
        return "FAIL", [Line("FAIL", f"{tag}: seed source {source!r} is not attestable")]
    entrant, value = str(receipt.get("entrant")), seed.get("value")
    if (entrant, value) not in log.entries:
        return "FAIL", [Line("FAIL", f"{tag}: seed not in dispatch log")]
    if (receipt.get("inputs") or {}) != log.entries[(entrant, value)]:
        return "FAIL", [Line("FAIL", f"{tag}: receipt inputs differ from dispatch log entry")]
    return "pass", [Line("PASS", f"{tag}: seed {value} in dispatch log for {entrant}; inputs match")]


def check_seed(receipt: Dict[str, Any], log: DispatchLog, tag: str) -> Tuple[str, List[Line]]:
    """Seed column value and report lines for one receipt."""
    seed = receipt.get("seed") or {}
    if seed.get("source") == "none":
        return "n/a", []
    if log.given:
        return _seed_under_log(receipt, seed, log, tag)
    if seed.get("source") == "os-entropy":
        return "unattested", [Line("WARN", f"{tag}: unattested seed (no dispatch log)")]
    return "argument", []
