"""Bind M1's semantic report to the exact sections allowed into the final artifact."""
from __future__ import annotations

import json
import re

from lib.bindings import BindResult, Check, cited_receipt_ids
from lib.errors import HarnessError
from lib.overlap import compare, items
from lib.paths import canonical_json, repo_root, sha256_file, git_output
from lib.receipt import list_receipts, load
from lib.median_seal import verify_attestation

VERIFICATION_CLASS = "replay-exact"
BOUND_SPAN = ("semantic scores recompute from pinned median and candidate; every candidate "
              "section exactly matches a numbered final proposal item; no section exceeds the CHOSEN overlap threshold")
NAMES = ("report_verbatim", "sections_verbatim", "semantic_gate")
FIELDS = ("median", "candidate", "config", "model_manifest")


def load_documents(receipt, output):
    root = repo_root()
    paths = output.get("inputs")
    if not isinstance(paths, dict) or set(paths) != set(FIELDS):
        raise ValueError("overlap output must name exactly its four inputs")
    if len(set(paths.values())) != 4 or set(paths.values()) != set(receipt["inputs"]):
        raise ValueError("overlap inputs do not match receipt")
    documents = []
    for key in FIELDS:
        path = (root / paths[key]).resolve()
        path.relative_to(root.resolve())
        if sha256_file(path) != receipt["inputs"][paths[key]]:
            raise ValueError("overlap binding input changed")
        documents.append(json.loads(path.read_text(encoding="utf-8")))
    return documents


def final_sections_match(record_text, sections):
    """Only numbered final proposal items count; trace copies cannot satisfy binding."""
    bodies = re.findall(r"^## Pass 1 proposal artifact\s*\n(.*?)(?=^## |\Z)",
                        record_text, flags=re.M | re.S)
    if len(bodies) != 1:
        return False
    body = bodies[0].strip()
    matches = list(re.finditer(r"^(\d+)\. +", body, flags=re.M))
    if len(matches) != len(sections) or not matches or matches[0].start() != 0:
        return False
    for index, (match, section) in enumerate(zip(matches, sections)):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        if int(match[1]) != index + 1 or body[match.end():end].strip() != section["text"].strip():
            return False
    return True


def matching_median_seal(record_text, receipt, output):
    root = repo_root()
    cited = set(cited_receipt_ids(record_text))
    seals = [load(path) for path in list_receipts(root, "M1")]
    seals = [value for value in seals if value.get("receipt_id") in cited
             and value.get("tool") == "seal-median"]
    if len(seals) != 1:
        raise ValueError("M1 requires exactly one cited authenticated median seal")
    seal = seals[0]
    problems = verify_attestation(root, seal)
    if problems:
        raise ValueError("invalid median seal: " + "; ".join(problems))
    attestation = seal["external_attestation"]
    path = output["inputs"]["median"]
    if (attestation["median_path"] != path
            or attestation["median_sha256"] != receipt["inputs"][path]):
        raise ValueError("overlap median differs from authenticated median")
    git_output(root, "merge-base", "--is-ancestor", seal["repo_commit"], receipt["repo_commit"])
    candidate = output["inputs"]["candidate"]
    existing = git_output(root, "ls-tree", "-r", "--name-only", attestation["seal_commit"],
                          "--", candidate).strip()
    if existing:
        raise ValueError("candidate path already existed when median was sealed")
    if seal["output"] not in record_text:
        raise ValueError("authenticated median output absent from record")


def check(record_text, receipt):
    try:
        if receipt.get("entrant") != "M1" or receipt.get("tool") != "overlap":
            raise ValueError("wrong overlap receipt identity")
        output = json.loads(receipt["output"])
        if output.get("tool") != "overlap" or output.get("entrant") != "M1":
            raise ValueError("wrong overlap output identity")
        documents = load_documents(receipt, output)
        matching_median_seal(record_text, receipt, output)
        result = compare(*documents)
        if result != output.get("comparison"):
            raise ValueError("semantic report does not recompute")
        expected = canonical_json(output)
        sections = items(documents[1], "sections")
        sections_match = final_sections_match(record_text, sections)
        checks = [Check("report_verbatim", "complete overlap report verbatim",
                        "present" if expected in record_text else "absent", expected in record_text),
                  Check("sections_verbatim", "candidate sections verbatim",
                        "exact final items" if sections_match else "final items differ", sections_match),
                  Check("semantic_gate", "no CHOSEN overlap at or above threshold",
                        "pass" if result["passed"] else "regeneration required", result["passed"])]
    except (HarnessError, OSError, ValueError, TypeError, KeyError) as exc:
        checks = [Check(name, "valid pinned semantic result", str(exc), False) for name in NAMES]
    return BindResult(all(c.passed for c in checks), BOUND_SPAN, checks)
