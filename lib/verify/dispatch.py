"""Dispatch log: seeds the orchestrator committed before dispatch (plan section 4)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, NamedTuple, Optional, Tuple

from lib.errors import HarnessError
from lib.paths import relative_to_root
from lib.tools import require_clean
from lib.verify import Line


class DispatchLog(NamedTuple):
    given: bool
    seeds: Dict[str, FrozenSet[int]]
    lines: List[Line]


NO_LOG = DispatchLog(False, {}, [])


def _parse_entries(data: Any) -> Dict[str, FrozenSet[int]]:
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        raise HarnessError("dispatch log must be an object with an 'entries' list")
    seeds: Dict[str, FrozenSet[int]] = {}
    for index, entry in enumerate(entries):
        entrant, seed = entry.get("entrant"), entry.get("seed")
        if not isinstance(entrant, str) or not isinstance(seed, int) or isinstance(seed, bool):
            raise HarnessError(f"dispatch log entry {index} needs a string entrant and an integer seed")
        seeds = {**seeds, entrant: seeds.get(entrant, frozenset()) | {seed}}
    return seeds


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


def _seed_under_log(entrant: str, seed: Dict[str, Any], log: DispatchLog, tag: str) -> Tuple[str, List[Line]]:
    source = seed.get("source")
    if source == "os-entropy":
        return "FAIL", [Line("FAIL", f"{tag}: seed source os-entropy is unattested under a dispatch log")]
    if source != "argument":
        return "FAIL", [Line("FAIL", f"{tag}: seed source {source!r} is not attestable")]
    if seed.get("value") not in log.seeds.get(entrant, frozenset()):
        return "FAIL", [Line("FAIL", f"{tag}: seed not in dispatch log")]
    return "pass", [Line("PASS", f"{tag}: seed {seed.get('value')} in dispatch log for {entrant}")]


def check_seed(receipt: Dict[str, Any], log: DispatchLog, tag: str) -> Tuple[str, List[Line]]:
    """Seed column value and report lines for one receipt."""
    seed = receipt.get("seed") or {}
    if receipt.get("status") != "ok" or seed.get("source") == "none":
        return "n/a", []
    if log.given:
        return _seed_under_log(str(receipt.get("entrant")), seed, log, tag)
    if seed.get("source") == "os-entropy":
        return "unattested", [Line("WARN", f"{tag}: unattested seed (no dispatch log)")]
    return "argument", []
