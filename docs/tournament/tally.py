"""Parse one round's panel verdicts into its own tally artifact."""
import argparse, datetime, re, json, sys, os, glob, random, subprocess
SP=os.path.dirname(os.path.abspath(__file__))
REPO_ROOT=os.path.abspath(os.path.join(SP,"..",".."))
AXES=["Distance","Mechanism","Irreducibility","Compounding","Generative failure"]
LEGACY_PANELS=["Builder","Skeptic","Ecologist"]
ROUND_ANCHORS={
    "s16": {"name":"Builder", "file_tag":"builder",
            "lead":"nuclear-reactor-operator", "lens":"magician-illusionist"},
    "e8": {"name":"Ecologist", "file_tag":"ecologist",
           "lead":"systems-thinker", "lens":"farmer"},
}
ROUND_GAME_COUNTS={"s16":8,"e8":4}
S16_SURVIVOR_ORDER=('E3','M5','E2','A3','E5','E1','A5','A6',
                    'A1','C8','E4','M1','M3','A2','C5','E6')
S16_SURVIVORS=set(S16_SURVIVOR_ORDER)
YIELD_PLACEHOLDERS={
    'strongest_a':'Idea number and exact identifying phrase.',
    'return_a':'The causal path from that proposal to the brief.',
    'repeat_a':'First idea number where early moves begin repeating, or NONE with reason.',
    'strongest_b':'Idea number and exact identifying phrase.',
    'return_b':'The causal path from that proposal to the brief.',
    'repeat_b':'First idea number where early moves begin repeating, or NONE with reason.',
    'reason':'Compare ideas 17–24 for surprising usefulness, penalizing distance with no causal return path.',
}
AXIS_REFERENCE_PLACEHOLDER='Place both entrants against the fixed anchors in `reference-sets.md`.'
AXIS_PREDICATE_PLACEHOLDERS={
    'Distance':'Name a concrete output each mechanism makes unavailable.',
    'Mechanism':'Name the file, tool, context boundary or external actor that runs and enforces each mechanism; disclose manual substitutions.',
    'Irreducibility':'Estimate what an ordinary prompt could reproduce and identify the inaccessible state, operation or guarantee.',
    'Compounding':'State what use 10 can produce that use 1 cannot, using observed trace evidence where available.',
    'Generative failure':'Give an exact plausible failure output and say whether it diagnoses an assumption or merely creates noise.',
}
ENACTMENT_PLACEHOLDER='Cite the relevant traces and substitutions.'
SACRIFICE_PLACEHOLDERS={
    'honored':'One principle or bias from this panel\'s loaded profile.',
    'sacrificed':'A genuinely competing principle from the same profile.',
    'cost':'Specific risk or loss this vote accepts.',
    'validation':'Explain where the game made both commitments impossible to honor costlessly.',
}
COLLISION_PLACEHOLDERS={
    'candidate':'NONE / short name',
    'mechanism':'The third mechanism visible only because A and B collided.',
    'not_a':'Difference in mechanism, actor, failure mode or timescale.',
    'not_b':'Difference in mechanism, actor, failure mode or timescale.',
    'why':'What it might make newly reachable.',
}
# Leading sentence of the template's DECIDED BY instruction; an unedited overall
# ballot repeats it verbatim and must not decide the Pass 2 winner.
DECIDED_PLACEHOLDER='One sentence naming the decisive mechanism evidence.'
# The fixed Pass 1 isolation affirmation carried verbatim in every live verdict's
# panel declaration; a blank or reworded attestation is not a receipt.
ISOLATION_ATTESTATION=("I did not inspect another panel's verdict, prior-round verdicts, "
                       "mechanism identities during Pass 1, or the current tally.")

# points: significantly=3, slightly=1, tie=0
# The template permits exactly these five comparative verdict strings; anything
# else (negations, hedged prose, partial matches) is rejected rather than scored,
# so malformed text can never award points or decide an axis.
VERDICT_POINTS={
    'a significantly better':('A',3),'a slightly better':('A',1),
    'b significantly better':('B',3),'b slightly better':('B',1),
    'tie':(None,0),
}
def parse_verdict(s):
    key=' '.join(str(s).strip().lower().rstrip('.').split())
    if key not in VERDICT_POINTS:
        raise ValueError(f"unparseable verdict: {s!r}")
    return VERDICT_POINTS[key]

