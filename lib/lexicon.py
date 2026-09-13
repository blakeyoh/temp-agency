"""E5 frozen surface-term rejection with retained prior-round evidence."""
import json
import re
import unicodedata

from lib.paths import canonical_json, relative_to_root


def items(candidate):
    if set(candidate) != {'schema_version', 'items'} or type(candidate['schema_version']) is not int or candidate['schema_version'] != 1:
        raise ValueError('candidate schema version must be 1')
    rows = candidate['items']
    if not isinstance(rows, list) or not rows or len(rows) > 100:
        raise ValueError('candidate must contain 1-100 items')
    seen = set()
    for row in rows:
        if (set(row) != {'id', 'text'} or not isinstance(row['id'], str)
                or not re.fullmatch('[A-Za-z0-9_-]+', row['id']) or row['id'] in seen
                or not isinstance(row['text'], str) or not row['text'].strip()):
            raise ValueError('invalid candidate item or duplicate ID')
        seen.add(row['id'])
    return rows


def scan(candidate, terms):
    if (not isinstance(terms, list) or not terms or
            any(not isinstance(t, str) or not t.strip() or t != t.strip() for t in terms)
            or len({t.casefold() for t in terms}) != len(terms)):
        raise ValueError('lexicon needs unique nonempty terms')
    findings = []
    for row in items(candidate):
        text = unicodedata.normalize('NFKC', row['text'])
        for term in terms:
            tokens = unicodedata.normalize('NFKC', term).split()
            pattern = re.compile(r'(?<!\w)' + r'[\W_]+'.join(re.escape(t) for t in tokens) + r'(?!\w)', re.I)
            for match in pattern.finditer(text):
                findings.append({'item_id': row['id'], 'term': term, 'normalized_quote': match[0],
                                 'normalized_start': match.start(), 'normalized_end': match.end()})
    return findings


def render(root, args):
    paths = {name: relative_to_root(root, root / getattr(args, name)) for name in ('lexicon', 'profile', 'candidate')}
    if args.previous:
        paths['previous'] = relative_to_root(root, root / args.previous)
    if len(set(paths.values())) != len(paths):
        raise ValueError('inputs must be distinct')
    config = json.loads((root / paths['lexicon']).read_text())
    if type(config.get('schema_version')) is not int or config['schema_version'] != 1:
        raise ValueError('unsupported lexicon schema')
    if type(config.get('era')) is not int or config['era'] != args.era:
        raise ValueError('no frozen lexicon for requested era')
    if paths['profile'] != 'roster/' + args.specialist + '.md':
        raise ValueError('specialist must match its real roster profile')
    if not (root / paths['profile']).read_text().strip():
        raise ValueError('empty specialist profile')
    interval = config['specialists'][args.specialist]
    if (any(type(interval[k]) is not int for k in ('min_year', 'max_year'))
            or not interval['min_year'] <= args.era <= interval['max_year']):
        raise ValueError('era outside frozen specialist range')
    candidate = json.loads((root / paths['candidate']).read_text())
    findings = scan(candidate, config['forbidden_terms'])
    previous_id = None
    if args.previous:
        prior = json.loads((root / paths['previous']).read_text())
        if any(prior.get(k) != v for k, v in {'tool': 'lexicon-check', 'entrant': 'E5', 'status': 'ok'}.items()):
            raise ValueError('previous must be a successful E5 check receipt')
        old = json.loads(prior['output'])
        if old['era'] != args.era or old['specialist'] != args.specialist:
            raise ValueError('regeneration cannot switch era or specialist')
        for key in ('lexicon', 'profile'):
            from lib.paths import sha256_file
            if prior['inputs'][old['inputs'][key]] != sha256_file(root / paths[key]):
                raise ValueError('regeneration cannot change the lexicon or profile')
        before = {r['id']: r['text'] for r in items(old['candidate'])}
        after = {r['id']: r['text'] for r in items(candidate)}
        if set(before) != set(after):
            raise ValueError('regeneration must preserve item IDs')
        if any(before[f['item_id']] == after[f['item_id']] for f in old['leaks']):
            raise ValueError('every leaking item must be regenerated')
        previous_id = prior['receipt_id']
    return canonical_json({'tool': 'lexicon-check', 'entrant': 'E5', 'inputs': paths,
        'specialist': args.specialist, 'era': args.era, 'candidate': candidate,
        'leaks': findings, 'passed': not findings, 'previous_receipt_id': previous_id,
        'bound_span': 'frozen surface terms only; not all post-era concepts'})
