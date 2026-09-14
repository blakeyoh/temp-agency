"""E3 thin adapter: authenticated route, independent verdict, retained regeneration."""
import json
import runpy
import pytest
from lib.frame_audit import KIND, EVALUATOR_BRIEF, routed_artifact
from lib.forage_audit import CONTEXT_PURPOSES
from lib.paths import canonical_json, sha256_file
from lib.verify.gate import run_gate
from test_route import prepare


def route(repo):
    prepare(repo)
    result = repo.run('bin/route','--entrant','E3','--brief','docs/brief.txt','--domain-specialist','beta')
    assert result.returncode == 0, result.stderr
    path = repo.receipts('E3')[-1]
    repo.commit_all('commit actual route receipt')
    return path


def round_inputs(repo, route_path, name, reject=False, previous=None, wrong_frame=False, self_review=False):
    base='docs/frame/'+name+'/'
    paths={key:base+key+('.txt' if key in ('brief','rubric') else '.json')
           for key in ('brief','artifact','candidate','rubric','response','manifest','invocation')}
    paths['route_receipt']=route_path.relative_to(repo.root).as_posix()
    if previous: paths['previous']=previous.relative_to(repo.root).as_posix()
    routed=json.loads(route_path.read_text())
    artifact=routed_artifact(repo.root,routed)
    if wrong_frame: artifact['lead']='gamma'
    candidate={'schema_version':1,'items':[{'id':'i'+str(i),'text':name+' rule '+str(i)+': wait for the soil to recover.'} for i in range(3)]}
    verdict={'schema_version':1,'verdicts':[{'item_id':row['id'],'decision':'unchanged' if reject and i==0 else 'dependent',
        'proposal_quote':row['text'],'artifact_quote':artifact['content'],
        'deletion_effect':'Synthetic fixture: deleting the frame removes the explicit condition.',
        'reason':'Synthetic enforcement evidence only, not a real model quality judgment.'} for i,row in enumerate(candidate['items'])]}
    request='gen-fixture-'+name
    packet={'content':'```json\n'+canonical_json(verdict)+'\n```','receipt':{
        'model':'z-ai/glm-5.3','provider':'Z.AI','request_id':request,'finish_reason':'stop','truncated':False}}
    repo.write(paths['brief'],(repo.root/'docs/brief.txt').read_text())
    repo.write(paths['rubric'],'Synthetic development rubric for frame checking.')
    for key,value in [('artifact',artifact),('candidate',candidate),('response',packet)]: repo.write(paths[key],canonical_json(value))
    hashes={paths[k]:sha256_file(repo.root/paths[k]) for k in CONTEXT_PURPOSES}
    manifest={'delegation':{'brief':EVALUATOR_BRIEF,'model':'z-ai/glm-5.3','provider_only':['z-ai'],
        'output_mode':'critique','acceptance_criteria':[],'constraints':[]},'context':[
        {'path':str(repo.root/paths[k]),'sha256':hashes[paths[k]],'purpose':purpose} for k,purpose in CONTEXT_PURPOSES.items()]}
    invocation={'schema_version':1,'kind':KIND,'mode':'development','independent':True,
        'generator_actor':'openrouter:'+request if self_review else 'fixture-author','evaluator_actor':'openrouter:'+request,
        'context_root':str(repo.root),'files_read':hashes,'disclosure':'Synthetic independent invocation fixture.'}
    repo.write(paths['manifest'],canonical_json(manifest));repo.write(paths['invocation'],canonical_json(invocation))
    repo.commit_all('seal '+name)
    seal=repo.git('rev-parse','HEAD').strip()
    repo.write(base+'dispatch.txt',seal);repo.commit_all('dispatch '+name)
    return paths,seal


def invoke(repo,paths,seal):
    args=['--entrant','E3','--seal-commit',seal,'--seed','3']
    for key,path in paths.items(): args+=['--'+key.replace('_','-'),path]
    return runpy.run_path(str(repo.root/'bin/frame-gate'))['main'](args)


def record(repo):
    rows=[json.loads(p.read_text()) for p in repo.receipts('E3')]
    last=json.loads(rows[-1]['output'])
    proposal='\n'.join(f"{i}. [{r['id']}] {r['text']}" for i,r in enumerate(last['candidate']['items'],1))
    return repo.write('docs/record.md','# E3\n\n## Provenance\n\n- **Entrant code:** E3\n\n'
        '## Mechanism output\n\nLEAD: alpha\nLENS: beta\n\n## Pass 1 proposal artifact\n\n'+proposal+
        '\n\n## Execution trace\n\n'+'\n'.join(r['output'] for r in rows)+'\n\n## Receipts\n\n'+
        '\n'.join('- '+r['receipt_id']+' '+r['tool'] for r in rows)+'\n')


def test_e3_rejection_regeneration_and_accepted_full_gate(repo):
    source=route(repo)
    paths,seal=round_inputs(repo,source,'first',reject=True)
    assert invoke(repo,paths,seal)==0
    prior=repo.receipts('E3')[-1]
    record(repo)
    assert not run_gate(repo.root,'docs/record.md').passed
    paths,seal=round_inputs(repo,source,'second',previous=prior)
    assert invoke(repo,paths,seal)==0
    target=record(repo)
    report=run_gate(repo.root,'docs/record.md')
    assert report.passed,'\n'.join(line.message for line in report.lines)
    text=target.read_text()
    target.write_text(text.replace('1. [i0] second rule','1. [i0] generic rule',1))
    assert not run_gate(repo.root,'docs/record.md').passed
    target.write_text(text.replace('- '+json.loads(prior.read_text())['receipt_id']+' frame-gate\n',''))
    assert not run_gate(repo.root,'docs/record.md').passed


@pytest.mark.parametrize('kind',['wrong_frame','self_review'])
def test_frame_substitution_and_self_review_rejected(repo,kind):
    from lib.errors import ToolError
    source=route(repo)
    paths,seal=round_inputs(repo,source,'bad',**{kind:True})
    with pytest.raises(ToolError): invoke(repo,paths,seal)
    assert repo.receipt('E3')['status']=='failed'
