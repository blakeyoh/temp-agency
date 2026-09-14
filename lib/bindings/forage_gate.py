"""Bind every evaluation round to one accepted, fully evaluated final E2 proposal."""
from __future__ import annotations

import json
import re

from lib.bindings import BindResult, Check, cited_receipt_ids
from lib.bindings.notation import body
from lib.forage_audit import verify_attestation
from lib.paths import repo_root, sha256_file, git_output
from lib.receipt import list_receipts, load

VERIFICATION_CLASS = 'hash-attested'
BOUND_SPAN = 'sealed independent verdicts; rejected items regenerated; accepted final proposal verbatim'


def proposal_matches(text, candidate):
    proposal = body(text, 'Pass 1 proposal artifact').strip()
    starts = list(re.finditer(r'^(\d+)\. +', proposal, re.M))
    items = candidate['items']
    if len(starts) != len(items) or not starts or starts[0].start() != 0:
        return False
    for i, (match, item) in enumerate(zip(starts, items)):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(proposal)
        expected = '[' + item['id'] + '] ' + item['text']
        if int(match[1]) != i + 1 or proposal[match.end():end].strip() != expected:
            return False
    return True


def evaluation_chain(root, text, fetch_id, entrant='E2', gate_tool='forage-gate',
                     source_tool='forage', source_key='fetch_receipt', validator=verify_attestation):
    source_id_key = source_key + '_id'
    cited = set(cited_receipt_ids(text))
    files = {load(p)['receipt_id']: p for p in list_receipts(root, entrant)}
    gates = {}
    for rid in cited:
        if rid not in files:
            continue
        value = load(files[rid])
        if value.get('tool') == gate_tool:
            output = json.loads(value['output'])
            if output[source_id_key] == fetch_id:
                problems = validator(root, value)
                if problems:
                    raise ValueError('; '.join(problems))
                gates[rid] = (value, output)
    if not gates:
        raise ValueError('no independently evaluated deletion gate is cited')
    children, roots = {}, []
    trace = body(text, 'Execution trace')
    for rid, (value, output) in gates.items():
        if value['output'] not in trace:
            raise ValueError('every evaluation round must appear in the trace')
        previous = output['previous_receipt_id']
        if previous is None:
            roots.append(rid)
            continue
        if previous not in gates or previous in children:
            raise ValueError('evaluation lineage is missing, forked or unrelated')
        path = output['inputs']['previous']
        if sha256_file(files[previous]) != value['inputs'][path]:
            raise ValueError('previous evaluation input differs from actual receipt')
        git_output(root, 'merge-base', '--is-ancestor', gates[previous][0]['repo_commit'],
                   value['external_attestation']['seal_commit'])
        children[previous] = rid
    if len(roots) != 1:
        raise ValueError('requires one complete evaluation lineage')
    visited, current = set(), roots[0]
    while current not in visited:
        visited.add(current)
        if current not in children:
            break
        current = children[current]
    if visited != set(gates):
        raise ValueError('evaluation lineage is cyclic or disconnected')
    final = gates[current][1]
    if not final['result']['passed']:
        raise ValueError('unchanged/indeterminate items require regeneration, or fewer than three survive')
    if not proposal_matches(text, final['candidate']):
        raise ValueError('final proposal differs from independently evaluated candidate')
    if fetch_id not in cited or fetch_id not in files or load(files[fetch_id]).get('tool') != source_tool:
        raise ValueError('evaluated source fetch must be cited')
    for value, output in gates.values():
        if sha256_file(files[fetch_id]) != value['inputs'][output['inputs'][source_key]]:
            raise ValueError('evaluation used a different fetch receipt')
    return current, gates


def check(record_text, receipt):
    try:
        problems = verify_attestation(repo_root(), receipt)
        if problems:
            raise ValueError('; '.join(problems))
        output = json.loads(receipt['output'])
        final_id, gates = evaluation_chain(repo_root(), record_text, output['fetch_receipt_id'])
        if receipt['receipt_id'] not in gates:
            raise ValueError('evaluation receipt missing from final lineage')
        checks = [Check('evaluation_lineage', BOUND_SPAN, 'accepted final evaluation ' + final_id, True)]
    except Exception as exc:
        checks = [Check('evaluation_lineage', BOUND_SPAN, str(exc), False)]
    return BindResult(all(c.passed for c in checks), BOUND_SPAN, checks)
