"""Binding rule for `bin/seed-string` (E9 — String Seed of Thought).

bound_span: every generated string verbatim; every derivation row's
arithmetic re-computes; every item's label equals the derived index's pool
entry.

This is E9's enactment directive: a record binds to a `bin/seed-string`
receipt only if it follows these conventions.

Pool section
    A heading line (any `#` level) whose text contains the word "pool"
    (case-insensitive). It is followed by lines `<idx>: <label>` — optionally
    bulleted, `- 0: label` — for idx 0..N-1, N = pool size. Blank lines are
    allowed. The section ends at the next heading line of any level.

Derivation table
    A markdown table whose header row cells include, case-insensitively,
    "string", "sum", and "index" (in any of the table's columns, any order).
    Each data row carries a string cell (may be wrapped in backticks), an
    integer sum cell, and an integer index cell; other cells are ignored.
    Every string the tool emitted must appear in exactly one row.

Item lines
    For string n (1-based, in the order the tool emitted it), the first line
    in the record matching `^\\s*n\\.\\s` must contain, case-insensitively,
    the pool label at the index recorded in that string's derivation row.

Checks
    strings_verbatim  -- every emitted string appears somewhere in the record.
    pool_parsed       -- a pool section parses with N >= 2 contiguous indices.
    derivation_rows   -- one row per string; sum and index both recompute.
    item_labels       -- item n's line names pool[recorded index] for its string.

If the receipt's own output does not parse (see `parse_output`), every check
fails with found="unparseable output": the rule cannot even locate the
strings it would otherwise verify.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

from lib.bindings.proposal import proposal_lines
from lib.bindings import BindResult, Check

BOUND_SPAN = (
    "every generated string verbatim; every derivation row's arithmetic "
    "re-computes; every item's label equals the derived index's pool entry"
)

HEADER_RE = re.compile(
    r"^SEED-STRINGS seed=(?P<seed>\d+) source=(?P<source>os-entropy|argument) "
    r"alphabet=(?P<alphabet>\S+) length=(?P<length>\d+) count=(?P<count>\d+)\s*$"
)
ITEM_OUTPUT_RE = re.compile(r"^(?P<n>\d+):\s(?P<value>.*)$")
POOL_HEADING_RE = re.compile(r"^#+\s.*pool", re.IGNORECASE)
HEADING_RE = re.compile(r"^#+\s")
POOL_ITEM_RE = re.compile(r"^\s*(?:[-*]\s+)?(\d+):\s*(.+?)\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:|-]+\|[\s:|-]*\|?\s*$")
BACKTICK_RE = re.compile(r"^`(.*)`$")
CHECK_NAMES = ("strings_verbatim", "pool_parsed", "derivation_rows", "item_labels")
VERIFICATION_CLASS = "replay-exact"


def parse_output(output: str) -> Optional[Dict[str, Any]]:
    """Parse a `bin/seed-string` stdout payload, or None if it does not fit."""
    lines = output.splitlines()
    if not lines:
        return None
    header = HEADER_RE.match(lines[0])
    if not header:
        return None
    count = int(header.group("count"))
    strings: List[str] = []
    for line in lines[1:]:
        match = ITEM_OUTPUT_RE.match(line)
        if not match:
            return None
        strings = strings + [match.group("value")]
    if len(strings) != count:
        return None
    return {
        "seed": int(header.group("seed")),
        "source": header.group("source"),
        "alphabet": header.group("alphabet"),
        "length": int(header.group("length")),
        "count": count,
        "strings": strings,
    }


def _check_strings_verbatim(strings: List[str], record_text: str) -> Check:
    missing = [s for s in strings if s not in record_text]
    expected = f"all {len(strings)} strings present"
    found = "all present" if not missing else "missing: " + ", ".join(missing)
    return Check("strings_verbatim", expected, found, not missing)


def _parse_pool(record_text: str) -> Tuple[Optional[List[str]], Check]:
    lines = record_text.splitlines()
    start = next((i for i, line in enumerate(lines) if POOL_HEADING_RE.match(line)), None)
    expected = "pool section with N >= 2 contiguous indices"
    if start is None:
        return None, Check("pool_parsed", expected, "no pool heading found", False)
    entries: Dict[int, str] = {}
    for line in lines[start + 1:]:
        if HEADING_RE.match(line):
            break
        if not line.strip():
            continue
        match = POOL_ITEM_RE.match(line)
        if match:
            entries = {**entries, int(match.group(1)): match.group(2)}
    n = len(entries)
    if n < 2 or set(entries) != set(range(n)):
        found = f"parsed {n} entries at indices {sorted(entries)}"
        return None, Check("pool_parsed", expected, found, False)
    pool = [entries[i] for i in range(n)]
    return pool, Check("pool_parsed", expected, f"N={n}, indices 0..{n - 1}", True)


def _split_row(line: str) -> List[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _find_table(lines: List[str]) -> Tuple[Optional[Tuple[int, int, int]], List[List[str]]]:
    for i, line in enumerate(lines):
        if "|" not in line:
            continue
        lowered = [cell.lower() for cell in _split_row(line)]
        idx_string = next((j for j, c in enumerate(lowered) if "string" in c), None)
        idx_sum = next((j for j, c in enumerate(lowered) if "sum" in c), None)
        idx_index = next((j for j, c in enumerate(lowered) if "index" in c), None)
        if idx_string is None or idx_sum is None or idx_index is None:
            continue
        if i + 1 >= len(lines) or not TABLE_SEP_RE.match(lines[i + 1]):
            continue
        rows = []
        for row_line in lines[i + 2:]:
            if "|" not in row_line or not row_line.strip():
                break
            rows = rows + [_split_row(row_line)]
        return (idx_string, idx_sum, idx_index), rows
    return None, []


def _cell_string(cell: str) -> str:
    match = BACKTICK_RE.match(cell.strip())
    return match.group(1) if match else cell.strip()


def _rows_by_string(rows: List[List[str]], columns: Tuple[int, int, int]) -> Dict[str, List[Tuple[int, int]]]:
    idx_string, idx_sum, idx_index = columns
    by_string: Dict[str, List[Tuple[int, int]]] = {}
    for row in rows:
        if len(row) <= max(idx_string, idx_sum, idx_index):
            continue
        try:
            row_sum = int(row[idx_sum].strip())
            row_index = int(row[idx_index].strip())
        except ValueError:
            continue
        key = _cell_string(row[idx_string])
        by_string = {**by_string, key: by_string.get(key, []) + [(row_sum, row_index)]}
    return by_string


def _check_derivation(strings: List[str], by_string: Dict[str, List[Tuple[int, int]]],
                      pool_size: Optional[int]) -> Check:
    failures: List[str] = []
    for s in strings:
        matches = by_string.get(s, [])
        if len(matches) != 1:
            failures = failures + [f"{s}: {len(matches)} rows (expected 1)"]
            continue
        row_sum, row_index = matches[0]
        expected_sum = sum(ord(c) for c in s)
        expected_index = expected_sum % pool_size if pool_size else None
        if row_sum != expected_sum:
            failures = failures + [f"{s}: sum {row_sum} != expected {expected_sum}"]
        elif expected_index is None or row_index != expected_index:
            failures = failures + [f"{s}: index {row_index} != expected {expected_index}"]
    expected = "one row per string; sum and index both recompute"
    found = "all rows correct" if not failures else "; ".join(failures)
    return Check("derivation_rows", expected, found, not failures)


def _find_item_line(lines: List[str], n: int) -> Optional[str]:
    pattern = re.compile(r"^\s*%d\.\s" % n)
    return next((line for line in lines if pattern.match(line)), None)


def _check_item_labels(strings: List[str], by_string: Dict[str, List[Tuple[int, int]]],
                       pool: Optional[List[str]], record_text: str) -> Check:
    lines = proposal_lines(record_text)
    failures: List[str] = []
    for n, s in enumerate(strings, start=1):
        matches = by_string.get(s, [])
        if len(matches) != 1:
            failures = failures + [f"item {n}: no unique derivation row for {s}"]
            continue
        _, row_index = matches[0]
        if pool is None or not 0 <= row_index < len(pool):
            failures = failures + [f"item {n}: index {row_index} out of pool range"]
            continue
        label = pool[row_index]
        line = _find_item_line(lines, n)
        if line is None:
            failures = failures + [f"item {n}: no line matching '{n}. '"]
        elif label.lower() not in line.lower():
            failures = failures + [f"item {n}: line does not name pool label {label!r}"]
    expected = "item n's line names pool[recorded index]"
    found = "all item lines match" if not failures else "; ".join(failures)
    return Check("item_labels", expected, found, not failures)


def _unparseable_result() -> BindResult:
    checks = [Check(name, "parsed tool output", "unparseable output", False) for name in CHECK_NAMES]
    return BindResult(passed=False, bound_span=BOUND_SPAN, checks=checks)


def check(record_text: str, receipt: Dict[str, Any]) -> BindResult:
    parsed = parse_output(str(receipt.get("output", "")))
    if parsed is None:
        return _unparseable_result()
    strings = parsed["strings"]
    lines = record_text.splitlines()
    verbatim = _check_strings_verbatim(strings, record_text)
    pool, pool_check = _parse_pool(record_text)
    columns, rows = _find_table(lines)
    by_string = _rows_by_string(rows, columns) if columns else {}
    derivation = _check_derivation(strings, by_string, len(pool) if pool else None)
    items = _check_item_labels(strings, by_string, pool, record_text)
    checks = [verbatim, pool_check, derivation, items]
    return BindResult(passed=all(c.passed for c in checks), bound_span=BOUND_SPAN, checks=checks)
