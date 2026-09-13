"""C5 notation structural validation and seven-form catalog enforcement.

Exports:
    validate_catalog(value) -> dict
    validate_artifact(artifact, catalog, notation_name) -> list[str]

Catalog problems (malformed structure, drift from implemented schemas) raise
ValueError. Artifact problems (wrong notation, bad counts, missing slots,
duplicates, malformed values) are returned as deterministic problem strings.
"""


import math


FORM_ORDER = [
    "recipe",
    "court-docket",
    "knitting-pattern",
    "chess-annotation",
    "liturgical-rubric",
    "flight-checklist",
    "circuit-diagram",
]


def _is_str(v):
    return isinstance(v, str) and v.strip() != ""


def _is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _check_nonempty_list(v):
    return isinstance(v, list) and len(v) > 0


def _slot_str(problems, slots, slot, where):
    if slot not in slots:
        problems.append("%s: missing slot '%s'" % (where, slot))
    elif not _is_str(slots[slot]):
        problems.append("%s: slot '%s' must be a non-empty string" % (where, slot))


def _slot_str_list(problems, slots, slot, where):
    if slot not in slots:
        problems.append("%s: missing slot '%s'" % (where, slot))
        return
    v = slots[slot]
    if not _check_nonempty_list(v):
        problems.append("%s: slot '%s' must be a non-empty list" % (where, slot))
        return
    for i, item in enumerate(v):
        if not _is_str(item):
            problems.append(
                "%s: slot '%s' entry %d must be a non-empty string"
                % (where, slot, i)
            )


def _slot_positive_number(problems, obj, key, where):
    if key not in obj:
        problems.append("%s: missing key '%s'" % (where, key))
    elif not _is_number(obj[key]) or obj[key] <= 0:
        problems.append("%s: key '%s' must be a positive number" % (where, key))


def _slot_str_dict_fields(problems, obj, keys, where):
    if not isinstance(obj, dict):
        problems.append("%s must be an object" % where)
        return
    for key in keys:
        _slot_str(problems, obj, key, "%s" % where)


def _validate_recipe(where, slots, problems):
    if not _check_nonempty_list(slots.get("ingredients")):
        problems.append("%s: ingredients must be a non-empty object list" % where)
    if "ingredients" in slots and _check_nonempty_list(slots["ingredients"]):
        for i, ing in enumerate(slots["ingredients"]):
            sub = "%s ingredients[%d]" % (where, i)
            if not isinstance(ing, dict):
                problems.append("%s must be an object" % sub)
                continue
            _slot_str(problems, ing, "name", sub)
            _slot_positive_number(problems, ing, "quantity", sub)
            _slot_str(problems, ing, "unit", sub)
    _slot_str_list(problems, slots, "steps", where)


def _validate_court_docket(where, slots, problems):
    _slot_str(problems, slots, "issue", where)
    for slot in ("parties", "evidence"):
        _slot_str_list(problems, slots, slot, where)
    _slot_str(problems, slots, "ruling", where)
    _slot_str_list(problems, slots, "remedies", where)


def _validate_knitting(where, slots, problems):
    if "gauge" not in slots:
        problems.append("%s: missing slot 'gauge'" % where)
    elif not isinstance(slots["gauge"], dict):
        problems.append("%s: slot 'gauge' must be an object" % where)
    else:
        gauge = slots["gauge"]
        _slot_positive_number(problems, gauge, "stitches_per_inch", where + " gauge")
        _slot_positive_number(problems, gauge, "rows_per_inch", where + " gauge")
    _slot_str_list(problems, slots, "stitches", where)
    _slot_str(problems, slots, "repeat", where)
    _slot_str(problems, slots, "bind_off", where)


def _validate_chess(where, slots, problems):
    if "moves" not in slots:
        problems.append("%s: missing slot 'moves'" % where)
        return
    moves = slots["moves"]
    if not _check_nonempty_list(moves):
        problems.append("%s: slot 'moves' must be a non-empty list" % where)
        return
    for i, mv in enumerate(moves):
        sub = "%s moves[%d]" % (where, i)
        if not isinstance(mv, dict):
            problems.append("%s must be an object" % sub)
            continue
        _slot_str(problems, mv, "move", sub)
        _slot_str(problems, mv, "countermove", sub)
        if "evaluation" not in mv:
            problems.append("%s: missing key 'evaluation'" % sub)
        elif not _is_number(mv["evaluation"]):
            problems.append("%s: key 'evaluation' must be a number" % sub)


def _validate_liturgical(where, slots, problems):
    if "cues" not in slots:
        problems.append("%s: missing slot 'cues'" % where)
        return
    cues = slots["cues"]
    if not _check_nonempty_list(cues):
        problems.append("%s: slot 'cues' must be a non-empty list" % where)
        return
    for i, cue in enumerate(cues):
        _slot_str_dict_fields(
            problems,
            cue,
            ("cue", "officiant", "response", "rubric"),
            "%s cues[%d]" % (where, i),
        )


def _validate_flight(where, slots, problems):
    if "checks" not in slots:
        problems.append("%s: missing slot 'checks'" % where)
        return
    checks = slots["checks"]
    if not _check_nonempty_list(checks):
        problems.append("%s: slot 'checks' must be a non-empty list" % where)
        return
    for i, chk in enumerate(checks):
        _slot_str_dict_fields(
            problems,
            chk,
            ("trigger", "challenge", "expected_response", "verify", "abort"),
            "%s checks[%d]" % (where, i),
        )


