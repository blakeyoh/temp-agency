"""Binding rules: per-tool checks that a source record derives from a receipt's output.

A rule is a module `lib.bindings.<tool name with '-' as '_'>` exposing
`check(record_text: str, receipt: dict) -> BindResult`.
"""
from __future__ import annotations

import importlib
import re
from types import ModuleType
from typing import List, NamedTuple

from lib.errors import VerifyError

RECEIPTS_HEADING = re.compile(r"^##\s+Receipts\s*$")
H2_HEADING = re.compile(r"^## ")
BULLET = re.compile(r"^-\s+(\S+)")
RECEIPT_ID = re.compile(r"^[0-9a-f]{12}$")


class Check(NamedTuple):
    name: str
    expected: str
    found: str
    passed: bool


class BindResult(NamedTuple):
    passed: bool
    bound_span: str
    checks: List[Check]


def rule_module_name(tool_name: str) -> str:
    return "lib.bindings." + tool_name.replace("-", "_")


def load_rule(tool_name: str) -> ModuleType:
    """Import the binding rule for a tool or raise VerifyError."""
    name = rule_module_name(tool_name)
    try:
        module = importlib.import_module(name)
    except ImportError as exc:
        raise VerifyError(f"no binding rule for tool {tool_name!r} (expected module {name})") from exc
    if not callable(getattr(module, "check", None)):
        raise VerifyError(f"binding rule {name} does not expose check(record_text, receipt)")
    return module


def _section_lines(record_text: str) -> List[str]:
    lines = record_text.splitlines()
    starts = [i for i, line in enumerate(lines) if RECEIPTS_HEADING.match(line)]
    if not starts:
        return []
    body: List[str] = []
    for line in lines[starts[0] + 1:]:
        if H2_HEADING.match(line):
            break
        body.append(line)
    return body


def cited_receipt_ids(record_text: str) -> List[str]:
    """Receipt ids cited in the record's `## Receipts` section, in order, deduplicated."""
    ids: List[str] = []
    for line in _section_lines(record_text):
        match = BULLET.match(line)
        if not match:
            continue
        token = match.group(1).strip("`*_:,;.")
        if RECEIPT_ID.match(token) and token not in ids:
            ids = ids + [token]
    return ids
