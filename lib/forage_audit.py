"""Git-sealed provenance for independent E2 model judgments, not causal proof."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from lib.forage_verdict import evaluate
from lib.paths import canonical_json, git_output, sha256_bytes

INPUT_NAMES = ('brief', 'artifact', 'candidate', 'rubric', 'response', 'manifest', 'invocation', 'fetch_receipt')
CONTEXT_PURPOSES = {'brief': 'Frozen task constraints', 'artifact': 'Verified source artifact',
                    'candidate': 'Frozen candidate to evaluate', 'rubric': 'Binding independent rubric'}
EVALUATOR_BRIEF = ('Apply the supplied independent E2 deletion rubric to every supplied candidate item. '
                   'Use only the four supplied context files. Return only the rubric-specified fenced JSON verdict, '
                   'without extra commentary, replacements, or an overall pass decision.')


def safe_path(value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError('audit paths must be repo-relative')
    if any(part in ('', '.', '..') for part in value.split('/')):
        raise ValueError('audit path contains unsafe components')
    return value


def blob(root, commit, path):
    safe_path(path)
    if not isinstance(commit, str) or not re.fullmatch('[0-9a-f]{40}', commit):
        raise ValueError('audit commit must be a full commit ID')
    return subprocess.run(['git', 'cat-file', 'blob', commit + ':' + path], cwd=root,
                          check=True, capture_output=True, timeout=60).stdout


def context(root, receipt, entrant='E2', tool='forage-gate',
            kind='independent-forage-evaluation', input_names=INPUT_NAMES):
    if any(receipt.get(k) != v for k, v in {'tool': tool, 'entrant': entrant,
        'status': 'ok', 'verification_class': 'hash-attested'}.items()):
        raise ValueError('invalid forage-gate receipt identity')
    att = receipt['external_attestation']
    if set(att) != {'kind', 'seal_commit', 'paths'} or att['kind'] != kind:
        raise ValueError('invalid evaluation attestation')
    paths = att['paths']
    if set(paths) not in (set(input_names), set(input_names) | {'previous'}):
        raise ValueError('evaluation must pin all audit inputs')
    if len(set(paths.values())) != len(paths) or set(receipt['inputs']) != set(paths.values()):
        raise ValueError('evaluation inputs must be distinct and match attestation')
    seal = att['seal_commit']
    if seal == receipt['repo_commit']:
        raise ValueError('evaluation seal must predate gate invocation')
    git_output(root, 'merge-base', '--is-ancestor', seal, receipt['repo_commit'])
    documents, hashes = {}, {}
    for name, path in paths.items():
        raw = blob(root, seal, path)
        digest = sha256_bytes(raw)
        if digest != receipt['inputs'][path] or sha256_bytes(blob(root, receipt['repo_commit'], path)) != digest:
            raise ValueError('audit input changed since evaluation seal: ' + path)
        hashes[path] = digest
        text = raw.decode('utf-8')
        documents[name] = text if name in ('brief', 'rubric') else json.loads(text)
    check_argv(receipt, paths, seal)
    return documents, hashes


def check_argv(receipt, paths, seal):
    argv = receipt['argv']
    if not isinstance(argv, list) or len(argv) % 2 or not all(isinstance(v, str) for v in argv):
        raise ValueError('audit argv must be option-value pairs')
    options = dict(zip(argv[::2], argv[1::2]))
    expected = {'--entrant': receipt['entrant'], '--seal-commit': seal,
                **{'--' + name.replace('_', '-'): path for name, path in paths.items()}}
    if len(options) != len(argv) // 2 or set(options) - set(expected) - {'--seed'}:
        raise ValueError('audit argv contains duplicate or unsupported options')
    if any(options.get(k) != v for k, v in expected.items()):
        raise ValueError('audit argv differs from pinned paths')
    if '--seed' in options and int(options['--seed']) != receipt['seed']['value']:
        raise ValueError('audit seed differs from argv')


def parse_verdict(packet):
    text = packet.get('content')
    if not isinstance(text, str):
        raise ValueError('model packet has no content')
    match = re.fullmatch(r'\s*```json\s*\n(.*?)\n```\s*', text, re.S)
    if not match:
        raise ValueError('evaluator must return exactly one fenced JSON verdict')
    return json.loads(match[1])


def validate_invocation(documents, paths, hashes, kind='independent-forage-evaluation',
                        request_brief=EVALUATOR_BRIEF):
    invocation = documents['invocation']
    if (type(invocation.get('schema_version')) is not int or invocation['schema_version'] != 1
            or invocation.get('kind') != kind
            or invocation.get('independent') is not True
            or invocation.get('mode') not in ('development', 'official')):
        raise ValueError('invalid independent evaluator invocation')
    for field in ('generator_actor', 'evaluator_actor', 'disclosure', 'context_root'):
        if not isinstance(invocation.get(field), str) or not invocation[field].strip():
            raise ValueError('invocation lacks ' + field)
    if invocation['generator_actor'] == invocation['evaluator_actor']:
        raise ValueError('generator cannot certify its own deletion verdict')
    expected = {paths[name]: hashes[paths[name]] for name in ('brief', 'artifact', 'candidate', 'rubric')}
    if invocation.get('files_read') != expected:
        raise ValueError('evaluator context must be exactly brief, artifact, candidate and rubric')
    manifest = documents['manifest']
    entries = manifest['context']
    expected_abs = {str(Path(invocation['context_root']) / path): digest for path, digest in expected.items()}
    if not Path(invocation['context_root']).is_absolute() or len(entries) != 4:
        raise ValueError('invalid recorded evaluator context root or count')
    if {entry['path']: entry['sha256'] for entry in entries} != expected_abs:
        raise ValueError('request manifest differs from attested evaluator context')
    purposes = {str(Path(invocation['context_root']) / paths[name]): purpose
                for name, purpose in CONTEXT_PURPOSES.items()}
    if any(entry.get('purpose') != purposes[entry['path']] for entry in entries):
        raise ValueError('evaluator attachment purposes differ from fixed instructions')
    request = manifest['delegation']
    if (request.get('output_mode') != 'critique' or request.get('acceptance_criteria') != []
            or request.get('constraints') != []):
        raise ValueError('evaluator request contains alternate or extra instructions')
    response = documents['response']['receipt']
    if request['brief'] != request_brief:
        raise ValueError('evaluator request used a different instruction')
    if response.get('model') != request.get('model') or response.get('finish_reason') != 'stop':
        raise ValueError('evaluator model changed or response incomplete')
    if response.get('truncated') is not False:
        raise ValueError('evaluator response must explicitly be complete')
    for field in ('model', 'provider', 'request_id'):
        if not isinstance(response.get(field), str) or not response[field].strip():
            raise ValueError('evaluator receipt lacks ' + field)
    normalize = lambda value: re.sub('[^a-z0-9]', '', value.lower())
    if normalize(response['provider']) not in [normalize(p) for p in request['provider_only']]:
        raise ValueError('evaluator provider differs from pinned request')
    if invocation['evaluator_actor'] != 'openrouter:' + response['request_id']:
        raise ValueError('evaluator actor differs from request receipt')


def compute(root, receipt):
    documents, hashes = context(root, receipt)
    paths = receipt['external_attestation']['paths']
    validate_invocation(documents, paths, hashes)
    fetched = documents['fetch_receipt']
    if any(fetched.get(k) != v for k, v in {'tool': 'forage', 'entrant': 'E2', 'status': 'ok'}.items()):
        raise ValueError('evaluation must use a successful E2 fetch')
    artifact = documents['artifact']
    if artifact != json.loads(fetched['output'])['artifact']:
        raise ValueError('evaluator artifact differs from fetched source')
    git_output(root, 'merge-base', '--is-ancestor', fetched['repo_commit'],
               receipt['external_attestation']['seal_commit'])
    verdict = parse_verdict(documents['response'])
    result = evaluate(documents['candidate'], verdict, artifact['content'])
    previous_id = None
    if 'previous' in documents:
        previous = documents['previous']
        if previous.get('tool') != 'forage-gate' or previous.get('entrant') != 'E2':
            raise ValueError('previous must be an E2 evaluation gate receipt')
        old = json.loads(previous['output'])
        old_items = {row['id']: row['text'] for row in old['candidate']['items']}
        new_items = {row['id']: row['text'] for row in documents['candidate']['items']}
        if set(old_items) != set(new_items):
            raise ValueError('regeneration must preserve all candidate item IDs')
        if any(old_items[item] == new_items[item] for item in old['result']['rejected']):
            raise ValueError('previously rejected items must be regenerated')
        if old['fetch_receipt_id'] != fetched['receipt_id']:
            raise ValueError('regeneration cannot swap the fetched artifact')
        previous_id = previous['receipt_id']
    return canonical_json({'tool': 'forage-gate', 'entrant': 'E2', 'inputs': paths,
        'seal_commit': receipt['external_attestation']['seal_commit'],
        'fetch_receipt_id': fetched['receipt_id'], 'previous_receipt_id': previous_id,
        'candidate': documents['candidate'], 'result': result,
        'evaluation_request': documents['response']['receipt']})


def verify_attestation(root, receipt):
    try:
        if receipt.get('output') != compute(root, receipt):
            return ['evaluation gate output differs from sealed evidence']
        return []
    except Exception as exc:
        return ['evaluation attestation: ' + str(exc)]
