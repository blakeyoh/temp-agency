#!/usr/bin/env python3
"""Collect a two-year git-history snapshot for later archive-only A3 replay.

Run this as the orchestrator, commit its JSON output before dispatch, then pass that
file to bin/churn or bin/seasons as --snapshot. The A3 tools never invoke git.
"""
from __future__ import annotations

import argparse
import calendar
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import List

TIMEOUT = 300


def git(repo: Path, *args: str, binary: bool = False):
    try:
        process = subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                                 check=True, timeout=TIMEOUT)
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        detail = getattr(exc, "stderr", b"") or b""
        raise SystemExit(f"git {' '.join(args)} failed: {detail.decode('utf-8', 'replace')}")
    return process.stdout if binary else process.stdout.decode("utf-8")


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    return parsed.astimezone(timezone.utc)


def years_before(value: datetime, years: int) -> datetime:
    year = value.year - years
    day = min(value.day, calendar.monthrange(year, value.month)[1])
    return value.replace(year=year, day=day)


def commits_in_window(repo: Path, commit: str, start: datetime, end: datetime) -> List[dict]:
    rows = []
    for line in git(repo, "log", "--format=%H%x09%cI", commit).splitlines():
        digest, raw_time = line.split("\t", 1)
        when = parse_time(raw_time)
        if start <= when <= end:
            rows.append((when, digest))
    result = []
    for when, digest in sorted(rows, key=lambda row: (row[0], row[1])):
        names = touched_files(repo, digest)
        result.append({"commit": digest, "committed_utc": when.isoformat().replace("+00:00", "Z"),
                       "touched_files": names})
    return result


def touched_files(repo: Path, commit: str) -> List[str]:
    ancestry = git(repo, "rev-list", "--parents", "-n", "1", commit).strip().split()
    if len(ancestry) == 1:
        raw = git(repo, "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "-z",
                  commit, binary=True)
    else:
        raw = git(repo, "diff", "--name-only", "-z", ancestry[1], commit, "--", binary=True)
    names = raw.decode("utf-8").split("\0")
    return sorted(set(path for path in names if path))


def source_name(repo: Path, override: str) -> str:
    if override:
        return override
    try:
        return git(repo, "remote", "get-url", "origin").strip()
    except SystemExit:
        return repo.resolve().as_posix()


def snapshot(repo: Path, revision: str, label: str) -> dict:
    commit = git(repo, "rev-parse", "--verify", f"{revision}^{{commit}}").strip()
    end = parse_time(git(repo, "show", "-s", "--format=%cI", commit))
    start = years_before(end, 2)
    return {
        "schema": "temp-agency.toolbelt-history/v1",
        "origin": {"collector": "scripts/snapshot-toolbelt-history.py/v1",
                   "source_repository": source_name(repo, label), "source_commit": commit,
                   "window_start_utc": start.isoformat().replace("+00:00", "Z"),
                   "window_end_utc": end.isoformat().replace("+00:00", "Z"), "window_years": 2},
        "limitations": [
            "Snapshot records commit timestamps and paths touched by each reachable commit; it omits diffs, authors, branches not reachable from source_commit, and working-tree changes.",
            "Each non-root commit is diffed against its first parent. Merge commits include merge-resolution changes relative to that parent, not a combined-parent view; renames are represented by reported paths without per-path git log --follow traversal.",
            "The first and last calendar-month cadence buckets can be partial because the window is anchored to the source commit timestamp.",
            "Archive replay validates only this committed snapshot and cannot inspect the source repository's .git directory.",
        ],
        "commits": commits_in_window(repo, commit, start, end),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path, help="source git repository")
    parser.add_argument("--commit", required=True, help="source commit or ref to resolve")
    parser.add_argument("--output", required=True, type=Path, help="JSON file to replace")
    parser.add_argument("--source-label", default="", help="stable source repository label")
    args = parser.parse_args()
    value = snapshot(args.repo.resolve(), args.commit, args.source_label)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {args.output} ({len(value['commits'])} commits at {value['origin']['source_commit']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
