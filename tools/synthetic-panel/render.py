#!/usr/bin/env python3
"""Render questions.json + data.json into a standalone panel page.

Nothing about the instrument is hardcoded: question codes, groups, ladder vs
spectrum, and the score range all come from the manifest, so swapping the
source documents and re-running is enough.

Usage:
  render.py --questions questions.json --data data.json --config panel.json -o panel.html
"""
import argparse, html, json
from pathlib import Path

e = html.escape

DEFAULTS = {
    'title': 'Synthetic Assessment Panel',
    'eyebrow': 'Synthetic assessment data',
    'headline': 'Synthetic\nassessment panel',
    'lede': 'Simulated respondents answering an organizational assessment in character.',
    'notice_lead': 'These answers are fabricated.',
    'notice': 'They are synthetic respondents, not real people, and nothing here reflects '
              'anything a real person has said or would score.',
    'panel_note': '',
    'footer': [],
}

# Ramp endpoints per theme: (ladder low, ladder high) and diverging (low, mid, high).
RAMPS = {
    'light': {'lad': ('#f0efe9', '#8a6f22'), 'sp': ('#cfe0e2', '#eceee9', '#e5c58c')},
    'dark':  {'lad': ('#1e2523', '#a3873a'), 'sp': ('#153f45', '#242d2b', '#6a5320')},
}


def hexrgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    ra, rb = hexrgb(a), hexrgb(b)
    return '#%02x%02x%02x' % tuple(round(ra[i] + (rb[i] - ra[i]) * t) for i in range(3))


def readable_on(bg):
    r, g, b = [c / 255 for c in hexrgb(bg)]
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return '#121a18' if lum > 0.55 else '#fbfdfc'


def ramp_css(scale, theme):
    """Emit --lad-N / --sp-N background and text tokens for every score."""
    n = len(scale)
    lo, hi = RAMPS[theme]['lad']
    slo, smid, shi = RAMPS[theme]['sp']
    out = []
    for i, s in enumerate(scale):
        t = i / max(n - 1, 1)
        lad = mix(lo, hi, t)
        sp = mix(slo, smid, t * 2) if t <= .5 else mix(smid, shi, (t - .5) * 2)
        out.append(f'  --lad-{s}:{lad}; --lad-{s}-t:{readable_on(lad)};'
                   f' --sp-{s}:{sp}; --sp-{s}-t:{readable_on(sp)};')
    return '\n'.join(out)


