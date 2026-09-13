"""E6 verifies its whole-corpus draw and literal card, not semantic obedience."""
import json
from lib.bindings import BindResult, Check
from lib.bindings.notation import body
from lib.oblique import input_paths, render
from lib.paths import repo_root, sha256_file

VERIFICATION_CLASS = 'replay-exact'
BOUND_SPAN = 'complete committed corpus draw and verbatim imperative in mechanism output; not literal obedience'


def check(record_text, receipt):
    try:
        if receipt.get('tool') != 'oblique' or receipt.get('entrant') != 'E6':
            raise ValueError('wrong oblique receipt identity')
        output = json.loads(receipt['output'])
        root = repo_root()
        expected = {path: sha256_file(root / path) for path in input_paths(root, output['deck'])}
        if receipt['inputs'] != expected:
            raise ValueError('receipt must pin the deck and every real positions pack')
        if render(root, output['deck'], output['pack_count'], receipt['seed']) != receipt['output']:
            raise ValueError('deck draw differs from receipt')
        if receipt['output'] not in body(record_text, 'Execution trace'):
            raise ValueError('draw output missing from trace')
        if output['card'] not in body(record_text, 'Mechanism output'):
            raise ValueError('selected card must appear verbatim in mechanism output')
        checks = [Check('deck_draw', BOUND_SPAN, output['card'], True)]
    except Exception as exc:
        checks = [Check('deck_draw', BOUND_SPAN, str(exc), False)]
    return BindResult(all(c.passed for c in checks), BOUND_SPAN, checks)
