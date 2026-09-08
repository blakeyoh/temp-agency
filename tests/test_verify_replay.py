"""bin/verify replay and chain against untouched and tampered receipts."""
from __future__ import annotations

import json

from conftest import INPUT_PATH


def run_once(repo, *extra):
    proc = repo.tool("--entrant", "E1", "--input", INPUT_PATH, *extra)
    assert proc.returncode == 0, proc.stderr
    return repo.receipts()[-1]


def test_replay_passes_on_untouched_receipt(repo):
    path = run_once(repo)
    proc = repo.verify("replay", str(path))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS replay output byte-equal" in proc.stdout
    assert proc.stdout.rstrip().endswith(f"PASS replay {path.name}")


def test_edited_seed_fails_chain_and_replay(repo):
    path = run_once(repo)
    receipt = json.loads(path.read_text())
    receipt["seed"]["value"] = receipt["seed"]["value"] + 1
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True))
    chain = repo.verify("chain", "E1")
    assert chain.returncode == 1 and "does not recompute" in chain.stdout
    replay = repo.verify("replay", str(path))
    assert replay.returncode == 1
    assert "FAIL replay output differs" in replay.stdout


def test_input_changed_in_a_later_commit_still_replays(repo):
    """Replay reads `git archive <repo_commit>`, not the working tree.

    This reverses the old `test_modified_committed_input_fails_replay`. Editing the
    input after the receipt used to fail; it now passes, because the archive holds
    the input as it stood at `repo_commit`. The check that matters — the archived
    input's hash equals the receipt's — is unaffected by later commits.
    """
    path = run_once(repo)
    repo.write(INPUT_PATH, "changed after the receipt\n")
    repo.commit_all("change input")
    proc = repo.verify("replay", str(path))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS input pinned at" in proc.stdout and INPUT_PATH in proc.stdout
    assert "PASS replay output byte-equal to receipt output" in proc.stdout


def test_modified_tool_warns_and_replays_the_committed_version(repo):
    """A working-tree tool that has since changed is a WARN, not a FAIL."""
    path = run_once(repo)
    tool = repo.root / "bin/echo-tool"
    tool.write_text(tool.read_text() + "\n# touched\n")
    repo.commit_all("touch tool")
    proc = repo.verify("replay", str(path))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARN bin/echo-tool has changed since this receipt" in proc.stdout
    assert "replay ran the committed version" in proc.stdout
    assert "PASS replay output byte-equal to receipt output" in proc.stdout


def test_failed_receipt_is_reported_not_replayed(repo):
    repo.tool("--entrant", "E1", "--text", "x", "--fail")
    proc = repo.verify("replay", str(repo.receipts()[0]))
    assert proc.returncode == 0
    assert "failed receipt (not replayable)" in proc.stdout


def test_chain_passes_and_reports_problem_count(repo):
    run_once(repo)
    run_once(repo, "--upper")
    proc = repo.verify("chain", "E1")
    assert proc.returncode == 0 and proc.stdout.strip() == "PASS chain E1"


def test_hash_attested_receipt_is_not_replayed(repo):
    path = run_once(repo)
    edited = {**json.loads(path.read_text()), "verification_class": "hash-attested"}
    path.write_text(json.dumps(edited, indent=2, sort_keys=True))
    proc = repo.verify("replay", str(path))
    assert proc.returncode == 0 and "replay does not apply" in proc.stdout
