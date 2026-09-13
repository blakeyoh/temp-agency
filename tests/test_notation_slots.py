"""Host tests for GLM's seven C5 forms, including defects found during review."""
import copy
import json
from pathlib import Path

import pytest

from lib.notation_slots import validate_artifact, validate_catalog

CATALOG = Path(__file__).resolve().parents[1] / 'docs/tournament/notation/catalog.json'
EXAMPLES = {
    'recipe': {'ingredients': [{'name': 'flour', 'quantity': 1, 'unit': 'cup'}], 'steps': ['Mix.']},
    'court-docket': {'issue': 'Noise', 'parties': ['A', 'B'], 'evidence': ['Log'],
                     'ruling': 'Adjust hours', 'remedies': ['Trial schedule']},
    'knitting-pattern': {'gauge': {'stitches_per_inch': 4, 'rows_per_inch': 6},
                         'stitches': ['knit'], 'repeat': 'twice', 'bind_off': 'loosely'},
    'chess-annotation': {'moves': [{'move': 'e4', 'countermove': 'e5', 'evaluation': 0.1}]},
    'liturgical-rubric': {'cues': [{'cue': 'bell', 'officiant': 'host', 'response': 'ready',
                                   'rubric': 'stand'}]},
    'flight-checklist': {'checks': [{'trigger': 'start', 'challenge': 'ready?',
                                    'expected_response': 'yes', 'verify': 'inspect', 'abort': 'stop'}]},
    'circuit-diagram': {'nodes': ['a', 'b'], 'connections': [{'from': 'a', 'to': 'b'}]},
}


def catalog():
    value = json.loads(CATALOG.read_text())
    value['item_count'] = 1
    return value


@pytest.mark.parametrize('name', list(EXAMPLES))
def test_all_forms_accept_valid_structure_and_reject_missing_slots(name):
    artifact = {'notation': name, 'items': [{'id': 'n1', **copy.deepcopy(EXAMPLES[name])}]}
    assert validate_artifact(artifact, catalog(), name) == []
    artifact['items'][0].pop(next(iter(EXAMPLES[name])))
    assert validate_artifact(artifact, catalog(), name)


@pytest.mark.parametrize('quantity', [True, 0, -1, float('nan'), float('inf')])
def test_recipe_rejects_invalid_quantity(quantity):
    item = {'id': 'n1', **copy.deepcopy(EXAMPLES['recipe'])}
    item['ingredients'][0]['quantity'] = quantity
    assert validate_artifact({'notation': 'recipe', 'items': [item]}, catalog(), 'recipe')


def test_duplicate_ids_and_unknown_graph_nodes():
    item = {'id': 'n1', **copy.deepcopy(EXAMPLES['circuit-diagram'])}
    item['connections'][0]['to'] = 'unknown'
    assert validate_artifact({'notation': 'circuit-diagram', 'items': [item]}, catalog(), 'circuit-diagram')
    value = catalog(); value['item_count'] = 2
    item = {'id': 'n1', **copy.deepcopy(EXAMPLES['recipe'])}
    assert any('duplicate' in p for p in validate_artifact(
        {'notation': 'recipe', 'items': [item, item]}, value, 'recipe'))


def test_catalog_cannot_disable_validation():
    value = catalog(); value['item_count'] = 0
    with pytest.raises(ValueError):
        validate_catalog(value)
    value = catalog(); value['notations'][0]['required_slots'] = []
    with pytest.raises(ValueError):
        validate_catalog(value)
