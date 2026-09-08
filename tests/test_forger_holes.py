"""The four holes the Phase 1 forger used, closed (plan v4 section 11).

1. Replay ran against the working tree; argv was never compared to inputs.
2. A one-option pool draws index 0 whatever the generator returns.
3. Label binding was substring matching.
4. `hash-attested` accepted any non-empty attestation dict.

Plus the two hygiene rules the same reading produced: a receipts directory holds
nothing but receipts and sidecars, and the receipts directory is relocatable so
fixtures never write into the official round's tree.
"""
from __future__ import annotations

import json

from conftest import INPUT_PATH

OTHER_INPUT = "docs/tournament/inputs/second.txt"
POOLS = "docs/tournament/inputs/pools.json"
FIXTURE_RECEIPTS = "docs/tournament/harness-fixtures/receipts"


def echo_receipt(repo, *extra):
    proc = repo.tool("--entrant", "E1", "--input", INPUT_PATH, *extra)
    assert proc.returncode == 0, proc.stderr
    path = repo.receipts()[-1]
    return json.loads(path.read_text()), path


def rewrite(path, receipt, **changes):
    path.write_text(json.dumps({**receipt, **changes}, indent=2, sort_keys=True))


def write_pools(repo, options, name="angle", draws=2):
    spec = {"draws": draws, "pools": [{"name": name, "options": options}]}
    repo.write(POOLS, json.dumps(spec, indent=2))
    repo.commit_all("pools")
    return POOLS


# --- Hole 1: replay reads the archive, and argv may not name undeclared files ---

def test_argv_naming_an_uncommitted_file_fails_replay(repo):
    """(a) inputs pin the committed file; argv points at one the forger never committed."""
    receipt, path = echo_receipt(repo)
    repo.write("docs/tournament/inputs/forged.txt", "written by the agent, never committed\n")
    rewrite(path, receipt,
            argv=["--entrant", "E1", "--input", "docs/tournament/inputs/forged.txt"])
    proc = repo.verify("replay", str(path))
    assert proc.returncode == 1
    assert "forged.txt" in proc.stdout
    assert "undeclared file" in proc.stdout or "replay exited" in proc.stdout


def test_argv_naming_a_committed_but_undeclared_file_fails_replay(repo):
    """The same check when the file does exist at repo_commit: it is still undeclared."""
    repo.write(OTHER_INPUT, "a second committed file\n")
    repo.commit_all("second input")
    receipt, path = echo_receipt(repo)
    rewrite(path, receipt, argv=["--entrant", "E1", "--input", INPUT_PATH, "--note", OTHER_INPUT])
    proc = repo.verify("replay", str(path))
    assert proc.returncode == 1
    assert f"FAIL argv names an undeclared file: {OTHER_INPUT}" in proc.stdout


def test_run_tool_refuses_argv_naming_an_undeclared_file(repo):
    """(i) the tool itself refuses before it produces anything."""
    proc = repo.tool("--entrant", "E1", "--text", INPUT_PATH)
    assert proc.returncode == 1
    assert f"argv names a file not declared as an input: {INPUT_PATH}" in proc.stderr
    assert repo.receipts() == []


# --- Hole 1, second half: the dispatch log pins inputs, not only the seed ---

LOG_PATH = "docs/tournament/official-runs/dispatch-log.json"


def test_receipt_inputs_must_equal_the_dispatch_entry(repo):
    """(b) the seed matches its entry, but the entry declares no inputs."""
    repo.write(LOG_PATH, json.dumps({"entries": [{"entrant": "E1", "seed": 77}]}))
    repo.commit_all("dispatch log")
    receipt, _path = echo_receipt(repo, "--seed", "77")
    assert receipt["inputs"] == {INPUT_PATH: receipt["inputs"][INPUT_PATH]}
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all", "--dispatch-log", LOG_PATH)
    assert proc.returncode == 1
    assert "receipt inputs differ from dispatch log entry" in proc.stdout


def test_matching_inputs_pass_the_dispatch_check(repo):
    receipt, _path = echo_receipt(repo, "--seed", "77")
    entry = {"entrant": "E1", "seed": 77, "inputs": dict(receipt["inputs"])}
    repo.write(LOG_PATH, json.dumps({"entries": [entry]}))
    repo.commit_all("dispatch log")
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all", "--dispatch-log", LOG_PATH)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "inputs match" in proc.stdout


# --- Hole 2: a pool needs a real choice ---

