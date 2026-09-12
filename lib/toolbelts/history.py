"""Validation and computations over an orchestrator-collected git snapshot."""
from __future__ import annotations

from collections import Counter
import calendar
from datetime import datetime
from typing import Any, Dict, List, Tuple

from lib.toolbelts.common import require_keys, require_list, require_object, require_string

SNAPSHOT_SCHEMA = "temp-agency.toolbelt-history/v1"


def _timestamp(value: Any, label: str) -> datetime:
    text = require_string(value, label)
    if not text.endswith("Z"):
        raise ValueError(f"{label} must be normalized UTC ending in Z")
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include a timezone")
    return parsed


def _years_before(value: datetime, years: int) -> datetime:
    year = value.year - years
    day = min(value.day, calendar.monthrange(year, value.month)[1])
    return value.replace(year=year, day=day)


def _origin(value: Any) -> Dict[str, Any]:
    data = require_object(value, "snapshot origin")
    required = {"source_repository", "source_commit", "window_start_utc",
                "window_end_utc", "window_years", "collector"}
    require_keys(data, required, "snapshot origin")
    require_string(data["source_repository"], "origin.source_repository")
    commit = require_string(data["source_commit"], "origin.source_commit")
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        raise ValueError("origin.source_commit must be a 40-character lowercase git hash")
    if data["window_years"] != 2:
        raise ValueError("origin.window_years must be 2")
    require_string(data["collector"], "origin.collector")
    start = _timestamp(data["window_start_utc"], "origin.window_start_utc")
    end = _timestamp(data["window_end_utc"], "origin.window_end_utc")
    if start >= end:
        raise ValueError("snapshot window start must precede end")
    if start != _years_before(end, 2):
        raise ValueError("snapshot window must span exactly two calendar years")
    return data


def _commit(value: Any, index: int, start: datetime, end: datetime) -> Dict[str, Any]:
    data = require_object(value, f"commit {index}")
    require_keys(data, {"commit", "committed_utc", "touched_files"}, f"commit {index}")
    commit = require_string(data["commit"], f"commit {index}.commit")
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        raise ValueError(f"commit {index}.commit must be a lowercase git hash")
    when = _timestamp(data["committed_utc"], f"commit {index}.committed_utc")
    if not start <= when <= end:
        raise ValueError(f"commit {index} lies outside the declared window")
    files = require_list(data["touched_files"], f"commit {index}.touched_files")
    if not all(isinstance(path, str) and path and not path.startswith("/") for path in files):
        raise ValueError(f"commit {index}.touched_files must contain relative paths")
    if files != sorted(set(files)):
        raise ValueError(f"commit {index}.touched_files must be sorted and unique")
    return data


def validate_snapshot(value: Any) -> Dict[str, Any]:
    data = require_object(value, "history snapshot")
    require_keys(data, {"schema", "origin", "limitations", "commits"}, "history snapshot")
    if data["schema"] != SNAPSHOT_SCHEMA:
        raise ValueError(f"history snapshot schema must be {SNAPSHOT_SCHEMA!r}")
    origin = _origin(data["origin"])
    limitations = require_list(data["limitations"], "snapshot limitations")
    if not limitations or not all(isinstance(item, str) and item for item in limitations):
        raise ValueError("snapshot limitations must contain non-empty strings")
    start = _timestamp(origin["window_start_utc"], "origin.window_start_utc")
    end = _timestamp(origin["window_end_utc"], "origin.window_end_utc")
    commits = [_commit(item, i, start, end)
               for i, item in enumerate(require_list(data["commits"], "commits"))]
    keys = [(item["committed_utc"], item["commit"]) for item in commits]
    if keys != sorted(keys) or len({item["commit"] for item in commits}) != len(commits):
        raise ValueError("commits must be unique and sorted by timestamp then hash")
    return data


def validate_history_config(value: Any, tool: str) -> Dict[str, Any]:
    data = require_object(value, f"{tool} config")
    common = {"schema", "window_years"}
    required = common | ({"top_n"} if tool == "churn" else {"include_zero_months"})
    require_keys(data, required, f"{tool} config")
    if data["schema"] != f"temp-agency.{tool}/v1":
        raise ValueError(f"{tool} config has unsupported schema")
    if data["window_years"] != 2:
        raise ValueError(f"{tool} window_years must be 2")
    if tool == "churn":
        top_n = data["top_n"]
        if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n < 1:
            raise ValueError("churn top_n must be an integer >= 1")
    elif not isinstance(data["include_zero_months"], bool):
        raise ValueError("seasons include_zero_months must be boolean")
    return data


def churn(snapshot: Dict[str, Any], top_n: int) -> Dict[str, Any]:
    counts = Counter(path for commit in snapshot["commits"] for path in commit["touched_files"])
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:top_n]
    return {"commits_considered": len(snapshot["commits"]),
            "distinct_files": len(counts),
            "file_touches": [{"path": path, "commit_count": count} for path, count in ranked]}


def _month_range(start: datetime, end: datetime) -> List[str]:
    year, month = start.year, start.month
    result = []
    while (year, month) <= (end.year, end.month):
        result.append(f"{year:04d}-{month:02d}")
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    return result


def seasons(snapshot: Dict[str, Any], include_zero: bool) -> Dict[str, Any]:
    origin = snapshot["origin"]
    start = _timestamp(origin["window_start_utc"], "window start")
    end = _timestamp(origin["window_end_utc"], "window end")
    counts = Counter(item["committed_utc"][:7] for item in snapshot["commits"])
    months = _month_range(start, end) if include_zero else sorted(counts)
    cadence = [{"month": month, "commit_count": counts.get(month, 0)} for month in months]
    return {"commits_considered": len(snapshot["commits"]), "monthly_cadence": cadence,
            "boundary_note": "first and last calendar months may be partial"}
