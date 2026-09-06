#!/usr/bin/env python3
"""Emit the answer-table skeleton to paste into a respondent prompt.

Every question code is listed explicitly. Agents silently drop rows they have
to infer, so the skeleton is generated rather than described.

Usage:
  build_skeleton.py --questions questions.json
  build_skeleton.py --questions questions.json --by group
"""
import argparse, json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--questions', required=True)
    ap.add_argument('--by', choices=['instrument', 'group', 'none'], default='instrument',
                    help='how to section the tables (default: instrument)')
    args = ap.parse_args()

    M = json.loads(Path(args.questions).read_text())
    Q, ORDER = M['questions'], M['order']
    lo, hi = M['scale'][0], M['scale'][-1]

    if args.by == 'instrument':
        sections = [(i, [c for c in ORDER if i in Q[c]['instruments']]) for i in M['instruments']]
    elif args.by == 'group':
        seen = {}
        for c in ORDER:
            seen.setdefault(Q[c]['group'], []).append(c)
        sections = list(seen.items())
    else:
        sections = [('All questions', ORDER)]

    out = []
    for name, codes in sections:
        if not codes:
            continue
        out.append(f'## {name.title()} ({len(codes)} questions)')
        out.append('| Code | Score | Option chosen (short paraphrase) | Why |')
        out.append('|---|---|---|---|')
        for c in codes:
            out.append(f'| {c} |  |  |  |')
        out.append('')
    out.append(f'Score is a single whole number from {lo} to {hi}. Fill every row.')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
