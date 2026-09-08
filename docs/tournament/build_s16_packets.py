"""Render isolated Sweet 16 Pass 1 and Pass 2 packets from official source records."""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "official-runs"
PACKETS = HERE / "packets"
DRAW = HERE / "s16-draw-map.json"
FIELD = HERE / "field-of-32.md"
CONTRACTS = HERE / "evidence-contracts-s16.md"

_RULE_HEADER_RE = re.compile(r"^(\d+)\.\s+(\S.*)$")


def section(text, heading, next_heading):
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## {re.escape(next_heading)}\s*$)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError(f"missing `{heading}` section")
    return match.group(1).strip()


def _parse_rules(artifact):
    """Parse numbered rules, folding indented or unnumbered continuation lines into
    the preceding rule instead of silently dropping them. A rule may wrap onto
    multiple physical lines; only a line matching `<digits>. ` starts a new rule."""
    rules = []
    current = None  # (number_str, [line, line, ...])
    for line in artifact.splitlines():
        match = _RULE_HEADER_RE.match(line)
        if match:
            if current is not None:
                rules.append((current[0], "\n".join(current[1]).rstrip()))
            current = (match.group(1), [match.group(2)])
        elif current is not None:
            current[1].append(line)
    if current is not None:
        rules.append((current[0], "\n".join(current[1]).rstrip()))
    return rules


