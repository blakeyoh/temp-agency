"""Tests for bin/seed-string and its binding rule (E9 — String Seed of Thought)."""
from __future__ import annotations

import json
import string
from typing import Dict, List

ENTRANT = "E9"


def _run(repo, *args: str):
    return repo.run("bin/seed-string", "--entrant", ENTRANT, *args)


def _items(stdout: str) -> List[str]:
    header, *lines = stdout.splitlines()
    return [line.split(": ", 1)[1] for line in lines]


# -- determinism, count/length/alphabet, os-entropy ------------------------


def test_same_seed_is_deterministic(repo):
    first = _run(repo, "--seed", "7")
    second = _run(repo, "--seed", "7")
    assert first.returncode == 0
    assert second.returncode == 0
    assert first.stdout == second.stdout


def test_different_seeds_differ(repo):
    first = _run(repo, "--seed", "1")
    second = _run(repo, "--seed", "2")
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout != second.stdout


def test_count_length_alphabet_are_honored(repo):
    proc = _run(repo, "--seed", "5", "--count", "4", "--length", "12", "--alphabet", "lower")
    assert proc.returncode == 0
    header = proc.stdout.splitlines()[0]
    assert "count=4" in header and "length=12" in header and "alphabet=lower" in header
    values = _items(proc.stdout)
    assert len(values) == 4
    for value in values:
        assert len(value) == 12
        assert all(c in string.ascii_lowercase for c in value)


def test_no_seed_draws_os_entropy_and_differs(repo):
    first = _run(repo)
    second = _run(repo)
    assert first.returncode == 0 and second.returncode == 0
    assert "source=os-entropy" in first.stdout.splitlines()[0]
    assert first.stdout != second.stdout


def test_invalid_count_fails_with_receipt(repo):
    proc = _run(repo, "--seed", "1", "--count", "0")
    assert proc.returncode == 1
    receipt = repo.receipt(ENTRANT)
    assert receipt["status"] == "failed"
    assert "ValueError" in receipt["error"]


# -- bin/verify replay -------------------------------------------------------


def test_verify_replay_passes_then_fails_on_tampered_seed(repo):
    proc = _run(repo, "--seed", "42")
    assert proc.returncode == 0
    receipt_path = repo.receipts(ENTRANT)[-1]

    ok = repo.verify("replay", str(receipt_path))
    assert ok.returncode == 0, ok.stdout + ok.stderr

    data = json.loads(receipt_path.read_text(encoding="utf-8"))
    tampered = {**data, "seed": {**data["seed"], "value": data["seed"]["value"] + 1}}
    receipt_path.write_text(json.dumps(tampered), encoding="utf-8")

    bad = repo.verify("replay", str(receipt_path))
    assert bad.returncode == 1


def test_replay_writes_no_receipt_and_no_nonce(repo):
    proc = _run(repo, "--seed", "9")
    assert proc.returncode == 0
    receipt_path = repo.receipts(ENTRANT)[-1]
    before = set(repo.receipts(ENTRANT))
    nonce_path = repo.root / "docs" / "tournament" / "receipts" / ".nonce"
    assert not nonce_path.exists()

    replay = repo.run("bin/seed-string", "--replay-of", str(receipt_path))
    assert replay.returncode == 0
    assert replay.stdout == proc.stdout
    assert set(repo.receipts(ENTRANT)) == before
    assert not nonce_path.exists()


# -- binding rule fixtures ----------------------------------------------------

POOL = [
    "food or drinks station",
    "most recent or upcoming session",
    "shared physical environment",
    "role or company, asked with curiosity",
    "name and origin story",
    "weather or travel logistics",
    "badge or lanyard detail",
    "shared line or queue",
    "nervous icebreaker admission",
    "compliment about the venue",
]


def _pool_section() -> str:
    body = "\n".join(f"- {i}: {label}" for i, label in enumerate(POOL))
    return f"## Angle pool\n\n{body}\n"


def _derivation(strings: List[str]) -> Dict[str, int]:
    return {s: sum(ord(c) for c in s) % len(POOL) for s in strings}


def _derivation_table(strings: List[str], index_by_string: Dict[str, int]) -> str:
    header = "| String | Sum | Index | Angle |\n|---|---|---|---|"
    rows = []
    for s in strings:
        total = sum(ord(c) for c in s)
        index = index_by_string[s]
        rows = rows + [f"| `{s}` | {total} | {index} | {POOL[index]} |"]
    return header + "\n" + "\n".join(rows) + "\n"


def _item_lines(strings: List[str], index_by_string: Dict[str, int]) -> str:
    lines = []
    for n, s in enumerate(strings, start=1):
        label = POOL[index_by_string[s]]
        lines = lines + [f'{n}. **{label}:** "Opener drawn for item {n}."']
    return "\n".join(lines) + "\n"


