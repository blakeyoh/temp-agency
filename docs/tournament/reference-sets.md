# Axis Reference Sets

The ruler. "Significantly better" is meaningless without fixed points to measure against,
so each axis pins named reference examples at known positions. A judge decides **which
references an idea sits between** — the way a difficulty table works in a judged sport,
rather than the way an impression works.

Judges may argue an idea sits *above* the ceiling reference. They may not skip the
comparison, and every verdict must carry the predicate named at the bottom of its axis.

---

## Distance
*How far from the median AI answer does this push the output?*

| Position | Reference |
|---|---|
| Floor | Reorganize the same answer with better headings |
| Low | Ask for "an unconventional angle" — you get a mildly unusual framing of the same answer |
| Mid | Require the answer to come from a named non-obvious domain *(this repo's left-fielder)* |
| High | Forbid the answer from containing the problem's own vocabulary |
| Ceiling | The output is unrecognizable as an answer to the question until it is translated back |

**Required predicate:** *"Name a specific output this forbids."* No nameable forbidden output → floor.

---

## Mechanism
*Does something actually execute, or is this exhortation?*

| Position | Reference |
|---|---|
| Floor | A paragraph in a markdown file asking the model to try harder |
| Low | A structured prompt template with required sections |
| Mid | A checklist the model is asked to self-verify against |
| High | A script that runs, whose output the model must consume |
| Ceiling | A gate that rejects the output and forces regeneration without the model's consent |

**Required predicate:** *"Name the file that runs."* No file → it scores as exhortation.

---

## Irreducibility
*Could the base model already do this if simply asked nicely?*

| Position | Reference |
|---|---|
| Floor | "Ask the model to be more creative" |
| Low | Hand the model a persona file *(this repo, v1)* — real, but promptable |
| Mid | Force output through a parser that rejects it — the model cannot opt out |
| High | Withhold a fact from the context window — cannot be simulated by a model that knows it |
| Ceiling | Change the weights |

**Required predicate:** *"A base model given only the prompt `___` reproduces about ___% of this."* Runnable.

---

## Compounding
*Does it get weirder with use, or does the novelty wear off?*

| Position | Reference |
|---|---|
| Floor | Identical on use #10 as on use #1 |
| Low | A novelty effect that fades as the pattern becomes familiar |
| Mid | Accumulates material you may consult but need not obey |
| High | Each use narrows the space of permitted answers |
| Ceiling | The constraint tightens automatically and cannot be relaxed |

**Required predicate:** *"State what use #10 produces that use #1 does not."* "The same thing" → floor.

---

## Generative failure
*When it breaks, does it produce a different kind of insight — or noise?*

| Position | Reference |
|---|---|
| Floor | Nothing — the pass silently produces the default answer |
| Low | An error; the run is wasted |
| Mid | Noise that must be discarded, but cheaply |
| High | An unusable answer that nonetheless names a hidden assumption |
| Ceiling | The failure is itself a proposal worth acting on |

**Required predicate:** *"Describe the exact failure output."* "It doesn't work" → floor.
