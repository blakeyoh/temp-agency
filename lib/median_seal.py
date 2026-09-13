"""M1 git-backed median attestation validator.

verify_attestation(root, receipt) independently re-checks a seal-median
receipt against the git object store: sealed blobs at seal_commit, context
hashes, and strict ancestry of seal_commit before receipt.repo_commit.
Every failure is returned as a problem string; no exception escapes.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from lib.paths import canonical_json, git_output, sha256_bytes

TOOL_NAME = "seal-median"
ENTRANT = "M1"
VERIFICATION_CLASS = "hash-attested"
ATTESTATION_KIND = "orchestrator-git-seal"
ALLOWED_CONTEXT = ("AGENTS.md", "CLAUDE.md")
MODES = ("development", "official")
LABELS = ("FORCED", "CHOSEN")
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
HEX_64 = re.compile(r"^[0-9a-f]{64}$")


def expected_output(median: Any, seal: Dict[str, str]) -> str:
    """Canonical output the tool must emit for a validated median and seal."""
    return canonical_json({"median": median, "seal": seal})


def _bad_path(path: Any) -> bool:
    """True when path is not a safe in-repo relative POSIX path."""
    if not isinstance(path, str) or not path:
        return True
    if path.startswith("/") or path.startswith("~"):
        return True
    parts = path.split("/")
    return any(part in ("", ".", "..") for part in parts)


def _blob(root: Path, commit: str, path: str) -> Optional[bytes]:
    """Blob bytes at commit:path, or None (errors are reported by callers)."""
    try:
        data = subprocess.run(["git", "cat-file", "blob", f"{commit}:{path}"],
                              cwd=root, capture_output=True, check=True, timeout=60).stdout
    except Exception:
        return None
    return data


def _blob_sha(root: Path, commit: str, path: str) -> Optional[str]:
    data = _blob(root, commit, path)
    return sha256_bytes(data) if data is not None else None


def _is_ancestor(root: Path, older: str, newer: str) -> bool:
    try:
        git_output(root, "merge-base", "--is-ancestor", older, newer)
    except Exception:
        return False
    return True


def _commit_exists(root: Path, commit: str) -> bool:
    try:
        git_output(root, "cat-file", "-e", f"{commit}^{{commit}}")
    except Exception:
        return False
    return True


def _check_invocation(inv: Any, problems: List[str]) -> None:
    if not isinstance(inv, dict):
        problems.append("invocation blob is not a JSON object")
        return
    if type(inv.get("schema_version")) is not int or inv["schema_version"] != 1:
        problems.append("invocation schema_version must be 1")
    if inv.get("kind") != "isolated-median":
        problems.append("invocation kind must be 'isolated-median'")
    if inv.get("entrant") != ENTRANT:
        problems.append(f"invocation entrant must be {ENTRANT}")
    if inv.get("candidate_exposure") is not False:
        problems.append("invocation candidate_exposure must be exactly false")
    for key in ("actor", "model", "disclosure"):
        if not isinstance(inv.get(key), str) or not inv[key].strip():
            problems.append(f"invocation {key} must be a non-empty string")
    if inv.get("mode") not in MODES:
        problems.append(f"invocation mode must be one of {MODES}")
    brief = inv.get("brief_path")
    if _bad_path(brief):
        problems.append("invocation brief_path must be a safe in-repo path")
    if _bad_path(inv.get("median_path")):
        problems.append("invocation median_path must be a safe in-repo path")
    if not (isinstance(inv.get("median_sha256"), str)
            and HEX_64.match(inv["median_sha256"])):
        problems.append("invocation median_sha256 must be a sha256 hex string")
    files_read = inv.get("files_read")
    if not isinstance(files_read, dict):
        problems.append("invocation files_read must be an object")
        return
    for path, digest in files_read.items():
        if _bad_path(path):
            problems.append(f"files_read path {path!r} is not a safe in-repo path")
        if not (isinstance(digest, str) and HEX_64.match(digest)):
            problems.append(f"files_read hash for {path!r} must be sha256 hex")
    allowed = set(ALLOWED_CONTEXT) | ({brief} if isinstance(brief, str) else set())
    extra = sorted(set(files_read) - allowed)
    if extra:
        problems.append(f"files_read contains unexpected files (candidate exposure): {extra}")
    if isinstance(brief, str) and brief not in files_read:
        problems.append("files_read is missing brief_path")


def _check_median(median: Any, problems: List[str]) -> None:
    if not isinstance(median, dict):
        problems.append("median blob is not a JSON object")
        return
    claims = median.get("claims")
    if not isinstance(claims, list) or not claims:
        problems.append("median claims must be a non-empty list")
        return
    seen: set = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            problems.append(f"claim {index} must be an object")
            continue
        cid = claim.get("id")
        if not isinstance(cid, str) or not cid.strip():
            problems.append(f"claim {index} id must be a non-empty string")
        elif cid in seen:
            problems.append(f"claim id {cid!r} is duplicated")
        else:
            seen.add(cid)
        if claim.get("label") not in LABELS:
            problems.append(f"claim {cid!r} label must be one of {LABELS}")
        if not isinstance(claim.get("text"), str) or not claim["text"].strip():
            problems.append(f"claim {cid!r} text must be a non-empty string")


def _check_argv(receipt, median, invocation, seal_commit):
    argv = receipt.get("argv")
    if not isinstance(argv, list) or not all(isinstance(v, str) for v in argv):
        return ["argv must be a string list"]
    if len(argv) % 2:
        return ["argv must contain option-value pairs"]
    pairs = list(zip(argv[::2], argv[1::2]))
    options = dict(pairs)
    allowed = {"--entrant", "--median", "--invocation", "--seal-commit", "--seed"}
    if len(options) != len(pairs) or set(options) - allowed:
        return ["argv contains duplicate or unsupported options"]
    expected = {"--entrant": ENTRANT, "--median": median,
                "--invocation": invocation, "--seal-commit": seal_commit}
    problems = ["argv " + key + " disagrees with attestation"
                for key, value in expected.items() if options.get(key) != value]
    if "--seed" in options:
        try:
            if int(options["--seed"]) != receipt["seed"]["value"]:
                problems.append("argv seed disagrees with receipt")
        except (ValueError, KeyError, TypeError):
            problems.append("invalid argv seed")
    return problems


def verify_attestation(root: Path, receipt: Dict[str, Any]) -> List[str]:
    """Return attestation problems for one seal-median receipt; empty if valid."""
    problems: List[str] = []
    try:
        root = Path(root)
        if not isinstance(receipt, dict):
            return ["receipt is not a JSON object"]

        if receipt.get("status") != "ok":
            return ["failed receipt is not an authenticated median"]
        if receipt.get("tool") != TOOL_NAME:
            problems.append(f"receipt tool must be {TOOL_NAME!r}")
        if receipt.get("entrant") != ENTRANT:
            problems.append(f"receipt entrant must be {ENTRANT}")
        if receipt.get("verification_class") != VERIFICATION_CLASS:
            problems.append(f"verification_class must be {VERIFICATION_CLASS!r}")

        att = receipt.get("external_attestation")
        if not isinstance(att, dict):
            return problems + ["external_attestation must be an object"]
        if att.get("kind") != ATTESTATION_KIND:
            problems.append(f"attestation kind must be {ATTESTATION_KIND!r}")
        seal_commit = att.get("seal_commit")
        if not (isinstance(seal_commit, str) and FULL_SHA.match(seal_commit)):
            problems.append("seal_commit must be a full 40-hex commit id")
            seal_commit = None
        repo_commit = receipt.get("repo_commit")
        if not (isinstance(repo_commit, str) and FULL_SHA.match(repo_commit)):
            problems.append("receipt repo_commit must be a full 40-hex commit id")
            repo_commit = None

        inv_path = att.get("invocation_path")
        med_path = att.get("median_path")
        inv_sha = att.get("invocation_sha256")
        med_sha = att.get("median_sha256")
        for name, value in (("invocation_path", inv_path), ("median_path", med_path)):
            if _bad_path(value):
                problems.append(f"attestation {name} must be a safe in-repo path")
        for name, value in (("invocation_sha256", inv_sha), ("median_sha256", med_sha)):
            if not (isinstance(value, str) and HEX_64.match(value)):
                problems.append(f"attestation {name} must be a sha256 hex string")

        inputs = receipt.get("inputs")
        if not isinstance(inputs, dict):
            problems.append("receipt inputs must be an object")
            inputs = {}
        if not _bad_path(inv_path) and isinstance(inv_sha, str):
            if inputs.get(inv_path) != inv_sha:
                problems.append("receipt inputs do not pin invocation path/hash")
        if not _bad_path(med_path) and isinstance(med_sha, str):
            if inputs.get(med_path) != med_sha:
                problems.append("receipt inputs do not pin median path/hash")

        if inv_path == med_path or set(inputs) != {inv_path, med_path}:
            problems.append("receipt must pin exactly two distinct median and invocation inputs")
        problems.extend(_check_argv(receipt, med_path, inv_path, seal_commit))

        if seal_commit and repo_commit:
            if not _commit_exists(root, seal_commit):
                problems.append("seal_commit is not a commit in this repository")
            elif not _commit_exists(root, repo_commit):
                problems.append("receipt repo_commit is not a commit in this repository")
            elif seal_commit == repo_commit:
                problems.append("seal_commit must strictly predate repo_commit")
            elif not _is_ancestor(root, seal_commit, repo_commit):
                problems.append("seal_commit is not an ancestor of repo_commit")

        invocation: Any = None
        median: Any = None
        if seal_commit and not _bad_path(inv_path) and isinstance(inv_sha, str):
            actual = _blob_sha(root, seal_commit, inv_path)
            if actual is None:
                problems.append(f"no invocation blob at seal_commit:{inv_path}")
            elif actual != inv_sha:
                problems.append("invocation blob at seal_commit does not match pinned hash")
            else:
                try:
                    invocation = json.loads(_blob(root, seal_commit, inv_path).decode("utf-8"))
                except (ValueError, UnicodeDecodeError):
                    problems.append("invocation blob is not valid JSON")
        if seal_commit and not _bad_path(med_path) and isinstance(med_sha, str):
            actual = _blob_sha(root, seal_commit, med_path)
            if actual is None:
                problems.append(f"no median blob at seal_commit:{med_path}")
            elif actual != med_sha:
                problems.append("median blob at seal_commit does not match pinned hash")
            else:
                try:
                    median = json.loads(_blob(root, seal_commit, med_path).decode("utf-8"))
                except (ValueError, UnicodeDecodeError):
                    problems.append("median blob is not valid JSON")

        if invocation is not None:
            _check_invocation(invocation, problems)
            if invocation.get("median_path") != med_path:
                problems.append("invocation median_path disagrees with attestation")
            if invocation.get("median_sha256") != med_sha:
                problems.append("invocation median_sha256 disagrees with attestation")
            files_read = invocation.get("files_read")
            if isinstance(files_read, dict) and seal_commit:
                for path, digest in files_read.items():
                    if _bad_path(path) or not isinstance(digest, str):
                        continue
                    actual = _blob_sha(root, seal_commit, path)
                    if actual is None:
                        problems.append(f"no context blob at seal_commit:{path}")
                    elif actual != digest:
                        problems.append(f"context file {path} hash mismatch at seal_commit")
        if median is not None:
            _check_median(median, problems)

        if median is not None and all(
                isinstance(v, str) for v in (inv_path, inv_sha, med_path, med_sha, seal_commit)):
            seal = {
                "invocation_path": inv_path,
                "invocation_sha256": inv_sha,
                "median_path": med_path,
                "median_sha256": med_sha,
                "seal_commit": seal_commit,
            }
            if receipt.get("output") != expected_output(median, seal):
                problems.append("receipt output is not the canonical JSON of the validated median and seal")
    except Exception as exc:  # no exception may escape the validator
        problems.append(f"validator error: {type(exc).__name__}: {exc}")
    return problems
