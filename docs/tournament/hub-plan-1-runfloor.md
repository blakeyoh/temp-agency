# Tournament Hub — Plan 1: Run Floor

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the phase of the commissioner hub that works before any judging happens — a
generator plus three views the commissioner can use while running the sixteen Sweet 16 games.

**Architecture:** A stdlib Python generator (`build_hub.py`) reads repo state and writes one
`hub-data.js` to a directory outside the working tree. An authored, committed shell renders it.
The shell is inert without the data file, so the repo never holds tournament evidence in a
greppable form during a live round.

**Tech Stack:** Python 3.13 (`~/.cache/temp-agency/harness-py313/bin/python`), `unittest`,
vanilla HTML/CSS/JS with no build step and no dependencies.

**Spec:** `docs/tournament/hub-design.md`

## Global Constraints

- Run every Python command with `~/.cache/temp-agency/harness-py313/bin/python`. System
  `python3` is 3.9 and fails harness tests.
- No third-party dependencies. Importing repo modules under `lib/` is allowed and precedented
  by `build_s16_packets.py`.
- Every file stays under 400 lines.
- The generated data file must never be written inside the repository tree. Task 1 enforces
  this in code.
- The committed shell must contain no entrant name, and must never assign `window.HUB_DATA`.
  Task 5 enforces this with a test.
- At `--phase runfloor` the payload carries field, draw and run-floor state only. No
  proposals, no yield evidence, no axis scores, no tally.
- Tests are `unittest.TestCase` classes living beside the module in `docs/tournament/`,
  matching `test_build_s16_packets.py`.
- The page is theme-aware (light and dark), and must not scroll horizontally at 400px width.
- Commit messages use `<type>: <description>`. No attribution lines.

## Scope

This plan covers the `runfloor` phase only. Plan 2 adds the Tail Reader at `--phase output`.
Plan 3 adds the Split Decision, Panel Feedback, Desk and ruling composer at
`--phase mechanism`. Each plan produces working software on its own.

## File Structure

| File | Responsibility |
|---|---|
| `docs/tournament/build_hub.py` | Generator. Phase gate, out-of-tree guard, readers, assembly, emission. |
| `docs/tournament/test_build_hub.py` | Tests for all of the above. |
| `docs/tournament/hub/index.html` | Shell. Loads data, styles and scripts in order. |
| `docs/tournament/hub/hub.css` | Tokens, chrome, editorial type, responsive rules. |
| `docs/tournament/hub/chrome.js` | Matchup switcher, phase banner, view routing. |
| `docs/tournament/hub/views/runfloor.js` | Sixteen-row pipeline table. |
| `docs/tournament/hub/views/bracket.js` | Eight game cards. |
| `docs/tournament/hub/views/entrant.js` | Entrant card panel. |
| `.gitignore` | Belt-and-braces guard against a mis-run generator. |

---

### Task 1: Phase gate and out-of-tree guard

This is the contamination guard from spec § 3. It lands first so nothing else can be written
without it.

**Files:**
- Create: `docs/tournament/build_hub.py`
- Test: `docs/tournament/test_build_hub.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `HERE: Path`, `ROOT: Path`, `PHASES: tuple[str, ...]`, `DEFAULT_OUT: Path`,
  `PhaseError(ValueError)`, `OutsideTreeError(ValueError)`, `resolve_phase(name: str) -> str`,
  `resolve_out_dir(raw: str | None) -> Path`.

- [ ] **Step 1: Write the failing test**

Create `docs/tournament/test_build_hub.py`:

```python
"""Tests for the commissioner hub generator."""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_hub as hub


class GuardTests(unittest.TestCase):
    def test_refuses_an_out_dir_inside_the_repo_tree(self):
        inside = str(hub.ROOT / "docs" / "tournament" / "hub")
        with self.assertRaisesRegex(hub.OutsideTreeError, "inside the repository tree"):
            hub.resolve_out_dir(inside)

    def test_accepts_an_out_dir_outside_the_repo_tree(self):
        self.assertEqual(hub.resolve_out_dir("/tmp/hub-out").name, "hub-out")

    def test_default_out_dir_is_outside_the_repo_tree(self):
        with self.assertRaises(ValueError):
            hub.resolve_out_dir(None).relative_to(hub.ROOT)

    def test_rejects_an_unknown_phase(self):
        with self.assertRaisesRegex(hub.PhaseError, "unknown phase"):
            hub.resolve_phase("everything")

    def test_accepts_each_known_phase(self):
        for phase in ("runfloor", "output", "mechanism"):
            self.assertEqual(hub.resolve_phase(phase), phase)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
~/.cache/temp-agency/harness-py313/bin/python -m pytest docs/tournament/test_build_hub.py -q
```

Expected: collection error, `ModuleNotFoundError: No module named 'build_hub'`.

- [ ] **Step 3: Write the minimal implementation**

Create `docs/tournament/build_hub.py`:

```python
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
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
~/.cache/temp-agency/harness-py313/bin/python -m pytest docs/tournament/test_build_hub.py -q
```

Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add docs/tournament/build_hub.py docs/tournament/test_build_hub.py
git commit -m "feat: guard hub data against the repo tree"
```

---

### Task 2: Field and contract readers

