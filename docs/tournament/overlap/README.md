# M1 semantic overlap development runtime

M1 uses semantic comparison, as approved by the commissioner. The current development
scorer is a pinned local NLI model, `cross-encoder/nli-deberta-v3-base`, at revision
`6c749ce3425cd33b46d187e45b92bbf96ee12ec7` (the authoritative full revision
is in `model.json`). Model assets are SHA-256 pinned individually in that manifest.

Install the Python 3.13 environment from the repository's `requirements-harness.lock`,
then run `scripts/setup-semantic-model.py --help` for the explicit asset setup command.
Inference is offline: it requires existing verified assets in `HARNESS_MODEL_CACHE`.
Missing assets, altered bytes, runtime version drift and oversized inputs fail closed;
there is no lexical fallback or automatic network download during receipt execution.
The current runtime manifest pins macOS arm64 CPU execution. Other platforms need a
separately validated manifest before receipt generation; do not silently relax its pins.

Both candidate and median sentences receive the fixed prefix `The proposed rule is: `.
The score is the maximum entailment probability in both directions. This detects a
specific restatement of a more general median claim as well as a general restatement
of a specific one. Scores are rounded to six decimals. Only median claims labeled
CHOSEN cause rejection, at or above the committed threshold of 0.7. FORCED claims
are scored for visibility but do not trigger rejection.

The development calibration file contains 16 labeled examples split into calibration
and holdout sets. This small fixture checks paraphrases, opposite rules and unrelated
ideas. It is not a general accuracy estimate or proof of originality. An earlier
embedding cosine probe ranked a contradictory proposal above a true paraphrase; that
approach was discarded. NLI is also fallible, so the model, fixed prefix, direction
rule, threshold and calibration evidence must be frozen before official dispatch.

`bin/overlap` consumes four distinct committed JSON files: median, candidate, config
and model manifest. Receipt replay recomputes every score in a git archive using the
same verified local model dependency. Binding requires the full report and exact
numbered final proposal text; putting checked text only in the trace is insufficient.
The separate median-seal attestation integration is still under development.

Model documentation: https://huggingface.co/cross-encoder/nli-deberta-v3-base
