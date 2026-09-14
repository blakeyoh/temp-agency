"""Generate the commissioner hub's data file.

Never writes inside the repository tree. See docs/tournament/hub-design.md § 3 for why:
the data file aggregates codes, names, A/B positions and results that the packet system
deliberately keeps apart, so it must not be readable by an agent working in the repo.
"""
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PHASES = ("runfloor", "output", "mechanism")
DEFAULT_OUT = Path.home() / ".cache" / "temp-agency" / "hub"


class PhaseError(ValueError):
    """Raised when an unknown release phase is requested."""


class OutsideTreeError(ValueError):
    """Raised when the out-directory would place hub data inside the repo."""


def resolve_phase(name):
    """Return `name` if it is a known phase, else raise PhaseError."""
    if name not in PHASES:
        raise PhaseError(f"unknown phase {name!r}; expected one of {', '.join(PHASES)}")
    return name


def _is_inside(path, root):
    """True when `path` is `root` or lives under it, judged by filesystem identity.

    `Path.resolve()` normalizes symlinks, `.` and `..`, but it does not canonicalize
    case. macOS APFS is case-insensitive by default, so `/USERS/x/repo` and
    `/Users/x/repo` are one directory that compares as two different strings. A string
    comparison therefore lets a differently-cased path through the guard. Compare by
    filesystem identity instead, walking up from the nearest ancestor that exists.
    """
    probe = path
    while not probe.exists():
        if probe.parent == probe:
            return False
        probe = probe.parent
    while True:
        if probe.samefile(root):
            return True
        if probe.parent == probe:
            return False
        probe = probe.parent


def resolve_out_dir(raw):
    """Resolve the out-directory, refusing any path inside the repository tree."""
    out = Path(raw).expanduser().resolve() if raw else DEFAULT_OUT.resolve()
    if _is_inside(out, ROOT):
        raise OutsideTreeError(f"refusing to write hub data inside the repository tree: {out}")
    return out


ENTRANT_RE = re.compile(r"^### (?P<code>[A-Z]\d+) · (?P<name>.+?)(?P<owner> ◆)?$", re.M)
CONTRACT_RE = re.compile(r"^## (?P<code>[A-Z]\d+) · ", re.M)
STATE_RE = re.compile(r"\*\*Enactment state:\*\* \*\*(?P<body>[^*]+)\*\*")


def _blocks(pattern, text):
    """Yield (match, block) where block runs to the next match or end of text."""
    marks = list(pattern.finditer(text))
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(text)
        yield mark, text[mark.end():end]


def _labelled(block, label):
    """Read a `**Label:** value` or `**Label** · value` run up to the blank line."""
    found = re.search(
        rf"\*\*{re.escape(label)}:?\*\*\s*·?\s*(.+?)(?=\n\n|\Z)", block, re.S)
    return " ".join(found.group(1).split()) if found else ""


def _first_paragraph(block):
    """First prose paragraph, skipping the italic provenance line and bold labels."""
    for para in block.strip().split("\n\n"):
        para = para.strip()
        if para and not para.startswith(("*(", "**")):
            return " ".join(para.split())
    return ""


def collect_field(text):
    """Parse field-of-32.md into {code: {code, name, owner, summary, not_native, status}}."""
    entries = {}
    for mark, block in _blocks(ENTRANT_RE, text):
        entries[mark.group("code")] = {
            "code": mark.group("code"),
            "name": mark.group("name").strip(),
            "owner": bool(mark.group("owner")),
            "summary": _first_paragraph(block),
            "not_native": _labelled(block, "Not native"),
            "status": _labelled(block, "Status"),
        }
    return entries


def collect_states(text):
    """Parse evidence-contracts-s16.md into {code: {state, flag}}."""
    states = {}
    for mark, block in _blocks(CONTRACT_RE, text):
        found = STATE_RE.search(block)
        if not found:
            continue
        body = found.group("body").strip().rstrip(".")
        state, _, flag = body.partition(",")
        states[mark.group("code")] = {"state": state.strip(), "flag": flag.strip()}
    return states
