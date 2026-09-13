"""E6 draws packs and cards from the complete committed positions corpus."""
from __future__ import annotations

import json
import random
import re

from lib.paths import canonical_json, relative_to_root, sha256_file

DEFAULT_DECK = 'docs/tournament/deck/cards.json'


def source_paths(root):
    paths = sorted(root.glob('knowledge/*/positions.md'))
    if any(path.is_symlink() or not path.is_file() for path in paths):
        raise ValueError('positions packs must be regular files')
    return [relative_to_root(root, path) for path in paths]


def input_paths(root, deck):
    return [relative_to_root(root, root / deck)] + source_paths(root)


def render(root, deck_path, pack_count, seed):
    deck_path = relative_to_root(root, root / deck_path)
    sources = source_paths(root)
    if not sources:
        raise ValueError('no real positions packs exist')
    deck = json.loads((root / deck_path).read_text(encoding='utf-8'))
    if (set(deck) != {'schema_version', 'discard_first', 'packs'}
            or type(deck['schema_version']) is not int or deck['schema_version'] != 1
            or type(deck['discard_first']) is not int or deck['discard_first'] != 10):
        raise ValueError('deck must use version 1 and discard the first ten cards')
    packs = deck['packs']
    if not isinstance(packs, list) or len(packs) != len(sources):
        raise ValueError('deck must cover every real positions pack')
    expected = [path.split('/')[1] for path in sources]
    if [pack.get('slug') for pack in packs] != expected:
        raise ValueError('deck packs must exactly match sorted real corpus; no missing or extra pack')
    for pack, path in zip(packs, sources):
        if set(pack) != {'slug', 'source_sha256', 'cards'} or not re.fullmatch('[a-z0-9-]+', pack['slug']):
            raise ValueError('invalid deck pack schema')
        if pack['source_sha256'] != sha256_file(root / path):
            raise ValueError('positions changed since distillation: ' + path)
        cards = pack['cards']
        if (not isinstance(cards, list) or len(cards) != 30
                or any(not isinstance(card, str) or not card.strip() or card != card.strip()
                       or '\n' in card or '\r' in card for card in cards)
                or len(set(cards)) != 30):
            raise ValueError('each pack requires thirty distinct one-line imperatives')
    if type(pack_count) is not int or not 1 <= pack_count <= len(packs):
        raise ValueError('pack count must fit the complete corpus')
    rng = random.Random(seed['value'])
    indices = rng.sample(range(len(packs)), pack_count)
    eligible = [(index, card_index) for index in indices for card_index in range(10, 30)]
    selected_index = rng.randrange(len(eligible))
    pack_index, card_index = eligible[selected_index]
    return canonical_json({'tool': 'oblique', 'entrant': 'E6', 'deck': deck_path,
        'deck_sha256': sha256_file(root / deck_path), 'sources': sources,
        'corpus_count': len(packs), 'corpus_slugs': expected, 'pack_count': pack_count,
        'selected_pack_indices': indices, 'selected_packs': [packs[i]['slug'] for i in indices],
        'eligible_card_count': len(eligible), 'selected_index': selected_index,
        'source_pack': packs[pack_index]['slug'], 'original_card_number': card_index + 1,
        'card': packs[pack_index]['cards'][card_index], 'seed': seed})
