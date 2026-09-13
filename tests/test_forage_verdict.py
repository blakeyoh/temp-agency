"""Host tests for strict enforcement of supplied independent deletion judgments."""
import copy

import pytest

from lib.forage_verdict import evaluate

ARTIFACT = 'The airport uses a reserve runway when the main approach is unavailable.'


def inputs(count=3):
    candidate = {'schema_version': 1, 'items': [
        {'id': 'i' + str(i), 'text': 'Switch pickup to the reserve area when the main alley is blocked.'}
        for i in range(count)]}
    evaluation = {'schema_version': 1, 'verdicts': [
        {'item_id': item['id'], 'decision': 'dependent', 'proposal_quote': item['text'],
         'artifact_quote': ARTIFACT, 'deletion_effect': 'Removing the reserve mechanism loses the fallback operating rule.',
         'reason': 'The quoted source mechanism supports a concrete alternate operating route.'}
        for item in candidate['items']]}
    return candidate, evaluation


def test_three_survivors_required_and_rejected_items_never_retained():
    candidate, evaluation = inputs()
    assert evaluate(candidate, evaluation, ARTIFACT)['passed']
    candidate, evaluation = inputs(2)
    assert not evaluate(candidate, evaluation, ARTIFACT)['passed']
    candidate, evaluation = inputs(4)
    evaluation['verdicts'][3]['decision'] = 'unchanged'
    result = evaluate(candidate, evaluation, ARTIFACT)
    assert len(result['survivors']) == 3
    assert result['rejected'] == ['i3'] and not result['passed']


@pytest.mark.parametrize('mutation', ['missing', 'duplicate', 'order', 'quote', 'reason', 'decision_type', 'bool_schema'])
def test_malformed_or_fabricated_evidence_is_not_a_verdict(mutation):
    candidate, evaluation = inputs()
    if mutation == 'missing': evaluation['verdicts'].pop()
    elif mutation == 'duplicate': evaluation['verdicts'][1] = copy.deepcopy(evaluation['verdicts'][0])
    elif mutation == 'order': evaluation['verdicts'].reverse()
    elif mutation == 'quote': evaluation['verdicts'][0]['artifact_quote'] = 'A fabricated source mechanism.'
    elif mutation == 'reason': evaluation['verdicts'][0]['reason'] = ' ' * 30
    elif mutation == 'decision_type': evaluation['verdicts'][0]['decision'] = []
    else: candidate['schema_version'] = True
    with pytest.raises(ValueError):
        evaluate(candidate, evaluation, ARTIFACT)


def test_uncertain_item_requires_regeneration():
    candidate, evaluation = inputs()
    evaluation['verdicts'][0]['decision'] = 'indeterminate'
    evaluation['verdicts'][0]['artifact_quote'] = ''
    result = evaluate(candidate, evaluation, ARTIFACT)
    assert not result['passed'] and result['rejected'] == ['i0']
