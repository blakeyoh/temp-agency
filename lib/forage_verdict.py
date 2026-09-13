"""Deterministic E2 verdict enforcer.

This module enforces supplied (independently authored) model verdicts
against structural and evidence-quoting rules. It does NOT independently
prove or judge causal dependence of any item; it only verifies that the
supplied semantic verdict is well-formed, fully covers every candidate
item, and is backed by verbatim quotes from the candidate and the
verified artifact text. Passing requires zero rejected items and at
least MINIMUM_SURVIVORS (3) dependent survivors, a fixed policy minimum.
"""

import re

SCHEMA_VERSION = 1
MINIMUM_SURVIVORS = 3
DECISIONS = frozenset(("dependent", "unchanged", "indeterminate"))
_ID_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$")
_QUOTE_MIN = 12
_REASON_MIN = 20
_MAX_ITEMS = 100


def _fail(msg):
    raise ValueError(msg)


def _require_exact_keys(obj, expected, ctx):
    if not isinstance(obj, dict):
        _fail("%s must be an object" % ctx)
    keys = set(obj)
    extra = keys - expected
    if extra:
        _fail("%s has unknown fields: %s" % (ctx, sorted(extra)))
    missing = expected - keys
    if missing:
        _fail("%s missing fields: %s" % (ctx, sorted(missing)))


def _nonempty_str(v, ctx):
    if not isinstance(v, str) or not v:
        _fail("%s must be a nonempty string" % ctx)
    if v != v.strip():
        _fail("%s must have no leading/trailing whitespace" % ctx)
    return v


def _check_schema_version(value, ctx):
    if isinstance(value, bool) or not isinstance(value, int):
        _fail("%s schema_version must be int (not bool)" % ctx)
    if value != SCHEMA_VERSION:
        _fail("%s schema_version must be %d" % (ctx, SCHEMA_VERSION))


def _validate_candidate(candidate):
    _require_exact_keys(candidate, {"schema_version", "items"}, "candidate")
    _check_schema_version(candidate["schema_version"], "candidate")
    items = candidate["items"]
    if not isinstance(items, list) or not 1 <= len(items) <= _MAX_ITEMS:
        _fail("candidate.items must be a list of 1..%d items" % _MAX_ITEMS)
    seen = set()
    out = []
    for idx, item in enumerate(items):
        ctx = "candidate.items[%d]" % idx
        _require_exact_keys(item, {"id", "text"}, ctx)
        item_id = _nonempty_str(item["id"], ctx + ".id")
        if not _ID_RE.match(item_id):
            _fail("%s.id fails safe-id pattern" % ctx)
        if item_id in seen:
            _fail("duplicate candidate id: %s" % item_id)
        seen.add(item_id)
        _nonempty_str(item["text"], ctx + ".text")
        out.append((item_id, item["text"]))
    return out


def _quote_ok(quote, source, ctx, allow_empty):
    if quote == "":
        if allow_empty:
            return
        _fail("%s must be nonempty for dependent decisions" % ctx)
    if not isinstance(quote, str):
        _fail("%s must be a string" % ctx)
    if quote != quote.strip():
        _fail("%s must have no surrounding whitespace" % ctx)
    if quote not in source:
        _fail("%s is not a verbatim substring of its source" % ctx)
    if len(quote) < _QUOTE_MIN and quote != source:
        _fail("%s must be >= %d chars or the entire source" % (ctx, _QUOTE_MIN))


def _validate_row(row, item_id, text, artifact_text, idx):
    ctx = "evaluation.verdicts[%d]" % idx
    _require_exact_keys(
        row,
        {"item_id", "decision", "proposal_quote", "artifact_quote",
         "deletion_effect", "reason"},
        ctx,
    )
    if row["item_id"] != item_id:
        _fail("%s.item_id must match candidate order (%r)" % (ctx, item_id))
    decision = row["decision"]
    if not isinstance(decision, str) or decision not in DECISIONS:
        _fail("%s.decision must be one of %s" % (ctx, sorted(DECISIONS)))
    proposal_quote = row["proposal_quote"]
    if not isinstance(proposal_quote, str):
        _fail("%s.proposal_quote must be a string" % ctx)
    _quote_ok(proposal_quote, text, ctx + ".proposal_quote", allow_empty=False)
    artifact_quote = row["artifact_quote"]
    if not isinstance(artifact_quote, str):
        _fail("%s.artifact_quote must be a string" % ctx)
    _quote_ok(
        artifact_quote, artifact_text, ctx + ".artifact_quote",
        allow_empty=(decision != "dependent"),
    )
    for field in ("deletion_effect", "reason"):
        val = row[field]
        if not isinstance(val, str) or len(val.strip()) < _REASON_MIN or val != val.strip():
            _fail(
                "%s.%s must be a nonempty string of >= %d chars"
                % (ctx, field, _REASON_MIN)
            )


def evaluate(candidate, evaluation, artifact_text):
    """Enforce a supplied model verdict deterministically.

    Verifies structure, complete per-item coverage in candidate order,
    and verbatim evidence quoting. Rejects every unchanged/indeterminate
    item. Returns {'passed', 'minimum_survivors', 'survivors',
    'rejected', 'verdicts'}. Raises ValueError on malformed input only;
    well-formed negative verdicts return passed=False without raising.
    This function cannot independently prove causal dependence.
    """
    if not isinstance(candidate, dict):
        _fail("candidate must be an object")
    if not isinstance(evaluation, dict):
        _fail("evaluation must be an object")
    if not isinstance(artifact_text, str) or not artifact_text:
        _fail("artifact_text must be a nonempty string")

    items = _validate_candidate(candidate)

    _require_exact_keys(evaluation, {"schema_version", "verdicts"}, "evaluation")
    _check_schema_version(evaluation["schema_version"], "evaluation")
    verdicts = evaluation["verdicts"]
    if not isinstance(verdicts, list):
        _fail("evaluation.verdicts must be a list")
    if len(verdicts) != len(items):
        _fail(
            "evaluation.verdicts must contain exactly one row per candidate item"
        )

    for idx, (row, (item_id, text)) in enumerate(zip(verdicts, items)):
        if not isinstance(row, dict):
            _fail("evaluation.verdicts[%d] must be an object" % idx)
        _validate_row(row, item_id, text, artifact_text, idx)

    survivors = []
    rejected = []
    for row in verdicts:
        if row["decision"] == "dependent":
            survivors.append(row["item_id"])
        else:
            rejected.append(row["item_id"])

    passed = (not rejected) and len(survivors) >= MINIMUM_SURVIVORS
    return {
        "passed": passed,
        "minimum_survivors": MINIMUM_SURVIVORS,
        "survivors": survivors,
        "rejected": rejected,
        "verdicts": verdicts,
    }
