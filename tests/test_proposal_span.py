"""Trace labels must not substitute for the delivered proposal's labels."""
from lib.bindings.draw import _item_line
from lib.bindings.proposal import proposal_lines
from lib.bindings.seed_string import _check_item_labels


def test_official_proposal_overrides_trace_and_legacy_openers():
    text = ('## Execution trace\n1. **correct:** evidence\n'
            '## Openers\n1. **correct:** old draft\n'
            '## Pass 1 proposal artifact\n1. **wrong:** final\n')
    assert _item_line(text, 1) == '1. **wrong:** final'
    assert not _check_item_labels(['s'], {'s': [(0, 0)]}, ['correct'], text).passed


def test_trace_only_and_duplicate_proposals_fail_closed():
    assert _item_line('## Execution trace\n1. label', 1) is None
    assert not proposal_lines('## Pass 1 proposal artifact\n1. good\n'
                              '## Pass 1 proposal artifact\n1. bad')
