"""bin/draw: the scrimmage regression, the receipt lifecycle, and the binding rule."""
from __future__ import annotations

import json
from pathlib import Path

from lib.bindings.draw import drawn_labels, parse_output
from lib.paths import sha256_file

REPO_ROOT = Path(__file__).resolve().parents[1]
POOLS = "docs/tournament/harness-fixtures/e1-pools-scrimmage.json"
POOLS_TEXT = (REPO_ROOT / POOLS).read_text(encoding="utf-8")
RECORDS = "docs/tournament/official-runs"
SCRIMMAGE = {
    "angle": [0, 3, 7, 1, 0, 8, 9, 4, 8, 5],
    "register": [0, 0, 1, 2, 2, 2, 2, 1, 2, 2],
    "device": [2, 2, 0, 2, 1, 0, 2, 0, 0, 2],
}
PROSE = "Opened on that thread and asked how the run went."
OTHER_PROSE = "Different opening entirely: named the object between us, flatly."


def with_pools(repo):
    repo.write(POOLS, POOLS_TEXT)
    repo.commit_all("add pools")
    return repo


def draw(repo, *args):
    return repo.run("bin/draw", *args)


def make(repo, *args):
    proc = draw(repo, "--entrant", "E1", "--pools", POOLS, *args)
    assert proc.returncode == 0, proc.stderr
    return proc, repo.receipt(), repo.receipts()[-1]


def item_lines(parsed, swap=None):
    lines = []
    for item in range(1, parsed["draws"] + 1):
        labels = list(drawn_labels(parsed, item))
        if swap and swap[0] == item:
            labels[0] = swap[1]
        lines.append('%d. **%s:** "%s"' % (item, " / ".join(labels), PROSE))
    return "\n".join(lines)


def build_record(entrant, ids, body, extra=""):
    bullets = "\n".join("- %s draw primary" % rid for rid in ids)
    return (
        "# Sweet 16 Official Source Record — %s\n\n## Provenance\n\n"
        "- **Entrant code:** %s\n\n## Execution trace\n\n%s\n\n%s## Receipts\n\n%s\n"
        % (entrant, entrant, body, extra, bullets)
    )


def counterfactual(item, labels, original=PROSE, replayed=OTHER_PROSE):
    return (
        "## Counterfactual replay\n\nItem: %d\nOriginal: %s\nReplayed: %s\n"
        "Replayed labels: %s\n\n" % (item, original, replayed, " / ".join(labels))
    )


def test_scrimmage_regression(repo):
    with_pools(repo)
    proc, _receipt, _path = make(repo, "--seed", "20260830")
    parsed = parse_output(proc.stdout)
    assert parsed["seed"] == 20260830 and parsed["source"] == "argument"
    assert parsed["draws"] == 10
    assert [name for name, _ in parsed["pools"]] == ["angle", "register", "device"]
    assert parsed["indices"] == SCRIMMAGE
    assert proc.stdout.endswith("]\n") and proc.stdout.count("\nDRAW ") == 0


def test_seed_source_and_recorded_inputs(repo):
    with_pools(repo)
    proc, receipt, _path = make(repo)
    assert receipt["seed"]["source"] == "os-entropy"
    assert receipt["output"] == proc.stdout
    assert receipt["inputs"] == {POOLS: sha256_file(repo.root / POOLS)}
    assert "receipt: " in proc.stderr
    seeded, receipt2, _p2 = make(repo, "--seed", "7")
    assert receipt2["seed"] == {"value": 7, "source": "argument"}
    assert "source=argument" in seeded.stdout


def test_verify_replay_passes_then_fails_on_edited_seed(repo):
    with_pools(repo)
    _proc, _receipt, path = make(repo, "--seed", "20260830")
    assert repo.verify("replay", str(path)).returncode == 0
    data = json.loads(path.read_text())
    data["seed"] = {**data["seed"], "value": 99}
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    assert repo.verify("replay", str(path)).returncode == 1


def test_replay_mode_writes_nothing(repo):
    with_pools(repo)
    proc, _receipt, path = make(repo, "--seed", "20260830")
    before = list(repo.receipts())
    replayed = draw(repo, "--replay-of", str(path))
    assert replayed.returncode == 0, replayed.stderr
    assert replayed.stdout == proc.stdout and "receipt:" not in replayed.stderr
    assert list(repo.receipts()) == before
    assert not (repo.root / "docs/tournament/receipts/.nonce").exists()


def test_uncommitted_pools_file_refuses(repo):
    repo.write(POOLS, POOLS_TEXT)
    dirty = draw(repo, "--entrant", "E1", "--pools", POOLS, "--seed", "1")
    assert dirty.returncode == 1 and "working tree is dirty" in dirty.stderr
    assert repo.receipts() == []
    repo.commit_all("add pools")
    assert draw(repo, "--entrant", "E1", "--pools", POOLS, "--seed", "1").returncode == 0
    assert repo.receipt()["status"] == "ok"


