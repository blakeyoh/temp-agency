"""Typed exceptions for the enactment harness."""


class HarnessError(Exception):
    """Base class for every harness failure."""


class ReceiptError(HarnessError):
    """Raised when a receipt cannot be issued, loaded, or validated."""


class ToolError(HarnessError):
    """Raised when a bin/ tool refuses to run or its produce() fails."""


class VerifyError(HarnessError):
    """Raised when bin/verify cannot complete a check."""
