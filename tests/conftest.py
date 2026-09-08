"""Shared fixture: a throwaway git repo carrying the real bin/ and lib/ plus a test tool."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.receipt import list_receipts, load  # noqa: E402

INPUT_PATH = "docs/tournament/inputs/hello.txt"
INPUT_TEXT = "hello from file\n"
RECORDS_DIR = "docs/tournament/official-runs"

ECHO_TOOL = '''#!/usr/bin/env python3
"""Test tool: echo --text or a committed --input file, with a seed header line."""
import argparse
import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib import tools  # noqa: E402


def build_parser():
    parser = argparse.ArgumentParser(prog="echo-tool")
    tools.add_common_args(parser)
    parser.add_argument("--text")
    parser.add_argument("--input", help="committed input file, relative to the repo root")
    parser.add_argument("--upper", action="store_true")
    parser.add_argument("--fail", action="store_true", help="make produce() raise")
    return parser


def render(args, seed, root):
    if args.fail:
        raise RuntimeError("forced failure")
    if args.text is None and args.input is None:
        raise ValueError("need --text or --input")
    body = args.text if args.text is not None else (root / args.input).read_text(encoding="utf-8")
    if args.upper:
        body = body.upper()
    return "seed=%s\\n%s" % (seed["value"], body)


def main(argv):
    parser = build_parser()
    replay = tools.maybe_replay(parser, argv)
    ctx = tools.make_context(__file__)
    if replay:
        args = parser.parse_args(tools.replay_args(replay))
        tools.emit(render(args, replay["seed"], ctx.root))
        return 0
    args = parser.parse_args(argv)
    entrant = tools.require_entrant(parser, args)
    seed = tools.draw_seed(args.seed)
    inputs = [args.input] if args.input else []
    output, path = tools.run_tool(
        ctx, entrant, argv, inputs, seed, "replay-exact", None,
        lambda: render(args, seed, ctx.root),
    )
    tools.emit(output)
    tools.report_receipt(path)
    return 0


if __name__ == "__main__":
    tools.exit_on_error(main)
'''

ECHO_RULE = (
    '"""Binding rule for the test tool: the example verbatim rule."""\n'
    'from lib.bindings._example import check  # noqa: F401\n\n'
    'VERIFICATION_CLASS = "replay-exact"\n'
)
ATTEST_RULE = (
    '"""Binding rule for a hypothetical hash-attested tool, used only by tests."""\n'
    'from lib.bindings._example import check  # noqa: F401\n\n'
    'VERIFICATION_CLASS = "hash-attested"\n'
)


def record_text(entrant: str, receipt_ids: Sequence[str], body: str) -> str:
    bullets = "\n".join(f"- {rid} echo-tool run" for rid in receipt_ids)
    return (
        f"# Sweet 16 Official Source Record — {entrant}\n\n## Provenance\n\n"
        f"- **Entrant code:** {entrant}\n\n## Execution trace\n\n{body}\n\n"
        f"## Receipts\n\n{bullets}\n"
    )


class Repo:
    """Handle on the throwaway repo. Tools run as subprocesses from its root."""

    def __init__(self, root: Path):
        self.root = root

    def git(self, *args: str) -> str:
        proc = subprocess.run(["git", *args], cwd=self.root, check=True,
                              capture_output=True, text=True)
        return proc.stdout

    def commit_all(self, message: str = "update") -> None:
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, *args], cwd=self.root,
                              capture_output=True, text=True)

    def tool(self, *args: str) -> subprocess.CompletedProcess:
        return self.run("bin/echo-tool", *args)

    def verify(self, *args: str) -> subprocess.CompletedProcess:
        return self.run("bin/verify", *args)

    def receipts(self, entrant: str = "E1") -> List[Path]:
        return list_receipts(self.root, entrant)

    def receipt(self, entrant: str = "E1", index: int = -1) -> Dict[str, Any]:
        return load(self.receipts(entrant)[index])

    def write(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def write_record(self, name: str, entrant: str, receipt_ids: Sequence[str],
                     body: str = "", directory: str = RECORDS_DIR) -> Path:
        return self.write(f"{directory}/{name}", record_text(entrant, receipt_ids, body))


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Repo:
    root = (tmp_path / "repo").resolve()
    root.mkdir()
    (tmp_path / "empty-gitconfig").write_text("")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(tmp_path / "empty-gitconfig"))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")
    handle = Repo(root)
    handle.git("init", "-q")
    handle.git("config", "user.name", "Harness Test")
    handle.git("config", "user.email", "harness@example.invalid")
    handle.git("config", "commit.gpgsign", "false")
    ignore = shutil.ignore_patterns("__pycache__")
    shutil.copytree(REPO_ROOT / "bin", root / "bin", ignore=ignore)
    shutil.copytree(REPO_ROOT / "lib", root / "lib", ignore=ignore)
    handle.write("docs/tournament/receipts/.gitkeep", "")
    handle.write(".gitignore", "__pycache__/\n")
    handle.write("bin/echo-tool", ECHO_TOOL).chmod(0o755)
    handle.write("lib/bindings/echo_tool.py", ECHO_RULE)
    handle.write("lib/bindings/attest_tool.py", ATTEST_RULE)
    handle.write(INPUT_PATH, INPUT_TEXT)
    handle.commit_all("harness under test")
    monkeypatch.chdir(root)
    return handle
