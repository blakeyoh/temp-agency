"""A6 binds the frozen degradation card and the unrepaired understudy proposal."""
import json
import re

from lib.bindings import BindResult, Check
from lib.bindings.notation import body
from lib.bindings.proposal import proposal_lines
from lib.paths import canonical_json, repo_root, sha256_file
from lib.understudy import render

VERIFICATION_CLASS = 'replay-exact'
BOUND_SPAN = ('frozen degradation card, its verbatim presence in the record, and a Pass 1 proposal '
              'that still runs the card phase order beside a canonically ordered expert response')

HEADING = re.compile(r'^#### Phase (\d+)\b', re.M)


def phase_sequence(text):
    return [int(number) for number in HEADING.findall(text)]


def principle_title(bullet):
    # Operators name a principle by its bold title, as the scrimmage did, not by quoting the whole bullet.
    match = re.match(r'-\s+\*\*(.+?)\*\*', bullet)
    return match[1] if match else bullet


def check(record_text, receipt):
    state = {}
    checks = []

    def run(name, action):
        try:
            action()
            checks.append(Check(name, BOUND_SPAN, 'ok', True))
        except Exception as exc:
            checks.append(Check(name, BOUND_SPAN, str(exc), False))

    def identity():
        if receipt.get('tool') != 'understudy' or receipt.get('entrant') != 'A6':
            raise ValueError('wrong understudy receipt identity')
        state['root'] = repo_root()
        state['card'] = json.loads(receipt['output'])

    def inputs():
        paths = list(receipt['inputs'])
        if len(paths) != 2 or state['card']['parent'] not in paths:
            raise ValueError('receipt must pin exactly the parent profile and the recipe')
        if receipt['inputs'] != {path: sha256_file(state['root'] / path) for path in paths}:
            raise ValueError('parent or recipe changed since dispatch')
        state['config'] = [path for path in paths if path != state['card']['parent']][0]

    def rerender():
        if render(state['root'], state['card']['parent'], state['config'], receipt['seed']) != receipt['output']:
            raise ValueError('card differs from the deterministic recipe')

    def trace():
        if receipt['output'] not in body(record_text, 'Execution trace'):
            raise ValueError('raw card output missing from trace')

    def mechanism():
        if canonical_json({'card': state['card']}) not in body(record_text, 'Mechanism output'):
            raise ValueError('literal degradation card missing from mechanism output')

    def expert():
        text = body(record_text, 'Expert response')
        if not text.strip():
            raise ValueError('Expert response section is empty')
        order = phase_sequence(text)
        if order != sorted(order) or order != list(range(1, len(order) + 1)):
            raise ValueError('expert response must run the canonical phase order')
        state['expert'] = order

    def understudy():
        state['pass1'] = body(record_text, 'Pass 1 proposal artifact')
        if phase_sequence(state['pass1']) != state['card']['phase_order']:
            raise ValueError('Pass 1 phases were repaired; the card order is not preserved')

    def principle():
        if principle_title(state['card']['false_principle']) not in state['pass1']:
            raise ValueError('misidentified principle missing from the Pass 1 artifact')

    def numbered():
        lines = [line for line in proposal_lines(record_text) if re.match(r'^\d+\. +\S', line)]
        if not lines:
            raise ValueError('Pass 1 artifact requires numbered proposal items')

    run('receipt_identity', identity)
    run('frozen_inputs', inputs)
    run('deterministic_card', rerender)
    run('raw_output_in_trace', trace)
    run('card_in_mechanism_output', mechanism)
    run('expert_response_canonical_order', expert)
    run('pass1_preserves_degraded_order', understudy)
    run('pass1_carries_false_principle', principle)
    run('pass1_numbered_items', numbered)
    return BindResult(all(c.passed for c in checks), BOUND_SPAN, checks)
