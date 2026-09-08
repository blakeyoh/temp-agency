"""Repository paths, git helpers, hashing, and canonical encodings."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional

from lib.errors import HarnessError

GIT_TIMEOUT_SECONDS = 60
RECEIPTS_DIR_ENV = "HARNESS_RECEIPTS_DIR"
DEFAULT_RECEIPTS_DIR = "docs/tournament/receipts"


def git_output(root: Optional[Path], *args: str) -> str:
    """Run a git command and return its stdout. Raise HarnessError on failure."""
    cmd: List[str] = ["git"] + list(args)
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(root) if root else None,
            capture_output=True,
            text=True,
            check=True,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except FileNotFoundError as exc:
        raise HarnessError("git executable not found on PATH") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()
        raise HarnessError(f"git {' '.join(args)} failed: {detail}") from exc
    return proc.stdout


def repo_root() -> Path:
    """Return the git top-level directory for the current working directory."""
    try:
        out = git_output(None, "rev-parse", "--show-toplevel")
    except HarnessError as exc:
        raise HarnessError("not inside a git repository") from exc
    return Path(out.strip()).resolve()


def receipts_dir(root: Path) -> Path:
    """The receipts directory: `HARNESS_RECEIPTS_DIR` (relative to root) or the default.

    Fixtures point the env var at their own tree so the live directory stays
    reserved for the official round.
    """
    relative = os.environ.get(RECEIPTS_DIR_ENV) or DEFAULT_RECEIPTS_DIR
    return Path(root) / relative


def head_commit(root: Path) -> str:
    return git_output(root, "rev-parse", "HEAD").strip()


def python_version() -> str:
    return "%d.%d.%d" % sys.version_info[:3]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def relative_to_root(root: Path, path: Path) -> str:
    """Return `path` as a POSIX path relative to `root`. Raise if outside."""
    resolved = Path(path).resolve()
    try:
        return resolved.relative_to(Path(root).resolve()).as_posix()
    except ValueError as exc:
        raise HarnessError(f"{path} is outside the repository root {root}") from exc
