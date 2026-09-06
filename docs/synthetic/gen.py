import json, html
D = json.load(open('data.json'))
Q = json.load(open('questions.json'))

CHECK = ['DS1','DC1','AS3','AC1','XT1','TX1']
FULL  = ['DS2','DS3','DS4','DC2','DC3','DC4','AS1','AS2','AS4','AC2','AC3','AC4',
         'DT1','DT2','AT1','AT2','TS1','TS2','TC1','TC2']
DIRECTION = ['DS1','DS2','DS3','DS4','DC1','DC2','DC3','DC4']
AGILITY   = ['AS1','AS2','AS3','AS4','AC1','AC2','AC3','AC4']
TRADEOFF  = ['XT1','TX1','DT1','DT2','AT1','AT2','TS1','TS2','TC1','TC2']
e = html.escape

def short(n):
    p = n.split()
    return p[-1]

def mean(p, codes):
    return sum(p['rows'][c]['score'] for c in codes)/len(codes)

# ---------- matrix ----------
def cell(code, sc):
    kind = 'sp' if code in TRADEOFF else 'lad'
    return f'<td class="cel {kind} v{sc}"><span>{sc}</span></td>'

def matrix_block(title, note, codes):
    rows = []
    for c in codes:
        q = Q[c]
        cells = ''.join(cell(c, p['rows'][c]['score']) for p in D)
        inst = 'Check + Full' if c in CHECK else 'Full only'
        rows.append(
            f'<tr><th scope="row" class="qh"><span class="qc">{c}</span>'
            f'<span class="qp">{e(q["prompt"])}</span>'
            f'<span class="qi">{inst}</span></th>{cells}</tr>')
    heads = ''.join(f'<th scope="col"><span>{e(short(p["name"]))}</span></th>' for p in D)
    return f'''<section class="mblock">
<h3 class="mbt">{title}</h3><p class="mbn">{note}</p>
<div class="scroller"><table class="matrix">
<thead><tr><th class="corner" scope="col">Question</th>{heads}</tr></thead>
<tbody>{''.join(rows)}</tbody></table></div></section>'''

# ---------- roster ----------
roster = ''.join(f'''<a class="rcard" href="#p{i+1}">
<span class="rnum">{i+1:02d}</span>
<span class="rname">{e(p['name'])}</span>
<span class="rtitle">{e(p['title'])}</span>
<span class="rpersona">{e(p['persona'])}</span>
<span class="rmeans"><span class="mn dir"><b>{mean(p,DIRECTION):.2f}</b> Direction</span><span class="mn agi"><b>{mean(p,AGILITY):.2f}</b> Agility</span></span>
</a>''' for i, p in enumerate(D))

# ---------- dossiers ----------
def ans_table(p, codes, cap):
    rows = ''
    for c in codes:
        q = Q[c]; r = p['rows'][c]
        tag = 'sp' if c in TRADEOFF else 'lad'
        rows += (f'<tr><td class="c-code">{c}</td>'
                 f'<td class="c-score"><span class="pill {tag} v{r["score"]}">{r["score"]}</span></td>'
                 f'<td class="c-q">{e(q["prompt"])}</td>'
                 f'<td class="c-opt">{e(r["opt"])}</td>'
                 f'<td class="c-why">{e(r["why"])}</td></tr>')
    return f'''<div class="tblwrap"><table class="ans">
<caption>{cap}</caption>
<thead><tr><th>Code</th><th>Score</th><th>Question</th><th>Option chosen</th><th>Reasoning</th></tr></thead>
<tbody>{rows}</tbody></table></div>'''

