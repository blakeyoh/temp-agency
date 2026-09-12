"""A3's four real computations, replay lifecycle, dispatch pins and strict credits."""
from __future__ import annotations

import json
from pathlib import Path

from lib.bindings._toolbelt import invocation
from lib.paths import sha256_file

REPO_ROOT = Path(__file__).resolve().parents[1]
BASE = "docs/tournament/toolbelts"
SNAPSHOT = f"{BASE}/temp-agency-history-1925816.json"
CONFIGS = {tool: f"{BASE}/{tool}.json" for tool in ("churn", "seasons", "units", "orders")}
SEEDS = {"churn": 101, "seasons": 102, "units": 103, "orders": 104}


def install_inputs(repo):
    for rel in [SNAPSHOT, *CONFIGS.values()]:
        repo.write(rel, (REPO_ROOT / rel).read_text(encoding="utf-8"))
    repo.commit_all("add A3 toolbelt inputs")


def command(tool):
    args = ["--entrant", "A3", "--seed", str(SEEDS[tool]), "--config", CONFIGS[tool]]
    if tool in ("churn", "seasons"):
        args += ["--snapshot", SNAPSHOT]
    return [f"bin/{tool}", *args]


def run_all(repo):
    results = {}
    for tool in SEEDS:
        proc = repo.run(*command(tool))
        assert proc.returncode == 0, proc.stderr
        results[tool] = (proc, repo.receipt("A3"), repo.receipts("A3")[-1])
    return results


def credit_block(receipt):
    return (f"### {receipt['receipt_id']}\n\nInvocation:\n\n```json\n"
            f"{invocation(receipt)}```\n\nRaw result:\n\n```json\n"
            f"{receipt['output']}```\n")


def record(receipts, credits=True, extra_credit=""):
    ids = "\n".join(f"- {item['receipt_id']} — {item['tool']}" for item in receipts)
    section = ""
    if credits:
        blocks = "\n".join(credit_block(item) for item in receipts) + extra_credit
        section = f"## Credited tools\n\n{blocks}\n"
    return ("# A3 toolbelt fixture\n\n## Provenance\n\n- **Entrant code:** A3\n\n"
            f"{section}## Receipts\n\n{ids}\n")


def write_dispatch(repo):
    entries = []
    for tool, seed in SEEDS.items():
        paths = [CONFIGS[tool]] + ([SNAPSHOT] if tool in ("churn", "seasons") else [])
        entries.append({"entrant": "A3", "seed": seed,
                        "inputs": {path: sha256_file(repo.root / path) for path in paths}})
    rel = f"{BASE}/dispatch-log.json"
    repo.write(rel, json.dumps({"entries": entries}, indent=2, sort_keys=True) + "\n")
    repo.commit_all("freeze A3 dispatch")
    return rel


def test_four_computations_are_real_and_structured(repo):
    install_inputs(repo)
    runs = run_all(repo)
    churn = json.loads(runs["churn"][0].stdout)
    assert churn["tool"] == "churn" and churn["result"]["commits_considered"] == 114
    assert churn["result"]["file_touches"]
    seasons = json.loads(runs["seasons"][0].stdout)
    cadence = seasons["result"]["monthly_cadence"]
    assert sum(row["commit_count"] for row in cadence) == 114
    units = json.loads(runs["units"][0].stdout)
    assert units["result"]["dependency_versions"] == {"Pint": "0.26.1"}
    assert units["result"]["operations"][0]["converted_value"].startswith("1.388888")
    orders = json.loads(runs["orders"][0].stdout)
    assert orders["result"][1]["ratio"] == "1000"
    assert orders["result"][1]["whole_orders"] == 3
    for tool, (_proc, receipt, _path) in runs.items():
        assert receipt["tool"] == tool and receipt["status"] == "ok"
        assert receipt["seed"] == {"source": "argument", "value": SEEDS[tool]}


def test_archive_replay_of_all_four_tools(repo):
    install_inputs(repo)
    for _tool, (_proc, _receipt, path) in run_all(repo).items():
        replay = repo.verify("replay", str(path))
        assert replay.returncode == 0, replay.stdout + replay.stderr
        assert "replay output byte-equal" in replay.stdout


def test_tampered_result_fails_archive_replay(repo):
    install_inputs(repo)
    proc = repo.run(*command("orders"))
    assert proc.returncode == 0
    path = repo.receipts("A3")[-1]
    receipt = json.loads(path.read_text(encoding="utf-8"))
    receipt["output"] = receipt["output"].replace('"whole_orders": 3', '"whole_orders": 4')
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert repo.verify("replay", str(path)).returncode == 1


def test_unsupported_unit_mints_failed_receipt(repo):
    install_inputs(repo)
    config = json.loads((repo.root / CONFIGS["units"]).read_text())
    config["operations"][0]["from"] = "furlong_of_moonlight"
    bad = f"{BASE}/units-unsupported.json"
    repo.write(bad, json.dumps(config, indent=2, sort_keys=True) + "\n")
    repo.commit_all("add unsupported units fixture")
    args = ["bin/units", "--entrant", "A3", "--seed", "1", "--config", bad]
    proc = repo.run(*args)
    assert proc.returncode == 1 and "unsupported" in proc.stderr
    receipt = repo.receipt("A3")
    assert receipt["status"] == "failed" and receipt["output"] == ""


