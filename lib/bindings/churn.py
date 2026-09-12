"""Binding rule for bin/churn."""
from lib.bindings._toolbelt import check_for_tool

VERIFICATION_CLASS = "replay-exact"


def check(record_text, receipt):
    return check_for_tool(record_text, receipt, "churn")

