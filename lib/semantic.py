"""Pinned offline natural-language inference for replayable semantic comparisons."""
from __future__ import annotations

import importlib.metadata
import os
import platform
import re
from functools import lru_cache
from pathlib import Path

from lib.paths import canonical_json, sha256_file

CACHE_ENV = "HARNESS_MODEL_CACHE"
RULE_PREFIX = "The proposed rule is: "
REQUIRED_FILES = {"config.json", "model.safetensors", "tokenizer.json",
                  "tokenizer_config.json", "added_tokens.json", "special_tokens_map.json", "spm.model"}
REQUIRED_RUNTIME = {"sentence-transformers", "torch", "transformers", "tokenizers",
                    "numpy", "safetensors", "scipy", "scikit-learn"}


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise ValueError("unsupported semantic model manifest")
    if manifest.get("model_id") != "cross-encoder/nli-deberta-v3-base":
        raise ValueError("unsupported model architecture; calibrate before adding a model")
    if not re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("revision", ""))):
        raise ValueError("model revision must be an immutable commit")
    files = manifest.get("files")
    if not isinstance(files, dict) or set(files) != REQUIRED_FILES:
        raise ValueError("model manifest must pin the complete inference file set")
    if not all(isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v) for v in files.values()):
        raise ValueError("invalid model file hash")
    runtime = manifest.get("runtime")
    if not isinstance(runtime, dict) or set(runtime) != REQUIRED_RUNTIME:
        raise ValueError("model manifest must pin every inference runtime dependency")
    if not all(isinstance(v, str) and v for v in runtime.values()):
        raise ValueError("runtime dependency versions must be nonempty strings")
    if manifest.get("device") != "cpu" or manifest.get("max_tokens") != 512:
        raise ValueError("semantic runtime requires CPU and the calibrated 512-token limit")
    if manifest.get("labels") != ["contradiction", "entailment", "neutral"]:
        raise ValueError("unexpected NLI label mapping")


def model_directory(manifest):
    validate_manifest(manifest)
    base = Path(os.environ.get(CACHE_ENV, str(Path.home() / ".cache/temp-agency/models")))
    if not base.is_absolute():
        raise ValueError("HARNESS_MODEL_CACHE must be absolute for archive replay")
    directory = base / manifest["revision"]
    for name, digest in manifest["files"].items():
        path = directory / name
        if not path.is_file() or sha256_file(path) != digest:
            raise ValueError("missing or changed semantic model file: %s; run setup-semantic-model.py" % name)
    actual = {p.relative_to(directory).as_posix() for p in directory.rglob("*") if p.is_file()}
    if actual != REQUIRED_FILES:
        raise ValueError("unmanifested files in semantic model cache")
    return directory


def check_runtime(manifest):
    for name, wanted in manifest["runtime"].items():
        try:
            actual = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError as exc:
            raise ValueError("install the pinned semantic runtime: missing %s" % name) from exc
        if actual != wanted:
            raise ValueError("semantic runtime drift: %s %s != %s" % (name, actual, wanted))
    expected = manifest.get("platform")
    if expected != {"system": platform.system(), "machine": platform.machine()}:
        raise ValueError("semantic runtime platform differs; validate and pin a new manifest")


@lru_cache(maxsize=1)
def _load(directory, identity):
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    tokenizer = AutoTokenizer.from_pretrained(directory, local_files_only=True, trust_remote_code=False)
    model = AutoModelForSequenceClassification.from_pretrained(
        directory, local_files_only=True, trust_remote_code=False,
        attn_implementation="eager", use_safetensors=True)
    model.to("cpu")
    model.eval()
    if model.config.id2label != {0: "contradiction", 1: "entailment", 2: "neutral"}:
        raise ValueError("model label mapping differs from calibrated NLI contract")
    return tokenizer, model


def _directional_score(tokenizer, model, first, second, limit):
    import torch

    inputs = tokenizer(RULE_PREFIX + first, RULE_PREFIX + second,
                       truncation=False, return_tensors="pt")
    if inputs["input_ids"].shape[1] > limit:
        raise ValueError("semantic pair exceeds 512 tokens; split into complete claim sections")
    with torch.inference_mode():
        probabilities = torch.softmax(model(**inputs).logits, dim=-1)
    return float(probabilities[0, 1])


def entailment_scores(pairs, manifest):
    """Score semantic inclusion in either direction, with a fixed rule framing.

    A more specific rendition of a generic claim still overlaps that claim. This
    is a model-based score, not proof of logical equivalence or causal novelty.
    """
    directory = model_directory(manifest)
    check_runtime(manifest)
    tokenizer, model = _load(str(directory), canonical_json(manifest))
    result = []
    for candidate, median in pairs:
        forward = _directional_score(tokenizer, model, candidate, median, manifest["max_tokens"])
        backward = _directional_score(tokenizer, model, median, candidate, manifest["max_tokens"])
        result.append(max(forward, backward))
    return result
