#!/usr/bin/env python3
"""Parse assessment question documents into a questions.json manifest.

The manifest is the single source of truth for every downstream step: which
questions exist, which instrument each belongs to, how they group, and whether
a question is a maturity ladder or a temperament spectrum.

Usage:
  parse_questions.py --docx check.docx:check --docx full.docx:full -o questions.json
  parse_questions.py --txt check.txt:check --overrides overrides.json -o questions.json

Expected document shape (one block per question):
    <CODE> · <Axis label>
    Prompt: <question text>
    0 · <option text>
    ...
    4 · <option text>

Codes are whatever the source document uses; nothing is hardcoded.
"""
import argparse, json, re, sys, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
CODE_RE = re.compile(r'^([A-Za-z]{1,4}\d{1,3})\s*[·:.\-]\s*(.+)$')
OPT_RE = re.compile(r'^(\d{1,2})\s*[·:.\-]\s*(.+)$')
PROMPT_RE = re.compile(r'^Prompt\s*:\s*(.+)$', re.I)


def docx_paragraphs(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read('word/document.xml'))
    for para in root.iter(W + 'p'):
        yield ''.join(n.text or '' for n in para.iter(W + 't'))


def txt_paragraphs(path):
    yield from Path(path).read_text(encoding='utf-8').split('\n')


def parse_source(path, instrument, questions, order):
    """Read one source document and add its questions to the shared manifest."""
    reader = docx_paragraphs if str(path).lower().endswith('.docx') else txt_paragraphs
    current = None
    for raw in reader(path):
        line = raw.strip()
        if not line:
            continue
        m = CODE_RE.match(line)
        if m and not OPT_RE.match(line):
            current = m.group(1).upper()
            if current in questions:
                # Same question appearing in a second instrument.
                questions[current]['instruments'].append(instrument)
                continue
            questions[current] = {
                'code': current,
                'axis': m.group(2).strip(),
                'prompt': '',
                'options': {},
                'instruments': [instrument],
            }
            order.append(current)
            continue
        if current is None:
            continue
        m = PROMPT_RE.match(line)
        if m:
            questions[current]['prompt'] = m.group(1).strip()
            continue
        m = OPT_RE.match(line)
        if m:
            questions[current]['options'][m.group(1)] = m.group(2).strip()


def derive_group(axis):
    """Collapse an axis label to the group it belongs to.

    'Direction Focus in a Sensing Context'            -> 'Direction Focus'
    'Sensing vs. Creating Tradeoff, Focused on Agility' -> 'Sensing vs. Creating Tradeoff'
    'Direction vs. Agility Tradeoff (Broad)'          -> 'Direction vs. Agility Tradeoff'
    """
    g = axis
    for pat in (r'\s*\(Broad\)\s*$', r',?\s*Focused on .+$', r',?\s*in an? .+ Context\s*$'):
        g = re.sub(pat, '', g, flags=re.I)
    return g.strip().rstrip(',')


def derive_kind(axis):
    """Tradeoff axes are temperament spectrums; everything else is a maturity ladder."""
    return 'spectrum' if 'tradeoff' in axis.lower() else 'ladder'


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--docx', action='append', default=[], metavar='PATH:INSTRUMENT',
                    help='Word source and the instrument name its questions belong to')
    ap.add_argument('--txt', action='append', default=[], metavar='PATH:INSTRUMENT',
                    help='Plain-text source, same PATH:INSTRUMENT form')
    ap.add_argument('--overrides', help='JSON file of per-code overrides, e.g. '
                                        '{"TC2": {"kind": "ladder", "group": "Portfolio"}}')
    ap.add_argument('-o', '--out', required=True)
    args = ap.parse_args()

    sources = []
    for spec in args.docx + args.txt:
        if ':' not in spec:
            ap.error(f'expected PATH:INSTRUMENT, got {spec!r}')
        path, _, instrument = spec.rpartition(':')
        sources.append((path, instrument))
    if not sources:
        ap.error('give at least one --docx or --txt')

    questions, order = {}, []
    for path, instrument in sources:
        parse_source(path, instrument, questions, order)

    for code in order:
        q = questions[code]
        q['group'] = derive_group(q['axis'])
        q['kind'] = derive_kind(q['axis'])

    if args.overrides:
        for code, patch in json.loads(Path(args.overrides).read_text()).items():
            if code.upper() not in questions:
                sys.exit(f'override names unknown question {code!r}')
            questions[code.upper()].update(patch)

    problems = []
    for code in order:
        q = questions[code]
        if not q['prompt']:
            problems.append(f'{code}: no prompt line')
        if len(q['options']) < 2:
            problems.append(f'{code}: only {len(q["options"])} option(s)')
    if problems:
        sys.exit('Could not parse cleanly:\n  ' + '\n  '.join(problems))

    manifest = {
        'scale': sorted({int(k) for c in order for k in questions[c]['options']}),
        'instruments': sorted({i for c in order for i in questions[c]['instruments']}),
        'order': order,
        'questions': {c: questions[c] for c in order},
    }
    Path(args.out).write_text(json.dumps(manifest, indent=1) + '\n')

    groups = {}
    for c in order:
        groups.setdefault(questions[c]['group'], []).append(c)
    print(f'{len(order)} questions -> {args.out}')
    print(f'  scale: {manifest["scale"][0]}-{manifest["scale"][-1]}')
    print(f'  instruments: {", ".join(manifest["instruments"])}')
    for g, codes in groups.items():
        print(f'  {g} [{questions[codes[0]]["kind"]}]: {len(codes)} — {" ".join(codes)}')


if __name__ == '__main__':
    main()