**Files:**
- Modify: `docs/tournament/build_hub.py`
- Modify: `docs/tournament/test_build_hub.py`

**Interfaces:**
- Consumes: Task 1's module.
- Produces: `collect_field(text: str) -> dict[str, dict]` where each value has keys
  `code`, `name`, `owner` (bool), `summary`, `not_native`, `status`.
  `collect_states(text: str) -> dict[str, dict]` where each value has keys `state` and `flag`.

Conventions verified against the live files: `field-of-32.md` uses `### CODE · Name` and marks
owner ideas with a trailing `◆` (11 of them, matching `box-score.html`'s `o: 1`).
`evidence-contracts-s16.md` uses `## CODE · Name` and writes
`- **Enactment state:** **MANUAL PROTOTYPE, DEFECT UNRESOLVED.**`, so the state carries an
optional qualifier after a comma.

- [ ] **Step 1: Write the failing test**

Append to `docs/tournament/test_build_hub.py`, above the `__main__` block:

```python
FIELD_FIXTURE = """### E1 · The Entropy Well ◆
*(owner idea 2, split: "scripts and shells")*

Randomness in this repo is currently rhetorical. Make it literal and seeded.

**Not native:** models simulate randomness by reaching for the most-likely option.

**Status** · **ADVANCED → Sweet 16** — Dog G6, 18–13, panels 2–1.

### A5 · The Hostile Environment

Remove a capability the persona depends on.

**Not native:** a model asked to work without a tool narrates the loss.

**Status** · **ADVANCED → Sweet 16** — Moat G10, 21–9.
"""

CONTRACT_FIXTURE = """## E1 · The Entropy Well

- **Enactment state:** **MANUAL PROTOTYPE.** The PRNG is cheap.

## A5 · The Hostile Environment

- **Enactment state:** **PROMISE, DEFECT UNRESOLVED.** No general mechanism yet.
"""


class FieldReaderTests(unittest.TestCase):
    def test_reads_code_name_and_owner_mark(self):
        field = hub.collect_field(FIELD_FIXTURE)
        self.assertEqual(set(field), {"E1", "A5"})
        self.assertEqual(field["E1"]["name"], "The Entropy Well")
        self.assertTrue(field["E1"]["owner"])
        self.assertFalse(field["A5"]["owner"])

    def test_reads_summary_skipping_the_provenance_italics(self):
        field = hub.collect_field(FIELD_FIXTURE)
        self.assertTrue(field["E1"]["summary"].startswith("Randomness in this repo"))

    def test_reads_labelled_sections_in_both_shapes(self):
        field = hub.collect_field(FIELD_FIXTURE)
        self.assertTrue(field["E1"]["not_native"].startswith("models simulate"))
        self.assertIn("ADVANCED", field["E1"]["status"])


class ContractReaderTests(unittest.TestCase):
    def test_splits_state_from_its_qualifier(self):
        states = hub.collect_states(CONTRACT_FIXTURE)
        self.assertEqual(states["E1"], {"state": "MANUAL PROTOTYPE", "flag": ""})
        self.assertEqual(states["A5"], {"state": "PROMISE", "flag": "DEFECT UNRESOLVED"})

    def test_reads_every_entrant_in_the_real_contracts_file(self):
        text = (hub.HERE / "evidence-contracts-s16.md").read_text(encoding="utf-8")
        states = hub.collect_states(text)
        # 17, not 16: M3 keeps its contract section after Ruling 22 moved it to the
        # wildcard bench. Verify with: grep -c '^## [A-Z][0-9]* ·' evidence-contracts-s16.md
        self.assertEqual(len(states), 17)
        for value in states.values():
            self.assertIn(value["state"], ("RUNNABLE", "MANUAL PROTOTYPE", "PROMISE"))
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
~/.cache/temp-agency/harness-py313/bin/python -m pytest docs/tournament/test_build_hub.py -q
```

Expected: FAIL with `AttributeError: module 'build_hub' has no attribute 'collect_field'`.

- [ ] **Step 3: Write the minimal implementation**

Add to `docs/tournament/build_hub.py`, after the guards. Add `import re` to the imports.

```python
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
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
~/.cache/temp-agency/harness-py313/bin/python -m pytest docs/tournament/test_build_hub.py -q
```

Expected: 10 passed.

- [ ] **Step 5: Commit**

```bash
git add docs/tournament/build_hub.py docs/tournament/test_build_hub.py
git commit -m "feat: read the field and evidence contracts for the hub"
```

---

### Task 3: Run-floor state deriver

Stages follow the pipeline in `HANDOFF.md` "Next session: run the Sweet 16. Exact order."
step 3: freeze inputs and commit a dispatch entry, run the tool, generate, write the source
record, then pass `bin/verify all`.

**Files:**
- Modify: `docs/tournament/build_hub.py`
- Modify: `docs/tournament/test_build_hub.py`

**Interfaces:**
- Consumes: Task 2's module.
- Produces: `STAGES: tuple[str, ...]`, `dispatched_codes(log: dict) -> set[str]`,
  `gated_codes(report) -> set[str]` taking a `lib.verify.gate.GateReport`,
  `run_floor(codes, dispatched, recorded, gated, receipts) -> list[dict]` returning rows with
  keys `code`, `stage`, `receipts`.

- [ ] **Step 1: Write the failing test**

Append to `docs/tournament/test_build_hub.py`:

```python
class Row:
    """Stand-in for lib.verify.gate.Row carrying only the fields gated_codes reads."""

    def __init__(self, entrant, status="ok", replay="pass", bind="pass", cited="pass"):
        self.entrant = entrant
        self.status = status
        self.replay = replay
        self.bind = bind
        self.cited = cited


class Report:
    def __init__(self, rows):
        self.rows = rows


class RunFloorTests(unittest.TestCase):
    def test_pending_when_nothing_has_happened(self):
        rows = hub.run_floor(["E1"], set(), set(), set(), {})
        self.assertEqual(rows, [{"code": "E1", "stage": "pending", "receipts": 0}])

    def test_stage_climbs_with_each_completed_step(self):
        codes = ["E1", "A5", "C8", "M1"]
        rows = hub.run_floor(codes, {"E1", "A5", "C8", "M1"}, {"A5", "C8", "M1"},
                             {"C8", "M1"}, {"M1": 3})
        self.assertEqual([r["stage"] for r in rows],
                         ["dispatched", "recorded", "gated", "gated"])
        self.assertEqual(rows[3]["receipts"], 3)

    def test_reads_dispatched_codes_from_the_log(self):
        log = {"entries": [{"entrant": "e1", "seed": 7}, {"entrant": "A5"}]}
        self.assertEqual(hub.dispatched_codes(log), {"E1", "A5"})

    def test_empty_dispatch_log_yields_no_codes(self):
        self.assertEqual(hub.dispatched_codes({"entries": []}), set())

    def test_gated_codes_excludes_any_entrant_with_a_failing_row(self):
        report = Report([Row("E1"), Row("A5", replay="FAIL"), Row("E1")])
        self.assertEqual(hub.gated_codes(report), {"E1"})

    def test_gated_codes_excludes_a_failed_status(self):
        report = Report([Row("C8", status="failed")])
        self.assertEqual(hub.gated_codes(report), set())
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
~/.cache/temp-agency/harness-py313/bin/python -m pytest docs/tournament/test_build_hub.py -q
```

Expected: FAIL with `AttributeError: module 'build_hub' has no attribute 'run_floor'`.

- [ ] **Step 3: Write the minimal implementation**

Add to `docs/tournament/build_hub.py`:

```python
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
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
~/.cache/temp-agency/harness-py313/bin/python -m pytest docs/tournament/test_build_hub.py -q
```

Expected: 16 passed.

- [ ] **Step 5: Commit**

```bash
git add docs/tournament/build_hub.py docs/tournament/test_build_hub.py
git commit -m "feat: derive run-floor stages from repo state"
```

---

### Task 4: Assembly, emission and the omission guard

**Files:**
- Modify: `docs/tournament/build_hub.py`
- Modify: `docs/tournament/test_build_hub.py`

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: `assemble(phase, field, states, draw, floor) -> dict` with keys
  `phase`, `generated`, `field`, `games`, `panels`, `floor`.
  `emit(payload: dict, out_dir: Path) -> Path` writing `hub-data.js`.
  `main(argv=None) -> int` wiring `--phase`, `--out` and `--gate`.

- [ ] **Step 1: Write the failing test**

Append to `docs/tournament/test_build_hub.py`. Add `import json` and `import tempfile` to the
imports at the top of the file.

```python
DRAW_FIXTURE = {
    "seed": 372500925,
    "games": [{"g": 1, "pair": ["A1", "E4"], "A": "A1", "B": "E4", "region": "Sweet 16"}],
    "panels": [{"name": "Builder", "file_tag": "builder", "lead": "nuclear-reactor-operator",
                "lens": "magician-illusionist", "fresh": False}],
}


class AssembleTests(unittest.TestCase):
    def payload(self):
        return hub.assemble(
            "runfloor",
            hub.collect_field(FIELD_FIXTURE),
            hub.collect_states(CONTRACT_FIXTURE),
            DRAW_FIXTURE,
            hub.run_floor(["E1", "A5"], {"E1"}, set(), set(), {}),
        )

    def test_carries_field_games_panels_and_floor(self):
        payload = self.payload()
        self.assertEqual(payload["phase"], "runfloor")
        self.assertEqual(len(payload["games"]), 1)
        self.assertEqual(payload["panels"][0]["name"], "Builder")
        self.assertEqual(len(payload["floor"]), 2)

    def test_merges_enactment_state_into_the_field(self):
        self.assertEqual(self.payload()["field"]["A5"]["state"], "PROMISE")
        self.assertEqual(self.payload()["field"]["A5"]["flag"], "DEFECT UNRESOLVED")

    def test_runfloor_payload_omits_all_judged_evidence(self):
        payload = self.payload()
        self.assertNotIn("proposals", payload)
        self.assertNotIn("results", payload)
        blob = json.dumps(payload, ensure_ascii=False)
        for leak in ("Distance", "Irreducibility", "Compounding", "Generative failure",
                     "ABSORBED", "ORTHOGONAL", "STRONGEST"):
            self.assertNotIn(leak, blob)

    def test_emit_writes_a_single_global_assignment(self):
        with tempfile.TemporaryDirectory() as temp:
            path = hub.emit({"phase": "runfloor"}, hub.Path(temp) / "out")
            text = path.read_text(encoding="utf-8")
        self.assertEqual(path.name, "hub-data.js")
        self.assertTrue(text.startswith("window.HUB_DATA = {"))
        self.assertTrue(text.rstrip().endswith("};"))

    def test_main_refuses_an_out_dir_inside_the_repo(self):
        inside = str(hub.ROOT / "docs" / "tournament" / "hub")
        with self.assertRaises(hub.OutsideTreeError):
            hub.main(["--phase", "runfloor", "--out", inside])
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
~/.cache/temp-agency/harness-py313/bin/python -m pytest docs/tournament/test_build_hub.py -q
```

Expected: FAIL with `AttributeError: module 'build_hub' has no attribute 'assemble'`.

- [ ] **Step 3: Write the minimal implementation**

Add to `docs/tournament/build_hub.py`. Add `import argparse`, `import json`, `import sys` and
`from datetime import datetime, timezone` to the imports.

```python
FIELD_FILE = HERE / "field-of-32.md"
CONTRACTS_FILE = HERE / "evidence-contracts-s16.md"
DRAW_FILE = HERE / "s16-draw-map.json"
DISPATCH_FILE = HERE / "dispatch-log.json"
RUNS_DIR = HERE / "official-runs"
RECEIPTS_DIR = HERE / "receipts"


def assemble(phase, field, states, draw, floor):
    """Build the payload for `phase`. Judged evidence is never read at runfloor."""
    merged = {}
    for code, entry in field.items():
        state = states.get(code, {"state": "", "flag": ""})
        merged[code] = dict(entry, state=state["state"], flag=state["flag"])
    return {
        "phase": phase,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "field": merged,
        "games": draw.get("games", []),
        "panels": draw.get("panels", []),
        "floor": floor,
    }


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


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate the commissioner hub data file.")
    parser.add_argument("--phase", required=True, choices=PHASES)
    parser.add_argument("--out", default=None,
                        help="Directory outside the repo. Defaults to ~/.cache/temp-agency/hub.")
    parser.add_argument("--gate", action="store_true",
                        help="Run bin/verify's gate to fill the gated column. Slower.")
    args = parser.parse_args(argv)

    phase = resolve_phase(args.phase)
    out_dir = resolve_out_dir(args.out)

    field = collect_field(FIELD_FILE.read_text(encoding="utf-8"))
    states = collect_states(CONTRACTS_FILE.read_text(encoding="utf-8"))
    draw = json.loads(DRAW_FILE.read_text(encoding="utf-8"))
    log = json.loads(DISPATCH_FILE.read_text(encoding="utf-8"))

    codes = [code for game in draw["games"] for code in (game["A"], game["B"])]
    floor = run_floor(codes, dispatched_codes(log), _recorded_codes(codes),
                      _gated(args.gate), _receipt_counts())

    path = emit(assemble(phase, field, states, draw, floor), out_dir)
    print(f"hub-data.js: {phase} phase, {len(codes)} entrants -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
~/.cache/temp-agency/harness-py313/bin/python -m pytest docs/tournament/test_build_hub.py -q
```

Expected: 21 passed.

- [ ] **Step 5: Run the generator against the real repo**

```bash
~/.cache/temp-agency/harness-py313/bin/python docs/tournament/build_hub.py --phase runfloor
```

Expected: `hub-data.js: runfloor phase, 16 entrants -> /Users/<you>/.cache/temp-agency/hub/hub-data.js`.
Confirm the repo is still clean:

```bash
git status --short
```

Expected: no untracked or modified files beyond the two you are about to commit.

- [ ] **Step 6: Commit**

```bash
git add docs/tournament/build_hub.py docs/tournament/test_build_hub.py
git commit -m "feat: assemble and emit the runfloor hub payload"
```

---

### Task 5: Shell, styles and chrome

**Files:**
- Create: `docs/tournament/hub/index.html`
- Create: `docs/tournament/hub/hub.css`
- Create: `docs/tournament/hub/chrome.js`
- Modify: `.gitignore`
- Modify: `docs/tournament/test_build_hub.py`

**Interfaces:**
- Consumes: `window.HUB_DATA` from Task 4.
- Produces: `window.HUB.mount(root)`, `window.HUB.state` holding `{view, game}`,
  `window.HUB.register(name, render)` where `render(container, data, state)` draws one view,
  `window.HUB.go(view, game)` switching subject or view and re-rendering.

Colors reuse the tokens already in `box-score.html:17-23` so the hub and the box score read as
one family.

- [ ] **Step 1: Write the failing test**

Append to `docs/tournament/test_build_hub.py`:

```python
class ShellTests(unittest.TestCase):
    def committed_files(self):
        hub_dir = hub.HERE / "hub"
        return [hub_dir / "index.html", hub_dir / "hub.css", hub_dir / "chrome.js"] + \
            sorted((hub_dir / "views").glob("*.js"))

    def test_the_committed_shell_never_assigns_hub_data(self):
        for path in self.committed_files():
            with self.subTest(path=path.name):
                self.assertNotRegex(path.read_text(encoding="utf-8"),
                                    r"window\.HUB_DATA\s*=")

    def test_the_committed_shell_names_no_entrant(self):
        field = hub.collect_field(hub.FIELD_FILE.read_text(encoding="utf-8"))
        names = [entry["name"] for entry in field.values()]
        for path in self.committed_files():
            text = path.read_text(encoding="utf-8")
            for name in names:
                with self.subTest(path=path.name, name=name):
                    self.assertNotIn(name, text)
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
~/.cache/temp-agency/harness-py313/bin/python -m pytest docs/tournament/test_build_hub.py -q
```

Expected: FAIL with `FileNotFoundError` for `hub/index.html`.

- [ ] **Step 3: Write the shell**

Create `docs/tournament/hub/index.html`:

```html
<title>The 99th Idea Bracket — Hub</title>
<link rel="stylesheet" href="hub.css">
<div id="hub"><noscript>This hub needs JavaScript.</noscript></div>
<script src="hub-data.js"></script>
<script src="chrome.js"></script>
<script src="views/runfloor.js"></script>
<script src="views/bracket.js"></script>
<script src="views/entrant.js"></script>
<script>window.HUB.mount(document.getElementById("hub"));</script>
```

Create `docs/tournament/hub/hub.css`:

```css
:root {
  --paper: #F6F7F6; --paper-sunk: #DFE3E3; --ground: #ECEEEE;
  --ink: #191C1F; --ink-2: #4A5257; --ink-3: #737C81;
  --rule: #C8CFCF; --live: #B4462A; --ok: #2F6B4F;
  --f-display: ui-serif, Georgia, serif;
  --f-body: ui-sans-serif, system-ui, sans-serif;
  --f-mono: ui-monospace, SFMono-Regular, Menlo, monospace;
}
:root:not([data-theme="light"]) { color-scheme: light dark; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper: #1A1E22; --paper-sunk: #0F1214; --ground: #15181B;
    --ink: #E8ECEC; --ink-2: #A6B0B4; --ink-3: #788388;
    --rule: #2C3237; --live: #E2714F; --ok: #6FBF95;
  }
}
:root[data-theme="dark"] {
  --paper: #1A1E22; --paper-sunk: #0F1214; --ground: #15181B;
  --ink: #E8ECEC; --ink-2: #A6B0B4; --ink-3: #788388;
  --rule: #2C3237; --live: #E2714F; --ok: #6FBF95;
}
body { background: var(--ground); color: var(--ink); font-family: var(--f-body); }
.wrap { max-width: 1100px; margin: 0 auto; padding: 16px; padding-block: 24px; }
.chrome {
  display: flex; flex-wrap: wrap; gap: 12px; align-items: center;
  font-family: var(--f-mono); font-size: 12px; letter-spacing: .06em;
  text-transform: uppercase; color: var(--ink-3);
  border-bottom: 1px solid var(--rule); padding-bottom: 10px;
}
.chrome .live { color: var(--live); }
.switcher { position: relative; margin-left: auto; }
.switcher button {
  font: inherit; text-transform: inherit; letter-spacing: inherit;
  color: var(--ink); background: var(--paper); border: 1px solid var(--rule);
  border-radius: 3px; padding: 6px 10px; cursor: pointer;
}
.switcher ul {
  position: absolute; right: 0; top: 110%; z-index: 9; margin: 0; padding: 4px;
  list-style: none; min-width: 260px; background: var(--paper);
  border: 1px solid var(--rule); border-radius: 4px;
}
.switcher li button { display: block; width: 100%; text-align: left; border: 0; }
.tabs { display: flex; gap: 4px; margin: 18px 0; flex-wrap: wrap; }
.tabs button {
  font-family: var(--f-mono); font-size: 12px; letter-spacing: .06em;
  text-transform: uppercase; padding: 8px 12px; cursor: pointer;
  background: none; border: 0; border-bottom: 2px solid transparent; color: var(--ink-3);
}
.tabs button[aria-current="true"] { color: var(--ink); border-bottom-color: var(--live); }
h1, h2, h3 { font-family: var(--f-display); font-weight: 600; line-height: 1.15; margin: 0; }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
th, td { text-align: left; padding: 9px 8px; border-bottom: 1px solid var(--rule); }
th { font-family: var(--f-mono); font-size: 11px; letter-spacing: .06em;
     text-transform: uppercase; color: var(--ink-3); }
.scroll { overflow-x: auto; }
.code { font-family: var(--f-mono); font-weight: 600; }
.cards { display: grid; gap: 12px; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }
.card { background: var(--paper); border: 1px solid var(--rule); border-radius: 5px; padding: 14px; }
.muted { color: var(--ink-3); }
.stage-pending { color: var(--ink-3); }
.stage-dispatched, .stage-recorded { color: var(--ink-2); }
.stage-gated { color: var(--ok); font-weight: 600; }
```

Create `docs/tournament/hub/chrome.js`:

```javascript
/* Chrome: phase banner, matchup switcher, view routing. Holds no tournament data. */
(function () {
  var views = {};
  var state = { view: "runfloor", game: 1 };
  var root = null;
  var ALL = { runfloor: true, bracket: true, entrant: true };  // views with no single subject

  function data() { return window.HUB_DATA || null; }

  function el(tag, attrs, kids) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") { node.textContent = attrs[k]; }
      else if (k === "cls") { node.className = attrs[k]; }
      else { node.setAttribute(k, attrs[k]); }
    });
    (kids || []).forEach(function (kid) { node.appendChild(kid); });
    return node;
  }

  function games() { return (data() && data().games) || []; }

  function label(game) {
    var f = data().field;
    var a = f[game.A] || { name: game.A };
    var b = f[game.B] || { name: game.B };
    return "Game " + game.g + " · " + a.name + " v " + b.name;
  }

  function switcher() {
    var box = el("div", { cls: "switcher" });
    if (ALL[state.view] || !games().length) { return box; }
    var current = games().filter(function (g) { return g.g === state.game; })[0] || games()[0];
    var list = el("ul", { hidden: "hidden" });
    var toggle = el("button", { text: label(current) + "  ▾", "aria-expanded": "false" });
    toggle.addEventListener("click", function () {
      var open = list.hidden;
      list.hidden = !open;
      toggle.setAttribute("aria-expanded", String(open));
    });
    games().forEach(function (game) {
      var pick = el("button", { text: label(game) });
      pick.addEventListener("click", function () { go(state.view, game.g); });
      list.appendChild(el("li", {}, [pick]));
    });
    box.appendChild(toggle);
    box.appendChild(list);
    return box;
  }

  function step(delta) {
    if (ALL[state.view] || !games().length) { return; }
    var order = games().map(function (g) { return g.g; });
    var at = order.indexOf(state.game);
    go(state.view, order[(at + delta + order.length) % order.length]);
  }

  function banner() {
    var d = data();
    var bar = el("div", { cls: "chrome" });
    bar.appendChild(el("span", { text: "The 99th Idea Bracket" }));
    bar.appendChild(el("span", { cls: "live", text: "● " + (d ? d.phase : "no data") }));
    if (d) { bar.appendChild(el("span", { cls: "muted", text: "built " + d.generated })); }
    bar.appendChild(switcher());
    return bar;
  }

  function tabs() {
    var bar = el("div", { cls: "tabs" });
    Object.keys(views).forEach(function (name) {
      var button = el("button", { text: name });
      if (name === state.view) { button.setAttribute("aria-current", "true"); }
      button.addEventListener("click", function () { go(name, state.game); });
      bar.appendChild(button);
    });
    return bar;
  }

  function render() {
    if (!root) { return; }
    root.textContent = "";
    var wrap = el("div", { cls: "wrap" });
    wrap.appendChild(banner());
    if (!data()) {
      wrap.appendChild(el("p", { cls: "muted",
        text: "No data file loaded. Run build_hub.py and publish its output alongside this page." }));
      root.appendChild(wrap);
      return;
    }
    wrap.appendChild(tabs());
    var body = el("div", {});
    views[state.view](body, data(), state);
    wrap.appendChild(body);
    root.appendChild(wrap);
  }

  function go(view, game) {
    state = { view: views[view] ? view : state.view, game: game || state.game };
    render();
  }

  window.HUB = {
    state: state,
    el: el,
    register: function (name, render_) { views[name] = render_; },
    go: go,
    mount: function (node) {
      root = node;
      document.addEventListener("keydown", function (event) {
        if (event.key === "ArrowRight") { step(1); }
        if (event.key === "ArrowLeft") { step(-1); }
      });
      render();
    }
  };
}());
```

- [ ] **Step 4: Add the belt-and-braces ignore rule**

Append to `.gitignore`:

```
docs/tournament/hub/hub-data.js
```

- [ ] **Step 5: Run the tests**

The shell test reads `hub/views/*.js`, which is empty until Task 6. That glob returns nothing,
so the test passes on the three files that exist.

```bash
~/.cache/temp-agency/harness-py313/bin/python -m pytest docs/tournament/test_build_hub.py -q
```

Expected: 23 passed.

- [ ] **Step 6: Commit**

```bash
git add docs/tournament/hub/index.html docs/tournament/hub/hub.css \
        docs/tournament/hub/chrome.js docs/tournament/test_build_hub.py .gitignore
git commit -m "feat: add the hub shell, tokens and chrome"
```

---

### Task 6: The Run Floor view

**Files:**
- Create: `docs/tournament/hub/views/runfloor.js`

**Interfaces:**
- Consumes: `window.HUB.register`, `window.HUB.el`, `window.HUB.go`, and
  `data.floor` rows `{code, stage, receipts}` plus `data.field[code]`.
- Produces: a registered view named `runfloor`.

- [ ] **Step 1: Write the view**

Create `docs/tournament/hub/views/runfloor.js`:

```javascript
/* Run Floor: the sixteen official runs and how far each has travelled. */
(function () {
  var el = window.HUB.el;
  var STEPS = ["pending", "dispatched", "recorded", "gated"];

  function counter(rows) {
    var gated = rows.filter(function (r) { return r.stage === "gated"; }).length;
    return gated + " of " + rows.length + " records gated";
  }

  function row(entry, field) {
    var meta = field[entry.code] || { name: entry.code, state: "", flag: "" };
    var cells = [
      el("td", {}, [el("span", { cls: "code", text: entry.code })]),
      el("td", { text: meta.name }),
      el("td", { text: meta.state || "—" }),
      el("td", { cls: "muted", text: meta.flag || "" }),
      el("td", { text: String(entry.receipts) }),
      el("td", {}, [el("span", { cls: "stage-" + entry.stage, text: entry.stage })])
    ];
    var line = el("tr", {});
    cells.forEach(function (cell) { line.appendChild(cell); });
    line.addEventListener("click", function () { window.HUB.go("entrant", null); });
    return line;
  }

  window.HUB.register("runfloor", function (container, data) {
    container.appendChild(el("h2", { text: "The run floor" }));
    container.appendChild(el("p", { cls: "muted", text: counter(data.floor) }));
    var head = el("tr", {});
    ["Code", "Entrant", "Evidence", "Flag", "Receipts", "Stage"].forEach(function (name) {
      head.appendChild(el("th", { text: name }));
    });
    var table = el("table", {}, [el("thead", {}, [head])]);
    var body = el("tbody", {});
    data.floor.forEach(function (entry) { body.appendChild(row(entry, data.field)); });
    table.appendChild(body);
    container.appendChild(el("div", { cls: "scroll" }, [table]));
    container.appendChild(el("p", { cls: "muted",
      text: "Stages: " + STEPS.join(" → ") + ". Stage is observed from repo state, not ruled." }));
  });
}());
```

- [ ] **Step 2: Build data and open the page**

```bash
~/.cache/temp-agency/harness-py313/bin/python docs/tournament/build_hub.py \
  --phase runfloor --out /tmp/hub-check
cp docs/tournament/hub/index.html docs/tournament/hub/hub.css \
   docs/tournament/hub/chrome.js /tmp/hub-check/
mkdir -p /tmp/hub-check/views && cp docs/tournament/hub/views/*.js /tmp/hub-check/views/
open /tmp/hub-check/index.html
```

Expected: a table of sixteen rows, every stage reading `pending`, the counter reading
"0 of 16 records gated", and the phase banner reading `● runfloor`.

- [ ] **Step 3: Run the tests**

```bash
~/.cache/temp-agency/harness-py313/bin/python -m pytest docs/tournament/test_build_hub.py -q
```

Expected: 23 passed. The shell tests now also scan `views/runfloor.js`.

- [ ] **Step 4: Commit**

```bash
git add docs/tournament/hub/views/runfloor.js
git commit -m "feat: add the run floor view"
```

---

### Task 7: The Bracket view

**Files:**
- Create: `docs/tournament/hub/views/bracket.js`

**Interfaces:**
- Consumes: `data.games` rows `{g, A, B, region}`, `data.field`, `data.floor`.
- Produces: a registered view named `bracket`.

- [ ] **Step 1: Write the view**

Create `docs/tournament/hub/views/bracket.js`:

```javascript
/* Bracket: eight game cards with the state of both sides. */
(function () {
  var el = window.HUB.el;

  function stageOf(floor, code) {
    var found = floor.filter(function (r) { return r.code === code; })[0];
    return found ? found.stage : "pending";
  }

  function side(data, code) {
    var meta = data.field[code] || { name: code, owner: false };
    var line = el("div", {});
    line.appendChild(el("span", { cls: "code", text: code + " " }));
    line.appendChild(el("span", { text: meta.name + (meta.owner ? " ◆" : "") }));
    line.appendChild(el("span", { cls: "muted stage-" + stageOf(data.floor, code),
                                  text: "  " + stageOf(data.floor, code) }));
    return line;
  }

  function card(data, game) {
    var box = el("div", { cls: "card" });
    box.appendChild(el("h3", { text: "Game " + game.g }));
    box.appendChild(side(data, game.A));
    box.appendChild(el("p", { cls: "muted", text: "versus" }));
    box.appendChild(side(data, game.B));
    box.addEventListener("click", function () { window.HUB.go("entrant", game.g); });
    return box;
  }

  window.HUB.register("bracket", function (container, data) {
    container.appendChild(el("h2", { text: "Sweet 16" }));
    container.appendChild(el("p", { cls: "muted",
      text: "Eight games. Draw seed " + (data.games.length ? "frozen" : "unset") + "." }));
    var grid = el("div", { cls: "cards" });
    data.games.forEach(function (game) { grid.appendChild(card(data, game)); });
    container.appendChild(grid);
  });
}());
```

- [ ] **Step 2: Rebuild and check the page**

```bash
~/.cache/temp-agency/harness-py313/bin/python docs/tournament/build_hub.py \
  --phase runfloor --out /tmp/hub-check
cp docs/tournament/hub/views/*.js /tmp/hub-check/views/
open /tmp/hub-check/index.html
```

Expected: a `bracket` tab showing eight cards. Game 8 shows `E9` in position A, per Ruling 22.
Owner ideas carry `◆`.

- [ ] **Step 3: Check the narrow viewport**

Resize the window to 400px wide. Expected: cards stack to one column, and the page does not
scroll sideways.

- [ ] **Step 4: Run the tests**

```bash
~/.cache/temp-agency/harness-py313/bin/python -m pytest docs/tournament/test_build_hub.py -q
```

Expected: 23 passed.

- [ ] **Step 5: Commit**

```bash
git add docs/tournament/hub/views/bracket.js
git commit -m "feat: add the bracket view"
```

---

### Task 8: The Entrant Card view and publish

**Files:**
- Create: `docs/tournament/hub/views/entrant.js`
- Modify: `docs/tournament/hub-design.md`

**Interfaces:**
- Consumes: `data.field[code]` with keys `code, name, owner, summary, not_native, status,
  state, flag`, and `data.floor`.
- Produces: a registered view named `entrant`.

- [ ] **Step 1: Write the view**

Create `docs/tournament/hub/views/entrant.js`:

```javascript
/* Entrant cards: definition, the not-native claim, R32 status, evidence state. */
(function () {
  var el = window.HUB.el;

  function card(data, entry) {
    var box = el("div", { cls: "card" });
    var head = el("h3", {});
    head.appendChild(el("span", { cls: "code", text: entry.code + " " }));
    head.appendChild(el("span", { text: entry.name + (entry.owner ? " ◆" : "") }));
    box.appendChild(head);
    box.appendChild(el("p", { text: entry.summary }));
    if (entry.not_native) {
      box.appendChild(el("p", { cls: "muted", text: "Not native: " + entry.not_native }));
    }
    if (entry.status) {
      box.appendChild(el("p", { cls: "muted", text: entry.status }));
    }
    box.appendChild(el("p", {
      text: "Evidence: " + (entry.state || "—") + (entry.flag ? " · " + entry.flag : "")
    }));
    return box;
  }

  window.HUB.register("entrant", function (container, data) {
    container.appendChild(el("h2", { text: "Entrants" }));
    container.appendChild(el("p", { cls: "muted",
      text: "The sixteen still standing. ◆ marks an owner idea." }));
    var grid = el("div", { cls: "cards" });
    data.floor.forEach(function (row) {
      var entry = data.field[row.code];
      if (entry) { grid.appendChild(card(data, entry)); }
    });
    container.appendChild(grid);
  });
}());
```

- [ ] **Step 2: Rebuild and check**

```bash
~/.cache/temp-agency/harness-py313/bin/python docs/tournament/build_hub.py \
  --phase runfloor --out /tmp/hub-check
cp docs/tournament/hub/views/*.js /tmp/hub-check/views/
open /tmp/hub-check/index.html
```

Expected: an `entrant` tab with sixteen cards, each naming an evidence state of `RUNNABLE`,
`MANUAL PROTOTYPE` or `PROMISE`. `A3` shows the flag `DEFECT UNRESOLVED`.

- [ ] **Step 3: Run the full tournament suite**

```bash
~/.cache/temp-agency/harness-py313/bin/python -m pytest tests docs/tournament -q
```

Expected: the pre-existing 322 tests still pass, plus the 23 new ones.

- [ ] **Step 4: Confirm the repo holds no hub data**

```bash
git status --short && ls docs/tournament/hub/
```

Expected: no `hub-data.js` under `docs/tournament/hub/`, and no untracked data file anywhere.

- [ ] **Step 5: Record the shipped state in the spec**

Add to the end of `docs/tournament/hub-design.md`:

```markdown
---

## 11. Shipped

- **Plan 1 (run floor)** — `build_hub.py` at `--phase runfloor`, plus the Bracket, Run Floor
  and Entrant Card views. See `hub-plan-1-runfloor.md`.
```

- [ ] **Step 6: Commit**

```bash
git add docs/tournament/hub/views/entrant.js docs/tournament/hub-design.md
git commit -m "feat: add the entrant card view"
```

- [ ] **Step 7: Publish**

Publish as a multi-file Artifact. Sources must sit under the working directory or the session
scratchpad, so build into the scratchpad rather than `~/.cache`:

```bash
~/.cache/temp-agency/harness-py313/bin/python docs/tournament/build_hub.py \
  --phase runfloor --out "$SCRATCHPAD/hub"
```

Publish `docs/tournament/hub/index.html` with `files` mapping `hub.css`, `chrome.js`,
`views/runfloor.js`, `views/bracket.js`, `views/entrant.js` from the repo, and `hub-data.js`
from the scratchpad. Favicon `🏟`, kept stable across redeploys.

---

## Self-Review

**Spec coverage.** § 3 guards 1 and 4 land in Task 1 and Task 5's `.gitignore` step. Guard 2
is the publish step in Task 8. Guard 3 is Task 4's omission test. § 4's data model is Tasks 2
through 4. § 5 views 1, 2 and 6 are Tasks 7, 6 and 8. § 6's phase gate is Task 1, with the
`runfloor` column of the phase table enforced by Task 4.

**Deferred to later plans, by design:** § 5 views 3, 4, 5 and 7, § 6's `--phase mechanism`
seal check, and § 7's ruling composer. The Tail Reader needs `official-runs/s16-*.md`, which
does not exist until the round runs.

**Known limitation.** `_gated` imports `lib.verify.gate` only when `--gate` is passed, so the
default build does not pay the cost of replaying receipts. Without the flag the Stage column
tops out at `recorded`. Task 6's view labels stage as observed, not ruled, so this reads
honestly rather than as a false negative.