def _build_record(header_line: str, strings: List[str], index_by_string: Dict[str, int],
                  receipt_id: str) -> str:
    return (
        f"# Sweet 16 Official Source Record — {ENTRANT}\n\n"
        f"## Provenance\n\n- **Entrant code:** {ENTRANT}\n\n"
        f"## Mechanism output\n\n{header_line}\n\n"
        f"{_pool_section()}\n"
        f"## Derivation\n\n{_derivation_table(strings, index_by_string)}\n"
        f"## Openers\n\n{_item_lines(strings, index_by_string)}\n"
        f"## Receipts\n\n- {receipt_id} seed-string run\n"
    )


def _honest_fixture(repo, seed: str):
    proc = _run(repo, "--seed", seed)
    assert proc.returncode == 0
    header_line = proc.stdout.splitlines()[0]
    strings = _items(proc.stdout)
    receipt = repo.receipt(ENTRANT)
    receipt_path = repo.receipts(ENTRANT)[-1]
    index_by_string = _derivation(strings)
    record_text = _build_record(header_line, strings, index_by_string, receipt["receipt_id"])
    return record_text, strings, index_by_string, receipt_path


def test_binding_positive(repo):
    record_text, _, _, receipt_path = _honest_fixture(repo, "123")
    record_path = repo.write("docs/tournament/official-runs/s16-e9-honest.md", record_text)
    result = repo.verify("bind", str(record_path), str(receipt_path))
    assert result.returncode == 0, result.stdout + result.stderr


def test_unparseable_output_fails_every_check(repo):
    record_text, _, _, receipt_path = _honest_fixture(repo, "9")
    record_path = repo.write("docs/tournament/official-runs/s16-e9-garbled.md", record_text)
    receipt = json.loads(receipt_path.read_text())
    receipt_path.write_text(json.dumps({**receipt, "output": "not a header\n"}, indent=2))
    result = repo.verify("bind", str(record_path), str(receipt_path))
    assert result.returncode == 1 and result.stdout.count("unparseable output") == 4


def test_binding_negative_bad_sum(repo):
    record_text, strings, index_by_string, receipt_path = _honest_fixture(repo, "5")
    target = strings[0]
    correct_sum = sum(ord(c) for c in target)
    index = index_by_string[target]
    old_row = f"| `{target}` | {correct_sum} | {index} | {POOL[index]} |"
    new_row = f"| `{target}` | {correct_sum + 1} | {index} | {POOL[index]} |"
    assert old_row in record_text
    record_text = record_text.replace(old_row, new_row, 1)
    record_path = repo.write("docs/tournament/official-runs/s16-e9-bad-sum.md", record_text)
    result = repo.verify("bind", str(record_path), str(receipt_path))
    assert result.returncode == 1
    assert "FAIL derivation_rows" in result.stdout
    assert target in result.stdout


def test_binding_negative_wrong_item_label(repo):
    record_text, strings, index_by_string, receipt_path = _honest_fixture(repo, "17")
    index0 = index_by_string[strings[0]]
    wrong_label = next(label for i, label in enumerate(POOL) if i != index0)
    old_line = f'1. **{POOL[index0]}:**'
    new_line = f'1. **{wrong_label}:**'
    assert old_line in record_text
    record_text = record_text.replace(old_line, new_line, 1)
    record_path = repo.write("docs/tournament/official-runs/s16-e9-wrong-label.md", record_text)
    result = repo.verify("bind", str(record_path), str(receipt_path))
    assert result.returncode == 1
    assert "FAIL item_labels" in result.stdout
    assert "PASS derivation_rows" in result.stdout


def test_binding_negative_missing_string(repo):
    record_text, strings, _, receipt_path = _honest_fixture(repo, "77")
    missing = strings[3]
    record_text = "\n".join(
        line for line in record_text.splitlines() if f"`{missing}`" not in line
    ) + "\n"
    record_path = repo.write("docs/tournament/official-runs/s16-e9-missing.md", record_text)
    result = repo.verify("bind", str(record_path), str(receipt_path))
    assert result.returncode == 1
    assert "FAIL strings_verbatim" in result.stdout


def test_binding_negative_bad_index(repo):
    record_text, strings, index_by_string, receipt_path = _honest_fixture(repo, "99")
    target = strings[0]
    correct_sum = sum(ord(c) for c in target)
    correct_index = index_by_string[target]
    wrong_index = (correct_index + 1) % len(POOL)
    old_row = f"| `{target}` | {correct_sum} | {correct_index} | {POOL[correct_index]} |"
    new_row = f"| `{target}` | {correct_sum} | {wrong_index} | {POOL[correct_index]} |"
    assert old_row in record_text
    record_text = record_text.replace(old_row, new_row, 1)
    record_path = repo.write("docs/tournament/official-runs/s16-e9-bad-index.md", record_text)
    result = repo.verify("bind", str(record_path), str(receipt_path))
    assert result.returncode == 1
    assert "FAIL derivation_rows" in result.stdout


def test_verify_all_passes_with_honest_record(repo):
    record_text, _, _, _ = _honest_fixture(repo, "321")
    repo.write("docs/tournament/official-runs/s16-e9.md", record_text)
    result = repo.verify("all", "--records", "docs/tournament/official-runs/s16-*.md")
    assert result.returncode == 0, result.stdout + result.stderr
