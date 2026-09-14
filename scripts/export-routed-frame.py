#!/usr/bin/env python3
"""Export E3's routed profile as the frozen evaluator artifact, without a receipt."""
import argparse
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.frame_audit import routed_artifact
from lib.paths import canonical_json, repo_root

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--route-receipt', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    root = repo_root()
    receipt = json.loads((root / args.route_receipt).read_text())
    artifact = routed_artifact(root, receipt)
    target = (root / args.out).resolve()
    target.relative_to(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as handle:
        handle.write(canonical_json(artifact) + '\n')
    print(target)