def test_one_option_pool_writes_a_failed_receipt(repo):
    """(c) one option makes every index 0 without any generator."""
    write_pools(repo, ["opener"])
    proc = repo.run("bin/draw", "--entrant", "E1", "--pools", POOLS, "--seed", "1")
    assert proc.returncode == 1
    assert "pool 'angle' must have at least two options" in proc.stderr
    receipt = repo.receipt()
    assert receipt["status"] == "failed" and receipt["output"] == ""
    assert "must have at least two options" in receipt["error"]


def test_two_option_pool_still_draws(repo):
    write_pools(repo, ["opener", "closer"])
    proc = repo.run("bin/draw", "--entrant", "E1", "--pools", POOLS, "--seed", "1")
    assert proc.returncode == 0, proc.stderr
    assert repo.receipt()["status"] == "ok"


# --- Hole 3: the bold label triple is compared exactly ---

DRAW_RECORD = (
    "# Record\n\n## Provenance\n\n- **Entrant code:** E1\n\n## Execution trace\n\n"
    "%s\n\n%s\n\n## Receipts\n\n- %s draw primary\n"
)


def draw_record(repo, item_lines, receipt, output):
    text = DRAW_RECORD % (output.strip(), item_lines, receipt["receipt_id"])
    return repo.write("docs/tournament/official-runs/s16-e1.md", text)


def draw_once(repo):
    write_pools(repo, ["alpha", "beta", "gamma"], draws=2)
    proc = repo.run("bin/draw", "--entrant", "E1", "--pools", POOLS, "--seed", "1")
    assert proc.returncode == 0, proc.stderr
    return proc.stdout, repo.receipt(), repo.receipts()[-1]


def drawn(output, item):
    from lib.bindings.draw import drawn_labels, parse_output
    return drawn_labels(parse_output(output), item)


def test_hidden_option_words_in_prose_do_not_bind(repo):
    """(d) the right words are in the line, but the bold triple is invented."""
    output, receipt, path = draw_once(repo)
    lines = "\n".join(
        '%d. **invented label %d** — the drawn option was %s, described in prose.'
        % (item, item, " and ".join(drawn(output, item)))
        for item in (1, 2))
    record = draw_record(repo, lines, receipt, output)
    proc = repo.verify("bind", str(record), str(path))
    assert proc.returncode == 1 and "FAIL item_labels" in proc.stdout
    assert "item 1: labels invented label 1 != drawn" in proc.stdout


def test_item_line_without_a_bold_triple_fails(repo):
    output, receipt, path = draw_once(repo)
    lines = "\n".join('%d. %s in plain prose.' % (item, " / ".join(drawn(output, item)))
                      for item in (1, 2))
    record = draw_record(repo, lines, receipt, output)
    proc = repo.verify("bind", str(record), str(path))
    assert proc.returncode == 1 and "item 1: no bold label triple" in proc.stdout


def test_exact_bold_triple_binds(repo):
    output, receipt, path = draw_once(repo)
    lines = "\n".join('%d. **%s:** "an opener."' % (item, " / ".join(drawn(output, item)))
                      for item in (1, 2))
    record = draw_record(repo, lines, receipt, output)
    proc = repo.verify("bind", str(record), str(path))
    assert proc.returncode == 0, proc.stdout + proc.stderr


# --- Hole 4: the verification class is declared in code ---

def test_draw_receipt_cannot_claim_hash_attested(repo):
    """(e) an attestation dict no longer buys an exemption from replay."""
    output, receipt, path = draw_once(repo)
    rewrite(path, receipt, verification_class="hash-attested",
            external_attestation={"source": "invented", "id": "1"})
    lines = "\n".join('%d. **%s:** "an opener."' % (item, " / ".join(drawn(output, item)))
                      for item in (1, 2))
    draw_record(repo, lines, receipt, output)
    proc = repo.verify("all")
    assert proc.returncode == 1
    assert "receipt claims hash-attested, tool declares replay-exact" in proc.stdout


def test_hash_attested_tool_still_needs_an_attestation(repo):
    """The attestation requirement survives for a tool that really declares it."""
    receipt, path = echo_receipt(repo)
    rewrite(path, receipt, tool="attest-tool", verification_class="hash-attested",
            external_attestation=None)
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all")
    assert proc.returncode == 1
    assert "hash-attested receipt lacks external_attestation" in proc.stdout


# --- Receipts directory hygiene ---

