"""A1 deterministic persona-specific brief transformations."""
from __future__ import annotations

import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from lib.pipeline import PrepareResult
from lib.pipeline.negative import term_pattern

SentenceResult = Tuple[List[str], List[str]]


def _sentences(text: str, config: Dict[str, Any]) -> List[str]:
    if config.get("sentence_split") != "regex":
        raise ValueError("sentence_split must be regex")
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]


def _record(before: str, after: Optional[str]) -> str:
    if after is None:
        return "dropped: %s" % before
    if after == before:
        return "kept: %s" % before
    return "rewritten: %s => %s" % (before, after)


def _contains_term(text: str, terms: Sequence[str]) -> bool:
    return any(term_pattern(str(term)).search(text) for term in terms)


def _filter(sentences: List[str], keep: Callable[[str], bool]) -> SentenceResult:
    output: List[str] = []
    records: List[str] = []
    for sentence in sentences:
        kept = keep(sentence)
        output += [sentence] if kept else []
        records.append(_record(sentence, sentence if kept else None))
    return output, records


def _strip_intent(sentences: List[str], params: Dict[str, Any]) -> SentenceResult:
    terms = list(params.get("duration_words", [])) + list(params.get("limit_words", []))
    numeric = re.compile(r"(?:\$\s*)?\d[\d,]*(?:\.\d+)?")
    return _filter(sentences, lambda sentence: bool(numeric.search(sentence)) or
                   _contains_term(sentence, terms))


def _reverse(sentences: List[str], params: Dict[str, Any]) -> SentenceResult:
    output = list(reversed(sentences))
    records = [_record(before, after) for before, after in zip(sentences, output)]
    return output, records


def _actor_names(sentence: str, actors: Sequence[str]) -> List[str]:
    candidates = []
    for actor in sorted(actors, key=len, reverse=True):
        candidates += [(match.start(), match.end(), actor)
                       for match in term_pattern(actor).finditer(sentence)]
    chosen: List[Tuple[int, int, str]] = []
    for start, end, actor in sorted(candidates, key=lambda item: (item[0], -item[1])):
        if not any(start < old_end and end > old_start for old_start, old_end, _ in chosen):
            chosen.append((start, end, actor))
    return [actor for _start, _end, actor in sorted(chosen)]


def _actors(sentences: List[str], params: Dict[str, Any]) -> SentenceResult:
    actors = [str(actor) for actor in params.get("actors", [])]
    output: List[str] = []
    records: List[str] = []
    for sentence in sentences:
        replacement = ", ".join(_actor_names(sentence, actors))
        output.append(replacement)
        records.append(_record(sentence, replacement))
    return output, records


def _sub_terms(text: str, terms: Sequence[str], replacement: str) -> str:
    result = text
    for term in sorted((str(value) for value in terms), key=len, reverse=True):
        result = term_pattern(term).sub(replacement, result)
    return result


def _tidy(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    return text.strip()


def _stocks_and_flows(sentences: List[str], params: Dict[str, Any]) -> SentenceResult:
    output: List[str] = []
    records: List[str] = []
    for sentence in sentences:
        changed = _sub_terms(sentence, params.get("adjectives", []), "")
        changed = _tidy(_sub_terms(changed, params.get("verbs", []), "→"))
        output.append(changed)
        records.append(_record(sentence, changed))
    return output, records


def _strip_preference(sentences: List[str], params: Dict[str, Any]) -> SentenceResult:
    markers = [str(item) for item in params.get(
        "markers", ["will not", "may not", "should", "must", "may"])]
    pattern = re.compile(r"\b(?:%s)\b" % "|".join(
        re.escape(item) for item in sorted(markers, key=len, reverse=True)), re.IGNORECASE)
    output: List[str] = []
    records: List[str] = []
    for sentence in sentences:
        match = pattern.search(sentence)
        changed = sentence if match is None else sentence[:match.start()].rstrip(" ,;:") + "."
        changed = _tidy(changed)
        output += [changed] if changed else []
        records.append(_record(sentence, changed if changed else None))
    return output, records


def _subtract(sentences: List[str], params: Dict[str, Any]) -> SentenceResult:
    creaturely = [str(term) for term in params.get("creaturely", [])]
    kept, _unused = _filter(sentences, lambda sentence: _contains_term(sentence, creaturely))
    output: List[str] = []
    for sentence in kept:
        output.append(_tidy(_sub_terms(sentence, params.get("remove", []), "")))
    by_sentence = iter(output)
    records = [_record(sentence, next(by_sentence) if _contains_term(sentence, creaturely)
                       else None) for sentence in sentences]
    return output, records


OPERATIONS: Dict[str, Callable[[List[str], Dict[str, Any]], SentenceResult]] = {
    "strip_intent_keep_limits": _strip_intent,
    "reverse_sentence_order": _reverse,
    "actors_only": _actors,
    "stocks_and_flows": _stocks_and_flows,
    "strip_stated_preference": _strip_preference,
    "subtract_to_core": _subtract,
}


def apply(brief_text: str, config: Dict[str, Any], persona: Optional[str]) -> PrepareResult:
    """Apply the configured operation for one of the six frozen personas."""
    personas = config.get("personas", {})
    if not persona or not isinstance(personas, dict) or persona not in personas:
        raise ValueError("transform requires a configured persona")
    entry = personas[persona]
    operation = entry.get("operation") if isinstance(entry, dict) else None
    if operation not in OPERATIONS:
        raise ValueError("unknown transform operation: %s" % operation)
    params = entry.get("params", {})
    if not isinstance(params, dict):
        raise ValueError("transform params must be an object")
    output, records = OPERATIONS[operation](_sentences(brief_text, config), params)
    return PrepareResult(visible="\n".join(output), record_lines=records)
