import json
from pathlib import Path
import pytest
from lib.lexicon import scan
from lib.paths import canonical_json
from lib.verify.gate import run_gate


def prepare(repo):
    repo.write('roster/farmer.md', '# Farmer\nA fixture specialist.')
    repo.write('docs/lexicon.json', canonical_json({'schema_version':1, 'era':1911,
        'specialists':{'farmer':{'min_year':1911,'max_year':1911}},
        'forbidden_terms':['social media','LinkedIn','network']}))


def invoke(repo, name, text, previous=None, era=1911):
    path = 'docs/' + name + '.json'
    repo.write(path, canonical_json({'schema_version':1,'items':[{'id':'i1','text':text}]}))
    repo.commit_all('freeze ' + name)
    args = ['bin/lexicon-check','--entrant','E5','--lexicon','docs/lexicon.json',
            '--profile','roster/farmer.md','--candidate',path,'--specialist','farmer','--era',str(era)]
    if previous: args += ['--previous', previous.relative_to(repo.root).as_posix()]
    return repo.run(*args)


def record(repo):
    values = [json.loads(p.read_text()) for p in repo.receipts('E5')]
    candidate = json.loads(values[-1]['output'])['candidate']
    proposal = '\n'.join(f"{i}. [{r['id']}] {r['text']}" for i,r in enumerate(candidate['items'],1))
    return repo.write('docs/record.md','# E5\n\n## Provenance\n\n- **Entrant code:** E5\n\n'
        '## Pass 1 proposal artifact\n\n'+proposal+'\n\n## Execution trace\n\n'+
        '\n'.join(v['output'] for v in values)+'\n\n## Receipts\n\n'+
        '\n'.join('- '+v['receipt_id']+' lexicon-check' for v in values)+'\n')


def test_reject_regenerate_retain_full_gate_and_replay(repo):
    prepare(repo)
    assert invoke(repo,'first','Use social media.').returncode == 0
    prior = repo.receipts('E5')[-1]
    assert not json.loads(repo.receipt('E5')['output'])['passed']
    record(repo)
    assert not run_gate(repo.root,'docs/record.md').passed
    assert invoke(repo,'second','Exchange visiting cards.',prior).returncode == 0
    target = record(repo)
    report = run_gate(repo.root,'docs/record.md')
    assert report.passed, '\n'.join(x.message for x in report.lines)
    original = target.read_text()
    target.write_text(original.replace('- '+json.loads(prior.read_text())['receipt_id']+' lexicon-check\n',''))
    assert not run_gate(repo.root,'docs/record.md').passed
    target.write_text(original.replace('1. [i1] Exchange visiting cards.','1. [i1] Use LinkedIn.'))
    assert not run_gate(repo.root,'docs/record.md').passed
    repo.write('docs/second.json','{}')
    assert repo.verify('replay',str(repo.receipts('E5')[-1])).returncode == 0


@pytest.mark.parametrize('text',['Social\nmedia','SOCIAL-MEDIA','social_media','ＬｉｎｋｅｄＩｎ','my network'])
def test_normalized_term_detection(text):
    result = scan({'schema_version':1,'items':[{'id':'i1','text':text}]},['social media','LinkedIn','network'])
    assert result


def test_unchanged_leak_cannot_be_resubmitted(repo):
    prepare(repo)
    assert invoke(repo,'first','Use LinkedIn.').returncode == 0
    assert invoke(repo,'second','Use LinkedIn.',repo.receipts('E5')[-1]).returncode != 0
    assert repo.receipt('E5')['status'] == 'failed'


def test_unconfigured_era_rejected(repo):
    prepare(repo)
    assert invoke(repo,'first','Exchange cards.',era=1950).returncode != 0
    assert repo.receipt('E5')['status'] == 'failed'


def test_real_era_metadata_covers_roster():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root/'docs/tournament/eras/1911.json').read_text())
    assert set(data['specialists']) == {p.stem for p in (root/'roster').glob('*.md') if p.stem!='TEMPLATE'}
    assert data['era'] == 1911
