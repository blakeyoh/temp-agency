"""E3 reuses E2's complete rejection/regeneration lineage binding."""
import json
from lib.bindings import BindResult, Check
from lib.bindings.forage_gate import evaluation_chain
from lib.frame_audit import verify_attestation
from lib.paths import repo_root

VERIFICATION_CLASS = 'hash-attested'
BOUND_SPAN = 'independent final-item frame judgments; complete regeneration chain and exact final proposal'


def frame_chain(root, text, route_id):
    return evaluation_chain(root, text, route_id, 'E3', 'frame-gate', 'route', 'route_receipt', verify_attestation)


def check(record_text, receipt):
    try:
        problems = verify_attestation(repo_root(), receipt)
        if problems:
            raise ValueError('; '.join(problems))
        final, rounds = frame_chain(repo_root(), record_text, json.loads(receipt['output'])['route_receipt_id'])
        if receipt['receipt_id'] not in rounds:
            raise ValueError('frame evaluation missing from cited lineage')
        checks = [Check('frame_lineage', BOUND_SPAN, final, True)]
    except Exception as exc:
        checks = [Check('frame_lineage', BOUND_SPAN, str(exc), False)]
    return BindResult(all(c.passed for c in checks), BOUND_SPAN, checks)
