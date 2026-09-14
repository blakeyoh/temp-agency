"""Generate the commissioner hub's data file.

Never writes inside the repository tree. See docs/tournament/hub-design.md § 3 for why:
the data file aggregates codes, names, A/B positions and results that the packet system
deliberately keeps apart, so it must not be readable by an agent working in the repo.
"""
import os
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
