"""Regenerate DATA in box-score.html from r32-results.json.

The box score was hand-assembled for brackets 1-2. This makes it reproducible:
verdict files -> tally.py -> r32-results.json -> this -> box-score.html.
Only the `games` array is regenerated; `field` and `seed` are preserved from the
existing DATA blob, since the field roster is authored, not derived.
"""
import json, re, os, sys

SP = os.path.dirname(os.path.abspath(__file__))
HTML = f"{SP}/box-score.html"
CATNAME = {"entropy":"Entropy","constraint":"Constraint","apparatus":"Apparatus","memory":"Memory"}

src = open(HTML).read()
m = re.search(r'^const DATA = (\{.*\});$', src, re.M)
if not m:
    sys.exit("could not locate the DATA blob in box-score.html")
data = json.loads(m.group(1))
byCode = {f["c"]: f for f in data["field"]}

res = json.load(open(f"{SP}/r32-results.json"))
PANELS = ["Builder", "Skeptic", "Ecologist"]

def side(code):
    f = byCode[code]
    return {"c": code, "n": f["n"], "cat": CATNAME[f["cat"]], "col": f["cat"], "owner": f["o"]}

games = []
for n in sorted(res, key=int):
    r = res[n]
    rows = [{"axis": row["axis"], "a": row["raw"]["A"], "b": row["raw"]["B"],
             "votes": [[v[0], v[1], v[2]] for v in row["votes"]],
             "unan": row["unanimous"]} for row in r["rows"]]
    games.append({
        "g": int(n), "region": r["region"], "rgn": r["region"].lower(), "rows": rows,
        "A": side(r["A"]), "B": side(r["B"]), "tot": r["tot"],
        "winner": r["winner"], "loser": r["loser"], "winSide": r["winner_side"],
        "margin": r["margin"], "contested": r["contested"],
        "panels": r["panel_winners"],
        "dec": {p: r["decided"].get(p, "") for p in PANELS},
        "disp": {p: r["absorb"].get(p, {}).get("disp", "") for p in PANELS},
    })

data["games"] = games
blob = json.dumps(data, separators=(", ", ": "))
open(HTML, "w").write(src[:m.start()] + f"const DATA = {blob};" + src[m.end():])
print(f"box-score.html: wrote {len(games)} games ({', '.join('G'+str(g['g']) for g in games)})")
