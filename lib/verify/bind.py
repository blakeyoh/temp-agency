"""Bind check: run a tool's binding rule against a record and write the sidecar."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, NamedTuple, Optional

from lib.bindings import BindResult, load_rule, rule_module_name
from lib.errors import VerifyError
from lib.paths import head_commit, relative_to_root, sha256_bytes, utc_now
from lib.receipt import load

VOLATILE_KEYS = ("checked_utc", "verifier_commit")


class BindOutcome(NamedTuple):
    result: BindResult
    sidecar_path: Path
    sidecar: Dict[str, Any]
    written: bool


def sidecar_path(receipt_path: Path) -> Path:
    name = receipt_path.name
    if not name.endswith(".json"):
        raise VerifyError(f"receipt path must end in .json: {receipt_path}")
    return receipt_path.with_name(name[:-len(".json")] + ".bind.json")


def run_check(record_bytes: bytes, receipt: Dict[str, Any]) -> BindResult:
    rule = load_rule(str(receipt.get("tool", "")))
    try:
        text = record_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerifyError(f"record is not UTF-8: {exc}") from exc
    result = rule.check(text, receipt)
    if not isinstance(result, BindResult):
        raise VerifyError(f"binding rule {rule.__name__} returned {type(result).__name__}, not BindResult")
    return result


def build_sidecar(root: Path, record_path: Path, record_bytes: bytes,
                  receipt: Dict[str, Any], result: BindResult) -> Dict[str, Any]:
    return {
        "receipt_id": receipt.get("receipt_id"),
        "record_path": relative_to_root(root, record_path),
        "artifact_sha256": sha256_bytes(record_bytes),
        "binding_rule": rule_module_name(str(receipt.get("tool", ""))),
        "bound_span": result.bound_span,
        "result": "pass" if result.passed else "fail",
        "checks": [
            {"name": c.name, "expected": c.expected, "found": c.found, "pass": c.passed}
            for c in result.checks
        ],
        "checked_utc": utc_now(),
        "verifier_commit": head_commit(root),
    }


def _load_existing(path: Path) -> Optional[Dict[str, Any]]:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def sidecar_is_current(existing: Optional[Dict[str, Any]], fresh: Dict[str, Any]) -> bool:
    """True when the stored sidecar equals the fresh one apart from volatile keys."""
    if existing is None:
        return False
    strip = lambda d: {k: v for k, v in d.items() if k not in VOLATILE_KEYS}  # noqa: E731
    return strip(existing) == strip(fresh)


def write_sidecar(path: Path, sidecar: Dict[str, Any]) -> None:
    text = json.dumps(sidecar, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")


def bind(root: Path, record_path: Path, receipt_path: Path, always_write: bool = True) -> BindOutcome:
    """Run the binding rule. Write the sidecar always, or only when stale/absent."""
    receipt = load(receipt_path)
    try:
        record_bytes = Path(record_path).read_bytes()
    except OSError as exc:
        raise VerifyError(f"cannot read record {record_path}: {exc}") from exc
    result = run_check(record_bytes, receipt)
    fresh = build_sidecar(root, Path(record_path), record_bytes, receipt, result)
    target = sidecar_path(Path(receipt_path))
    if not always_write and sidecar_is_current(_load_existing(target), fresh):
        return BindOutcome(result, target, fresh, False)
    write_sidecar(target, fresh)
    return BindOutcome(result, target, fresh, True)