dossiers = ''
for i, p in enumerate(D):
    dossiers += f'''<article class="dossier" id="p{i+1}">
<header class="dhead">
  <span class="dnum">{i+1:02d}</span>
  <div class="dwho"><h3>{e(p['name'])}</h3><p class="drole">{e(p['title'])}</p></div>
  <div class="dpersona"><span class="plabel">Temp Agency lens</span><span class="pname">{e(p['persona'])}</span></div>
  <div class="dscores">
    <span class="ds dir"><b>{mean(p,DIRECTION):.2f}</b><i>Direction focus</i></span>
    <span class="ds agi"><b>{mean(p,AGILITY):.2f}</b><i>Agility focus</i></span>
  </div>
</header>
<div class="dnotes">
  <p><span class="nl">Why this persona</span>{e(p['fit'])}</p>
  <p><span class="nl">Answering posture</span>{e(p['posture'])}</p>
</div>
{ans_table(p, CHECK, 'Future Ready Check &mdash; 6 questions')}
{ans_table(p, FULL, 'Future Ready Full &mdash; 20 additional questions')}
</article>'''

# ---------- spread stats ----------
allsc = [p['rows'][c]['score'] for p in D for c in CHECK+FULL]
dist = {s: allsc.count(s) for s in range(5)}
distbar = ''.join(f'<span class="db v{s}" style="flex:{dist[s]}"><i>{s}</i><b>{dist[s]}</b></span>' for s in range(5))

lowest = sorted(D, key=lambda p: (mean(p,DIRECTION)+mean(p,AGILITY))/2)[0]
highest = sorted(D, key=lambda p: (mean(p,DIRECTION)+mean(p,AGILITY))/2)[-1]