def parse_panel(text):
    """-> {matchup_no: {'winner':'A'/'B','decided':str,'axes':{axis:(side,pts,ref,pred)},'absorb':{...}}}"""
    out={}
    opened=re.search(r'^- \*\*Mechanism packet opened \(UTC\):\*\*[ \t]*(.+?)\s*$',
                     text,re.M)
    mechanism_opened=opened.group(1).strip() if opened else ''
    output=re.search(r'^- \*\*Output packet opened \(UTC\):\*\*[ \t]*(.+?)\s*$',
                     text,re.M)
    output_opened=output.group(1).strip() if output else ''
    chunks=re.split(r'^##\s+MATCHUP\s+(\d+)\s*$', text, flags=re.M)
    matchup_numbers=[int(chunks[i]) for i in range(1,len(chunks),2)]
    duplicates=sorted({n for n in matchup_numbers if matchup_numbers.count(n)>1})
    if duplicates:
        raise ValueError(f"duplicate matchup records in one verdict file: {duplicates}")
    for i in range(1,len(chunks),2):
        n=int(chunks[i]); body=chunks[i+1]
        rec={'axes':{},'absorb':{},'mechanism_opened':mechanism_opened,
             'output_opened':output_opened}
        w=re.search(r'^WINNER:[ \t]*(A|B)\b', body, re.M)
        rec['winner']=w.group(1) if w else None
        d=re.search(r'^DECIDED BY:[ \t]*(\S[^\n]*)', body, re.M)
        rec['decided']=d.group(1).strip() if d else ''
        pass1=re.search(r'^###\s+PASS 1.*OUTPUT-ONLY YIELD\s*$(.*?)(?=^###|^##|\Z)',
                        body, re.M|re.S)
        rec['yield_evidence']={}
        if pass1:
            p1=pass1.group(1)
            y=re.search(r'^YIELD VERDICT:[ \t]*(A|B|TIE)[ \t]*$', p1, re.M|re.I)
            if y: rec['yield']=None if y.group(1).upper()=='TIE' else y.group(1).upper()
            for key,label in [
                ('strongest_a','STRONGEST A'),('return_a','A RETURN PATH'),
                ('repeat_a','A REPETITION ONSET'),('strongest_b','STRONGEST B'),
                ('return_b','B RETURN PATH'),('repeat_b','B REPETITION ONSET'),
                ('reason','YIELD REASON'),('sealed','PASS 1 SEALED \\(UTC\\)')]:
                m=re.search(
                    rf'^{label}:[ \t]*(\S[^\n]*(?:\n(?![A-Z0-9][A-Z0-9 ()\-]+:)[^\n]*)*)',
                    p1,re.M)
                if m: rec['yield_evidence'][key]=' '.join(m.group(1).split())
        for ax in AXES:
            sec=re.search(rf'^###\s+{re.escape(ax)}\s*$(.*?)(?=^###|\Z)', body, re.M|re.S)
            if not sec: continue
            b=sec.group(1)
            v=re.search(r'^VERDICT:[ \t]*(\S[^\n]*)', b, re.M)
            ref=re.search(r'^REFERENCE:[ \t]*(\S[^\n]*(?:\n(?!\w+:)[^\n]*)*)', b, re.M)
            pr=re.search(r'^PREDICATE:[ \t]*(\S[^\n]*(?:\n(?!\w+:)[^\n]*)*)', b, re.M)
            if not v: continue
            try:
                side,pts=parse_verdict(v.group(1))
            except ValueError:
                # A non-canonical verdict is recorded as invalid (pts=None) and
                # flagged per-axis in validation, rather than aborting the whole
                # tally at parse time; it still scores nothing and blocks the round.
                side,pts=None,None
            rec['axes'][ax]={'side':side,'pts':pts,
                             'ref':' '.join(ref.group(1).split()) if ref else '',
                             'pred':' '.join(pr.group(1).split()) if pr else ''}
        a=re.search(r'^###\s+ABSORPTION\s*$(.*?)(?=^###|^##|\Z)', body, re.M|re.S)
        if a:
            ab=a.group(1)
            for k,lbl in [('mech','LOWER|LOSER.S STRONGEST MECHANISM'),('same','SAME-THESIS'),
                          ('del','DELETION'),('one','ONE-SENTENCE'),('disp','DISPOSITION'),('note','NOTE')]:
                m=re.search(rf'^(?:{lbl}):[ \t]*(\S[^\n]*(?:\n(?![A-Z][A-Z\- ]+:)[^\n]*)*)', ab, re.M)
                rec['absorb'][k]=' '.join(m.group(1).split()) if m else ''
        e=re.search(r'^###\s+FAITHFUL ENACTMENT\s*$(.*?)(?=^###|^##|\Z)', body, re.M|re.S)
        rec['enactment']={}
        rec['enactment_evidence']=''
        if e:
            for side in ('A','B'):
                m=re.search(rf'^{side} STATUS:[ \t]*(FAITHFUL|PARTIAL|NOT ENACTED|PROMISE ONLY)[ \t]*$', e.group(1), re.M|re.I)
                if m: rec['enactment'][side]=m.group(1).upper()
            evidence=re.search(r'^EVIDENCE:[ \t]*(\S[^\n]*)', e.group(1), re.M)
            if evidence: rec['enactment_evidence']=' '.join(evidence.group(1).split())
        for heading,key,labels in [
            ('SACRIFICE RECEIPT','sacrifice',
             [('honored','HONORED'),('sacrificed','SACRIFICED'),
              ('cost','ACCEPTED COST'),('validation','VALIDATION')]),
            ('COLLISION RESIDUE','collision',
             [('candidate','CANDIDATE'),('mechanism','MECHANISM'),('not_a','NOT IN A'),
              ('not_b','NOT IN B'),('why','WHY IT MATTERS')])]:
            sec=re.search(rf'^###\s+{heading}\s*$(.*?)(?=^###|^##|\Z)', body, re.M|re.S)
            rec[key]={}
            if sec:
                for short,label in labels:
                    m=re.search(rf'^{label}:[ \t]*(\S[^\n]*(?:\n(?![A-Z][A-Z ]+:)[^\n]*)*)', sec.group(1), re.M)
                    if m: rec[key][short]=' '.join(m.group(1).split())
        out[n]=rec
    return out

