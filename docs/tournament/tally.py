"""Parse one round's panel verdicts into its own tally artifact."""
import argparse, datetime, re, json, sys, os, glob
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

# points: significantly=3, slightly=1, tie=0
def parse_verdict(s):
    s=s.strip().lower().rstrip('.')
    m=re.match(r'^(a|b)\s+(significantly|slightly)\s+better', s)
    if m: return (m.group(1).upper(), 3 if m.group(2)=="significantly" else 1)
    if s.startswith('tie') or 'tie' == s: return (None, 0)
    m=re.search(r'\b(a|b)\b.*\b(significantly|slightly)\b', s)
    if m: return (m.group(1).upper(), 3 if m.group(2)=="significantly" else 1)
    if 'tie' in s: return (None, 0)
    raise ValueError(f"unparseable verdict: {s!r}")

def parse_panel(text):
    """-> {matchup_no: {'winner':'A'/'B','decided':str,'axes':{axis:(side,pts,ref,pred)},'absorb':{...}}}"""
    out={}
    chunks=re.split(r'^##\s+MATCHUP\s+(\d+)\s*$', text, flags=re.M)
    matchup_numbers=[int(chunks[i]) for i in range(1,len(chunks),2)]
    duplicates=sorted({n for n in matchup_numbers if matchup_numbers.count(n)>1})
    if duplicates:
        raise ValueError(f"duplicate matchup records in one verdict file: {duplicates}")
    for i in range(1,len(chunks),2):
        n=int(chunks[i]); body=chunks[i+1]
        rec={'axes':{},'absorb':{}}
        w=re.search(r'^WINNER:\s*(A|B)', body, re.M)
        rec['winner']=w.group(1) if w else None
        d=re.search(r'^DECIDED BY:\s*(.+)$', body, re.M)
        rec['decided']=d.group(1).strip() if d else ''
        pass1=re.search(r'^###\s+PASS 1.*OUTPUT-ONLY YIELD\s*$(.*?)(?=^###|^##|\Z)',
                        body, re.M|re.S)
        rec['yield_evidence']={}
        if pass1:
            p1=pass1.group(1)
            y=re.search(r'^YIELD VERDICT:\s*(A|B|TIE)\s*$', p1, re.M|re.I)
            if y: rec['yield']=None if y.group(1).upper()=='TIE' else y.group(1).upper()
            for key,label in [
                ('strongest_a','STRONGEST A'),('return_a','A RETURN PATH'),
                ('repeat_a','A REPETITION ONSET'),('strongest_b','STRONGEST B'),
                ('return_b','B RETURN PATH'),('repeat_b','B REPETITION ONSET'),
                ('reason','YIELD REASON'),('sealed','PASS 1 SEALED \\(UTC\\)')]:
                m=re.search(rf'^{label}:\s*(.+?)(?=^[A-Z0-9][A-Z0-9 ()\-]+:|\Z)',
                            p1, re.M|re.S)
                if m: rec['yield_evidence'][key]=' '.join(m.group(1).split())
        for ax in AXES:
            sec=re.search(rf'^###\s+{re.escape(ax)}\s*$(.*?)(?=^###|\Z)', body, re.M|re.S)
            if not sec: continue
            b=sec.group(1)
            v=re.search(r'^VERDICT:\s*(.+)$', b, re.M)
            ref=re.search(r'^REFERENCE:\s*(.+?)(?=^\w+:|\Z)', b, re.M|re.S)
            pr=re.search(r'^PREDICATE:\s*(.+?)(?=^\w+:|\Z)', b, re.M|re.S)
            if not v: continue
            side,pts=parse_verdict(v.group(1))
            rec['axes'][ax]={'side':side,'pts':pts,
                             'ref':' '.join(ref.group(1).split()) if ref else '',
                             'pred':' '.join(pr.group(1).split()) if pr else ''}
        a=re.search(r'^###\s+ABSORPTION\s*$(.*?)(?=^###|^##|\Z)', body, re.M|re.S)
        if a:
            ab=a.group(1)
            for k,lbl in [('mech','LOWER|LOSER.S STRONGEST MECHANISM'),('same','SAME-THESIS'),
                          ('del','DELETION'),('one','ONE-SENTENCE'),('disp','DISPOSITION'),('note','NOTE')]:
                m=re.search(rf'^(?:{lbl}):\s*(.+?)(?=^[A-Z][A-Z\- ]+:|\Z)', ab, re.M|re.S)
                rec['absorb'][k]=' '.join(m.group(1).split()) if m else ''
        e=re.search(r'^###\s+FAITHFUL ENACTMENT\s*$(.*?)(?=^###|^##|\Z)', body, re.M|re.S)
        rec['enactment']={}
        rec['enactment_evidence']=''
        if e:
            for side in ('A','B'):
                m=re.search(rf'^{side} STATUS:\s*(FAITHFUL|PARTIAL|NOT ENACTED|PROMISE ONLY)\s*$', e.group(1), re.M|re.I)
                if m: rec['enactment'][side]=m.group(1).upper()
            evidence=re.search(r'^EVIDENCE:\s*(.+?)\s*$', e.group(1), re.M|re.S)
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
                    m=re.search(rf'^{label}:\s*(.+?)(?=^[A-Z][A-Z ]+:|\Z)', sec.group(1), re.M|re.S)
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

