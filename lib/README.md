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

## Advanced runtime (Phases 3–4)

The original core keeps its Python 3.9 syntax floor. Full verification now requires the
pinned Python 3.13 runtime libraries and local semantic model, currently validated on
macOS arm64 CPU. Use a durable virtual environment outside the checkout:

```sh
python3.13 -m venv ~/.cache/temp-agency/harness-py313
~/.cache/temp-agency/harness-py313/bin/pip install -r requirements-harness.lock
~/.cache/temp-agency/harness-py313/bin/python scripts/setup-semantic-model.py \
  --manifest docs/tournament/overlap/model.json --cache ~/.cache/temp-agency/models
~/.cache/temp-agency/harness-py313/bin/python -m pytest tests -q
```

`~/.cache/temp-agency/models` is the default `HARNESS_MODEL_CACHE` location, so once it
is populated no env var is needed; set `HARNESS_MODEL_CACHE` only to point at a different
cache. Model setup is an explicit network operation. Inference and replay only use
verified local assets. The manifest pins hashes, package versions and platform; drift
fails closed.
Python 3.9 core compatibility can be checked with `python3 -m pytest tests
--ignore=tests/test_toolbelts.py -q`; model-dependent tests skip when their runtime is
unavailable, so that command is not a substitute for full advanced verification.

A3 documentation is in `docs/tournament/toolbelts/README.md`. M1's scorer and limits are
in `docs/tournament/overlap/README.md`. `bin/seal-median` authenticates earlier git blobs
and context hashes before M1 comparison; it does not prove hidden model context.
A hash-attested binding may export `verify_attestation(root, receipt) -> list[str]`.
The full gate invokes that hook independently for successful receipts and rejects any
reported problem. Failed receipts never count as authenticated median evidence.

C5 uses `bin/notation --mode select --catalog PATH`, then commits the resulting selection
receipt before artifact authoring. `--mode validate --catalog PATH --selection RECEIPT
--artifact PATH` checks the committed authored structure. Supply entrant and seed on each
call. The record must reproduce both outputs in `## Execution trace` and translate the
notation into numbered `## Pass 1 proposal artifact` items prefixed `[notation-item-id]`.
Both selection and validation receipts must be cited. Slot failure forbids a passing bind.


## E2 independent evaluation gate

After the committed corpus draw and `bin/forage` fetch, save the exact returned artifact
and freeze a candidate JSON (`schema_version: 1`, ordered `items` with `id` and `text`).
The independent OpenRouter request uses `lib.forage_audit.EVALUATOR_BRIEF`, output mode
`critique`, no added constraints/acceptance criteria, and exactly four context files.
Use the fixed purpose strings in `CONTEXT_PURPOSES` for brief, artifact, candidate and
rubric. The generator must not make this judgment in its own invocation.

Persist the complete response and manifest. Run `scripts/record-forage-evaluation.py`
with `--manifest`, `--response`, `--brief`, `--artifact`, `--candidate`, `--rubric`,
`--generator-actor`, `--mode development|official`, `--attest-independent` and `--out`.
This records the host's isolation attestation; it is not a receipt writer. Commit all
inputs and this invocation. Make a later dispatch commit, then invoke `bin/forage-gate`
with `--entrant E2`, `--seal-commit` (full prior commit ID), the six named evaluation file inputs,
`--invocation`, and `--fetch-receipt` pointing to the actual successful source receipt.
All tool input paths are repository-relative.

A well-formed negative semantic verdict creates an ok receipt whose result is false;
malformed evidence creates a failed receipt. Regenerate every rejected item, preserve
IDs, reevaluate the complete candidate in a fresh request, and include the actual prior
gate receipt through `--previous` in the next sealed round. Cite every round and fetch
in the record, retain their exact outputs in Execution trace, and render the accepted
candidate as numbered `1. [item-id] text` items in Pass 1 proposal artifact. At least
three must survive and no rejected item may remain. The enclosing packet enforces the
brief's final item count; this generic gate also supports smaller development subsets.

The full gate checks the independently resolving source plus the evaluator evidence and
lineage. A development probe artifact without a real fetch receipt cannot be promoted
into an enacted record by writing an evaluation file.

## E6 oblique draw

`bin/oblique --entrant E6 --seed N` consumes the committed full-corpus deck at
`docs/tournament/deck/cards.json` and every real positions pack. It samples two packs
(default), excludes cards 1-10 of each pack and draws from the remaining cards.
`--pack-count` changes the number of sampled packs; no preferred-pack selector exists.
Changed source hashes or incomplete corpus coverage reject the draw. Full output belongs
in Execution trace and the exact selected card belongs in Mechanism output. Binding
verifies those bytes, not obedience in generated prose. See the deck README for provenance.

