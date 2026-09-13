"""E2 fetch evidence is verifiable, but cannot enact E2 without its deletion gate."""
from __future__ import annotations

import json

from lib.bindings import BindResult, Check, cited_receipt_ids
from lib.errors import HarnessError
from lib.forage import selected_corpus, verify_attestation
from lib.paths import repo_root, sha256_file, git_output
from lib.receipt import list_receipts, load

VERIFICATION_CLASS = 'hash-attested'
BOUND_SPAN = 'server revision and exact artifact text, prior corpus draw; deletion gate pending'


def _trace(text):
    from lib.bindings.notation import body
    return body(text, 'Execution trace')


def check_corpus(record_text, receipt):
    """bin/draw's E2 mode binds the source selection, not E1's proposal triples."""
    try:
        root = repo_root()
        if len(receipt['inputs']) != 1:
            raise ValueError('corpus draw must pin one pool file')
        matches = [p for p in list_receipts(root, 'E2') if load(p)['receipt_id'] == receipt['receipt_id']]
        if len(matches) != 1:
            raise ValueError('corpus receipt missing or ambiguous')
        pools = next(iter(receipt['inputs']))
        selected_corpus(root, pools, matches[0].relative_to(root).as_posix())
        if receipt['output'] not in _trace(record_text):
            raise ValueError('corpus draw output absent from trace')
        checks = [Check('corpus_draw', 'recomputed corpus selection in trace', 'verified', True)]
    except (HarnessError, ValueError, KeyError, TypeError, OSError) as exc:
        checks = [Check('corpus_draw', 'valid pinned corpus selection', str(exc), False)]
    return BindResult(all(c.passed for c in checks), 'E2 corpus selection only', checks)


def check(record_text, receipt):
    try:
        root = repo_root()
        problems = verify_attestation(root, receipt)
        output = json.loads(receipt['output'])
        selection_path = output['inputs']['selection']
        selection = load(root / selection_path)
        matches = [p for p in list_receipts(root, 'E2')
                   if load(p)['receipt_id'] == selection['receipt_id']]
        if len(matches) != 1 or selection['receipt_id'] not in cited_receipt_ids(record_text):
            problems.append('actual corpus draw must be cited')
        elif sha256_file(matches[0]) != receipt['inputs'][selection_path]:
            problems.append('selection input differs from actual draw receipt')
        if selection['repo_commit'] == receipt['repo_commit']:
            problems.append('corpus selection must precede artifact fetch commit')
        git_output(root, 'merge-base', '--is-ancestor', selection['repo_commit'], receipt['repo_commit'])
        if receipt['output'] not in _trace(record_text):
            problems.append('foraged artifact output absent from trace')
        checks = [Check('source_attestation', 'independent server verification and cited corpus draw',
                        '; '.join(problems) if problems else 'verified', not problems)]
    except (HarnessError, ValueError, KeyError, TypeError, OSError) as exc:
        checks = [Check('source_attestation', 'verified external source', str(exc), False)]
    # Deliberately fail closed. Fetch-only evidence cannot pass the amended E2 contract.
    checks.append(Check('deletion_gate', 'at least three surviving artifact-dependent items',
                        'NOT ENACTED: deletion-gate decision pending', False))
    return BindResult(False, BOUND_SPAN, checks)
