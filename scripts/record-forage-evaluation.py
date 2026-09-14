#!/usr/bin/env python3
"""Record the host's independent evaluator invocation after a completed model call.

This is an orchestrator attestation, not proof of isolation. Commit all inputs and this
invocation, then make a later dispatch commit before invoking bin/forage-gate.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.forage_audit import CONTEXT_PURPOSES, EVALUATOR_BRIEF, parse_verdict
from lib.paths import canonical_json, repo_root, sha256_file


def main(kind='independent-forage-evaluation', evaluator_brief=EVALUATOR_BRIEF):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('manifest', 'response', 'brief', 'artifact', 'candidate', 'rubric', 'out', 'generator-actor'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--mode', choices=['development', 'official'], required=True)
    parser.add_argument('--attest-independent', action='store_true', required=True)
    args = parser.parse_args()
    root = repo_root()
    paths = {name: (root / getattr(args, name)).resolve() for name in ('brief', 'artifact', 'candidate', 'rubric')}
    relative = {name: path.relative_to(root).as_posix() for name, path in paths.items()}
    hashes = {relative[name]: sha256_file(path) for name, path in paths.items()}
    manifest = json.loads((root / args.manifest).read_text())
    packet = json.loads((root / args.response).read_text())
    expected = {str(path): hashes[relative[name]] for name, path in paths.items()}
    actual = {row['path']: row['sha256'] for row in manifest['context']}
    if len(manifest['context']) != 4 or actual != expected:
        raise ValueError('manifest does not match exactly the four frozen evaluator inputs')
    purposes = {str(paths[name]): purpose for name, purpose in CONTEXT_PURPOSES.items()}
    if any(row.get('purpose') != purposes[row['path']] for row in manifest['context']):
        raise ValueError('manifest purpose text differs from fixed evaluator instructions')
    request = manifest['delegation']
    if (request.get('output_mode') != 'critique' or request.get('acceptance_criteria') != []
            or request.get('constraints') != []):
        raise ValueError('manifest contains alternate or extra evaluator instructions')
    if manifest['delegation']['brief'] != evaluator_brief:
        raise ValueError('manifest does not use the frozen evaluator instruction')
    response = packet['receipt']
    if response['model'] != manifest['delegation']['model'] or response['finish_reason'] != 'stop' or response['truncated'] is not False:
        raise ValueError('model response is incomplete or uses a different model')
    parse_verdict(packet)
    evaluator = 'openrouter:' + response['request_id']
    if not args.generator_actor.strip() or args.generator_actor == evaluator:
        raise ValueError('generator actor must be disclosed and distinct from evaluator')
    value = {'schema_version': 1, 'kind': kind, 'mode': args.mode,
             'independent': True, 'generator_actor': args.generator_actor, 'evaluator_actor': evaluator,
             'context_root': str(root), 'files_read': hashes,
             'disclosure': 'Host attests a separate stateless request with only the four manifested task inputs. This is not cryptographic proof of the model context or semantic correctness.'}
    target = root / args.out
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as handle:
        handle.write(canonical_json(value) + '\n')
    print(target)


if __name__ == '__main__':
    main()
