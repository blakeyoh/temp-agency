"""Parse one round's panel verdicts into its own tally artifact."""
import argparse, re, json, sys, os, glob
SP=os.path.dirname(os.path.abspath(__file__))
AXES=["Distance","Mechanism","Irreducibility","Compounding","Generative failure"]
LEGACY_PANELS=["Builder","Skeptic","Ecologist"]

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
    for i in range(1,len(chunks),2):
        n=int(chunks[i]); body=chunks[i+1]
        rec={'axes':{},'absorb':{}}
        w=re.search(r'^WINNER:\s*(A|B)', body, re.M)
        rec['winner']=w.group(1) if w else None
        d=re.search(r'^DECIDED BY:\s*(.+)$', body, re.M)
        rec['decided']=d.group(1).strip() if d else ''
        y=re.search(r'^YIELD VERDICT:\s*(A|B|TIE)\s*$', body, re.M|re.I)
        if y: rec['yield']=None if y.group(1).upper()=='TIE' else y.group(1).upper()
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
        if e:
            for side in ('A','B'):
                m=re.search(rf'^{side} STATUS:\s*(FAITHFUL|PARTIAL|NOT ENACTED|PROMISE ONLY)\s*$', e.group(1), re.M|re.I)
                if m: rec['enactment'][side]=m.group(1).upper()
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

def majority(votes):
    counts={side:votes.count(side) for side in ('A','B')}
    if counts['A'] == counts['B']: return None
    return 'A' if counts['A'] > counts['B'] else 'B'

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
        yield_winner=majority(yield_votes) if have_yield else None
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
                            or any(s.startswith(('YIELD-', 'ENACTMENT-')) for s in splits)
                            or tot['A']==tot['B'],
                'splits':sorted(set(splits)),'panel_winners':dict(zip(panel_names,panel_winners)),
                'decided':{p:panels.get(p,{}).get(n,{}).get('decided','') for p in panel_names},
                'absorb':{p:panels.get(p,{}).get(n,{}).get('absorb',{}) for p in panel_names}}
        if have_yield:
            game['yield']={'votes':dict(zip(panel_names,yield_votes)),
                           'winner_side':yield_winner,
                           'winner':g[yield_winner] if yield_winner else None}
        if have_enactment: game['enactment']=enactment
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
    gmap={g['g']:g for g in draw['games']}
    raw_panel_specs=draw.get('panels') or [
        {'name':p, 'file_tag':p.lower()} for p in LEGACY_PANELS
    ]
    panel_specs=[]
    for spec in raw_panel_specs:
        if isinstance(spec, str):
            spec={'name':spec, 'file_tag':spec.lower()}
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
        panel_specs.append((name,tag))
    if len(panel_specs) != 3 or len({p[0] for p in panel_specs}) != 3 or len({p[1] for p in panel_specs}) != 3:
        parser.error("draw-map panels must contain exactly three unique names and file_tags")
    if draw.get('require_live_evidence') and sum(bool(s.get('fresh')) for s in raw_panel_specs) != 2:
        parser.error("live-evidence rounds require one calibration anchor and two fresh panels")
    panel_names=[p[0] for p in panel_specs]
    panels={}
    for p,tag in panel_specs:
        fs=sorted(glob.glob(f"{SP}/verdicts/{round_id}-*-{tag}.md"))
        merged={}
        for f in fs: merged.update(parse_panel(open(f).read()))
        panels[p]=merged
        print(f"{p}: parsed {len(merged)} matchups from {len(fs)} file(s)", file=sys.stderr)
    if draw.get('require_live_evidence'):
        incomplete=[]
        for n in sorted(gmap):
            for p in panel_names:
                rec=panels.get(p,{}).get(n,{})
                missing=[]
                if rec.get('winner') not in ('A','B'): missing.append('winner')
                if not rec.get('decided'): missing.append('decided-by')
                if set(rec.get('axes',{})) != set(AXES): missing.append('five-axes')
                if rec.get('absorb',{}).get('disp') not in ('ABSORBED','ORTHOGONAL','SUBSUMED','REFUSED'):
                    missing.append('absorption')
                if 'yield' not in rec: missing.append('yield')
                if not rec.get('enactment',{}).keys() >= {'A','B'}: missing.append('enactment')
                if not rec.get('sacrifice',{}).keys() >= {'honored','sacrificed','cost','validation'}:
                    missing.append('sacrifice')
                if not rec.get('collision',{}).keys() >= {'candidate','mechanism','not_a','not_b','why'}:
                    missing.append('collision')
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
