"""Generate the commissioner hub's data file.

Never writes inside the repository tree. See docs/tournament/hub-design.md § 3 for why:
the data file aggregates codes, names, A/B positions and results that the packet system
deliberately keeps apart, so it must not be readable by an agent working in the repo.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
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


# A heading's trailing glyph marks origin: ◆ owner idea, ◇ not an owner idea,
# ✦ a late substitution (which may carry trailing text such as "— AMENDED").
# Keep the glyph out of the name and preserve whatever follows it as a note.
ENTRANT_RE = re.compile(
    r"^### (?P<code>[A-Z]\d+) · (?P<name>.+?)(?P<mark>\s+[◆◇✦][^\n]*)?$", re.M)
CONTRACT_RE = re.compile(r"^## (?P<code>[A-Z]\d+) · ", re.M)
STATE_RE = re.compile(r"\*\*Enactment state:\*\* \*\*(?P<body>[^*]+)\*\*")


def _blocks(pattern, text):
    """Yield (match, block) where block runs to the next match or end of text."""
    marks = list(pattern.finditer(text))
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(text)
        yield mark, text[mark.end():end]


_MD_EMPHASIS = re.compile(r"\*\*(.+?)\*\*|`([^`]+)`|\*(.+?)\*", re.S)


def _plain(text):
    """Flatten markdown emphasis so the hub renders prose, not syntax.

    field-of-32.md is authored as markdown, and the page sets text with
    textContent — never innerHTML, because entrant prose is user-authored.
    Without this a card shows a literal `**ADVANCED**` and stray backticks.

    Emphasis nests: E9's prose puts backticked code inside a bold run, and one
    substitution pass leaves the inner marks behind. Re-run until the text
    stops changing, bounded so malformed input can never spin.
    """
    for _ in range(4):
        flattened = _MD_EMPHASIS.sub(
            lambda m: m.group(1) or m.group(2) or m.group(3) or "", text)
        if flattened == text:
            return flattened
        text = flattened
    return text


def _labelled(block, label):
    """Read a `**Label:** value` or `**Label** · value` run up to the blank line."""
    found = re.search(
        rf"\*\*{re.escape(label)}:?\*\*\s*·?\s*(.+?)(?=\n\n|\Z)", block, re.S)
    return _plain(" ".join(found.group(1).split())) if found else ""


def _first_paragraph(block):
    """First prose paragraph, skipping the italic provenance line and bold labels."""
    for para in block.strip().split("\n\n"):
        para = para.strip()
        if para and not para.startswith(("*(", "**")):
            return _plain(" ".join(para.split()))
    return ""


def collect_field(text):
    """Parse field-of-32.md into {code: {code, name, owner, summary, not_native, status}}."""
    entries = {}
    for mark, block in _blocks(ENTRANT_RE, text):
        glyphs = mark.group("mark") or ""
        entries[mark.group("code")] = {
            "code": mark.group("code"),
            "name": mark.group("name").strip(),
            "owner": "◆" in glyphs,
            "note": glyphs.lstrip(" ◆◇✦—- ").strip(),
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


TAIL_ITEM_RE = re.compile(r"^(?P<n>\d+)\.\s+(?P<text>.+?)\s*$", re.M)


def collect_tail(text):
    """Parse the 24 numbered proposals out of one official source record.

    Returns [] when the section is missing or empty, so a record that has not
    been generated yet is absent rather than half-present.
    """
    match = re.search(
        r"^## Pass 1 proposal artifact\s*$\n(.*?)(?=^## )", text, re.M | re.S)
    if not match:
        return []
    items = {}
    for item in TAIL_ITEM_RE.finditer(match.group(1)):
        body = _plain(" ".join(item.group("text").split()))
        if body:
            items[int(item.group("n"))] = body
    return [items[n] for n in sorted(items)]


def preview_tail(code, scrimmage_text, size=24):
    """Build a preview proposal list from an entrant's own scrimmage output.

    Preview only. Real generated text, but from the unscored scrimmage rather
    than an official run, so it must never be presented as tournament evidence.
    Cycling past the source's length is deliberate: repetition is the thing the
    view exists to show.
    """
    lines = []
    for item in TAIL_ITEM_RE.finditer(scrimmage_text):
        body = _plain(" ".join(item.group("text").split()))
        if len(body) > 30:
            lines.append(body)
    if not lines:
        return []
    return [lines[n % len(lines)] for n in range(size)]


STAGES = ("pending", "dispatched", "recorded", "gated")


def dispatched_codes(log):
    """Entrant codes carrying a committed dispatch-log entry."""
    return {str(entry.get("entrant", "")).upper()
            for entry in log.get("entries", []) if entry.get("entrant")}


def gated_codes(report):
    """Codes whose every gate row passed. `report` is a lib.verify.gate.GateReport."""
    clean = {}
    for row in report.rows:
        code = row.entrant.upper()
        ok = row.status == "ok" and "FAIL" not in (row.replay, row.bind, row.cited)
        clean[code] = clean.get(code, True) and ok
    return {code for code, ok in clean.items() if ok}


def run_floor(codes, dispatched, recorded, gated, receipts):
    """Resolve each entrant to its furthest completed pipeline stage."""
    rows = []
    for code in codes:
        if code in gated:
            stage = "gated"
        elif code in recorded:
            stage = "recorded"
        elif code in dispatched:
            stage = "dispatched"
        else:
            stage = "pending"
        rows.append({"code": code, "stage": stage, "receipts": receipts.get(code, 0)})
    return rows


FIELD_FILE = HERE / "field-of-32.md"
CONTRACTS_FILE = HERE / "evidence-contracts-s16.md"
DRAW_FILE = HERE / "s16-draw-map.json"
DISPATCH_FILE = HERE / "dispatch-log.json"
RUNS_DIR = HERE / "official-runs"
RECEIPTS_DIR = HERE / "receipts"
SCRIMMAGES_DIR = HERE / "scrimmages"


def assemble(phase, field, states, draw, floor, tails=None, demo=False):
    """Build the payload for `phase`. Judged evidence is never read at runfloor.

    `tails` and `demo` are only ever added outside runfloor: the runfloor key set
    is a frozen contract (see AssembleTests.test_runfloor_payload_carries_state_
    and_omits_judged_evidence in test_build_hub.py), so runfloor ignores both
    arguments rather than trusting the caller not to pass them.
    """
    merged = {}
    for code, entry in field.items():
        state = states.get(code, {"state": "", "flag": ""})
        merged[code] = dict(entry, state=state["state"], flag=state["flag"])
    payload = {
        "phase": phase,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "field": merged,
        "games": draw.get("games", []),
        "panels": draw.get("panels", []),
        "floor": floor,
    }
    if phase == "runfloor":
        return payload
    if tails:
        payload["tails"] = tails
    if demo:
        payload["demo"] = True
    return payload


def emit(payload, out_dir):
    """Write hub-data.js into `out_dir`, creating it if needed."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "hub-data.js"
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    path.write_text(f"window.HUB_DATA = {blob};\n", encoding="utf-8")
    return path


