"""C5 binds the selected notation, valid slots and explicit translated item IDs."""
from __future__ import annotations

import json
import re
from types import SimpleNamespace

from lib.bindings import BindResult, Check, cited_receipt_ids
from lib.errors import HarnessError
from lib.notation import render, select, read_json
from lib.paths import canonical_json, git_output, repo_root, sha256_file
from lib.receipt import list_receipts, load

VERIFICATION_CLASS = 'replay-exact'
BOUND_SPAN = ('selected notation and validated artifact verbatim in trace; numbered prose maps '
              'every notation item; cited selection receipt matches committed input')


def body(text, heading):
    pattern = r'^## ' + re.escape(heading) + r'\s*\n(.*?)(?=^## |\Z)'
    found = re.findall(pattern, text, flags=re.M | re.S)
    if len(found) != 1:
        raise ValueError('requires exactly one ' + heading + ' section')
    return found[0]


def translation_matches(text, artifact):
    prose = body(text, 'Pass 1 proposal artifact').strip()
    starts = list(re.finditer(r'^(\d+)\. +', prose, re.M))
    items = artifact['items']
    if len(starts) != len(items) or not starts or starts[0].start() != 0:
        return False
    for i, start in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(prose)
        value = prose[start.end():end].strip()
        prefix = '[' + items[i]['id'] + '] '
        if int(start[1]) != i + 1 or not value.startswith(prefix) or not value[len(prefix):].strip():
            return False
    return True


def verify_selection_link(root, receipt, output, text):
    path = output['inputs']['selection']
    selection = load(root / path)
    cited = set(cited_receipt_ids(text))
    known = [p for p in list_receipts(root, 'C5')
             if load(p).get('receipt_id') == selection.get('receipt_id')]
    if len(known) != 1 or selection['receipt_id'] not in cited:
        raise ValueError('validate requires the actual cited selection receipt')
    if (sha256_file(known[0]) != receipt['inputs'][path]
            or output['selection_sha256'] != receipt['inputs'][path]):
        raise ValueError('selection input differs from actual cited receipt')
    if selection['repo_commit'] == receipt['repo_commit']:
        raise ValueError('selection must precede artifact validation commit')
    git_output(root, 'merge-base', '--is-ancestor', selection['repo_commit'], receipt['repo_commit'])
    existing = git_output(root, 'ls-tree', '-r', '--name-only', selection['repo_commit'],
                          '--', output['inputs']['artifact']).strip()
    if existing:
        raise ValueError('artifact path existed before independent notation selection')
    if selection['output'] not in body(text, 'Execution trace'):
        raise ValueError('selection output missing from trace')


def check(record_text, receipt):
    try:
        root = repo_root()
        if receipt.get('entrant') != 'C5' or receipt.get('tool') != 'notation':
            raise ValueError('wrong notation receipt identity')
        output = json.loads(receipt['output'])
        for path, digest in receipt['inputs'].items():
            if sha256_file(root / path) != digest:
                raise ValueError('notation input changed')
        if output['mode'] == 'select':
            if len(receipt['inputs']) != 1:
                raise ValueError('selection must pin only its catalog')
            path, digest = next(iter(receipt['inputs'].items()))
            expected = canonical_json(select(read_json(root, path), digest, receipt['seed']))
        elif output['mode'] == 'validate':
            paths = output['inputs']
            if set(paths) != {'catalog', 'selection', 'artifact'} or set(paths.values()) != set(receipt['inputs']):
                raise ValueError('validation inputs differ from receipt')
            args = SimpleNamespace(entrant='C5', mode='validate', **paths)
            expected = render(root, args, receipt['seed'])
            verify_selection_link(root, receipt, output, record_text)
            if not output['validation']['passed']:
                raise ValueError('notation slots failed validation')
            if not translation_matches(record_text, output['artifact']):
                raise ValueError('numbered translation must map every notation item ID')
        else:
            raise ValueError('unknown notation mode')
        if expected != receipt['output'] or expected not in body(record_text, 'Execution trace'):
            raise ValueError('recomputed notation output missing or different in trace')
        checks = [Check('notation_binding', BOUND_SPAN, 'verified', True)]
    except (HarnessError, OSError, ValueError, KeyError, TypeError) as exc:
        checks = [Check('notation_binding', BOUND_SPAN, str(exc), False)]
    return BindResult(all(c.passed for c in checks), BOUND_SPAN, checks)