HTML = f'''<title>Community Harvest Synthetic Panel</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;800&family=IBM+Plex+Mono:wght@400;500;600&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&display=swap">
<style>
:root {{
  --ground:#edf0ee; --panel:#ffffff; --panel2:#f6f8f7; --ink:#141d1b; --ink2:#3d4a47;
  --muted:#6c7a76; --line:#d5dcd9; --line2:#c2ccc8;
  --dir:#a9670f; --dir-soft:#f2e3cd; --agi:#1c6670; --agi-soft:#d7e7e8;
  --v0:#f0efe9; --v1:#e2ddcb; --v2:#cbc39f; --v3:#b09a5c; --v4:#8a6f22;
  --v0t:#3d4a47; --v1t:#3d4a47; --v2t:#2b2716; --v3t:#ffffff; --v4t:#ffffff;
  --s0:#cfe0e2; --s1:#e0e9e6; --s2:#eceee9; --s3:#f0e2c9; --s4:#e5c58c;
  --s0t:#123c42; --s1t:#1d3a37; --s2t:#3d4a47; --s3t:#4d3a10; --s4t:#4d3a10;
  --shadow:0 1px 2px rgba(20,29,27,.06), 0 8px 24px -16px rgba(20,29,27,.35);
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --ground:#101614; --panel:#18201e; --panel2:#1d2624; --ink:#e8eeeb; --ink2:#b6c2be;
    --muted:#8b9995; --line:#2b3532; --line2:#3a4642;
    --dir:#dda447; --dir-soft:#3a2d15; --agi:#63b7c1; --agi-soft:#13322f;
    --v0:#1e2523; --v1:#2f3428; --v2:#4a4a2c; --v3:#6f6132; --v4:#a3873a;
    --v0t:#9aa8a4; --v1t:#c4c8b4; --v2t:#e6e4cd; --v3t:#fdf6e6; --v4t:#1a1405;
    --s0:#153f45; --s1:#1b2f30; --s2:#242d2b; --s3:#3d3117; --s4:#6a5320;
    --s0t:#bfe6ea; --s1t:#c2d4d1; --s2t:#b6c2be; --s3t:#f0dcb4; --s4t:#f7e3bb;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 30px -18px rgba(0,0,0,.9);
  }}
}}
:root[data-theme="dark"] {{
  --ground:#101614; --panel:#18201e; --panel2:#1d2624; --ink:#e8eeeb; --ink2:#b6c2be;
  --muted:#8b9995; --line:#2b3532; --line2:#3a4642;
  --dir:#dda447; --dir-soft:#3a2d15; --agi:#63b7c1; --agi-soft:#13322f;
  --v0:#1e2523; --v1:#2f3428; --v2:#4a4a2c; --v3:#6f6132; --v4:#a3873a;
  --v0t:#9aa8a4; --v1t:#c4c8b4; --v2t:#e6e4cd; --v3t:#fdf6e6; --v4t:#1a1405;
  --s0:#153f45; --s1:#1b2f30; --s2:#242d2b; --s3:#3d3117; --s4:#6a5320;
  --s0t:#bfe6ea; --s1t:#c2d4d1; --s2t:#b6c2be; --s3t:#f0dcb4; --s4t:#f7e3bb;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 30px -18px rgba(0,0,0,.9);
}}
* {{ box-sizing:border-box; }}
body {{ background:var(--ground); color:var(--ink);
  font-family:"Newsreader",Georgia,"Times New Roman",serif; font-size:16px; line-height:1.55; }}
.wrap {{ max-width:1180px; margin:0 auto; padding:0 24px 96px; }}
h1,h2,h3,h4,.ui {{ font-family:"Archivo","Helvetica Neue",Arial,sans-serif; text-wrap:balance; }}
.mono {{ font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace; }}

/* header */
.top {{ border-bottom:2px solid var(--ink); margin-bottom:40px; padding:44px 0 26px; }}
.eyebrow {{ font-family:"IBM Plex Mono",monospace; font-size:11px; letter-spacing:.16em;
  text-transform:uppercase; color:var(--muted); margin:0 0 14px; }}
h1 {{ font-size:clamp(30px,4.6vw,52px); font-weight:800; letter-spacing:-.02em; line-height:1.04; margin:0 0 14px; }}
.lede {{ font-size:19px; color:var(--ink2); max-width:62ch; margin:0 0 22px; }}
.facts {{ display:flex; flex-wrap:wrap; gap:8px 28px; font-family:"IBM Plex Mono",monospace;
  font-size:12px; color:var(--muted); }}
.facts b {{ color:var(--ink); font-weight:600; }}
.warn {{ margin-top:24px; border-left:3px solid var(--dir); background:var(--dir-soft);
  padding:12px 16px; font-size:14.5px; color:var(--ink2); border-radius:0 3px 3px 0; }}
.warn b {{ color:var(--ink); }}

h2 {{ font-size:13px; font-weight:600; letter-spacing:.14em; text-transform:uppercase;
  color:var(--muted); margin:64px 0 6px; padding-bottom:8px; border-bottom:1px solid var(--line2); }}
.sublede {{ font-size:16px; color:var(--ink2); max-width:66ch; margin:14px 0 26px; }}

/* roster */
.roster {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(218px,1fr)); gap:10px; }}
.rcard {{ background:var(--panel); border:1px solid var(--line2); padding:16px 16px 14px;
  display:flex; flex-direction:column; gap:3px; text-decoration:none; color:inherit;
  transition:background .12s, border-color .12s; }}
.rcard:hover {{ border-color:var(--agi); }}
.rcard:hover, .rcard:focus-visible {{ background:var(--panel2); outline:none; }}
.rcard:focus-visible {{ box-shadow:inset 0 0 0 2px var(--agi); }}
.rnum {{ font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--muted); }}
.rname {{ font-family:"Archivo",sans-serif; font-weight:600; font-size:17px; line-height:1.2; }}
.rtitle {{ font-size:14px; color:var(--muted); line-height:1.3; }}
.rpersona {{ font-family:"IBM Plex Mono",monospace; font-size:11px; letter-spacing:.03em;
  color:var(--agi); margin-top:7px; text-transform:uppercase; }}
.rmeans {{ display:flex; gap:14px; margin-top:10px; padding-top:9px; border-top:1px solid var(--line);
  font-family:"IBM Plex Mono",monospace; font-size:10.5px; color:var(--muted);
  text-transform:uppercase; letter-spacing:.05em; }}
.mn b {{ font-size:14px; letter-spacing:0; display:block; }}
.mn.dir b {{ color:var(--dir); }} .mn.agi b {{ color:var(--agi); }}

/* legend + distribution */
.legend {{ display:flex; flex-wrap:wrap; gap:26px; align-items:flex-start; margin:0 0 26px; }}
.lg {{ font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--muted); }}
.lg .lgt {{ display:block; text-transform:uppercase; letter-spacing:.1em; margin-bottom:7px; }}
.chips {{ display:flex; gap:3px; }}
.chip {{ width:26px; height:26px; display:grid; place-items:center; font-size:12px; font-weight:600;
  border:1px solid var(--line2); }}
.distbar {{ display:flex; height:38px; border:1px solid var(--line2); margin:0 0 8px; }}
.db {{ display:flex; align-items:center; justify-content:center; gap:6px; min-width:0;
  font-family:"IBM Plex Mono",monospace; font-size:11px; }}
.db i {{ font-style:normal; opacity:.7; }} .db b {{ font-weight:600; }}
.distnote {{ font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--muted); margin:0 0 34px; }}

/* matrix */
.mblock {{ margin-bottom:34px; }}
.mbt {{ font-size:15px; font-weight:600; margin:0 0 3px; }}
.mbn {{ font-size:14px; color:var(--muted); margin:0 0 12px; max-width:70ch; }}
.scroller {{ overflow-x:auto; border:1px solid var(--line2); background:var(--panel); }}
.matrix {{ border-collapse:collapse; width:100%; min-width:900px; }}
.matrix th, .matrix td {{ border-bottom:1px solid var(--line); }}
.matrix thead th {{ position:sticky; top:0; background:var(--panel2); z-index:2;
  font-family:"Archivo",sans-serif; font-size:11.5px; font-weight:600; padding:10px 4px;
  border-bottom:1px solid var(--line2); color:var(--ink2); }}
.matrix thead th.corner {{ text-align:left; padding-left:14px; width:46%; }}
.qh {{ text-align:left; padding:9px 14px 9px 14px; font-weight:400; vertical-align:top; }}
.qc {{ font-family:"IBM Plex Mono",monospace; font-size:11px; font-weight:600; color:var(--muted);
  display:inline-block; width:42px; }}
.qp {{ font-size:14.5px; color:var(--ink2); }}
.qi {{ font-family:"IBM Plex Mono",monospace; font-size:10px; color:var(--muted);
  display:block; margin:3px 0 0 42px; text-transform:uppercase; letter-spacing:.07em; }}
.cel {{ text-align:center; font-family:"IBM Plex Mono",monospace; font-size:13px; font-weight:600;
  border-left:1px solid var(--line); }}
.cel span {{ display:block; padding:8px 0; }}
.lad.v0 {{ background:var(--v0); color:var(--v0t); }} .lad.v1 {{ background:var(--v1); color:var(--v1t); }}
.lad.v2 {{ background:var(--v2); color:var(--v2t); }} .lad.v3 {{ background:var(--v3); color:var(--v3t); }}
.lad.v4 {{ background:var(--v4); color:var(--v4t); }}
.sp.v0 {{ background:var(--s0); color:var(--s0t); }} .sp.v1 {{ background:var(--s1); color:var(--s1t); }}
.sp.v2 {{ background:var(--s2); color:var(--s2t); }} .sp.v3 {{ background:var(--s3); color:var(--s3t); }}
.sp.v4 {{ background:var(--s4); color:var(--s4t); }}

/* dossiers */
.dossier {{ background:var(--panel); border:1px solid var(--line2); margin-bottom:26px;
  box-shadow:var(--shadow); scroll-margin-top:16px; }}
.dhead {{ display:flex; flex-wrap:wrap; gap:18px 26px; align-items:baseline;
  padding:20px 24px; border-bottom:1px solid var(--line2); background:var(--panel2); }}
.dnum {{ font-family:"IBM Plex Mono",monospace; font-size:12px; color:var(--muted); }}
.dwho {{ flex:1 1 240px; }}
.dwho h3 {{ margin:0; font-size:23px; font-weight:700; letter-spacing:-.01em; }}
.drole {{ margin:1px 0 0; font-size:15px; color:var(--muted); }}
.dpersona {{ border-left:2px solid var(--agi); padding-left:12px; }}
.plabel {{ display:block; font-family:"IBM Plex Mono",monospace; font-size:10px; color:var(--muted);
  text-transform:uppercase; letter-spacing:.1em; }}
.pname {{ font-family:"Archivo",sans-serif; font-weight:600; font-size:15px; color:var(--agi); }}
.dscores {{ display:flex; gap:20px; }}
.ds {{ text-align:right; }}
.ds b {{ display:block; font-family:"IBM Plex Mono",monospace; font-size:21px; font-weight:600;
  font-variant-numeric:tabular-nums; line-height:1.1; }}
.ds i {{ font-style:normal; font-family:"IBM Plex Mono",monospace; font-size:9.5px;
  color:var(--muted); text-transform:uppercase; letter-spacing:.08em; }}
.ds.dir b {{ color:var(--dir); }} .ds.agi b {{ color:var(--agi); }}
.dnotes {{ padding:18px 24px 4px; display:grid; gap:12px; }}
.dnotes p {{ margin:0; font-size:15.5px; color:var(--ink2); max-width:78ch; }}
.nl {{ display:block; font-family:"IBM Plex Mono",monospace; font-size:10px; color:var(--muted);
  text-transform:uppercase; letter-spacing:.1em; margin-bottom:2px; }}

.tblwrap {{ overflow-x:auto; margin:20px 0 0; border-top:1px solid var(--line); }}
.ans {{ border-collapse:collapse; width:100%; min-width:820px; }}
.ans caption {{ text-align:left; padding:14px 24px 10px; font-family:"IBM Plex Mono",monospace;
  font-size:11px; letter-spacing:.1em; text-transform:uppercase; color:var(--muted); }}
.ans thead th {{ text-align:left; font-family:"Archivo",sans-serif; font-size:10.5px; font-weight:600;
  text-transform:uppercase; letter-spacing:.08em; color:var(--muted); padding:6px 10px;
  border-bottom:1px solid var(--line2); }}
.ans thead th:first-child {{ padding-left:24px; }}
.ans td {{ padding:9px 10px; border-bottom:1px solid var(--line); vertical-align:top; font-size:14.5px; }}
.ans tbody tr:last-child td {{ border-bottom:none; }}
.ans tbody tr:hover td {{ background:var(--panel2); }}
.c-code {{ padding-left:24px !important; font-family:"IBM Plex Mono",monospace; font-size:11.5px;
  color:var(--muted); white-space:nowrap; }}
.c-score {{ width:44px; }}
.pill {{ display:inline-grid; place-items:center; width:24px; height:24px;
  font-family:"IBM Plex Mono",monospace; font-size:12.5px; font-weight:600;
  border:1px solid var(--line2); }}
.pill.lad.v0 {{ background:var(--v0); color:var(--v0t); }} .pill.lad.v1 {{ background:var(--v1); color:var(--v1t); }}
.pill.lad.v2 {{ background:var(--v2); color:var(--v2t); }} .pill.lad.v3 {{ background:var(--v3); color:var(--v3t); }}
.pill.lad.v4 {{ background:var(--v4); color:var(--v4t); }}
.c-q {{ width:30%; color:var(--muted); }}
.c-opt {{ width:26%; color:var(--ink); }}
.c-why {{ width:26%; color:var(--ink2); font-style:italic; }}
.c-why::before {{ content:"\\201C"; }} .c-why::after {{ content:"\\201D"; }}

footer {{ margin-top:60px; padding-top:20px; border-top:1px solid var(--line2);
  font-family:"IBM Plex Mono",monospace; font-size:11.5px; color:var(--muted); line-height:1.8; }}
@media (prefers-reduced-motion: reduce) {{ * {{ transition:none !important; animation:none !important; }} }}
@media (max-width:640px) {{
  .dhead {{ gap:12px; }} .dscores {{ gap:16px; }} .ds {{ text-align:left; }}
}}
</style>

<div class="wrap">
<header class="top">
  <p class="eyebrow">Synthetic assessment data &middot; Temp Agency roster</p>
  <h1>Ten voices from<br>Community Harvest</h1>
  <p class="lede">Every named paid staff member at Community Harvest Food Bank of Northeast Indiana,
  matched to a Temp Agency specialist persona, then simulated answering all 26 Future Ready
  questions &mdash; the 6-question Check and the 20 questions that only appear in the Full assessment.</p>
  <div class="facts">
    <span><b>10</b> employees</span><span><b>10</b> distinct personas</span>
    <span><b>26</b> questions each</span><span><b>260</b> scored answers</span>
    <span><b>Sonnet</b> simulation agents</span>
  </div>
  <p class="warn"><b>These answers are fabricated.</b> Real people hold these jobs at a real food bank.
  Nothing here reflects anything they have said, believe, or would score. This panel exists to
  stress-test the assessment instrument with plausible, differentiated synthetic respondents.</p>
</header>

<h2>The panel</h2>
<p class="sublede">Board members were excluded &mdash; they are unpaid governance, not employees.
Volunteer-operations staff Elan Williams and Ethan Horan fall outside the ten-person limit.
Each person drew a different persona, so no two respondents reason the same way.</p>
<div class="roster">{roster}</div>

<h2>How the panel answered</h2>
<p class="sublede">Two scales are in play, and they do not mean the same thing.
<b>Focus</b> questions run 0&rarr;4 as a maturity ladder, where 4 is genuinely more capable.
<b>Tradeoff</b> questions run 0&rarr;4 as a temperament spectrum &mdash; a 1 is not worse than a 3,
it sits at the other end. They are colored differently below so the matrix is not misread.</p>

<div class="legend">
  <div class="lg"><span class="lgt">Focus &mdash; maturity ladder</span>
    <div class="chips"><span class="chip lad v0">0</span><span class="chip lad v1">1</span><span class="chip lad v2">2</span><span class="chip lad v3">3</span><span class="chip lad v4">4</span></div>
  </div>
  <div class="lg"><span class="lgt">Tradeoff &mdash; temperament spectrum</span>
    <div class="chips"><span class="chip sp v0">0</span><span class="chip sp v1">1</span><span class="chip sp v2">2</span><span class="chip sp v3">3</span><span class="chip sp v4">4</span></div>
  </div>
</div>

<div class="distbar">{distbar}</div>
<p class="distnote">Distribution of all 260 answers. The panel clusters at 1&ndash;2: a lean,
audit-driven, volunteer-dependent organization does not score itself as future-ready.
Widest spread sits on <b>{e(highest['name'])}</b> ({(mean(highest,DIRECTION)+mean(highest,AGILITY))/2:.2f} focus mean)
against <b>{e(lowest['name'])}</b> ({(mean(lowest,DIRECTION)+mean(lowest,AGILITY))/2:.2f}).</p>

{matrix_block('Direction focus &mdash; 8 questions',
  'Whether the organization understands what stakeholders actually need, and whether mission functions as a real constraint on decisions.',
  DIRECTION)}
{matrix_block('Agility focus &mdash; 8 questions',
  'Whether the organization can sense change, question itself, and move resources and authority when it matters.',
  AGILITY)}
{matrix_block('Tradeoff questions &mdash; 10 questions',
  'Temperament, not capability. Low sits toward deliberation, endurance and protecting what works; high sits toward tempo, pruning and pursuing the new.',
  TRADEOFF)}

<h2>Individual responses</h2>
<p class="sublede">Each dossier carries the persona rationale, the answering posture the simulation
adopted, and all 26 answers with the respondent&rsquo;s own ten-word reasoning.</p>
{dossiers}

<footer>
Source documents: Community Harvest Organizational Analysis; Future Ready Check (6 questions);
Future Ready Full (20 additional questions).<br>
Personas drawn from the Temp Agency roster &mdash; 24 built specialist profiles.<br>
Generated {len(D)} &times; 26 = {len(D)*26} synthetic answers. Not real respondent data.
</footer>
</div>'''

open('/home/user/temp-agency/docs/synthetic/community-harvest-panel.html','w').write(HTML)
print('written', len(HTML), 'bytes')
