"""C5 selects a notation independently, then validates a committed authored artifact."""
from __future__ import annotations

import json
import random
from pathlib import Path

from lib.notation_slots import validate_artifact, validate_catalog
from lib.paths import canonical_json, sha256_file


def read_json(root, path):
    relative = Path(path)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('notation inputs must be repo-relative')
    target = (root / relative).resolve()
    target.relative_to(root.resolve())
    return json.loads(target.read_text(encoding='utf-8'))


def select(catalog, digest, seed):
    validate_catalog(catalog)
    index = random.Random(seed['value']).randrange(len(catalog['notations']))
    return {'tool': 'notation', 'entrant': 'C5', 'mode': 'select', 'catalog_sha256': digest,
            'seed': seed, 'index': index, 'notation': catalog['notations'][index],
            'item_count': catalog['item_count']}


def selected_receipt(catalog, catalog_path, digest, receipt):
    if not isinstance(receipt, dict) or any(receipt.get(k) != v for k, v in
        {'tool': 'notation', 'entrant': 'C5', 'status': 'ok', 'verification_class': 'replay-exact'}.items()):
        raise ValueError('selection must be an ok C5 notation receipt')
    if receipt.get('inputs') != {catalog_path: digest}:
        raise ValueError('selection receipt must pin the same catalog')
    seed = receipt.get('seed')
    if not isinstance(seed, dict) or type(seed.get('value')) is not int:
        raise ValueError('selection seed must be an integer')
    expected = select(catalog, digest, seed)
    if receipt.get('output') != canonical_json(expected):
        raise ValueError('selection output does not recompute')
    return expected


def render(root, args, seed):
    if args.entrant != 'C5':
        raise ValueError('notation is reserved for C5')
    catalog = read_json(root, args.catalog)
    digest = sha256_file(root / args.catalog)
    if args.mode == 'select':
        return canonical_json(select(catalog, digest, seed))
    selection = read_json(root, args.selection)
    chosen = selected_receipt(catalog, args.catalog, digest, selection)
    artifact = read_json(root, args.artifact)
    problems = validate_artifact(artifact, catalog, chosen['notation']['name'])
    return canonical_json({'tool': 'notation', 'entrant': 'C5', 'mode': 'validate',
        'inputs': {'catalog': args.catalog, 'selection': args.selection, 'artifact': args.artifact},
        'selection_receipt_id': selection['receipt_id'],
        'selection_sha256': sha256_file(root / args.selection),
        'notation': chosen['notation']['name'], 'item_count': catalog['item_count'],
        'artifact': artifact, 'validation': {'passed': not problems, 'problems': problems}})
