"""Tests for the commissioner hub generator."""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_hub as hub

CASE_BLIND = (str(hub.ROOT) != str(hub.ROOT).upper()
              and os.path.exists(str(hub.ROOT).upper()))


class GuardTests(unittest.TestCase):
    def test_refuses_an_out_dir_inside_the_repo_tree(self):
        inside = str(hub.ROOT / "docs" / "tournament" / "hub")
        with self.assertRaisesRegex(hub.OutsideTreeError, "inside the repository tree"):
            hub.resolve_out_dir(inside)

    @unittest.skipUnless(CASE_BLIND, "needs a case-insensitive filesystem")
    def test_refuses_a_differently_cased_path_into_the_repo(self):
        attack = str(hub.ROOT).upper() + "/docs/tournament/hub"
        with self.assertRaisesRegex(hub.OutsideTreeError, "inside the repository tree"):
            hub.resolve_out_dir(attack)

    def test_refuses_a_symlink_pointing_into_the_repo(self):
        with tempfile.TemporaryDirectory() as temp:
            link = os.path.join(temp, "sneaky")
            os.symlink(str(hub.ROOT / "docs"), link)
            with self.assertRaises(hub.OutsideTreeError):
                hub.resolve_out_dir(os.path.join(link, "tournament", "hub"))

    def test_accepts_an_out_dir_outside_the_repo_tree(self):
        got = hub.resolve_out_dir("/tmp/hub-out")
        self.assertTrue(got.is_absolute())
        self.assertEqual(got, hub.Path("/tmp/hub-out").resolve())

    def test_accepts_the_default_out_dir(self):
        self.assertEqual(hub.resolve_out_dir(None), hub.DEFAULT_OUT.resolve())

    def test_rejects_a_default_that_points_inside_the_repo(self):
        original = hub.DEFAULT_OUT
        hub.DEFAULT_OUT = hub.ROOT / "docs" / "tournament" / "hub"
        try:
            with self.assertRaises(hub.OutsideTreeError):
                hub.resolve_out_dir(None)
        finally:
            hub.DEFAULT_OUT = original

    def test_rejects_an_unknown_phase(self):
        with self.assertRaisesRegex(hub.PhaseError, "unknown phase"):
            hub.resolve_phase("everything")

    def test_accepts_each_known_phase(self):
        for phase in ("runfloor", "output", "mechanism"):
            self.assertEqual(hub.resolve_phase(phase), phase)


FIELD_FIXTURE = """### E1 · The Entropy Well ◆
*(owner idea 2, split: "scripts and shells")*

Randomness in this repo is currently rhetorical. Make it literal and seeded.

**Not native:** models simulate randomness by reaching for the most-likely option.

**Status** · **ADVANCED → Sweet 16** — Dog G6, 18–13, panels 2–1.

### A5 · The Hostile Environment

Remove a capability the persona depends on.

**Not native:** a model asked to work without a tool narrates the loss.

**Status** · **ADVANCED → Sweet 16** — Moat G10, 21–9.
"""

CONTRACT_FIXTURE = """## E1 · The Entropy Well

- **Enactment state:** **MANUAL PROTOTYPE.** The PRNG is cheap.

## A5 · The Hostile Environment

- **Enactment state:** **PROMISE, DEFECT UNRESOLVED.** No general mechanism yet.
"""


class FieldReaderTests(unittest.TestCase):
    def test_reads_code_name_and_owner_mark(self):
        field = hub.collect_field(FIELD_FIXTURE)
        self.assertEqual(set(field), {"E1", "A5"})
        self.assertEqual(field["E1"]["name"], "The Entropy Well")
        self.assertTrue(field["E1"]["owner"])
        self.assertFalse(field["A5"]["owner"])

    def test_reads_summary_skipping_the_provenance_italics(self):
        field = hub.collect_field(FIELD_FIXTURE)
        self.assertTrue(field["E1"]["summary"].startswith("Randomness in this repo"))

    def test_reads_labelled_sections_in_both_shapes(self):
        field = hub.collect_field(FIELD_FIXTURE)
        self.assertTrue(field["E1"]["not_native"].startswith("models simulate"))
        self.assertIn("ADVANCED", field["E1"]["status"])