def majority(votes, count_ties=False):
    """Return A/B winner, or None for a tied result."""
    counts={side:votes.count(side) for side in ('A','B')}
    if count_ties:
        counts[None]=votes.count(None)
        high=max(counts.values())
        leaders=[side for side,count in counts.items() if count==high]
        return leaders[0] if len(leaders)==1 and leaders[0] in ('A','B') else None
    if counts['A'] == counts['B']: return None
    return 'A' if counts['A'] > counts['B'] else 'B'

def suffix_collisions(tags):
    """Return panel tags whose suffixes make the verdict glob ambiguous."""
    return sorted({tuple(sorted((a,b))) for a in tags for b in tags
                   if a != b and (a.endswith('-'+b) or b.endswith('-'+a))})

def specialist_errors(spec, repo_root=REPO_ROOT):
    """Validate live panel specialist slugs and claimed knowledge-pack status."""
    errors=[]
    for role in ('lead','lens'):
        slug=spec.get(role)
        if not isinstance(slug,str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):
            errors.append(role+'-slug')
            continue
        if not os.path.isfile(os.path.join(repo_root,'roster',slug+'.md')):
            errors.append(role+'-profile')
            continue
        actual='complete' if os.path.isfile(
            os.path.join(repo_root,'knowledge',slug,'positions.md')) else 'incomplete'
        if spec.get(role+'_pack') != actual:
            errors.append(role+'-pack-status')
    if spec.get('lead') == spec.get('lens'): errors.append('duplicate-specialist')
    return errors

def anchor_errors(round_id, specs):
    """Pin a live round's lone non-fresh panel to its prescribed anchor roster."""
    expected=ROUND_ANCHORS.get(round_id)
    if not expected:
        return []
    anchors=[spec for spec in specs if isinstance(spec,dict) and spec.get('fresh') is False]
    if len(anchors) != 1:
        return ['anchor-count']
    anchor=anchors[0]
    return [key for key,value in expected.items() if anchor.get(key) != value]

def fresh_pair_errors(specs):
    """Reject any fresh specialist pair reused elsewhere in the panel slate."""
    pairs=[]
    for spec in specs:
        if isinstance(spec,dict):
            pairs.append(tuple(sorted((spec.get('lead'),spec.get('lens')))))
    return ['duplicate-panel-pair'] if len(pairs) != len(set(pairs)) else []

def panel_declaration_errors(text,spec,draw):
    """Bind a verdict artifact to its draw-map panel, frozen draw, and two-pass receipts."""
    labels={
        'name':'Panel name','lead':'Lead specialist','lens':'Lens specialist',
        'draw':'Draw seed and draw-map commit',
    }
    declared={}
    for key,label in labels.items():
        match=re.search(rf'^- \*\*{re.escape(label)}:\*\*[ \t]*(.+?)\s*$',text,re.M)
        declared[key]=match.group(1).strip() if match else ''
    expected={'name':spec.get('name',''),'lead':spec.get('lead',''),
              'lens':spec.get('lens',''),
              'draw':f"{draw.get('seed','')} / {draw.get('_commit','')}"}
    errors=[key for key in labels if not declared[key] or declared[key] != expected[key]]
    # Provenance receipts: the isolation attestation and the two-pass packet order
    # must establish that Pass 1 saw only outputs before mechanism disclosure.
    def line(label):
        m=re.search(rf'^- \*\*{re.escape(label)}:\*\*[ \t]*(.+?)\s*$',text,re.M)
        return m.group(1).strip() if m else ''
    output_opened=line('Output packet opened (UTC)')
    mechanism_opened=line('Mechanism packet opened (UTC)')
    att=re.search(r'^- \*\*Isolation attestation:\*\*[ \t]*(\S.*?)(?=^- \*\*|^---|^#|\Z)',
                  text,re.M|re.S)
    attestation=' '.join(att.group(1).split()) if att else ''
    if attestation != ISOLATION_ATTESTATION:
        errors.append('isolation-attestation')
    if not utc_seal(output_opened):
        errors.append('output-packet-open')
    if not utc_seal(mechanism_opened):
        errors.append('mechanism-packet-open')
    if utc_seal(output_opened) and utc_seal(mechanism_opened) \
            and not utc_not_after(output_opened,mechanism_opened):
        errors.append('packet-chronology')
    return errors

