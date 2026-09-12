"""M1 schemas and real offline semantic replay/gating (when the model is installed)."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

import pytest

from lib.overlap import decisions, items, threshold
from lib.paths import canonical_json, sha256_file
from lib.semantic import validate_manifest

ROOT = Path(__file__).resolve().parents[1]
BASE = 'docs/tournament/overlap/'
MANIFEST = BASE + 'model.json'
CONFIG = BASE + 'config.json'
MEDIAN = BASE + 'median.json'
CANDIDATE = BASE + 'candidate.json'
DISPATCH = BASE + 'dispatch.json'
SEMANTIC_AVAILABLE = bool(os.environ.get('HARNESS_MODEL_CACHE')) and bool(importlib.util.find_spec('torch'))
semantic = pytest.mark.skipif(not SEMANTIC_AVAILABLE, reason='install pinned runtime and set HARNESS_MODEL_CACHE')


def test_chosen_only_and_exact_threshold_rejection():
    claims = [{'id': 'forced', 'text': 'a', 'label': 'FORCED'},
              {'id': 'chosen', 'text': 'b', 'label': 'CHOSEN'}]
    rows = decisions(claims, [{'id': 's1', 'text': 'x'}, {'id': 's2', 'text': 'y'}],
                     [1.0, 0.7, 1.0, 0.699999], 0.7)
    assert rows[0]['decision'] == 'REJECT'
    assert rows[0]['overlapping_chosen'] == ['chosen']
    assert rows[1]['decision'] == 'KEEP'


@pytest.mark.parametrize('value', [True, 0, -1, 1.01, float('nan'), float('inf'), 0.1234567])
def test_invalid_threshold(value):
    with pytest.raises(ValueError):
        threshold({'schema_version': 1, 'metric': 'bidirectional-entailment-max', 'decimals': 6,
                   'threshold': value})


@pytest.mark.parametrize('rows', [[], [{'id': 'a', 'text': '', 'label': 'CHOSEN'}],
    [{'id': 'a', 'text': 'x', 'label': 'AMBIGUOUS'}],
    [{'id': 'a', 'text': 'x', 'label': 'CHOSEN'}] * 2])
def test_invalid_median(rows):
    with pytest.raises(ValueError):
        items({'claims': rows}, 'claims', True)


def test_manifest_requires_all_assets_and_runtime_pins():
    manifest = json.loads((ROOT / MANIFEST).read_text())
    validate_manifest(manifest)
    manifest['files'].pop('model.safetensors')
    with pytest.raises(ValueError):
        validate_manifest(manifest)


def inputs(repo, chosen=False):
    for path in (CONFIG, MANIFEST):
        repo.write(path, (ROOT / path).read_text())
    median = {'claims': [{'id': 'm1', 'label': 'CHOSEN' if chosen else 'FORCED',
                         'text': 'Submit complaints without names through a shared form.'}]}
    candidate = {'sections': [{'id': 's1', 'text': 'Report disturbances anonymously using one common questionnaire.'}]}
    repo.write(MEDIAN, canonical_json(median))
    repo.commit_all('seal development median before candidate')
    repo.write(CANDIDATE, canonical_json(candidate))
    hashes = {path: sha256_file(repo.root / path) for path in (CONFIG, MANIFEST, MEDIAN, CANDIDATE)}
    repo.write(DISPATCH, canonical_json({'entries': [{'entrant': 'M1', 'seed': 1, 'inputs': hashes}]}))
    repo.commit_all('freeze candidate and dispatch inputs')
    return candidate


def invoke(repo):
    return repo.run('bin/overlap', '--entrant', 'M1', '--seed', '1', '--median', MEDIAN,
                    '--candidate', CANDIDATE, '--config', CONFIG, '--model-manifest', MANIFEST)


def record(repo, candidate, receipt):
    text = ('# Development M1 record\n\n## Provenance\n\n- **Entrant code:** M1\n\n'
            '## Pass 1 proposal artifact\n\n1. ' + candidate['sections'][0]['text'] +
            '\n\n## Execution trace\n\n' + receipt['output'] +
            '\n## Receipts\n\n- ' + receipt['receipt_id'] + ' overlap\n')
    return repo.write(BASE + 'record.md', text)


@semantic
def test_real_model_calibration_and_holdout():
    from lib.semantic import entailment_scores
    manifest = json.loads((ROOT / MANIFEST).read_text())
    config = json.loads((ROOT / CONFIG).read_text())
    cases = json.loads((ROOT / (BASE + 'calibration.json')).read_text())['cases']
    scores = entailment_scores([(c['candidate'], c['median']) for c in cases], manifest)
    failures = [(c['id'], score, c['overlap']) for c, score in zip(cases, scores)
                if (round(score, 6) >= threshold(config)) != c['overlap']]
    assert not failures


@semantic
def test_real_archive_replay_and_honest_full_gate(repo):
    candidate = inputs(repo)
    proc = invoke(repo)
    assert proc.returncode == 0, proc.stderr
    receipt = repo.receipt('M1')
    path = repo.receipts('M1')[-1]
    assert json.loads(proc.stdout)['comparison']['passed']
    record(repo, candidate, receipt)
    replay = repo.verify('replay', str(path))
    assert replay.returncode == 0, replay.stdout + replay.stderr
    gate = repo.verify('all', '--records', BASE + 'record.md', '--dispatch-log', DISPATCH)
    assert gate.returncode == 0, gate.stdout + gate.stderr


@semantic
def test_real_paraphrase_rejection_requires_regeneration(repo):
    candidate = inputs(repo, chosen=True)
    proc = invoke(repo)
    assert proc.returncode == 0, proc.stderr
    receipt = repo.receipt('M1')
    assert not json.loads(proc.stdout)['comparison']['passed']
    target = record(repo, candidate, receipt)
    bound = repo.verify('bind', str(target), str(repo.receipts('M1')[-1]))
    assert bound.returncode == 1 and 'FAIL semantic_gate' in bound.stdout


@semantic
def test_missing_model_fails_receipt_without_lexical_fallback(repo, monkeypatch):
    inputs(repo)
    monkeypatch.setenv('HARNESS_MODEL_CACHE', str(repo.root / 'missing-cache'))
    proc = invoke(repo)
    assert proc.returncode == 1
    receipt = repo.receipt('M1')
    assert receipt['status'] == 'failed' and receipt['output'] == ''
    assert 'missing or changed semantic model file' in receipt['error']


@semantic
def test_overlength_pair_and_runtime_drift_fail_closed():
    from lib.semantic import entailment_scores
    manifest = json.loads((ROOT / MANIFEST).read_text())
    with pytest.raises(ValueError, match='exceeds 512'):
        entailment_scores([('word ' * 520, 'another claim')], manifest)
    manifest['runtime']['torch'] = '0.0.0'
    with pytest.raises(ValueError, match='runtime drift'):
        entailment_scores([('a claim', 'a claim')], manifest)


def test_trace_copy_cannot_satisfy_final_section_binding():
    from lib.bindings.overlap import final_sections_match
    sections = [{"id": "s1", "text": "Use a quiet entrance."}]
    honest = "## Pass 1 proposal artifact\n\n1. Use a quiet entrance.\n\n## Execution trace\n"
    assert final_sections_match(honest, sections)
    assert not final_sections_match(honest.replace("1. Use a quiet entrance.",
        "1. Add a public naming board.") + "Use a quiet entrance.", sections)
    assert not final_sections_match(honest + honest, sections)
    assert not final_sections_match(honest.replace("1. Use", "2. Use"), sections)
    assert not final_sections_match(honest.replace("entrance.", "entrance. Extra unchecked idea."), sections)
