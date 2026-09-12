"""Bounded dimensional analysis and order-of-magnitude calculations."""
from __future__ import annotations

import math
from decimal import Decimal, InvalidOperation, localcontext
from typing import Any, Dict

try:
    import pint
except ImportError:
    pint = None

from lib.toolbelts.common import require_keys, require_list, require_object, require_string

PINT_VERSION = getattr(pint, "__version__", "unavailable")


def decimal_value(value: Any, label: str, positive: bool = False) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError(f"{label} must be a decimal string or number")
    try:
        number = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{label} is not a decimal number") from exc
    if not number.is_finite() or (positive and number <= 0):
        qualifier = "finite and positive" if positive else "finite"
        raise ValueError(f"{label} must be {qualifier}")
    return number


def _registry() -> pint.UnitRegistry:
    if pint is None:
        raise ValueError("Pint is unavailable; install the pinned harness requirements")
    return pint.UnitRegistry(non_int_type=Decimal)


def _unit(registry: pint.UnitRegistry, value: Any, label: str):
    text = require_string(value, label)
    try:
        return registry.parse_units(text)
    except (pint.errors.PintError, TypeError, ValueError) as exc:
        raise ValueError(f"{label} is unsupported: {text!r}: {exc}") from exc


def _decimal_text(value: Decimal) -> str:
    text = format(value.normalize(), "f")
    return "0" if text in ("-0", "") else text


def validate_units_config(value: Any) -> Dict[str, Any]:
    data = require_object(value, "units config")
    require_keys(data, {"schema", "pint_version", "operations"}, "units config")
    if data["schema"] != "temp-agency.units/v1":
        raise ValueError("units config has unsupported schema")
    if data["pint_version"] != PINT_VERSION:
        raise ValueError(f"units config pins Pint {data['pint_version']!r}, runtime is {PINT_VERSION!r}")
    operations = require_list(data["operations"], "units operations")
    if not operations:
        raise ValueError("units operations must not be empty")
    registry = _registry()
    seen = set()
    for index, item in enumerate(operations):
        op = require_object(item, f"units operation {index}")
        kind = op.get("operation")
        fields = {"id", "operation", "from", "to", "value"} if kind == "convert" \
            else {"id", "operation", "left", "right"}
        require_keys(op, fields, f"units operation {index}")
        identifier = require_string(op["id"], f"units operation {index}.id")
        if identifier in seen:
            raise ValueError(f"duplicate units operation id: {identifier}")
        seen.add(identifier)
        if kind == "convert":
            decimal_value(op["value"], f"units operation {identifier}.value")
            source = _unit(registry, op["from"], f"units operation {identifier}.from")
            target = _unit(registry, op["to"], f"units operation {identifier}.to")
            if source.dimensionality != target.dimensionality:
                raise ValueError(f"units operation {identifier} has incompatible dimensions")
        elif kind == "check":
            _unit(registry, op["left"], f"units operation {identifier}.left")
            _unit(registry, op["right"], f"units operation {identifier}.right")
        else:
            raise ValueError(f"units operation {identifier} has unsupported operation {kind!r}")
    return data


def units_results(config: Dict[str, Any]) -> Dict[str, Any]:
    registry = _registry()
    results = []
    for op in config["operations"]:
        if op["operation"] == "check":
            left = _unit(registry, op["left"], "left unit")
            right = _unit(registry, op["right"], "right unit")
            results.append({"id": op["id"], "operation": "check",
                            "compatible": left.dimensionality == right.dimensionality,
                            "left": op["left"], "right": op["right"]})
            continue
        source = _unit(registry, op["from"], "source unit")
        target = _unit(registry, op["to"], "target unit")
        magnitude = decimal_value(op["value"], f"units operation {op['id']}.value")
        try:
            converted = registry.Quantity(magnitude, source).to(target).magnitude
        except pint.errors.PintError as exc:
            raise ValueError(f"units operation {op['id']} cannot convert: {exc}") from exc
        results.append({"id": op["id"], "operation": "convert", "value": str(op["value"]),
                        "from": op["from"], "to": op["to"],
                        "converted_value": _decimal_text(Decimal(str(converted)))})
    return {"dependency_versions": {"Pint": PINT_VERSION}, "operations": results}


def validate_orders_config(value: Any) -> Dict[str, Any]:
    data = require_object(value, "orders config")
    require_keys(data, {"schema", "comparisons"}, "orders config")
    if data["schema"] != "temp-agency.orders/v1":
        raise ValueError("orders config has unsupported schema")
    comparisons = require_list(data["comparisons"], "orders comparisons")
    if not comparisons:
        raise ValueError("orders comparisons must not be empty")
    seen = set()
    for index, item in enumerate(comparisons):
        row = require_object(item, f"orders comparison {index}")
        require_keys(row, {"id", "numerator", "denominator"}, f"orders comparison {index}")
        identifier = require_string(row["id"], f"orders comparison {index}.id")
        if identifier in seen:
            raise ValueError(f"duplicate orders comparison id: {identifier}")
        seen.add(identifier)
        decimal_value(row["numerator"], f"orders comparison {identifier}.numerator", True)
        decimal_value(row["denominator"], f"orders comparison {identifier}.denominator", True)
    return data


def _log10(value: Decimal) -> float:
    exponent = value.adjusted()
    mantissa = value.scaleb(-exponent)
    return exponent + math.log10(float(mantissa))


def orders_results(config: Dict[str, Any]) -> list:
    results = []
    with localcontext() as context:
        context.prec = 40
        for item in config["comparisons"]:
            numerator = decimal_value(item["numerator"], "numerator", True)
            denominator = decimal_value(item["denominator"], "denominator", True)
            ratio = numerator / denominator
            log_ratio = _log10(ratio)
            results.append({"id": item["id"], "numerator": str(item["numerator"]),
                            "denominator": str(item["denominator"]),
                            "ratio": _decimal_text(ratio),
                            "log10_ratio": format(log_ratio, ".12f"),
                            "whole_orders": math.floor(abs(log_ratio))})
    return results
