"""Verify frozen new inputs and independently reviewed prerequisites by SHA-256."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check_hashes():
 for p,h in json.loads((HERE/'INPUT_SHA256.json').read_text()).items():assert sha(HERE/'snapshot'/p)==h,p
 for name,rec in json.loads((HERE/'PRIOR_REVIEW_SHA256.json').read_text()).items():
  prior=ROOT/name;assert sha(prior/'MANIFEST_SHA256.json')==rec['manifest_sha256'],name
  for p,h in rec['files'].items():assert sha(prior/p)==h,(name,p)
 manifest=HERE/'snapshot/low_band/frontier_g007_g010/FROZEN_MANIFEST_1845.json'
 assert sha(manifest)=='55b0ddf8e317c6953d0487a26880b075231d7fcc37c5a91a475a83b5a71dcb47'
 for p,h in json.loads(manifest.read_text())['files'].items():assert sha(manifest.parent/p)==h,p
 for p,h in json.loads((manifest.parent/'geometry_source_sha256.json').read_text()).items():
  assert sha(ROOT/'large_seed_review/snapshot/research_20261010'/p)==h,p
 print('NEW INPUTS AND PRIOR SEALED SOURCES PASS',flush=True)
if __name__=='__main__':check_hashes()
