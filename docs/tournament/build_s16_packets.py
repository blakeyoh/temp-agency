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


def section(text, heading, next_heading):
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## {re.escape(next_heading)}\s*$)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError(f"missing `{heading}` section")
    return match.group(1).strip()


def source_record(code):
    path = RUNS / f"s16-{code.lower()}.md"
    if not path.is_file():
        raise ValueError(f"missing source record: {path.relative_to(HERE)}")
    text = path.read_text()
    declared = re.search(r"^- \*\*Entrant code:\*\*\s*(\S+)\s*$", text, re.MULTILINE)
    if not declared or declared.group(1).upper() != code:
        raise ValueError(f"{path.name}: entrant-code receipt does not match {code}")
    artifact = section(text, "Pass 1 proposal artifact", "Execution trace")
    rules = re.findall(r"^(\d+)\.\s+(\S.*)$", artifact, re.MULTILINE)
    numbers = [int(number) for number, _ in rules]
    if numbers != list(range(1, 25)):
        raise ValueError(f"{path.name}: requires exactly one populated rule numbered 1–24")
    return {"path": path, "text": text, "rules": rules}


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


def mechanism_packet(game, a_code, b_code, a, b):
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
            "## IDEA A SOURCE RECORD",
            "",
            a["text"].rstrip(),
            "",
            "---",
            "",
            "## IDEA B SOURCE RECORD",
            "",
            b["text"].rstrip(),
            "",
        ]
    )


def render(write=False):
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

    packets = []
    for game in draw["games"]:
        number = game["g"]
        a_code, b_code = game["A"], game["B"]
        a, b = records[a_code], records[b_code]
        packets.extend(
            [
                (PACKETS / f"s16-{number:02d}-output.md", output_packet(number, a, b)),
                (PACKETS / f"s16-{number:02d}-mechanism-trace.md",
                 mechanism_packet(number, a_code, b_code, a, b)),
            ]
        )
    if write:
        PACKETS.mkdir(parents=True, exist_ok=True)
        for path, content in packets:
            path.write_text(content)
    return packets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the 16 packet files")
    args = parser.parse_args()
    try:
        packets = render(write=args.write)
    except ValueError as error:
        parser.error(str(error))
    action = "wrote" if args.write else "validated"
    print(f"{action} {len(packets)} Sweet 16 packet artifacts")


if __name__ == "__main__":
    main()
