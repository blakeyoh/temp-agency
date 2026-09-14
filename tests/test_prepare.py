"""Phase 2 pre-persona preparation: frozen inputs, replay, and binding."""
from __future__ import annotations

import difflib
import json
import re
from pathlib import Path

import pytest

from lib.paths import sha256_file
from lib.receipt import load
from lib.pipeline import run
from lib.pipeline.negative import leaks

ROOT = Path(__file__).resolve().parents[1]
BRIEF = "docs/tournament/pipeline/tail-test-s16.txt"
CONFIGS = {
    "A1": "docs/tournament/pipeline/a1-transforms.json",
    "C8": "docs/tournament/pipeline/c8-mask-map.json",
    "A5": "docs/tournament/pipeline/a5-withhold.json",
}
DISPATCH = "docs/tournament/pipeline/test-dispatch-log.json"
RECORDS = "docs/tournament/official-runs"
PERSONAS = (
    "nuclear-reactor-operator", "magician-illusionist", "civil-rights-activist",
    "systems-thinker", "behavioral-psychologist", "franciscan-monk",
)
HEADER = re.compile(
    r"^PREPARE entrant=(\S+) adapter=(\S+) persona=(\S+) brief=(\S+) "
    r"config=(\S+) brief_sha256=([0-9a-f]{64}) config_sha256=([0-9a-f]{64})$"
)


def copy_inputs(repo):
    """Put the production brief and frozen configs in an otherwise-empty repo."""
    repo.write(BRIEF, (ROOT / "docs/tournament/tail-test-s16.txt").read_text())
    for path in CONFIGS.values():
        repo.write(path, (ROOT / path).read_text())
    commit_if_changed(repo, "commit prepare inputs")
    write_dispatch(repo)
    return repo


def write_dispatch(repo, extra=None):
    """Commit a dispatch log before issuing any receipt that this test will gate."""
    entries = []
    for entrant, config in CONFIGS.items():
        inputs = {BRIEF: sha256_file(repo.root / BRIEF), config: sha256_file(repo.root / config)}
        for seed in range(1, 80):
            entries.append({"entrant": entrant, "seed": seed, "inputs": inputs})
    if extra:
        entries.append(extra)
    repo.write(DISPATCH, json.dumps({"entries": entries}, indent=2) + "\n")
    commit_if_changed(repo, "commit prepare dispatch")


def commit_if_changed(repo, message):
    if repo.git("status", "--porcelain").strip():
        repo.commit_all(message)


def invoke(repo, entrant, adapter, seed=1, persona=None, config=None):
    """Run prepare and return its process, receipt, receipt path, and parsed output."""
    args = ["bin/prepare", "--entrant", entrant, "--adapter", adapter, "--brief", BRIEF,
            "--config", config or CONFIGS[entrant], "--seed", str(seed)]
    if persona:
        args.extend(["--persona", persona])
    proc = repo.run(*args)
    receipt = repo.receipt(entrant)
    parsed = parse_output(proc.stdout) if proc.returncode == 0 else None
    return proc, receipt, repo.receipts(entrant)[-1], parsed


def parse_output(output):
    """Parse the deliberately small, exact prepare output protocol."""
    lines = output.splitlines()
    match = HEADER.match(lines[0]) if lines else None
    if not match or len(lines) < 8 or lines[1] or lines[2] != "=== PERSONA-VISIBLE INPUT ===":
        raise ValueError("output has no valid PREPARE envelope")
    first_end = find_end(lines, 3)
    if first_end is None or first_end + 2 >= len(lines) or lines[first_end + 1]:
        raise ValueError("output has no visible-input terminator")
    if lines[first_end + 2] != "=== TRANSFORM RECORD ===":
        raise ValueError("output has no transform-record header")
    second_end = find_end(lines, first_end + 3)
    if second_end != len(lines) - 1:
        raise ValueError("output has no final transform-record terminator")
    return {"header": match.groups(), "visible": "\n".join(lines[3:first_end]),
            "record": lines[first_end + 3:second_end]}


def find_end(lines, start):
    for index in range(start, len(lines)):
        if lines[index] == "=== END ===":
            return index
    return None


def prepared(repo, entrant, adapter, seed=1, persona=None):
    proc, receipt, path, parsed = invoke(repo, entrant, adapter, seed, persona)
    assert proc.returncode == 0, proc.stderr
    return receipt, path, parsed


