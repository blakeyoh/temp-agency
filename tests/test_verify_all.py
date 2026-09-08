"""bin/verify all: the gate over chains, replay, single-use citation, and sidecars."""
from __future__ import annotations

import json

from lib.paths import sha256_file


def issue_one(repo, entrant="E1", text="gate text"):
    proc = repo.tool("--entrant", entrant, "--text", text)
    assert proc.returncode == 0, proc.stderr
    return repo.receipt(entrant), repo.receipts(entrant)[-1]


def sidecar_of(path):
    return json.loads(path.with_name(path.name[:-5] + ".bind.json").read_text())


def test_no_receipts_passes(repo):
    proc = repo.verify("all")
    assert proc.returncode == 0 and "PASS 0 receipts" in proc.stdout


def test_cited_once_passes_and_writes_sidecar(repo):
    receipt, path = issue_one(repo)
    record = repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS chain E1: intact" in proc.stdout
    assert "PASS 1 receipts" in proc.stdout
    row = [line for line in proc.stdout.splitlines() if line.startswith(receipt["receipt_id"])]
    assert row and row[0].split() == [
        receipt["receipt_id"], "E1", "echo-tool", "replay-exact", "pass", "pass", "pass", "unattested"]
    assert "WARN" in proc.stdout and "unattested seed (no dispatch log)" in proc.stdout
    assert sidecar_of(path)["artifact_sha256"] == sha256_file(record)


def test_uncited_receipt_fails(repo):
    receipt, _ = issue_one(repo)
    proc = repo.verify("all")
    assert proc.returncode == 1
    assert "uncited receipt" in proc.stdout and "FAIL 1 receipts" in proc.stdout


def test_receipt_cited_by_two_records_fails(repo):
    receipt, _ = issue_one(repo)
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    repo.write_record("s16-e2.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all")
    assert proc.returncode == 1 and "receipt cited by multiple records" in proc.stdout


def test_entrant_code_mismatch_fails(repo):
    receipt, _ = issue_one(repo)
    repo.write_record("s16-e1.md", "E2", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all")
    assert proc.returncode == 1 and "entrant code 'E2' != receipt entrant 'E1'" in proc.stdout


def test_stale_sidecar_is_regenerated(repo):
    receipt, path = issue_one(repo)
    record = repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    assert repo.verify("all").returncode == 0
    old_hash = sidecar_of(path)["artifact_sha256"]
    record.write_text(record.read_text() + "\nedited after bind\n")
    assert repo.verify("all").returncode == 0
    assert sidecar_of(path)["artifact_sha256"] == sha256_file(record) != old_hash
    record.write_text(record.read_text().replace(receipt["output"], "gestured at"))
    proc = repo.verify("all")
    assert proc.returncode == 1 and sidecar_of(path)["result"] == "fail"


def test_current_sidecar_is_not_rewritten(repo):
    receipt, path = issue_one(repo)
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    assert repo.verify("all").returncode == 0
    before = path.with_name(path.name[:-5] + ".bind.json").read_bytes()
    proc = repo.verify("all")
    assert proc.returncode == 0 and "current)" in proc.stdout
    assert path.with_name(path.name[:-5] + ".bind.json").read_bytes() == before


def test_failed_receipt_is_not_a_replay_failure(repo):
    proc = repo.tool("--entrant", "E1", "--text", "x", "--fail")
    assert proc.returncode == 1
    receipt = repo.receipt()
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], "NOT ENACTED")
    proc = repo.verify("all")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "failed receipt (not replayable)" in proc.stdout
    assert "n/a (failed)" in proc.stdout


def test_hash_attested_without_attestation_fails(repo):
    receipt, path = issue_one(repo)
    edited = {**receipt, "verification_class": "hash-attested"}
    path.write_text(json.dumps(edited, indent=2, sort_keys=True))
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all")
    assert proc.returncode == 1
    assert "lacks external_attestation" in proc.stdout
    assert "does not recompute" in proc.stdout


def test_records_glob_override_and_tampered_chain(repo):
    receipt, path = issue_one(repo)
    repo.write_record("run-e1.md", "E1", [receipt["receipt_id"]], receipt["output"],
                      directory="docs/tournament/scratch")
    assert repo.verify("all").returncode == 1
    proc = repo.verify("all", "--records", "docs/tournament/scratch/run-*.md")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    tampered = {**receipt, "output": receipt["output"] + "!"}
    path.write_text(json.dumps(tampered, indent=2, sort_keys=True))
    proc = repo.verify("all", "--records", "docs/tournament/scratch/run-*.md")
    assert proc.returncode == 1 and "FAIL chain E1" in proc.stdout


