"""Small E3 adapter over E2's sealed independent-verdict enforcement."""
import json
from lib.forage_audit import blob, context, validate_invocation, parse_verdict
from lib.forage_verdict import evaluate
from lib.paths import canonical_json, git_output, sha256_bytes

INPUT_NAMES = ('brief', 'artifact', 'candidate', 'rubric', 'response', 'manifest', 'invocation', 'route_receipt')
KIND = 'independent-frame-evaluation'
EVALUATOR_BRIEF = ('Apply the supplied independent E3 frame-deletion rubric to every supplied final candidate item. '
                   'Use only the four supplied context files. Return only the rubric-specified fenced JSON verdict, '
                   'without extra commentary, replacements, or an overall pass decision.')


def routed_artifact(root, route):
    if any(route.get(k) != v for k, v in {'tool': 'route', 'entrant': 'E3', 'status': 'ok'}.items()):
        raise ValueError('frame requires a successful E3 routing receipt')
    output = json.loads(route['output'])
    path = 'roster/' + output['lead'] + '.md'
    raw = blob(root, route['repo_commit'], path)
    if sha256_bytes(raw) != route['inputs'].get(path):
        raise ValueError('routed profile differs from pinned input')
    return {'lead': output['lead'], 'lens': output['lens'], 'route_receipt_id': route['receipt_id'],
            'content': raw.decode('utf-8').replace('**', ''), 'profile_path': path,
            'profile_sha256': sha256_bytes(raw), 'normalization': 'remove Markdown double-asterisk markers only'}


def compute(root, receipt):
    documents, hashes = context(root, receipt, 'E3', 'frame-gate', KIND, INPUT_NAMES)
    paths = receipt['external_attestation']['paths']
    validate_invocation(documents, paths, hashes, KIND, EVALUATOR_BRIEF)
    route = documents['route_receipt']
    artifact = routed_artifact(root, route)
    if documents['artifact'] != artifact:
        raise ValueError('evaluator frame differs from routed specialist')
    routed = json.loads(route['output'])
    if sha256_bytes(documents['brief'].encode('utf-8')) != route['inputs'].get(routed['brief']):
        raise ValueError('evaluator brief differs from routed task')
    git_output(root, 'merge-base', '--is-ancestor', route['repo_commit'], receipt['external_attestation']['seal_commit'])
    result = evaluate(documents['candidate'], parse_verdict(documents['response']), artifact['content'])
    previous_id = None
    if 'previous' in documents:
        previous = documents['previous']
        if any(previous.get(k) != v for k,v in {'tool':'frame-gate','entrant':'E3','status':'ok'}.items()):
            raise ValueError('previous must be an E3 evaluation receipt')
        old = json.loads(previous['output'])
        before = {row['id']: row['text'] for row in old['candidate']['items']}
        after = {row['id']: row['text'] for row in documents['candidate']['items']}
        if set(before) != set(after) or any(before[i] == after[i] for i in old['result']['rejected']):
            raise ValueError('preserve IDs and regenerate every rejected item')
        if old['route_receipt_id'] != route['receipt_id']:
            raise ValueError('regeneration cannot reroute specialists')
        previous_id = previous['receipt_id']
    return canonical_json({'tool':'frame-gate','entrant':'E3','inputs':paths,
        'seal_commit':receipt['external_attestation']['seal_commit'],
        'route_receipt_id':route['receipt_id'],'previous_receipt_id':previous_id,
        'candidate':documents['candidate'],'result':result,
        'evaluation_request':documents['response']['receipt']})


def verify_attestation(root, receipt):
    try:
        return [] if compute(root, receipt) == receipt['output'] else ['frame gate differs from sealed evidence']
    except Exception as exc:
        return ['frame attestation: ' + str(exc)]
