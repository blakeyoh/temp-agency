"""E5 binds the entire rejected-round chain to a leak-free final candidate."""
import json
from types import SimpleNamespace
from lib.bindings import BindResult, Check, cited_receipt_ids
from lib.bindings.forage_gate import proposal_matches
from lib.bindings.notation import body
from lib.lexicon import render
from lib.paths import repo_root, sha256_file, git_output
from lib.receipt import list_receipts, load

VERIFICATION_CLASS = 'replay-exact'
BOUND_SPAN = 'frozen term scans, retained rejected drafts, and exact final proposal; not hidden concepts'


def check(record_text, receipt):
    try:
        if receipt.get('tool') != 'lexicon-check' or receipt.get('entrant') != 'E5':
            raise ValueError('wrong lexicon receipt identity')
        root = repo_root()
        files = {load(p)['receipt_id']: p for p in list_receipts(root, 'E5')}
        rounds = {}
        for rid in cited_receipt_ids(record_text):
            if rid in files:
                value = load(files[rid])
                if value['tool'] != 'lexicon-check':
                    continue
                if value['status'] != 'ok':
                    raise ValueError('malformed evaluation in lineage')
                output = json.loads(value['output'])
                paths = output['inputs']
                if set(paths) not in ({'lexicon', 'profile', 'candidate'}, {'lexicon', 'profile', 'candidate', 'previous'}):
                    raise ValueError('unexpected lexicon inputs')
                if {p: sha256_file(root / p) for p in paths.values()} != value['inputs']:
                    raise ValueError('lexicon inputs changed')
                args = SimpleNamespace(**paths, **({'previous': None} if 'previous' not in paths else {}),
                                       era=output['era'], specialist=output['specialist'])
                if render(root, args) != value['output']:
                    raise ValueError('lexicon output differs from deterministic check')
                if value['output'] not in body(record_text, 'Execution trace'):
                    raise ValueError('all rejected and accepted rounds must remain in trace')
                rounds[rid] = (value, output)
        if receipt['receipt_id'] not in rounds:
            raise ValueError('receipt missing from cited lineage')
        roots, children = [], {}
        for rid, (value, output) in rounds.items():
            previous = output['previous_receipt_id']
            if previous is None:
                roots.append(rid)
            else:
                if previous not in rounds or previous in children:
                    raise ValueError('missing or forked prior check')
                if sha256_file(files[previous]) != value['inputs'][output['inputs']['previous']]:
                    raise ValueError('previous input differs from actual check receipt')
                if rounds[previous][0]['repo_commit'] == value['repo_commit']:
                    raise ValueError('previous check must predate regenerated candidate')
                git_output(root, 'merge-base', '--is-ancestor', rounds[previous][0]['repo_commit'], value['repo_commit'])
                children[previous] = rid
        if len(roots) != 1:
            raise ValueError('requires one complete check lineage')
        seen, current = set(), roots[0]
        while current not in seen:
            seen.add(current)
            if current not in children:
                break
            current = children[current]
        if seen != set(rounds):
            raise ValueError('disconnected or cyclic check lineage')
        final = rounds[current][1]
        if not final['passed'] or not proposal_matches(record_text, final['candidate']):
            raise ValueError('final proposal must match the last leak-free candidate')
        checks = [Check('era_lexicon', BOUND_SPAN, 'accepted final check ' + current, True)]
    except Exception as exc:
        checks = [Check('era_lexicon', BOUND_SPAN, str(exc), False)]
    return BindResult(all(c.passed for c in checks), BOUND_SPAN, checks)