def _extract_heading_block(text, source_name, level, code):
    """Extract the block starting at a `#`*level heading for `code` (formatted
    `<hashes> <CODE> ·`) up through, but not including, the next heading at
    level 2 or 3. Used to pull one entrant's own section out of a shared file."""
    hashes = "#" * level
    pattern = re.compile(
        rf"^{hashes}\s+{re.escape(code)}\s+·.*?(?=^#{{2,3}}\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise ValueError(f"{source_name}: missing entry for {code}")
    block = match.group(0).rstrip()
    # A block captured up to the next region's `##` heading commonly ends on the
    # `---` divider that precedes that heading; drop it, it belongs to the region
    # boundary, not to this entrant's own definition.
    if block.endswith("---"):
        block = block[: -len("---")].rstrip()
    return block


def source_record(code):
    path = RUNS / f"s16-{code.lower()}.md"
    if not path.is_file():
        raise ValueError(f"missing source record: {path.relative_to(HERE)}")
    text = path.read_text()
    declared = re.search(r"^- \*\*Entrant code:\*\*\s*(\S+)\s*$", text, re.MULTILINE)
    if not declared or declared.group(1).upper() != code:
        raise ValueError(f"{path.name}: entrant-code receipt does not match {code}")
    artifact = section(text, "Pass 1 proposal artifact", "Execution trace")
    rules = _parse_rules(artifact)
    numbers = [int(number) for number, _ in rules]
    if numbers != list(range(1, 25)):
        raise ValueError(f"{path.name}: requires exactly one populated rule numbered 1–24")
    return {"path": path, "text": text, "rules": rules}


def entrant_definitions(codes, field_text, contracts_text):
    """Pull each entrant's frozen field-of-32.md definition and evidence-contracts-s16.md
    contract, both required in the Pass 2 packet per next-round-protocol.md's Pass 2
    spec: "The same panel receives the frozen definitions, evidence contracts and
    execution traces." """
    out = {}
    for code in codes:
        out[code] = {
            "definition": _extract_heading_block(field_text, "field-of-32.md", 3, code),
            "contract": _extract_heading_block(contracts_text, "evidence-contracts-s16.md", 2, code),
        }
    return out


def output_packet(game, a, b):
    return "\n".join(
        [
            f"# Sweet 16 — Matchup {game} — Pass 1 Output-Only Packet",
            "",
            "Judge only the anonymous proposal artifacts below. Do not inspect source files,",
            "mechanism packets, draws, prior results, or other panels' work.",
            "",
            "For each side, name the strongest surprising proposal, its causal return path to",
            "the Juniper Court brief, and the first repeated early move. Then vote A, B, or Tie",
            "on ideas 17–24 for surprising usefulness. Seal Pass 1 before opening Pass 2.",
            "",
            "---",
            "",
            "## IDEA A",
            "",
            *[f"{number}. {rule}" for number, rule in a["rules"]],
            "",
            "---",
            "",
            "## IDEA B",
            "",
            *[f"{number}. {rule}" for number, rule in b["rules"]],
            "",
        ]
    )


def mechanism_packet(game, a_code, b_code, a, b, definitions):
    return "\n".join(
        [
            f"# Sweet 16 — Matchup {game} — Pass 2 Mechanism-and-Trace Packet",
            "",
            "Open only after the panel seals its Pass 1 output-only yield record.",
            "",
            f"- **Idea A entrant:** {a_code}",
            f"- **Idea B entrant:** {b_code}",
            "",
            "---",
            "",
            "## IDEA A — FROZEN DEFINITION",
            "",
            definitions[a_code]["definition"],
            "",
            "## IDEA A — EVIDENCE CONTRACT",
            "",
            definitions[a_code]["contract"],
            "",
            "## IDEA A SOURCE RECORD",
            "",
            a["text"].rstrip(),
            "",
            "---",
            "",
            "## IDEA B — FROZEN DEFINITION",
            "",
            definitions[b_code]["definition"],
            "",
            "## IDEA B — EVIDENCE CONTRACT",
            "",
            definitions[b_code]["contract"],
            "",
            "## IDEA B SOURCE RECORD",
            "",
            b["text"].rstrip(),
            "",
        ]
    )


def render(write=False, phase=None):
    """phase: None validates/renders everything (read-only default). "output" or
    "mechanism" restricts what gets returned/written — required whenever `write`
    is true, per official-runs/README.md's Packet release order: output packets
    are rendered and Pass 1 is sealed *before* mechanism packets are released, so
    a single --write can never emit both at once."""
    draw = json.loads(DRAW.read_text())
    errors = []
    records = {}
    for game in draw.get("games", []):
        for code in (game.get("A"), game.get("B")):
            if code and code not in records:
                try:
                    records[code] = source_record(code)
                except ValueError as error:
                    errors.append(str(error))
    if errors:
        raise ValueError("\n".join(errors))

    definitions = {}
    if phase in (None, "mechanism"):
        field_text = FIELD.read_text()
        contracts_text = CONTRACTS.read_text()
        try:
            definitions = entrant_definitions(records.keys(), field_text, contracts_text)
        except ValueError as error:
            raise ValueError(str(error))

    packets = []
    for game in draw["games"]:
        number = game["g"]
        a_code, b_code = game["A"], game["B"]
        a, b = records[a_code], records[b_code]
        if phase in (None, "output"):
            packets.append((PACKETS / f"s16-{number:02d}-output.md", output_packet(number, a, b)))
        if phase in (None, "mechanism"):
            packets.append(
                (
                    PACKETS / f"s16-{number:02d}-mechanism-trace.md",
                    mechanism_packet(number, a_code, b_code, a, b, definitions),
                )
            )
    if write:
        PACKETS.mkdir(parents=True, exist_ok=True)
        for path, content in packets:
            path.write_text(content)
    return packets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the packet files")
    parser.add_argument(
        "--phase",
        choices=["output", "mechanism"],
        help="Restrict rendering to one release phase. Required together with --write: "
        "'output' writes only the Pass 1 anonymous packets (safe to run before any panel "
        "is dispatched); 'mechanism' writes only the Pass 2 definition/contract/trace "
        "packets, and must not be run until every panel has sealed its Pass 1 record. "
        "Omit --phase (with --write omitted too) to validate all sixteen source records "
        "without writing anything.",
    )
    args = parser.parse_args()
    if args.write and not args.phase:
        parser.error(
            "--write requires --phase {output,mechanism} — writing both phases in one "
            "call would release mechanism-and-trace packets before Pass 1 is sealed"
        )
    try:
        packets = render(write=args.write, phase=args.phase)
    except ValueError as error:
        parser.error(str(error))
    action = "wrote" if args.write else "validated"
    phase_note = f" ({args.phase} phase)" if args.phase else ""
    print(f"{action} {len(packets)} Sweet 16 packet artifacts{phase_note}")


if __name__ == "__main__":
    main()
