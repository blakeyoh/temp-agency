"""Crossover fidelity, malformed parents, archive replay and anti-blending binding."""
import json
from pathlib import Path

import pytest

from lib.breed import render, section
from lib.paths import canonical_json
from lib.verify.gate import run_gate


def parent(name):
    return (f'# {name}\n\n## Core Principles\n\n- Keep {name}.\n\n## Methodology\n\n'
            f'### Phase 1: Observe\n\nObserve {name}.\n\n### Phase 2: Act\n\nAct {name}.\n\n'
            f'## Anti-Patterns\n\n- Avoid {name} first.\n  Preserve continuation.\n\n- Avoid {name} second.\n')


def prepare(repo):
    repo.write('roster/a.md', parent('A'))
    repo.write('roster/b.md', parent('B'))
    repo.commit_all('freeze parents')


def test_literal_crossover_replay_and_full_gate(repo):
    prepare(repo)
    result = repo.run('bin/breed', '--entrant', 'E4', '--parent-a', 'roster/a.md', '--parent-b', 'roster/b.md', '--seed', '42')
    assert result.returncode == 0, result.stderr
    receipt = repo.receipt('E4')
    output = json.loads(receipt['output'])
    child = output['child']
    assert section(child, 'Core Principles') == section(parent('A'), 'Core Principles')
    assert section(child, 'Methodology') == section(parent('B'), 'Methodology')
    assert len(output['anti_pattern_order']) == 4
    literal = canonical_json({'child': child})
    text = ('# E4\n\n## Provenance\n\n- **Entrant code:** E4\n\n## Mechanism output\n\n' + literal +
            '\n\n## Execution trace\n\n' + receipt['output'] + '\n\n## Receipts\n\n- ' + receipt['receipt_id'] + ' breed\n')
    target = repo.write('docs/record.md', text)
    report = run_gate(repo.root, 'docs/record.md')
    assert report.passed, '\n'.join(line.message for line in report.lines)
    target.write_text(text.replace(literal, 'A blend of two perspectives.', 1))
    assert not run_gate(repo.root, 'docs/record.md').passed
    repo.write('roster/a.md', 'Changed after dispatch')
    assert repo.verify('replay', str(repo.receipts('E4')[-1])).returncode == 0


@pytest.mark.parametrize('problem', ['duplicate_section', 'no_phases', 'same_parent'])
def test_invalid_crossover_mints_failed_receipt(repo, problem):
    prepare(repo)
    if problem == 'duplicate_section': repo.write('roster/a.md', parent('A') + '\n## Core Principles\n\n- More.\n')
    elif problem == 'no_phases': repo.write('roster/b.md', parent('B').replace('### Phase', '### Step'))
    if problem != 'same_parent': repo.commit_all('malformed parent')
    result = repo.run('bin/breed', '--entrant', 'E4', '--parent-a', 'roster/a.md', '--parent-b',
                      'roster/a.md' if problem == 'same_parent' else 'roster/b.md', '--seed', '1')
    assert result.returncode != 0
    assert repo.receipt('E4')['status'] == 'failed'


def test_real_parent_profiles():
    root = Path(__file__).resolve().parents[1]
    output = json.loads(render(root, 'roster/anthropologist.md', 'roster/magician-illusionist.md', {'value': 271828, 'source': 'argument'}))
    assert len(output['anti_pattern_order']) >= 6
    assert output['scope'] == 'crossover-only'
