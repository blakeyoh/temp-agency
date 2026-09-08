"""The only receipt writer. See lib/README.md for the lifecycle.

Receipts are immutable once written. A one-shot nonce in
`docs/tournament/receipts/.nonce` gates `issue()`; it is a misuse guardrail,
not a security boundary (plan section 4).
"""
from __future__ import annotations

import json
import re
import secrets
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from lib.errors import ReceiptError
from lib.paths import canonical_json, receipts_dir, sha256_bytes

NONCE_FILE = ".nonce"
GENESIS = "genesis"
RECEIPT_NAME = re.compile(r"^(\d{3})-([0-9a-f]{12})\.json$")
ENTRANT_CODE = re.compile(r"^[A-Z][A-Z0-9]{0,7}$")
VERIFICATION_CLASSES = ("replay-exact", "hash-attested")
STATUSES = ("ok", "failed")
SEED_SOURCES = ("os-entropy", "argument", "none")

ISSUED_FIELDS = (
    "entrant", "tool", "tool_sha256", "repo_commit", "python_version",
    "argv", "inputs", "input_sha256", "seed", "output", "output_sha256",
    "verification_class", "external_attestation", "status", "error",
    "started_utc", "completed_utc",
)
CHAIN_FIELDS = ("receipt_id", "chain_prev", "chain_hash")
ALL_FIELDS = ISSUED_FIELDS + CHAIN_FIELDS


def mint_nonce(root: Path) -> str:
    """Write a fresh one-shot nonce and return it."""
    directory = receipts_dir(root)
    directory.mkdir(parents=True, exist_ok=True)
    nonce = secrets.token_hex(16)
    (directory / NONCE_FILE).write_text(nonce, encoding="utf-8")
    return nonce


def _consume_nonce(root: Path, nonce: str) -> None:
    nonce_path = receipts_dir(root) / NONCE_FILE
    message = "no live nonce: receipts are issued only by bin/ tools"
    if not nonce_path.is_file():
        raise ReceiptError(message)
    live = nonce_path.read_text(encoding="utf-8")
    nonce_path.unlink()
    if live != nonce:
        raise ReceiptError(message)


def _validate_fields(fields: Dict[str, Any]) -> None:
    missing = [key for key in ISSUED_FIELDS if key not in fields]
    extra = [key for key in fields if key not in ISSUED_FIELDS]
    if missing or extra:
        raise ReceiptError(f"receipt fields missing={missing} unexpected={extra}")
    if not ENTRANT_CODE.match(str(fields["entrant"])):
        raise ReceiptError(f"entrant must be an uppercase code, got {fields['entrant']!r}")
    if fields["verification_class"] not in VERIFICATION_CLASSES:
        raise ReceiptError(f"verification_class must be one of {VERIFICATION_CLASSES}")
    if fields["status"] not in STATUSES:
        raise ReceiptError(f"status must be one of {STATUSES}")
    seed = fields["seed"]
    if not isinstance(seed, dict) or seed.get("source") not in SEED_SOURCES:
        raise ReceiptError(f"seed must be a dict with source in {SEED_SOURCES}")
    attestation = fields["external_attestation"]
    if attestation is not None and not isinstance(attestation, dict):
        raise ReceiptError("external_attestation must be a dict or None")
    if not isinstance(fields["inputs"], dict) or not isinstance(fields["argv"], list):
        raise ReceiptError("inputs must be a dict and argv a list")


def _entrant_dir(root: Path, entrant: str) -> Path:
    return receipts_dir(root) / entrant


def _sequence_of(path: Path) -> int:
    match = RECEIPT_NAME.match(path.name)
    return int(match.group(1)) if match else -1


def list_receipts(root: Path, entrant: str) -> List[Path]:
    """Issued receipts for one entrant, ordered by sequence number."""
    directory = _entrant_dir(root, entrant)
    if not directory.is_dir():
        return []
    found = [p for p in directory.iterdir() if RECEIPT_NAME.match(p.name)]
    return sorted(found, key=_sequence_of)


def load(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ReceiptError(f"cannot load receipt {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ReceiptError(f"receipt {path} is not a JSON object")
    return data


def recompute_chain_hash(receipt: Dict[str, Any]) -> str:
    body = {k: v for k, v in receipt.items() if k != "chain_hash"}
    return sha256_bytes(canonical_json(body).encode("utf-8"))


def _chain_tail(root: Path, entrant: str) -> Tuple[int, str]:
    """Return (next sequence number, chain_prev) for a new receipt."""
    existing = list_receipts(root, entrant)
    if not existing:
        return 1, GENESIS
    last = existing[-1]
    prev = load(last)
    return _sequence_of(last) + 1, str(prev.get("chain_hash", ""))


def issue(root: Path, nonce: str, **fields: Any) -> Path:
    """Consume the live nonce and write one immutable receipt. Return its path."""
    _consume_nonce(root, nonce)
    _validate_fields(fields)
    entrant = str(fields["entrant"])
    sequence, chain_prev = _chain_tail(root, entrant)
    receipt_id = secrets.token_hex(6)
    body = {**fields, "receipt_id": receipt_id, "chain_prev": chain_prev}
    receipt = {**body, "chain_hash": recompute_chain_hash(body)}
    directory = _entrant_dir(root, entrant)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{sequence:03d}-{receipt_id}.json"
    text = json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    try:
        with open(path, "x", encoding="utf-8") as handle:
            handle.write(text)
    except FileExistsError as exc:
        raise ReceiptError(f"receipt {path} already exists; receipts are immutable") from exc
    return path


def _check_one(path: Path, receipt: Dict[str, Any], entrant: str,
               expected_prev: str) -> List[str]:
    problems: List[str] = []
    if receipt.get("entrant") != entrant:
        problems.append(f"{path.name}: entrant {receipt.get('entrant')} filed under {entrant}")
    name_id = RECEIPT_NAME.match(path.name).group(2)
    if receipt.get("receipt_id") != name_id:
        problems.append(f"{path.name}: receipt_id {receipt.get('receipt_id')} != filename id {name_id}")
    if receipt.get("chain_hash") != recompute_chain_hash(receipt):
        problems.append(f"{path.name}: chain_hash does not recompute (receipt edited)")
    if receipt.get("chain_prev") != expected_prev:
        problems.append(f"{path.name}: chain_prev {receipt.get('chain_prev')} != expected {expected_prev}")
    return problems


def verify_chain(root: Path, entrant: str) -> List[str]:
    """Return a list of chain problems for one entrant; empty means intact."""
    problems: List[str] = []
    expected_prev: Optional[str] = GENESIS
    for index, path in enumerate(list_receipts(root, entrant), start=1):
        if _sequence_of(path) != index:
            problems.append(f"{path.name}: sequence gap, expected {index:03d}")
        try:
            receipt = load(path)
        except ReceiptError as exc:
            problems.append(str(exc))
            expected_prev = None
            continue
        problems.extend(_check_one(path, receipt, entrant, expected_prev or ""))
        expected_prev = str(receipt.get("chain_hash", ""))
    return problems