def test_bad_pools_schema_fails_with_receipt(repo):
    repo.write(POOLS, json.dumps({"draws": 0, "pools": []}))
    repo.commit_all("bad pools")
    proc = draw(repo, "--entrant", "E1", "--pools", POOLS, "--seed", "1")
    assert proc.returncode == 1 and "ValueError" in proc.stderr
    assert repo.receipt()["status"] == "failed"


def test_bind_passes_on_a_derived_record(repo):
    with_pools(repo)
    proc, receipt, path = make(repo, "--seed", "20260830")
    parsed = parse_output(proc.stdout)
    body = proc.stdout.strip() + "\n\n" + item_lines(parsed)
    record = repo.write(f"{RECORDS}/s16-e1.md",
                        build_record("E1", [receipt["receipt_id"]], body))
    result = repo.verify("bind", str(record), str(path))
    assert result.returncode == 0, result.stdout
    sidecar = json.loads(path.with_name(path.name[:-5] + ".bind.json").read_text())
    assert sidecar["result"] == "pass"
    assert [c["name"] for c in sidecar["checks"]] == [
        "header_verbatim", "item_labels", "counterfactual"]
    assert sidecar["checks"][2]["found"] == "not applicable (single draw receipt)"


def test_bind_fails_on_mislabeled_item(repo):
    with_pools(repo)
    proc, receipt, path = make(repo, "--seed", "20260830")
    parsed = parse_output(proc.stdout)
    body = proc.stdout.strip() + "\n\n" + item_lines(parsed, swap=(3, "logistics"))
    record = repo.write(f"{RECORDS}/s16-e1.md",
                        build_record("E1", [receipt["receipt_id"]], body))
    result = repo.verify("bind", str(record), str(path))
    assert result.returncode == 1
    assert "FAIL item_labels" in result.stdout and "item 3: missing favor-ask" in result.stdout


def test_bind_fails_without_the_header(repo):
    with_pools(repo)
    proc, receipt, path = make(repo, "--seed", "20260830")
    body = "we drew ten openers from the committed pools\n\n" + item_lines(
        parse_output(proc.stdout))
    record = repo.write(f"{RECORDS}/s16-e1.md",
                        build_record("E1", [receipt["receipt_id"]], body))
    result = repo.verify("bind", str(record), str(path))
    assert result.returncode == 1 and "FAIL header_verbatim" in result.stdout


def two_draws(repo):
    with_pools(repo)
    first, primary, primary_path = make(repo, "--seed", "20260830")
    second, other, other_path = make(repo, "--seed", "20260831")
    return (first, primary, primary_path), (second, other, other_path)


def counterfactual_record(repo, labels=None, original=PROSE, replayed=OTHER_PROSE):
    (first, primary, primary_path), (second, other, other_path) = two_draws(repo)
    parsed, alt = parse_output(first.stdout), parse_output(second.stdout)
    body = first.stdout.strip() + "\n\n" + second.stdout.strip() + "\n\n" + item_lines(parsed)
    section = counterfactual(1, labels or drawn_labels(alt, 1), original, replayed)
    text = build_record("E1", [primary["receipt_id"], other["receipt_id"]], body, section)
    record = repo.write(f"{RECORDS}/s16-e1.md", text)
    return record, primary_path, other_path


def test_counterfactual_binds_both_receipts(repo):
    record, primary_path, other_path = counterfactual_record(repo)
    assert repo.verify("bind", str(record), str(primary_path)).returncode == 0
    result = repo.verify("bind", str(record), str(other_path))
    assert result.returncode == 0, result.stdout
    sidecar = json.loads(other_path.with_name(other_path.name[:-5] + ".bind.json").read_text())
    assert sidecar["checks"][1]["found"] == "not applicable (counterfactual receipt)"
    assert sidecar["checks"][2]["pass"] is True


def test_counterfactual_fails_when_prose_is_unchanged(repo):
    record, _primary, other_path = counterfactual_record(repo, replayed=PROSE)
    result = repo.verify("bind", str(record), str(other_path))
    assert result.returncode == 1 and "similarity" in result.stdout


def test_counterfactual_fails_on_wrong_labels(repo):
    record, _primary, other_path = counterfactual_record(
        repo, labels=["logistics", "formal", "statement"])
    result = repo.verify("bind", str(record), str(other_path))
    assert result.returncode == 1 and "replayed labels" in result.stdout


def test_counterfactual_fails_when_original_is_not_item_line(repo):
    record, _primary, other_path = counterfactual_record(
        repo, original="a sentence that appears nowhere in the item lines")
    result = repo.verify("bind", str(record), str(other_path))
    assert result.returncode == 1 and "Original does not match item 1" in result.stdout


def test_verify_all_passes_on_the_honest_record(repo):
    counterfactual_record(repo)
    proc = repo.verify("all", "--records", f"{RECORDS}/s16-*.md")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS chain E1: intact" in proc.stdout and "PASS 2 receipts" in proc.stdout
