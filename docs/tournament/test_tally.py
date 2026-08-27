"""Focused regression tests for round-specific tournament tally behavior."""
import copy
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
        'axes':{a:{'side':side,'pts':1,'ref':'fixed anchor','pred':'falsifiable output'}
                for a in tally.AXES},
        'absorb':{'mech':'loser mechanism','same':'FAIL — distinct thesis',
                  'del':'FAIL — merely smaller','one':'FAIL — requires and also',
                  'disp':'ORTHOGONAL','note':'kept separate'},
        'enactment':{'A':'PROMISE ONLY','B':'FAITHFUL'},
        'enactment_evidence':'execution traces',
        'sacrifice':{'honored':'x','sacrificed':'y','cost':'z','validation':'conflict'},
        'collision':{'candidate':'NONE','mechanism':'N/A','not_a':'N/A',
                     'not_b':'N/A','why':'none'},
    }


class TallyTests(unittest.TestCase):
    def test_parser_captures_yield_and_enactment_evidence(self):
        text='''## MATCHUP 1
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
        self.assertEqual('traces/a.md and traces/b.md',rec['enactment_evidence'])

    def test_parser_rejects_duplicate_matchups_within_one_file(self):
        text='''## MATCHUP 1
WINNER: A
## MATCHUP 1
WINNER: B
'''
        with self.assertRaisesRegex(ValueError,'duplicate matchup records'):
            tally.parse_panel(text)

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

    def test_draw_rejects_reused_games_and_entrants(self):
        games=[{'g':1,'A':'E1','B':'E2','region':'One'},
               {'g':1,'A':'E2','B':'E3','region':'Two'}]
        errors=tally.draw_errors(games)
        self.assertIn('duplicate-game-id',errors)
        self.assertIn('duplicate-entrant',errors)
        self.assertIn('missing-games',tally.draw_errors([]))


if __name__ == '__main__':
    unittest.main()
