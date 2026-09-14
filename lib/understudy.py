"""A6 degradation card: the frozen three-operator misapplication of a parent's own method."""
import json
import random
import re

from lib.breed import section
from lib.paths import canonical_json, relative_to_root

PHASE = re.compile(r'^### Phase (\d+):[ \t]*(.+?)\s*$', re.M)
CONSEQUENCE_KEYS = ('phase_order', 'principle', 'technique')


def phase_titles(methodology):
    found = PHASE.findall(methodology)
    numbers = [int(number) for number, _ in found]
    if len(found) < 2:
        raise ValueError('Methodology requires at least two numbered phases')
    if numbers != list(range(1, len(numbers) + 1)):
        raise ValueError('Methodology phases must be numbered 1..N in order')
    return [title for _, title in found]


def principle_bullets(text):
    block = section(text, 'Core Principles')
    starts = list(re.finditer(r'^- ', block, re.M))
    if not starts or block[:starts[0].start()].strip():
        raise ValueError('Core Principles must be bullet blocks')
    items = [block[start.start():(starts[i + 1].start() if i + 1 < len(starts) else len(block))].strip()
             for i, start in enumerate(starts)]
    if len(items) < 2:
        raise ValueError('Core Principles require at least two bullets')
    return items


def degraded_order(rng, count):
    canonical = list(range(1, count + 1))
    for _ in range(1000):
        draw = rng.sample(canonical, count)
        if draw != canonical and draw[0] != 1:
            return draw
    raise ValueError('no degraded phase order is available for this methodology')


def render(root, parent_path, config_path, seed):
    parent = relative_to_root(root, root / parent_path)
    config_rel = relative_to_root(root, root / config_path)
    config = json.loads((root / config_rel).read_text(encoding='utf-8'))
    if relative_to_root(root, root / config['parent']) != parent:
        raise ValueError('recipe names a different parent profile')
    text = (root / parent).read_text(encoding='utf-8')
    titles = phase_titles(section(text, 'Methodology'))
    bullets = principle_bullets(text)
    true_principle = config['true_principle']
    if true_principle not in text:
        raise ValueError('true_principle is not verbatim in the parent profile')
    remaining = [bullet for bullet in bullets if true_principle not in bullet]
    if len(remaining) == len(bullets):
        raise ValueError('true_principle does not match a Core Principle bullet')
    if not remaining:
        raise ValueError('no alternative Core Principle is available to misidentify')
    techniques = config['signature_techniques']
    if not techniques:
        raise ValueError('recipe requires at least one signature technique')
    for technique in techniques:
        if technique not in text:
            raise ValueError('signature technique is not verbatim in the parent profile')
    consequences = config['consequences']
    if set(consequences) != set(CONSEQUENCE_KEYS) or not all(consequences[key] for key in CONSEQUENCE_KEYS):
        raise ValueError('recipe requires one output consequence per degradation operator')
    rng = random.Random(seed['value'])
    order = degraded_order(rng, len(titles))
    return canonical_json({
        'parent': parent,
        'phase_order': order,
        'phase_titles': [titles[number - 1] for number in order],
        'overused_technique': rng.choice(techniques),
        'false_principle': rng.choice(remaining),
        'true_principle': true_principle,
        'consequences': {key: consequences[key] for key in CONSEQUENCE_KEYS},
    })
