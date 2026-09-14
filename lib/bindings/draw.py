"""Binding rule for bin/draw: the header is verbatim and the prose carries the draw."""
from __future__ import annotations

import difflib
import re
from typing import Any, Dict, List, Optional, Tuple

from lib.bindings.proposal import proposal_lines
from lib.bindings import BindResult, Check, cited_receipt_ids
from lib.paths import repo_root
from lib.receipt import list_receipts, load

VERIFICATION_CLASS = "replay-exact"

BOUND_SPAN = (
    "draw header verbatim; per-item labels equal the drawn options; "
    "counterfactual replay is item k's own opener and differs materially when two draw receipts are cited"
)
CHECK_NAMES = ("header_verbatim", "item_labels", "counterfactual")
SIMILARITY_MAX = 0.8

HEADER = re.compile(r"^DRAW seed=(-?\d+) source=(\S+) pools=(.*) draws=(\d+)$")
POOL_LINE = re.compile(r"^(.*) \((\d+)\): (.*)$")
INDEX_LINE = re.compile(r"^(.*): \[(.*)\]$")
OPTION = re.compile(r"^(\d+) (.*)$")
BOLD_TRIPLE = re.compile(r"^\s*\d+\.\s+\*\*(.+?)\*\*")
COUNTERFACTUAL = re.compile(r"^##\s+Counterfactual replay\s*$")
H2 = re.compile(r"^## ")


def _parse_pool(line: str) -> Tuple[str, List[str]]:
    match = POOL_LINE.match(line)
    if not match:
        raise ValueError(f"not a pool line: {line!r}")
    name, count, body = match.group(1), int(match.group(2)), match.group(3)
    options: List[str] = []
    for position, item in enumerate(body.split(" | ")):
        found = OPTION.match(item)
        if not found or int(found.group(1)) != position:
            raise ValueError(f"bad option {item!r} in pool {name!r}")
        options = options + [found.group(2)]
    if len(options) != count:
        raise ValueError(f"pool {name!r} declares {count} options, lists {len(options)}")
    return (name, options)


def _parse_index(line: str) -> Tuple[str, List[int]]:
    match = INDEX_LINE.match(line)
    if not match:
        raise ValueError(f"not an index line: {line!r}")
    body = match.group(2).strip()
    values = [] if not body else [int(part.strip()) for part in body.split(",")]
    return (match.group(1), values)


def parse_output(output: str) -> Dict[str, Any]:
    """Recover the header fields, the pools and the drawn indices from a draw output."""
    lines = str(output).strip("\n").split("\n")
    header = HEADER.match(lines[0]) if lines else None
    if header is None:
        raise ValueError("output has no DRAW header")
    body = lines[1:]
    if not body or len(body) % 2 != 0:
        raise ValueError("output must carry one legend line and one index line per pool")
    half = len(body) // 2
    pools = [_parse_pool(line) for line in body[:half]]
    indices = dict(_parse_index(line) for line in body[half:])
    draws = int(header.group(4))
    for name, values in indices.items():
        if len(values) != draws:
            raise ValueError(f"pool {name!r} has {len(values)} draws, header says {draws}")
    return {"seed": int(header.group(1)), "source": header.group(2),
            "draws": draws, "pools": pools, "indices": indices}


def drawn_labels(parsed: Dict[str, Any], item: int) -> List[str]:
    """The option text each pool drew for 1-based item number `item`."""
    labels: List[str] = []
    for name, options in parsed["pools"]:
        values = parsed["indices"].get(name)
        if values is None or not 1 <= item <= len(values):
            raise ValueError(f"no draw for item {item} in pool {name!r}")
        labels = labels + [options[values[item - 1]]]
    return labels


def _item_triple(line: str) -> Optional[List[str]]:
    """The bold `**a / b / c**` label triple opening an item line, lowercased."""
    match = BOLD_TRIPLE.match(line)
    if match is None:
        return None
    text = match.group(1).strip()
    text = text[:-1] if text.endswith(":") else text
    return [part.strip().lower() for part in text.split(" / ")]


def _item_line(record_text: str, item: int) -> Optional[str]:
    pattern = re.compile(r"^\s*%d\.\s" % item)
    for line in proposal_lines(record_text):
        if pattern.match(line):
            return line
    return None


def _item_label_problem(record_text: str, parsed: Dict[str, Any], item: int) -> Optional[str]:
    """Item `item` must open with the exact bold triple its draw produced."""
    line = _item_line(record_text, item)
    if line is None:
        return f"item {item}: no line"
    found = _item_triple(line)
    if found is None:
        return f"item {item}: no bold label triple"
    drawn = [label.strip().lower() for label in drawn_labels(parsed, item)]
    if found != drawn:
        return "item %d: labels %s != drawn %s" % (item, " / ".join(found), " / ".join(drawn))
    return None


def _check_item_labels(record_text: str, parsed: Dict[str, Any]) -> Check:
    problems = [_item_label_problem(record_text, parsed, item)
                for item in range(1, parsed["draws"] + 1)]
    missing = [problem for problem in problems if problem is not None]
    expected = f"{parsed['draws']} item lines opening with their exact drawn label triple"
    found = "all items labeled" if not missing else "; ".join(missing)
    return Check("item_labels", expected, found, not missing)


