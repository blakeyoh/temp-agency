"""Replay check: extract `repo_commit`, re-run the archived tool, byte-compare stdout.

The working tree is never the subject of a replay. `git archive <repo_commit>` is
extracted to a temporary directory and the tool runs there, so a file the agent
wrote but never committed simply does not exist (plan v4 section 11, hole 1).
"""
from __future__ import annotations

import io
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional

from lib.paths import python_version, sha256_bytes, sha256_file
from lib.receipt import load
from lib.tools import argv_file_tokens
from lib.verify import Line, has_failure

REPLAY_TIMEOUT_SECONDS = 300
ARCHIVE_TIMEOUT_SECONDS = 300
STDERR_EXCERPT = 300
TOOL_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
EXTRACT_KWARGS = {"filter": "data"} if sys.version_info >= (3, 12) else {}


class ReplayReport(NamedTuple):
    lines: List[Line]
    passed: bool
    attempted: bool


def _extract(root: Path, commit: str, destination: Path) -> Optional[Line]:
    """Extract `git archive <commit>` into `destination`. Return a FAIL line or None."""
    cmd = ["git", "archive", "--format=tar", commit]
    try:
        proc = subprocess.run(cmd, cwd=str(root), capture_output=True,
                              timeout=ARCHIVE_TIMEOUT_SECONDS)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return Line("FAIL", f"git archive {commit[:12]} could not run: {exc}")
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()[-STDERR_EXCERPT:]
        return Line("FAIL", f"git archive {commit[:12]} failed: {detail}")
    try:
        with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as tar:
            tar.extractall(str(destination), **EXTRACT_KWARGS)
    except (tarfile.TarError, OSError) as exc:
        return Line("FAIL", f"cannot extract archive of {commit[:12]}: {exc}")
    return _init_repo(destination)


def _init_repo(destination: Path) -> Optional[Line]:
    """Give the extraction an empty `.git`.

    The archive carries no `.git`, so a tool issued before `make_context` stopped
    calling `git rev-parse` would walk out of the temporary directory looking for
    one. An empty repository stops that walk at the extraction root and pins the
    root to the archive. Nothing here is committed and no working-tree check runs
    during a replay.
    """
    try:
        proc = subprocess.run(["git", "init", "-q"], cwd=str(destination),
                              capture_output=True, timeout=ARCHIVE_TIMEOUT_SECONDS)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return Line("FAIL", f"cannot initialise the replay checkout: {exc}")
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()[-STDERR_EXCERPT:]
        return Line("FAIL", f"cannot initialise the replay checkout: {detail}")
    return None


def _check_tool(root: Path, archive: Path, receipt: Dict[str, Any]) -> List[Line]:
    name = str(receipt.get("tool", ""))
    if not TOOL_NAME.match(name):
        return [Line("FAIL", f"tool name is not a plain bin/ name: {name!r}")]
    archived = archive / "bin" / name
    if not archived.is_file():
        return [Line("FAIL", f"tool missing at repo_commit: bin/{name}")]
    if sha256_file(archived) != receipt.get("tool_sha256"):
        return [Line("FAIL", f"tool at repo_commit does not match receipt: bin/{name}")]
    lines = [Line("PASS", f"tool_sha256 matches bin/{name} at repo_commit")]
    working = root / "bin" / name
    if not working.is_file() or sha256_file(working) != receipt.get("tool_sha256"):
        return lines + [Line("WARN", f"bin/{name} has changed since this receipt; "
                                     "replay ran the committed version")]
    return lines


def _inside(archive: Path, rel: str) -> bool:
    """True when `rel` is a relative path that stays inside the archive."""
    if Path(rel).is_absolute():
        return False
    try:
        (archive / rel).resolve().relative_to(archive.resolve())
    except ValueError:
        return False
    return True


def _check_inputs(archive: Path, receipt: Dict[str, Any]) -> List[Line]:
    inputs = receipt.get("inputs") or {}
    short = str(receipt.get("repo_commit", ""))[:12]
    lines: List[Line] = []
    for rel, expected in sorted(inputs.items()):
        target = archive / rel
        if not _inside(archive, rel):
            lines = lines + [Line("FAIL", f"input path escapes the archive: {rel}")]
        elif not target.is_file():
            lines = lines + [Line("FAIL", f"input missing at {short}: {rel}")]
        elif sha256_file(target) != str(expected):
            lines = lines + [Line("FAIL", f"input differs at {short}: {rel}")]
        else:
            lines = lines + [Line("PASS", f"input pinned at {short}: {rel}")]
    return lines


def _check_argv(archive: Path, receipt: Dict[str, Any]) -> List[Line]:
    """Every argv token naming a real file at repo_commit must be a declared input."""
    declared = set((receipt.get("inputs") or {}).keys())
    argv = [str(token) for token in receipt.get("argv") or []]
    undeclared = [rel for rel in argv_file_tokens(archive, argv) if rel not in declared]
    if undeclared:
        return [Line("FAIL", f"argv names an undeclared file: {rel}") for rel in undeclared]
    return [Line("PASS", "argv names no file outside inputs")]


def _check_python(receipt: Dict[str, Any]) -> List[Line]:
    recorded = receipt.get("python_version")
    current = python_version()
    if recorded != current:
        return [Line("WARN", f"python_version {recorded} at issue, {current} now")]
    return []


def _run_replay(archive: Path, receipt: Dict[str, Any], receipt_path: Path) -> List[Line]:
    tool_path = archive / "bin" / str(receipt.get("tool", ""))
    cmd = [sys.executable, str(tool_path), "--replay-of", str(receipt_path)]
    try:
        proc = subprocess.run(cmd, cwd=str(archive), capture_output=True,
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


def _not_replayable(receipt: Dict[str, Any]) -> Optional[ReplayReport]:
    if receipt.get("verification_class") != "replay-exact":
        note = f"{receipt.get('verification_class')} receipt (replay does not apply)"
        return ReplayReport([Line("INFO", note)], True, False)
    if receipt.get("status") != "ok":
        return ReplayReport([Line("INFO", "failed receipt (not replayable)")], True, False)
    return None


def _in_archive(root: Path, archive: Path, receipt: Dict[str, Any],
                receipt_path: Path) -> ReplayReport:
    lines = (_check_tool(root, archive, receipt) + _check_inputs(archive, receipt)
             + _check_argv(archive, receipt) + _check_python(receipt))
    if has_failure(lines):
        return ReplayReport(lines, False, False)
    lines = lines + _run_replay(archive, receipt, receipt_path)
    return ReplayReport(lines, not has_failure(lines), True)


def check_replay(root: Path, receipt_path: Path) -> ReplayReport:
    """Verify one receipt by replay. Failed receipts are reported, not replayed."""
    path = Path(receipt_path).resolve()
    receipt = load(path)
    skip = _not_replayable(receipt)
    if skip is not None:
        return skip
    commit = str(receipt.get("repo_commit", ""))
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp).resolve()
        problem = _extract(root, commit, archive)
        if problem is not None:
            return ReplayReport([problem], False, False)
        return _in_archive(root, archive, receipt, path)
