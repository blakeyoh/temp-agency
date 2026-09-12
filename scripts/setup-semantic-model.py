#!/usr/bin/env python3
"""Download only the committed semantic model files, checking every SHA-256."""
import argparse
import json
import os
import shutil
import sys
import urllib.request
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.paths import sha256_file  # noqa: E402
from lib.semantic import validate_manifest  # noqa: E402


def download(manifest, cache):
    validate_manifest(manifest)
    target = cache / manifest["revision"]
    for name, digest in manifest["files"].items():
        path = target / name
        if path.is_file() and sha256_file(path) == digest:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        url = "https://huggingface.co/%s/resolve/%s/%s" % (
            manifest["model_id"], manifest["revision"], name)
        temporary = path.with_name(path.name + ".download")
        try:
            with urllib.request.urlopen(url, timeout=120) as source, temporary.open("wb") as dest:
                shutil.copyfileobj(source, dest)
            if sha256_file(temporary) != digest:
                raise ValueError("download hash mismatch for %s" % name)
            temporary.replace(path)
        finally:
            if temporary.exists():
                temporary.unlink()
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--cache", type=Path, default=Path(os.environ.get(
        "HARNESS_MODEL_CACHE", str(Path.home() / ".cache/temp-agency/models"))))
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    print(download(manifest, args.cache.resolve()))


if __name__ == "__main__":
    main()
