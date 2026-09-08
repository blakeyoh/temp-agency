# Enactment harness — lib/ API

Phase 0 of `docs/tournament/enactment-harness-plan.md`. Python 3.9+, stdlib only.

## Lifecycle of a tool run

Every `bin/<tool>` follows one sequence, provided by `lib/tools.py`:

1. `add_common_args(parser)` adds `--entrant`, `--seed INT`, `--replay-of PATH`.
   Do not mark tool arguments `required`; replay re-parses the receipt's argv.
2. `maybe_replay(parser, argv)` returns the receipt to replay, or `None`.
3. `make_context(__file__)` records the repo root, tool name, tool path, start time.
4. `require_entrant(parser, args)` and `draw_seed(args.seed)`. No `--seed` draws
   `secrets.randbits(32)` (`seed.source = "os-entropy"`); a value records `"argument"`.
5. `run_tool(ctx, entrant, argv, inputs, seed, verification_class, external_attestation, produce)`:
   - refuses if `git status --porcelain -- bin lib <inputs>` is non-empty (`ToolError`)
   - refuses if any input is not committed at HEAD (`ToolError`)
   - hashes inputs, calls `produce()`, mints the nonce, issues the receipt
   - if `produce()` raises, issues a `status: failed` receipt and re-raises as `ToolError`
   - prints nothing; returns `(output, receipt_path)`
6. The tool calls `emit(output)` (stdout, byte-exact) and `report_receipt(path)` (stderr).

Wrap `main(argv)` in `exit_on_error(main)`: a `HarnessError` becomes `error: ...` and exit 1.

## Replay contract

`bin/<tool> --replay-of <receipt.json>` re-parses `receipt["argv"]`, forces the seed to
`receipt["seed"]`, prints the output to stdout, and writes no receipt and no nonce.
`bin/verify replay <receipt>` pins `tool_sha256`, every input (working tree and
`git show <repo_commit>:<path>`), warns on an interpreter change, then runs the replay
with `sys.executable` and byte-compares stdout. A `status: failed` or `hash-attested`
receipt is reported as not replayable and is not a failure by itself.

## The nonce

`lib/receipt.py` is the only receipt writer. `issue()` consumes a one-shot nonce that
`run_tool` mints into `docs/tournament/receipts/.nonce` immediately beforehand. Plan
section 4 states its purpose: the token, the chain, and single-use IDs are "a guardrail
against accidental misuse and lazy fabrication, not a boundary against a determined
forger." A subagent that imports `lib.receipt` directly is knowingly forging. The real
controls are deterministic replay, external attestation, and the orchestrator's commit.

## Receipt files

`docs/tournament/receipts/<ENTRANT>/<NNN>-<receipt_id>.json`, immutable, chained by
`chain_prev` / `chain_hash` (sha256 of the canonical JSON of every other field).
`bin/verify chain <ENTRANT>` recomputes every hash and link. Sidecars
`<NNN>-<receipt_id>.bind.json` belong to the verifier and may be rewritten.

## Adding a binding rule

Create `lib/bindings/<tool_name>.py` (hyphens become underscores) exposing
`check(record_text: str, receipt: dict) -> BindResult`. Return `BindResult(passed,
bound_span, checks)` where `bound_span` is one sentence naming what the rule can check
and each `Check(name, expected, found, passed)` is one mechanical comparison. Ship a
negative fixture: a record that gestures at the output without deriving from it must
fail. `lib/bindings/_example.py` is the reference (output must appear verbatim).

`bin/verify bind <record.md> <receipt.json>` runs the rule and writes the sidecar.
`bin/verify all [--records GLOB]` runs chain, class, replay, single-use citation
(`## Receipts` bullets in each record, exactly one citing record, entrant code must
match), and bind for every receipt. It re-runs bind every time and rewrites a sidecar
whenever the result or the record hash differs; it never trusts a stored result.
With `--dispatch-log PATH` (a committed, clean JSON `{"entries": [{"entrant", "seed", ...}]}`
that the orchestrator wrote before dispatch, plan section 4) every `ok` receipt's seed must
be `source: argument` and present in the log for its entrant, or the gate fails. Without
the flag an OS-entropy seed only warns and the `seed` column reads `unattested`.

## Tests

    python3 -m pytest tests -q

`tests/conftest.py` builds a throwaway git repo with a copy of `bin/` and `lib/`, a test
tool `bin/echo-tool`, and `lib/bindings/echo_tool.py` (an alias of the example rule) so
`verify all` can bind it. Tools run as subprocesses from that repo's root.
