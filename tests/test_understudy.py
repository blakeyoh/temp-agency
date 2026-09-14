"""Degradation card determinism, malformed parents, archive replay and anti-repair binding."""
import json
from pathlib import Path

import pytest

from lib.paths import canonical_json
from lib.bindings.understudy import principle_title
from lib.understudy import render
from lib.verify.gate import run_gate

CONFIG = 'docs/tournament/understudy/parent.json'
PARENT = 'roster/parent.md'
TRUE_PRINCIPLE = '**Context shapes choice**: Behavior follows the environment.'

PROFILE = ('# Parent\n\n## Core Principles\n\n'
           '- ' + TRUE_PRINCIPLE + '\n'
           '- **Measure behavior, not attitude**: Surveys are easy, observation is valid.\n'
           '- **Revealed preference**: Do beats say.\n\n'
           '## Methodology\n\n'
           '### Phase 1: Define the Specific Behavior\n\nName it precisely.\n\n'
           '### Phase 2: Map the Decision Architecture\n\nDescribe the defaults.\n\n'
           '### Phase 3: Surface the Gap\n\nCompare stated with revealed.\n\n'
           '### Phase 4: Design the Intervention\n\nFriction reduction and default changes.\n\n'
           '## Anti-Patterns\n\n- Moralizing behavior.\n')

RECIPE = {
    'parent': PARENT,
    'true_principle': TRUE_PRINCIPLE,
    'signature_techniques': ['Friction reduction', 'default changes'],
    'consequences': {
        'phase_order': 'Later phases defend the intervention instead of producing it.',
        'technique': 'Every item uses the one overused technique.',
        'principle': 'Every item becomes a quick measurement.',
    },
}


def prepare(repo, profile=PROFILE, recipe=None):
    repo.write(PARENT, profile)
    repo.write(CONFIG, json.dumps(recipe if recipe is not None else RECIPE, indent=2) + '\n')
    repo.commit_all('freeze parent and recipe')


def dispatch(repo, seed='42'):
    result = repo.run('bin/understudy', '--entrant', 'A6', '--parent', PARENT,
                      '--config', CONFIG, '--seed', seed)
    assert result.returncode == 0, result.stderr
    return repo.receipt('A6')


def phases(card, order, false_principle=True):
    blocks = []
    for position, number in enumerate(order, start=1):
        blocks.append('#### Phase %d: run %d\n\n%s\n' % (number, position,
                      card['false_principle'] if false_principle and position == 1 else 'Bounded prose.'))
    return '\n'.join(blocks)


def build_record(receipt, card, pass1_order=None, expert=True, false_principle=True):
    literal = canonical_json({'card': card})
    items = '\n'.join('%d. Opener %d using %s.' % (i, i, card['overused_technique']) for i in range(1, 4))
    text = ('# A6\n\n## Provenance\n\n- **Entrant code:** A6\n\n## Mechanism output\n\n' + literal +
            '\n\n## Execution trace\n\n' + receipt['output'] + '\n\n')
    if expert:
        text += ('## Expert response\n\n' +
                 phases(card, sorted(card['phase_order']), False) + '\n')
    text += ('## Pass 1 proposal artifact\n\n' +
             phases(card, pass1_order or card['phase_order'], false_principle) + '\n' + items +
             '\n\n## Receipts\n\n- ' + receipt['receipt_id'] + ' understudy\n')
    return text


def test_degradation_card_replay_and_full_gate(repo):
    prepare(repo)
    receipt = dispatch(repo)
    card = json.loads(receipt['output'])
    assert card['phase_order'] != [1, 2, 3, 4] and card['phase_order'][0] != 1
    assert card['true_principle'] == TRUE_PRINCIPLE
    assert card['false_principle'] != TRUE_PRINCIPLE
    text = build_record(receipt, card)
    repo.write('docs/record.md', text)
    report = run_gate(repo.root, 'docs/record.md')
    assert report.passed, '\n'.join(line.message for line in report.lines)
    repo.write(PARENT, 'Changed after dispatch')
    assert repo.verify('replay', str(repo.receipts('A6')[-1])).returncode == 0


def test_repaired_pass_one_order_fails(repo):
    prepare(repo)
    receipt = dispatch(repo)
    card = json.loads(receipt['output'])
    repo.write('docs/record.md', build_record(receipt, card, pass1_order=sorted(card['phase_order'])))
    assert not run_gate(repo.root, 'docs/record.md').passed


def test_removed_false_principle_fails(repo):
    prepare(repo)
    receipt = dispatch(repo)
    card = json.loads(receipt['output'])
    repo.write('docs/record.md', build_record(receipt, card, false_principle=False))
    assert not run_gate(repo.root, 'docs/record.md').passed


def test_missing_expert_response_fails(repo):
    prepare(repo)
    receipt = dispatch(repo)
    card = json.loads(receipt['output'])
    repo.write('docs/record.md', build_record(receipt, card, expert=False))
    assert not run_gate(repo.root, 'docs/record.md').passed


@pytest.mark.parametrize('problem', ['duplicate_section', 'no_phases', 'one_principle',
                                     'unknown_principle', 'wrong_parent'])
def test_malformed_recipe_mints_failed_receipt(repo, problem):
    profile, recipe = PROFILE, dict(RECIPE)
    if problem == 'duplicate_section':
        profile = PROFILE + '\n## Core Principles\n\n- More.\n'
    elif problem == 'no_phases':
        profile = PROFILE.replace('### Phase', '### Step')
    elif problem == 'one_principle':
        profile = PROFILE.replace('- **Measure behavior, not attitude**: Surveys are easy, observation is valid.\n', '')
        profile = profile.replace('- **Revealed preference**: Do beats say.\n', '')
    elif problem == 'unknown_principle':
        recipe['true_principle'] = '**Absent principle**: Never written down.'
    elif problem == 'wrong_parent':
        recipe['parent'] = 'roster/other.md'
    prepare(repo, profile, recipe)
    result = repo.run('bin/understudy', '--entrant', 'A6', '--parent', PARENT,
                      '--config', CONFIG, '--seed', '1')
    assert result.returncode != 0
    assert repo.receipt('A6')['status'] == 'failed'


def test_wrong_entrant_is_refused(repo):
    prepare(repo)
    result = repo.run('bin/understudy', '--entrant', 'E4', '--parent', PARENT,
                      '--config', CONFIG, '--seed', '1')
    assert result.returncode != 0


def test_real_parent_profile_always_degrades():
    root = Path(__file__).resolve().parents[1]
    config = 'docs/tournament/understudy/behavioral-psychologist.json'
    for value in range(1, 51):
        card = json.loads(render(root, 'roster/behavioral-psychologist.md', config,
                                 {'value': value, 'source': 'argument'}))
        assert card['phase_order'] != [1, 2, 3, 4]
        assert card['phase_order'][0] != 1
        assert sorted(card['phase_order']) == [1, 2, 3, 4]
        assert card['false_principle'] != card['true_principle']
        assert set(card['consequences']) == {'phase_order', 'principle', 'technique'}


def test_naming_false_principle_by_bold_title_passes(repo):
    prepare(repo)
    receipt = dispatch(repo)
    card = json.loads(receipt['output'])
    title = principle_title(card['false_principle'])
    assert title != card['false_principle']
    text = build_record(receipt, card, false_principle=False).replace(
        '## Pass 1 proposal artifact\n\n',
        '## Pass 1 proposal artifact\n\nTreat %s as load-bearing.\n\n' % title, 1)
    repo.write('docs/record.md', text)
    report = run_gate(repo.root, 'docs/record.md')
    assert report.passed, '\n'.join(line.message for line in report.lines)
