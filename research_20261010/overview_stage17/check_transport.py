#!/usr/bin/env python3
"""Independent empty-root hydration check against final content-addressed transport."""
import sys;sys.dont_write_bytecode=True
from common import *
import argparse,subprocess,tempfile,stat
ap=argparse.ArgumentParser();ap.add_argument('--check-only',action='store_true');args=ap.parse_args()
p=ROOT/'reproducibility/stage11_exact_evidence/MANIFEST.json'
assert sha(p)=='8afcfc07988ec6f285b75555928e155b82f80378792d7811437b993a53d82d37'
x=json.loads(p.read_text());script=p.with_name('materialize.py')
with tempfile.TemporaryDirectory(prefix='stage12-hydration-') as t:
 result=json.loads(subprocess.check_output([sys.executable,str(script),'--repo-root',t],text=True))
 assert result['status']=='PASS' and result['restored_paths']==18 and result['unique_contents']==9
 verified=[]
 for obj in x['objects']:
  for target in obj['targets']:
   new=Path(t)/target['path'];old=ROOT/target['path']
   assert sha(new)==sha(old)==obj['raw_sha256']
   assert new.stat().st_size==old.stat().st_size==obj['raw_bytes']
   assert stat.S_IMODE(new.stat().st_mode)==int(target['mode'],8)
   verified.append(target['path'])
 second=json.loads(subprocess.check_output([sys.executable,str(script),'--repo-root',t],text=True))
 assert second['status']=='PASS' and second['restored_paths']==0
 report=dict(status='PASS',manifest_sha256=sha(p),materializer_sha256=sha(script),clean_restored_paths=len(verified),unique_contents=9,restored_original_bytes_and_modes=True,idempotent=True,verified_paths=verified)
 if not args.check_only:
  assert not (HERE/'MANIFEST_SHA256.json').exists()
  (HERE/'transport_reproducibility.json').write_text(json.dumps(report,indent=2)+'\n')
 else:
  assert report==json.loads((HERE/'transport_reproducibility.json').read_text())
 print(json.dumps({k:v for k,v in report.items() if k!='verified_paths'}))
