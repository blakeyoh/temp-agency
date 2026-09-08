"""Scaffolding every bin/ tool uses: clean-tree checks, seeds, run lifecycle, replay.

Lifecycle of one run (see lib/README.md):
  parse args -> maybe_replay -> require_clean -> hash_inputs -> produce()
  -> mint nonce -> receipt.issue -> caller prints output + receipt path.
"""
from __future__ import annotations

import argparse
import secrets
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Sequence, Tuple

from lib import receipt as receipt_lib
from lib.errors import HarnessError, ReceiptError, ToolError
from lib.paths import (
    canonical_json, git_output, head_commit, python_version, relative_to_root,
    repo_root, sha256_bytes, sha256_file, utc_now,
)

GUARDED_PATHS: Tuple[str, ...] = ("bin", "lib")
NO_SEED: Dict[str, Any] = {"value": None, "source": "none"}
SEED_BITS = 32


class ToolContext(NamedTuple):
    """Where a tool is running: repo root, its own name and file, start time."""

    root: Path
    tool_name: str
    tool_path: Path
    started_utc: str


def make_context(tool_file: str) -> ToolContext:
    """Build a ToolContext from the tool's own `__file__`."""
    tool_path = Path(tool_file).resolve()
    return ToolContext(repo_root(), tool_path.name, tool_path, utc_now())


def _relative_paths(root: Path, paths: Sequence[str]) -> List[str]:
    absolute = [Path(p) if Path(p).is_absolute() else root / p for p in paths]
    return [relative_to_root(root, p) for p in absolute]


def require_clean(root: Path, paths: Sequence[str]) -> None:
    """Refuse unless every path is clean in the working tree and exists at HEAD."""
    rel = _relative_paths(root, paths)
    if not rel:
        return
    status = git_output(root, "status", "--porcelain", "--", *rel)
    dirty = [line[3:] for line in status.splitlines() if line.strip()]
    if dirty:
        raise ToolError(
            "working tree is dirty under: " + ", ".join(dirty)
            + "; commit before issuing a receipt"
        )
    for path in rel:
        try:
            git_output(root, "cat-file", "-e", f"HEAD:{path}")
        except HarnessError as exc:
            raise ToolError(f"input {path} is not committed at HEAD") from exc


def hash_inputs(root: Path, paths: Sequence[str]) -> Dict[str, str]:
    """Map each relative input path to the sha256 of its working-tree bytes."""
    hashes: Dict[str, str] = {}
    for rel in _relative_paths(root, paths):
        target = root / rel
        if not target.is_file():
            raise ToolError(f"input {rel} is not a file")
        hashes = {**hashes, rel: sha256_file(target)}
    return hashes


def draw_seed(arg: Optional[int]) -> Dict[str, Any]:
    """OS entropy when no argument is given; the argument otherwise."""
    if arg is None:
        return {"value": secrets.randbits(SEED_BITS), "source": "os-entropy"}
    return {"value": int(arg), "source": "argument"}


def _base_fields(
    ctx: ToolContext, entrant: str, argv: Sequence[str], inputs: Dict[str, str],
    seed: Dict[str, Any], verification_class: str,
    external_attestation: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    attestation = dict(external_attestation) if external_attestation is not None else None
    return {
        "entrant": entrant,
        "tool": ctx.tool_name,
        "tool_sha256": sha256_file(ctx.tool_path),
        "repo_commit": head_commit(ctx.root),
        "python_version": python_version(),
        "argv": list(argv),
        "inputs": dict(inputs),
        "input_sha256": sha256_bytes(canonical_json(inputs).encode("utf-8")),
        "seed": dict(seed),
        "verification_class": verification_class,
        "external_attestation": attestation,
        "started_utc": ctx.started_utc,
    }


def _issue(root: Path, base: Dict[str, Any], output: str, status: str,
           error: Optional[str]) -> Path:
    fields = {
        **base,
        "output": output,
        "output_sha256": sha256_bytes(output.encode("utf-8")),
        "status": status,
        "error": error,
        "completed_utc": utc_now(),
    }
    nonce = receipt_lib.mint_nonce(root)
    return receipt_lib.issue(root, nonce, **fields)


def _produce_text(produce: Callable[[], str]) -> str:
    output = produce()
    if not isinstance(output, str):
        raise TypeError(f"produce() must return str, got {type(output).__name__}")
    return output


def run_tool(
    ctx: ToolContext, entrant: str, argv: Sequence[str], inputs: Sequence[str],
    seed: Dict[str, Any], verification_class: str,
    external_attestation: Optional[Dict[str, Any]], produce: Callable[[], str],
) -> Tuple[str, Path]:
    """Standard lifecycle. Returns (output, receipt_path). Prints nothing."""
    rel_inputs = _relative_paths(ctx.root, inputs)
    require_clean(ctx.root, list(GUARDED_PATHS) + rel_inputs)
    hashes = hash_inputs(ctx.root, rel_inputs)
    base = _base_fields(ctx, entrant, argv, hashes, seed, verification_class,
                        external_attestation)
    try:
        output = _produce_text(produce)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        path = _issue(ctx.root, base, "", "failed", error)
        raise ToolError(f"{ctx.tool_name} failed: {error} (failed receipt: {path})") from exc
    path = _issue(ctx.root, base, output, "ok", None)
    return output, path


def replay_args(receipt: Dict[str, Any]) -> List[str]:
    """The argv a replaying tool must re-parse."""
    return [str(arg) for arg in receipt.get("argv", [])]


def add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add --entrant, --seed, --replay-of. Do not mark tool args required."""
    group = parser.add_argument_group("harness")
    group.add_argument("--entrant", help="entrant code, e.g. E1 (required unless --replay-of)")
    group.add_argument("--seed", type=int, help="seed value; recorded as seed.source=argument")
    group.add_argument("--replay-of", metavar="RECEIPT",
                       help="re-run a receipt: re-parse its argv, force its seed, write nothing")


def maybe_replay(parser: argparse.ArgumentParser, argv: Sequence[str]) -> Optional[Dict[str, Any]]:
    """Return the receipt to replay when --replay-of is present, else None."""
    known, _unknown = parser.parse_known_args(list(argv))
    target = getattr(known, "replay_of", None)
    if not target:
        return None
    try:
        return receipt_lib.load(Path(target))
    except ReceiptError as exc:
        raise ToolError(f"cannot replay: {exc}") from exc


def require_entrant(parser: argparse.ArgumentParser, args: argparse.Namespace) -> str:
    """Return the validated entrant code or raise ToolError."""
    entrant = getattr(args, "entrant", None)
    if not entrant:
        raise ToolError(f"{parser.prog}: --entrant is required unless --replay-of is given")
    if not receipt_lib.ENTRANT_CODE.match(entrant):
        raise ToolError(f"{parser.prog}: --entrant must be an uppercase code like E1, got {entrant!r}")
    return entrant


def emit(output: str) -> None:
    """Write output to stdout byte-exactly (no added newline)."""
    sys.stdout.buffer.write(output.encode("utf-8"))
    sys.stdout.flush()


def report_receipt(path: Path) -> None:
    sys.stderr.write(f"receipt: {path}\n")
    sys.stderr.flush()


def exit_on_error(main: Callable[[List[str]], int]) -> None:
    """Run a tool's main(argv) and turn HarnessError into `error: ...` + exit 1."""
    try:
        code = main(sys.argv[1:])
    except HarnessError as exc:
        sys.stderr.write(f"error: {exc}\n")
        sys.exit(1)
    sys.exit(int(code or 0))