def advancement_field(round_id,repo_root=REPO_ROOT):
    """Load the prior round's ratified advancers for a downstream draw.

    Elite 8 membership comes from a frozen, committed post-ruling advancement
    ledger, never from the raw Sweet 16 tally: the commissioner may overrule a
    tally winner, so the ratified advancer and the record's `winner` can differ.
    """
    if round_id != 'e8':
        return None
    path=os.path.join(repo_root,'docs','tournament','s16-advancers.json')
    if not committed_version(path,repo_root):
        return set()
    try:
        with open(path) as source:
            ledger=json.load(source)
    except (OSError,json.JSONDecodeError):
        return set()
    advancers=ledger.get('advancers') if isinstance(ledger,dict) else None
    if not isinstance(ledger,dict) or ledger.get('round') != 's16' \
            or ledger.get('ratified_by') != 'commissioner':
        return set()
    if not isinstance(advancers,list) or not all(isinstance(code,str) for code in advancers):
        return set()
    field=set(advancers)
    return field if len(advancers)==8 and len(field)==8 and field <= S16_SURVIVORS else set()

def reseed_errors(draw):
    """Replay the prescribed S16 shuffle and independent A/B assignment."""
    errors=[]
    if draw.get('algorithm') != 'python-random-v1': errors.append('reseed-algorithm')
    seed=draw.get('seed'); ab_seed=draw.get('ab_seed'); order=draw.get('input_order')
    if type(seed) is not int: errors.append('reseed-seed')
    if type(ab_seed) is not int or ab_seed == seed: errors.append('ab-seed')
    if order != list(S16_SURVIVOR_ORDER):
        errors.append('reseed-input-order')
    if errors: return errors
    shuffled=list(order); random.Random(seed).shuffle(shuffled)
    ab=random.Random(ab_seed)
    expected=[]
    for index in range(0,16,2):
        pair=shuffled[index:index+2]
        if ab.getrandbits(1): pair.reverse()
        expected.append(tuple(pair))
    actual=[(game.get('A'),game.get('B')) for game in draw.get('games',[])
            if isinstance(game,dict)]
    if actual != expected: errors.append('reseed-replay')
    return errors

def e8_return_errors(games,repo_root=REPO_ROOT):
    """Require each Elite 8 game to freeze all three Return Test artifacts."""
    errors=[]; used_artifacts=[]
    repo_real=os.path.realpath(repo_root)
    for game in games:
        if not isinstance(game,dict):
            continue
        game_id=game.get('g','?')
        receipt=game.get('return_test')
        if not isinstance(receipt,dict):
            errors.append(f'game-{game_id}-return-test')
            continue
        seed=receipt.get('contact_seed')
        direction=receipt.get('direction')
        if receipt.get('algorithm') != 'python-random-v1':
            errors.append(f'game-{game_id}-contact-algorithm')
        if type(seed) is not int:
            errors.append(f'game-{game_id}-contact-seed')
        elif direction != ('A→B' if random.Random(seed).getrandbits(1) else 'B→A'):
            errors.append(f'game-{game_id}-contact-direction')
        artifacts=receipt.get('artifacts')
        if not isinstance(artifacts,dict):
            errors.append(f'game-{game_id}-return-artifacts')
            continue
        for key in ('a_solo','b_solo','contact'):
            relpath=artifacts.get(key)
            if not isinstance(relpath,str) or not relpath.strip():
                errors.append(f'game-{game_id}-{key}-artifact')
                continue
            # Resolve `.`, `..`, and symlinks to a canonical identity so path
            # aliases cannot masquerade as three separate frozen artifacts, and a
            # symlink escaping the repository is rejected outright.
            resolved=os.path.realpath(os.path.join(repo_real,relpath))
            if os.path.commonpath((repo_real,resolved)) != repo_real \
                    or not os.path.isfile(resolved) \
                    or not committed_version(resolved,repo_real):
                errors.append(f'game-{game_id}-{key}-artifact')
                continue
            used_artifacts.append(resolved)
    if len(used_artifacts) != len(set(used_artifacts)):
        errors.append('duplicate-return-artifact')
    return errors