RECEIPT_NAME = re.compile(r"^\d{3}-[0-9a-f]{12}\.json$")


def _receipt_counts():
    """Count issued receipts per entrant.

    Matches lib/receipt.py:20's RECEIPT_NAME exactly. A plain `*.json` glob would also
    match the `NNN-<hex>.bind.json` sidecars and double every count.
    """
    if not RECEIPTS_DIR.is_dir():
        return {}
    return {child.name.upper():
            len([f for f in child.iterdir() if RECEIPT_NAME.match(f.name)])
            for child in RECEIPTS_DIR.iterdir() if child.is_dir()}


def _recorded_codes(codes):
    return {code for code in codes if (RUNS_DIR / f"s16-{code.lower()}.md").is_file()}


def _gated(run_gate_enabled):
    if not run_gate_enabled:
        return set()
    sys.path.insert(0, str(ROOT))
    from lib.verify.gate import run_gate
    return gated_codes(run_gate(ROOT, dispatch_log="docs/tournament/dispatch-log.json"))


def _collect_tails(codes, demo):
    """Resolve each code to an official tail, falling back to a scrimmage preview.

    A code is skipped entirely when neither source yields ideas, so the hub never
    renders an empty card for an entrant that has not been generated yet.
    """
    tails = {}
    for code in codes:
        lower = code.lower()
        run_file = RUNS_DIR / f"s16-{lower}.md"
        ideas = collect_tail(run_file.read_text(encoding="utf-8")) if run_file.is_file() else []
        source = "official"
        if not ideas and demo:
            scrimmage_file = SCRIMMAGES_DIR / f"s16-{lower}.md"
            if scrimmage_file.is_file():
                ideas = preview_tail(code, scrimmage_file.read_text(encoding="utf-8"))
                source = "preview"
        if ideas:
            tails[code] = {"ideas": ideas, "source": source}
    return tails


def _tail_note(tails):
    """Render the tail-count suffix for the CLI summary line. Empty when no phase-level tails apply."""
    if not tails:
        return ""
    counts = {}
    for entry in tails.values():
        counts[entry["source"]] = counts.get(entry["source"], 0) + 1
    if len(counts) == 1:
        detail = next(iter(counts))
    else:
        detail = ", ".join(f"{n} {source}" for source, n in sorted(counts.items()))
    return f", {len(tails)} tails ({detail})"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate the commissioner hub data file.")
    parser.add_argument("--phase", required=True, choices=PHASES)
    parser.add_argument("--out", default=None,
                        help="Directory outside the repo. Defaults to ~/.cache/temp-agency/hub.")
    parser.add_argument("--gate", action="store_true",
                        help="Run bin/verify's gate to fill the gated column. Slower.")
    parser.add_argument(
        "--demo", action="store_true",
        help="Build preview tails from scrimmage text when no official run exists.")
    args = parser.parse_args(argv)

    phase = resolve_phase(args.phase)
    if args.demo and phase == "runfloor":
        raise PhaseError("runfloor carries no tails; --demo has nothing to preview")
    out_dir = resolve_out_dir(args.out)

    field = collect_field(FIELD_FILE.read_text(encoding="utf-8"))
    states = collect_states(CONTRACTS_FILE.read_text(encoding="utf-8"))
    draw = json.loads(DRAW_FILE.read_text(encoding="utf-8"))
    log = json.loads(DISPATCH_FILE.read_text(encoding="utf-8"))

    codes = [code for game in draw["games"] for code in (game["A"], game["B"])]
    floor = run_floor(codes, dispatched_codes(log), _recorded_codes(codes),
                      _gated(args.gate), _receipt_counts())

    tails = {} if phase == "runfloor" else _collect_tails(codes, args.demo)

    path = emit(assemble(phase, field, states, draw, floor, tails=tails, demo=args.demo), out_dir)
    print(f"hub-data.js: {phase} phase, {len(codes)} entrants"
          f"{_tail_note(tails)} -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