def source_record(entrant, receipt, visible, section, lines=None):
    numbered = lines or ["%d. concrete action without protected facts" % n for n in range(1, 11)]
    return (
        "# Sweet 16 Official Source Record — %s\n\n## Provenance\n\n"
        "- **Entrant code:** %s\n\n## Execution trace\n\n%s\n\n## %s\n\n%s\n\n"
        "## Receipts\n\n- %s prepare run\n"
        % (entrant, entrant, visible, section, "\n".join(numbered), receipt["receipt_id"])
    )


@pytest.mark.parametrize("persona", PERSONAS)
def test_transform_personas_pin_inputs_and_change_the_brief(repo, persona):
    copy_inputs(repo)
    receipt, _path, parsed = prepared(repo, "A1", "transform", persona=persona)
    brief = (repo.root / BRIEF).read_text().strip()
    assert receipt["inputs"] == {BRIEF: sha256_file(repo.root / BRIEF),
                                 CONFIGS["A1"]: sha256_file(repo.root / CONFIGS["A1"])}
    assert receipt["seed"] == {"value": 1, "source": "argument"}
    assert parsed["header"][0:3] == ("A1", "transform", persona)
    assert difflib.SequenceMatcher(None, brief, parsed["visible"]).ratio() < 0.9
    assert parsed["record"] and any("kept" in line or "dropped" in line or "rewritten:" in line
                                        for line in parsed["record"])


def test_transform_personas_are_pairwise_materially_different(repo):
    copy_inputs(repo)
    visible = [prepared(repo, "A1", "transform", seed=index + 1, persona=persona)[2]["visible"]
               for index, persona in enumerate(PERSONAS)]
    for index, left in enumerate(visible):
        for right in visible[index + 1:]:
            assert difflib.SequenceMatcher(None, left, right).ratio() < 0.9


def test_mask_removes_frozen_nouns_and_prefers_the_longest_phrase(repo):
    copy_inputs(repo)
    _receipt, _path, parsed = prepared(repo, "C8", "mask")
    mapping = json.loads((repo.root / CONFIGS["C8"]).read_text())["map"]
    assert len(set(mapping.values())) == len(mapping)
    assert all(not re.search(r"\b%s\b" % re.escape(noun), parsed["visible"], re.I)
               for noun in mapping)
    assert any(line.startswith("masked_nouns=") for line in parsed["record"])
    config = "docs/tournament/pipeline/test-longest-map.json"
    repo.write(config, json.dumps({"map": {"recreation center": "PLACE_A", "center": "ENTITY_A"}}))
    commit_if_changed(repo, "commit longest-first mask")
    write_dispatch(repo, {"entrant": "C8", "seed": 79,
                          "inputs": {BRIEF: sha256_file(repo.root / BRIEF),
                                     config: sha256_file(repo.root / config)}})
    _proc, _receipt, _path, longest = invoke(repo, "C8", "mask", 79, config=config)
    assert "PLACE_A" in longest["visible"] and "recreation ENTITY_A" not in longest["visible"]


def test_withhold_conditions_and_absent_span_failure_receipt(repo):
    copy_inputs(repo)
    for seed, condition in ((1, "budget"), (2, "night-shift")):
        config = json.loads((repo.root / CONFIGS["A5"]).read_text())
        config["condition"] = condition
        repo.write(CONFIGS["A5"], json.dumps(config, indent=2) + "\n")
        commit_if_changed(repo, "select withheld condition")
        write_dispatch(repo)
        proc, _receipt, _path, parsed = invoke(repo, "A5", "withhold", seed)
        assert proc.returncode == 0, proc.stderr
        withheld = config["conditions"][condition]["withhold"]
        assert withheld not in parsed["visible"] and withheld not in proc.stdout
    config = json.loads((repo.root / CONFIGS["A5"]).read_text())
    config["conditions"]["night-shift"]["withhold"] = "this span is absent"
    repo.write(CONFIGS["A5"], json.dumps(config, indent=2) + "\n")
    commit_if_changed(repo, "commit absent withheld span")
    write_dispatch(repo)
    proc, receipt, _path, _parsed = invoke(repo, "A5", "withhold", 3)
    assert proc.returncode == 1 and receipt["status"] == "failed"
    assert "ValueError" in receipt["error"] and receipt["output"] == ""


def test_replay_uses_archived_config_while_dirty_config_blocks_new_runs(repo):
    copy_inputs(repo)
    _receipt, path, _parsed = prepared(repo, "A1", "transform", persona=PERSONAS[0])
    original = (repo.root / CONFIGS["A1"]).read_text()
    repo.write(CONFIGS["A1"], original + "\n")
    blocked, _receipt, _path, _parsed = invoke(repo, "A1", "transform", 2, PERSONAS[0])
    assert blocked.returncode == 1 and "working tree is dirty" in blocked.stderr
    assert repo.verify("replay", str(path)).returncode == 0