## E4 crossover builder

`bin/breed --entrant E4 --parent-a roster/<a>.md --parent-b roster/<b>.md --seed N`
performs a deterministic, crossover-only build. It takes `Core Principles` from parent A,
`Methodology` from parent B, and interleaves both parents' `Anti-Patterns` blocks using the
seed. Parents must be distinct, and the selected methodology must contain at least two
numbered phases. The receipt is replay-exact and pins both parent hashes.

Put the complete receipt output in Execution trace. In Mechanism output, preserve the
canonical JSON object `{"child": <exact child string>}`; this keeps the child's Markdown
headings from being confused with the surrounding record sections.

The child is a one-task crossover fragment. Point mutation, child scoring, promotion, and
death history are deliberately outside this executable and its binding rule; it does not
implement the complete breeding lifecycle described by the original entrant proposal.

## E5 dated specialist checker

`bin/lexicon-check --entrant E5 --lexicon docs/tournament/eras/1911.json \
  --profile roster/<specialist>.md --candidate <candidate.json> \
  --specialist <specialist> --era 1911 [--previous <receipt.json>]`
checks candidate items against the frozen era lexicon and emits a replay-exact receipt.
The current supported era is 1911. All 24 real roster profiles are eligible in the frozen
configuration. Matching normalizes Unicode with NFKC and permits punctuation, underscore,
and whitespace variants around multiword terms. A rejected candidate can be regenerated
with `--previous`; the binding requires one retained, non-forked chain, preserves item IDs,
requires every leaking item to change, and requires the final leak-free candidate to match
the proposal.

The 1911 list is a model-authored surface blacklist preserved from the scrimmage. It catches
those frozen terms and their normalized variants, not conceptual anachronisms or every term
that could be historically unavailable. The era metadata is experimental dispatch
eligibility, not a claim that the modern role existed in 1911.

## E3 opposite-specialist routing

`bin/route --entrant E3 --brief <brief> --index references/roster.md \
  --domain-specialist <lens>` routes against the complete built roster. It validates that
the roster index and actual profile corpus contain the same 24 built specialists, computes
unique word-token Jaccard overlap after NFKC normalization and frozen stopwords, and chooses
the lowest-scoring eligible profile with slug-ascending tie-breaking. The supplied domain
specialist is recorded as the LENS and excluded from LEAD selection; that supplied choice is
not independently classified by the tool. The receipt is replay-exact and pins the brief,
index, and all profile hashes.

The binding verifies the recorded corpus, scores and exact LEAD/LENS labels, then requires
an accepted independent evaluation chain from `bin/frame-gate`. Routing alone cannot pass.
The frame gate reuses E2's sealed evidence, per-item verdict and regeneration checks.

Phase 5 focused verification for these three tools totals 20 tests: 5 for E4, 9 for E5,
and 6 for E3. The integrated suite passed 250 tests; subsequent E3 label hardening passed nine focused
route tests, including three new cases. See the Phase 5 contract-review note for pending
mechanism choices.


### E3 independent frame gate

Export the actual route with `scripts/export-routed-frame.py --route-receipt <receipt>
--out <artifact.json>`. It derives the routed LEAD from the receipt's git commit, checks
the source hash and removes only double-asterisk Markdown markers for quote-friendly
text. The original profile hash remains in the artifact. No source facts are rewritten.

Evaluate the final candidate after LENS input using exactly four attachments: the exact
routed brief, exported artifact, candidate JSON and `docs/tournament/route/evaluator-rubric.md`.
Use `lib.frame_audit.EVALUATOR_BRIEF` and `lib.forage_audit.CONTEXT_PURPOSES` in the request.
Use `scripts/record-frame-evaluation.py` with the same file options as the E2 helper to
record the separate evaluator invocation. Commit those inputs, the response, manifest,
invocation and actual route receipt, then make a later dispatch commit.

Invoke `bin/frame-gate --entrant E3 --seal-commit <prior-full-commit>` with `--brief`,
`--artifact`, `--candidate`, `--rubric`, `--response`, `--manifest`, `--invocation` and
`--route-receipt`. Use `--previous` for regeneration rounds. Preserve every round in
Execution trace and Receipts. The final numbered proposal must match the accepted
candidate exactly, with stable item IDs. At least three items must survive and no
unchanged/indeterminate item may remain. There is no larger creativity-scoring system.

E4's crossover-only scope and E5's instruction-plus-1911-wordlist scope were confirmed
by the commissioner. E5 gets no additional independent concept-review step.
