"""bin/verify bind with the example verbatim rule (aliased as lib/bindings/echo_tool.py)."""
from __future__ import annotations

import json

from lib.paths import sha256_file


def test_bind_passes_when_record_contains_output(repo):
    repo.tool("--entrant", "E1", "--text", "bound text")
    receipt, path = repo.receipt(), repo.receipts()[0]
    record = repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("bind", str(record), str(path))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    sidecar_path = path.with_name(path.name[:-5] + ".bind.json")
    sidecar = json.loads(sidecar_path.read_text())
    assert sidecar["result"] == "pass"
    assert sidecar["receipt_id"] == receipt["receipt_id"]
    assert sidecar["record_path"] == "docs/tournament/official-runs/s16-e1.md"
    assert sidecar["artifact_sha256"] == sha256_file(record)
    assert sidecar["binding_rule"] == "lib.bindings.echo_tool"
    assert sidecar["bound_span"] == "receipt output appears verbatim in the record"
    assert sidecar["checks"] == [
        {"name": "output_verbatim", "expected": "present", "found": "present", "pass": True}
    ]
    assert sidecar["verifier_commit"] == repo.git("rev-parse", "HEAD").strip()
    assert sidecar["checked_utc"].endswith("Z")


def test_bind_fails_when_record_gestures_without_output(repo):
    repo.tool("--entrant", "E1", "--text", "bound text")
    receipt, path = repo.receipt(), repo.receipts()[0]
    record = repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], "we ran it, trust us")
    proc = repo.verify("bind", str(record), str(path))
    assert proc.returncode == 1
    assert "FAIL output_verbatim" in proc.stdout
    sidecar = json.loads(path.with_name(path.name[:-5] + ".bind.json").read_text())
    assert sidecar["result"] == "fail"
    assert sidecar["checks"][0]["found"] == "absent"


def test_bind_overwrites_existing_sidecar(repo):
    repo.tool("--entrant", "E1", "--text", "bound text")
    receipt, path = repo.receipt(), repo.receipts()[0]
    record = repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], "nope")
    assert repo.verify("bind", str(record), str(path)).returncode == 1
    record = repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    assert repo.verify("bind", str(record), str(path)).returncode == 0
    sidecar = json.loads(path.with_name(path.name[:-5] + ".bind.json").read_text())
    assert sidecar["result"] == "pass"


def test_bind_without_rule_is_a_verify_error(repo):
    repo.tool("--entrant", "E1", "--text", "x")
    receipt, path = repo.receipt(), repo.receipts()[0]
    (repo.root / "lib/bindings/echo_tool.py").unlink()
    record = repo.write_record("s16-e1.md", "E1", [receipt["receipt_id"]], receipt["output"])
    proc = repo.verify("bind", str(record), str(path))
    assert proc.returncode == 2 and "no binding rule for tool 'echo-tool'" in proc.stderr
