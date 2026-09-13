"""Literal E4 section crossover; mutation and selection lifecycle are out of scope."""
import random
import re

from lib.paths import canonical_json, relative_to_root, sha256_file


def section(text, heading):
    matches = re.findall(r'^## ' + re.escape(heading) + r'\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    if len(matches) != 1 or not matches[0].strip():
        raise ValueError('requires exactly one nonempty ' + heading)
    return matches[0].strip()


def bullets(text):
    starts = list(re.finditer(r'^- ', text, re.M))
    if not starts or text[:starts[0].start()].strip():
        raise ValueError('Anti-Patterns must be bullet blocks')
    return [text[start.start():starts[i + 1].start() if i + 1 < len(starts) else len(text)].strip()
            for i, start in enumerate(starts)]


def render(root, parent_a, parent_b, seed):
    paths = [relative_to_root(root, root / p) for p in (parent_a, parent_b)]
    if paths[0] == paths[1]:
        raise ValueError('crossover requires two distinct parents')
    texts = [(root / p).read_text(encoding='utf-8') for p in paths]
    principles = section(texts[0], 'Core Principles')
    methodology = section(texts[1], 'Methodology')
    if len(re.findall(r'^### Phase \d+:', methodology, re.M)) < 2:
        raise ValueError('Methodology requires at least two numbered phases')
    antis = [bullets(section(t, 'Anti-Patterns')) for t in texts]
    first = random.Random(seed['value']).randrange(2)
    interleaved = []
    lineage = []
    for i in range(max(map(len, antis))):
        for parent in (first, 1 - first):
            if i < len(antis[parent]):
                interleaved.append(antis[parent][i])
                lineage.append({'parent': 'A' if parent == 0 else 'B', 'bullet': i + 1})
    child = ('# E4 crossover child\n\nDerived from ' + paths[0] + ' and ' + paths[1] +
             '. One-task crossover fragment; not a promoted roster profile.\n\n## Core Principles\n\n' +
             principles + '\n\n## Methodology\n\n' + methodology + '\n\n## Anti-Patterns\n\n' +
             '\n\n'.join(interleaved) + '\n')
    return canonical_json({'tool': 'breed', 'entrant': 'E4', 'scope': 'crossover-only',
        'parents': dict(zip(('A', 'B'), paths)),
        'parent_sha256': {p: sha256_file(root / p) for p in paths}, 'seed': seed,
        'anti_pattern_order': lineage, 'child': child,
        'limitations': ['no point mutation', 'no child scoring', 'no promotion or death history']})
