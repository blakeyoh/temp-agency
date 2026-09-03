"""Focused regression tests for round-specific tournament tally behavior."""
import copy
import json
import os
import sys
import unittest

HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
import tally


def live_record(side='B'):
    return {
        'winner':side,
        'decided':'mechanism evidence',
        'yield':side,
        'yield_evidence':{
            'strongest_a':'A17','return_a':'causal A','repeat_a':'A20',
            'strongest_b':'B19','return_b':'causal B','repeat_b':'NONE',
            'reason':'late-window comparison','sealed':'2026-08-27T12:00:00Z',
        },
        'output_opened':'2026-08-27T11:59:00Z',
        'mechanism_opened':'2026-08-27T12:01:00Z',
        'axes':{a:{'side':side,'pts':1,'ref':'fixed anchor','pred':'falsifiable output'}
                for a in tally.AXES},
        'absorb':{'mech':'loser mechanism','same':'FAIL — distinct thesis',
                  'del':'FAIL — merely smaller','one':'FAIL — requires and also',
                  'disp':'ORTHOGONAL','note':'kept separate'},
        'enactment':{'A':'PROMISE ONLY','B':'FAITHFUL'},
        'enactment_evidence':'execution traces',
        'sacrifice':{'honored':'x','sacrificed':'y','cost':'z','validation':'conflict'},
        'collision':{'candidate':'NONE','mechanism':'N/A','not_a':'N/A',
                     'not_b':'N/A','why':'N/A'},
    }