def committed_version(path,repo_root=REPO_ROOT):
    """Return the commit that froze a file, or empty when it is uncommitted or dirty.

    A file counts as frozen only when its working-tree and index contents still
    match the committed blob. An operator edit to a committed artifact (a changed
    seed, pairing, panel, or advancer) must not be accepted under the artifact's
    old commit SHA while verdicts keep declaring that SHA.
    """
    abspath=os.path.abspath(path)
    try:
        value=subprocess.check_output(
            ['git','log','-1','--format=%H','--',abspath],
            cwd=repo_root,text=True,stderr=subprocess.DEVNULL).strip()
        if not re.fullmatch(r'[0-9a-f]{40}',value):
            return ''
        status=subprocess.check_output(
            ['git','status','--porcelain','--',abspath],
            cwd=repo_root,text=True,stderr=subprocess.DEVNULL)
        return value if not status.strip() else ''
    except (OSError,subprocess.CalledProcessError):
        return ''

def absorption_test(value):
    """Return PASS/FAIL only for a completed test with an explanatory receipt."""
    if not isinstance(value,str):
        return None
    match=re.fullmatch(r'(PASS|FAIL)\s+(?:—|-)\s+(.+)', value.strip())
    if not match:
        return None
    explanation=match.group(2).strip()
    # Reject unresolved placeholder text: a bare word, or any bracketed [...] token
    # that is not a Markdown link ([label](url)). This still allows links and
    # ordinary prose, but a leftover placeholder such as [reason] or [TODO fill in],
    # anywhere in the explanation, does not clear the test.
    if explanation.lower() in {'reason','explanation','rationale'} \
            or re.search(r'\[[^\]]*\](?!\()', explanation):
        return None
    return match.group(1)

def utc_seal(value):
    """Accept the explicit second-resolution UTC timestamp required by Pass 1."""
    if not isinstance(value,str):
        return False
    try:
        datetime.datetime.strptime(value.strip(),'%Y-%m-%dT%H:%M:%SZ')
        return True
    except ValueError:
        return False

def utc_not_after(earlier,later):
    """True only when both are UTC receipts and earlier is no later than later."""
    try:
        first=datetime.datetime.strptime(str(earlier).strip(),'%Y-%m-%dT%H:%M:%SZ')
        second=datetime.datetime.strptime(str(later).strip(),'%Y-%m-%dT%H:%M:%SZ')
        return first <= second
    except ValueError:
        return False

def valid_pass1_chronology(output_opened,sealed,mechanism_opened):
    """Require output disclosure, sealing, and mechanism disclosure in order."""
    return utc_not_after(output_opened,sealed) and utc_not_after(sealed,mechanism_opened)

def draw_errors(games, round_id=None, expected_field=None):
    """Reject draw maps that would silently overwrite games or reuse entrants."""
    errors=[]; game_ids=[]; entrants=[]
    if not games: errors.append('missing-games')
    for index,game in enumerate(games):
        if not isinstance(game,dict):
            errors.append(f'game-{index}-record')
            continue
        game_id=game.get('g')
        if not isinstance(game_id,int) or isinstance(game_id,bool) or game_id < 1:
            errors.append(f'game-{index}-id')
        else: game_ids.append(game_id)
        for side in ('A','B'):
            code=game.get(side)
            if not isinstance(code,str) or not code.strip(): errors.append(f'game-{index}-{side}')
            else: entrants.append(code)
        if game.get('A') == game.get('B'): errors.append(f'game-{index}-self-match')
        if not isinstance(game.get('region'),str) or not game['region'].strip():
            errors.append(f'game-{index}-region')
    if len(game_ids) != len(set(game_ids)): errors.append('duplicate-game-id')
    if len(entrants) != len(set(entrants)): errors.append('duplicate-entrant')
    expected_count=ROUND_GAME_COUNTS.get(round_id)
    if expected_count is not None:
        expected_ids=set(range(1,expected_count+1))
        if len(games) != expected_count: errors.append(f'{round_id}-game-count')
        if set(game_ids) != expected_ids: errors.append(f'{round_id}-game-ids')
    if round_id == 's16' and set(entrants) != S16_SURVIVORS:
        errors.append('s16-survivor-field')
    if round_id == 'e8' and set(entrants) != (expected_field or set()):
        errors.append('e8-advancer-field')
    return errors

