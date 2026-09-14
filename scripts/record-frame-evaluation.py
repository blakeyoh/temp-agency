#!/usr/bin/env python3
"""Record an E3 evaluator invocation using the shared E2 attestation helper."""
import runpy
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.frame_audit import KIND, EVALUATOR_BRIEF

if __name__ == '__main__':
    helper = runpy.run_path(str(Path(__file__).with_name('record-forage-evaluation.py')))
    helper['main'](KIND, EVALUATOR_BRIEF)
