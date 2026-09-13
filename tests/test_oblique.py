"""Full-corpus deck draws, deletion of first ten, archive replay and literal binding."""
import json
from pathlib import Path

import pytest

from lib.oblique import DEFAULT_DECK, render
from lib.paths import canonical_json, sha256_file
from lib.verify.gate import run_gate


def prepare(repo):
    packs = []
    for slug in ['alpha', 'beta', 'gamma']:
        source = repo.write('knowledge/' + slug + '/positions.md', 'Positions for ' + slug)
        packs.append({'slug': slug, 'source_sha256': sha256_file(source),
                      'cards': ['Do ' + slug + ' action ' + str(i) + '.' for i in range(1, 31)]})
    repo.write(DEFAULT_DECK, canonical_json({'schema_version': 1, 'discard_first': 10, 'packs': packs}))
    repo.commit_all('freeze complete development deck')


def record(repo, card=True):
    receipt = repo.receipt('E6')
    output = json.loads(receipt['output'])
    return repo.write('docs/record.md', '# E6\n\n## Provenance\n\n- **Entrant code:** E6\n\n'
                      '## Mechanism output\n\n' + (output['card'] if card else 'A vaguely related instruction.') +
                      '\n\n## Execution trace\n\n' + receipt['output'] + '\n\n## Receipts\n\n- ' +
                      receipt['receipt_id'] + ' oblique\n')


def test_draw_full_gate_and_archive_replay(repo):
    prepare(repo)
    result = repo.run('bin/oblique', '--entrant', 'E6', '--seed', '42')
    assert result.returncode == 0, result.stderr
    receipt = repo.receipt('E6')
    output = json.loads(receipt['output'])
    assert len(receipt['inputs']) == 4
    assert output['corpus_count'] == 3 and len(output['selected_packs']) == 2
    assert output['original_card_number'] > 10
    record(repo)
    report = run_gate(repo.root, 'docs/record.md')
    assert report.passed, '\n'.join(line.message for line in report.lines)
    record(repo, card=False)
    assert not run_gate(repo.root, 'docs/record.md').passed
    repo.write(DEFAULT_DECK, '{}')
    replay = repo.verify('replay', str(repo.receipts('E6')[-1]))
    assert replay.returncode == 0, replay.stderr  # archive, not changed working deck


@pytest.mark.parametrize('change', ['missing', 'extra', 'changed_source', 'removed_source', 'added_source', 'early_cards', 'duplicate_card'])
def test_corpus_or_deck_drift_mints_failed_receipt(repo, change):
    prepare(repo)
    path = repo.root / DEFAULT_DECK
    deck = json.loads(path.read_text())
    if change == 'missing': deck['packs'].pop()
    elif change == 'extra': deck['packs'].append(dict(deck['packs'][0], slug='delta'))
    elif change == 'changed_source': repo.write('knowledge/alpha/positions.md', 'Changed position')
    elif change == 'removed_source': (repo.root / 'knowledge/alpha/positions.md').unlink()
    elif change == 'added_source': repo.write('knowledge/delta/positions.md', 'New position')
    elif change == 'early_cards': deck['discard_first'] = 0
    else: deck['packs'][0]['cards'][29] = deck['packs'][0]['cards'][10]
    path.write_text(canonical_json(deck))
    repo.commit_all('commit invalid deck or changed corpus')
    result = repo.run('bin/oblique', '--entrant', 'E6', '--seed', '42')
    assert result.returncode != 0
    assert repo.receipt('E6')['status'] == 'failed'


def test_seeded_reachability_and_no_deleted_cards(repo):
    prepare(repo)
    selected = set()
    for seed in range(200):
        output = json.loads(render(repo.root, DEFAULT_DECK, 2, {'value': seed, 'source': 'argument'}))
        assert 11 <= output['original_card_number'] <= 30
        selected.add(output['source_pack'])
    assert selected == {'alpha', 'beta', 'gamma'}


def test_real_committed_distillation_covers_all_packs():
    root = Path(__file__).resolve().parents[1]
    output = json.loads(render(root, DEFAULT_DECK, 2, {'value': 42, 'source': 'argument'}))
    assert output['corpus_count'] == 16
    assert output['eligible_card_count'] == 40