def _validate_circuit(where, slots, problems):
    if "nodes" not in slots:
        problems.append("%s: missing slot 'nodes'" % where)
        return
    nodes = slots["nodes"]
    if not _check_nonempty_list(nodes):
        problems.append("%s: slot 'nodes' must be a non-empty list" % where)
        return
    seen = set()
    for i, node in enumerate(nodes):
        if not _is_str(node):
            problems.append(
                "%s: nodes[%d] must be a non-empty string" % (where, i)
            )
        elif node in seen:
            problems.append("%s: duplicate node id '%s'" % (where, node))
        else:
            seen.add(node)
    if "connections" not in slots:
        problems.append("%s: missing slot 'connections'" % where)
        return
    conns = slots["connections"]
    if not _check_nonempty_list(conns):
        problems.append(
            "%s: slot 'connections' must be a non-empty list" % where
        )
        return
    for i, conn in enumerate(conns):
        sub = "%s connections[%d]" % (where, i)
        if not isinstance(conn, dict):
            problems.append("%s must be an object" % sub)
            continue
        _slot_str(problems, conn, "from", sub)
        _slot_str(problems, conn, "to", sub)
        if _is_str(conn.get("from")) and conn["from"] not in seen:
            problems.append("%s: 'from' references unknown node '%s'"
                            % (sub, conn["from"]))
        if _is_str(conn.get("to")) and conn["to"] not in seen:
            problems.append("%s: 'to' references unknown node '%s'"
                            % (sub, conn["to"]))


FORM_SCHEMAS = {
    "recipe": {"required_slots": ["ingredients", "steps"],
               "validate": _validate_recipe},
    "court-docket": {"required_slots": ["issue", "parties", "evidence",
                                        "ruling", "remedies"],
                     "validate": _validate_court_docket},
    "knitting-pattern": {"required_slots": ["gauge", "stitches", "repeat",
                                            "bind_off"],
                         "validate": _validate_knitting},
    "chess-annotation": {"required_slots": ["moves"],
                         "validate": _validate_chess},
    "liturgical-rubric": {"required_slots": ["cues"],
                           "validate": _validate_liturgical},
    "flight-checklist": {"required_slots": ["checks"],
                         "validate": _validate_flight},
    "circuit-diagram": {"required_slots": ["nodes", "connections"],
                        "validate": _validate_circuit},
}


def validate_catalog(value):
    """Validate the C5 notation catalog; return it if structurally sound.

    Raises ValueError on malformed structure or drift from the implemented
    form schemas (names, ordering, required_slots).
    """
    if not isinstance(value, dict):
        raise ValueError("catalog must be an object")
    if type(value.get("schema_version")) is not int or value["schema_version"] != 1:
        raise ValueError("catalog schema_version must be 1")
    item_count = value.get("item_count")
    if not _is_number(item_count) or isinstance(item_count, float) \
            or item_count < 1:
        raise ValueError("catalog item_count must be a positive integer")
    notations = value.get("notations")
    if not isinstance(notations, list):
        raise ValueError("catalog notations must be a list")
    names = []
    for i, entry in enumerate(notations):
        if not isinstance(entry, dict):
            raise ValueError("notations[%d] must be an object" % i)
        name = entry.get("name")
        if not _is_str(name):
            raise ValueError("notations[%d] name must be a non-empty string" % i)
        if name not in FORM_SCHEMAS:
            raise ValueError("notations[%d] has unknown notation '%s'"
                             % (i, name))
        if name in names:
            raise ValueError("duplicate notation entry '%s'" % name)
        names.append(name)
        if not _is_str(entry.get("description")):
            raise ValueError("notations[%d] description must be a non-empty "
                             "string" % i)
        expected = FORM_SCHEMAS[name]["required_slots"]
        if entry.get("required_slots") != expected:
            raise ValueError(
                "notations[%d] ('%s') required_slots drift: expected %r, "
                "got %r" % (i, name, expected, entry.get("required_slots"))
            )
    if names != FORM_ORDER:
        raise ValueError("catalog notations must be exactly %r in order, "
                         "got %r" % (FORM_ORDER, names))
    return value


def validate_artifact(artifact, catalog, notation_name):
    """Structurally validate a C5 notation artifact against a catalog.

    Returns a deterministic list of problem strings; empty means valid.
    Raises ValueError only if the artifact or catalog top-level shape is
    malformed (non-dict/non-list), including a drifted catalog.
    """
    if not isinstance(artifact, dict):
        raise ValueError("artifact must be an object")
    catalog = validate_catalog(catalog)
    if not _is_str(notation_name):
        raise ValueError("notation_name must be a non-empty string")
    problems = []
    if artifact.get("notation") != notation_name:
        problems.append("notation mismatch: expected '%s', got %r"
                        % (notation_name, artifact.get("notation")))
    if notation_name not in FORM_SCHEMAS:
        problems.append("unknown notation '%s'" % notation_name)
        return problems
    items = artifact.get("items")
    if not isinstance(items, list):
        raise ValueError("artifact items must be a list")
    expected_count = catalog["item_count"]
    if len(items) != expected_count:
        problems.append("item count mismatch: catalog declares %d, "
                        "artifact has %d" % (expected_count, len(items)))
    seen_ids = set()
    form = FORM_SCHEMAS[notation_name]
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError("items[%d] must be an object" % i)
        where = "item %d" % i
        item_id = item.get("id")
        if not _is_str(item_id):
            problems.append("%s: 'id' must be a non-empty string" % where)
        elif item_id in seen_ids:
            problems.append("%s: duplicate id '%s'" % (where, item_id))
        else:
            seen_ids.add(item_id)
        for slot in form["required_slots"]:
            if slot not in item:
                problems.append("%s: missing slot '%s'" % (where, slot))
        form["validate"](where, item, problems)
    return problems