class TallyTests(unittest.TestCase):
    def test_parser_captures_yield_and_enactment_evidence(self):
        text='''- **Output packet opened (UTC):** 2026-08-27T11:59:00Z
- **Mechanism packet opened (UTC):** 2026-08-27T12:01:00Z
## MATCHUP 1
WINNER: B
DECIDED BY: mechanism evidence

### PASS 1 — OUTPUT-ONLY YIELD
STRONGEST A: A17 moat
A RETURN PATH: protects the house
A REPETITION ONSET: A20
STRONGEST B: B19 UFO
B RETURN PATH: intercepts the threat
B REPETITION ONSET: NONE
YIELD VERDICT: TIE
YIELD REASON: both late windows travel
PASS 1 SEALED (UTC): 2026-08-27T12:00:00Z

### FAITHFUL ENACTMENT
A STATUS: PROMISE ONLY
B STATUS: FAITHFUL
EVIDENCE: traces/a.md and traces/b.md
'''
        rec=tally.parse_panel(text)[1]
        self.assertIn('yield',rec)
        self.assertIsNone(rec['yield'])
        self.assertEqual('A17 moat',rec['yield_evidence']['strongest_a'])
        self.assertEqual('2026-08-27T12:00:00Z',rec['yield_evidence']['sealed'])
        self.assertEqual('2026-08-27T12:01:00Z',rec['mechanism_opened'])
        self.assertEqual('2026-08-27T11:59:00Z',rec['output_opened'])
        self.assertEqual('traces/a.md and traces/b.md',rec['enactment_evidence'])

    def test_parser_rejects_duplicate_matchups_within_one_file(self):
        text='''## MATCHUP 1
WINNER: A
## MATCHUP 1
WINNER: B
'''
        with self.assertRaisesRegex(ValueError,'duplicate matchup records'):
            tally.parse_panel(text)

    def test_blank_structured_fields_do_not_consume_the_next_label(self):
        # Blank overall and axis verdicts must not borrow text from the next line.
        blank=tally.parse_panel(
            '## MATCHUP 1\nWINNER: A\nDECIDED BY:\n'
            '### PASS 1 — OUTPUT-ONLY YIELD\n')[1]
        self.assertEqual('',blank['decided'])
        axis_vote=tally.parse_panel(
            '## MATCHUP 1\nWINNER: A\n### Distance\n'
            'VERDICT:\nREFERENCE: A significantly better than the floor\n'
            'PREDICATE: concrete predicate\n')[1]
        self.assertNotIn('Distance',axis_vote['axes'])
        # A blank axis REFERENCE must not swallow the following PREDICATE line.
        axis=tally.parse_panel(
            '## MATCHUP 1\nWINNER: A\n### Distance\n'
            'VERDICT: A slightly better\nREFERENCE:\nPREDICATE: concrete predicate\n')[1]
        self.assertEqual('',axis['axes']['Distance']['ref'])
        self.assertEqual('concrete predicate',axis['axes']['Distance']['pred'])
        # A blank enactment EVIDENCE must not capture the --- separator.
        enact=tally.parse_panel(
            '## MATCHUP 1\nWINNER: A\n### FAITHFUL ENACTMENT\n'
            'A STATUS: FAITHFUL\nB STATUS: PROMISE ONLY\nEVIDENCE:\n\n---\n')[1]
        self.assertEqual('',enact['enactment_evidence'])
        # A blank Sacrifice receipt must not capture the next receipt line.
        sac=tally.parse_panel(
            '## MATCHUP 1\nWINNER: A\n### SACRIFICE RECEIPT\n'
            'HONORED:\nSACRIFICED: competing principle\n'
            'ACCEPTED COST: a cost\nVALIDATION: a validation\n')[1]
        self.assertNotIn('honored',sac['sacrifice'])
        self.assertEqual('competing principle',sac['sacrifice']['sacrificed'])
        # A blank absorption field must not capture the next receipt line.
        absorb=tally.parse_panel(
            '## MATCHUP 1\nWINNER: A\n### ABSORPTION\n'
            "LOSER'S STRONGEST MECHANISM:\nSAME-THESIS: FAIL — distinct thesis\n")[1]
        self.assertEqual('',absorb['absorb']['mech'])
        self.assertEqual('FAIL — distinct thesis',absorb['absorb']['same'])

    def test_tie_ballots_count_in_yield_vote(self):
        self.assertIsNone(tally.majority(['A',None,None],count_ties=True))
        self.assertEqual('A',tally.majority(['A','A',None],count_ties=True))

    def test_live_record_requires_auditable_evidence(self):
        rec=live_record()
        self.assertEqual([],tally.validate_live_record(rec))
        rec['axes']['Distance']['pred']=''
        self.assertIn('axis-evidence:Distance',tally.validate_live_record(rec))
        rec=live_record(); del rec['yield_evidence']['sealed']
        self.assertIn('yield-evidence:sealed',tally.validate_live_record(rec))
        rec=live_record(); rec['enactment_evidence']=' '
        self.assertIn('enactment-evidence',tally.validate_live_record(rec))
        rec=live_record(); rec['axes']['Distance']['ref']=tally.AXIS_REFERENCE_PLACEHOLDER
        self.assertIn('axis-placeholders:Distance',tally.validate_live_record(rec))
        rec=live_record(); rec['enactment_evidence']=tally.ENACTMENT_PLACEHOLDER
        self.assertIn('enactment-placeholder',tally.validate_live_record(rec))
        rec=live_record(); rec['sacrifice']['honored']=tally.SACRIFICE_PLACEHOLDERS['honored']
        self.assertIn('sacrifice-placeholders:honored',tally.validate_live_record(rec))
        rec=live_record(); rec['collision']['candidate']='NONE / short name'
        self.assertIn('collision-placeholders:candidate',tally.validate_live_record(rec))

    def test_refused_is_not_a_disposition(self):
        rec=live_record(); rec['absorb']['disp']='REFUSED'
        self.assertIn('absorption',tally.validate_live_record(rec))

    def test_absorption_requires_receipts_and_consistent_disposition(self):
        rec=live_record(); del rec['absorb']['same']
        self.assertIn('absorption-evidence:same',tally.validate_live_record(rec))
        rec=live_record(); rec['absorb'].update(
            {'same':'PASS — yes','del':'PASS — worse','one':'PASS — one claim',
             'disp':'ORTHOGONAL'})
        self.assertIn('absorption-inconsistent',tally.validate_live_record(rec))
        rec['absorb']['disp']='ABSORBED'
        self.assertNotIn('absorption-inconsistent',tally.validate_live_record(rec))
        rec['absorb']['disp']='SUBSUMED'
        self.assertIn('absorption-inconsistent',tally.validate_live_record(rec))

    def test_absorption_rejects_unresolved_or_unexplained_tests(self):
        rec=live_record(); rec['absorb']['same']='PASS / FAIL — reason'
        self.assertIn('absorption-tests',tally.validate_live_record(rec))
        rec=live_record(); rec['absorb']['same']='PASS'
        self.assertIn('absorption-tests',tally.validate_live_record(rec))
        rec=live_record(); rec['absorb']['same']='PASS — reason'
        self.assertIn('absorption-tests',tally.validate_live_record(rec))
        rec=live_record(); rec['absorb']['same']='PASS — supported by the receipt'
        self.assertNotIn('absorption-tests',tally.validate_live_record(rec))

    def test_pass_1_seal_requires_an_explicit_utc_timestamp(self):
        rec=live_record(); rec['yield_evidence']['sealed']='later'
        self.assertIn('yield-seal',tally.validate_live_record(rec))
        rec['yield_evidence']['sealed']='2026-08-27T12:00:00Z'
        self.assertNotIn('yield-seal',tally.validate_live_record(rec))

    def test_pass_1_must_precede_mechanism_disclosure(self):
        rec=live_record(); rec['mechanism_opened']='2026-08-27T11:59:59Z'
        self.assertIn('pass1-chronology',tally.validate_live_record(rec))
        rec['mechanism_opened']='2026-08-27T12:00:01Z'
        self.assertNotIn('pass1-chronology',tally.validate_live_record(rec))
        rec['output_opened']='2026-08-27T12:00:01Z'
        self.assertIn('pass1-chronology',tally.validate_live_record(rec))

    def test_blank_pass_1_field_does_not_consume_the_next_label(self):
        text='''## MATCHUP 1
### PASS 1 — OUTPUT-ONLY YIELD
STRONGEST A:
A RETURN PATH: causal A
A REPETITION ONSET: A20
'''
        evidence=tally.parse_panel(text)[1]['yield_evidence']
        self.assertNotIn('strongest_a',evidence)
        self.assertEqual('causal A',evidence['return_a'])

    def test_pass_1_template_boilerplate_is_rejected(self):
        for field,placeholder in tally.YIELD_PLACEHOLDERS.items():
            with self.subTest(field=field):
                rec=live_record(); rec['yield_evidence'][field]=placeholder
                errors=tally.validate_live_record(rec)
                self.assertTrue(any(e.startswith('yield-placeholders:') for e in errors))

    def test_enactment_limit_alone_is_not_contested(self):
        names=['Builder','Fresh One','Fresh Two']
        panels={p:{1:copy.deepcopy(live_record())} for p in names}
        result=tally.tally(panels,{1:{'A':'X','B':'Y','region':'Test'}},names)[1]
        self.assertIn('ENACTMENT-LIMIT',result['splits'])
        self.assertFalse(result['contested'])
        panels['Fresh Two'][1]['enactment']['A']='PARTIAL'
        self.assertTrue(tally.tally(
            panels,{1:{'A':'X','B':'Y','region':'Test'}},names)[1]['contested'])

    def test_suffix_colliding_panel_tags_are_rejected(self):
        self.assertEqual([('builder','fresh-builder')],
                         tally.suffix_collisions(['builder','fresh-builder','play']))
        self.assertEqual([],tally.suffix_collisions(['builder','fresh-one','fresh-two']))

    def test_specialists_and_pack_claims_match_filesystem(self):
        valid={'lead':'nuclear-reactor-operator','lens':'magician-illusionist',
               'lead_pack':'complete','lens_pack':'complete'}
        self.assertEqual([],tally.specialist_errors(valid))
        invalid={**valid,'lead':'does-not-exist'}
        self.assertIn('lead-profile',tally.specialist_errors(invalid))
        false_pack={**valid,'lead_pack':'incomplete'}
        self.assertIn('lead-pack-status',tally.specialist_errors(false_pack))

    def test_sweet_16_anchor_identity_and_roster_are_pinned(self):
        builder={'name':'Builder','file_tag':'builder','fresh':False,
                 'lead':'nuclear-reactor-operator','lens':'magician-illusionist'}
        fresh=[{'name':'Fresh One','fresh':True},{'name':'Fresh Two','fresh':True}]
        self.assertEqual([],tally.anchor_errors('s16',[builder,*fresh]))
        wrong={**builder,'lens':'farmer'}
        self.assertEqual(['lens'],tally.anchor_errors('s16',[wrong,*fresh]))

    def test_fresh_panels_require_distinct_specialist_pairs(self):
        fresh=[{'fresh':True,'lead':'farmer','lens':'physicist'},
               {'fresh':True,'lead':'physicist','lens':'farmer'}]
        self.assertEqual(['duplicate-panel-pair'],tally.fresh_pair_errors(fresh))
        fresh[1]['lens']='skeptic'
        self.assertEqual([],tally.fresh_pair_errors(fresh))
        anchor={'fresh':False,'lead':'physicist','lens':'farmer'}
        self.assertEqual(['duplicate-panel-pair'],tally.fresh_pair_errors([anchor,*fresh]))

    def test_verdict_declaration_is_bound_to_panel_and_draw(self):
        spec={'name':'Fresh One','lead':'farmer','lens':'physicist'}
        draw={'seed':17,'_commit':'a'*40}
        text=('- **Panel name:** Fresh One\n'
              '- **Lead specialist:** farmer\n'
              '- **Lens specialist:** physicist\n'
              '- **Draw seed and draw-map commit:** 17 / '+('a'*40)+'\n'
              '- **Output packet opened (UTC):** 2026-09-01T10:00:00Z\n'
              '- **Mechanism packet opened (UTC):** 2026-09-01T10:30:00Z\n'
              '- **Isolation attestation:** '+tally.ISOLATION_ATTESTATION+'\n\n---\n')
        self.assertEqual([],tally.panel_declaration_errors(text,spec,draw))
        self.assertEqual(['name'],
            tally.panel_declaration_errors(text.replace('Fresh One','Fresh Two',1),spec,draw))

    def test_verdict_declaration_requires_provenance_receipts(self):
        spec={'name':'Fresh One','lead':'farmer','lens':'physicist'}
        draw={'seed':17,'_commit':'a'*40}
        text=('- **Panel name:** Fresh One\n'
              '- **Lead specialist:** farmer\n'
              '- **Lens specialist:** physicist\n'
              '- **Draw seed and draw-map commit:** 17 / '+('a'*40)+'\n'
              '- **Output packet opened (UTC):** 2026-09-01T10:00:00Z\n'
              '- **Mechanism packet opened (UTC):** 2026-09-01T10:30:00Z\n'
              '- **Isolation attestation:** '+tally.ISOLATION_ATTESTATION+'\n\n---\n')
        # A blank isolation attestation is not a receipt.
        blank=text.replace('- **Isolation attestation:** '+tally.ISOLATION_ATTESTATION,
                           '- **Isolation attestation:**')
        self.assertIn('isolation-attestation',
                      tally.panel_declaration_errors(blank,spec,draw))
        # A missing output-packet-open timestamp is rejected.
        no_output=text.replace('2026-09-01T10:00:00Z','')
        self.assertIn('output-packet-open',
                      tally.panel_declaration_errors(no_output,spec,draw))
        # The output packet must open no later than mechanism disclosure.
        reversed_order=text.replace('2026-09-01T10:00:00Z','2026-09-01T11:00:00Z')
        self.assertIn('packet-chronology',
                      tally.panel_declaration_errors(reversed_order,spec,draw))

    def test_decided_by_placeholder_is_rejected(self):
        rec=live_record()
        rec['decided']=('One sentence naming the decisive mechanism evidence. '
                        'This is the Pass 2 overall')
        self.assertIn('decided-placeholder',tally.validate_live_record(rec))
        rec['decided']=''
        self.assertIn('decided-by',tally.validate_live_record(rec))
        self.assertNotIn('decided-placeholder',tally.validate_live_record(live_record()))

    def test_committed_version_rejects_dirty_and_uncommitted_artifacts(self):
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as repo:
            def git(*a):
                subprocess.run(['git',*a],cwd=repo,check=True,
                               stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            git('init'); git('config','user.email','t@example.com'); git('config','user.name','t')
            path=os.path.join(repo,'artifact.json')
            with open(path,'w') as fh: fh.write('{"frozen": true}\n')
            # Untracked -> not frozen.
            self.assertEqual('',tally.committed_version(path,repo))
            git('add','artifact.json'); git('commit','-m','freeze')
            self.assertRegex(tally.committed_version(path,repo),r'^[0-9a-f]{40}$')
            # An operator edit after freezing is no longer frozen.
            with open(path,'w') as fh: fh.write('{"frozen": false}\n')
            self.assertEqual('',tally.committed_version(path,repo))
            # Staged-but-uncommitted is still dirty.
            git('add','artifact.json')
            self.assertEqual('',tally.committed_version(path,repo))

    def test_dirty_paths_handles_git_quoted_filenames(self):
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as repo:
            def git(*a):
                subprocess.run(['git',*a],cwd=repo,check=True,
                               stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            git('init'); git('config','user.email','t@example.com'); git('config','user.name','t')
            paths=[]
            for name in ('artifact with spaces.md','artifact-\N{SNOWMAN}.md'):
                path=os.path.join(repo,name)
                with open(path,'w') as fh: fh.write('frozen\n')
                paths.append(path)
            git('add','.'); git('commit','-m','freeze')
            for path in paths:
                with open(path,'a') as fh: fh.write('operator edit\n')
            dirty=tally.dirty_paths(paths,repo)
            self.assertEqual(set(map(os.path.realpath,paths)),dirty)
            for path in paths:
                self.assertEqual('',tally.committed_version(path,repo,dirty_set=dirty))

    def test_dirty_paths_marks_both_sides_of_a_staged_rename(self):
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as repo:
            def git(*a):
                subprocess.run(['git',*a],cwd=repo,check=True,
                               stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            git('init'); git('config','user.email','t@example.com'); git('config','user.name','t')
            old=os.path.join(repo,'old artifact.md')
            new=os.path.join(repo,'new artifact.md')
            with open(old,'w') as fh: fh.write('frozen\n')
            git('add','.'); git('commit','-m','freeze')
            git('mv','old artifact.md','new artifact.md')
            dirty=tally.dirty_paths([old,new],repo)
            self.assertEqual({os.path.realpath(old),os.path.realpath(new)},dirty)

    def test_elite_8_field_derives_from_committed_ledger(self):
        # A non-downstream round has no advancement field.
        self.assertIsNone(tally.advancement_field('s16'))
        # With no committed post-ruling ledger, the field is empty and blocks any E8 draw.
        self.assertEqual(set(),tally.advancement_field('e8'))

    def test_elite_8_ledger_requires_commissioner_attestation(self):
        import json, subprocess, tempfile
        with tempfile.TemporaryDirectory() as repo:
            tournament=os.path.join(repo,'docs','tournament')
            os.makedirs(tournament)
            def git(*args):
                subprocess.run(['git',*args],cwd=repo,check=True,
                               stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            git('init'); git('config','user.email','t@example.com'); git('config','user.name','t')
            path=os.path.join(tournament,'s16-advancers.json')
            def commit_ledger(payload,message):
                with open(path,'w') as fh: json.dump(payload,fh)
                git('add','docs/tournament/s16-advancers.json'); git('commit','-m',message)
            codes=list(tally.S16_SURVIVOR_ORDER[:8])
            commit_ledger({'advancers':codes},'draft')
            self.assertEqual(set(),tally.advancement_field('e8',repo))
            commit_ledger({'round':'s16','ratified_by':'panel','advancers':codes},'panel')
            self.assertEqual(set(),tally.advancement_field('e8',repo))
            commit_ledger({'round':'s16','ratified_by':'commissioner','advancers':codes},'ratify')
            self.assertEqual(set(codes),tally.advancement_field('e8',repo))

    def test_draw_rejects_reused_games_and_entrants(self):
        games=[{'g':1,'A':'E1','B':'E2','region':'One'},
               {'g':1,'A':'E2','B':'E3','region':'Two'}]
        errors=tally.draw_errors(games)
        self.assertIn('duplicate-game-id',errors)
        self.assertIn('duplicate-entrant',errors)
        self.assertIn('missing-games',tally.draw_errors([]))

    def test_sweet_16_draw_requires_all_eight_numbered_games(self):
        entrants=sorted(tally.S16_SURVIVORS)
        games=[{'g':n,'A':entrants[(n-1)*2],'B':entrants[(n-1)*2+1],'region':'Test'}
               for n in range(1,9)]
        self.assertEqual([],tally.draw_errors(games,'s16'))
        errors=tally.draw_errors(games[:-1],'s16')
        self.assertIn('s16-game-count',errors)
        self.assertIn('s16-game-ids',errors)
        games[0]['A']='TYPO'
        self.assertIn('s16-survivor-field',tally.draw_errors(games,'s16'))

    def test_elite_8_draw_requires_prior_round_advancers(self):
        field={f'W{n}' for n in range(1,9)}
        entrants=sorted(field)
        games=[{'g':n,'A':entrants[(n-1)*2],'B':entrants[(n-1)*2+1],'region':'Test'}
               for n in range(1,5)]
        self.assertNotIn('e8-advancer-field',tally.draw_errors(games,'e8',field))
        games[0]['A']='TYPO'
        self.assertIn('e8-advancer-field',tally.draw_errors(games,'e8',field))

    def test_sweet_16_reseed_receipts_replay_draw(self):
        order=list(tally.S16_SURVIVOR_ORDER); seed=17; ab_seed=29
        shuffled=list(order); tally.random.Random(seed).shuffle(shuffled)
        ab=tally.random.Random(ab_seed); games=[]
        for n,index in enumerate(range(0,16,2),1):
            pair=shuffled[index:index+2]
            if ab.getrandbits(1): pair.reverse()
            games.append({'g':n,'A':pair[0],'B':pair[1],'region':'Test'})
        draw={'algorithm':'python-random-v1','seed':seed,'ab_seed':ab_seed,
              'input_order':order,'games':games}
        self.assertEqual([],tally.reseed_errors(draw))
        draw['seed']=True; draw['ab_seed']=False
        self.assertIn('reseed-seed',tally.reseed_errors(draw))
        self.assertIn('ab-seed',tally.reseed_errors(draw))
        draw['seed']=seed; draw['ab_seed']=ab_seed
        draw['games'][0]['A'],draw['games'][1]['A']=draw['games'][1]['A'],draw['games'][0]['A']
        self.assertIn('reseed-replay',tally.reseed_errors(draw))

    def test_committed_sweet_16_draw_is_live_tally_compatible(self):
        with open(os.path.join(os.path.dirname(__file__),'s16-draw-map.json')) as f:
            draw=json.load(f)
        self.assertEqual([], tally.draw_errors(draw['games'], 's16'))
        self.assertEqual([], tally.reseed_errors(draw))

    def test_elite_8_requires_committed_return_test_artifacts(self):
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as repo:
            def git(*args):
                subprocess.run(['git',*args],cwd=repo,check=True,
                               stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            git('init'); git('config','user.email','t@example.com'); git('config','user.name','t')
            os.makedirs(os.path.join(repo,'docs','tournament','artifacts'))
            artifacts={}
            for key in ('a_solo','b_solo','contact'):
                rel=f'docs/tournament/artifacts/g1-{key}.md'
                with open(os.path.join(repo,rel),'w') as fh: fh.write(key+'\n')
                artifacts[key]=rel
            git('add','.'); git('commit','-m','freeze return test')
            seed=17
            direction='A→B' if tally.random.Random(seed).getrandbits(1) else 'B→A'
            game={'g':1,'return_test':{'algorithm':'python-random-v1',
                                      'contact_seed':seed,'direction':direction,
                                      'artifacts':artifacts}}
            self.assertEqual([],tally.e8_return_errors([game],repo))
            game['return_test']['direction']='B→A' if direction == 'A→B' else 'A→B'
            self.assertIn('game-1-contact-direction',tally.e8_return_errors([game],repo))
            game['return_test']['direction']=direction
            game['return_test']['contact_seed']=True
            self.assertIn('game-1-contact-seed',tally.e8_return_errors([game],repo))
            game['return_test']['contact_seed']=seed
            with open(os.path.join(repo,artifacts['contact']),'a') as fh: fh.write('dirty\n')
            self.assertIn('game-1-contact-artifact',tally.e8_return_errors([game],repo))

    def test_elite_8_return_artifacts_reject_aliases_and_escapes(self):
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as repo:
            def git(*args):
                subprocess.run(['git',*args],cwd=repo,check=True,
                               stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            git('init'); git('config','user.email','t@example.com'); git('config','user.name','t')
            base='docs/tournament/artifacts'
            os.makedirs(os.path.join(repo,base))
            for name in ('one.md','two.md','three.md'):
                with open(os.path.join(repo,base,name),'w') as fh: fh.write(name+'\n')
            git('add','.'); git('commit','-m','freeze')
            seed=17
            direction='A→B' if tally.random.Random(seed).getrandbits(1) else 'B→A'
            def game(a,b,c):
                return {'g':1,'return_test':{'algorithm':'python-random-v1',
                        'contact_seed':seed,'direction':direction,
                        'artifacts':{'a_solo':a,'b_solo':b,'contact':c}}}
            # Lexical aliases of one committed file share a resolved identity.
            aliases=game(f'{base}/one.md',f'./{base}/one.md',
                         f'{base}/../artifacts/one.md')
            self.assertIn('duplicate-return-artifact',
                          tally.e8_return_errors([aliases],repo))
            # A symlink escaping the repository is rejected as an invalid artifact.
            outside=tempfile.NamedTemporaryFile(delete=False,suffix='.md')
            outside.write(b'x'); outside.close()
            try:
                os.symlink(outside.name,os.path.join(repo,base,'escape.md'))
                git('add','.'); git('commit','-m','link')
                errors=tally.e8_return_errors(
                    [game(f'{base}/escape.md',f'{base}/two.md',f'{base}/three.md')],repo)
                self.assertIn('game-1-a_solo-artifact',errors)
                self.assertNotIn('duplicate-return-artifact',errors)
            finally:
                os.unlink(outside.name)

    def test_elite_8_return_artifacts_reject_absolute_paths(self):
        # os.path.join discards its first argument when the second is absolute,
        # so an absolute path recorded under this exact checkout used to resolve
        # to a real, committed, in-repo file and pass every check — while being
        # unreplayable from any other clone. next-round-protocol.md requires
        # repository-relative paths.
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as repo:
            def git(*args):
                subprocess.run(['git',*args],cwd=repo,check=True,
                               stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            git('init'); git('config','user.email','t@example.com'); git('config','user.name','t')
            base='docs/tournament/artifacts'
            os.makedirs(os.path.join(repo,base))
            for name in ('a.md','b.md','c.md'):
                with open(os.path.join(repo,base,name),'w') as fh: fh.write(name+'\n')
            git('add','.'); git('commit','-m','freeze')
            seed=17
            direction='A→B' if tally.random.Random(seed).getrandbits(1) else 'B→A'
            abs_a=os.path.join(repo,base,'a.md')
            game={'g':1,'return_test':{'algorithm':'python-random-v1',
                    'contact_seed':seed,'direction':direction,
                    'artifacts':{'a_solo':abs_a,'b_solo':f'{base}/b.md','contact':f'{base}/c.md'}}}
            self.assertIn('game-1-a_solo-artifact-absolute',tally.e8_return_errors([game],repo))
            game['return_test']['artifacts']['a_solo']=f'{base}/a.md'
            self.assertEqual([],tally.e8_return_errors([game],repo))

    def test_verdict_accepts_only_canonical_strings(self):
        self.assertEqual(('A',3),tally.parse_verdict('A significantly better'))
        self.assertEqual(('B',1),tally.parse_verdict('b slightly better.'))
        self.assertEqual((None,0),tally.parse_verdict(' Tie '))
        for bad in ('B is not significantly better','A better','significantly better',
                    'A significantly worse','maybe A slightly better',''):
            with self.assertRaises(ValueError):
                tally.parse_verdict(bad)

    def test_malformed_axis_verdict_is_flagged_not_crashed(self):
        # A non-canonical verdict is captured as invalid (no score) instead of
        # aborting the whole parse, and is rejected by a targeted validation error.
        rec=tally.parse_panel('## MATCHUP 1\nWINNER: A\n### Distance\n'
            'VERDICT: B is not significantly better\nREFERENCE: r\nPREDICATE: p\n')[1]
        self.assertIsNone(rec['axes']['Distance']['pts'])
        live=live_record(); live['axes']['Distance']['pts']=None
        self.assertIn('axis-verdict:Distance',tally.validate_live_record(live))

    def test_absorption_allows_markdown_but_rejects_placeholders(self):
        self.assertEqual('PASS',tally.absorption_test(
            'PASS — supported by [G1 trace](artifacts/g1.md)'))
        self.assertIsNone(tally.absorption_test('PASS — [reason]'))
        self.assertIsNone(tally.absorption_test('FAIL — rationale'))
        # A placeholder embedded in prose must not clear the test either.
        self.assertIsNone(tally.absorption_test('PASS — resolved via [TODO fill in]'))
        self.assertEqual('FAIL',tally.absorption_test('FAIL — merely smaller'))

    def test_draw_rejects_boolean_game_id(self):
        self.assertIn('game-0-id',
                      tally.draw_errors([{'g':True,'A':'E3','B':'M5','region':'x'}]))

    def test_incomplete_panels_flags_any_missing_game_in_any_round(self):
        # A truncated panel used to be silently dropped from the tally (gmap was
        # filtered to only fully-covered games before writing results), which is
        # exactly the class of bug HANDOFF.md records nearly losing a bracket to.
        # This applies to every round, not only live-evidence ones like s16/e8 —
        # r32 has no ROUND_GAME_COUNTS entry and so gets no other completeness gate.
        gmap={1:{'A':'E1','B':'E2'},2:{'A':'E3','B':'E4'},3:{'A':'E5','B':'E6'}}
        complete={'Builder':{1:{},2:{},3:{}},'Skeptic':{1:{},2:{},3:{}},'Ecologist':{1:{},2:{},3:{}}}
        self.assertEqual({},tally.incomplete_panels(gmap,complete,list(complete)))
        truncated={'Builder':{1:{},2:{},3:{}},'Skeptic':{1:{},3:{}},'Ecologist':{1:{},2:{},3:{}}}
        self.assertEqual({'Skeptic':[2]},tally.incomplete_panels(gmap,truncated,list(truncated)))
        empty_panel={'Builder':{1:{},2:{},3:{}},'Skeptic':{},'Ecologist':{1:{},2:{},3:{}}}
        self.assertEqual({'Skeptic':[1,2,3]},tally.incomplete_panels(gmap,empty_panel,list(empty_panel)))


if __name__ == '__main__':
    unittest.main()
