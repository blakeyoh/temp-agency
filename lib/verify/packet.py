"""Packet admission: required tools plus a freshly executed complete receipt gate."""
import json
import os
import re
from pathlib import Path

from lib.bindings import cited_receipt_ids
from lib.paths import relative_to_root, receipts_dir, git_output
from lib.receipt import list_receipts, load
from lib.tools import require_clean
from lib.verify.gate import run_gate

REQUIRED = {
    'E1': {'draw'}, 'E2': {'draw', 'forage', 'forage-gate'},
    'E3': {'route', 'frame-gate'}, 'E4': {'breed'}, 'E5': {'lexicon-check'},
    'E6': {'oblique'}, 'E9': {'seed-string'},
    'A1': {'prepare'}, 'A3': {'churn','seasons','units','orders'}, 'A5': {'prepare'},
    'C5': {'notation'}, 'C8': {'prepare'}, 'M1': {'seal-median','overlap'},
}
PROMISE = {'A2','M5'}
STATUS = re.compile(r'^- \*\*Enactment status:\*\*\s*`?(FAITHFUL|PARTIAL|NOT ENACTED|PROMISE ONLY)`?\s*$', re.M)


def validate_sources(root, records, runs, dispatch_log):
    root = Path(root).resolve()
    directory = receipts_dir(root)
    receipt_paths = [p for entrant in directory.iterdir() if entrant.is_dir()
                     for p in list_receipts(root, entrant.name)] if directory.exists() else []
    known = {}
    for path in receipt_paths:
        row = load(path)
        if row['receipt_id'] in known:
            raise ValueError('duplicate receipt identity')
        known[row['receipt_id']] = row
    paths = [relative_to_root(root, record['path']) for record in records.values()]
    require_clean(root, paths + [dispatch_log])
    log = json.loads((root / dispatch_log).read_text())
    entries = log.get('entries', [])
    for code, record in records.items():
        if Path(record['path']).read_text() != record['text']:
            raise ValueError(code + ': source differs from committed file')
        states = STATUS.findall(record['text'])
        if len(states) != 1:
            raise ValueError(code + ': requires exactly one explicit enactment status')
        ids = cited_receipt_ids(record['text'])
        if code in PROMISE:
            if states[0] != 'PROMISE ONLY' or ids or not re.search(r'^- \*\*Pass 1 provenance:\*\* baseline\s*$', record['text'], re.M):
                raise ValueError(code + ': unavailable mechanism requires explicit receipt-free baseline')
            continue
        if code not in REQUIRED:
            raise ValueError(code + ': no approved implemented admission policy; resolve deferred entrant first')
        if not ids or any(rid not in known for rid in ids):
            raise ValueError(code + ': every non-PROMISE record requires real receipt IDs')
        receipts = [known[rid] for rid in ids]
        if any(row['entrant'] != code or row['tool'] not in REQUIRED[code] for row in receipts):
            raise ValueError(code + ': receipt entrant or tool differs from admission policy')
        if states[0] == 'NOT ENACTED':
            if not any(row['status'] == 'failed' for row in receipts):
                raise ValueError(code + ': NOT ENACTED requires a real failed-tool receipt')
        elif states[0] in ('FAITHFUL','PARTIAL'):
            if {row['tool'] for row in receipts if row['status'] == 'ok'} != REQUIRED[code]:
                raise ValueError(code + ': required mechanism tools are missing')
            if code == 'E1' and len([r for r in receipts if r['status'] == 'ok']) < 2:
                raise ValueError('E1: primary and counterfactual draw receipts are required')
            if code == 'C5' and {json.loads(r['output']).get('mode') for r in receipts if r['status']=='ok'} != {'select','validate'}:
                raise ValueError('C5: both notation selection and artifact validation are required')
        else:
            raise ValueError(code + ': PROMISE ONLY is not permitted for an implemented entrant')
        for row in receipts:
            # Deterministic tools still need their exact inputs precommitted in the dispatch log.
            seed = row['seed']
            value = seed['value']
            if seed['source'] not in ('argument','none'):
                raise ValueError(code + ': official receipt has an uncommitted entropy seed')
            def matches(entry):
                return (entry.get('entrant') == code and entry.get('seed') == value
                        and entry.get('inputs') == row['inputs'])
            if not any(matches(entry) for entry in entries):
                raise ValueError(code + ': invocation inputs/seed absent from dispatch log')
            try:
                historical = json.loads(git_output(root, 'show', row['repo_commit'] + ':' + dispatch_log))
            except Exception as exc:
                raise ValueError(code + ': dispatch log did not exist at invocation') from exc
            if not any(matches(entry) for entry in historical.get('entries', [])):
                raise ValueError(code + ': dispatch entry was added after invocation')
    # Existing bindings resolve repo_root from cwd. Keep that root consistent for this synchronous gate.
    previous = Path.cwd()
    try:
        os.chdir(root)
        report = run_gate(root, relative_to_root(root, runs) + '/s16-*.md')
    finally:
        os.chdir(previous)
    if not report.passed:
        raise ValueError('receipt gate rejected packet sources:\n' + '\n'.join(line.message for line in report.lines if line.level=='FAIL'))
    cited = {rid for record in records.values() for rid in cited_receipt_ids(record['text'])}
    if cited != set(known):
        raise ValueError('all receipt evidence must belong to the current draw records')
    return report
