"""E3 routing validation fails closed until its substantive deletion test exists."""
import json
import re
from lib.bindings import BindResult, Check
from lib.bindings.notation import body
from lib.route import inputs, render
from lib.paths import repo_root, sha256_file

VERIFICATION_CLASS = 'replay-exact'
BOUND_SPAN = 'full-corpus routing and explicit LEAD/LENS; deletion gate not yet implemented'


def check(record_text, receipt):
    checks = []
    try:
        if receipt.get('tool') != 'route' or receipt.get('entrant') != 'E3':
            raise ValueError('wrong route receipt identity')
        output = json.loads(receipt['output'])
        root = repo_root()
        expected = {p: sha256_file(root / p) for p in inputs(root, output['brief'], output['index'])}
        if receipt['inputs'] != expected:
            raise ValueError('routing must pin full roster, index and brief')
        if render(root, output['brief'], output['index'], output['lens']) != receipt['output']:
            raise ValueError('routing differs from recorded lowest score')
        if receipt['output'] not in body(record_text, 'Execution trace'):
            raise ValueError('routing output missing from trace')
        mechanism = body(record_text, 'Mechanism output')
        for label, key in (('LEAD', 'lead'), ('LENS', 'lens')):
            values = re.findall(r'^' + label + r': ([a-z0-9-]+)[ \t]*$', mechanism, re.M)
            if values != [output[key]]:
                raise ValueError('requires exactly one matching ' + label + ' line')
        checks.append(Check('routing', 'lowest eligible score and supplied domain lens', output['lead'], True))
    except Exception as exc:
        checks.append(Check('routing', BOUND_SPAN, str(exc), False))
    checks.append(Check('deletion_gate', 'independent per-item frame dependence and regeneration',
                        'not implemented; routing alone cannot enact E3', False))
    return BindResult(False, BOUND_SPAN, checks)
