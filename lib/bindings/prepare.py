"""Bind a prepared input and check the proposal's frozen negative wordlists.

Verbatim presence and absence are mechanically checkable. They do not prove
that the persona did not see other context, or that its prose was caused by it.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from lib.bindings import BindResult, Check
from lib.errors import HarnessError
from lib.paths import repo_root, sha256_bytes
from lib.pipeline import run
from lib.pipeline.negative import leaks

VERIFICATION_CLASS = "replay-exact"
BOUND_SPAN = ("persona-visible input verbatim; record generated from it; "
              "negative wordlist absent from the reasoning span")
CHECK_NAMES = ("visible_verbatim", "raw_brief_absent", "negative_words", "record_sections")
ENTRANTS = {"transform": "A1", "mask": "C8", "withhold": "A5"}
HEADER = re.compile(
    r"PREPARE entrant=(A1|C8|A5) adapter=(transform|mask|withhold) "
    r"persona=([a-z0-9-]+) brief=(\S+) config=(\S+) "
    r"brief_sha256=([0-9a-f]{64}) config_sha256=([0-9a-f]{64})")
OUTPUT = re.compile(r"([^\n]+)\n\n=== PERSONA-VISIBLE INPUT ===\n(.*?)"
                    r"\n=== END ===\n\n=== TRANSFORM RECORD ===\n(.*?)\n=== END ===\n", re.S)
H2 = re.compile(r"^##\s+(.+?)\s*$")


def _pinned_text(root, path, digest, inputs):
    relative = Path(path)
    if relative.is_absolute() or ".." in relative.parts or inputs.get(path) != digest:
        raise ValueError("header input is not pinned by receipt")
    target = (root / relative).resolve()
    target.relative_to(root.resolve())
    data = target.read_bytes()
    if sha256_bytes(data) != digest:
        raise ValueError("binding input changed since receipt")
    return data.decode("utf-8")


def _parse(receipt):
    output = receipt.get("output")
    match = OUTPUT.fullmatch(output) if isinstance(output, str) else None
    header = HEADER.fullmatch(match[1]) if match else None
    if not header:
        raise ValueError("malformed prepare output")
    entrant, adapter, persona, brief_path, config_path, brief_hash, config_hash = header.groups()
    if ENTRANTS[adapter] != entrant or entrant != receipt.get("entrant"):
        raise ValueError("entrant does not match adapter")
    if (adapter != "transform" and persona != "none") or (adapter == "transform" and persona == "none"):
        raise ValueError("invalid persona for adapter")
    inputs = receipt.get("inputs")
    if not isinstance(inputs, dict) or set(inputs) != {brief_path, config_path}:
        raise ValueError("prepare must pin exactly brief and config")
    root = repo_root()
    brief = _pinned_text(root, brief_path, brief_hash, inputs)
    config = json.loads(_pinned_text(root, config_path, config_hash, inputs))
    result = run(adapter, brief, config, None if persona == "none" else persona)
    if not match[2].strip() or (match[2], match[3]) != (result.visible, "\n".join(result.record_lines)):
        raise ValueError("output differs from pinned preparation")
    return adapter, brief, config, match[2]


def _sections(text):
    sections = {}
    heading = ""
    outside = []
    for line in text.splitlines(keepends=True):
        match = H2.match(line.rstrip("\r\n"))
        if match:
            heading = match[1]
            sections.setdefault(heading, []).append("")
        elif heading:
            sections[heading][-1] += line
        if heading != "Execution trace":
            outside.append(line)
    return sections, "".join(outside)


def _negative(adapter, config, sections):
    if adapter == "transform":
        return Check("negative_words", "not applicable", "not applicable (transform)", True)
    if adapter == "mask":
        words = list(config["map"])
        headings = ("Abstract proposal",)
    else:
        words = config["conditions"][config["condition"]]["negative_words"]
        headings = ("Pass 1 proposal artifact", "Abstract proposal")
    text = "\n".join(body for name in headings for body in sections.get(name, []))
    found = leaks(text, words)
    return Check("negative_words", "no frozen negative words in reasoning",
                 ", ".join(found) if found else "none", not found)


def _record_sections(adapter, sections):
    heading = "Abstract proposal" if adapter == "mask" else "Pass 1 proposal artifact"
    bodies = sections.get(heading, [])
    count = len(re.findall(r"^\s*\d+\.\s+\S", bodies[0], re.M)) if len(bodies) == 1 else 0
    unique = all(len(sections.get(name, [])) <= 1 for name in
                 ("Execution trace", "Abstract proposal", "Pass 1 proposal artifact"))
    return Check("record_sections", "one proposal section with at least 10 numbered lines",
                 "%d numbered lines; sections unique=%s" % (count, unique), count >= 10 and unique)


def check(record_text, receipt):
    try:
        adapter, brief, config, visible = _parse(receipt)
        sections, outside = _sections(record_text)
        sentences = re.split(r"(?<=[.!?])\s+", brief.strip())
        raw = [s for i, s in enumerate(sentences) if s and (i == 0 or len(s) > 40) and s in outside]
        checks = [Check("visible_verbatim", "persona-visible input present verbatim",
                        "present" if visible in record_text else "absent", visible in record_text),
                  Check("raw_brief_absent", "no raw brief sentences outside Execution trace",
                        "%d raw sentences" % len(raw), not raw),
                  _negative(adapter, config, sections), _record_sections(adapter, sections)]
    except (HarnessError, OSError, ValueError, TypeError, KeyError) as exc:
        checks = [Check(name, "valid pinned prepare output", str(exc), False) for name in CHECK_NAMES]
    return BindResult(all(c.passed for c in checks), BOUND_SPAN, checks)