def absorption_test(value):
    """Return PASS/FAIL only for a completed test with an explanatory receipt."""
    if not isinstance(value,str):
        return None
    match=re.fullmatch(r'(PASS|FAIL)\s+(?:—|-)\s+(.+)', value.strip())
    if not match:
        return None
    explanation=match.group(2).strip()
    if explanation.lower() in {'reason','explanation','rationale'} or '[' in explanation:
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

def draw_errors(games):
    """Reject draw maps that would silently overwrite games or reuse entrants."""
    errors=[]; game_ids=[]; entrants=[]
    if not games: errors.append('missing-games')
    for index,game in enumerate(games):
        if not isinstance(game,dict):
            errors.append(f'game-{index}-record')
            continue
        game_id=game.get('g')
        if not isinstance(game_id,int) or game_id < 1: errors.append(f'game-{index}-id')
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
    return errors

def validate_live_record(rec):
    """Return missing or invalid fields that must block a live-evidence tally."""
    missing=[]
    if rec.get('winner') not in ('A','B'): missing.append('winner')
    if not rec.get('decided'): missing.append('decided-by')
    axes=rec.get('axes',{})
    if set(axes) != set(AXES):
        missing.append('five-axes')
    else:
        invalid=[ax for ax in AXES if not axes[ax].get('ref','').strip()
                 or not axes[ax].get('pred','').strip()]
        if invalid: missing.append('axis-evidence:' + '|'.join(invalid))
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
    if absorb.get('disp') == 'ORTHOGONAL' and tests == ['PASS','PASS','PASS']:
        missing.append('absorption-inconsistent')
    if 'yield' not in rec: missing.append('yield')
    yield_required={'strongest_a','return_a','repeat_a','strongest_b','return_b',
                    'repeat_b','reason','sealed'}
    absent=sorted(yield_required-rec.get('yield_evidence',{}).keys())
    if absent: missing.append('yield-evidence:'+'|'.join(absent))
    elif not utc_seal(rec['yield_evidence']['sealed']): missing.append('yield-seal')
    if not rec.get('enactment',{}).keys() >= {'A','B'}: missing.append('enactment')
    if not rec.get('enactment_evidence','').strip(): missing.append('enactment-evidence')
    if not rec.get('sacrifice',{}).keys() >= {'honored','sacrificed','cost','validation'}:
        missing.append('sacrifice')
    if not rec.get('collision',{}).keys() >= {'candidate','mechanism','not_a','not_b','why'}:
        missing.append('collision')
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
    games=draw.get('games',[])
    invalid_draw=draw_errors(games)
    if invalid_draw: parser.error("invalid draw map: " + ", ".join(invalid_draw))
    gmap={g['g']:g for g in games}
    raw_panel_specs=draw.get('panels') or [
        {'name':p, 'file_tag':p.lower()} for p in LEGACY_PANELS
    ]
    if not isinstance(raw_panel_specs,list):
        parser.error("draw-map panels must be an array")
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
        if draw.get('require_live_evidence'):
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
        panel_specs.append((name,tag))
    if len(panel_specs) != 3 or len({p[0] for p in panel_specs}) != 3 or len({p[1] for p in panel_specs}) != 3:
        parser.error("draw-map panels must contain exactly three unique names and file_tags")
    if draw.get('require_live_evidence') and sum(bool(s.get('fresh')) for s in raw_panel_specs) != 2:
        parser.error("live-evidence rounds require one calibration anchor and two fresh panels")
    invalid_anchor=anchor_errors(round_id,raw_panel_specs) if draw.get('require_live_evidence') else []
    if invalid_anchor:
        parser.error(f"{round_id} calibration anchor does not match the prescribed roster: " +
                     ", ".join(invalid_anchor))
    collisions=suffix_collisions([p[1] for p in panel_specs])
    if collisions:
        parser.error("panel file_tags have ambiguous suffixes: " +
                     ", ".join('/'.join(pair) for pair in collisions))
    panel_names=[p[0] for p in panel_specs]
    panels={}
    for p,tag in panel_specs:
        fs=sorted(glob.glob(f"{SP}/verdicts/{round_id}-*-{tag}.md"))
        merged={}
        for f in fs:
            try:
                parsed=parse_panel(open(f).read())
            except ValueError as exc:
                parser.error(f"{f}: {exc}")
            duplicates=sorted(set(merged)&set(parsed))
            if duplicates:
                parser.error(f"{p} has duplicate matchup records: {duplicates}")
            merged.update(parsed)
        panels[p]=merged
        print(f"{p}: parsed {len(merged)} matchups from {len(fs)} file(s)", file=sys.stderr)
    if draw.get('require_live_evidence'):
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
