"""bin/ tool lifecycle through lib.tools: schema, refusals, failure receipts, replay mode."""
from __future__ import annotations

from lib.paths import sha256_bytes
from lib.receipt import ALL_FIELDS

from conftest import INPUT_PATH, INPUT_TEXT


def test_run_issues_receipt_with_full_schema(repo):
    proc = repo.tool("--entrant", "E1", "--input", INPUT_PATH, "--upper")
    assert proc.returncode == 0, proc.stderr
    receipt = repo.receipt()
    assert set(receipt) == set(ALL_FIELDS)
    assert receipt["status"] == "ok" and receipt["error"] is None
    assert receipt["entrant"] == "E1" and receipt["tool"] == "echo-tool"
    assert receipt["seed"]["source"] == "os-entropy"
    assert receipt["output"] == proc.stdout
    assert receipt["output"].endswith(INPUT_TEXT.upper())
    assert receipt["output_sha256"] == sha256_bytes(proc.stdout.encode())
    assert receipt["inputs"] == {INPUT_PATH: sha256_bytes(INPUT_TEXT.encode())}
    assert receipt["argv"] == ["--entrant", "E1", "--input", INPUT_PATH, "--upper"]
    assert receipt["repo_commit"] == repo.git("rev-parse", "HEAD").strip()
    assert "receipt: " in proc.stderr


def test_seed_argument_is_recorded_as_argument_source(repo):
    proc = repo.tool("--entrant", "E1", "--text", "x", "--seed", "42")
    assert proc.returncode == 0, proc.stderr
    assert repo.receipt()["seed"] == {"value": 42, "source": "argument"}
    assert proc.stdout.startswith("seed=42\n")


def test_dirty_bin_refuses_and_writes_nothing(repo):
    repo.write("bin/scratch.txt", "uncommitted")
    proc = repo.tool("--entrant", "E1", "--text", "x")
    assert proc.returncode == 1
    assert "working tree is dirty under: bin/scratch.txt" in proc.stderr
    assert repo.receipts() == []
    assert not (repo.root / "docs/tournament/receipts/.nonce").exists()


def test_uncommitted_input_refuses(repo):
    repo.write("docs/tournament/inputs/new.txt", "fresh")
    proc = repo.tool("--entrant", "E1", "--input", "docs/tournament/inputs/new.txt")
    assert proc.returncode == 1
    assert "not committed at HEAD" in proc.stderr or "dirty" in proc.stderr
    assert repo.receipts() == []


def test_missing_entrant_refuses(repo):
    proc = repo.tool("--text", "x")
    assert proc.returncode == 1 and "--entrant is required" in proc.stderr
    assert repo.receipts() == []


def test_failed_produce_writes_failed_receipt(repo):
    proc = repo.tool("--entrant", "E1", "--text", "x", "--fail")
    assert proc.returncode == 1
    assert "RuntimeError: forced failure" in proc.stderr
    receipt = repo.receipt()
    assert receipt["status"] == "failed" and receipt["output"] == ""
    assert "forced failure" in receipt["error"]
    assert proc.stdout == ""


def test_replay_mode_writes_no_receipt_and_no_nonce(repo):
    original = repo.tool("--entrant", "E1", "--text", "x")
    path = repo.receipts()[0]
    replay = repo.tool("--replay-of", str(path), "--text", "ignored", "--entrant", "E9")
    assert replay.returncode == 0, replay.stderr
    assert replay.stdout == original.stdout
    assert len(repo.receipts()) == 1
    assert not (repo.root / "docs/tournament/receipts/.nonce").exists()
