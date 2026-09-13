"""E2 source acquisition: corpus draw followed by the selected server's random draw."""
from __future__ import annotations

import json
import random
import subprocess
from pathlib import Path

from lib.bindings.draw import parse_output
from lib.forage_wikipedia import fetch_random, verify_remote
from lib.paths import canonical_json, sha256_file, sha256_bytes

ENDPOINTS = {'wikipedia-en': 'https://en.wikipedia.org/w/api.php',
             'wikipedia-simple': 'https://simple.wikipedia.org/w/api.php'}
ATTESTATION = {'kind': 'wikipedia-revision', 'artifact_field': 'artifact'}


def read(root, path):
    relative = Path(path)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('forage inputs must be repo-relative')
    target = (root / relative).resolve()
    target.relative_to(root.resolve())
    return json.loads(target.read_text(encoding='utf-8'))


def selected_corpus(root, pools_path, selection_path):
    spec = read(root, pools_path)
    expected = {'draws': 1, 'pools': [{'name': 'corpus', 'options': list(ENDPOINTS)}]}
    if not isinstance(spec, dict) or type(spec.get("draws")) is not int or spec != expected:
        raise ValueError('forage pools must declare exactly the two supported corpora')
    receipt = read(root, selection_path)
    for key, value in {'tool': 'draw', 'entrant': 'E2', 'status': 'ok',
                       'verification_class': 'replay-exact'}.items():
        if receipt.get(key) != value:
            raise ValueError('forage selection must be an ok E2 draw receipt')
    if receipt['inputs'] != {pools_path: sha256_file(root / pools_path)}:
        raise ValueError('corpus draw must pin the same pool file')
    parsed = parse_output(receipt['output'])
    seed = receipt['seed']
    if type(seed.get('value')) is not int:
        raise ValueError('corpus draw seed must be an integer')
    index = random.Random(seed['value']).choice(range(len(ENDPOINTS)))
    if (parsed['draws'] != 1 or parsed['seed'] != seed['value']
            or parsed['source'] != seed['source']
            or parsed['pools'] != [('corpus', list(ENDPOINTS))]
            or parsed['indices'] != {'corpus': [index]}):
        raise ValueError('corpus draw does not recompute from the pinned pool and seed')
    return list(ENDPOINTS)[index], receipt


def render(root, entrant, pools_path, selection_path):
    if entrant != 'E2':
        raise ValueError('forage is reserved for E2')
    corpus, selection = selected_corpus(root, pools_path, selection_path)
    artifact = fetch_random(ENDPOINTS[corpus])
    return canonical_json({'tool': 'forage', 'entrant': entrant, 'corpus': corpus,
        'inputs': {'pools': pools_path, 'selection': selection_path},
        'source_draw_receipt_id': selection['receipt_id'], 'artifact': artifact})


def verify_attestation(root, receipt):
    """Fresh server lookup proves the archived revision's existence and exact text."""
    try:
        for key, value in {'tool': 'forage', 'entrant': 'E2', 'status': 'ok',
                           'verification_class': 'hash-attested',
                           'external_attestation': ATTESTATION}.items():
            if receipt.get(key) != value:
                raise ValueError('invalid forage receipt ' + key)
        output = json.loads(receipt['output'])
        paths = output['inputs']
        if set(paths) != {'pools', 'selection'} or set(paths.values()) != set(receipt['inputs']):
            raise ValueError('forage output inputs differ from receipt')
        for path, digest in receipt['inputs'].items():
            if sha256_file(root / path) != digest:
                raise ValueError('forage committed input changed')
        verify_pins_and_arguments(root, receipt, paths)
        corpus, selection = selected_corpus(root, paths['pools'], paths['selection'])
        if (output['corpus'] != corpus or output['source_draw_receipt_id'] != selection['receipt_id']
                or output['artifact']['endpoint'] != ENDPOINTS[corpus]
                or output['tool'] != 'forage' or output['entrant'] != 'E2'):
            raise ValueError('artifact does not match selected corpus')
        if canonical_json(output) != receipt['output']:
            raise ValueError('forage output must be canonical JSON')
        return verify_remote(output['artifact'], receipt['completed_utc'])
    except Exception as exc:
        return ['forage attestation: ' + str(exc)]


def verify_pins_and_arguments(root, receipt, paths):
    argv = receipt.get('argv')
    if not isinstance(argv, list) or not all(isinstance(v, str) for v in argv) or len(argv) % 2:
        raise ValueError('forage argv must be option-value pairs')
    pairs = list(zip(argv[::2], argv[1::2]))
    options = dict(pairs)
    if len(options) != len(pairs) or set(options) - {'--entrant', '--pools', '--selection', '--seed'}:
        raise ValueError('forage argv contains duplicate or unsupported options')
    for key, value in {'--entrant': 'E2', '--pools': paths['pools'],
                       '--selection': paths['selection']}.items():
        if options.get(key) != value:
            raise ValueError('forage argv disagrees with pinned input ' + key)
    if '--seed' in options and int(options['--seed']) != receipt['seed']['value']:
        raise ValueError('forage seed differs from argv')
    for path, digest in receipt['inputs'].items():
        proc = subprocess.run(['git', 'cat-file', 'blob', receipt['repo_commit'] + ':' + path],
                              cwd=root, capture_output=True, check=True, timeout=60)
        if sha256_bytes(proc.stdout) != digest:
            raise ValueError('forage input differs from receipt commit')
