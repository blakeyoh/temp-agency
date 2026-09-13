"""E2 source lifecycle: genuine adapter contract, failed network, no fetch-only pass."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import pytest

from lib import forage_wikipedia as wiki
from lib.errors import ToolError
from lib.paths import canonical_json
from lib.verify.gate import run_gate
from test_forage_wikipedia import payload, DATE

ROOT = Path(__file__).resolve().parents[1]
POOLS = 'docs/tournament/forage/corpora.json'


def prepare(repo):
    repo.write(POOLS, (ROOT / POOLS).read_text())
    repo.commit_all('freeze E2 corpora')
    drawn = repo.run('bin/draw', '--entrant', 'E2', '--pools', POOLS, '--seed', '1')
    assert drawn.returncode == 0
    path = repo.receipts('E2')[-1]
    repo.commit_all('commit corpus selection before server draw')
    return path.relative_to(repo.root).as_posix()


def invoke(repo, selection):
    tool = runpy.run_path(str(repo.root / 'bin/forage'))
    return tool['main'](['--entrant', 'E2', '--pools', POOLS, '--selection', selection, '--seed', '2'])


def test_fetch_receipt_and_no_fetch_only_enactment(repo, monkeypatch):
    selection = prepare(repo)
    monkeypatch.setattr('lib.tools.utc_now', lambda: '2026-09-13T12:00:01+00:00')
    monkeypatch.setattr(wiki, '_http_get', lambda url: (json.dumps(payload()).encode(), {'Date': DATE}))
    assert invoke(repo, selection) == 0
    fetched = repo.receipt('E2')
    assert fetched['status'] == 'ok'
    assert fetched['verification_class'] == 'hash-attested'
    assert json.loads(fetched['output'])['artifact']['revid'] == 42
    draw = repo.receipt('E2', 0)
    repo.write_record('e2.md', 'E2', [draw['receipt_id'], fetched['receipt_id']],
                      draw['output'] + fetched['output'])
    result = run_gate(repo.root, 'docs/tournament/official-runs/e2.md')
    assert not result.passed
    assert any('bind fail' in line.message for line in result.lines)
    sidecar_path = repo.receipts('E2')[-1].with_suffix('.bind.json')
    checks = json.loads(sidecar_path.read_text())['checks']
    assert next(c for c in checks if c['name'] == 'source_attestation')['pass']
    assert not next(c for c in checks if c['name'] == 'deletion_gate')['pass']


def test_network_failure_issues_failed_receipt(repo, monkeypatch):
    selection = prepare(repo)
    def broken(url):
        raise TimeoutError('network unreachable')
    monkeypatch.setattr(wiki, '_http_get', broken)
    with pytest.raises(ToolError, match='failed receipt'):
        invoke(repo, selection)
    receipt = repo.receipt('E2')
    assert receipt['status'] == 'failed' and receipt['output'] == ''
    assert 'network unreachable' in receipt['error']


def test_forged_corpus_draw_rejected_before_network(repo, monkeypatch):
    selection = prepare(repo)
    draw = repo.receipt('E2')
    draw['output'] = draw['output'].replace('corpus: [0]', 'corpus: [99]')
    repo.write('docs/forged-draw.json', canonical_json(draw))
    repo.commit_all('commit forged draw fixture')
    called = []
    monkeypatch.setattr(wiki, '_http_get', lambda url: called.append(url))
    with pytest.raises(ToolError):
        invoke(repo, 'docs/forged-draw.json')
    assert called == []
    assert repo.receipt('E2')['status'] == 'failed'


@pytest.mark.parametrize('mutation', ['argv', 'commit'])
def test_attestation_rejects_unpinned_execution_claims(repo, monkeypatch, mutation):
    from lib.forage import verify_attestation
    selection = prepare(repo)
    monkeypatch.setattr('lib.tools.utc_now', lambda: '2026-09-13T12:00:01+00:00')
    monkeypatch.setattr(wiki, '_http_get', lambda url: (json.dumps(payload()).encode(), {'Date': DATE}))
    assert invoke(repo, selection) == 0
    receipt = repo.receipt('E2')
    if mutation == 'argv':
        receipt['argv'][receipt['argv'].index('--selection') + 1] = 'different.json'
    else:
        receipt['repo_commit'] = 'f' * 40
    assert verify_attestation(repo.root, receipt)
