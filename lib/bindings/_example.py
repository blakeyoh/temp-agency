"""Example binding rule, used only by tests: the output must appear verbatim."""
from __future__ import annotations

from typing import Any, Dict

from lib.bindings import BindResult, Check

VERIFICATION_CLASS = "replay-exact"
BOUND_SPAN = "receipt output appears verbatim in the record"


def check(record_text: str, receipt: Dict[str, Any]) -> BindResult:
    output = str(receipt.get("output", ""))
    present = output in record_text
    checks = [Check("output_verbatim", "present", "present" if present else "absent", present)]
    return BindResult(passed=present, bound_span=BOUND_SPAN, checks=checks)
