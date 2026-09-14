"""Locate the authoritative numbered proposal, excluding execution evidence."""
import re


def proposal_lines(text):
    sections = {}
    current = None
    for line in text.splitlines():
        match = re.fullmatch(r'##\s+(.+?)\s*', line)
        if match:
            current = match[1]
            sections.setdefault(current, []).append([])
        elif current is not None:
            sections[current][-1].append(line)
    # Official artifact takes precedence over legacy development record headings.
    for heading in ('Pass 1 proposal artifact', 'Openers', 'Mechanism output'):
        if heading in sections:
            bodies = sections[heading]
            return bodies[0] if len(bodies) == 1 else []
    return []