@pytest.mark.parametrize("entrant,adapter,persona,section", (
    ("A1", "transform", "nuclear-reactor-operator", "Pass 1 proposal artifact"),
    ("C8", "mask", None, "Abstract proposal"),
    ("A5", "withhold", None, "Pass 1 proposal artifact"),
))
def test_bind_accepts_an_honest_record_for_each_adapter(repo, entrant, adapter, persona, section):
    copy_inputs(repo)
    receipt, path, parsed = prepared(repo, entrant, adapter, persona=persona)
    record = repo.write("%s/s16-%s.md" % (RECORDS, entrant.lower()),
                        source_record(entrant, receipt, parsed["visible"], section))
    result = repo.verify("bind", str(record), str(path))
    assert result.returncode == 0, result.stdout


def test_binding_fails_on_raw_brief_leak_and_missing_or_duplicate_sections(repo):
    copy_inputs(repo)
    receipt, path, parsed = prepared(repo, "A1", "transform", persona=PERSONAS[0])
    sentence = (repo.root / BRIEF).read_text().split(". ")[0] + "."
    record = source_record("A1", receipt, parsed["visible"], "Pass 1 proposal artifact",
                           [sentence] + ["%d. action" % n for n in range(2, 11)])
    bad = repo.write("%s/raw.md" % RECORDS, record)
    assert "FAIL raw_brief_absent" in repo.verify("bind", str(bad), str(path)).stdout
    missing = repo.write("%s/missing.md" % RECORDS, record.replace("## Pass 1 proposal artifact", "## Other"))
    assert "FAIL record_sections" in repo.verify("bind", str(missing), str(path)).stdout
    duplicate = repo.write("%s/duplicate.md" % RECORDS,
                           record.replace("## Receipts", "## Pass 1 proposal artifact\n\n1. again\n\n## Receipts"))
    assert repo.verify("bind", str(duplicate), str(path)).returncode == 1


def test_binding_fails_on_mask_and_withhold_negative_word_leaks(repo):
    copy_inputs(repo)
    mask, mask_path, mask_out = prepared(repo, "C8", "mask")
    noun = next(iter(json.loads((repo.root / CONFIGS["C8"]).read_text())["map"]))
    masked = repo.write("%s/mask-leak.md" % RECORDS,
                        source_record("C8", mask, mask_out["visible"], "Abstract proposal",
                                      ["1. %s appears" % noun] + ["%d. action" % n for n in range(2, 11)]))
    assert "FAIL negative_words" in repo.verify("bind", str(masked), str(mask_path)).stdout
    held, held_path, held_out = prepared(repo, "A5", "withhold", seed=2)
    word = json.loads((repo.root / CONFIGS["A5"]).read_text())["conditions"]["budget"]["negative_words"][0]
    withheld = repo.write("%s/withhold-leak.md" % RECORDS,
                          source_record("A5", held, held_out["visible"], "Pass 1 proposal artifact",
                                        ["1. %s appears" % word] + ["%d. action" % n for n in range(2, 11)]))
    assert "FAIL negative_words" in repo.verify("bind", str(withheld), str(held_path)).stdout


def test_malformed_receipt_output_fails_closed_and_gate_accepts_honest_set(repo):
    copy_inputs(repo)
    prepared_runs = [
        ("A1", "transform", PERSONAS[0], "Pass 1 proposal artifact"),
        ("C8", "mask", None, "Abstract proposal"),
        ("A5", "withhold", None, "Pass 1 proposal artifact"),
    ]
    for seed, (entrant, adapter, persona, section) in enumerate(prepared_runs, 1):
        receipt, path, parsed = prepared(repo, entrant, adapter, seed, persona)
        record = repo.write("%s/s16-%s.md" % (RECORDS, entrant.lower()),
                            source_record(entrant, receipt, parsed["visible"], section))
        assert repo.verify("bind", str(record), str(path)).returncode == 0
    gated = repo.verify("all", "--records", "%s/s16-*.md" % RECORDS,
                        "--dispatch-log", DISPATCH)
    assert gated.returncode == 0, gated.stdout + gated.stderr
    receipt_path = repo.receipts("A1")[0]
    receipt = load(receipt_path)
    receipt_path.write_text(json.dumps({**receipt, "output": "corrupt\n"}))
    bad = repo.verify("bind", str(repo.root / ("%s/s16-a1.md" % RECORDS)), str(receipt_path))
    assert bad.returncode == 1
    for name in ("visible_verbatim", "raw_brief_absent", "negative_words", "record_sections"):
        assert "FAIL %s:" % name in bad.stdout


