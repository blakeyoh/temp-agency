"""Tests for the commissioner hub generator."""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_hub as hub


class GuardTests(unittest.TestCase):
    def test_refuses_an_out_dir_inside_the_repo_tree(self):
        inside = str(hub.ROOT / "docs" / "tournament" / "hub")
        with self.assertRaisesRegex(hub.OutsideTreeError, "inside the repository tree"):
            hub.resolve_out_dir(inside)

    def test_accepts_an_out_dir_outside_the_repo_tree(self):
        self.assertEqual(hub.resolve_out_dir("/tmp/hub-out").name, "hub-out")

    def test_default_out_dir_is_outside_the_repo_tree(self):
        with self.assertRaises(ValueError):
            hub.resolve_out_dir(None).relative_to(hub.ROOT)

    def test_rejects_an_unknown_phase(self):
        with self.assertRaisesRegex(hub.PhaseError, "unknown phase"):
            hub.resolve_phase("everything")

    def test_accepts_each_known_phase(self):
        for phase in ("runfloor", "output", "mechanism"):
            self.assertEqual(hub.resolve_phase(phase), phase)


if __name__ == "__main__":
    unittest.main()
