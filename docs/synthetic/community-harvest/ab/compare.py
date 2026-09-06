#!/usr/bin/env python3
"""Compare two prompt variants over the respondents they share.

Reports per-group means and, for spectrum groups, whether removing the scale
key from the prompt pushed answers upward.
"""
import argparse, json, sys
from pathlib import Path
from statistics import mean

ap = argparse.ArgumentParser()
ap.add_argument('--questions', required=True)
ap.add_argument('--a', required=True, help='data.json for variant A')
ap.add_argument('--b', required=True, help='data.json for variant B')
ap.add_argument('--label-a', default='A')
ap.add_argument('--label-b', default='B')
args = ap.parse_args()

M = json.loads(Path(args.questions).read_text())
Q, ORDER = M['questions'], M['order']
groups, kind = {}, {}
for c in ORDER:
    groups.setdefault(Q[c]['group'], []).append(c)
    kind[Q[c]['group']] = Q[c]['kind']

A = {p['name']: p for p in json.loads(Path(args.a).read_text())}
B = {p['name']: p for p in json.loads(Path(args.b).read_text())}
shared = [n for n in A if n in B]
if not shared:
    sys.exit('no respondents in common')

print(f'Comparing {len(shared)} shared respondent(s): {", ".join(shared)}\n')

W = max(len(g) for g in groups) + 2
print(f'{"GROUP":<{W}} {"kind":<9} {args.label_a:>7} {args.label_b:>7} {"delta":>7}')
print('-' * (W + 34))
for g, codes in groups.items():
    a = mean(A[n]['rows'][c]['score'] for n in shared for c in codes)
    b = mean(B[n]['rows'][c]['score'] for n in shared for c in codes)
    print(f'{g:<{W}} {kind[g]:<9} {a:>7.2f} {b:>7.2f} {b-a:>+7.2f}')

alla = [A[n]['rows'][c]['score'] for n in shared for c in ORDER]
allb = [B[n]['rows'][c]['score'] for n in shared for c in ORDER]
print(f'\n{"ALL QUESTIONS":<{W}} {"":<9} {mean(alla):>7.2f} {mean(allb):>7.2f} {mean(allb)-mean(alla):>+7.2f}')

spec = [c for c in ORDER if Q[c]['kind'] == 'spectrum']
print(f'\nSpectrum items only ({len(spec)} questions) — the ones the removed scale key covered:')
for n in shared:
    a = [A[n]['rows'][c]['score'] for c in spec]
    b = [B[n]['rows'][c]['score'] for c in spec]
    moved = sum(1 for c in spec if A[n]['rows'][c]['score'] != B[n]['rows'][c]['score'])
    print(f'  {n:<22} {args.label_a} {mean(a):.2f}  ->  {args.label_b} {mean(b):.2f} '
          f'({mean(b)-mean(a):+.2f}), {moved}/{len(spec)} answers changed')

print('\nPer-respondent, all questions:')
for n in shared:
    a = [A[n]['rows'][c]['score'] for c in ORDER]
    b = [B[n]['rows'][c]['score'] for c in ORDER]
    moved = sum(1 for c in ORDER if A[n]['rows'][c]['score'] != B[n]['rows'][c]['score'])
    print(f'  {n:<22} {mean(a):.2f}  ->  {mean(b):.2f} ({mean(b)-mean(a):+.2f}), '
          f'{moved}/{len(ORDER)} answers changed')

print('\nLargest single-question moves:')
deltas = []
for n in shared:
    for c in ORDER:
        d = B[n]['rows'][c]['score'] - A[n]['rows'][c]['score']
        if d:
            deltas.append((abs(d), d, n, c, Q[c]['kind']))
for _, d, n, c, k in sorted(deltas, reverse=True)[:10]:
    print(f'  {c:<5} {k:<9} {n:<22} {d:+d}')
