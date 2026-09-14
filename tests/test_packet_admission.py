"""Actual receipts and archive replay guard packet release in throwaway repos."""
import json

import pytest

from lib.paths import canonical_json, sha256_file
from lib.verify.packet import validate_sources
from test_breed import prepare

RUNS = 'docs/tournament/official-runs'
LOG = 'docs/tournament/dispatch-log.json'


def setup_packet(repo, log_before=True):
    prepare(repo)
    entry = {'entrant': 'E4', 'seed': 42, 'inputs': {
        p: sha256_file(repo.root / p) for p in ('roster/a.md', 'roster/b.md')}}
    repo.write(LOG, json.dumps({'entries': [entry] if log_before else []}))
    repo.commit_all('pin dispatch')
    result = repo.run('bin/breed', '--entrant', 'E4', '--parent-a', 'roster/a.md',
                      '--parent-b', 'roster/b.md', '--seed', '42')
    assert result.returncode == 0, result.stderr
    row = repo.receipt('E4')
    literal = canonical_json({'child': json.loads(row['output'])['child']})
    text = ('# E4\n\n## Provenance\n- **Entrant code:** E4\n'
            '- **Enactment status:** FAITHFUL\n\n## Mechanism output\n' + literal +
            '\n\n## Execution trace\n' + row['output'] + '\n## Receipts\n- ' + row['receipt_id'] + ' breed\n')
    path = repo.write(RUNS + '/s16-e4.md', text)
    repo.write(LOG, json.dumps({'entries': [entry]}))
    repo.commit_all('seal source')
    return {'E4': {'path': path, 'text': text}}


def test_real_packet_admission_then_proposal_tamper(repo):
    records = setup_packet(repo)
    assert validate_sources(repo.root, records, repo.root / RUNS, LOG).passed
    record = records['E4']
    record['text'] = record['text'].replace('## Mechanism output', '## Discarded output')
    record['path'].write_text(record['text'])
    repo.commit_all('alter source')
    with pytest.raises(ValueError, match='receipt gate rejected'):
        validate_sources(repo.root, records, repo.root / RUNS, LOG)


def test_late_dispatch_log_rejected(repo):
    records = setup_packet(repo, log_before=False)
    with pytest.raises(ValueError, match='added after invocation'):
        validate_sources(repo.root, records, repo.root / RUNS, LOG)


def test_missing_receipts_do_not_pass_empty_gate(repo):
    path = repo.write(RUNS + '/s16-e4.md', '- **Enactment status:** FAITHFUL\n')
    repo.write(LOG, '{"entries": []}')
    repo.commit_all('empty evidence')
    with pytest.raises(ValueError, match='requires real receipt'):
        validate_sources(repo.root, {'E4': {'path': path, 'text': path.read_text()}}, repo.root / RUNS, LOG)


def test_promise_baseline_is_explicit_and_deferred_entrant_is_blocked(repo):
    text = '- **Enactment status:** PROMISE ONLY\n- **Pass 1 provenance:** baseline\n'
    path = repo.write(RUNS + '/s16-a2.md', text)
    repo.write(LOG, '{"entries": []}')
    repo.commit_all('baseline')
    records = {'A2': {'path': path, 'text': text}}
    assert validate_sources(repo.root, records, repo.root / RUNS, LOG).passed
    with pytest.raises(ValueError, match='deferred entrant'):
        validate_sources(repo.root, {'M3': records['A2']}, repo.root / RUNS, LOG)


def test_e1_primary_draw_alone_cannot_release_packet(repo):
    from test_draw import with_pools, make, build_record, item_lines, parse_output, POOLS
    with_pools(repo)
    entry = {'entrant': 'E1', 'seed': 42, 'inputs': {POOLS: sha256_file(repo.root / POOLS)}}
    repo.write(LOG, json.dumps({'entries': [entry]}))
    repo.commit_all('pin primary draw')
    result, row, _ = make(repo, '--seed', '42')
    text = build_record('E1', [row['receipt_id']], result.stdout + item_lines(parse_output(result.stdout)))
    text = text.replace('## Provenance', '## Provenance\n- **Enactment status:** FAITHFUL')
    path = repo.write(RUNS + '/s16-e1.md', text)
    repo.commit_all('seal primary without replay')
    with pytest.raises(ValueError, match='counterfactual draw receipts'):
        validate_sources(repo.root, {'E1': {'path': path, 'text': text}}, repo.root / RUNS, LOG)
