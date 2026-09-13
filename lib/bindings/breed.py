"""Bind the literal crossover child, without claiming the full E4 lifecycle."""
import json
from lib.bindings import BindResult, Check
from lib.bindings.notation import body
from lib.breed import render
from lib.paths import canonical_json, repo_root, sha256_file

VERIFICATION_CLASS = 'replay-exact'
BOUND_SPAN = 'literal crossover child and source hashes; excludes mutation, scoring and promotion/death'


def check(record_text, receipt):
    try:
        if receipt.get('tool') != 'breed' or receipt.get('entrant') != 'E4':
            raise ValueError('wrong breed receipt identity')
        output = json.loads(receipt['output'])
        root = repo_root()
        parents = output['parents']
        if set(parents) != {'A', 'B'}:
            raise ValueError('requires exactly two parents')
        hashes = {p: sha256_file(root / p) for p in parents.values()}
        if receipt['inputs'] != hashes:
            raise ValueError('parent inputs changed')
        if render(root, parents['A'], parents['B'], receipt['seed']) != receipt['output']:
            raise ValueError('child differs from deterministic crossover')
        if receipt['output'] not in body(record_text, 'Execution trace'):
            raise ValueError('crossover result missing from trace')
        if canonical_json({'child': output['child']}) not in body(record_text, 'Mechanism output'):
            raise ValueError('literal child missing from mechanism output')
        checks = [Check('crossover_child', BOUND_SPAN, 'exact child preserved', True)]
    except Exception as exc:
        checks = [Check('crossover_child', BOUND_SPAN, str(exc), False)]
    return BindResult(all(c.passed for c in checks), BOUND_SPAN, checks)
