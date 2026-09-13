"""E3 deterministic lowest keyword-overlap routing over the complete built roster."""
import re
import unicodedata
from fractions import Fraction

from lib.paths import canonical_json, relative_to_root

STOP = frozenset('a an and are as at be by for from has have how i in is it its of on or that the their this to was we what when which who will with you your'.split())


def tokens(text):
    return set(re.findall(r'[a-z0-9]+', unicodedata.normalize('NFKC', text).casefold())) - STOP


def profile_paths(root):
    return sorted(relative_to_root(root, p) for p in (root / 'roster').glob('*.md') if p.name != 'TEMPLATE.md')


def inputs(root, brief, index):
    return [relative_to_root(root, root / brief), relative_to_root(root, root / index)] + profile_paths(root)


def render(root, brief, index, domain_specialist):
    paths = profile_paths(root)
    if len(paths) < 2:
        raise ValueError('routing needs at least two built specialists')
    slugs = [p.split('/')[-1][:-3] for p in paths]
    index_text = (root / index).read_text(encoding='utf-8')
    indexed = re.findall(r'^\|\s*`([a-z0-9-]+)`\s*\|[^\n]*✓ Built', index_text, re.M)
    if len(indexed) != len(set(indexed)) or set(indexed) != set(slugs):
        raise ValueError('built roster index must exactly match actual profile corpus')
    if domain_specialist not in slugs:
        raise ValueError('domain-appropriate specialist must be a real indexed profile')
    brief_tokens = tokens((root / brief).read_text(encoding='utf-8'))
    if not brief_tokens:
        raise ValueError('task has no usable keywords')
    ranked = []
    for path, slug in zip(paths, slugs):
        words = tokens((root / path).read_text(encoding='utf-8'))
        if not words:
            raise ValueError('empty profile keyword set: ' + slug)
        common = sorted(brief_tokens & words)
        union = len(brief_tokens | words)
        ranked.append((Fraction(len(common), union), slug, common, union))
    ranked.sort(key=lambda row: (row[0], row[1]))
    lead = next(row[1] for row in ranked if row[1] != domain_specialist)
    return canonical_json({'tool': 'route', 'entrant': 'E3', 'brief': relative_to_root(root, root / brief),
        'index': relative_to_root(root, root / index), 'profiles': paths,
        'metric': 'unique ASCII word-token Jaccard overlap after NFKC and frozen stopwords',
        'tie_break': 'slug ascending', 'lead': lead, 'lens': domain_specialist,
        'domain_specialist_source': 'orchestrator-supplied; not independently classified',
        'scores': [{'slug': slug, 'intersection': len(common), 'union': union,
                    'shared_tokens': common, 'eligible_for_lead': slug != domain_specialist}
                   for score, slug, common, union in ranked],
        'bound_span': 'lowest lexical overlap among non-lens profiles; not semantic distance or frame dependence'})
