"""Bounded exact replay; preserve historical outputs and verify inputs before imports."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo-root', type=Path, default=HERE.parents[2],
                    help='Defaults to repository root inferred from this file location')
parser.add_argument('--output-dir', type=Path,
                    help='New output directory; must not already exist')
args = parser.parse_args()
BASE = args.repo_root.resolve()
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
OUT = (args.output_dir or HERE / ('rerun_' + stamp)).resolve()
if sys.flags.optimize:
    raise SystemExit('Do not use python -O: the historical verifiers require assertions.')
inputs = json.loads((HERE / 'input_hashes.json').read_text())
for row in inputs:
    path = BASE / row['path']
    if not path.is_file():
        raise SystemExit('Missing required input: ' + row['path'])
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != row['sha256']:
        raise SystemExit('Input changed since recorded audit: ' + row['path'])
OUT.mkdir(parents=True, exist_ok=False)
sys.dont_write_bytecode = True
sys.path.insert(0, str(BASE / 'audit/independent'))
import verify_baseline as vb
import verify_ground_only as vg
vb.OUT = OUT
vg.OUT = OUT
start = time.monotonic()
vb.main()
vg.check(BASE / 'low_energy/certificate_s1_W1_g1d20_k0.json')
report = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'PASS', 'python': sys.version, 'platform': platform.platform(),
    'seconds': time.monotonic() - start, 'verified_input_count': len(inputs),
    'repo_root': str(BASE), 'output_dir': str(OUT),
    'scope': 'Fresh replay of existing exact arithmetic certificates; not a new theorem or full-project replay.'
}
(OUT / 'run_environment.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
