# Frozen era configurations

`1911.json` is the current frozen era configuration for E5. It supports experimental
dispatch eligibility for all 24 real roster profiles, with each profile eligible only for
era 1911. The ranges do not assert that the modern specialist roles existed in that year.

The file preserves a model-authored surface blacklist from the E5 scrimmage. The checker
normalizes candidate text and terms with Unicode NFKC and detects punctuation, underscore,
and whitespace variants of the listed terms. This is a conservative lexical screen, not a
historical dictionary: it does not identify every conceptual anachronism or prove that a
candidate has reasoned from period-appropriate primitives.

Run the checker from the repository root with:

```sh
bin/lexicon-check --entrant E5 \
  --lexicon docs/tournament/eras/1911.json \
  --profile roster/<specialist>.md \
  --candidate <candidate.json> \
  --specialist <specialist> --era 1911
```

When a candidate leaks terms, regenerate it with the prior successful receipt supplied via
`--previous`. The binding preserves every rejected round in one retained regeneration chain,
requires stable item IDs and changed leaking items, and checks that the final accepted
candidate is the proposal. There is no supported era other than the frozen 1911 configuration
at present.
