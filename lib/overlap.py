"""M1 comparison: semantic similarity, with only CHOSEN overlap rejecting a section."""
from __future__ import annotations

import math
import re

from lib.semantic import entailment_scores, validate_manifest

ID = re.compile(r"[A-Za-z0-9_-]{1,64}")


def items(document, key, labeled=False):
    rows = document.get(key) if isinstance(document, dict) else None
    if not isinstance(rows, list) or not 1 <= len(rows) <= 100:
        raise ValueError("%s must contain 1..100 items" % key)
    seen = set()
    for row in rows:
        fields = {"id", "text", "label"} if labeled else {"id", "text"}
        if not isinstance(row, dict) or set(row) != fields:
            raise ValueError("each %s item must have exactly %s" % (key, sorted(fields)))
        if not isinstance(row["id"], str) or not ID.fullmatch(row["id"]) or row["id"] in seen:
            raise ValueError("%s IDs must be valid and unique" % key)
        if not isinstance(row["text"], str) or not row["text"].strip():
            raise ValueError("%s text must be nonempty" % key)
        if labeled and row["label"] not in ("FORCED", "CHOSEN"):
            raise ValueError("median labels must be FORCED or CHOSEN")
        seen.add(row["id"])
    return rows


def threshold(config):
    if not isinstance(config, dict) or config.get("schema_version") != 1:
        raise ValueError("invalid overlap config")
    if config.get("metric") != "bidirectional-entailment-max" or config.get("decimals") != 6:
        raise ValueError("unsupported semantic metric or precision")
    value = config.get("threshold")
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("overlap threshold must be finite")
    if not 0 < value <= 1 or round(value, 6) != value:
        raise ValueError("threshold must be in (0, 1] with at most six decimal places")
    return value


def decisions(claims, sections, probabilities, cutoff):
    output = []
    for index, section in enumerate(sections):
        scores = [{"claim_id": claim["id"], "label": claim["label"],
                   "score": round(probabilities[index * len(claims) + j], 6)}
                  for j, claim in enumerate(claims)]
        rejected = [s["claim_id"] for s in scores if s["label"] == "CHOSEN" and s["score"] >= cutoff]
        output.append({"section_id": section["id"], "scores": scores,
                       "decision": "REJECT" if rejected else "KEEP", "overlapping_chosen": rejected})
    return output


def compare(median, candidate, config, manifest):
    claims, sections = items(median, "claims", True), items(candidate, "sections")
    cutoff = threshold(config)
    validate_manifest(manifest)
    probabilities = entailment_scores([(section["text"], claim["text"])
                                     for section in sections for claim in claims], manifest)
    if any(not math.isfinite(p) or not 0 <= p <= 1 for p in probabilities):
        raise ValueError("non-finite or invalid entailment probability")
    rows = decisions(claims, sections, probabilities, cutoff)
    return {"metric": config["metric"], "threshold": cutoff, "decimals": 6,
            "sections": rows, "passed": all(row["decision"] == "KEEP" for row in rows)}
