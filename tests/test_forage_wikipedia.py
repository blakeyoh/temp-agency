"""Host verification of GLM's live-source adapter; no real network in unit tests."""
import copy
import json

import pytest

from lib import forage_wikipedia as wiki

ENDPOINT = 'https://en.wikipedia.org/w/api.php'
DATE = 'Sun, 13 Sep 2026 12:00:00 GMT'
COMPLETED = '2026-09-13T12:00:01+00:00'


def payload():
    return {'query': {'pages': [{'pageid': 4, 'ns': 0, 'title': 'Fixture article',
        'revisions': [{'revid': 42, 'timestamp': '2026-01-01T01:00:00Z',
                      'slots': {'main': {'content': 'Exact source text.\r\nSecond line.'}}}]}]}}


@pytest.fixture
def network(monkeypatch):
    calls = []
    def get(url):
        calls.append(url)
        return json.dumps(payload()).encode(), {'Date': DATE}
    monkeypatch.setattr(wiki, '_http_get', get)
    return calls


def test_random_then_independent_exact_revision_lookup(network):
    artifact = wiki.fetch_random(ENDPOINT)
    assert artifact['content'] == 'Exact source text.\r\nSecond line.'
    assert wiki.verify_remote(artifact, COMPLETED) == []
    assert 'generator=random' in network[0]
    assert 'revids=42' in network[1] and 'generator=random' not in network[1]


@pytest.mark.parametrize('field,value', [('content', 'Invented source'), ('revid', 99),
    ('pageid', 99), ('content_sha256', '0'*64), ('revision_url', 'https://example.invalid'),
    ('revision_timestamp', '2027-01-01T00:00:00Z'), ('response_date', 'Mon, 14 Sep 2026 12:00:00 GMT')])
def test_forged_claims_fail(network, field, value):
    artifact = wiki.fetch_random(ENDPOINT)
    artifact[field] = value
    assert wiki.verify_remote(artifact, COMPLETED)


def test_network_failure_never_authenticates(network, monkeypatch):
    artifact = wiki.fetch_random(ENDPOINT)
    def broken(url):
        raise TimeoutError('read timed out')
    monkeypatch.setattr(wiki, '_http_get', broken)
    assert wiki.verify_remote(artifact, COMPLETED)
    with pytest.raises(ValueError):
        wiki.fetch_random(ENDPOINT)


def test_redirect_is_rejected_before_following():
    handler = wiki._NoRedirect()
    with pytest.raises(ValueError, match='redirects'):
        handler.redirect_request(None, None, 302, '', {}, 'https://unapproved.example/')


@pytest.mark.parametrize('kind', ['bool_id', 'suppressed', 'multiple_pages', 'missing_revision'])
def test_bad_api_payloads_rejected(monkeypatch, kind):
    value = payload()
    page = value['query']['pages'][0]
    if kind == 'bool_id': page['pageid'] = True
    elif kind == 'suppressed': page['revisions'][0]['texthidden'] = ''
    elif kind == 'multiple_pages': value['query']['pages'].append(copy.deepcopy(page))
    else: page['revisions'] = []
    monkeypatch.setattr(wiki, '_http_get', lambda url: (json.dumps(value).encode(), {'Date': DATE}))
    with pytest.raises(ValueError):
        wiki.fetch_random(ENDPOINT)


def test_non_allowlisted_endpoint_never_requests(network):
    with pytest.raises(ValueError):
        wiki.fetch_random('https://other.example/w/api.php')
    assert network == []
