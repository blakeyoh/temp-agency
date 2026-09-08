"""Replay check: pin tool and inputs, re-run the tool, byte-compare stdout."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from lib.errors import HarnessError
from lib.paths import git_show_bytes, python_version, sha256_bytes, sha256_file
from lib.receipt import load
from lib.verify import Line, has_failure

REPLAY_TIMEOUT_SECONDS = 300
STDERR_EXCERPT = 300


class ReplayReport(NamedTuple):
    lines: List[Line]
    passed: bool
    attempted: bool


def _check_tool(root: Path, receipt: Dict[str, Any]) -> List[Line]:
    tool_path = root / "bin" / str(receipt.get("tool", ""))
    if not tool_path.is_file():
        return [Line("FAIL", f"tool missing: {tool_path}")]
    if sha256_file(tool_path) != receipt.get("tool_sha256"):
        return [Line("FAIL", f"tool changed since receipt: bin/{receipt.get('tool')}")]
    return [Line("PASS", f"tool_sha256 matches bin/{receipt.get('tool')}")]


def _check_input(root: Path, commit: str, rel: str, expected: str) -> List[Line]:
    target = root / rel
    if not target.is_file():
        return [Line("FAIL", f"input missing from working tree: {rel}")]
    if sha256_file(target) != expected:
        return [Line("FAIL", f"input changed in working tree: {rel}")]
    try:
        committed = sha256_bytes(git_show_bytes(root, commit, rel))
    except HarnessError as exc:
        return [Line("FAIL", f"input not readable at {commit[:12]}: {rel} ({exc})")]
    if committed != expected:
        return [Line("FAIL", f"input differs at {commit[:12]}: {rel}")]
    return [Line("PASS", f"input pinned: {rel}")]


def _check_inputs(root: Path, receipt: Dict[str, Any]) -> List[Line]:
    inputs = receipt.get("inputs") or {}
    commit = str(receipt.get("repo_commit", ""))
    lines: List[Line] = []
    for rel, expected in sorted(inputs.items()):
        lines = lines + _check_input(root, commit, rel, str(expected))
    return lines


def _check_python(receipt: Dict[str, Any]) -> List[Line]:
    recorded = receipt.get("python_version")
    current = python_version()
    if recorded != current:
        return [Line("WARN", f"python_version {recorded} at issue, {current} now")]
    return []


def _run_replay(root: Path, receipt: Dict[str, Any], receipt_path: Path) -> List[Line]:
    tool_path = root / "bin" / str(receipt.get("tool", ""))
    cmd = [sys.executable, str(tool_path), "--replay-of", str(receipt_path)]
    try:
        proc = subprocess.run(cmd, cwd=str(root), capture_output=True,
                              timeout=REPLAY_TIMEOUT_SECONDS)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [Line("FAIL", f"replay could not run: {exc}")]
    if proc.returncode != 0:
        excerpt = proc.stderr.decode("utf-8", "replace").strip()[-STDERR_EXCERPT:]
        return [Line("FAIL", f"replay exited {proc.returncode}: {excerpt}")]
    expected = str(receipt.get("output", "")).encode("utf-8")
    if proc.stdout != expected:
        return [Line("FAIL", "replay output differs from receipt output")]
    return [Line("PASS", "replay output byte-equal to receipt output")]


def check_replay(root: Path, receipt_path: Path) -> ReplayReport:
    """Verify one receipt by replay. Failed receipts are reported, not replayed."""
    receipt = load(receipt_path)
    if receipt.get("verification_class") != "replay-exact":
        note = f"{receipt.get('verification_class')} receipt (replay does not apply)"
        return ReplayReport([Line("INFO", note)], True, False)
    if receipt.get("status") != "ok":
        return ReplayReport([Line("INFO", "failed receipt (not replayable)")], True, False)
    lines = _check_tool(root, receipt) + _check_inputs(root, receipt) + _check_python(receipt)
    if has_failure(lines):
        return ReplayReport(lines, False, False)
    lines = lines + _run_replay(root, receipt, receipt_path)
    return ReplayReport(lines, not has_failure(lines), True)