def validate_live_record(rec):
    """Return missing or invalid fields that must block a live-evidence tally."""
    missing=[]
    if rec.get('winner') not in ('A','B'): missing.append('winner')
    if not rec.get('decided'): missing.append('decided-by')
    elif rec.get('decided','').strip().startswith(DECIDED_PLACEHOLDER):
        missing.append('decided-placeholder')
    axes=rec.get('axes',{})
    if set(axes) != set(AXES):
        missing.append('five-axes')
    else:
        invalid=[ax for ax in AXES if not axes[ax].get('ref','').strip()
                 or not axes[ax].get('pred','').strip()]
        if invalid: missing.append('axis-evidence:' + '|'.join(invalid))
        bad_verdict=[ax for ax in AXES if axes[ax].get('pts') is None]
        if bad_verdict: missing.append('axis-verdict:'+'|'.join(bad_verdict))
        placeholders=[ax for ax in AXES
                      if axes[ax].get('ref','').strip() == AXIS_REFERENCE_PLACEHOLDER
                      or axes[ax].get('pred','').strip() == AXIS_PREDICATE_PLACEHOLDERS[ax]]
        if placeholders: missing.append('axis-placeholders:'+'|'.join(placeholders))
    absorb=rec.get('absorb',{})
    if absorb.get('disp') not in ('ABSORBED','ORTHOGONAL','SUBSUMED'):
        missing.append('absorption')
    absorb_required={'mech','same','del','one','disp','note'}
    absent_absorb=sorted(k for k in absorb_required if not str(absorb.get(k,'')).strip())
    if absent_absorb: missing.append('absorption-evidence:'+'|'.join(absent_absorb))
    tests=[absorption_test(absorb.get(k,'')) for k in ('same','del','one')]
    if any(v is None for v in tests): missing.append('absorption-tests')
    if absorb.get('disp') == 'ABSORBED' and tests != ['PASS','PASS','PASS']:
        missing.append('absorption-inconsistent')
    if absorb.get('disp') != 'ABSORBED' and tests == ['PASS','PASS','PASS']:
        missing.append('absorption-inconsistent')
    if 'yield' not in rec: missing.append('yield')
    yield_required={'strongest_a','return_a','repeat_a','strongest_b','return_b',
                    'repeat_b','reason','sealed'}
    absent=sorted(yield_required-rec.get('yield_evidence',{}).keys())
    if absent: missing.append('yield-evidence:'+'|'.join(absent))
    else:
        unresolved=sorted(k for k,v in YIELD_PLACEHOLDERS.items()
                          if rec['yield_evidence'].get(k,'').strip() == v)
        if unresolved: missing.append('yield-placeholders:'+'|'.join(unresolved))
        if not utc_seal(rec['yield_evidence']['sealed']): missing.append('yield-seal')
        if not valid_pass1_chronology(rec.get('output_opened',''),
                                     rec['yield_evidence']['sealed'],
                                     rec.get('mechanism_opened','')):
            missing.append('pass1-chronology')
    if not rec.get('enactment',{}).keys() >= {'A','B'}: missing.append('enactment')
    enactment_evidence=rec.get('enactment_evidence','').strip()
    if not enactment_evidence: missing.append('enactment-evidence')
    elif enactment_evidence == ENACTMENT_PLACEHOLDER: missing.append('enactment-placeholder')
    if not rec.get('sacrifice',{}).keys() >= {'honored','sacrificed','cost','validation'}:
        missing.append('sacrifice')
    if not rec.get('collision',{}).keys() >= {'candidate','mechanism','not_a','not_b','why'}:
        missing.append('collision')
    sacrifice=rec.get('sacrifice',{})
    unresolved_sacrifice=sorted(k for k,v in SACRIFICE_PLACEHOLDERS.items()
                                if sacrifice.get(k,'').strip() == v)
    if unresolved_sacrifice: missing.append('sacrifice-placeholders:'+'|'.join(unresolved_sacrifice))
    collision=rec.get('collision',{})
    unresolved_collision=sorted(k for k,v in COLLISION_PLACEHOLDERS.items()
                                if collision.get(k,'').strip() == v)
    if unresolved_collision: missing.append('collision-placeholders:'+'|'.join(unresolved_collision))
    if collision.get('candidate','').strip() == 'NONE':
        if any(collision.get(k,'').strip() != 'N/A' for k in ('mechanism','not_a','not_b','why')):
            missing.append('collision-none-form')
    elif any(collision.get(k,'').strip() in ('NONE','N/A') for k in ('candidate','mechanism','not_a','not_b','why')):
        missing.append('collision-none-form')
    return missing

