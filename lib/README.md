# Enactment harness — lib/ API

Phase 0 of `docs/tournament/enactment-harness-plan.md`. Existing core: Python 3.9+. Libraries are welcome under the user-approved dependency policy in CLAUDE.md.

## Lifecycle of a tool run

Every `bin/<tool>` follows one sequence, provided by `lib/tools.py`:

1. `add_common_args(parser)` adds `--entrant`, `--seed INT`, `--replay-of PATH`.
   Do not mark tool arguments `required`; replay re-parses the receipt's argv.
2. `maybe_replay(parser, argv)` returns the receipt to replay, or `None`.
3. `make_context(__file__)` records the repo root, tool name, tool path, start time.
4. `require_entrant(parser, args)` and `draw_seed(args.seed)`. No `--seed` draws
   `secrets.randbits(32)` (`seed.source = "os-entropy"`); a value records `"argument"`.
5. `run_tool(ctx, entrant, argv, inputs, seed, verification_class, external_attestation, produce)`:
   - refuses if any argv token resolves to an existing file that is not a declared
     input (`ToolError`) — an argv may not reach a file the receipt does not pin
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

`bin/verify replay <receipt>` **never reads the working tree**. It extracts
`git archive --format=tar <repo_commit>` into a temporary directory and runs
`sys.executable <tmp>/bin/<tool> --replay-of <absolute receipt path>` with that
directory as the working directory, then byte-compares stdout. Inside the archive it
checks:

- the archived `bin/<tool>` hashes to `tool_sha256` (FAIL otherwise). A working-tree
  tool that has since changed is a WARN — the replay ran the committed version.
- every `inputs` entry exists at `repo_commit` and hashes to the recorded value.
- no argv token resolves, relative to the archive root, to a file outside `inputs`
  ("argv names an undeclared file"). This is what the Phase 1 forger exploited: an
  `inputs` map pinning the honest pools file while `argv` named an uncommitted one.

A `status: failed` or `hash-attested` receipt is reported as not replayable and is not
a failure by itself. Because the archive has no `.git`, `lib.tools.make_context`
derives the repo root from the tool's own path, not from `git rev-parse`.

## The nonce

`lib/receipt.py` is the only receipt writer. `issue()` consumes a one-shot nonce that
`run_tool` mints into `docs/tournament/receipts/.nonce` immediately beforehand. Plan
section 4 states its purpose: the token, the chain, and single-use IDs are "a guardrail
against accidental misuse and lazy fabrication, not a boundary against a determined
forger." A subagent that imports `lib.receipt` directly is knowingly forging. The real
controls are deterministic replay, external attestation, and the orchestrator's commit.

## Receipt files

`<receipts dir>/<ENTRANT>/<NNN>-<receipt_id>.json`, immutable, chained by
`chain_prev` / `chain_hash` (sha256 of the canonical JSON of every other field).
`bin/verify chain <ENTRANT>` recomputes every hash and link. Sidecars
`<NNN>-<receipt_id>.bind.json` belong to the verifier and may be rewritten. An entrant
directory holds nothing else: any other file fails the gate ("foreign file in receipts
dir"), as does a sidecar with no receipt ("orphan sidecar").

### Where the receipts directory lives

`lib.paths.receipts_dir(root)` reads the environment variable `HARNESS_RECEIPTS_DIR`,
a path relative to the repo root, and falls back to `docs/tournament/receipts`. Tools
and every `bin/verify` mode go through it, so the whole harness moves together. The
default directory is reserved for the official round. Fixtures set the variable:

    HARNESS_RECEIPTS_DIR=docs/tournament/harness-fixtures/receipts \
      python3 bin/verify all --records 'docs/tournament/harness-fixtures/*.md' \
      --dispatch-log docs/tournament/harness-fixtures/dispatch-log.json

## Adding a binding rule

Create `lib/bindings/<tool_name>.py` (hyphens become underscores) exposing
`check(record_text: str, receipt: dict) -> BindResult` and
`VERIFICATION_CLASS` (`"replay-exact"` or `"hash-attested"`). The class lives in code,
not in the receipt: the gate fails a receipt that claims a class its tool does not
declare. Return `BindResult(passed,
bound_span, checks)` where `bound_span` is one sentence naming what the rule can check
and each `Check(name, expected, found, passed)` is one mechanical comparison. Ship a
negative fixture: a record that gestures at the output without deriving from it must
fail. `lib/bindings/_example.py` is the reference (output must appear verbatim).

`bin/verify bind <record.md> <receipt.json>` runs the rule and writes the sidecar.
`bin/verify all [--records GLOB]` runs chain, class, replay, single-use citation
(`## Receipts` bullets in each record, exactly one citing record, entrant code must
match), and bind for every receipt. It re-runs bind every time and rewrites a sidecar
whenever the result or the record hash differs; it never trusts a stored result.
With `--dispatch-log PATH` (a committed, clean JSON
`{"entries": [{"entrant", "seed", "inputs", ...}]}` that the orchestrator wrote before
dispatch, plan section 4) every `ok` receipt's seed must be `source: argument` and its
`(entrant, seed)` pair must appear in the log, and the receipt's `inputs` must equal
that entry's `inputs` exactly (an absent `inputs` means `{}`). Otherwise the gate fails.
Without the flag an OS-entropy seed only warns and the `seed` column reads `unattested`.

## Tests

    python3 -m pytest tests -q

`tests/conftest.py` builds a throwaway git repo with a copy of `bin/` and `lib/`, a test
tool `bin/echo-tool`, and `lib/bindings/echo_tool.py` (an alias of the example rule) so
`verify all` can bind it. Tools run as subprocesses from that repo's root.

## Pre-persona pipeline (Phase 2)

`bin/prepare --entrant A1 --adapter transform --brief docs/tournament/tail-test-s16.txt
--config docs/tournament/pipeline/a1-transforms.json --persona nuclear-reactor-operator
--seed 1` follows the standard lifecycle. Use C8/mask or A5/withhold with the corresponding
config and omit persona. Both input files must be committed before a receipt is issued.
The deterministic adapters record a seed for dispatch attestation but do not use it.

Only the `PERSONA-VISIBLE INPUT` payload belongs in the persona context. The transform
record and withheld-fact config are audit material, not persona input. Store verbatim
payload/audit evidence in `## Execution trace`; proposals use `## Abstract proposal`
(mask) or `## Pass 1 proposal artifact` (transform/withhold). The binding check requires
at least ten numbered proposal lines, checks frozen-wordlist leaks, and rejects raw brief
sentences outside the trace. Verbatim presence is not proof of isolation or causal use.