def test_foreign_file_in_receipts_dir_fails(repo):
    """(f) the forger's pools files lived beside its receipts."""
    receipt, path = echo_receipt(repo)
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    assert repo.verify("all").returncode == 0
    repo.write("docs/tournament/receipts/E1/forger-pools.json", '{"draws": 1}')
    proc = repo.verify("all")
    assert proc.returncode == 1
    assert "foreign file in receipts dir: forger-pools.json" in proc.stdout


def test_orphan_sidecar_fails(repo):
    receipt, path = echo_receipt(repo)
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    assert repo.verify("all").returncode == 0
    orphan = "docs/tournament/receipts/E1/009-aaaaaaaaaaaa.bind.json"
    repo.write(orphan, "{}")
    proc = repo.verify("all")
    assert proc.returncode == 1
    assert "orphan sidecar: 009-aaaaaaaaaaaa.bind.json" in proc.stdout


# --- Relocatable receipts directory ---

def test_receipts_dir_env_var_moves_the_whole_harness(repo, monkeypatch):
    """(h) the tool writes there and `verify all` reads there."""
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", FIXTURE_RECEIPTS)
    proc = repo.tool("--entrant", "E1", "--text", "relocated")
    assert proc.returncode == 0, proc.stderr
    moved = sorted((repo.root / FIXTURE_RECEIPTS / "E1").glob("001-*.json"))
    assert len(moved) == 1 and not (repo.root / "docs/tournament/receipts/E1").exists()
    receipt = json.loads(moved[0].read_text())
    assert receipt["output"].endswith("relocated")
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    verify = repo.verify("all")
    assert verify.returncode == 0, verify.stdout + verify.stderr
    assert "PASS 1 receipts" in verify.stdout
    monkeypatch.delenv("HARNESS_RECEIPTS_DIR")
    assert "PASS 0 receipts" in repo.verify("all").stdout


# --- Orchestrator additions: path-shaped escapes from the archive ---

def test_absolute_input_key_cannot_pin_a_working_tree_file(repo):
    """An input key that is an absolute path would resolve outside the archive."""
    receipt, path = echo_receipt(repo)
    absolute = str(repo.root / INPUT_PATH)
    rewrite(path, receipt, inputs={absolute: receipt["inputs"][INPUT_PATH]},
            argv=["--entrant", "E1", "--input", absolute])
    proc = repo.verify("replay", str(path))
    assert proc.returncode == 1 and "escapes the archive" in proc.stdout


def test_parent_traversal_input_key_fails_replay(repo):
    receipt, path = echo_receipt(repo)
    escaped = "../" + repo.root.name + "/" + INPUT_PATH
    rewrite(path, receipt, inputs={escaped: receipt["inputs"][INPUT_PATH]},
            argv=["--entrant", "E1", "--input", escaped])
    proc = repo.verify("replay", str(path))
    assert proc.returncode == 1 and "escapes the archive" in proc.stdout


def test_tool_name_must_be_a_plain_bin_name(repo):
    receipt, path = echo_receipt(repo)
    rewrite(path, receipt, tool="../bin/echo-tool")
    proc = repo.verify("replay", str(path))
    assert proc.returncode == 1 and "not a plain bin/ name" in proc.stdout


# --- Second forger: status is validated, never trusted ---

def test_status_variant_is_rejected(repo):
    """`status: "OK"` used to skip replay and the dispatch check as 'not applicable'."""
    receipt, path = echo_receipt(repo)
    rewrite(path, receipt, status="OK")
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all")
    assert proc.returncode == 1 and "invalid status 'OK'" in proc.stdout


def test_failed_receipt_must_be_empty_and_cited_as_not_enacted(repo):
    receipt, path = echo_receipt(repo)
    rewrite(path, receipt, status="failed", error="forced")
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("all")
    assert proc.returncode == 1
    assert "failed receipt must have empty output" in proc.stdout
    assert "is not NOT ENACTED" in proc.stdout


def test_failed_receipt_still_owes_its_seed_under_a_dispatch_log(repo):
    proc = repo.tool("--entrant", "E1", "--text", "x", "--fail")
    assert proc.returncode == 1
    receipt = repo.receipt()
    repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], "NOT ENACTED")
    repo.write("docs/tournament/dispatch-log.json", json.dumps({"entries": []}))
    repo.commit_all("log")
    proc = repo.verify("all", "--dispatch-log", "docs/tournament/dispatch-log.json")
    assert proc.returncode == 1 and "unattested under a dispatch log" in proc.stdout