def test_malformed_history_snapshot_mints_failed_receipt(repo):
    install_inputs(repo)
    snapshot = json.loads((repo.root / SNAPSHOT).read_text())
    snapshot["origin"]["window_years"] = 1
    bad = f"{BASE}/history-malformed.json"
    repo.write(bad, json.dumps(snapshot, indent=2, sort_keys=True) + "\n")
    repo.commit_all("add malformed snapshot")
    args = ["bin/churn", "--entrant", "A3", "--seed", "2", "--config", CONFIGS["churn"],
            "--snapshot", bad]
    proc = repo.run(*args)
    assert proc.returncode == 1
    assert repo.receipt("A3")["status"] == "failed"


def test_binding_requires_explicit_credited_tools_section(repo):
    install_inputs(repo)
    proc = repo.run(*command("orders"))
    assert proc.returncode == 0
    receipt, path = repo.receipt("A3"), repo.receipts("A3")[-1]
    record_path = repo.write("docs/tournament/official-runs/s16-a3.md", record([receipt], credits=False))
    bound = repo.verify("bind", str(record_path), str(path))
    assert bound.returncode == 1 and "FAIL credited_section" in bound.stdout


def test_binding_rejects_fake_credit_without_receipt(repo):
    install_inputs(repo)
    proc = repo.run(*command("orders"))
    assert proc.returncode == 0
    receipt, path = repo.receipt("A3"), repo.receipts("A3")[-1]
    fake = {**receipt, "receipt_id": "deadbeef1234", "tool": "units"}
    text = record([receipt, fake], extra_credit="\n" + credit_block(fake))
    record_path = repo.write("docs/tournament/official-runs/s16-a3.md", text)
    bound = repo.verify("bind", str(record_path), str(path))
    assert bound.returncode == 1 and "no receipt found" in bound.stdout


def test_dispatch_log_freezes_every_seed_and_input_hash(repo):
    install_inputs(repo)
    dispatch = write_dispatch(repo)
    runs = run_all(repo)
    receipts = [runs[tool][1] for tool in SEEDS]
    repo.write("docs/tournament/official-runs/s16-a3.md", record(receipts))
    gate = repo.verify("all", "--records", "docs/tournament/official-runs/s16-a3.md",
                       "--dispatch-log", dispatch)
    assert gate.returncode == 0, gate.stdout + gate.stderr
    assert gate.stdout.count("inputs match") == 4
    assert "PASS 4 receipts" in gate.stdout


def test_dispatch_log_rejects_wrong_frozen_hash(repo):
    install_inputs(repo)
    dispatch = write_dispatch(repo)
    data = json.loads((repo.root / dispatch).read_text())
    data["entries"][0]["inputs"][CONFIGS["churn"]] = "0" * 64
    repo.write(dispatch, json.dumps(data, indent=2, sort_keys=True) + "\n")
    repo.commit_all("freeze wrong A3 hash")
    runs = run_all(repo)
    receipts = [runs[tool][1] for tool in SEEDS]
    repo.write("docs/tournament/official-runs/s16-a3.md", record(receipts))
    gate = repo.verify("all", "--records", "docs/tournament/official-runs/s16-a3.md",
                       "--dispatch-log", dispatch)
    assert gate.returncode == 1 and "receipt inputs differ" in gate.stdout


def test_offset_temperature_conversion():
    from lib.toolbelts.measure import units_results, validate_units_config
    config = {"schema": "temp-agency.units/v1", "pint_version": "0.26.1",
              "operations": [{"id": "freezing", "operation": "convert", "value": "0",
                              "from": "degC", "to": "kelvin"}]}
    result = units_results(validate_units_config(config))
    assert result["operations"][0]["converted_value"] == "273.15"


def test_history_rejects_false_window_and_non_utc():
    import copy
    import pytest
    from lib.toolbelts.history import validate_snapshot
    snapshot = json.loads((REPO_ROOT / SNAPSHOT).read_text())
    for field, value in [("window_start_utc", "2000-01-01T00:00:00Z"),
                         ("window_end_utc", "2026-09-12T00:00:00+01:00")]:
        altered = copy.deepcopy(snapshot)
        altered["origin"][field] = value
        with pytest.raises(ValueError):
            validate_snapshot(altered)


def test_wrong_entrant_mints_failed_receipt(repo):
    install_inputs(repo)
    proc = repo.run("bin/orders", "--entrant", "E1", "--seed", "1", "--config", CONFIGS["orders"])
    assert proc.returncode == 1
    assert repo.receipt("E1")["status"] == "failed"


def test_collector_includes_merge_changes(repo):
    import runpy
    collector = runpy.run_path(str(REPO_ROOT / "scripts/snapshot-toolbelt-history.py"))
    original = repo.git("branch", "--show-current").strip()
    repo.git("checkout", "-q", "-b", "side")
    repo.write("side.txt", "side contribution\n")
    repo.commit_all("side change")
    repo.git("checkout", "-q", original)
    repo.write("main.txt", "main contribution\n")
    repo.commit_all("main change")
    repo.git("merge", "--no-ff", "-m", "merge side", "side")
    assert collector["touched_files"](repo.root, "HEAD") == ["side.txt"]
