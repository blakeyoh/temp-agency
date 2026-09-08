"""The all-receipts gate: chains, classes, replay, single-use citation, binding."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

from lib.bindings import cited_receipt_ids, load_rule
from lib.errors import HarnessError, VerifyError
from lib.paths import receipts_dir, relative_to_root
from lib.receipt import RECEIPT_NAME, list_receipts, load, verify_chain
from lib.verify import Line
from lib.verify.bind import bind
from lib.verify.dispatch import DispatchLog, check_seed, load_dispatch_log
from lib.verify.replay import check_replay

DEFAULT_RECORDS_GLOB = "docs/tournament/official-runs/s16-*.md"
ENTRANT_LINE = re.compile(r"^-\s+\*\*Entrant code:\*\*\s*(\S+)", re.MULTILINE)
COLUMNS = ("receipt_id", "entrant", "tool", "class", "status", "replay", "bind", "cited", "seed")
STATUSES = ("ok", "failed")
NOT_ENACTED = re.compile(r"NOT ENACTED")
SIDECAR_NAME = re.compile(r"^(\d{3}-[0-9a-f]{12})\.bind\.json$")


class Record(NamedTuple):
    path: Path
    rel: str
    entrant_code: Optional[str]
    receipt_ids: List[str]


class Row(NamedTuple):
    receipt_id: str
    entrant: str
    tool: str
    klass: str
    status: str
    replay: str
    bind: str
    cited: str
    seed: str


class GateReport(NamedTuple):
    rows: List[Row]
    lines: List[Line]
    passed: bool


def load_records(root: Path, glob: str) -> List[Record]:
    records: List[Record] = []
    for path in sorted(Path(root).glob(glob)):
        text = path.read_text(encoding="utf-8")
        match = ENTRANT_LINE.search(text)
        code = match.group(1).strip("`* ") if match else None
        rel = relative_to_root(root, path)
        records = records + [Record(path, rel, code, cited_receipt_ids(text))]
    return records


def citing_records(records: List[Record], receipt_id: str) -> List[Record]:
    return [r for r in records if receipt_id in r.receipt_ids]


def _check_class(receipt: Dict[str, Any], tag: str) -> Tuple[str, List[Line]]:
    """The class the receipt claims must be the class its tool declares in code."""
    klass = str(receipt.get("verification_class"))
    try:
        declared = str(getattr(load_rule(str(receipt.get("tool"))), "VERIFICATION_CLASS"))
    except VerifyError as exc:
        return klass, [Line("FAIL", f"{tag}: {exc}")]
    if klass != declared:
        return klass, [Line("FAIL", f"{tag}: receipt claims {klass}, tool declares {declared}")]
    if declared == "hash-attested":
        attestation = receipt.get("external_attestation")
        if not isinstance(attestation, dict) or not attestation:
            return klass, [Line("FAIL", f"{tag}: hash-attested receipt lacks external_attestation")]
    return klass, []


def _check_status(receipt: Dict[str, Any], citing: List[Record], tag: str) -> Tuple[str, List[Line]]:
    """`status` is validated here, not trusted: exactly ok or failed, and a failed
    receipt carries no output and is cited only by a NOT ENACTED record."""
    status = receipt.get("status")
    if status not in STATUSES:
        return str(status), [Line("FAIL", f"{tag}: invalid status {status!r} (must be ok or failed)")]
    if status == "ok":
        return "ok", []
    problems: List[Line] = []
    if receipt.get("output") != "" or not receipt.get("error"):
        problems = problems + [Line("FAIL", f"{tag}: failed receipt must have empty output and an error")]
    for record in citing:
        if not NOT_ENACTED.search(record.path.read_text(encoding="utf-8")):
            problems = problems + [Line("FAIL", f"{tag}: {record.rel} cites a failed receipt but is not NOT ENACTED")]
    return "failed", problems


def _check_replay(root: Path, path: Path, receipt: Dict[str, Any], tag: str) -> Tuple[str, List[Line]]:
    if receipt.get("verification_class") != "replay-exact":
        return "n/a", []
    if receipt.get("status") == "failed":
        return "n/a (failed)", [Line("INFO", f"{tag}: failed receipt (not replayable)")]
    report = check_replay(root, path)
    lines = [Line(l.level, f"{tag}: {l.message}") for l in report.lines]
    return ("pass" if report.passed else "FAIL"), lines


def _check_citation(receipt: Dict[str, Any], citing: List[Record], tag: str) -> Tuple[str, List[Line]]:
    if not citing:
        return "FAIL", [Line("FAIL", f"{tag}: uncited receipt")]
    if len(citing) > 1:
        names = ", ".join(r.rel for r in citing)
        return "FAIL", [Line("FAIL", f"{tag}: receipt cited by multiple records: {names}")]
    record = citing[0]
    if record.entrant_code != receipt.get("entrant"):
        return "FAIL", [Line("FAIL", f"{tag}: record {record.rel} entrant code "
                             f"{record.entrant_code!r} != receipt entrant {receipt.get('entrant')!r}")]
    return "pass", [Line("PASS", f"{tag}: cited once by {record.rel}")]


def _check_bind(root: Path, path: Path, receipt: Dict[str, Any], citing: List[Record],
                tag: str) -> Tuple[str, List[Line]]:
    if len(citing) != 1:
        return "skip", []
    if receipt.get("status") != "ok":
        return "skip (failed)", []
    try:
        outcome = bind(root, citing[0].path, path, always_write=False)
    except HarnessError as exc:
        return "FAIL", [Line("FAIL", f"{tag}: bind error: {exc}")]
    verb = "written" if outcome.written else "current"
    status = "pass" if outcome.result.passed else "FAIL"
    return status, [Line("PASS" if outcome.result.passed else "FAIL",
                         f"{tag}: bind {outcome.sidecar['result']} ({outcome.sidecar_path.name} {verb})")]


def _gate_receipt(root: Path, path: Path, records: List[Record],
                  log: DispatchLog) -> Tuple[Row, List[Line]]:
    receipt = load(path)
    receipt_id = str(receipt.get("receipt_id", path.stem))
    tag = f"{receipt.get('entrant')}/{path.name}"
    klass, lines = _check_class(receipt, tag)
    citing = citing_records(records, receipt_id)
    status, status_lines = _check_status(receipt, citing, tag)
    replay, replay_lines = _check_replay(root, path, receipt, tag)
    cited, cite_lines = _check_citation(receipt, citing, tag)
    bound, bind_lines = _check_bind(root, path, receipt, citing, tag)
    seed, seed_lines = check_seed(receipt, log, tag)
    row = Row(receipt_id, str(receipt.get("entrant")), str(receipt.get("tool")),
              klass, status, replay, bound, cited, seed)
    return row, lines + status_lines + replay_lines + cite_lines + bind_lines + seed_lines


def _entrant_dirs(root: Path) -> List[Path]:
    base = receipts_dir(root)
    if not base.is_dir():
        return []
    return sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith("."))


def _check_directory(entrant_dir: Path) -> List[Line]:
    """A receipts directory holds receipts and their sidecars, and nothing else."""
    names = sorted(p.name for p in entrant_dir.iterdir() if p.is_file())
    lines: List[Line] = []
    for name in names:
        sidecar = SIDECAR_NAME.match(name)
        if not sidecar and not RECEIPT_NAME.match(name):
            lines = lines + [Line("FAIL", f"foreign file in receipts dir: {name}")]
        elif sidecar and sidecar.group(1) + ".json" not in names:
            lines = lines + [Line("FAIL", f"orphan sidecar: {name}")]
    return lines


def run_gate(root: Path, glob: str = DEFAULT_RECORDS_GLOB,
             dispatch_log: Optional[str] = None) -> GateReport:
    """Check every entrant chain and every receipt against the cited records."""
    records = load_records(root, glob)
    log = load_dispatch_log(root, dispatch_log)
    rows: List[Row] = []
    lines: List[Line] = list(log.lines)
    for entrant_dir in _entrant_dirs(root):
        entrant = entrant_dir.name
        lines = lines + _check_directory(entrant_dir)
        chain = verify_chain(root, entrant)
        lines = lines + [Line("FAIL", f"chain {entrant}: {p}") for p in chain]
        if not chain:
            lines = lines + [Line("PASS", f"chain {entrant}: intact")]
        for path in list_receipts(root, entrant):
            row, row_lines = _gate_receipt(root, path, records, log)
            rows = rows + [row]
            lines = lines + row_lines
    passed = not any(line.level == "FAIL" for line in lines)
    return GateReport(rows, lines, passed)


def format_table(rows: List[Row]) -> str:
    """Render the summary table as aligned plain text."""
    cells = [tuple(COLUMNS)] + [tuple(str(v) for v in row) for row in rows]
    widths = [max(len(r[i]) for r in cells) for i in range(len(COLUMNS))]
    return "\n".join("  ".join(c.ljust(w) for c, w in zip(r, widths)).rstrip() for r in cells)
