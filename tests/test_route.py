import json
from pathlib import Path
import pytest
from lib.route import render
from lib.verify.gate import run_gate


def prepare(repo):
    for slug, text in [('alpha','soil soil seasons'),('beta','sound sound traffic'),('gamma','music music sound')]:
        repo.write('roster/'+slug+'.md',text)
    repo.write('references/roster.md','\n'.join('|`'+s+'` | Title | ✓ Built |' for s in ['alpha','beta','gamma']))
    repo.write('docs/brief.txt','sound music traffic')
    repo.commit_all('freeze routing corpus')


def test_route_replay_and_source_only_gate_rejection(repo):
    prepare(repo)
    result = repo.run('bin/route','--entrant','E3','--brief','docs/brief.txt','--domain-specialist','beta')
    assert result.returncode == 0, result.stderr
    receipt = repo.receipt('E3'); output = json.loads(receipt['output'])
    assert output['lead']=='alpha' and output['lens']=='beta'
    assert len(receipt['inputs'])==5
    assert repo.verify('replay',str(repo.receipts('E3')[-1])).returncode==0
    repo.write('docs/record.md','# E3\n\n## Provenance\n\n- **Entrant code:** E3\n\n## Mechanism output\n\n'
        'LEAD: alpha\nLENS: beta\n\n## Execution trace\n\n'+receipt['output']+'\n\n## Receipts\n\n- '+receipt['receipt_id']+' route\n')
    report=run_gate(repo.root,'docs/record.md')
    assert not report.passed
    assert any('bind fail' in line.message for line in report.lines)


@pytest.mark.parametrize('kind',['missing_profile','new_profile','unknown_lens','empty_brief'])
def test_invalid_routing_mints_failed_receipt(repo,kind):
    prepare(repo)
    if kind=='missing_profile': (repo.root/'roster/alpha.md').unlink()
    elif kind=='new_profile': repo.write('roster/delta.md','unexpected')
    elif kind=='empty_brief': repo.write('docs/brief.txt','the and of')
    if kind!='unknown_lens': repo.commit_all('changed routing corpus')
    result=repo.run('bin/route','--entrant','E3','--brief','docs/brief.txt','--domain-specialist','unknown' if kind=='unknown_lens' else 'beta')
    assert result.returncode!=0
    assert repo.receipt('E3')['status']=='failed'


def test_real_roster_route():
    root=Path(__file__).resolve().parents[1]
    result=json.loads(render(root,'docs/tournament/forage/calibration/brief.txt','references/roster.md','systems-thinker'))
    assert len(result['profiles'])==24
    assert result['lead']!=result['lens']


@pytest.mark.parametrize('label', ['LEAD: alpha-extra', 'LEAD: alpha\nLEAD: beta', 'NOT LEAD: alpha'])
def test_routing_label_cannot_be_substring_or_duplicate(repo, label):
    from lib.bindings.route import check
    prepare(repo)
    assert repo.run('bin/route','--entrant','E3','--brief','docs/brief.txt','--domain-specialist','beta').returncode == 0
    receipt=repo.receipt('E3')
    record='## Mechanism output\n\n'+label+'\nLENS: beta\n\n## Execution trace\n\n'+receipt['output']+'\n'
    result=check(record,receipt)
    assert not result.checks[0].passed
