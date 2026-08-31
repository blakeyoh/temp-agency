"""Regression tests for the Sweet 16 packet renderer."""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_s16_packets as builder


def source(code, rule_prefix):
    rules = "\n".join(f"{n}. {rule_prefix} rule {n}" for n in range(1, 25))
    return f"""# Sweet 16 Official Source Record — {code}

## Provenance

- **Entrant code:** {code}

## Pass 1 proposal artifact

{rules}

## Execution trace

Trace for {code}.
"""


class PacketRendererTests(unittest.TestCase):
    def test_render_keeps_pass_1_anonymous_and_releases_trace_separately(self):
        original = builder.RUNS, builder.PACKETS, builder.DRAW
        with tempfile.TemporaryDirectory() as temp:
            root = os.path.abspath(temp)
            builder.RUNS = builder.Path(root, "official-runs")
            builder.PACKETS = builder.Path(root, "packets")
            builder.DRAW = builder.Path(root, "s16-draw-map.json")
            builder.RUNS.mkdir()
            (builder.RUNS / "s16-a1.md").write_text(source("A1", "alpha"))
            (builder.RUNS / "s16-e4.md").write_text(source("E4", "beta"))
            builder.DRAW.write_text(json.dumps({"games": [
                {"g": 1, "A": "A1", "B": "E4", "region": "Sweet 16"}
            ]}))
            packets = builder.render(write=True)
            self.assertEqual(2, len(packets))
            output = (builder.PACKETS / "s16-01-output.md").read_text()
            trace = (builder.PACKETS / "s16-01-mechanism-trace.md").read_text()
            self.assertIn("alpha rule 24", output)
            self.assertIn("beta rule 24", output)
            self.assertNotIn("Entrant code", output)
            self.assertIn("Idea A entrant:** A1", trace)
            self.assertIn("Trace for E4.", trace)
        builder.RUNS, builder.PACKETS, builder.DRAW = original


if __name__ == "__main__":
    unittest.main()
