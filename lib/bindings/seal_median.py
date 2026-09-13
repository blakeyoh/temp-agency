"""Bind the validated git-sealed median; isolation remains a host attestation."""
from lib.bindings import BindResult, Check
from lib.median_seal import verify_attestation
from lib.paths import repo_root

VERIFICATION_CLASS = 'hash-attested'
BOUND_SPAN = 'median and invocation match an earlier git seal; canonical output verbatim'


def check(record_text, receipt):
    problems = verify_attestation(repo_root(), receipt)
    output = receipt.get('output')
    present = isinstance(output, str) and bool(output) and output in record_text
    checks = [Check('median_attestation', 'independently checked earlier git seal',
                    '; '.join(problems) if problems else 'valid', not problems),
              Check('median_verbatim', 'canonical median output verbatim',
                    'present' if present else 'absent', present)]
    return BindResult(all(c.passed for c in checks), BOUND_SPAN, checks)