def tally(panels, gmap, panel_names):
    """panels: {panel_name: parsed}. gmap: {n: {'A':code,'B':code,...}}"""
    res={}
    for n in sorted(gmap):
        g=gmap[n]; rows=[]; tot={'A':0,'B':0}; contested=False; splits=[]
        for ax in AXES:
            votes=[]
            for p in panel_names:
                r=panels.get(p,{}).get(n,{}).get('axes',{}).get(ax)
                votes.append((p, r['side'] if r else None, r['pts'] if r else 0, r))
            sides=[v[1] for v in votes]
            # opposite "significantly" -> contested
            hard={v[1] for v in votes if v[2]==3 and v[1]}
            if len(hard)>1: contested=True; splits.append(ax)
            named=[s for s in sides if s]
            if named and len(set(named))>1: splits.append(ax)
            # raw signed sum across panels: each panel casts 1 or 3, range -9..+9 per axis
            sa=sum(v[2] for v in votes if v[1]=='A'); sb=sum(v[2] for v in votes if v[1]=='B')
            side = 'A' if sa>sb else ('B' if sb>sa else None)
            pts = abs(sa-sb)
            tot['A']+=sa; tot['B']+=sb
            rows.append({'axis':ax,'votes':[(v[0],v[1],v[2]) for v in votes],
                         'side':side,'pts':pts,'raw':{'A':sa,'B':sb},
                         'unanimous':len(set(sides))==1,
                         'detail':[v[3] for v in votes]})
        panel_winners=[panels.get(p,{}).get(n,{}).get('winner') for p in panel_names]
        if len(set(x for x in panel_winners if x))>1: splits.append('OVERALL')
        wside='A' if tot['A']>tot['B'] else ('B' if tot['B']>tot['A'] else None)
        maj=majority(panel_winners)
        if wside and maj and wside!=maj: splits.append('AGGREGATE-VS-PANEL')
        panel_records=[panels.get(p,{}).get(n,{}) for p in panel_names]
        yield_votes=[rec.get('yield') for rec in panel_records]
        have_yield=any('yield' in rec for rec in panel_records)
        yield_winner=majority(yield_votes, count_ties=True) if have_yield else None
        if have_yield and yield_winner != wside: splits.append('YIELD-VS-AGGREGATE')
        if have_yield and yield_winner != maj: splits.append('YIELD-VS-PANEL')
        enactment={p:panels.get(p,{}).get(n,{}).get('enactment',{}) for p in panel_names}
        have_enactment=any(bool(v) for v in enactment.values())
        if have_enactment:
            for side in ('A','B'):
                statuses=[enactment[p].get(side) for p in panel_names]
                if any(s is None for s in statuses): splits.append('ENACTMENT-INCOMPLETE')
                if len(set(s for s in statuses if s))>1: splits.append('ENACTMENT-SPLIT')
                if any(s != 'FAITHFUL' for s in statuses if s): splits.append('ENACTMENT-LIMIT')
        game={'A':g['A'],'B':g['B'],'region':g['region'],'rows':rows,'tot':tot,
                'winner_side':wside,'winner':g[wside] if wside else None,
                'loser':g['B' if wside=='A' else 'A'] if wside else None,
                'margin':abs(tot['A']-tot['B']),
                'contested':contested or 'OVERALL' in splits or 'AGGREGATE-VS-PANEL' in splits
                            or any(s.startswith('YIELD-') for s in splits)
                            or 'ENACTMENT-INCOMPLETE' in splits or 'ENACTMENT-SPLIT' in splits
                            or tot['A']==tot['B'],
                'splits':sorted(set(splits)),'panel_winners':dict(zip(panel_names,panel_winners)),
                'decided':{p:panels.get(p,{}).get(n,{}).get('decided','') for p in panel_names},
                'absorb':{p:panels.get(p,{}).get(n,{}).get('absorb',{}) for p in panel_names}}
        if have_yield:
            game['yield']={'votes':dict(zip(panel_names,yield_votes)),
                           'winner_side':yield_winner,
                           'winner':g[yield_winner] if yield_winner else None,
                           'evidence':{p:panels[p][n].get('yield_evidence',{})
                                       for p in panel_names}}
        if have_enactment:
            game['enactment']=enactment
            game['enactment_evidence']={p:panels[p][n].get('enactment_evidence','')
                                         for p in panel_names}
        sacrifices={p:panels.get(p,{}).get(n,{}).get('sacrifice',{}) for p in panel_names}
        collisions={p:panels.get(p,{}).get(n,{}).get('collision',{}) for p in panel_names}
        if any(bool(v) for v in sacrifices.values()): game['sacrifice']=sacrifices
        if any(bool(v) for v in collisions.values()): game['collision']=collisions
        res[n]=game
    return res

