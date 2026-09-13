"""A real earlier git seal is required; asserted isolation alone is insufficient."""
from __future__ import annotations

import json

import pytest

from lib.paths import canonical_json, sha256_file

MEDIAN = 'docs/median.json'
INVOCATION = 'docs/invocation.json'
BRIEF = 'docs/brief.txt'


def sealed_inputs(repo, change=None):
    for path in ('AGENTS.md', 'CLAUDE.md', BRIEF):
        repo.write(path, 'Development context: ' + path + '\n')
    repo.write(MEDIAN, canonical_json({'claims': [
        {'id': 'm1', 'label': 'CHOSEN', 'text': 'Use a shared anonymous feedback form.'}]}))
    invocation = {'schema_version': 1, 'kind': 'isolated-median', 'mode': 'development',
                  'entrant': 'M1', 'actor': 'test isolated worker', 'model': 'test-model',
                  'median_path': MEDIAN, 'median_sha256': sha256_file(repo.root / MEDIAN),
                  'brief_path': BRIEF, 'candidate_exposure': False,
                  'disclosure': 'Development host attestation; not cryptographic isolation.',
                  'files_read': {p: sha256_file(repo.root / p)
                                 for p in ('AGENTS.md', 'CLAUDE.md', BRIEF)}}
    if change:
        change(invocation)
    repo.write(INVOCATION, canonical_json(invocation))
    repo.commit_all('seal isolated median before candidate exists')
    seal = repo.git('rev-parse', 'HEAD').strip()
    repo.write('docs/readiness.txt', 'Later candidate preparation begins.\n')
    repo.commit_all('later readiness commit')
    return seal


def invoke_seal(repo, seal):
    return repo.run('bin/seal-median', '--entrant', 'M1', '--median', MEDIAN,
                    '--invocation', INVOCATION, '--seal-commit', seal, '--seed', '7')


def test_honest_seal_and_binding(repo):
    from lib.median_seal import verify_attestation
    seal = sealed_inputs(repo)
    result = invoke_seal(repo, seal)
    assert result.returncode == 0, result.stderr
    receipt = repo.receipt('M1')
    assert verify_attestation(repo.root, receipt) == []
    record = repo.write_record('m1.md', 'M1', [receipt['receipt_id']], receipt['output'])
    bound = repo.verify('bind', str(record), str(repo.receipts('M1')[-1]))
    assert bound.returncode == 0, bound.stdout + bound.stderr


@pytest.mark.parametrize('exposure', [True, 0, None])
def test_exposed_or_ambiguous_context_mints_failed_receipt(repo, exposure):
    seal = sealed_inputs(repo, lambda value: value.update(candidate_exposure=exposure))
    assert invoke_seal(repo, seal).returncode == 1
    assert repo.receipt('M1')['status'] == 'failed'


def test_extra_context_rejected(repo):
    repo.write('candidate.txt', 'Candidate contamination')
    seal = sealed_inputs(repo, lambda value: value['files_read'].update(
        {'candidate.txt': sha256_file(repo.root / 'candidate.txt')}))
    assert invoke_seal(repo, seal).returncode == 1
    assert repo.receipt('M1')['status'] == 'failed'


@pytest.mark.parametrize('kind', ['nonexistent', 'same_commit', 'changed_median'])
def test_fabricated_or_unordered_seal_fails(repo, kind):
    seal = sealed_inputs(repo)
    if kind == 'nonexistent':
        seal = 'f' * 40
    elif kind == 'same_commit':
        seal = repo.git('rev-parse', 'HEAD').strip()
    else:
        repo.write(MEDIAN, canonical_json({'claims': [
            {'id': 'm1', 'label': 'FORCED', 'text': 'Changed after seal.'}]}))
        repo.commit_all('replace sealed median')
    assert invoke_seal(repo, seal).returncode == 1
    assert repo.receipt('M1')['status'] == 'failed'


def test_attestation_checks_git_blobs_not_mutable_worktree(repo):
    from lib.median_seal import verify_attestation
    seal = sealed_inputs(repo)
    assert invoke_seal(repo, seal).returncode == 0
    receipt = repo.receipt('M1')
    repo.write(INVOCATION, '{}')
    assert verify_attestation(repo.root, receipt) == []
    forged = json.loads(json.dumps(receipt))
    forged['external_attestation']['seal_commit'] = 'f' * 40
    assert verify_attestation(repo.root, forged)


def test_self_consistent_forgery_passes_chain_but_fails_full_gate(repo):
    from lib.receipt import ISSUED_FIELDS, issue, mint_nonce, verify_chain
    from lib.median_seal import expected_output
    from lib.paths import sha256_bytes
    seal = sealed_inputs(repo)
    assert invoke_seal(repo, seal).returncode == 0
    honest = repo.receipt('M1')
    forged = {key: json.loads(json.dumps(honest[key])) for key in ISSUED_FIELDS}
    forged['external_attestation']['seal_commit'] = 'f' * 40
    position = forged['argv'].index('--seal-commit') + 1
    forged['argv'][position] = 'f' * 40
    identity = {k: v for k, v in forged['external_attestation'].items() if k != 'kind'}
    median = json.loads(honest['output'])['median']
    forged['output'] = expected_output(median, identity)
    forged['output_sha256'] = sha256_bytes(forged['output'].encode())
    issue(repo.root, mint_nonce(repo.root), **forged)
    fake = repo.receipt('M1')
    assert verify_chain(repo.root, 'M1') == []
    repo.write_record('m1.md', 'M1', [honest['receipt_id'], fake['receipt_id']],
                      honest['output'] + fake['output'])
    gate = repo.verify('all', '--records', 'docs/tournament/official-runs/m1.md')
    assert gate.returncode == 1, gate.stdout + gate.stderr
    assert 'attestation:' in gate.stdout and 'seal_commit is not a commit' in gate.stdout


def test_argument_values_must_match_attested_inputs(repo):
    from lib.median_seal import verify_attestation
    seal = sealed_inputs(repo)
    assert invoke_seal(repo, seal).returncode == 0
    receipt = repo.receipt('M1')
    receipt['argv'][receipt['argv'].index('--median') + 1] = 'different.json'
    assert any('argv --median' in p for p in verify_attestation(repo.root, receipt))
