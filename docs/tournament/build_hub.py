"""Generate the commissioner hub's data file.

Never writes inside the repository tree. See docs/tournament/hub-design.md § 3 for why:
the data file aggregates codes, names, A/B positions and results that the packet system
deliberately keeps apart, so it must not be readable by an agent working in the repo.
"""
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


def resolve_out_dir(raw):
    """Resolve the out-directory, refusing any path inside the repository tree."""
    out = Path(raw).expanduser().resolve() if raw else DEFAULT_OUT.resolve()
    try:
        out.relative_to(ROOT)
    except ValueError:
        return out
    raise OutsideTreeError(f"refusing to write hub data inside the repository tree: {out}")
