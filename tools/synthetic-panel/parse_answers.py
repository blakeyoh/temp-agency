#!/usr/bin/env python3
"""Validate simulated respondent files and collect them into data.json.

Every respondent file must answer every question in the manifest. Missing,
unknown, duplicated, or out-of-range answers are hard errors — a silently
dropped column is worse than a failed build.

Usage:
  parse_answers.py --questions questions.json --answers answers/ -o data.json
"""
import argparse, html, json, re, sys
from pathlib import Path

HEAD_RE = re.compile(r'^#\s+(.+?)\s+[—–-]\s+(.+?)\s*$', re.M)
FIELD_RE = r'^\*\*{label}[^:]*:\*\*\s*(.+?)\s*$'
ROW_RE = re.compile(r'^\|\s*([A-Za-z]{1,4}\d{1,3})\s*\|\s*(\d{1,2})\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$', re.M)


def field(text, label, required=True, default=''):
    m = re.search(FIELD_RE.format(label=re.escape(label)), text, re.M)
    if m:
        return m.group(1).strip()
    if required:
        raise ValueError(f'missing "**{label}:**" line')
    return default


def parse_one(path, manifest):
    text = path.read_text(encoding='utf-8')
    codes = manifest['order']
    scale = set(manifest['scale'])

    m = HEAD_RE.search(text)
    if not m:
        raise ValueError('first line must be "# Name — Title"')
    name, title = m.group(1).strip(), m.group(2).strip()

    rows, seen = {}, []
    for code, score, opt, why in ROW_RE.findall(text):
        code = code.upper()
        seen.append(code)
        if code not in manifest['questions']:
            raise ValueError(f'{code} is not in the question manifest')
        if int(score) not in scale:
            raise ValueError(f'{code}: score {score} outside scale {sorted(scale)}')
        rows[code] = {'score': int(score), 'option': opt, 'why': why}

    dupes = {c for c in seen if seen.count(c) > 1}
    if dupes:
        raise ValueError(f'answered more than once: {", ".join(sorted(dupes))}')
    missing = [c for c in codes if c not in rows]
    if missing:
        raise ValueError(f'no answer for: {", ".join(missing)}')

    return {
        'file': path.name,
        'name': name,
        'title': title,
        'persona': field(text, 'Persona'),
        'fit': field(text, 'Persona fit', required=False),
        'posture': field(text, 'Answering posture', required=False),
        'rows': rows,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--questions', required=True)
    ap.add_argument('--answers', required=True, help='directory of respondent .md files')
    ap.add_argument('-o', '--out', required=True)
    args = ap.parse_args()

    manifest = json.loads(Path(args.questions).read_text())
    files = sorted(Path(args.answers).glob('*.md'))
    if not files:
        sys.exit(f'no .md files in {args.answers}')

    people, errors = [], []
    for path in files:
        try:
            people.append(parse_one(path, manifest))
        except ValueError as e:
            errors.append(f'{path.name}: {e}')
    if errors:
        sys.exit('Respondent files rejected:\n  ' + '\n  '.join(errors))

    personas = [p['persona'] for p in people]
    repeats = {p for p in personas if personas.count(p) > 1}

    Path(args.out).write_text(json.dumps(people, indent=1) + '\n')
    print(f'{len(people)} respondents x {len(manifest["order"])} questions '
          f'= {len(people) * len(manifest["order"])} answers -> {args.out}')
    if repeats:
        print(f'  note: persona reused by more than one respondent: {", ".join(sorted(repeats))}')


if __name__ == '__main__':
    main()
