"""Parse panel verdicts -> per-axis tally, margins, CONTESTED flags, dispositions."""
import re, json, sys, os, glob
SP=os.path.dirname(os.path.abspath(__file__))
AXES=["Distance","Mechanism","Irreducibility","Compounding","Generative failure"]
PANELS=["Builder","Skeptic","Ecologist"]

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
        a=re.search(r'^###\s+ABSORPTION\s*$(.*?)(?=^##|\Z)', body, re.M|re.S)
        if a:
            ab=a.group(1)
            for k,lbl in [('mech','LOWER|LOSER.S STRONGEST MECHANISM'),('same','SAME-THESIS'),
                          ('del','DELETION'),('one','ONE-SENTENCE'),('disp','DISPOSITION'),('note','NOTE')]:
                m=re.search(rf'^(?:{lbl}):\s*(.+?)(?=^[A-Z][A-Z\- ]+:|\Z)', ab, re.M|re.S)
                rec['absorb'][k]=' '.join(m.group(1).split()) if m else ''
        out[n]=rec
    return out

def tally(panels, gmap):
    """panels: {panel_name: parsed}. gmap: {n: {'A':code,'B':code,...}}"""
    res={}
    for n in sorted(gmap):
        g=gmap[n]; rows=[]; tot={'A':0,'B':0}; contested=False; splits=[]
        for ax in AXES:
            votes=[]
            for p in PANELS:
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
        panel_winners=[panels.get(p,{}).get(n,{}).get('winner') for p in PANELS]
        if len(set(x for x in panel_winners if x))>1: splits.append('OVERALL')
        wside='A' if tot['A']>tot['B'] else ('B' if tot['B']>tot['A'] else None)
        maj=max(set(panel_winners), key=panel_winners.count) if panel_winners else None
        if wside and maj and wside!=maj: splits.append('AGGREGATE-VS-PANEL')
        res[n]={'A':g['A'],'B':g['B'],'region':g['region'],'rows':rows,'tot':tot,
                'winner_side':wside,'winner':g[wside] if wside else None,
                'loser':g['B' if wside=='A' else 'A'] if wside else None,
                'margin':abs(tot['A']-tot['B']),'contested':contested or 'OVERALL' in splits or 'AGGREGATE-VS-PANEL' in splits or tot['A']==tot['B'],
                'splits':sorted(set(splits)),'panel_winners':dict(zip(PANELS,panel_winners)),
                'decided':{p:panels.get(p,{}).get(n,{}).get('decided','') for p in PANELS},
                'absorb':{p:panels.get(p,{}).get(n,{}).get('absorb',{}) for p in PANELS}}
    return res

if __name__=="__main__":
    gmap={g['g']:g for g in json.load(open(f"{SP}/r32-draw-map.json"))['games']}
    panels={}
    for p in PANELS:
        fs=sorted(glob.glob(f"{SP}/verdicts/r32-*-{p.lower()}.md"))
        merged={}
        for f in fs: merged.update(parse_panel(open(f).read()))
        panels[p]=merged
        print(f"{p}: parsed {len(merged)} matchups from {len(fs)} file(s)", file=sys.stderr)
    res=tally(panels, {k:v for k,v in gmap.items() if all(k in panels[p] for p in PANELS)})
    json.dump(res, open(f"{SP}/r32-results.json","w"), indent=1)
    for n in sorted(res):
        r=res[n]
        flag=" ** CONTESTED **" if r['contested'] else ""
        dis=[r['absorb'][p].get('disp','?') for p in PANELS]
        w = r['winner'] or 'TIE'; l = r['loser'] or f"{r['A']}/{r['B']}"
        rel = 'over' if r['winner'] else ' -- '
        print(f"G{n:2} [{r['region']:5}] {w:>3} {rel} {l:<7} "
              f"{r['tot']['A']:2}-{r['tot']['B']:<2} (margin {r['margin']:2}) "
              f"panels={list(r['panel_winners'].values())} disp={dis}{flag}")