def test_mask_preserves_verbs_adjectives_and_whole_word_boundaries():
    config = json.loads((ROOT / CONFIGS["C8"]).read_text())
    brief = (ROOT / "docs/tournament/tail-test-s16.txt").read_text()
    visible = run("mask", brief, config, None).visible
    for phrase in ("narrow", "insulated", "night-shift", "published", "reporting", "legitimate"):
        assert phrase in visible
    assert leaks("HOSPITAL, eight; 12,000. volunteer hours", [
        "hospital", "eight", "12,000", "volunteer hours"]) == [
        "hospital", "eight", "12,000", "volunteer hours"]
    assert leaks("hospitality eighteen 112,000 volunteer hourly", [
        "hospital", "eight", "12,000", "volunteer hours"]) == []


@pytest.mark.parametrize("mapping", (
    {}, {"a": "ENTITY_A", "b": "ENTITY_A"}, {"A": "ENTITY_A", "a": "ENTITY_B"},
    {"": "ENTITY_A"}, {"a": "not a token"},
))
def test_invalid_mask_config_is_rejected(mapping):
    with pytest.raises(ValueError):
        run("mask", "a b", {"map": mapping}, None)


def test_transform_operations_and_no_mutation():
    config = json.loads((ROOT / CONFIGS["A1"]).read_text())
    before = json.dumps(config, sort_keys=True)
    brief = "Residents sleep. The city must keep 3 limits. Mixed-use homes exist."
    reverse = run("transform", brief, config, "magician-illusionist")
    assert reverse.visible.splitlines() == [
        "Mixed-use homes exist.", "The city must keep 3 limits.", "Residents sleep."]
    limits = run("transform", brief, config, "nuclear-reactor-operator")
    assert limits.visible == "The city must keep 3 limits."
    stocks = run("transform", "A small mixed-use strip has noise.", config, "systems-thinker")
    assert "mixed" not in stocks.visible and "small" not in stocks.visible
    assert "has" not in stocks.visible and "→" in stocks.visible
    assert json.dumps(config, sort_keys=True) == before


@pytest.mark.parametrize("condition", ("budget", "night-shift"))
def test_withheld_visible_is_exact_subtraction_and_duplicate_span_fails(condition):
    brief = (ROOT / "docs/tournament/tail-test-s16.txt").read_text()
    config = json.loads((ROOT / CONFIGS["A5"]).read_text())
    config["condition"] = condition
    entry = config["conditions"][condition]
    result = run("withhold", brief, config, None)
    assert result.visible == brief.replace(entry["withhold"], "", 1)
    assert not leaks(result.visible, entry["negative_words"])
    assert entry["key"] not in "\n".join(result.record_lines)
    with pytest.raises(ValueError):
        run("withhold", brief + entry["withhold"], config, None)


def test_binding_rejects_input_tamper_and_optional_abstract_leak(repo):
    copy_inputs(repo)
    receipt, path, parsed = prepared(repo, "A5", "withhold")
    text = source_record("A5", receipt, parsed["visible"], "Pass 1 proposal artifact")
    record = repo.write("%s/leak.md" % RECORDS, text + "\n## Abstract proposal\nEight people.\n")
    assert "FAIL negative_words" in repo.verify("bind", str(record), str(path)).stdout
    record.write_text(text)
    config = repo.root / CONFIGS["A5"]
    config.write_text(config.read_text() + "\n")
    assert repo.verify("bind", str(record), str(path)).returncode == 1


@pytest.mark.parametrize('entrant,adapter,section,word', [
    ('C8', 'mask', 'Abstract proposal', 'hospital workers'),
    ('A5', 'withhold', 'Pass 1 proposal artifact', 'Eight'),
])
@pytest.mark.parametrize('heading', ['', '## Reasoning\n', '## Approach\n'])
def test_negative_scan_includes_other_reasoning(repo, entrant, adapter, section, word, heading):
    copy_inputs(repo)
    receipt, path, parsed = prepared(repo, entrant, adapter)
    text = source_record(entrant, receipt, parsed['visible'], section)
    record = repo.write(RECORDS + '/leak.md', heading + word + '\n' + text)
    assert 'FAIL negative_words' in repo.verify('bind', str(record), str(path)).stdout


def test_mask_allows_decoded_final_proposal(repo):
    copy_inputs(repo)
    receipt, path, parsed = prepared(repo, 'C8', 'mask')
    text = source_record('C8', receipt, parsed['visible'], 'Abstract proposal')
    record = repo.write(RECORDS + '/decoded.md', text + '\n## Pass 1 proposal artifact\n1. hospital workers\n')
    assert repo.verify('bind', str(record), str(path)).returncode == 0
