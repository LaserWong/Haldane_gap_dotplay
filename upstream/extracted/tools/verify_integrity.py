#!/usr/bin/env python3
"""Read-only SHA-256 and size verification against the final package manifest."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / "MANIFEST_SHA256.json").read_text())
    failures = []
    for row in manifest["files"]:
        p = ROOT / row["path"]
        if not p.is_file():
            failures.append({"path": row["path"], "reason": "missing"})
        elif p.stat().st_size != row["bytes"] or hashlib.sha256(p.read_bytes()).hexdigest() != row["sha256"]:
            failures.append({"path": row["path"], "reason": "content mismatch"})
    print(json.dumps({"status": "PASS" if not failures else "FAIL",
                      "files_checked": len(manifest["files"]), "failures": failures}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