if __name__=="__main__":
    parser = argparse.ArgumentParser(
        description="Tally a single tournament round without touching another round's evidence."
    )
    parser.add_argument("--round", required=True, dest="round_id",
                        help="Round file prefix, for example r32 or s16.")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.round_id):
        parser.error("--round must use lowercase letters, digits, and hyphens only")

    round_id = args.round_id
    draw_map = f"{SP}/{round_id}-draw-map.json"
    results_path = f"{SP}/{round_id}-results.json"
    draw=json.load(open(draw_map))
    draw['_commit']=committed_version(draw_map)
    games=draw.get('games',[])
    prior_field=advancement_field(round_id)
    invalid_draw=draw_errors(games,round_id,prior_field)
    if round_id == 's16': invalid_draw.extend(reseed_errors(draw))
    if round_id == 'e8': invalid_draw.extend(e8_return_errors(games))
    if invalid_draw: parser.error("invalid draw map: " + ", ".join(invalid_draw))
    gmap={g['g']:g for g in games}
    raw_panel_specs=draw.get('panels') or [
        {'name':p, 'file_tag':p.lower()} for p in LEGACY_PANELS
    ]
    if not isinstance(raw_panel_specs,list):
        parser.error("draw-map panels must be an array")
    live_evidence_required=round_id in ROUND_GAME_COUNTS
    if live_evidence_required and not draw['_commit']:
        parser.error(f"{round_id} draw map must be committed before tallying")
    if live_evidence_required and draw.get('require_live_evidence') is not True:
        parser.error(f"{round_id} requires live evidence")
    panel_specs=[]
    for spec in raw_panel_specs:
        if isinstance(spec, str):
            spec={'name':spec, 'file_tag':spec.lower()}
        if not isinstance(spec,dict):
            parser.error("each draw-map panel must be a record")
        name=spec.get('name','').strip()
        tag=spec.get('file_tag','').strip()
        if not name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', tag):
            parser.error("draw-map panels require a name and lowercase file_tag")
        if live_evidence_required:
            required=('lead','lens','lead_pack','lens_pack','fresh')
            if any(k not in spec for k in required):
                parser.error("live-evidence panel records require lead, lens, pack statuses, and fresh")
            if spec['lead_pack'] not in ('complete','incomplete') or spec['lens_pack'] not in ('complete','incomplete'):
                parser.error("panel pack status must be complete or incomplete")
            if not isinstance(spec['fresh'], bool):
                parser.error("panel fresh status must be true or false")
            if spec['fresh'] and spec['lead_pack']=='incomplete' and spec['lens_pack']=='incomplete':
                parser.error(f"fresh panel {name} violates the issue #21 pack guardrail")
            errors=specialist_errors(spec)
            if errors:
                parser.error(f"live panel {name} has invalid specialist configuration: {','.join(errors)}")
        panel_specs.append((name,tag,spec))
    if len(panel_specs) != 3 or len({p[0] for p in panel_specs}) != 3 or len({p[1] for p in panel_specs}) != 3:
        parser.error("draw-map panels must contain exactly three unique names and file_tags")
    if live_evidence_required and sum(bool(s.get('fresh')) for s in raw_panel_specs) != 2:
        parser.error("live-evidence rounds require one calibration anchor and two fresh panels")
    invalid_pairs=fresh_pair_errors(raw_panel_specs) if live_evidence_required else []
    if invalid_pairs:
        parser.error("live-evidence fresh panels must use distinct specialist pairs")
    invalid_anchor=anchor_errors(round_id,raw_panel_specs) if live_evidence_required else []
    if invalid_anchor:
        parser.error(f"{round_id} calibration anchor does not match the prescribed roster: " +
                     ", ".join(invalid_anchor))
    collisions=suffix_collisions([p[1] for p in panel_specs])
    if collisions:
        parser.error("panel file_tags have ambiguous suffixes: " +
                     ", ".join('/'.join(pair) for pair in collisions))
    panel_names=[p[0] for p in panel_specs]
    panels={}
    for p,tag,spec in panel_specs:
        fs=sorted(glob.glob(f"{SP}/verdicts/{round_id}-*-{tag}.md"))
        merged={}
        for f in fs:
            try:
                verdict_text=open(f).read()
                declaration_errors=panel_declaration_errors(verdict_text,spec,draw) if live_evidence_required else []
                if declaration_errors:
                    parser.error(f"{f}: panel declaration mismatch: {','.join(declaration_errors)}")
                parsed=parse_panel(verdict_text)
            except ValueError as exc:
                parser.error(f"{f}: {exc}")
            duplicates=sorted(set(merged)&set(parsed))
            if duplicates:
                parser.error(f"{p} has duplicate matchup records: {duplicates}")
            merged.update(parsed)
        panels[p]=merged
        print(f"{p}: parsed {len(merged)} matchups from {len(fs)} file(s)", file=sys.stderr)
    if live_evidence_required:
        incomplete=[]
        expected=set(gmap)
        for p in panel_names:
            extra=sorted(set(panels[p])-expected)
            if extra: parser.error(f"{p} has matchups absent from the draw map: {extra}")
        for n in sorted(gmap):
            for p in panel_names:
                rec=panels.get(p,{}).get(n,{})
                missing=validate_live_record(rec)
                if missing: incomplete.append(f"G{n}:{p}({','.join(missing)})")
        if incomplete:
            parser.error("live-evidence fields missing for " + ", ".join(incomplete))
    res=tally(panels, {k:v for k,v in gmap.items() if all(k in panels[p] for p in panel_names)}, panel_names)
    json.dump(res, open(results_path,"w"), indent=1)
    for n in sorted(res):
        r=res[n]
        flag=" ** CONTESTED **" if r['contested'] else ""
        dis=[r['absorb'][p].get('disp','?') for p in panel_names]
        w = r['winner'] or 'TIE'; l = r['loser'] or f"{r['A']}/{r['B']}"
        rel = 'over' if r['winner'] else ' -- '
        print(f"G{n:2} [{r['region']:5}] {w:>3} {rel} {l:<7} "
              f"{r['tot']['A']:2}-{r['tot']['B']:<2} (margin {r['margin']:2}) "
              f"panels={list(r['panel_winners'].values())} disp={dis}{flag}")
