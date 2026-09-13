"""Shared JSON loading, validation, and rendering for toolbelt tools."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Set

from lib.paths import sha256_file


def read_json(root: Path, rel: str, label: str) -> Any:
    path = Path(rel) if Path(rel).is_absolute() else root / rel
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"cannot read {label} {rel}: {exc}") from exc


def require_object(value: Any, label: str) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def require_keys(data: Dict[str, Any], required: Iterable[str], label: str,
                 optional: Iterable[str] = ()) -> None:
    required_set, allowed = set(required), set(required) | set(optional)
    missing = sorted(required_set - set(data))
    extra = sorted(set(data) - allowed)
    if missing:
        raise ValueError(f"{label} missing fields: {', '.join(missing)}")
    if extra:
        raise ValueError(f"{label} has unsupported fields: {', '.join(extra)}")


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


def require_list(value: Any, label: str) -> list:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a JSON array")
    return value


def input_provenance(root: Path, paths: Iterable[str]) -> list:
    return [{"path": rel, "sha256": sha256_file(root / rel)} for rel in paths]


def render_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