LOG_PATH = "docs/tournament/official-runs/dispatch-log.json"


def commit_log(repo, entries, path=LOG_PATH):
    repo.write(path, json.dumps({"entries": entries}, indent=2))
    repo.commit_all("dispatch log")


def entry(entrant, seed):
    return {"entrant": entrant, "seed": seed, "purpose": "test", "record": "s16-e1.md",
            "issued_utc": "2026-09-08T00:00:00Z"}


def test_seed_matching_committed_log_passes(repo):
    commit_log(repo, [entry("E1", 123), entry("E2", 999)])
    proc = repo.tool("--entrant", "E1", "--text", "x", "--seed", "123")
    assert proc.returncode == 0, proc.stderr
    receipt = repo.receipt()
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all", "--dispatch-log", LOG_PATH)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS dispatch log docs/tournament/official-runs/dispatch-log.json: committed and clean" in proc.stdout
    assert "seed 123 in dispatch log for E1" in proc.stdout
    row = [line for line in proc.stdout.splitlines() if line.startswith(receipt["receipt_id"])]
    assert row[0].split()[-1] == "pass"


def test_seed_absent_from_log_fails(repo):
    commit_log(repo, [entry("E1", 123), entry("E2", 456)])
    repo.tool("--entrant", "E1", "--text", "x", "--seed", "456")
    receipt = repo.receipt()
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all", "--dispatch-log", LOG_PATH)
    assert proc.returncode == 1 and "seed not in dispatch log" in proc.stdout


def test_os_entropy_seed_under_log_fails(repo):
    commit_log(repo, [entry("E1", 123)])
    repo.tool("--entrant", "E1", "--text", "x")
    receipt = repo.receipt()
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all", "--dispatch-log", LOG_PATH)
    assert proc.returncode == 1
    assert "seed source os-entropy is unattested under a dispatch log" in proc.stdout


def test_no_dispatch_log_warns_and_passes(repo):
    repo.tool("--entrant", "E1", "--text", "x")
    receipt = repo.receipt()
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARN E1/001-" in proc.stdout and "unattested seed (no dispatch log)" in proc.stdout
    assert proc.stdout.splitlines()[-2].split()[-1] == "unattested"


def test_argument_seed_without_log_shows_argument(repo):
    repo.tool("--entrant", "E1", "--text", "x", "--seed", "7")
    receipt = repo.receipt()
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all")
    assert proc.returncode == 0 and "WARN" not in proc.stdout
    assert proc.stdout.splitlines()[-2].split()[-1] == "argument"


def test_uncommitted_dispatch_log_fails(repo):
    commit_log(repo, [entry("E1", 123)])
    repo.tool("--entrant", "E1", "--text", "x", "--seed", "123")
    receipt = repo.receipt()
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    repo.write(LOG_PATH, json.dumps({"entries": [entry("E1", 123), entry("E1", 5)]}))
    proc = repo.verify("all", "--dispatch-log", LOG_PATH)
    assert proc.returncode == 1 and "FAIL dispatch log" in proc.stdout
    assert "working tree is dirty under" in proc.stdout
    repo.write("docs/tournament/official-runs/fresh-log.json", json.dumps({"entries": []}))
    proc = repo.verify("all", "--dispatch-log", "docs/tournament/official-runs/fresh-log.json")
    assert proc.returncode == 1 and "FAIL dispatch log" in proc.stdout
    assert "fresh-log.json" in proc.stdout


def test_missing_or_malformed_dispatch_log_fails(repo):
    repo.tool("--entrant", "E1", "--text", "x", "--seed", "1")
    receipt = repo.receipt()
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all", "--dispatch-log", "docs/tournament/official-runs/none.json")
    assert proc.returncode == 1 and "FAIL dispatch log" in proc.stdout
    repo.write(LOG_PATH, '{"entries": [{"entrant": "E1", "seed": "1"}]}')
    repo.commit_all("bad log")
    proc = repo.verify("all", "--dispatch-log", LOG_PATH)
    assert proc.returncode == 1 and "integer seed" in proc.stdout


def test_failed_receipt_seed_is_not_checked(repo):
    commit_log(repo, [entry("E1", 123)])
    repo.tool("--entrant", "E1", "--text", "x", "--fail")
    receipt = repo.receipt()
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], "NOT ENACTED")
    proc = repo.verify("all", "--dispatch-log", LOG_PATH)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.splitlines()[-2].split()[-1] == "n/a"
