# A3 persona toolbelts

These four CLIs perform the data-producing parts of A3. `churn` counts how many commits
touched each path in the preceding two years; `seasons` bins those commits by calendar
month; `units` converts and dimension-checks quantities with Pint; `orders` computes
positive ratios and their base-10 order gaps. Every result is deterministic JSON and
uses the standard receipt and replay lifecycle.

## Dependency

`bin/units` requires exactly `Pint==0.26.1`. The pinned version is a consumed field in
`units.json` and is also emitted in the result. This makes a dependency drift visible as
a failed run or replay rather than silently changing a receipt. The other three tools
use the Python standard library. All source syntax retains the Python 3.9 floor; the
official runtime must also support the pinned Pint version.

## History snapshot boundary

An archive replay has no access to the source repository's `.git` directory. Before
dispatch, the orchestrator collects real history at the chosen source commit:

```text
python3 scripts/snapshot-toolbelt-history.py \
  --repo . \
  --commit 192581631d646dadfbdc5c0e120d2b060b618b0f \
  --source-label https://github.com/blakeyoh/temp-agency \
  --output docs/tournament/toolbelts/temp-agency-history-1925816.json
```

The collector resolves the exact commit, anchors a two-year interval to that commit's
committer timestamp, reads every reachable commit and its changed paths, and writes origin
and limitation fields. A root commit uses `git diff-tree --root`; every other commit is
diffed against its first parent, so merge-resolution changes are retained while a combined
parent view is deliberately excluded. Commit the snapshot before drawing and include its
path/hash in the dispatch log. `churn` and `seasons` consume only that pinned JSON.

Example runs after the configs, snapshot, seed and input hashes are committed:

```text
python3 bin/churn --entrant A3 --seed 101 --config docs/tournament/toolbelts/churn.json --snapshot docs/tournament/toolbelts/temp-agency-history-1925816.json
python3 bin/seasons --entrant A3 --seed 102 --config docs/tournament/toolbelts/seasons.json --snapshot docs/tournament/toolbelts/temp-agency-history-1925816.json
python3 bin/units --entrant A3 --seed 103 --config docs/tournament/toolbelts/units.json
python3 bin/orders --entrant A3 --seed 104 --config docs/tournament/toolbelts/orders.json
```

## Record binding

Every credited A3 receipt must have one block in the record's sole `## Credited tools`
section. The invocation JSON is the normalized receipt `argv` and tool name. The raw
result is the receipt's output byte-for-byte, including its final newline:

````text
## Credited tools

### abcdef123456

Invocation:

```json
{
  "argv": ["--entrant", "A3", "--seed", "101", "--config", "..."],
  "tool": "bin/churn"
}
```

Raw result:

```json
{...exact stdout...}
```
````

The binding rule discovers receipt files through `lib.paths.receipts_dir(root)`. It
rejects missing blocks, uncited or nonexistent receipt IDs, duplicate or malformed
blocks, altered invocations, altered raw results, failed receipts and non-A3 tools.
