"""lib.receipt: nonce gate, chaining, immutability, citation parsing."""
from __future__ import annotations

import pytest

from lib.bindings import cited_receipt_ids
from lib.errors import ReceiptError
from lib.receipt import ALL_FIELDS, issue, list_receipts, mint_nonce, verify_chain


def sample_fields(**over):
    base = {
        "entrant": "E1", "tool": "echo-tool", "tool_sha256": "0" * 64,
        "repo_commit": "0" * 40, "python_version": "3.9.6", "argv": [],
        "inputs": {}, "input_sha256": "0" * 64,
        "seed": {"value": 1, "source": "argument"}, "output": "hi",
        "output_sha256": "0" * 64, "verification_class": "replay-exact",
        "external_attestation": None, "status": "ok", "error": None,
        "started_utc": "2026-01-01T00:00:00Z", "completed_utc": "2026-01-01T00:00:00Z",
    }
    return {**base, **over}


def test_issue_without_live_nonce_raises(repo):
    with pytest.raises(ReceiptError, match="no live nonce"):
        issue(repo.root, "not-minted", **sample_fields())
    assert repo.receipts() == []


def test_wrong_nonce_is_consumed_and_rejected(repo):
    mint_nonce(repo.root)
    with pytest.raises(ReceiptError, match="no live nonce"):
        issue(repo.root, "wrong", **sample_fields())
    assert not (repo.root / "docs/tournament/receipts/.nonce").exists()


def test_direct_issue_with_live_nonce_writes_receipt(repo):
    path = issue(repo.root, mint_nonce(repo.root), **sample_fields())
    assert path.exists()
    assert not (repo.root / "docs/tournament/receipts/.nonce").exists()
    assert set(repo.receipt()) == set(ALL_FIELDS)


def test_two_runs_chain(repo):
    assert repo.tool("--entrant", "E1", "--text", "one").returncode == 0
    assert repo.tool("--entrant", "E1", "--text", "two").returncode == 0
    first, second = repo.receipt(index=0), repo.receipt(index=1)
    assert first["chain_prev"] == "genesis"
    assert second["chain_prev"] == first["chain_hash"]
    assert verify_chain(repo.root, "E1") == []


def test_receipts_are_never_overwritten(repo):
    repo.tool("--entrant", "E1", "--text", "one")
    repo.tool("--entrant", "E1", "--text", "one")
    paths = list_receipts(repo.root, "E1")
    assert len(paths) == 2
    assert paths[0].name.startswith("001-") and paths[1].name.startswith("002-")
    assert paths[0].name != paths[1].name
    assert all(p.exists() for p in paths)


def test_chain_flags_receipt_in_wrong_entrant_dir(repo):
    repo.tool("--entrant", "E1", "--text", "one")
    path = repo.receipts()[0]
    moved = repo.root / "docs/tournament/receipts/E2" / path.name
    moved.parent.mkdir()
    moved.write_bytes(path.read_bytes())
    problems = verify_chain(repo.root, "E2")
    assert problems and "entrant" in problems[0]


def test_cited_receipt_ids_parses_receipts_section():
    text = (
        "## Provenance\n- abc\n## Receipts\n\n- 0123456789ab first\n"
        "- `fedcba987654`: second\n- not-a-receipt\n### Sub\n- 0123456789ab dup\n"
        "## Next\n- 111111111111 outside\n"
    )
    assert cited_receipt_ids(text) == ["0123456789ab", "fedcba987654"]
    assert cited_receipt_ids("# No receipts here\n- 0123456789ab\n") == []
