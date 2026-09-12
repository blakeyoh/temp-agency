"""Standard receipt lifecycle for the four A3 toolbelt executables."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Callable, Dict, List, Sequence

from lib import tools
from lib.errors import ToolError
from lib.toolbelts.common import input_provenance, read_json, render_json

Compute = Callable[[argparse.Namespace, Path], Dict[str, Any]]


def parser_for(tool: str, history: bool) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=tool)
    tools.add_common_args(parser)
    parser.add_argument("--config", help="committed JSON configuration")
    if history:
        parser.add_argument("--snapshot", help="committed orchestrator git-history snapshot")
    return parser


def _required(parser: argparse.ArgumentParser, args: argparse.Namespace, name: str) -> str:
    value = getattr(args, name)
    if not value or Path(value).is_absolute() or ".." in Path(value).parts:
        raise ToolError(f"{parser.prog}: --{name} must be a repo-relative file")
    return value


def _paths(parser: argparse.ArgumentParser, args: argparse.Namespace, history: bool) -> List[str]:
    paths = [_required(parser, args, "config")]
    if history:
        paths.append(_required(parser, args, "snapshot"))
    return paths


def _render(tool: str, args: argparse.Namespace, seed: Dict[str, Any], root: Path,
            paths: List[str], compute: Compute) -> str:
    if args.entrant != "A3":
        raise ValueError(f"{tool} is reserved for entrant A3, got {args.entrant!r}")
    result = {
        "inputs": input_provenance(root, paths),
        "invocation": {"arguments": {"config": args.config,
                                      **({"snapshot": args.snapshot} if hasattr(args, "snapshot") else {})},
                       "entrant": args.entrant, "seed": seed, "tool": f"bin/{tool}"},
        "result": compute(args, root),
        "schema": "temp-agency.toolbelt-result/v1",
        "tool": tool,
    }
    return render_json(result)


def main(tool_file: str, argv: Sequence[str], history: bool, compute: Compute) -> int:
    tool = Path(tool_file).name
    parser = parser_for(tool, history)
    replay = tools.maybe_replay(parser, argv)
    ctx = tools.make_context(tool_file)
    if replay:
        args = parser.parse_args(tools.replay_args(replay))
        paths = _paths(parser, args, history)
        tools.emit(_render(tool, args, replay["seed"], ctx.root, paths, compute))
        return 0
    args = parser.parse_args(list(argv))
    entrant = tools.require_entrant(parser, args)
    paths = _paths(parser, args, history)
    seed = tools.draw_seed(args.seed)
    output, receipt_path = tools.run_tool(
        ctx, entrant, list(argv), paths, seed, "replay-exact", None,
        lambda: _render(tool, args, seed, ctx.root, paths, compute),
    )
    tools.emit(output)
    tools.report_receipt(receipt_path)
    return 0
