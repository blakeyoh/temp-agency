"""Tests for the commissioner hub generator."""
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


if __name__ == "__main__":
    unittest.main()