def score_classes(scale):
    rules = []
    for s in scale:
        rules.append(f'.lad.v{s}{{background:var(--lad-{s});color:var(--lad-{s}-t);}}')
        rules.append(f'.sp.v{s}{{background:var(--sp-{s});color:var(--sp-{s}-t);}}')
    return '\n'.join(rules)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--questions', required=True)
    ap.add_argument('--data', required=True)
    ap.add_argument('--config', help='optional JSON of page copy; see DEFAULTS in this file')
    ap.add_argument('-o', '--out', required=True)
    args = ap.parse_args()

    M = json.loads(Path(args.questions).read_text())
    D = json.loads(Path(args.data).read_text())
    cfg = dict(DEFAULTS)
    if args.config:
        cfg.update(json.loads(Path(args.config).read_text()))

    Q, ORDER, SCALE = M['questions'], M['order'], M['scale']
    INSTRUMENTS = M['instruments']

    groups, gkind = {}, {}
    for c in ORDER:
        groups.setdefault(Q[c]['group'], []).append(c)
        gkind[Q[c]['group']] = Q[c]['kind']
    ladder_groups = [g for g in groups if gkind[g] == 'ladder']

    def gmean(p, g):
        codes = groups[g]
        return sum(p['rows'][c]['score'] for c in codes) / len(codes)

    def surname(n):
        return n.split()[-1]

    def instr_label(c):
        return ' + '.join(Q[c]['instruments'])

    # ---- roster ----
    roster = ''
    for i, p in enumerate(D):
        means = ''.join(
            f'<span class="mn g{gi}"><b>{gmean(p, g):.2f}</b>{e(g.replace(" Focus", ""))}</span>'
            for gi, g in enumerate(ladder_groups))
        roster += (f'<a class="rcard" href="#p{i+1}"><span class="rnum">{i+1:02d}</span>'
                   f'<span class="rname">{e(p["name"])}</span>'
                   f'<span class="rtitle">{e(p["title"])}</span>'
                   f'<span class="rpersona">{e(p["persona"])}</span>'
                   f'<span class="rmeans">{means}</span></a>')

    # ---- matrix ----
    heads = ''.join(f'<th scope="col"><span>{e(surname(p["name"]))}</span></th>' for p in D)
    matrix = ''
    for g, codes in groups.items():
        kind = gkind[g]
        rows = ''
        for c in codes:
            cells = ''.join(
                f'<td class="cel {"sp" if kind == "spectrum" else "lad"} '
                f'v{p["rows"][c]["score"]}"><span>{p["rows"][c]["score"]}</span></td>' for p in D)
            rows += (f'<tr><th scope="row" class="qh"><span class="qc">{c}</span>'
                     f'<span class="qp">{e(Q[c]["prompt"])}</span>'
                     f'<span class="qi">{e(instr_label(c))}</span></th>{cells}</tr>')
        note = ('Temperament, not capability &mdash; a low score sits at the other end of the '
                'spectrum, not lower on a ladder.' if kind == 'spectrum'
                else 'Maturity ladder &mdash; a higher score is a stronger capability.')
        matrix += (f'<section class="mblock"><h3 class="mbt">{e(g)} '
                   f'<span class="mbc">{len(codes)} questions</span></h3>'
                   f'<p class="mbn">{note}</p><div class="scroller"><table class="matrix">'
                   f'<thead><tr><th class="corner" scope="col">Question</th>{heads}</tr></thead>'
                   f'<tbody>{rows}</tbody></table></div></section>')

    # ---- dossiers ----
    def table(p, codes, cap):
        rows = ''
        for c in codes:
            r, kind = p['rows'][c], Q[c]['kind']
            rows += (f'<tr><td class="c-code">{c}</td>'
                     f'<td class="c-score"><span class="pill '
                     f'{"sp" if kind == "spectrum" else "lad"} v{r["score"]}">{r["score"]}</span></td>'
                     f'<td class="c-q">{e(Q[c]["prompt"])}</td>'
                     f'<td class="c-opt">{e(r["option"])}</td>'
                     f'<td class="c-why">{e(r["why"])}</td></tr>')
        return (f'<div class="tblwrap"><table class="ans"><caption>{cap}</caption><thead><tr>'
                f'<th>Code</th><th>Score</th><th>Question</th><th>Option chosen</th>'
                f'<th>Reasoning</th></tr></thead><tbody>{rows}</tbody></table></div>')

    dossiers = ''
    for i, p in enumerate(D):
        scores = ''.join(
            f'<span class="ds g{gi}"><b>{gmean(p, g):.2f}</b><i>{e(g)}</i></span>'
            for gi, g in enumerate(ladder_groups))
        notes = ''
        if p['fit']:
            notes += f'<p><span class="nl">Why this persona</span>{e(p["fit"])}</p>'
        if p['posture']:
            notes += f'<p><span class="nl">Answering posture</span>{e(p["posture"])}</p>'
        tables = ''
        for inst in INSTRUMENTS:
            codes = [c for c in ORDER if inst in Q[c]['instruments']]
            if codes:
                tables += table(p, codes, f'{e(inst).title()} &mdash; {len(codes)} questions')
        dossiers += (f'<article class="dossier" id="p{i+1}"><header class="dhead">'
                     f'<span class="dnum">{i+1:02d}</span>'
                     f'<div class="dwho"><h3>{e(p["name"])}</h3>'
                     f'<p class="drole">{e(p["title"])}</p></div>'
                     f'<div class="dpersona"><span class="plabel">Persona lens</span>'
                     f'<span class="pname">{e(p["persona"])}</span></div>'
                     f'<div class="dscores">{scores}</div></header>'
                     f'<div class="dnotes">{notes}</div>{tables}</article>')

    # ---- distribution ----
    allsc = [p['rows'][c]['score'] for p in D for c in ORDER]
    dist = {s: allsc.count(s) for s in SCALE}
    distbar = ''.join(
        f'<span class="db lad v{s}" style="flex:{max(dist[s], 1)}"><i>{s}</i><b>{dist[s]}</b></span>'
        for s in SCALE)

    chips = ''
    for kind, cls in (('Maturity ladder', 'lad'), ('Temperament spectrum', 'sp')):
        c = ''.join(f'<span class="chip {cls} v{s}">{s}</span>' for s in SCALE)
        chips += (f'<div class="lg"><span class="lgt">{kind}</span>'
                  f'<div class="chips">{c}</div></div>')

    facts = ''.join(f'<span><b>{v}</b> {k}</span>' for k, v in [
        ('respondents', len(D)), ('questions each', len(ORDER)),
        ('scored answers', len(D) * len(ORDER)),
        ('instruments', len(INSTRUMENTS)), ('question groups', len(groups))])

    footer = '<br>\n'.join(e(l) for l in cfg['footer']) or (
        f'{len(D)} respondents &times; {len(ORDER)} questions = {len(D) * len(ORDER)} '
        f'synthetic answers. Not real respondent data.')

    headline = '<br>'.join(e(l) for l in cfg['headline'].split('\n'))
    panel_note = f'<p class="sublede">{e(cfg["panel_note"])}</p>' if cfg['panel_note'] else ''

    HTML = f'''<title>{e(cfg['title'])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;800&family=IBM+Plex+Mono:wght@400;500;600&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&display=swap">
<style>
:root {{
  --ground:#edf0ee; --panel:#ffffff; --panel2:#f6f8f7; --ink:#141d1b; --ink2:#3d4a47;
  --muted:#6c7a76; --line:#d5dcd9; --line2:#c2ccc8;
  --g0:#a9670f; --g0-soft:#f2e3cd; --g1:#1c6670; --g2:#6b4f7a; --g3:#3f6b3a;
  --shadow:0 1px 2px rgba(20,29,27,.06), 0 8px 24px -16px rgba(20,29,27,.35);
{ramp_css(SCALE, 'light')}
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --ground:#101614; --panel:#18201e; --panel2:#1d2624; --ink:#e8eeeb; --ink2:#b6c2be;
    --muted:#8b9995; --line:#2b3532; --line2:#3a4642;
    --g0:#dda447; --g0-soft:#3a2d15; --g1:#63b7c1; --g2:#b394c4; --g3:#8dbd85;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 30px -18px rgba(0,0,0,.9);
{ramp_css(SCALE, 'dark')}
  }}
}}
:root[data-theme="dark"] {{
  --ground:#101614; --panel:#18201e; --panel2:#1d2624; --ink:#e8eeeb; --ink2:#b6c2be;
  --muted:#8b9995; --line:#2b3532; --line2:#3a4642;
  --g0:#dda447; --g0-soft:#3a2d15; --g1:#63b7c1; --g2:#b394c4; --g3:#8dbd85;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 30px -18px rgba(0,0,0,.9);
{ramp_css(SCALE, 'dark')}
}}
* {{ box-sizing:border-box; }}
body {{ background:var(--ground); color:var(--ink);
  font-family:"Newsreader",Georgia,"Times New Roman",serif; font-size:16px; line-height:1.55; }}
.wrap {{ max-width:1180px; margin:0 auto; padding:0 24px 96px; }}
h1,h2,h3,h4 {{ font-family:"Archivo","Helvetica Neue",Arial,sans-serif; text-wrap:balance; }}
.top {{ border-bottom:2px solid var(--ink); margin-bottom:40px; padding:44px 0 26px; }}
.eyebrow {{ font-family:"IBM Plex Mono",monospace; font-size:11px; letter-spacing:.16em;
  text-transform:uppercase; color:var(--muted); margin:0 0 14px; }}
h1 {{ font-size:clamp(30px,4.6vw,52px); font-weight:800; letter-spacing:-.02em;
  line-height:1.04; margin:0 0 14px; }}
.lede {{ font-size:19px; color:var(--ink2); max-width:62ch; margin:0 0 22px; }}
.facts {{ display:flex; flex-wrap:wrap; gap:8px 28px; font-family:"IBM Plex Mono",monospace;
  font-size:12px; color:var(--muted); }}
.facts b {{ color:var(--ink); font-weight:600; }}
.warn {{ margin-top:24px; border-left:3px solid var(--g0); background:var(--g0-soft);
  padding:12px 16px; font-size:14.5px; color:var(--ink2); border-radius:0 3px 3px 0; }}
.warn b {{ color:var(--ink); }}
h2 {{ font-size:13px; font-weight:600; letter-spacing:.14em; text-transform:uppercase;
  color:var(--muted); margin:64px 0 6px; padding-bottom:8px; border-bottom:1px solid var(--line2); }}
.sublede {{ font-size:16px; color:var(--ink2); max-width:66ch; margin:14px 0 26px; }}
.roster {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(218px,1fr)); gap:10px; }}
.rcard {{ background:var(--panel); border:1px solid var(--line2); padding:16px 16px 14px;
  display:flex; flex-direction:column; gap:3px; text-decoration:none; color:inherit;
  transition:background .12s, border-color .12s; }}
.rcard:hover {{ background:var(--panel2); border-color:var(--g1); }}
.rcard:focus-visible {{ outline:2px solid var(--g1); outline-offset:2px; }}
.rnum {{ font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--muted); }}
.rname {{ font-family:"Archivo",sans-serif; font-weight:600; font-size:17px; line-height:1.2; }}
.rtitle {{ font-size:14px; color:var(--muted); line-height:1.3; }}
.rpersona {{ font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--g1);
  margin-top:7px; text-transform:uppercase; letter-spacing:.03em; }}
.rmeans {{ display:flex; flex-wrap:wrap; gap:14px; margin-top:10px; padding-top:9px;
  border-top:1px solid var(--line); font-family:"IBM Plex Mono",monospace; font-size:10.5px;
  color:var(--muted); text-transform:uppercase; letter-spacing:.05em; }}
.mn b {{ font-size:14px; letter-spacing:0; display:block; }}
.mn.g0 b {{ color:var(--g0); }} .mn.g1 b {{ color:var(--g1); }}
.mn.g2 b {{ color:var(--g2); }} .mn.g3 b {{ color:var(--g3); }}
.legend {{ display:flex; flex-wrap:wrap; gap:26px; margin:0 0 26px; }}
.lg {{ font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--muted); }}
.lgt {{ display:block; text-transform:uppercase; letter-spacing:.1em; margin-bottom:7px; }}
.chips {{ display:flex; gap:3px; }}
.chip {{ width:26px; height:26px; display:grid; place-items:center; font-size:12px;
  font-weight:600; border:1px solid var(--line2); }}
.distbar {{ display:flex; height:38px; border:1px solid var(--line2); margin:0 0 8px; }}
.db {{ display:flex; align-items:center; justify-content:center; gap:6px; min-width:0;
  font-family:"IBM Plex Mono",monospace; font-size:11px; }}
.db i {{ font-style:normal; opacity:.7; }} .db b {{ font-weight:600; }}
.distnote {{ font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--muted);
  margin:0 0 34px; }}
.mblock {{ margin-bottom:34px; }}
.mbt {{ font-size:15px; font-weight:600; margin:0 0 3px; }}
.mbc {{ font-family:"IBM Plex Mono",monospace; font-size:11px; font-weight:400;
  color:var(--muted); letter-spacing:.04em; }}
.mbn {{ font-size:14px; color:var(--muted); margin:0 0 12px; max-width:70ch; }}
.scroller {{ overflow-x:auto; border:1px solid var(--line2); background:var(--panel); }}
.matrix {{ border-collapse:collapse; width:100%; min-width:900px; }}
.matrix th, .matrix td {{ border-bottom:1px solid var(--line); }}
.matrix thead th {{ position:sticky; top:0; background:var(--panel2); z-index:2;
  font-family:"Archivo",sans-serif; font-size:11.5px; font-weight:600; padding:10px 4px;
  border-bottom:1px solid var(--line2); color:var(--ink2); }}
.matrix thead th.corner {{ text-align:left; padding-left:14px; width:46%; }}
.qh {{ text-align:left; padding:9px 14px; font-weight:400; vertical-align:top; }}
.qc {{ font-family:"IBM Plex Mono",monospace; font-size:11px; font-weight:600;
  color:var(--muted); display:inline-block; width:42px; }}
.qp {{ font-size:14.5px; color:var(--ink2); }}
.qi {{ font-family:"IBM Plex Mono",monospace; font-size:10px; color:var(--muted);
  display:block; margin:3px 0 0 42px; text-transform:uppercase; letter-spacing:.07em; }}
.cel {{ text-align:center; font-family:"IBM Plex Mono",monospace; font-size:13px;
  font-weight:600; border-left:1px solid var(--line); }}
.cel span {{ display:block; padding:8px 0; }}
{score_classes(SCALE)}
.dossier {{ background:var(--panel); border:1px solid var(--line2); margin-bottom:26px;
  box-shadow:var(--shadow); scroll-margin-top:16px; }}
.dhead {{ display:flex; flex-wrap:wrap; gap:18px 26px; align-items:baseline; padding:20px 24px;
  border-bottom:1px solid var(--line2); background:var(--panel2); }}
.dnum {{ font-family:"IBM Plex Mono",monospace; font-size:12px; color:var(--muted); }}
.dwho {{ flex:1 1 240px; }}
.dwho h3 {{ margin:0; font-size:23px; font-weight:700; letter-spacing:-.01em; }}
.drole {{ margin:1px 0 0; font-size:15px; color:var(--muted); }}
.dpersona {{ border-left:2px solid var(--g1); padding-left:12px; }}
.plabel {{ display:block; font-family:"IBM Plex Mono",monospace; font-size:10px;
  color:var(--muted); text-transform:uppercase; letter-spacing:.1em; }}
.pname {{ font-family:"Archivo",sans-serif; font-weight:600; font-size:15px; color:var(--g1); }}
.dscores {{ display:flex; flex-wrap:wrap; gap:20px; }}
.ds {{ text-align:right; }}
.ds b {{ display:block; font-family:"IBM Plex Mono",monospace; font-size:21px; font-weight:600;
  font-variant-numeric:tabular-nums; line-height:1.1; }}
.ds i {{ font-style:normal; font-family:"IBM Plex Mono",monospace; font-size:9.5px;
  color:var(--muted); text-transform:uppercase; letter-spacing:.08em; }}
.ds.g0 b {{ color:var(--g0); }} .ds.g1 b {{ color:var(--g1); }}
.ds.g2 b {{ color:var(--g2); }} .ds.g3 b {{ color:var(--g3); }}
.dnotes {{ padding:18px 24px 4px; display:grid; gap:12px; }}
.dnotes p {{ margin:0; font-size:15.5px; color:var(--ink2); max-width:78ch; }}
.nl {{ display:block; font-family:"IBM Plex Mono",monospace; font-size:10px; color:var(--muted);
  text-transform:uppercase; letter-spacing:.1em; margin-bottom:2px; }}
.tblwrap {{ overflow-x:auto; margin:20px 0 0; border-top:1px solid var(--line); }}
.ans {{ border-collapse:collapse; width:100%; min-width:820px; }}
.ans caption {{ text-align:left; padding:14px 24px 10px; font-family:"IBM Plex Mono",monospace;
  font-size:11px; letter-spacing:.1em; text-transform:uppercase; color:var(--muted); }}
.ans thead th {{ text-align:left; font-family:"Archivo",sans-serif; font-size:10.5px;
  font-weight:600; text-transform:uppercase; letter-spacing:.08em; color:var(--muted);
  padding:6px 10px; border-bottom:1px solid var(--line2); }}
.ans thead th:first-child {{ padding-left:24px; }}
.ans td {{ padding:9px 10px; border-bottom:1px solid var(--line); vertical-align:top;
  font-size:14.5px; }}
.ans tbody tr:last-child td {{ border-bottom:none; }}
.ans tbody tr:hover td {{ background:var(--panel2); }}
.c-code {{ padding-left:24px !important; font-family:"IBM Plex Mono",monospace; font-size:11.5px;
  color:var(--muted); white-space:nowrap; }}
.c-score {{ width:44px; }}
.pill {{ display:inline-grid; place-items:center; width:24px; height:24px;
  font-family:"IBM Plex Mono",monospace; font-size:12.5px; font-weight:600;
  border:1px solid var(--line2); }}
.c-q {{ width:30%; color:var(--muted); }}
.c-opt {{ width:26%; color:var(--ink); }}
.c-why {{ width:26%; color:var(--ink2); font-style:italic; }}
.c-why::before {{ content:"\\201C"; }} .c-why::after {{ content:"\\201D"; }}
footer {{ margin-top:60px; padding-top:20px; border-top:1px solid var(--line2);
  font-family:"IBM Plex Mono",monospace; font-size:11.5px; color:var(--muted); line-height:1.8; }}
@media (prefers-reduced-motion: reduce) {{ * {{ transition:none !important; }} }}
@media (max-width:640px) {{ .dscores {{ gap:16px; }} .ds {{ text-align:left; }} }}
</style>
<div class="wrap">
<header class="top">
  <p class="eyebrow">{e(cfg['eyebrow'])}</p>
  <h1>{headline}</h1>
  <p class="lede">{e(cfg['lede'])}</p>
  <div class="facts">{facts}</div>
  <p class="warn"><b>{e(cfg['notice_lead'])}</b> {e(cfg['notice'])}</p>
</header>
<h2>The panel</h2>
{panel_note}
<div class="roster">{roster}</div>
<h2>How the panel answered</h2>
<p class="sublede">Two kinds of scale are in play. <b>Ladder</b> questions run low to high as a
maturity scale, where the top option is genuinely stronger. <b>Spectrum</b> questions describe
temperament, where a low score sits at the opposite end rather than lower down. They are colored
differently so the matrix is not misread.</p>
<div class="legend">{chips}</div>
<div class="distbar">{distbar}</div>
<p class="distnote">Distribution of all {len(allsc)} answers.</p>
{matrix}
<h2>Individual responses</h2>
<p class="sublede">Each dossier carries the persona rationale, the answering posture the
simulation adopted, and every answer with the respondent&rsquo;s own short reasoning.</p>
{dossiers}
<footer>{footer}</footer>
</div>'''

    Path(args.out).write_text(HTML)
    print(f'{args.out}  ({len(HTML):,} bytes)')
    print(f'  {len(D)} respondents, {len(ORDER)} questions, scale {SCALE[0]}-{SCALE[-1]}')
    print(f'  groups: ' + ', '.join(f'{g} ({gkind[g]}, {len(c)})' for g, c in groups.items()))


if __name__ == '__main__':
    main()
