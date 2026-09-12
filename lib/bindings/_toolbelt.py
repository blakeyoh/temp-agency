"""Shared A3 rule: every explicit tool credit must resolve and byte-match a receipt."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from lib.bindings import BindResult, Check, cited_receipt_ids
from lib.paths import receipts_dir, repo_root
from lib.receipt import RECEIPT_NAME, load

TOOLS = {"churn", "seasons", "units", "orders"}
H2 = re.compile(r"^##\s+(.+?)\s*$")
H3 = re.compile(r"^###\s+([0-9a-f]{12})\s*$", re.MULTILINE)
ENTRY = re.compile(
    r"^###\s+([0-9a-f]{12})\s*\n\nInvocation:\n\n```json\n(.*?)```"
    r"\n\nRaw result:\n\n```json\n(.*?)```\s*$", re.S)
BOUND_SPAN = ("every block in the explicit Credited tools section resolves to one cited "
              "A3 receipt; its normalized invocation and raw result byte-match that receipt")


def invocation(receipt: Dict[str, Any]) -> str:
    value = {"argv": receipt.get("argv", []), "tool": f"bin/{receipt.get('tool', '')}"}
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _section(record_text: str) -> Tuple[Optional[str], str]:
    lines = record_text.splitlines(keepends=True)
    starts = [index for index, line in enumerate(lines)
              if H2.match(line.rstrip("\r\n")) and H2.match(line.rstrip("\r\n")).group(1) == "Credited tools"]
    if len(starts) != 1:
        return None, f"found {len(starts)} Credited tools sections"
    body = []
    for line in lines[starts[0] + 1:]:
        if H2.match(line.rstrip("\r\n")):
            break
        body.append(line)
    return "".join(body).strip() + "\n", ""


def _entries(section: str) -> Tuple[Dict[str, Tuple[str, str]], List[str]]:
    matches = list(H3.finditer(section))
    if not matches:
        return {}, ["section has no receipt credit blocks"]
    problems, parsed = [], {}
    if section[:matches[0].start()].strip():
        problems.append("text before first credit block")
    for index, heading in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(section)
        block = section[heading.start():end].strip() + "\n"
        match = ENTRY.fullmatch(block.strip())
        if match is None:
            problems.append(f"malformed credit block {heading.group(1)}")
            continue
        receipt_id, called, output = match.groups()
        if receipt_id in parsed:
            problems.append(f"duplicate credit block {receipt_id}")
        parsed[receipt_id] = (called, output)
    return parsed, problems


def _receipt_index(root: Path) -> Dict[str, Dict[str, Any]]:
    indexed = {}
    base = receipts_dir(root)
    if not base.is_dir():
        return indexed
    for path in base.glob("*/*.json"):
        if RECEIPT_NAME.match(path.name):
            receipt = load(path)
            indexed[str(receipt.get("receipt_id"))] = receipt
    return indexed


def _validate(entries: Dict[str, Tuple[str, str]], cited: List[str],
              receipts: Dict[str, Dict[str, Any]]) -> List[str]:
    problems = []
    for receipt_id, (called, output) in entries.items():
        receipt = receipts.get(receipt_id)
        if receipt is None:
            problems.append(f"{receipt_id}: no receipt found")
        elif receipt_id not in cited:
            problems.append(f"{receipt_id}: receipt is not cited in ## Receipts")
        elif (receipt.get("tool") not in TOOLS or receipt.get("status") != "ok"
              or receipt.get("entrant") != "A3"):
            problems.append(f"{receipt_id}: receipt is not an ok A3 tool receipt")
        else:
            if called != invocation(receipt):
                problems.append(f"{receipt_id}: invocation differs from receipt")
            if output != receipt.get("output"):
                problems.append(f"{receipt_id}: raw result differs from receipt")
    credited = set(entries)
    expected = {receipt_id for receipt_id in cited
                if receipts.get(receipt_id, {}).get("tool") in TOOLS}
    if credited != expected:
        problems.append("credited receipt ids differ from cited A3 receipt ids")
    return problems


def check_for_tool(record_text: str, receipt: Dict[str, Any], tool: str) -> BindResult:
    section, section_problem = _section(record_text)
    section_check = Check("credited_section", "exactly one explicit ## Credited tools section",
                          section_problem or "one section", section is not None)
    if section is None:
        checks = [section_check, Check("credited_receipts", "all credits valid", section_problem, False)]
        return BindResult(False, BOUND_SPAN, checks)
    entries, parse_problems = _entries(section)
    root = repo_root()
    receipts = _receipt_index(root)
    problems = parse_problems + _validate(entries, cited_receipt_ids(record_text), receipts)
    current_id = str(receipt.get("receipt_id", ""))
    if receipt.get("tool") != tool:
        problems.append(f"binding module {tool} received {receipt.get('tool')}")
    if current_id not in entries:
        problems.append(f"current receipt {current_id} has no credit block")
    credit_check = Check("credited_receipts", "every cited A3 receipt credited exactly and byte-matched",
                         "all credits match" if not problems else "; ".join(problems), not problems)
    return BindResult(section_check.passed and credit_check.passed, BOUND_SPAN,
                      [section_check, credit_check])
