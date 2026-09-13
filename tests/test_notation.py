"""C5's independent draw, committed artifact, replay and translated-item binding."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from lib.paths import canonical_json, sha256_file
from test_notation_slots import EXAMPLES

ROOT = Path(__file__).resolve().parents[1]
CATALOG = 'docs/tournament/notation/catalog.json'
ARTIFACT = 'docs/tournament/notation/artifact.json'
DISPATCH = 'docs/tournament/notation/dispatch.json'
RECORD = 'docs/tournament/notation/record.md'


def prepare(repo):
    catalog = json.loads((ROOT / CATALOG).read_text())
    catalog['item_count'] = 2
    repo.write(CATALOG, canonical_json(catalog))
    entry = {'entrant': 'C5', 'seed': 1, 'inputs': {CATALOG: sha256_file(repo.root / CATALOG)}}
    repo.write(DISPATCH, canonical_json({'entries': [entry]}))
    repo.commit_all('freeze independent notation draw')
    proc = repo.run('bin/notation', '--entrant', 'C5', '--mode', 'select',
                    '--catalog', CATALOG, '--seed', '1')
    assert proc.returncode == 0, proc.stderr
    selected_path = repo.receipts('C5')[-1]
    selected = repo.receipt('C5')
    repo.commit_all('commit selection before authoring')
    notation = json.loads(proc.stdout)['notation']['name']
    artifact = {'notation': notation, 'items': [
        {'id': 'n' + str(i), **copy.deepcopy(EXAMPLES[notation])} for i in (1, 2)]}
    return artifact, selected, selected_path, entry


def validate(repo, artifact, selected_path, entry):
    repo.write(ARTIFACT, canonical_json(artifact))
    selection = selected_path.relative_to(repo.root).as_posix()
    hashes = {p: sha256_file(repo.root / p) for p in (CATALOG, ARTIFACT, selection)}
    repo.write(DISPATCH, canonical_json({'entries': [entry,
        {'entrant': 'C5', 'seed': 2, 'inputs': hashes}]}))
    repo.commit_all('freeze authored artifact and validation inputs')
    return repo.run('bin/notation', '--entrant', 'C5', '--mode', 'validate', '--catalog', CATALOG,
                    '--selection', selection, '--artifact', ARTIFACT, '--seed', '2')


def record(repo, selected, validated):
    artifact = json.loads(validated['output'])['artifact']
    items = '\n'.join(f"{i}. [{row['id']}] Translation of the authored notation item."
                      for i, row in enumerate(artifact['items'], 1))
    text = ('# C5 development fixture\n\n## Provenance\n\n- **Entrant code:** C5\n\n'
            '## Pass 1 proposal artifact\n\n' + items + '\n\n## Execution trace\n\n' +
            selected['output'] + validated['output'] + '\n## Receipts\n\n- ' +
            selected['receipt_id'] + ' select\n- ' + validated['receipt_id'] + ' validate\n')
    return repo.write(RECORD, text)


def test_two_stage_archive_replay_and_full_gate(repo):
    artifact, selected, path, entry = prepare(repo)
    result = validate(repo, artifact, path, entry)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['validation']['passed']
    validated = repo.receipt('C5')
    record(repo, selected, validated)
    for receipt_path in repo.receipts('C5'):
        replay = repo.verify('replay', str(receipt_path))
        assert replay.returncode == 0, replay.stdout + replay.stderr
    gate = repo.verify('all', '--records', RECORD, '--dispatch-log', DISPATCH)
    assert gate.returncode == 0, gate.stdout + gate.stderr


def test_bad_slots_produce_rejection_and_fail_binding(repo):
    artifact, selected, path, entry = prepare(repo)
    artifact['items'][0].pop(next(iter(EXAMPLES[artifact['notation']])))
    result = validate(repo, artifact, path, entry)
    assert result.returncode == 0
    assert not json.loads(result.stdout)['validation']['passed']
    record(repo, selected, repo.receipt('C5'))
    bound = repo.verify('bind', RECORD, str(repo.receipts('C5')[-1]))
    assert bound.returncode == 1 and 'slots failed' in bound.stdout


def test_wrong_notation_rejected(repo):
    artifact, selected, path, entry = prepare(repo)
    artifact['notation'] = 'arbitrary'
    result = validate(repo, artifact, path, entry)
    assert result.returncode == 0
    assert not json.loads(result.stdout)['validation']['passed']


def test_fabricated_selection_fails_receipt(repo):
    artifact, selected, path, entry = prepare(repo)
    altered = copy.deepcopy(selected)
    output = json.loads(altered['output']); output['index'] = 999
    altered['output'] = canonical_json(output)
    fake = repo.write('docs/fake-selection.json', canonical_json(altered))
    result = validate(repo, artifact, fake, entry)
    assert result.returncode == 1
    assert repo.receipt('C5')['status'] == 'failed'


def test_translation_and_actual_selection_citation_required(repo):
    artifact, selected, path, entry = prepare(repo)
    assert validate(repo, artifact, path, entry).returncode == 0
    validated = repo.receipt('C5')
    target = record(repo, selected, validated)
    good = target.read_text()
    for bad in [good.replace('[n1]', '[invented]'),
                good.replace('- ' + selected['receipt_id'] + ' select\n', ''),
                good.replace('## Execution trace', '## Other trace')]:
        target.write_text(bad)
        assert repo.verify('bind', RECORD, str(repo.receipts('C5')[-1])).returncode == 1