class ContractReaderTests(unittest.TestCase):
    def test_splits_state_from_its_qualifier(self):
        states = hub.collect_states(CONTRACT_FIXTURE)
        self.assertEqual(states["E1"], {"state": "MANUAL PROTOTYPE", "flag": ""})
        self.assertEqual(states["A5"], {"state": "PROMISE", "flag": "DEFECT UNRESOLVED"})

    def test_reads_every_entrant_in_the_real_contracts_file(self):
        text = (hub.HERE / "evidence-contracts-s16.md").read_text(encoding="utf-8")
        states = hub.collect_states(text)
        # 17, not 16: M3 keeps its contract section after Ruling 22 moved it to the
        # wildcard bench. Verify with: grep -c '^## [A-Z][0-9]* ·' evidence-contracts-s16.md
        self.assertEqual(len(states), 17)
        for value in states.values():
            self.assertIn(value["state"], ("RUNNABLE", "MANUAL PROTOTYPE", "PROMISE"))


if __name__ == "__main__":
    unittest.main()


class Row:
    """Stand-in for lib.verify.gate.Row carrying only the fields gated_codes reads."""

    def __init__(self, entrant, status="ok", replay="pass", bind="pass", cited="pass"):
        self.entrant = entrant
        self.status = status
        self.replay = replay
        self.bind = bind
        self.cited = cited


class Report:
    def __init__(self, rows):
        self.rows = rows


class RunFloorTests(unittest.TestCase):
    def test_stage_climbs_with_each_completed_step(self):
        # One row per stage, so this single case covers all four.
        rows = hub.run_floor(["E6", "E1", "A5", "C8"], {"E1", "A5", "C8"},
                             {"A5", "C8"}, {"C8"}, {"C8": 3})
        self.assertEqual([r["stage"] for r in rows],
                         ["pending", "dispatched", "recorded", "gated"])
        self.assertEqual(rows[3]["receipts"], 3)

    def test_reads_dispatch_and_gate_state(self):
        self.assertEqual(
            hub.dispatched_codes({"entries": [{"entrant": "e1"}, {"entrant": "A5"}]}),
            {"E1", "A5"})
        self.assertEqual(hub.dispatched_codes({"entries": []}), set())
        report = Report([Row("E1"), Row("A5", replay="FAIL"), Row("E1")])
        self.assertEqual(hub.gated_codes(report), {"E1"})


DRAW_FIXTURE = {
    "seed": 372500925,
    "games": [{"g": 1, "pair": ["A1", "E4"], "A": "A1", "B": "E4", "region": "Sweet 16"}],
    "panels": [{"name": "Builder", "file_tag": "builder", "lead": "nuclear-reactor-operator",
                "lens": "magician-illusionist", "fresh": False}],
}


class AssembleTests(unittest.TestCase):
    def test_runfloor_payload_carries_state_and_omits_judged_evidence(self):
        payload = hub.assemble(
            "runfloor", hub.collect_field(FIELD_FIXTURE),
            hub.collect_states(CONTRACT_FIXTURE), DRAW_FIXTURE,
            hub.run_floor(["E1", "A5"], {"E1"}, set(), set(), {}))
        self.assertEqual(payload["phase"], "runfloor")
        self.assertEqual(payload["field"]["A5"]["state"], "PROMISE")
        self.assertEqual(payload["field"]["A5"]["flag"], "DEFECT UNRESOLVED")
        self.assertEqual(len(payload["games"]), 1)
        self.assertEqual(len(payload["floor"]), 2)
        # The phase gate works by omission: judged evidence must be absent from the bytes.
        blob = json.dumps(payload, ensure_ascii=False)
        for leak in ("Distance", "Irreducibility", "Compounding", "Generative failure",
                     "ABSORBED", "ORTHOGONAL", "STRONGEST"):
            self.assertNotIn(leak, blob)

    def test_emit_writes_a_single_global_assignment(self):
        with tempfile.TemporaryDirectory() as temp:
            path = hub.emit({"phase": "runfloor"}, hub.Path(temp) / "out")
            text = path.read_text(encoding="utf-8")
        self.assertEqual(path.name, "hub-data.js")
        self.assertTrue(text.startswith("window.HUB_DATA = {"))
        self.assertTrue(text.rstrip().endswith("};"))