def cited_draw_receipts(record_text: str, receipt: Dict[str, Any]) -> List[Dict[str, Any]]:
    """The record's cited receipts whose tool is `draw`, in citation order."""
    entrant = str(receipt.get("entrant", ""))
    by_id: Dict[str, Dict[str, Any]] = {}
    for path in list_receipts(repo_root(), entrant):
        loaded = load(path)
        by_id = {**by_id, str(loaded.get("receipt_id")): loaded}
    cited: List[Dict[str, Any]] = []
    for receipt_id in cited_receipt_ids(record_text):
        other = by_id.get(receipt_id)
        if other is not None and other.get("tool") == "draw":
            cited = cited + [other]
    return cited


def _section(record_text: str) -> List[str]:
    lines = record_text.splitlines()
    starts = [i for i, line in enumerate(lines) if COUNTERFACTUAL.match(line)]
    if not starts:
        return []
    body: List[str] = []
    for line in lines[starts[0] + 1:]:
        if H2.match(line):
            break
        body = body + [line]
    return body


def _field(body: List[str], label: str) -> Optional[str]:
    pattern = re.compile(r"^\s*(?:[-*]\s+)?%s:\s*(.*)$" % re.escape(label))
    for line in body:
        match = pattern.match(line)
        if match:
            return match.group(1).strip()
    return None


def _counterfactual_problems(body: List[str], parsed: Dict[str, Any],
                             record_text: str) -> List[str]:
    fields = {name: _field(body, name)
              for name in ("Item", "Original", "Replayed", "Replayed labels")}
    absent = [name for name, value in fields.items() if not value]
    if absent:
        return [f"missing {', '.join(absent)}"]
    try:
        item = int(str(fields["Item"]))
        expected = [label.strip().lower() for label in drawn_labels(parsed, item)]
    except ValueError as exc:
        return [str(exc)]
    got = [part.strip().lower() for part in str(fields["Replayed labels"]).split(" / ")]
    problems = [] if got == expected else [
        "replayed labels %s != drawn %s" % (" / ".join(got), " / ".join(expected))]
    problems = problems + _original_problems(record_text, item, str(fields["Original"]))
    ratio = difflib.SequenceMatcher(None, fields["Original"], fields["Replayed"]).ratio()
    if ratio >= SIMILARITY_MAX:
        problems = problems + ["original and replayed prose similarity %.2f >= %.2f"
                               % (ratio, SIMILARITY_MAX)]
    return problems


def _original_problems(record_text: str, item: int, original: str) -> List[str]:
    """The Original line must be item k's own opener, not any text."""
    line = _item_line(record_text, item)
    wanted = original.strip().strip('"\u201c\u201d').lower()
    if line is None:
        return [f"item {item} has no line to compare Original against"]
    if not wanted or wanted not in line.lower():
        return [f"Original does not match item {item}'s line"]
    return []


def _check_counterfactual(record_text: str, parsed: Dict[str, Any],
                          cited: List[Dict[str, Any]], is_primary: bool) -> Check:
    expected = "replayed item labeled by this receipt's draw and materially different prose"
    if len(cited) < 2:
        return Check("counterfactual", expected, "not applicable (single draw receipt)", True)
    if is_primary:
        return Check("counterfactual", expected,
                     "primary draw; counterfactual checked on the second receipt", True)
    body = _section(record_text)
    if not body:
        return Check("counterfactual", expected, "no '## Counterfactual replay' section", False)
    problems = _counterfactual_problems(body, parsed, record_text)
    found = "counterfactual replay derives from this receipt" if not problems \
        else "; ".join(problems)
    return Check("counterfactual", expected, found, not problems)


def _unparseable() -> BindResult:
    checks = [Check(name, "parseable draw output", "unparseable output", False)
              for name in CHECK_NAMES]
    return BindResult(passed=False, bound_span=BOUND_SPAN, checks=checks)


def check(record_text: str, receipt: Dict[str, Any]) -> BindResult:
    """Bind a source record to one bin/draw receipt."""
    if receipt.get("entrant") == "E2":
        from lib.bindings.forage import check_corpus
        return check_corpus(record_text, receipt)
    output = str(receipt.get("output", ""))
    try:
        parsed = parse_output(output)
    except ValueError:
        return _unparseable()
    present = output.strip() in record_text
    checks = [Check("header_verbatim", "draw header present verbatim",
                    "present" if present else "absent", present)]
    cited = cited_draw_receipts(record_text, receipt)
    receipt_id = str(receipt.get("receipt_id"))
    is_primary = not cited or str(cited[0].get("receipt_id")) == receipt_id
    if is_primary:
        checks = checks + [_check_item_labels(record_text, parsed)]
    else:
        checks = checks + [Check("item_labels", "labels checked on the primary draw",
                                 "not applicable (counterfactual receipt)", True)]
    checks = checks + [_check_counterfactual(record_text, parsed, cited, is_primary)]
    return BindResult(passed=all(c.passed for c in checks), bound_span=BOUND_SPAN,
                      checks=checks)
